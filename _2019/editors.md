---
layout: lecture
title: "편집기"
lang: ko
presenter: Anish
date: 2019-01-22
order: 1
video:
  aspect: 62.5
  id: 1vLcusYSrI4
---

# 편집기가 중요한 이유
{: id="importance-of-editors"}

프로그래머는 대부분의 시간을 일반 텍스트 파일을 편집하며 보냅니다. 자신의 필요에 맞는 편집기를 배우는 데 시간을 투자할 가치가 있습니다.

새 편집기는 어떻게 배울까요? 당장은 작업 속도가 느려지더라도 한동안 그 편집기만 사용해 보세요. 곧 효과를 볼 수 있습니다. 기본을 배우는 데는 2주 정도면 충분합니다.

이 수업에서는 Vim을 가르치지만, 다른 편집기도 사용해 보길 권합니다. 편집기 선택은 개인 취향을 많이 타며, 사람마다 [의견도 강합니다](https://en.wikipedia.org/wiki/Editor_war).

50분 안에 강력한 편집기의 사용법을 전부 가르칠 수는 없습니다. 기본을 설명하고, 고급 기능 일부를 보여 주며, 더 깊이 배울 수 있는 자료를 소개하겠습니다. Vim을 기준으로 설명하지만 대부분의 개념은 다른 강력한 편집기에도 적용됩니다. 이런 개념을 적용할 수 없다면 그 편집기를 계속 써야 할지 생각해 볼 만합니다.

![편집기별 학습 곡선](/2019/files/editor-learning-curves.jpg)

<!-- source: https://blogs.msdn.microsoft.com/steverowe/2004/11/17/code-editor-learning-curves/ -->

위의 학습 곡선 그래프는 과장입니다. 강력한 편집기라도 기본을 배우기는 어렵지 않습니다. 완전히 익히는 데는 몇 년이 걸릴 수 있지만요.

어떤 편집기가 인기를 끄는지 궁금하다면 [Stack Overflow 설문](https://insights.stackoverflow.com/survey/2018/#development-environments-and-tools)을 참고하세요. Stack Overflow 사용자가 모든 프로그래머를 대표하지는 않으므로 편향이 있을 수 있습니다.

## 명령줄 편집기
{: id="command-line-editors"}

주로 GUI 편집기를 쓰기로 했더라도 명령줄 편집기를 익혀 두면 원격 컴퓨터의 파일을 편리하게 편집할 수 있습니다.

# Nano
{: id="nano"}

Nano는 단순한 명령줄 편집기입니다.

- 화살표 키로 이동합니다.
- 저장과 종료를 비롯한 다른 단축키는 화면 아래에 표시됩니다.

# Vim
{: id="vim"}

Vi/Vim은 강력한 텍스트 편집기입니다. 여러 시스템에 기본으로 설치된 명령줄 프로그램이어서 원격 컴퓨터의 파일을 편집할 때 편리합니다.

GVim이나 [MacVim](https://macvim-dev.github.io/macvim/)처럼 그래픽 인터페이스를 제공하는 버전도 있습니다. 24비트 색상, 메뉴, 팝업 등의 기능을 제공합니다.

## Vim의 철학
{: id="philosophy-of-vim"}

- 프로그래밍할 때는 새로 작성하는 시간보다 읽고 수정하는 시간이 더 많습니다.
    - Vim은 **모드가 있는 편집기**입니다. 텍스트를 입력할 때와 조작할 때 서로 다른 모드를 사용합니다.
- Vimscript뿐 아니라 Python 같은 언어로도 Vim을 프로그래밍할 수 있습니다.
- Vim의 조작 방식 자체가 프로그래밍 언어와 비슷합니다.
    - 의미를 연상하기 쉬운 키 입력이 명령이 됩니다.
    - 명령들을 조합할 수 있습니다.
- 마우스를 쓰지 마세요. 너무 느립니다.
- 편집기는 생각하는 속도를 따라올 수 있어야 합니다.

## Vim 입문
{: id="introductory-vim"}

### 모드
{: id="modes"}

Vim은 왼쪽 아래에 현재 모드를 표시합니다.

- 일반 모드(Normal): 파일 안에서 이동하고 편집합니다.
    - 대부분의 시간을 이 모드에서 보냅니다.
- 삽입 모드(Insert): 텍스트를 입력합니다.
- 비주얼 모드(Visual): 문자, 줄, 블록 단위로 텍스트를 선택합니다.

어느 모드에서든 `<ESC>`를 누르면 일반 모드로 돌아갑니다. 일반 모드에서 `i`를 누르면 삽입 모드, `v`는 비주얼 모드, `V`는 비주얼 줄 모드, `<C-v>`는 비주얼 블록 모드로 전환됩니다.

Vim에서는 `<ESC>`를 자주 누릅니다. Caps Lock을 Escape에 매핑하는 것도 고려해 보세요.

### 기본 명령
{: id="basics"}

Vim의 Ex 명령은 일반 모드에서 `:{명령}` 형태로 입력합니다.

- `:q`: 종료하기. 현재 창을 닫습니다.
- `:w`: 저장하기
- `:wq`: 저장하고 종료하기
- `:e {파일 이름}`: 편집할 파일 열기
- `:ls`: 열린 버퍼 목록 보기
- `:help {주제}`: 도움말 열기
    - `:help :w`: Ex 명령 `:w`의 도움말
    - `:help w`: 이동 명령 `w`의 도움말

### 이동
{: id="movement"}

Vim의 핵심은 효율적인 이동입니다. 일반 모드에서 파일을 탐색하세요.

- 화살표 키에 의존하는 습관을 피하려면 다음과 같이 비활성화할 수 있습니다.

```vim
nnoremap <Left> :echoe "Use h"<CR>
nnoremap <Right> :echoe "Use l"<CR>
nnoremap <Up> :echoe "Use k"<CR>
nnoremap <Down> :echoe "Use j"<CR>
```

- 기본 이동: `hjkl`은 각각 왼쪽, 아래, 위, 오른쪽입니다.
- 단어: `w`는 다음 단어, `b`는 단어 시작, `e`는 단어 끝으로 이동합니다.
- 줄: `0`은 줄 시작, `^`는 첫 번째 공백 아닌 문자, `$`는 줄 끝으로 이동합니다.
- 화면: `H`는 화면 위, `M`은 가운데, `L`은 아래로 이동합니다.
- 파일: `gg`는 파일 시작, `G`는 파일 끝으로 이동합니다.
- 줄 번호: `:{번호}<CR>` 또는 `{번호}G`로 해당 줄에 갑니다.
- 기타: `%`는 대응하는 괄호 등으로 이동합니다.
- 문자 찾기: `f{문자}`, `t{문자}`, `F{문자}`, `T{문자}`
    - 현재 줄에서 앞이나 뒤로 해당 문자를 찾고, 그 문자 또는 바로 앞까지 이동합니다.
- N번 반복: `{숫자}{이동 명령}`. 예를 들어 `10j`는 10줄 아래로 이동합니다.
- 검색: `/{정규 표현식}`으로 검색하고, `n`과 `N`으로 검색 결과를 오갑니다.

### 선택
{: id="selection"}

비주얼 모드에는 다음 세 가지가 있습니다.

- 비주얼 모드: 문자 단위
- 비주얼 줄 모드: 줄 단위
- 비주얼 블록 모드: 사각 영역 단위

이동 명령으로 선택 범위를 지정할 수 있습니다.

### 텍스트 조작
{: id="manipulating-text"}

마우스로 하던 작업을 이제 키보드와 조합 가능한 명령으로 합니다.

- `i`: 삽입 모드로 전환합니다.
    - 텍스트를 수정하거나 지울 때 Backspace만 쓰는 것보다 나은 방법이 있습니다.
- `o` / `O`: 아래 / 위에 새 줄을 넣습니다.
- `d{이동 명령}`: 이동 범위의 텍스트를 지웁니다.
    - `dw`는 단어, `d$`는 줄 끝까지, `d0`은 줄 시작까지 지웁니다.
- `c{이동 명령}`: 이동 범위의 텍스트를 바꿉니다.
    - `cw`는 단어를 바꿉니다.
    - `d{이동 명령}` 다음에 `i`를 누르는 것과 비슷합니다.
- `x`: 문자 하나를 지웁니다. `dl`과 같습니다.
- `s`: 문자 하나를 바꿉니다. `xi`와 같습니다.
- 비주얼 모드와 조작 명령을 조합할 수 있습니다.
    - 텍스트를 선택한 뒤 `d`로 지우거나 `c`로 바꿉니다.
- `u`: 실행 취소. `<C-r>`: 다시 실행.
- 더 배울 기능이 많습니다. 예를 들어 `~`는 문자의 대소문자를 바꿉니다.

### 학습 자료
{: id="resources"}

- `vimtutor`: Vim 사용법을 가르치는 명령줄 프로그램
- [Vim Adventures](https://vim-adventures.com/): 게임으로 배우는 Vim

## Vim 설정하기
{: id="customizing-vim"}

Vim은 `~/.vimrc`라는 일반 텍스트 설정 파일로 사용자 설정을 합니다. 이 파일에는 Vimscript 명령을 넣습니다. 기본 설정 중에서도 켜 두면 편리한 기능이 많습니다.

GitHub에서 다른 사람의 dotfile을 참고하되, 설정 전체를 그대로 복사하지는 마세요. 읽고 이해한 다음 필요한 부분만 가져오세요.

살펴볼 만한 설정은 다음과 같습니다.

- 구문 강조: `syntax on`
- 색상 테마
- 줄 번호: `set nu` / `set rnu`
- 들여쓰기, 줄바꿈, 입력 시작 지점을 넘어 Backspace 사용: `set backspace=indent,eol,start`

## 고급 Vim
{: id="advanced-vim"}

편집기의 강력함을 보여 주는 예를 몇 가지 소개하겠습니다. 이런 기능을 전부 가르칠 수는 없지만 사용하면서 익히게 될 것입니다. 편집기를 쓰다가 "더 나은 방법이 있을 텐데"라는 생각이 들면 실제로 있을 가능성이 큽니다. 온라인에서 찾아보세요.

### 검색과 치환
{: id="search-and-replace"}

`:s`는 치환 명령입니다. [설명](https://vim.fandom.com/wiki/Search_and_replace)을 참고하세요.

- `%s/foo/bar/g`
    - 파일 전체에서 `foo`를 `bar`로 바꿉니다.
- `%s/\[.*\](\(.*\))/\1/g`
    - 이름이 붙은 Markdown 링크를 URL만 남도록 바꿉니다.

### 여러 창 사용하기
{: id="multiple-windows"}

- `sp` / `vsp`로 창을 가로 / 세로로 나눕니다.
- 같은 버퍼를 여러 창에서 볼 수 있습니다.

### 마우스 지원
{: id="mouse-support"}

- `set mouse+=a`
    - 클릭, 스크롤, 선택을 사용할 수 있습니다.

### 매크로
{: id="macros"}

- `q{문자}`: `{문자}` 레지스터에 매크로 녹화를 시작합니다.
- `q`: 녹화를 끝냅니다.
- `@{문자}`: 매크로를 재생합니다.
- 오류가 발생하면 매크로 실행이 멈춥니다.
- `{숫자}@{문자}`: 매크로를 지정한 횟수만큼 실행합니다.
- 매크로는 재귀적으로 호출할 수 있습니다.
    - 먼저 `q{문자}q`로 해당 레지스터를 비웁니다.
    - 매크로를 녹화하면서 `@{문자}`를 넣어 자기 자신을 호출합니다. 녹화가 끝나기 전에는 아무 동작도 하지 않습니다.
- 예: XML을 JSON으로 바꾸기. [예제 파일](/2019/files/example-data.xml)을 사용하세요.
    - `name`과 `email`을 키로 갖는 객체의 배열을 만듭니다.
    - Python 프로그램으로 할까요?
    - `sed`와 정규 표현식을 쓸 수도 있습니다.
        - `g/people/d`
        - `%s/<person>/{/g`
        - `%s/<name>\(.*\)<\/name>/"name": "\1",/g`
        - 그 밖의 변환도 추가합니다.
    - Vim 명령과 매크로로 해 봅시다.
        - `Gdd`, `ggdd`로 마지막 줄과 첫 줄을 지웁니다.
        - 항목 하나의 형식을 바꾸는 매크로를 `e` 레지스터에 녹화합니다.
            - `<name>`이 있는 줄로 이동합니다.
            - `qe^r"f>s": "<ESC>f<C"<ESC>q`
        - 사람 한 명의 형식을 바꾸는 매크로를 만듭니다.
            - `<person>`이 있는 줄로 이동합니다.
            - `qpS{<ESC>j@eA,<ESC>j@ejS},<ESC>q`
        - 한 명을 변환한 뒤 다음 사람으로 이동하는 매크로를 만듭니다.
            - `<person>`이 있는 줄로 이동합니다.
            - `qq@pjq`
        - 파일 끝까지 매크로를 실행합니다.
            - `999@q`
        - 마지막 `,`를 직접 지우고, 배열 구분자인 `[`와 `]`를 추가합니다.

## Vim 확장하기
{: id="extending-vim"}

Vim을 확장하는 플러그인은 아주 많습니다.

먼저 [vim-plug](https://github.com/junegunn/vim-plug), [Vundle](https://github.com/VundleVim/Vundle.vim), [pathogen.vim](https://github.com/tpope/vim-pathogen) 같은 플러그인 관리자를 설정하세요.

사용해 볼 만한 플러그인은 다음과 같습니다.

- [ctrlp.vim](https://github.com/kien/ctrlp.vim): 퍼지 파일 검색
- [vim-fugitive](https://github.com/tpope/vim-fugitive): Git 연동
- [vim-surround](https://github.com/tpope/vim-surround): 텍스트를 감싸는 괄호나 따옴표 조작
- [gundo.vim](https://github.com/sjl/gundo.vim): 실행 취소 트리 탐색
- [nerdtree](https://github.com/scrooloose/nerdtree): 파일 탐색기
- [syntastic](https://github.com/vim-syntastic/syntastic): 구문 검사
- [vim-easymotion](https://github.com/easymotion/vim-easymotion): 빠른 이동
- [vim-over](https://github.com/osyo-manga/vim-over): 치환 결과 미리 보기

다음 사이트에서도 플러그인을 찾아볼 수 있습니다.

- [Vim Awesome](https://vimawesome.com/)

## 다른 프로그램에서 Vim 모드 사용하기
{: id="vim-mode-in-other-programs"}

Vim이나 Emacs처럼 널리 쓰이는 편집기의 조작 방식을 다른 도구에서도 사용할 수 있습니다.

- 셸
    - Bash: `set -o vi`
    - Zsh: `bindkey -v`
    - `export EDITOR=vim`: `git` 같은 프로그램이 사용하는 편집기를 환경 변수로 지정합니다.
- `~/.inputrc`
    - `set editing-mode vi`

웹 [브라우저용 Vim 키 바인딩 확장](https://vim.fandom.com/wiki/Vim_key_bindings_for_web_browsers)도 있습니다. Google Chrome의 [Vimium](https://chrome.google.com/webstore/detail/vimium/dbepggeogbaibhgnhhndojpepiihcmeb?hl=en), Firefox의 [Tridactyl](https://github.com/tridactyl/tridactyl) 등이 알려져 있습니다.

## 참고 자료
{: id="resources-1"}

- [Vim Tips Wiki](https://vim.fandom.com/wiki/Vim_Tips_Wiki)
- [Vim Advent Calendar](https://vimways.org/2018/): 여러 Vim 사용 팁
- [Neovim](https://neovim.io/): Vim을 현대적으로 다시 구현한 프로젝트로, 더 활발하게 개발되고 있습니다.
- [Vim Golf](https://www.vimgolf.com/): 여러 Vim 도전 과제

{% comment %}
# Resources

TODO resources for other editors?
{% endcomment %}

# 연습 문제
{: id="exercises"}

1. 여러 편집기를 사용해 보세요. Vim 같은 명령줄 편집기와 Atom 같은 GUI 편집기를 적어도 하나씩 써 보세요. `vimtutor`나 각 편집기의 튜토리얼로 배워 보세요. 새 편집기를 제대로 경험하려면 며칠 동안 실제 작업에 그 편집기만 사용해 보세요.

1. 편집기를 자신에게 맞게 설정하세요. 온라인에서 사용 팁을 찾아보고, 다른 사람의 설정도 살펴보세요. 설정에 설명이 잘 붙어 있는 경우가 많습니다.

1. 편집기 플러그인을 사용해 보세요.

1. 강력한 편집기를 적어도 몇 주 동안 사용해 보세요. 그쯤이면 이점이 보이기 시작할 것입니다. 언젠가는 생각하는 속도로 편집기를 다룰 수 있어야 합니다.

1. Python의 pyflakes 같은 린터를 설치하고 편집기에 연결한 뒤, 잘 동작하는지 확인하세요.
