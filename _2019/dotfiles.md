---
layout: lecture
title: "설정 파일 관리"
lang: ko
presenter: Anish
date: 2019-01-24
order: 1
video:
  aspect: 62.5
  id: YSZBWWJw3mI
---

많은 프로그램은 "dotfile"이라고 부르는 일반 텍스트 파일로 설정합니다. `~/.gitconfig`처럼 파일 이름이 `.`으로 시작해서 붙은 이름입니다. 이런 파일은 기본 `ls` 출력에서 보이지 않습니다.

평소 사용하는 도구에도 세밀하게 조정할 수 있는 설정이 많을 것입니다. Vim은 Vimscript를, 셸은 해당 셸의 언어를 사용하는 것처럼 전용 언어로 설정하는 경우도 많습니다.

도구를 자신의 작업 방식에 맞게 바꾸면 생산성을 높일 수 있습니다. 다른 사람의 dotfile을 GitHub에서 통째로 복제하기보다는 직접 설정하는 데 시간을 들이길 권합니다.

이미 설정한 dotfile이 있을 수도 있습니다. 다음 위치를 살펴보세요.

- `~/.bashrc`
- `~/.emacs`
- `~/.vim`
- `~/.gitconfig`

프로그램에 따라 홈 디렉터리 바로 아래가 아니라 `~/.config`의 하위 디렉터리에 설정 파일을 저장하기도 합니다.

Dotfile은 명령줄 프로그램만 사용하는 것이 아닙니다. 예를 들어 [MPV](https://mpv.io/) 동영상 플레이어는 `~/.config/mpv` 안의 파일을 편집해 설정할 수 있습니다.

# 도구 설정법 배우기
{: id="learning-to-customize-tools"}

온라인 문서나 [매뉴얼 페이지](https://en.wikipedia.org/wiki/Man_page)에서 도구의 설정을 배울 수 있습니다. 특정 프로그램에 관한 블로그 글을 찾아보는 것도 좋습니다. 작성자가 선호하는 설정과 그 이유를 설명하는 경우가 많습니다. 다른 사람의 dotfile을 살펴보는 방법도 있습니다. GitHub에는 [dotfile 저장소](https://github.com/search?o=desc&q=dotfiles&s=stars&type=Repositories)가 많습니다. 가장 인기 있는 [이 저장소](https://github.com/mathiasbynens/dotfiles)도 참고하세요. 다만 이해하지 못한 설정을 무작정 복사하지는 마세요.

# 파일 구성
{: id="organization"}

Dotfile은 어떻게 관리하면 좋을까요? 별도 디렉터리에 모아 버전 관리하고, 스크립트로 필요한 위치에 **심볼릭 링크**를 만드세요. 다음과 같은 이점이 있습니다.

- **간편한 설치**: 새 컴퓨터에 로그인해도 짧은 시간 안에 자신의 설정을 적용할 수 있습니다.
- **이식성**: 어디서나 도구를 같은 방식으로 사용할 수 있습니다.
- **동기화**: 어느 컴퓨터에서든 설정을 수정하고 다른 컴퓨터에도 반영할 수 있습니다.
- **변경 추적**: 프로그래머로 일하는 동안 계속 관리할 파일입니다. 오래 유지하는 프로젝트에는 변경 이력이 유용합니다.

다음 예는 설정 파일과 설치 스크립트를 만들고 Git에 저장합니다. 설치 스크립트에서는 저장소의 `bashrc`를 `~/.bashrc`에 심볼릭 링크로 연결합니다.

```shell
cd ~/src
mkdir dotfiles
cd dotfiles
git init
touch bashrc
# create a bashrc with some settings, e.g.:
#     PS1='\w > '
touch install
chmod +x install
# insert the following into the install script:
#     #!/usr/bin/env bash
#     BASEDIR=$(dirname $0)
#     cd $BASEDIR
#
#     ln -s ${PWD}/bashrc ~/.bashrc
git add bashrc install
git commit -m 'Initial commit'
```

# 고급 주제
{: id="advanced-topics"}

## 컴퓨터별 설정
{: id="machine-specific-customizations"}

대부분은 모든 컴퓨터에서 같은 설정을 쓰고 싶겠지만, 특정 컴퓨터에서만 조금 다르게 설정해야 할 때도 있습니다. 다음과 같은 방법이 있습니다.

### 컴퓨터마다 브랜치 만들기
{: id="branch-per-machine"}

버전 관리 시스템에서 컴퓨터별 브랜치를 유지합니다. 개념은 단순하지만 관리가 번거로워질 수 있습니다.

### 조건문
{: id="if-statements"}

설정 파일이 조건문을 지원한다면 컴퓨터에 따라 다른 설정을 적용할 수 있습니다. 예를 들어 셸에서는 `uname`으로 운영체제를 구분하고, `hostname`으로 특정 컴퓨터인지 확인할 수 있습니다. 다음 예의 `{do_something}` 같은 부분은 실제 실행할 명령으로 바꿔야 합니다.

```shell
if [[ "$(uname)" == "Linux" ]]; then {do_something else}; fi

# Darwin is the architecture name for macOS systems
if [[ "$(uname)" == "Darwin" ]]; then {do_something}; fi

# You can also make it machine specific
if [[ "$(hostname)" == "myServer" ]]; then {do_something}; fi
```

### 다른 설정 파일 포함하기
{: id="includes"}

설정 파일이 다른 파일을 포함하는 기능을 지원한다면 이를 활용하세요. 예를 들어 `~/.gitconfig`에 다음 설정을 넣을 수 있습니다.

```
[include]
    path = ~/.gitconfig_local
```

각 컴퓨터의 `~/.gitconfig_local`에는 해당 컴퓨터에서만 사용할 설정을 넣습니다. 컴퓨터별 설정을 별도 저장소에서 관리할 수도 있습니다.

이 방법은 여러 프로그램이 설정 일부를 공유할 때도 유용합니다. 예를 들어 `bash`와 `zsh`에서 같은 별칭을 쓰려면 `.aliases`에 별칭을 작성하고 두 셸의 설정 파일에 다음 코드를 넣으면 됩니다. 파일이 있는지 확인한 다음 불러옵니다.

```bash
# Test if ~/.aliases exists and source it
if [ -f ~/.aliases ]; then
    source ~/.aliases
fi
```

# 참고 자료
{: id="resources"}

- 강사진의 dotfile: [Anish](https://github.com/anishathalye/dotfiles), [Jon](https://github.com/jonhoo/configs), [Jose](https://github.com/jjgo/dotfiles)
- [GitHub does dotfiles](https://dotfiles.github.io/): dotfile 프레임워크, 도구, 예제, 튜토리얼
- [셸 시작 스크립트](https://web.archive.org/web/20260329133158/https://blog.flowblok.id.au/2013-02/shell-startup-scripts.html): 셸이 사용하는 여러 설정 파일에 관한 설명

# 연습 문제
{: id="exercises"}

1. Dotfile을 모을 디렉터리를 만들고 [버전 관리](/2019/version-control/)를 설정하세요.
1. 셸처럼 자주 쓰는 프로그램의 설정을 적어도 하나 추가하세요. 처음에는 `$PS1`로 셸 프롬프트를 바꾸는 정도여도 됩니다.
1. 새 컴퓨터에서 dotfile을 빠르게 자동 설치할 방법을 마련하세요. 파일마다 `ln -s`를 실행하는 간단한 셸 스크립트도 좋고, [전용 도구](https://dotfiles.github.io/utilities/)를 써도 됩니다.
1. 새 가상 머신에서 설치 스크립트를 시험하세요.
1. 현재 사용하는 도구의 설정을 모두 dotfile 저장소로 옮기세요.
1. Dotfile을 GitHub에 공개하세요.
