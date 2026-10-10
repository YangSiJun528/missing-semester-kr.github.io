---
layout: lecture
title: "보안과 개인정보 보호"
lang: ko
presenter: Jon
date: 2019-01-31
order: 2
video:
  aspect: 56.25
  id: OBx_c-i-M8s
special: true
---

세상은 무서운 곳이고, 모두가 여러분을 노리고 있습니다.

물론 꼭 그렇지는 않겠지만, 그렇다고 모든 비밀을 드러내고 싶지는 않을 것입니다. 보안과 개인정보 보호의 핵심은 공격자가 넘어야 할 문턱을 높이는 데 있습니다. 자신의 위협 모델을 파악하고 거기에 맞춰 보호 수단을 설계하세요. 상대가 NSA나 모사드라면 꽤 어려운 싸움이 될 것입니다.

디지털 환경에서 자신을 더 안전하게 지키는 방법은 많습니다. 여기서는 여러 주제의 큰 틀을 살펴봅니다. 보안은 계속 관리해야 하는 과정이며, 스스로 배우는 것이 가장 좋은 방법 중 하나입니다.

## 보안을 잘 아는 사람들의 글 읽기
{: #follow-the-right-people}

보안 지식을 늘리는 좋은 방법은 보안에 관해 활발히 이야기하는 사람들을 꾸준히 지켜보는 것입니다. 다음 계정을 추천합니다.

- [@TroyHunt](https://twitter.com/TroyHunt)
- [@SwiftOnSecurity](https://twitter.com/SwiftOnSecurity)
- [@taviso](https://twitter.com/taviso)
- [@thegrugq](https://twitter.com/thegrugq)
- [@tqbf](https://twitter.com/tqbf)
- [@mattblaze](https://twitter.com/mattblaze)
- [@moxie](https://twitter.com/moxie)

[이 목록](https://heimdalsecurity.com/blog/best-twitter-cybersec-accounts/)에서도 다른 계정을 찾아볼 수 있습니다.

## 일반적인 보안 조언
{: #general-security-advice}

Tech Solidarity의 [언론인을 위한 보안 수칙](https://web.archive.org/web/20221123204419/https://techsolidarity.org/resources/basic_security.htm)은 유용한 조언을 많이 담고 있으며 비교적 최신인 자료입니다. [@thegrugq](https://medium.com/@thegrugq)의 [여행 중 보안에 관한 글](https://medium.com/@thegrugq/stop-fabricating-travel-security-advice-35259bf0e869)도 읽어볼 만합니다. 여기서는 이 자료들의 조언을 상당 부분 다시 다루고 몇 가지를 더 보탭니다. [USB를 이용한 공격](https://www.bleepingcomputer.com/news/security/heres-a-list-of-29-different-types-of-usb-attacks/)에 대비해 [USB 데이터 차단기](https://www.amazon.com/dp/B00QRRZ2QM/)도 마련하세요.

## 인증
{: #authentication}

아직 비밀번호 관리자를 쓰지 않는다면 먼저 설치하세요. 다음 도구를 추천합니다.

- [1Password](https://1password.com/)
- [KeePass](https://keepass.info/)
- [Bitwarden](https://bitwarden.com/)
- [`pass`](https://git.zx2c4.com/password-store/about/)

보안을 특히 중요하게 생각한다면 서버에 평문으로 저장하는 방식이 아니라, 자신의 컴퓨터에서 비밀번호를 암호화하는 도구를 사용하세요. 중요한 웹사이트의 비밀번호를 비밀번호 관리자로 생성하세요. 그런 다음 2단계 인증을 켜세요. 가능하면 [FIDO/U2F](https://fidoalliance.org/) 보안 키를 사용하세요. 예를 들어 [YubiKey](https://www.yubico.com/quiz/)는 [학생에게 20% 할인](https://www.yubico.com/why-yubico/for-education/)을 제공합니다. Google Authenticator나 Duo 같은 TOTP 방식도 대안이지만 [피싱을 막지는 못합니다](https://twitter.com/taviso/status/1082015009348104192). SMS는 위협 모델이 제삼자가 전송 중인 비밀번호를 가로채는 상황으로 한정되지 않는 한 사실상 쓸모가 없습니다.

종이에 보관하는 복구 키도 생각해볼 필요가 있습니다. 많은 서비스가 주 인증 수단을 잃어버렸을 때 두 번째 인증 요소로 쓸 수 있는 "백업 키"를 제공합니다. 여분의 보안 키도 안전한 장소에 보관하세요. 복구 키를 비밀번호 관리자에 넣을 *수는* 있지만, 누군가 관리자에 접근하면 비밀번호와 복구 수단을 모두 얻게 됩니다. 자신의 위협 모델에서 이 위험을 감수할 수 있는지 판단하세요. 더 엄격하게 분리하려면 복구 키를 출력하고 디지털 사본은 보관하지 않은 채 실제 금고에 넣을 수 있습니다.

## 비공개 통신
{: #private-communication}

[Signal](https://www.signal.org/)을 사용하세요([설정 안내](https://medium.com/@mshelton/signal-for-beginners-c6b44f76a1f0)). [Wire](https://wire.com/en/)도 [괜찮은 선택](https://www.securemessagingapps.com/)이고, WhatsApp도 사용할 만합니다. [Telegram은 사용하지 마세요](https://twitter.com/bascule/status/897187286554628096). 데스크톱 메신저에는 문제가 많습니다. 많은 프로그램이 Electron에 의존하여 신뢰해야 할 소프트웨어 계층이 크다는 점도 그 이유 중 하나입니다.

이메일은 PGP 서명을 사용하더라도 특히 까다롭습니다. 일반적으로 전방향 안전성(forward secrecy)을 제공하지 않고, 키 배포 문제도 큽니다. [keybase.io](https://keybase.io/)가 키 배포에 도움이 되며 다른 용도로도 유용합니다. 또한 PGP 키는 대개 데스크톱 컴퓨터에서 다루는데, 이는 보안상 가장 취약한 컴퓨팅 환경 중 하나입니다. 이런 맥락에서 Chromebook을 쓰거나 태블릿에 키보드를 연결해 작업하는 방법도 고려하세요.

## 파일 보안
{: #file-security}

파일 보안은 어렵고 여러 계층에 걸쳐 있습니다. 먼저 무엇으로부터 보호하려는지 생각해야 합니다.

[![5달러짜리 렌치](https://imgs.xkcd.com/comics/security.png)](https://xkcd.com/538/)

- **오프라인 공격**: 컴퓨터가 꺼져 있을 때 누군가 노트북을 훔치는 상황입니다. 전체 디스크 암호화를 켜세요. Linux에서는 [cryptsetup과 LUKS](https://wiki.archlinux.org/index.php/Dm-crypt/Encrypting_a_non-root_file_system), Windows에서는 [BitLocker](https://fossbytes.com/enable-full-disk-encryption-windows-10/), macOS에서는 [FileVault](https://support.apple.com/en-us/HT204837)를 사용할 수 있습니다. 다만 공격자가 여러분까지 붙잡고 비밀을 내놓으라고 강요하는 상황에는 도움이 되지 않습니다.
- **온라인 공격**: 컴퓨터가 켜진 상태로 다른 사람의 손에 들어가는 상황입니다. 파일 암호화를 사용하세요. 크게 두 가지 방식이 있습니다.
  - **암호화된 파일 시스템**: 기존 파일 시스템 위에 암호화 계층을 두는 방식은 블록 장치 전체 대신 파일을 개별적으로 암호화합니다. 복호화 키를 제공해 "마운트"하면 안의 파일을 자유롭게 탐색할 수 있고, 마운트를 해제하면 다시 접근할 수 없게 됩니다. [gocryptfs](https://github.com/rfjakob/gocryptfs)와 [eCryptFS](https://www.ecryptfs.org/)가 예입니다. [gocryptfs 비교 자료](https://nuetzlich.net/gocryptfs/comparison/)와 [Arch Wiki 비교표](https://wiki.archlinux.org/index.php/disk_encryption#Comparison_table)도 참고하세요.
  - **암호화된 파일**: 비밀 키와 대칭 암호로 개별 파일을 암호화합니다(`gpg -c` 참고). 또는 `pass`처럼 그 키를 공개 키로도 암호화하여 나중에 자신의 개인 키로만 읽을 수 있게 합니다. 구체적인 암호화 설정이 매우 중요합니다.
- **[그럴듯한 부인 가능성](https://en.wikipedia.org/wiki/Plausible_deniability)**: 비밀 데이터의 존재를 부인할 여지를 두는 방식입니다. 일반적으로 성능이 낮아지고 데이터를 잃기도 쉽습니다. 실제로 [부인 가능한 암호화](https://en.wikipedia.org/wiki/Deniable_encryption)를 제공하는지 입증하기도 어렵습니다. [관련 논의](https://security.stackexchange.com/questions/135846/is-plausible-deniability-actually-feasible-for-encrypted-volumes-disks)를 읽고, TrueCrypt를 이어받아 유지보수하는 포크인 [VeraCrypt](https://www.veracrypt.fr/en/Home.html)를 사용해볼지 판단하세요.
- **암호화된 백업**: [Tarsnap](https://www.tarsnap.com/)이나 [BorgBase](https://www.borgbase.com/)를 사용할 수 있습니다.
  - 공격자가 노트북을 손에 넣었을 때 백업까지 지울 수 있는지도 생각해보세요.

## 인터넷 보안과 개인정보 보호
{: #internet-security--privacy}

인터넷은 위험할 수 있습니다. 개방형 Wi-Fi 네트워크도 [위험 요소가](https://www.troyhunt.com/the-beginners-guide-to-breaking-website/) [있습니다](https://www.troyhunt.com/talking-with-scott-hanselman-on/). 사용한 뒤에는 저장된 네트워크를 삭제하세요. 그렇지 않으면 휴대전화가 그 네트워크를 찾는 신호를 보내거나, 나중에 이름이 같은 네트워크에 다시 연결할 수 있습니다.

신뢰할 수 없는 네트워크에서는 VPN이 유용할 *수* 있습니다. 다만 VPN 제공업체를 상당히 많이 신뢰하게 된다는 점을 기억하세요. 인터넷 서비스 제공업체보다 더 믿을 수 있나요? VPN이 꼭 필요하다면 신뢰할 수 있는 제공업체를 고르고 유료 서비스를 고려하세요. 직접 [WireGuard](https://www.wireguard.com/)를 설정하는 방법도 있습니다. [훌륭한 도구입니다](https://web.archive.org/web/20210526211307/https://latacora.micro.blog/there-will-be/)!

[cipherlist.eu](https://cipherlist.eu/)에는 여러 인터넷 애플리케이션의 보안 설정이 있습니다. 개인정보 보호에 관심이 많다면 [privacytools.io](https://privacytools.io)도 참고할 만합니다.

[Tor](https://www.torproject.org/)가 궁금할 수도 있습니다. Tor는 전 세계의 트래픽을 관찰할 수 있는 강력한 공격자나 트래픽 분석 공격에 특히 강하지 않습니다. 제한된 범위에서 트래픽을 숨기는 데 도움이 될 수 있지만, 개인정보 보호 측면에서 큰 이점을 주지는 않습니다. 처음부터 Signal이나 TLS와 인증서 고정(certificate pinning)처럼 더 안전한 서비스를 사용하는 편이 낫습니다.

## 웹 보안
{: #web-security}

웹도 사용하고 싶다고요? 위험을 하나 더 감수하게 되는 셈입니다.

[HTTPS Everywhere](https://www.eff.org/https-everywhere)를 설치하세요. SSL/TLS가 [중요한 이유](https://www.troyhunt.com/ssl-is-not-about-encryption/)는 암호화뿐만이 아닙니다. 애초에 올바른 서비스와 통신하고 있는지 검증하는 역할도 합니다. 웹 서버를 운영한다면 [TLS 설정을 검사](https://www.ssllabs.com/ssltest/index.html)해보세요. [설정이 복잡해질 수 있습니다](https://wiki.mozilla.org/Security/Server_Side_TLS). HTTPS Everywhere는 대안이 있으면 HTTP 대신 HTTPS로 접속하도록 최대한 돕습니다. 모든 문제를 해결하지는 못해도 도움이 됩니다. 보안을 특히 중요하게 생각한다면 꼭 필요하지 않은 SSL/TLS 인증 기관(CA)을 차단하세요.

[uBlock Origin](https://github.com/gorhill/uBlock)을 설치하세요. 광고만 막는 것이 아니라, 페이지가 시도하는 각종 제삼자 통신과 인라인 스크립트 등을 차단하는 [범용 차단기](https://github.com/gorhill/uBlock/wiki/Blocking-mode)입니다. 사이트가 작동하도록 설정을 조정하는 데 시간을 들일 수 있다면 [미디엄 모드](https://github.com/gorhill/uBlock/wiki/Blocking-mode:-medium-mode)나 [하드 모드](https://github.com/gorhill/uBlock/wiki/Blocking-mode:-hard-mode)를 사용할 수 있습니다. 설정을 충분히 조정하기 전에는 일부 사이트가 작동하지 않을 수 있지만, 온라인 보안을 강화할 수 있습니다.

Firefox를 사용한다면 [Multi-Account Containers](https://support.mozilla.org/en-US/kb/containers)를 켜세요. 소셜 네트워크, 은행, 쇼핑 등을 위한 컨테이너를 각각 만들 수 있습니다. Firefox가 컨테이너별 쿠키와 상태를 분리하므로, 한 컨테이너에서 방문한 사이트가 다른 컨테이너의 정보를 엿보지 못하게 할 수 있습니다. Google Chrome에서는 [프로필](https://support.google.com/chrome/answer/2364824)로 비슷하게 분리할 수 있습니다.

## 연습 문제
{: #exercises}

1. PGP로 파일을 암호화하세요.
1. VeraCrypt로 간단한 암호화 볼륨을 만드세요.
1. Gmail, Dropbox, GitHub 등 민감한 데이터가 많은 계정에 2단계 인증을 설정하세요.
