---
layout: lecture
title: "명령줄 환경"
lang: ko
presenter: Jose
date: 2019-01-17
order: 1
video:
  aspect: 62.5
  id: i0rf1gpKL1E
---

## 별칭과 함수
{: id="aliases--functions"}

플래그나 긴 옵션이 많은 명령을 매번 입력하면 번거롭습니다. 대부분의 셸은 **별칭(alias)**을 지원합니다. Bash에서는 다음과 같이 지정합니다. `=` 양옆에 공백을 넣지 마세요.

```bash
alias alias_name="command_to_alias"
```

<!-- We can alias common flags for our commands like `alias ll=ls -ltAh`. Alias can be composed -->

별칭에는 여러 편리한 활용법이 있습니다. 자주 쓰는 옵션을 묶고, 긴 명령을 줄이며, 기존 명령 이름에 기본 옵션을 추가할 수 있습니다. 별칭끼리 조합할 수도 있습니다. 별칭을 무시하려면 명령 앞에 `\`를 붙이고, 지우려면 `unalias`를 사용합니다.

```bash
# Alias can summarize good default flags
alias ll="ls -lh"

# Save a lot of typing for common commands
alias gc="git commit"

# Alias can overwrite existing commands
alias mv="mv -i"
alias mkdir="mkdir -p"

# Alias can be composed
alias la="ls -A"
alias lla="la -l"

# To ignore an alias run it prepended with \
\ls
# Or can be disabled using unalias
unalias la

```

<!-- To get rid of an alias you can run `unalias alias_name` or to ignore alias when running a command you can prepend the command with a backward slash `\alias_name`. This is convenient when an alias is overwriting an existing name. -->

하지만 별칭만으로는 부족할 때가 있습니다. 특히 같은 인자를 받는 여러 명령을 연결하려면 제한이 있습니다. 이때 **함수**를 사용할 수 있습니다. 별칭과 별도 셸 스크립트의 중간쯤에 해당합니다.

다음 함수는 디렉터리를 만들고 그 안으로 이동합니다.

```bash
mcd () {
    mkdir -p $1
    cd $1
}
```

별칭과 함수는 기본적으로 셸 세션이 끝나면 사라집니다. 계속 사용하려면 `.bashrc`나 `.zshrc` 같은 셸 시작 파일에 넣어야 합니다. 별도 `.alias` 파일에 작성하고 각 셸 설정 파일에서 `source`로 불러오는 방법을 권합니다.

<!-- Lastly, if you decide to alias any of these tools with the "improved" version, e.g. `alias bat=cat` it is useful to know that you can tell bash to ignore aliases by doing `\cat` and ignore both aliases and functions by doing `command cat` -->

## 셸과 프레임워크
{: id="shells--frameworks"}

셸과 스크립팅 강의에서는 가장 널리 보급되어 있고 대부분의 시스템에서 기본으로 사용하는 `bash`를 다뤘습니다. 하지만 셸에는 다른 선택지도 있습니다.

예를 들어 `zsh`는 `bash`의 상위 집합으로, 다음과 같은 편리한 기능을 기본으로 제공합니다.

- `**`를 이용한 고급 글로빙
- 입력 중 글로빙·와일드카드 확장
- 철자 교정
- 개선된 탭 자동 완성과 후보 선택
- 경로 확장: `cd /u/lo/b`를 `/usr/local/bin`으로 확장하는 식입니다.

**프레임워크**로 셸을 확장할 수도 있습니다. [prezto](https://github.com/sorin-ionescu/prezto), [oh-my-zsh](https://github.com/robbyrussell/oh-my-zsh)처럼 여러 기능을 제공하는 것도 있고, [zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting), [zsh-history-substring-search](https://github.com/zsh-users/zsh-history-substring-search)처럼 특정 기능에 집중하는 작은 도구도 있습니다. [fish](https://fishshell.com/)처럼 이런 편의 기능을 기본으로 제공하는 셸도 있습니다. 예를 들면 다음과 같습니다.

- 오른쪽 프롬프트
- 명령 구문 강조
- 명령 기록에서 부분 문자열 검색
- 매뉴얼 페이지를 바탕으로 한 플래그 자동 완성
- 개선된 자동 완성
- 프롬프트 테마

프레임워크가 실행하는 코드가 너무 많거나 충분히 최적화되지 않았다면 셸이 느려질 수 있습니다. 프로파일링으로 원인을 찾고, 자주 쓰지 않거나 속도보다 중요하지 않은 기능은 꺼 두세요.

## 터미널 에뮬레이터와 멀티플렉서
{: id="terminal-emulators--multiplexers"}

셸을 설정하는 것과 함께 **터미널 에뮬레이터**의 종류와 설정도 살펴볼 만합니다. 터미널 에뮬레이터에는 여러 선택지가 있습니다. [비교 글](https://anarc.at/blog/2018-04-12-terminal-emulators-1/)을 참고하세요.

터미널을 수백, 수천 시간 사용하게 될 수 있으므로 설정을 살펴보는 데 시간을 들일 가치가 있습니다. 다음과 같은 항목을 바꿀 수 있습니다.

- 글꼴
- 색상 테마
- 키보드 단축키
- 탭과 분할 창 지원
- 이전 출력으로 스크롤할 수 있는 범위
- 성능: [Alacritty](https://github.com/jwilm/alacritty)처럼 GPU 가속을 제공하는 터미널도 있습니다.

[tmux](https://github.com/tmux/tmux) 같은 **터미널 멀티플렉서**도 알아둘 만합니다. `tmux`는 여러 셸 세션을 창과 분할 영역으로 구성합니다. 세션에 연결하거나 연결을 끊는 기능도 있습니다. 원격 서버에서 접속을 끊어도 셸을 유지하고 싶을 때 유용합니다. 보통 로그아웃하면 프로세스가 종료될 수 있으므로, 이런 기능이 없으면 `disown` 등을 신경 써야 합니다. `tmux`를 사용하면 여러 창으로 구성된 작업 환경에서 나갔다가 그대로 돌아올 수 있습니다. `~/.tmux.conf`를 편집해 다양한 설정도 바꿀 수 있습니다.

## 명령줄 도구
{: id="command-line-utilities"}

대부분의 유닉스 계열 운영체제가 기본으로 제공하는 명령줄 도구만으로도 일상적인 작업의 거의 전부를 처리할 수 있습니다.

이 절에서는 자주 하는 셸 작업을 더 편리하게 만드는 대체 도구를 소개합니다. 기능을 추가한 도구도 있고, 기본 설정이나 인터페이스를 더 간단하고 직관적으로 만든 도구도 있습니다.

### `fasd`와 `cd`
{: id="fasd-vs-cd"}

경로 확장과 탭 자동 완성이 있어도 디렉터리 이동은 반복적인 작업이 되기 쉽습니다. [Fasd](https://github.com/clvv/fasd)나 [autojump](https://github.com/wting/autojump)는 최근에 방문했거나 자주 방문하는 디렉터리를 기록하고 퍼지 검색으로 찾아줍니다.

예를 들어 `/home/user/awesome_project/code`를 방문한 적이 있다면 `z code`만 입력해도 그곳으로 이동할 수 있습니다. `code`라는 디렉터리가 여러 개라면 `z awe code`로 검색 범위를 좁힐 수 있습니다. `fasd`는 `autojump`와 달리 `cd`로 이동하는 대신 자주 쓰거나 최근에 쓴 파일·디렉터리의 경로를 확장해 주는 명령도 제공합니다.

### `bat`와 `cat`
{: id="bat-vs-cat"}

`cat`은 제 역할을 잘하지만, [bat](https://github.com/sharkdp/bat)은 구문 강조, 페이지 단위 표시, 줄 번호, Git 연동 기능을 더합니다.

### `exa`·`ranger`와 `ls`
{: id="exaranger-vs-ls"}

`ls`는 훌륭한 명령이지만 파일 크기를 바이트 단위로 표시하는 것처럼 기본 설정이 불편할 때도 있습니다. [exa](https://github.com/ogham/exa)는 더 편리한 기본 설정을 제공합니다.

여러 디렉터리를 탐색하거나 많은 파일을 미리 봐야 한다면, 편리한 인터페이스를 갖춘 [ranger](https://github.com/ranger/ranger)가 `cd`와 `cat`보다 효율적일 수 있습니다. 다양한 설정을 지원하며, 알맞게 설정하면 터미널에서 [이미지 미리 보기](https://github.com/ranger/ranger/wiki/Image-Previews)도 가능합니다.

### `fd`와 `find`
{: id="fd-vs-find"}

[fd](https://github.com/sharkdp/fd)는 `find`를 대체하는 간단하고 빠르며 쓰기 쉬운 도구입니다. `find`에서는 파일 이름으로 검색하려면 `-name` 같은 옵션을 지정해야 하지만, `fd`는 이런 일상적인 검색을 간단하게 만듭니다. Git도 인식하므로 기본적으로 `.gitignore`에 지정한 파일과 `.git` 디렉터리를 건너뜁니다. 색상으로 결과를 구분하는 기능도 기본으로 제공합니다.

### `rg`·`fzf`와 `grep`
{: id="rgfzf-vs-grep"}

`grep`은 훌륭하지만 여러 파일을 한꺼번에 검색하는 데 더 적합한 도구도 있습니다. [ack](https://github.com/beyondgrep/ack3), [ag](https://github.com/ggreer/the_silver_searcher), [rg](https://github.com/BurntSushi/ripgrep)는 파일 제외 규칙을 적용하면서 현재 디렉터리 아래를 재귀적으로 정규 표현식 검색합니다. 사용법은 대체로 비슷하지만, 저는 홈 디렉터리 전체를 빠르게 검색할 수 있는 `rg`를 선호합니다.

`CMD | grep PATTERN`을 반복해서 입력할 때도 많습니다. [fzf](https://github.com/junegunn/fzf)는 거의 모든 명령의 출력을 대화형으로 걸러 볼 수 있는 명령줄 퍼지 검색 도구입니다.

### `rsync`와 `cp`·`scp`
{: id="rsync-vs-cpscp"}

대부분의 상황에서는 기본 복사·이동 명령으로 충분합니다. 하지만 파일 수가 많거나 파일이 크거나 일부 데이터가 이미 목적지에 있다면 `rsync`가 훨씬 유용합니다. 이미 전송한 파일은 건너뛰며, `--partial`을 지정하면 전송이 중단됐을 때 일부 데이터를 남겨 다음 전송에 활용할 수 있습니다.

### `trash`와 `rm`
{: id="trash-vs-rm"}

`rm`으로 파일을 지우면 명령 자체로는 되돌릴 수 없습니다. 반면 운영체제의 파일 탐색기는 보통 파일을 바로 삭제하지 않고 휴지통으로 옮깁니다. 이후 휴지통을 비울 때 삭제됩니다.

휴지통 관리 방식은 운영체제마다 달라 공통 명령줄 도구 하나로 통일돼 있지는 않습니다. macOS에는 [trash](https://hasseg.org/trash/), Linux에는 [trash-cli](https://github.com/andreafrancia/trash-cli/) 등이 있습니다.

### `mosh`와 `ssh`
{: id="mosh-vs-ssh"}

`ssh`는 편리하지만 연결이 느리면 지연이 거슬리고, 연결이 끊어지면 다시 접속해야 합니다. [mosh](https://mosh.org/)는 네트워크가 바뀌거나 연결이 불안정한 상황을 지원하고, 로컬에서 입력을 예측해 보여 주는 도구입니다.

### `tldr`와 `man`
{: id="tldr-vs-man"}

대부분의 명령은 `man`, `-h`, `--help`로 기능과 옵션을 알아볼 수 있습니다. 하지만 설명이 너무 자세하면 원하는 내용을 찾기가 어려울 수 있습니다.

[tldr](https://github.com/tldr-pages/tldr)는 커뮤니티가 함께 만드는 문서 도구입니다. 명령줄에서 명령의 기능과 자주 쓰는 옵션을 몇 가지 간단한 예로 확인할 수 있습니다.

### `aunpack`과 `tar`·`unzip`·`unrar`
{: id="aunpack-vs-tarunzipunrar"}

[이 xkcd 만화](https://xkcd.com/1168/)처럼 `tar` 옵션은 기억하기 어려울 수 있습니다. `.rar` 파일에 `unrar`를 쓰듯 아예 다른 도구가 필요한 경우도 있습니다. [atool](https://www.nongnu.org/atool/) 패키지의 `aunpack`은 파일 형식에 맞는 옵션을 선택하고, 압축 해제한 파일이 흩어지지 않도록 디렉터리를 관리해 줍니다.

## 연습 문제
{: id="exercises"}

1. `cat .bash_history | sort | uniq -c | sort -rn | head -n 10`을 실행해 가장 자주 쓴 명령 10개를 찾아보세요. Zsh에서는 `cat .zhistory | sort | uniq -c | sort -rn | head -n 10`을 사용할 수 있습니다. 자주 쓰는 명령에 짧은 별칭을 붙일지 생각해 보세요.
1. 터미널 에뮬레이터를 하나 선택하고 다음 설정을 바꾸는 방법을 알아보세요.
    - 글꼴
    - 색상 테마. 일반적인 테마에는 색상이 몇 개 있나요? 왜 그런가요?
    - 이전 출력 기록의 크기
1. `fasd`나 비슷한 도구를 설치하고 `v`라는 Bash 또는 Zsh 함수를 작성하세요. 전달받은 인자로 퍼지 검색을 한 뒤 가장 잘 맞는 파일을 원하는 편집기로 열어야 합니다. 결과가 여러 개면 `fzf`로 선택할 수 있도록 수정하세요.
1. `fzf`는 퍼지 검색에 편리하며, 셸 명령 기록을 찾는 일도 퍼지 검색에 잘 맞습니다. `fzf`를 `^R`에 연결하는 방법을 알아보세요. [설정 안내](https://github.com/junegunn/fzf/wiki/Configuring-shell-key-bindings)를 참고할 수 있습니다.
1. `ack`의 `--bar` 옵션은 무엇을 하나요?
