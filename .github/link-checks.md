# 외부 링크 검사 실패의 원인과 처리

2026-11-18 KST에 이슈 #40을 로컬 macOS와 사용자 fork의 GitHub Actions에서 비교했다. 실패 원인은 하나가 아니었다. 브라우저에서 열리거나 HTTP 200을 받는 것만으로 링크가 정상이라고 판단할 수 없고, CI의 모든 실패를 IP 차단으로 설명할 수도 없다.

## 확인한 원인

| 대상 | 재현 결과 | 처리 |
| --- | --- | --- |
| 나무위키 | 기존 자동 검사에서 challenge 403. 대체 한국어 위키백과 3개는 GET 200 | 링크 교체, 나무위키 검사 예외 삭제 |
| Warpspeed | 로컬의 200 응답도 제품 문서가 아니라 `/lander`로 이동하는 주차 페이지. Ubuntu에서는 TLS 연결 종료 | 제작자가 공개한 `kallsyms/warpspeed` 저장소로 교체 |
| command-not-found.com | 로컬·CI 모두 최종적으로 개인 Linktree로 이동 | tldr 설명은 공식 설치 안내로, 일반 설명은 해당 도구의 공식 문서·패키지 관리자를 안내하도록 수정 |
| OpenUserJS | 로컬 및 Ubuntu 두 대에서 비압축 GET 6회 모두 130,821바이트 뒤 시간 초과. 압축 GET 6회는 모두 완료 | 검사기의 HTTP 압축·자동 압축 해제를 활성화 |
| Fandom | 일반 요청에 `cf-mitigated: challenge`와 403. Chrome 형식 요청도 CI에서는 실패 | 기존 `vim.fandom.com` 한정 예외 유지 |
| Velog의 SemVer 설명 | 두 검사기와 curl 모두 CI에서 504 또는 시간 초과. curl 응답의 서버는 `awselb/2.0` | 해당 글도 참고하는 공식 한국어 SemVer 명세로 교체 |
| MIT | 실행에 따라 성공과 시간 초과가 바뀜. 같은 runner의 대조에서 성공도 확인 | 일괄 제외하지 않고 기존 검사를 유지 |
| Fosstodon의 강의 소개 게시물 | Masto.host의 403 본문이 네트워크·브라우저 요청량에 따른 비로그인 접근 제한을 명시. 실제 게시물 본문은 로컬과 CI 대조에서 확인 | 해당 게시물 URL 하나만 검사 예외로 기록 |

Warpspeed는 동일 IPv4 목적지 고정, HTTP/1.1, TLS 1.2, OpenSSL/BoringSSL 및 호스트/컨테이너 비교에서도 CI 실패가 유지됐다. 따라서 CI 경로에 의존하는 TLS 종료는 확인했지만, 서버 내부의 정확한 IP 차단 규칙까지 확인한 것은 아니다. 이미 주차 도메인이므로 정상 페이지로 연결하는 것이 수정의 목적이다.

MIT의 과거 시간 초과는 이번 대조에서 재현되지 않은 경우도 있었다. 이전 장애의 원인이나 영구 해결을 확정하지 않는다. Fandom의 challenge 응답 또한 모든 403 응답의 공통 원인이라는 뜻은 아니다.

## 압축 설정이 필요한 이유

OpenUserJS에서는 HTTP 상태가 먼저 200으로 도착해도 본문 전송이 끝나지 않았다. 비압축·압축·압축·비압축 순서로 요청하고 같은 호스트 요청 사이에 15초를 두어, 짧은 요청 간격이나 순서에 따른 영향을 줄였다. 압축 요청은 약 0.16–1.19초에 완료됐다. 서버 내부의 결함까지 확인한 것은 아니지만 압축 여부와 전송 완료의 차이는 세 환경에서 반복됐다.

HTMLProofer 5.2.1로 실제 페이지의 `#footer`를 검사했을 때도 비압축 응답은 시간 초과 후 앵커 누락으로 보고됐고, 압축을 켜면 통과했다. 일부러 없는 앵커를 지정하면 압축을 켜도 실패했다. 즉 오류를 무시해서 얻은 성공이 아니다.

`accept_encoding: ""`는 libcurl이 지원하는 압축 형식을 요청하고 응답을 자동으로 해제하는 공식 옵션이다. `Accept-Encoding` 헤더만 넣는 것과 다르다. 현재 `proof-html` Action에는 이 옵션을 전달하는 입력이 없어, 같은 HTMLProofer 이미지와 공개 Ruby API를 사용하는 작은 실행 파일로 외부 검사를 구성한다.

## 변경 범위

- Build의 HTML·내부 링크 검사는 그대로 유지한다.
- 외부 검사도 HTMLProofer 5.2.1을 유지한다. 링크, 이미지, 스크립트, OpenGraph, favicon 및 외부 앵커 검사를 보존한다.
- 기존 URL 예외·정규식·자체 사이트 주소 변환·GitHub 앵커 변환을 설정 파일로 옮긴다. 나무위키 예외를 제거하고, 접근 제한과 본문을 확인한 Fosstodon 게시물 URL 하나만 추가한다.
- GitHub 토큰은 HTTPS의 `github.com` 요청에만 추가한다.
- 요청 제한 120초·연결 제한 30초는 유지하고, 동시 요청은 50개에서 10개로 줄인다. 총 3회 검사하며 실패 후 15초·30초를 기다린다. 성공 URL 캐시는 재시도 사이에 유지한다.
- 403·429·5xx를 전체적으로 성공 처리하지 않는다. 최종 실패는 CI 실패로 남고 로그를 artifact로 보존한다.

Lychee도 압축 페이지와 404·없는 앵커 대조를 통과했지만 최종안으로 채택하지 않았다. 같은 runner에서 기본 User-Agent로 Naver가 403, 기존 User-Agent로 200을 반환했다. 또한 HTML 추출 규칙이 기존 스크립트·OpenGraph 검사와 달라, 압축 문제를 해결하기 위해 바꾸는 동작 범위가 더 컸다.

Fosstodon에서는 같은 이미지로 기본 요청, Accept 변경, 새 브라우저 User-Agent, 도구 User-Agent, HTTP/1.1, 기본 요청 재실행을 비교했다. 다른 요청이 통과한 뒤 기본 요청도 CDN 캐시를 통해 통과했다. 순서와 캐시 효과를 분리하지 못했으므로 특정 User-Agent나 HTTP 버전이 영구 해결책이라고 주장하지 않는다. 게시물의 존재와 접근 제한 안내를 확인한 정확한 URL만 예외로 남긴다.

## 일반적으로 적용할 기준

자동 검사와 브라우저 결과가 다르면 같은 URL·클라이언트·목적지 IP를 가능한 한 맞추고, DNS/TCP/TLS/HTTP 상태/본문 완료 중 어디에서 실패하는지 먼저 확인한다. 실패를 구분한 뒤 정상 주소로 교체할지, 요청 설정을 바꿀지, 접근 제한이 확인된 URL만 예외로 둘지 결정한다.

200 응답이나 리다이렉트 성공은 원래 내용이 남아 있다는 보장이 아니다. 링크를 수정할 때 최종 목적지와 본문도 확인한다. 반대로 실제 서버 오류를 CI에서 없애기 위해 광범위한 상태 코드 예외를 추가하지 않는다.

## 검증 근거

- [로컬과 독립 Ubuntu runner 두 대의 비교](https://github.com/YangSiJun528/missing-semester-kr.github.io/actions/runs/44112849883): Linux 결과는 수집 완료. 대기 중이던 macOS job은 취소했으며 macOS CI 결과로 계산하지 않았다.
- [HTMLProofer 압축 및 없는 앵커 대조](https://github.com/YangSiJun528/missing-semester-kr.github.io/actions/runs/44114609776): 성공.
- [Lychee의 압축·404·없는 앵커 대조](https://github.com/YangSiJun528/missing-semester-kr.github.io/actions/runs/44115099346): 성공.
- [동일 runner에서 curl·검사기·User-Agent 비교](https://github.com/YangSiJun528/missing-semester-kr.github.io/actions/runs/44116228635).
- [같은 HTMLProofer 이미지에서 Fosstodon 요청 조건 비교](https://github.com/YangSiJun528/missing-semester-kr.github.io/actions/runs/44119247391): 두 runner에서 접근 제한 안내와 실제 게시물 본문을 확인했다.
- [기존 검사기의 전체 사이트 결과](https://github.com/YangSiJun528/missing-semester-kr.github.io/actions/runs/44113810736), [Lychee 후보의 전체 사이트 결과](https://github.com/YangSiJun528/missing-semester-kr.github.io/actions/runs/44114611481): 모두 실패했으며 실패 목록을 비교해 최종 구성을 결정했다.
- [HTMLProofer 공식 옵션](https://github.com/gjtorikian/html-proofer/blob/v5.2.1/README.md#configuring-typhoeus-and-hydra), [libcurl 압축 옵션](https://curl.se/libcurl/c/CURLOPT_ACCEPT_ENCODING.html).
- [Warpspeed 제작자 설명](https://nickgregory.me/post/2024/06/23/warpspeed/), [공식 한국어 SemVer 명세](https://semver.org/lang/ko/).
