---
layout: lecture
title: "개발 환경과 도구"
description: >
  IDE, Vim, 언어 서버, AI 개발 도구를 알아봅니다.
thumbnail: /static/assets/thumbnails/2026/lec3.png
date: 2026-01-14
ready: true
video:
  aspect: 56.25
  id: QnM1nVzrkx8
---

*개발 환경*은 소프트웨어를 만드는 도구들의 집합입니다. 중심에는 텍스트 편집 기능이 있고, 구문 강조, 타입 검사, 코드 서식 지정, 자동 완성 등이 함께 제공됩니다. [VS Code][vs-code] 같은 *통합 개발 환경*(IDE)은 이 기능들을 하나의 애플리케이션으로 묶습니다. 터미널 기반 작업에서는 [tmux](https://github.com/tmux/tmux)(터미널 멀티플렉서), [Vim](https://www.vim.org/)(텍스트 편집기), [Zsh](https://www.zsh.org/)(셸), 그리고 [Ruff](https://docs.astral.sh/ruff/)(Python 린터·포매터), [Mypy](https://mypy-lang.org/)(Python 타입 검사기) 같은 언어별 명령줄 도구를 조합합니다.

IDE와 터미널 기반 작업에는 각각 장단점이 있습니다. 그래픽 IDE는 배우기 쉽고 AI 자동 완성 같은 기능도 대개 잘 통합되어 있습니다. 터미널 기반 도구는 가볍고, GUI가 없거나 소프트웨어를 설치할 수 없는 환경에서는 유일한 선택지일 수 있습니다. 두 방식 모두 기본 사용법을 익히고 적어도 하나에는 능숙해지기를 권합니다. 선호하는 IDE가 없다면 [VS Code][vs-code]로 시작하세요.

이번 강의의 내용은 다음과 같습니다.

- [텍스트 편집과 Vim](#text-editing-and-vim)
- [코드 분석 기능과 언어 서버](#code-intelligence-and-language-servers)
- [AI를 활용한 개발](#ai-powered-development)
- [확장 기능과 그 밖의 IDE 기능](#extensions-and-other-ide-functionality)

[vs-code]: https://code.visualstudio.com/

# 텍스트 편집과 Vim
{: #text-editing-and-vim}

프로그래밍에서는 코드를 길게 입력하거나 파일을 처음부터 끝까지 읽기보다, 코드를 찾아 이동하고 일부를 읽고 수정하는 데 대부분의 시간을 씁니다. [Vim]은 이런 작업 비중에 맞춰 설계된 편집기입니다.

**Vim의 철학.** Vim의 핵심 아이디어는 인터페이스 자체가 텍스트 탐색과 편집을 위한 프로그래밍 언어라는 것입니다. 기억하기 쉬운 키 입력이 명령이며, 명령을 조합할 수 있습니다. 마우스는 느려서 피하고, 방향키조차 손을 많이 움직여야 하므로 피합니다. 그 결과 생각하는 속도를 따라가는, 마치 뇌와 컴퓨터를 직접 연결한 듯한 편집기가 됩니다.

**다른 소프트웨어의 Vim 지원.** 이 아이디어의 장점을 얻기 위해 반드시 [Vim] 자체를 쓸 필요는 없습니다. 텍스트를 편집하는 여러 프로그램이 내장 기능이나 플러그인으로 "Vim 모드"를 지원합니다. VS Code에는 [VSCodeVim](https://marketplace.visualstudio.com/items?itemName=vscodevim.vim)이 있고, Zsh에는 [Vim 에뮬레이션](https://zsh.sourceforge.io/Guide/zshguide04.html)이 내장되어 있으며, Claude Code에도 [Vim 편집 모드](https://code.claude.com/docs/en/interactive-mode#vim-editor-mode)가 있습니다. 여러분이 사용하는 텍스트 편집 도구도 어떤 형태로든 지원할 가능성이 높습니다.

## 모드 기반 편집
{: #modal-editing}

Vim은 작업 종류에 따라 동작 모드가 달라지는 *모드 기반 편집기*입니다.

- **일반(Normal)**: 파일을 탐색하고 편집합니다.
- **삽입(Insert)**: 텍스트를 입력합니다.
- **바꾸기(Replace)**: 기존 텍스트를 덮어씁니다.
- **비주얼(Visual)**: 일반·줄·블록 단위로 텍스트를 선택합니다.
- **명령줄(Command-line)**: 명령을 실행합니다.

같은 키도 모드에 따라 뜻이 다릅니다. `x`는 삽입 모드에서 문자 "x"를 입력하지만, 일반 모드에서는 커서 아래 문자를 지우고 비주얼 모드에서는 선택 영역을 지웁니다.

기본 설정에서는 왼쪽 아래에 현재 모드가 표시됩니다. 시작 모드는 일반 모드이며, 보통 일반 모드와 삽입 모드에서 대부분의 시간을 보냅니다.

어떤 모드에서든 `<ESC>`를 누르면 일반 모드로 돌아옵니다. 일반 모드에서 `i`는 삽입, `R`은 바꾸기, `v`는 비주얼, `V`는 비주얼 줄, `<C-v>`(Ctrl-V 또는 `^V`)는 비주얼 블록, `:`는 명령줄 모드로 전환합니다.

`<ESC>`를 자주 쓰므로 Caps Lock을 Escape로 바꾸거나([macOS 안내](https://vim.fandom.com/wiki/Map_caps_lock_to_escape_in_macOS)), 간단한 키 조합에 [대체 매핑](https://vim.fandom.com/wiki/Avoid_the_escape_key#Mappings)을 설정하는 것도 좋습니다.

## 기본: 텍스트 입력
{: #basics-inserting-text}

일반 모드에서 `i`를 누르면 삽입 모드가 됩니다. `<ESC>`로 돌아오기 전까지는 다른 텍스트 편집기처럼 동작합니다. 앞서 설명한 기본 기능과 이것만 알아도 파일을 편집할 수 있습니다. 다만 늘 삽입 모드에서만 편집한다면 효율적이지는 않습니다.

## Vim의 인터페이스는 프로그래밍 언어입니다
{: #vims-interface-is-a-programming-language}

키 입력은 기억하기 쉬운 이름을 가진 명령이며 서로 *조합*됩니다. 자판을 익히면 타이핑이 빨라지듯 명령이 손에 익으면 이동과 편집이 효율적입니다.

### 이동
{: #movement}

일반 모드에서 이동 명령으로 파일을 탐색하는 데 대부분의 시간을 쓰는 것이 좋습니다. 이동은 텍스트의 범위를 가리키므로 "명사"라고도 합니다.

- 기본 이동: `hjkl`(왼쪽, 아래, 위, 오른쪽)
- 단어: `w`(다음 단어), `b`(단어 시작), `e`(단어 끝)
- 줄: `0`(줄 시작), `^`(첫 공백 아닌 문자), `$`(줄 끝)
- 화면: `H`(위), `M`(가운데), `L`(아래)
- 스크롤: `Ctrl-u`(위), `Ctrl-d`(아래)
- 파일: `gg`(처음), `G`(끝)
- 줄 번호: `:{number}<CR>` 또는 `{number}G`로 해당 줄에 이동합니다. `<CR>`은 Enter 키입니다.
- 기타: `%`는 대응하는 괄호 등으로 이동합니다.
- 문자 찾기: `f{character}`, `t{character}`, `F{character}`, `T{character}`로 현재 줄의 문자를 앞·뒤로 찾거나 그 직전까지 이동합니다. `,`와 `;`로 일치 항목 사이를 이동합니다.
- 검색: `/{regex}`로 검색하고 `n`과 `N`으로 일치 항목 사이를 이동합니다.

### 선택
{: #selection}

비주얼 모드는 다음과 같습니다.

- 비주얼: `v`
- 비주얼 줄: `V`
- 비주얼 블록: `Ctrl-v`

이동 키로 선택 범위를 늘릴 수 있습니다.

### 편집
{: #edits}

마우스로 하던 일을 이제 이동 명령과 결합한 키보드 편집 명령으로 합니다. 여기서부터 Vim이 프로그래밍 언어처럼 보입니다. 편집 명령은 명사에 작용하므로 "동사"라고도 합니다.

- `i`: 삽입 모드로 들어갑니다. 텍스트 수정·삭제에는 백스페이스보다 강력한 명령을 활용하세요.
- `o` / `O`: 아래·위에 새 줄을 삽입합니다.
- `d{motion}`: 이동 범위를 삭제합니다. `dw`는 단어, `d$`는 줄 끝까지, `d0`은 줄 시작까지 삭제합니다.
- `c{motion}`: 이동 범위를 바꿉니다. `cw`는 단어를 바꿉니다. `d{motion}` 다음 `i`를 누르는 것과 비슷합니다.
- `x`: 문자를 삭제합니다(`dl`과 같음).
- `s`: 문자를 바꿉니다(`cl`과 같음).
- 비주얼 모드로 선택한 뒤 `d`로 삭제하거나 `c`로 바꿀 수 있습니다.
- `u`: 실행 취소. `<C-r>`: 다시 실행.
- `y`: 복사, 즉 "yank". `d` 같은 일부 명령도 내용을 복사합니다.
- `p`: 붙여넣기.
- 더 많은 명령이 있습니다. 예를 들어 `~`는 대소문자를 바꾸고, `J`는 줄을 합칩니다.

### 횟수
{: #counts}

명사와 동사에 횟수를 붙이면 작업을 여러 번 수행합니다.

- `3w`: 세 단어 앞으로 이동합니다.
- `5j`: 다섯 줄 아래로 이동합니다.
- `7dw`: 일곱 단어를 삭제합니다.

### 수식어
{: #modifiers}

명사의 뜻을 바꾸는 수식어도 있습니다. `i`는 "안쪽(inner/inside)", `a`는 "주변까지(around)"를 뜻합니다.

- `ci(`: 현재 소괄호 안의 내용을 바꿉니다.
- `ci[`: 현재 대괄호 안의 내용을 바꿉니다.
- `da'`: 작은따옴표로 둘러싼 문자열을 따옴표까지 삭제합니다.

## 모두 조합해 보기
{: #putting-it-all-together}

다음은 오류가 있는 [fizz buzz](https://en.wikipedia.org/wiki/Fizz_buzz) 구현입니다.

```python
def fizz_buzz(limit):
    for i in range(limit):
        if i % 3 == 0:
            print("fizz", end="")
        if i % 5 == 0:
            print("fizz", end="")
        if i % 3 and i % 5:
            print(i, end="")
        print()

def main():
    fizz_buzz(20)
```

일반 모드에서 시작해 다음 순서로 수정합니다.

- `main`이 호출되지 않습니다. `G`로 파일 끝에 가서 `o`로 아래에 줄을 열고 `if __name__ == "__main__": main()`을 입력합니다. Python을 지원하는 편집기는 들여쓰기를 자동으로 해 줄 수도 있습니다. `<ESC>`로 일반 모드로 돌아옵니다.
- 1 대신 0부터 시작합니다. `/range<CR>`로 `range`를 찾고 `ww`로 두 단어 이동합니다. `2w`도 되지만 작은 횟수는 키를 반복하기도 합니다. `i`로 들어가 `1,`을 추가한 뒤 `<ESC>`를 누릅니다. `e`로 다음 단어의 끝에 가서 `a`로 뒤에 `+ 1`을 추가하고 `<ESC>`를 누릅니다.
- 5의 배수에 "fizz"를 출력합니다. `:6<CR>`로 6번 줄에 가고, `ci"`로 큰따옴표 안의 내용을 `buzz`로 바꾼 뒤 `<ESC>`를 누릅니다.

## Vim 배우기
{: #learning-vim}

가장 좋은 방법은 지금까지 다룬 기초를 익힌 뒤, 모든 소프트웨어에서 Vim 모드를 켜고 실제로 사용하는 것입니다. 마우스나 방향키를 쓰고 싶은 유혹을 참으세요. 일부 편집기는 방향키 매핑을 해제해 좋은 습관을 들이도록 할 수도 있습니다.

### 추가 자료
{: #additional-resources}

- 이전 수업의 [Vim 강의](/2020/editors/): Vim을 더 자세히 다룹니다.
- `vimtutor`: Vim과 함께 설치되는 튜토리얼입니다. Vim이 설치되어 있다면 셸에서 실행할 수 있습니다.
- [Vim Adventures](https://vim-adventures.com/): 게임으로 Vim을 배웁니다.
- [Vim Tips Wiki](https://vim.fandom.com/wiki/Vim_Tips_Wiki)
- [Vim Advent Calendar](https://vimways.org/2019/): 다양한 Vim 팁.
- [VimGolf](https://www.vimgolf.com/): Vim 인터페이스를 언어로 사용하는 [코드 골프](https://en.wikipedia.org/wiki/Code_golf).
- [Vi/Vim Stack Exchange](https://vi.stackexchange.com/)
- [Vim Screencasts](http://vimcasts.org/)
- [Practical Vim](https://pragprog.com/titles/dnvim2/)(책)

[Vim]: https://www.vim.org/

# 코드 분석 기능과 언어 서버
{: #code-intelligence-and-language-servers}

IDE는 보통 [Language Server Protocol](https://microsoft.github.io/language-server-protocol/)을 구현한 *언어 서버*에 확장 기능으로 연결하여 코드의 의미를 이해해야 하는 언어별 기능을 제공합니다. 예를 들어 [VS Code Python 확장](https://marketplace.visualstudio.com/items?itemName=ms-python.python)은 [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)에, [Go 확장](https://marketplace.visualstudio.com/items?itemName=golang.go)은 Go 프로젝트의 [gopls](https://go.dev/gopls/)에 의존합니다. 사용하는 언어의 확장과 언어 서버를 설치하면 다음 기능을 활용할 수 있습니다.

- **코드 완성**: `object.` 뒤에 필드와 메서드를 보여 주는 등 더 정확한 자동 완성과 제안을 제공합니다.
- **인라인 문서**: 마우스를 올리거나 자동 완성을 사용할 때 문서를 보여 줍니다.
- **정의로 이동**: `object.field` 같은 참조 위치에서 필드 정의로 이동합니다.
- **참조 찾기**: 반대로 필드나 타입이 참조된 모든 위치를 찾습니다.
- **임포트 지원**: 임포트를 정리하고, 사용하지 않는 임포트를 지우고, 빠진 임포트를 표시합니다.
- **코드 품질**: 독립 실행도 가능한 도구들이 언어 서버에 통합되곤 합니다. 포매터가 들여쓰기와 서식을 정리하고, 타입 검사기와 린터가 입력 중 오류를 찾습니다. [코드 품질 강의](/2026/code-quality/)에서 자세히 다룹니다.

## 언어 서버 설정
{: #configuring-language-servers}

일부 언어는 확장과 서버 설치만으로 준비가 끝납니다. 다른 언어는 IDE에 환경을 알려 줘야 충분히 활용할 수 있습니다. 예를 들어 VS Code에 [Python 환경](https://code.visualstudio.com/docs/python/environments)을 지정하면 설치된 패키지를 언어 서버가 확인할 수 있습니다. 환경은 [코드 패키징과 배포 강의](/2026/shipping-code/)에서 자세히 다룹니다.

언어에 따라 조정할 설정도 있습니다. 예를 들어 Python의 선택적 타입 표기를 쓰지 않는 프로젝트에서는 VS Code의 정적 타입 검사를 끌 수 있습니다.

# AI를 활용한 개발
{: #ai-powered-development}

2021년 중반 OpenAI의 [Codex 모델](https://openai.com/index/openai-codex/)을 사용한 [GitHub Copilot][github-copilot]이 나온 뒤로, [LLM](https://en.wikipedia.org/wiki/Large_language_model)은 소프트웨어 공학에 널리 도입되었습니다. 현재 주로 쓰이는 형태는 자동 완성, 인라인 채팅, 코딩 에이전트입니다.

[github-copilot]: https://github.com/features/copilot/ai-code-editor

## 자동 완성
{: #autocomplete}

AI 자동 완성은 IDE의 기존 자동 완성처럼 입력 중 커서 위치에 이어질 코드를 제안합니다. 사용자가 별도로 개입하지 않아도 동작하기도 하지만, 보통 코드 주석으로 [프롬프트](https://en.wikipedia.org/wiki/Prompt_engineering)를 전달할 수도 있습니다.

예를 들어 이 강의 노트를 내려받아 모든 링크를 추출하는 스크립트를 작성해 봅시다.

```python
import requests

def download_contents(url: str) -> str:
```

모델이 함수 본문을 완성합니다.

```python
    response = requests.get(url)
    return response.text
```

주석으로 더 구체적으로 유도할 수 있습니다. 모든 Markdown 링크를 추출하는 함수에 다음처럼 모호한 이름을 붙였다고 합시다.

```python
def extract(contents: str) -> list[str]:
```

모델은 다음처럼 완성할 수 있습니다.

```python
    lines = contents.splitlines()
    return [line for line in lines if line.strip()]
```

코드 주석으로 원하는 동작을 알려 줍니다.

```python
def extract(content: str) -> list[str]:
    # extract all Markdown links from the content
```

이번에는 더 적절한 코드를 제안합니다.

```python
    import re
    pattern = r'\[.*?\]\((.*?)\)'
    return re.findall(pattern, content)
```

이 도구의 한계도 드러납니다. 커서 위치에서만 코드를 추가할 수 있습니다. 여기서는 `import re`를 함수 안보다 모듈 수준에 두는 편이 좋습니다.

위에서는 주석의 효과를 보이려고 모호한 함수 이름을 썼습니다. 실제로는 `extract_links`처럼 뜻이 분명한 이름과 독스트링을 쓰세요. 이를 바탕으로 모델도 위와 비슷한 코드를 만들 수 있습니다.

시연을 위해 스크립트를 완성하면 다음과 같습니다.

```python
print(extract(download_contents("https://raw.githubusercontent.com/missing-semester/missing-semester/refs/heads/master/_2026/development-environment.md")))
```

## 인라인 채팅
{: #inline-chat}

인라인 채팅은 줄이나 블록을 선택하고 AI에 수정안을 요청하는 기능입니다. 커서 뒤만 채우는 자동 완성과 달리 기존 코드를 바꿀 수 있습니다.

앞의 예제에서 외부 라이브러리 `requests`를 쓰지 않기로 했다면, 관련 세 줄을 선택해 인라인 채팅으로 "대신 내장 라이브러리를 사용해 줘"라고 요청할 수 있습니다.

```
use built-in libraries instead
```

모델의 제안은 다음과 같습니다.

```python
from urllib.request import urlopen

def download_contents(url: str) -> str:
    with urlopen(url) as response:
        return response.read().decode('utf-8')
```

## 코딩 에이전트
{: #coding-agents}

코딩 에이전트는 [에이전트 코딩 강의](/2026/agentic-coding/)에서 자세히 다룹니다.

## 권장 소프트웨어
{: #recommended-software}

널리 쓰이는 AI IDE로는 [GitHub Copilot][github-copilot] 확장을 설치한 [VS Code][vs-code]와 [Cursor](https://cursor.com/)가 있습니다. 강의 작성 시점에 GitHub Copilot은 [학생](https://github.com/education/students), 교사, 인기 오픈 소스 프로젝트의 유지보수자에게 무료로 제공됩니다. 빠르게 변하는 분야이며 주요 제품은 대체로 비슷한 기능을 제공합니다.

# 확장 기능과 그 밖의 IDE 기능
{: #extensions-and-other-ide-functionality}

IDE는 강력한 도구이며 *확장 기능*으로 더 강력해집니다. 한 강의에서 모두 다룰 수는 없지만 인기 있는 몇 가지를 소개합니다. [Vim Awesome](https://vimawesome.com/)이나 [설치 수순 VS Code 확장 목록](https://marketplace.visualstudio.com/search?target=VSCode&category=All%20categories&sortBy=Installs) 등 온라인 목록을 직접 탐색해 보세요.

- [개발 컨테이너](https://containers.dev/): [VS Code](https://code.visualstudio.com/docs/devcontainers/containers) 등 주요 IDE가 지원합니다. 컨테이너 안에서 개발 도구를 실행해 이식성과 격리를 확보합니다. [코드 패키징과 배포 강의](/2026/shipping-code/)에서 자세히 다룹니다.
- 원격 개발: [VS Code Remote SSH 확장](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh) 등으로 SSH를 통해 원격 컴퓨터에서 개발합니다. 클라우드의 강력한 GPU 머신에서 코드를 개발하고 실행할 때 유용합니다.
- 공동 편집: [VS Code Live Share 확장](https://marketplace.visualstudio.com/items?itemName=MS-vsliveshare.vsliveshare) 등으로 Google Docs처럼 같은 파일을 함께 편집합니다.

# 연습문제
{: #exercises}

1. 편집기와 셸 등 지원하는 모든 소프트웨어에서 Vim 모드를 켜고 한 달간 모든 텍스트 편집에 사용하세요. 비효율적으로 느껴지거나 "더 좋은 방법이 있을 텐데"라는 생각이 들면 검색해 보세요. 대개 더 좋은 방법이 있습니다.
1. [VimGolf](https://www.vimgolf.com/)의 문제 하나를 풀어 보세요.
1. 작업 중인 프로젝트에 IDE 확장과 언어 서버를 설정하세요. 의존 라이브러리의 정의로 이동하는 기능 등 필요한 기능이 모두 작동하는지 확인하세요. 사용할 코드가 없다면 [이 프로젝트](https://github.com/spf13/cobra) 같은 GitHub의 오픈 소스 프로젝트를 사용하세요.
1. IDE 확장 목록에서 유용해 보이는 것을 하나 설치하세요.
