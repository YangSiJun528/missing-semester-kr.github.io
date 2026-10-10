---
layout: lecture
title: "코드 품질"
description: >
  서식 지정, 린트, 테스트, 지속적 통합 등 코드 품질을 높이는 기법을 배웁니다.
thumbnail: /static/assets/thumbnails/2026/lec9.png
date: 2026-01-23
ready: true
video:
  aspect: 56.25
  id: XBiLUNx84CQ
---

개발자가 좋은 코드를 쓰도록 돕는 도구와 기법은 다양합니다. 이번 강의에서는 다음을 다룹니다.

- [서식 지정](#formatting)
- [린트](#linting)
- [테스트](#testing)
- [커밋 전 훅](#pre-commit-hooks)
- [지속적 통합](#continuous-integration)
- [명령 실행 도구](#command-runners)

추가로 [정규 표현식](#regular-expressions)도 다룹니다. 패턴에 맞는 테스트만 실행하는 코드 품질 작업부터 IDE의 검색·치환까지 여러 분야에서 쓰이는 주제입니다.

많은 도구는 Python의 [Ruff](https://docs.astral.sh/ruff/)처럼 언어별로 제공되고, [Prettier](https://prettier.io/)처럼 여러 언어를 지원하기도 합니다. 하지만 개념은 거의 공통적입니다. 어떤 언어든 포매터, 린터, 테스트 라이브러리 등을 찾을 수 있습니다.

# 서식 지정
{: #formatting}

자동 포매터는 코드의 표면적인 형태를 정리합니다. 문자열의 `'`와 `"` 통일, `x+y` 대신 `x + y`처럼 연산자 주변 공백, 임포트 정렬, 긴 줄 나누기 등을 맡겨 개발자는 더 어려운 문제에 집중할 수 있습니다. 같은 코드베이스에서 일하는 개발자들의 스타일을 통일한다는 것도 큰 장점입니다.

Prettier처럼 [다양한 설정](https://prettier.io/docs/configuration)을 제공하는 도구는 설정 파일을 프로젝트의 [버전 관리](/2026/version-control/)에 포함하세요. [Black](https://github.com/psf/black), [gofmt](https://pkg.go.dev/cmd/gofmt)는 사소한 형식 논쟁인 [바이크셰딩](https://en.wikipedia.org/wiki/Law_of_triviality)을 줄이려고 설정을 제한하거나 제공하지 않습니다.

[IDE 통합](/2026/development-environment/#code-intelligence-and-language-servers)으로 입력 중이나 저장 시 자동 정리하게 할 수 있습니다. [EditorConfig](https://editorconfig.org/) 파일로 파일 종류별 들여쓰기 크기 등 프로젝트 설정을 편집기에 전달할 수도 있습니다.

# 린트
{: #linting}

린터는 코드를 실행하지 않는 정적 분석으로 안티패턴과 잠재적 문제를 찾습니다. 표면적인 문법 형식보다 깊이 살펴보며 분석 범위는 도구마다 다릅니다.

린터에는 *규칙* 목록과 사전 설정이 있고 프로젝트별로 조정할 수 있습니다. 오탐이 생기는 규칙은 파일이나 줄 단위로 끌 수도 있습니다.

좋은 린터는 규칙이 찾는 패턴, 문제인 이유, 더 나은 대안을 설명합니다. Python의 불필요한 중첩 `if`를 찾는 [Ruff](https://docs.astral.sh/ruff/)의 [SIM102 규칙](https://docs.astral.sh/ruff/rules/collapsible-if/)이 한 예입니다. 일부 도구는 탐지뿐 아니라 자동 수정도 합니다.

여러 언어를 지원하는 [semgrep](https://github.com/semgrep/semgrep)도 유용합니다. 문자 대신 추상 구문 트리(AST)를 검색하는 "의미 기반 grep"으로, 프로젝트 전용 규칙을 쉽게 만들 수 있습니다. 예를 들어 Python에서 위험한 `subprocess.Popen(..., shell=True)` 사용을 찾으려면 다음과 같이 합니다.

```bash
semgrep -l python -e "subprocess.Popen(..., shell=True, ...)"
```

# 테스트
{: #testing}

테스트는 코드가 올바르다는 확신을 높이는 표준 기법입니다. 작성한 코드를 실행해 보고 기대와 다르면 오류를 내는 코드를 추가합니다.

함수별 *단위 테스트*, 모듈·서비스 상호작용의 *통합 테스트*, 전체 시나리오의 *기능 테스트*처럼 여러 수준을 검사할 수 있습니다. 구현 전에 테스트를 쓰는 *테스트 주도 개발*도 가능합니다. 버그를 찾았다면 같은 문제가 다시 생길 때 잡는 *회귀 테스트*를 추가하세요. Haskell의 [QuickCheck](https://hackage.haskell.org/package/QuickCheck)가 개척하고 Python의 [Hypothesis](https://hypothesis.readthedocs.io/) 등으로 확산된 *속성 기반 테스트*도 있습니다. 적합한 조합은 프로젝트에 따라 달라집니다.

데이터베이스나 웹 API 같은 외부 의존성은 테스트 중 실제 서비스와 통신하는 대신 *모킹(mocking)*하는 것이 유용할 수 있습니다.

## 코드 커버리지
{: #code-coverage}

커버리지는 테스트가 코드를 얼마나 실행했는지 나타내는 지표입니다. 테스트 실행 시 어느 줄이 실행됐는지 확인하여 빠진 경로를 찾습니다. 줄별 보고서는 테스트 작성을 돕고, [Codecov](https://app.codecov.io) 같은 서비스는 프로젝트 이력에 따른 커버리지를 웹에서 추적하게 합니다.

완벽한 지표는 아닙니다. 수치 자체에 매달리지 말고 좋은 테스트를 쓰는 데 집중하세요.

# 커밋 전 훅
{: #pre-commit-hooks}

Git의 pre-commit [훅](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)은 커밋 전에 지정한 코드를 자동 실행합니다. [pre-commit](https://pre-commit.com/) 프레임워크로 쉽게 관리할 수 있습니다. 보통 포매터·린터, 때로는 테스트를 실행하여 커밋이 프로젝트 스타일을 지키고 특정 오류를 포함하지 않게 합니다.

# 지속적 통합
{: #continuous-integration}

[GitHub Actions](https://github.com/features/actions) 같은 지속적 통합(CI) 서비스는 푸시, PR, 일정에 맞춰 스크립트를 실행합니다. 포매터, 린터, 테스트 등 품질 검사를 자주 수행합니다. 컴파일 언어는 빌드 여부를, 정적 타입 언어는 타입 검사 통과 여부를 확인할 수 있습니다. 푸시마다 실행하면 주 코드의 새 오류를, PR마다 실행하면 기여의 문제를, 주기적으로 실행하면 의존성의 문제를 잡습니다. 예를 들어 의존성이 [SemVer상 호환되는 버전](/2026/shipping-code/#releases--versioning)에 실수로 호환성 파괴를 넣은 경우입니다.

개발자 컴퓨터와 별개로 실행되므로 오래 걸리는 작업도 맡길 수 있습니다. 운영체제와 언어 버전을 조합한 테스트 *행렬(matrix)*을 실행해 여러 환경을 확인하는 것이 한 예입니다.

보통 CI는 코드를 직접 수정하지 않고 "검사 전용" 모드로 실행합니다. 따라서 포매터도 서식이 맞지 않으면 고치는 대신 오류를 냅니다.

README에는 CI나 커버리지의 [상태 배지](https://docs.github.com/en/actions/how-tos/monitor-workflows/add-a-status-badge)를 넣기도 합니다. 다음은 영문 Missing Semester의 현재 빌드 상태입니다.

[![빌드 상태](https://github.com/missing-semester/missing-semester/actions/workflows/build.yml/badge.svg)](https://github.com/missing-semester/missing-semester/actions/workflows/build.yml) [![링크 검사 상태](https://github.com/missing-semester/missing-semester/actions/workflows/links.yml/badge.svg)](https://github.com/missing-semester/missing-semester/actions/workflows/links.yml)

> [proof-html](https://github.com/anishathalye/proof-html)을 사용하는 [링크 검사](https://github.com/missing-semester/missing-semester/blob/master/.github/workflows/links.yml)는 외부 사이트 문제로 자주 실패합니다. 그래도 오타나, 리다이렉트 없이 옮겨지거나 사라진 페이지의 링크를 많이 찾고 고치는 데 도움이 됐습니다.

CI·포매터·린터·테스트 라이브러리의 세부 사용법은 좋은 사례로 배우기 좋습니다. 언어, 분야, 규모, 범위가 비슷한 좋은 오픈 소스 프로젝트에서 `pyproject.toml`, `.github/workflows/`, `DEVELOPMENT.md` 등을 살펴보세요.

## 지속적 배포
{: #continuous-deployment}

지속적 배포는 CI 인프라로 변경을 실제 *배포*합니다. 예를 들어 원본 Missing Semester 저장소는 강의 노트를 `git push`하면 GitHub Pages에 자동으로 빌드·배포됩니다. CI에서 앱 바이너리나 서비스용 Docker 이미지 같은 다른 [아티팩트](/2026/shipping-code/)도 만들 수 있습니다.

# 명령 실행 도구
{: #command-runners}

[just](https://github.com/casey/just) 같은 도구는 프로젝트 명령을 쉽게 실행하게 합니다. 개발자에게 `uv run ruff check --fix`를 외우게 하는 대신 `just lint`로 줄이고, `just format`, `just typecheck`처럼 일관된 이름을 제공할 수 있습니다.

언어별 프로젝트·패키지 관리 도구에 내장되기도 합니다. [npm](https://nodejs.org/en/learn/getting-started/an-introduction-to-the-npm-package-manager)의 `package.json`에 있는 `scripts`, Python [Hatch](https://hatch.pypa.io/)의 `pyproject.toml`에 있는 `tool.hatch.envs.*.scripts`가 예입니다. 이런 경우 범용 도구 `just`가 따로 필요하지 않습니다.

# 정규 표현식
{: #regular-expressions}

*정규 표현식*(regex)은 문자열 집합을 표현하는 언어입니다. CLI와 IDE 등에서 패턴 검색에 사용합니다. [ag](https://github.com/ggreer/the_silver_searcher)로 `ag "import .* as .*"`를 실행하면 Python에서 별칭을 지정한 임포트를 찾을 수 있습니다. [go test](https://pkg.go.dev/cmd/go#hdr-Test_packages)의 `-run [regexp]`는 테스트 일부를 선택합니다. 언어의 내장 기능이나 라이브러리로도 패턴 일치, 검증, 파싱 등에 활용합니다.

이번 강의는 [Python 정규 표현식 문법](https://docs.python.org/3/library/re.html)을 사용합니다. 정규 표현식에는 여러 변형이 있고 특히 고급 기능에 차이가 있습니다. [regex101](https://regex101.com/) 같은 온라인 도구로 만들고 디버깅할 수 있습니다.

- `abc`: 문자열 "abc"와 일치합니다.
- `missing|semester`: "missing" 또는 "semester"와 일치합니다.
- `\d{4}-\d{2}-\d{2}`: "2026-01-14" 같은 YYYY-MM-DD 형식과 일치합니다. 숫자 네 개·대시·두 개·대시·두 개만 검사하므로 "2026-01-99"도 통과합니다. 실제 날짜의 유효성 검사는 아닙니다.
- `.+@.+`: 문자들, `@`, 다시 문자들로 된 이메일 같은 문자열을 찾습니다. 기본 형태만 검사하므로 "nonsense@@@email"도 통과합니다. 오탐·누락 없이 이메일 주소를 찾는 복잡한 표현식도 [있지만](https://pdw.ex-parrot.com/Mail-RFC822-Address.html) 실용적이지 않습니다.

## 정규 표현식 문법
{: #regex-syntax}

전체 문법은 [문서](https://docs.python.org/3/library/re.html#regular-expression-syntax)를 참고하세요. 기본 요소는 다음과 같습니다.

- `abc`: 특별한 의미가 없는 문자는 그대로 일치합니다.
- `.`: 문자 하나와 일치합니다. 기본 Python 모드에서는 줄바꿈을 제외합니다.
- `[abc]`: 대괄호 안의 문자 하나, 즉 `a`, `b`, `c`와 일치합니다.
- `[^abc]`: 나열한 문자 이외의 문자 하나와 일치합니다. 예: `d`.
- `[a-f]`: 범위 안의 문자 하나와 일치합니다. `c`는 포함되지만 `q`는 아닙니다.
- `a|b`: 두 패턴 중 하나와 일치합니다.
- `\d`: 숫자 한 문자와 일치합니다. 예: `3`.
- `\w`: 단어를 구성하는 문자와 일치합니다. 예: `x`.
- `\b`: 단어의 *경계*와 일치합니다. "missing semester"에서 `m` 앞, `g` 뒤, `s` 앞, `r` 뒤입니다.
- `(...)`: 패턴을 그룹으로 묶습니다.
- `...?`: 앞 패턴 0개 또는 1개. `words?`는 "word", "words"와 일치합니다.
- `...*`: 앞 패턴 0개 이상. `.*`는 임의 개수의 문자와 일치합니다.
- `...+`: 앞 패턴 1개 이상. `\d+`는 하나 이상의 숫자와 일치합니다.
- `...{N}`: 앞 패턴 정확히 N개. `\d{4}`는 숫자 네 개입니다.
- `\.`: 마침표 자체와 일치합니다.
- `\\`: 백슬래시 자체와 일치합니다.
- `^`: 시작 위치와 일치합니다. 여러 줄 모드에서는 각 줄의 시작입니다.
- `$`: 끝 위치와 일치합니다. 여러 줄 모드에서는 각 줄의 끝입니다.

## 캡처 그룹과 참조
{: #capture-groups-and-references}

`(...)`로 그룹을 만들면 일치한 부분을 추출하거나 치환에서 참조할 수 있습니다. YYYY-MM-DD 날짜에서 월만 추출하는 예입니다.

```python
>>> import re
>>> re.match(r"\d{4}-(\d{2})-\d{2}", "2026-01-14").group(1)
'01'
```

편집기의 치환 패턴에서도 참조할 수 있지만 문법은 다릅니다. VS Code는 `$1`, `$2`, Vim은 `\1`, `\2` 등으로 그룹을 가리킵니다.

## 한계
{: #limitations}

[정규 언어](https://en.wikipedia.org/wiki/Regular_language)는 강력하지만 한계가 있습니다. 같은 수의 a와 b가 순서대로 나오는 {a^n b^n \| n &ge; 0} 같은 집합은 표준 정규 표현식으로 나타낼 수 [없습니다](https://en.wikipedia.org/wiki/Pumping_lemma_for_regular_languages). 실제 사례로 HTML도 정규 언어가 아닙니다. 현대 엔진은 전방 탐색과 역참조 등으로 정규 언어보다 넓은 범위를 지원하지만 여전히 표현력에 한계가 있습니다. 복잡한 언어에는 [PEG](https://en.wikipedia.org/wiki/Parsing_expression_grammar) 파서인 [pyparsing](https://github.com/pyparsing/pyparsing) 같은 더 강력한 파서가 필요할 수 있습니다.

## 정규 표현식 배우기
{: #learning-regex}

문법 전체를 외우기보다 이 강의의 기본을 익히고 필요할 때 참고 문서를 보세요.

대화형 AI도 패턴 작성에 도움이 됩니다. 예를 들어 다음 Nginx 로그에서 요청 경로를 추출하는 Python 정규 표현식을 요청해 보세요.

```
Write a Python-style regex pattern that matches the requested path from log lines from Nginx. Here is an example log line:

169.254.1.1 - - [09/Jan/2026:21:28:51 +0000] "GET /feed.xml HTTP/2.0" 200 2995 "-" "python-requests/2.32.3"
```

# 연습문제
{: #exercises}

1. 작업 중인 프로젝트에 포매터, 린터, pre-commit 훅을 설정하세요. 서식 오류는 자동 정리하고, 린트 오류는 [AI 에이전트](/2026/agentic-coding/)로 고쳐 보세요. 린터를 직접 실행하고 결과를 볼 수 있게 하여 반복 수정하게 하세요. 코드를 망가뜨리지 않았는지 결과를 주의 깊게 확인하세요.
1. 아는 언어의 테스트 라이브러리를 배우고 단위 테스트를 작성하세요. 커버리지 도구로 HTML 보고서를 만들어 실행된 줄을 찾아보세요. 아마 수치가 낮을 것입니다. 직접 테스트를 추가한 뒤 [AI 에이전트](/2026/agentic-coding/)로도 개선해 보세요. 에이전트가 줄별 커버리지를 얻어 어디에 집중할지 알 수 있게 하세요. 생성된 테스트는 실제로 좋은가요?
1. 푸시마다 서식·린트·테스트를 실행하는 CI를 설정하세요. 린트 위반 등 일부러 오류를 넣어 감지하는지 확인하세요.
1. [정규 표현식](#regular-expressions)과 [`grep`](/2026/course-shell/)으로 `subprocess.Popen(..., shell=True)` 사용을 찾으세요. 이어서 패턴이 놓치는 사례를 만들어 보세요. [semgrep](#linting)은 그 위험한 코드도 찾나요?
1. IDE나 편집기의 정규 표현식 치환으로 [강의 노트](https://raw.githubusercontent.com/missing-semester/missing-semester/refs/heads/master/_2026/code-quality.md)의 [Markdown 목록 기호](https://spec.commonmark.org/0.31.2/#bullet-list-marker) `-`를 `*`로 바꾸세요. 목록이 아닌 용도로도 쓰이므로 모든 `-`를 바꾸면 안 됩니다.
1. `{"name": "Alyssa P. Hacker", "college": "MIT"}` 같은 JSON에서 이름만 캡처하는 정규 표현식을 쓰세요. 처음에는 `Alyssa P. Hacker", "college": "MIT`까지 잡을 수 있습니다. [Python 문서](https://docs.python.org/3/library/re.html)의 탐욕적 수량자를 읽고 고치세요.
   1. 이름에 `"`가 들어 있어도 동작하게 하세요. JSON에서는 `\"`로 이스케이프할 수 있습니다.
   1. 실제로 복잡한 파싱에 정규 표현식을 쓰는 것은 **권장하지 않습니다**. 언어의 JSON 파서로 해결하세요. stdin으로 위 형식의 JSON을 받고 stdout으로 이름을 출력하는 CLI를 만드세요. 몇 줄이면 되며 Python에서는 `import json` 외에 한 줄로도 가능합니다.
