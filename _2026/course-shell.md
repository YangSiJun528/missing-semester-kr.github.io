---
layout: lecture
title: "수업 개요와 셸 입문"
description: >
  수업을 만든 이유를 알아보고 셸 사용을 시작합니다.
thumbnail: /static/assets/thumbnails/2026/lec1.png
date: 2026-01-12
ready: true
translation_status: ai-draft
human_review: pending
translation_source: 1d695c94ccafdce3f06d6b9dfe3e6f106097693a
video:
  aspect: 56.25
  id: MSgoeuMqUmU
---

# 강사진 소개
{: #who-are-we}

이 수업은 [Anish](https://anish.io/), [Jon](https://thesquareplanet.com/), [Jose](http://josejg.com/)가 함께 가르칩니다. 모두 MIT 졸업생으로, 재학 중에 이 MIT IAP 수업을 시작했습니다. 강사진에게 연락하려면 [missing-semester@mit.edu](mailto:missing-semester@mit.edu)로 이메일을 보내세요.

우리는 수업의 대가를 받지 않으며 어떤 방식으로도 수익을 얻지 않습니다. 모든 [강의 자료](https://missing.csail.mit.edu/)와 [녹화 영상](https://www.youtube.com/@MissingSemester)을 온라인에 무료로 공개합니다. 우리를 지원하고 싶다면 수업을 널리 알려 주세요. 기업, 대학 등에서 여러 사람을 대상으로 이 자료를 활용한다면, 경험이나 후기를 이메일로 보내 주세요. 어떻게 활용되는지 듣고 싶습니다.

# 수업의 동기
{: #motivation}

컴퓨터 과학을 공부하는 우리는 컴퓨터가 반복 작업을 잘 처리한다는 사실을 압니다. 하지만 이것이 프로그램으로 수행하려는 계산뿐 아니라 컴퓨터를 *사용하는 방식*에도 적용된다는 사실은 자주 잊습니다. 컴퓨터와 관련된 문제를 풀 때 생산성을 높이고 더 복잡한 문제를 해결하도록 돕는 도구가 아주 많습니다. 그런데도 우리는 그중 일부만 쓰는 경우가 많습니다. 겨우 작업을 마칠 정도의 명령만 주문처럼 외우고, 막히면 인터넷의 명령을 무작정 복사해 붙여 넣습니다.

이 수업은 [그 문제를 해결하려는 시도](/about/)입니다.

이미 아는 도구를 최대한 활용하는 법과 새로 익힐 도구를 소개하고, 여러분 스스로 더 많은 도구를 탐색하거나 만들어 보고 싶게 하는 것이 목표입니다. 우리는 이것이 대부분의 컴퓨터 과학 교과과정에서 빠진 한 학기라고 생각합니다.

# 수업 구성
{: #class-structure}

학점이 없는 이 수업은 각각 [특정 주제](/2026/)를 다루는 1시간짜리 강의 9개로 구성됩니다. 강의는 대체로 독립적이지만, 뒤로 갈수록 앞선 내용을 알고 있다고 가정합니다. 강의 노트는 온라인에 공개하며, 시연 등 노트에 없는 내용을 수업에서 다루기도 합니다. 예년처럼 강의를 녹화해 [온라인](https://www.youtube.com/@MissingSemester)에 올립니다.

몇 차례의 1시간 강의로 많은 내용을 다루기 때문에 밀도가 높습니다. 각자 속도에 맞춰 익힐 수 있도록 핵심 내용을 따라 해 보는 연습문제를 강의마다 제공합니다. 별도의 질의응답 시간은 운영하지 않지만, [OSSU Discord](https://ossu.dev/#community)의 `#missing-semester-forum`이나 [이메일](mailto:missing-semester@mit.edu)로 질문해 주세요.

시간이 제한되어 있어 정규 수업처럼 모든 도구를 자세히 다룰 수는 없습니다. 가능한 한 더 공부할 자료를 안내하겠습니다. 특히 흥미로운 주제가 있다면 주저하지 말고 관련 자료를 문의하세요.

수업에 대한 의견도 [missing-semester@mit.edu](mailto:missing-semester@mit.edu)로 보내 주세요.

# 첫 번째 주제: 셸
{: #topic-1-the-shell}

{% comment %}
lecturer: Jon
{% endcomment %}

## 셸이란?
{: #what-is-the-shell}

요즘 컴퓨터에는 그래픽 사용자 인터페이스, 음성 인터페이스, AR/VR, 최근의 LLM까지 명령을 전달하는 다양한 인터페이스가 있습니다. 사용 사례의 80%에는 잘 맞지만, 할 수 있는 일에는 근본적인 제약이 있는 경우가 많습니다. 없는 버튼을 누르거나 구현되지 않은 음성 명령을 내릴 수는 없습니다. 컴퓨터가 제공하는 도구를 충분히 활용하려면 고전적인 텍스트 인터페이스인 셸로 내려가야 합니다.

거의 모든 플랫폼에는 어떤 형태로든 셸이 있으며, 여러 셸 중에서 고를 수 있는 플랫폼도 많습니다. 세부 사항은 달라도 핵심은 비슷합니다. 프로그램을 실행하고, 입력을 전달하고, 출력을 어느 정도 구조화된 방식으로 살펴볼 수 있습니다.

명령을 입력하는 셸 *프롬프트*를 열려면 먼저 셸의 시각적 인터페이스인 *터미널*이 필요합니다. 대개 기기에 설치되어 있으며, 없더라도 쉽게 설치할 수 있습니다.

- **Linux:** 대부분의 배포판에서 `Ctrl + Alt + T`를 누르거나 애플리케이션 메뉴에서 "Terminal"을 검색합니다.
- **Windows:** `Win + R`을 누르고 `cmd` 또는 `powershell`을 입력한 다음 Enter를 누릅니다. 시작 메뉴에서 "Terminal"이나 "명령 프롬프트"를 검색할 수도 있습니다.
- **macOS:** `Cmd + Space`로 Spotlight를 열고 "터미널"을 입력한 다음 Enter를 누릅니다. 응용 프로그램 → 유틸리티 → 터미널에서도 찾을 수 있습니다.

Linux와 macOS에서는 보통 Bourne Again SHell, 줄여서 "bash"가 열립니다. 가장 널리 쓰이는 셸 중 하나로, 문법도 다른 여러 셸과 비슷합니다. Windows에서는 실행한 명령에 따라 "batch" 또는 "powershell" 셸이 열립니다. 이들은 Windows 전용이며, 수업에서 다룰 기능과 대응하는 기능이 대부분 있지만 이 수업의 중심은 아닙니다. 대신 [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/)나 Linux 가상 머신을 사용하세요.

bash보다 사용 편의성을 개선한 셸도 있습니다. 대표적으로 fish와 zsh가 있습니다. 강사진도 모두 이런 셸을 사용하며 인기도 높지만, bash만큼 어디에나 있는 것은 아니고 많은 개념을 공유하므로 이번 강의에서는 집중적으로 다루지 않습니다.

## 왜 배워야 할까요?
{: #why-should-you-care-about-it}

셸은 보통 마우스로 클릭하는 것보다 훨씬 빠를 뿐 아니라, 하나의 그래픽 프로그램에서는 쉽게 얻기 어려운 표현력을 제공합니다. 곧 살펴보겠지만, 프로그램을 창의적으로 *조합*해 거의 모든 작업을 자동화할 수 있습니다.

셸에 익숙하면 오픈 소스 소프트웨어를 다루거나(설치 지침에 셸 명령이 자주 나옵니다), [코드 품질 강의](/2026/code-quality/)에서 다룰 지속적 통합을 구축하거나, 다른 프로그램이 실패했을 때 오류를 디버깅하는 데도 유용합니다.

## 셸에서 이동하기
{: #navigating-in-the-shell}

터미널을 실행하면 대개 다음과 비슷한 *프롬프트*가 나타납니다.

```console
missing:~$
```

셸의 기본 텍스트 인터페이스입니다. 컴퓨터 이름은 `missing`이고, "현재 작업 디렉터리", 즉 현재 위치는 홈 디렉터리를 뜻하는 `~`임을 알려 줍니다. `$`는 루트 사용자가 아니라는 뜻입니다. 이에 대해서는 뒤에서 다룹니다. 여기에 *명령*을 입력하면 셸이 해석합니다. 가장 기본적인 명령은 프로그램을 실행하는 것입니다.

```console
missing:~$ date
Fri 10 Jan 2020 11:49:31 AM EST
missing:~$
```

`date` 프로그램을 실행하면 현재 날짜와 시각이 출력됩니다. 그러고 나면 셸은 다음 명령을 기다립니다. 명령에 *인자*를 전달할 수도 있습니다.

```console
missing:~$ echo hello
hello
```

여기서는 `echo` 프로그램에 `hello`라는 인자를 전달했습니다. `echo`는 받은 인자를 그대로 출력합니다. 셸은 공백을 기준으로 명령을 나누고, 첫 단어가 가리키는 프로그램을 실행하면서 나머지 단어를 인자로 전달합니다. "My Photos"라는 디렉터리처럼 공백이나 특수문자가 들어간 인자를 전달하려면 `'` 또는 `"`로 감싸거나(`"My Photos"`), 해당 문자 앞에 `\`를 붙여 이스케이프합니다(`My\ Photos`).

처음 배울 때 가장 중요한 명령은 "manual"의 약자인 `man`일 것입니다. `man`으로 시스템의 명령에 대한 자세한 설명 등을 볼 수 있습니다. 예를 들어 `man date`는 `date`의 역할과 동작을 바꾸는 여러 인자를 설명합니다. 대부분의 명령은 `--help`를 인자로 주면 짧은 도움말도 출력합니다.

> `man`과 함께 [`tldr`](https://tldr.sh/)도 사용해 보세요. 자주 쓰는 예제를 터미널에서 바로 보여 줍니다. LLM도 명령의 동작이나 원하는 작업에 맞는 호출 방법을 설명하는 데 대체로 능숙합니다.

`man` 다음으로 중요한 명령은 "change directory"의 약자인 `cd`입니다. 별도 프로그램이 아니라 셸에 내장된 명령입니다. `which cd`를 실행하면 "no cd found"가 나옵니다. 경로를 전달하면 그 경로가 현재 작업 디렉터리가 되며 프롬프트에도 반영됩니다.

```console
missing:~$ cd /bin
missing:/bin$ cd /
missing:/$ cd ~
missing:~$
```

> 셸에는 자동 완성 기능이 있으므로 `<TAB>`을 눌러 경로를 빠르게 완성할 수 있습니다!

많은 명령은 별도로 경로를 지정하지 않으면 현재 작업 디렉터리에서 동작합니다. 현재 위치가 헷갈리면 `pwd`를 실행하거나 `echo $PWD`로 `$PWD` 환경 변수를 출력하세요. 둘 다 현재 작업 디렉터리를 보여 줍니다.

현재 작업 디렉터리는 *상대 경로*를 사용할 수 있게 해 준다는 점에서도 유용합니다. 앞에서 본 경로는 `/`로 시작해 파일 시스템의 루트(`/`)에서 목적지까지의 디렉터리를 모두 지정하는 *절대 경로*였습니다. 실제로는 현재 작업 디렉터리를 기준으로 하는 상대 경로를 더 자주 사용합니다. `/`로 시작하지 않는 상대 경로에서는 첫 요소를 현재 작업 디렉터리에서 찾고, 이후 요소를 차례로 따라갑니다.

```console
missing:~$ cd /
missing:/$ cd bin
missing:/bin$
```

모든 디렉터리에는 특별한 요소 두 개가 있습니다. `.`은 "현재 디렉터리", `..`은 "상위 디렉터리"입니다. 따라서 다음처럼 이동할 수 있습니다.

```console
missing:~$ cd /
missing:/$ cd bin/../bin/../bin/././../bin/..
missing:/$
```

명령의 인자에는 대체로 절대 경로와 상대 경로를 모두 쓸 수 있습니다. 상대 경로를 쓸 때는 현재 작업 디렉터리를 기억하세요!

> [`zoxide`](https://github.com/ajeetdsouza/zoxide)를 사용하면 디렉터리 이동이 빨라집니다. `z`가 자주 방문하는 경로를 기억하므로 더 적게 입력하고 이동할 수 있습니다.

## 셸에서 무엇을 사용할 수 있을까요?
{: #what-is-available-in-the-shell}

셸은 `date`나 `echo` 같은 프로그램을 어떻게 찾을까요? 명령을 실행하라는 요청을 받으면, 프로그램을 찾을 디렉터리 목록이 담긴 `$PATH`라는 *환경 변수*를 확인합니다.

```console
missing:~$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
missing:~$ which echo
/bin/echo
missing:~$ /bin/echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

`echo` 명령을 실행하면 셸은 `$PATH`에서 `:`로 구분된 디렉터리를 찾아보며 같은 이름의 파일을 검색합니다. 파일을 찾고 그 파일이 *실행 가능*하다면 실행합니다. 실행 권한은 뒤에서 다룹니다. `which`로 프로그램 이름에 대응하는 파일을 확인할 수 있으며, 실행할 파일의 *경로*를 직접 주면 `$PATH`를 거치지 않을 수도 있습니다.

이 원리를 이용하면 셸에서 실행할 수 있는 *모든* 프로그램을 알아보는 방법도 떠올릴 수 있습니다. `$PATH`에 있는 각 디렉터리의 내용을 나열하면 됩니다. 파일 목록을 보여 주는 `ls`에 디렉터리 경로를 전달하세요.

```console
missing:~$ ls /bin
```

> 더 읽기 편한 `ls`를 원한다면 [`eza`](https://eza.rocks/)를 사용해 보세요.

대부분의 컴퓨터에서는 프로그램이 아주 많이 나옵니다. 여기서는 중요한 몇 가지만 살펴보겠습니다. 먼저 간단한 명령입니다.

- `cat file`: `file`의 내용을 출력합니다.
- `sort file`: `file`의 줄을 정렬해 출력합니다.
- `uniq file`: `file`에서 연속으로 중복되는 줄을 제거합니다.
- `head file`, `tail file`: 각각 `file`의 처음과 마지막 몇 줄을 출력합니다.

> 구문 강조와 스크롤 기능이 필요하다면 `cat` 대신 [`bat`](https://github.com/sharkdp/bat)를 사용해 보세요.

`grep pattern file`은 `file`에서 `pattern`에 맞는 줄을 찾습니다. 매우 유용하며 생각보다 기능도 다양하므로 조금 더 살펴볼 가치가 있습니다. `pattern`은 복잡한 패턴도 표현할 수 있는 *정규 표현식*입니다. [코드 품질 강의](/2026/code-quality/#regular-expressions)에서 다룹니다. 파일 대신 디렉터리를 지정하고 `-r`을 주면 그 안의 모든 파일을 재귀적으로 검색합니다. 디렉터리를 생략하면 `.`을 사용합니다.

> `grep`보다 빠르고 사용하기 편한 [`ripgrep`](https://github.com/BurntSushi/ripgrep)도 사용해 보세요. 다만 이식성은 떨어집니다. 기본적으로 현재 작업 디렉터리를 재귀적으로 검색합니다!

사용법이 조금 더 복잡하지만 유용한 도구도 있습니다. 먼저 `sed`는 프로그램으로 파일을 편집하는 도구입니다. 편집을 자동화하는 자체 언어가 있지만, 가장 흔한 사용법은 다음과 같습니다.

```console
missing:~$ sed -i 's/pattern/replacement/g' file
```

`file`에서 `pattern`과 일치하는 부분을 모두 `replacement`로 바꿉니다. `-i`는 변경한 내용을 출력하기만 하는 대신 파일 자체를 수정하라는 뜻입니다. `s/`는 sed 언어에서 치환을 뜻하고, `/`는 패턴과 대체 문자열을 구분합니다. 마지막 `/g`는 각 줄의 첫 번째 일치 항목만이 아니라 *모든* 일치 항목을 바꾸라는 뜻입니다. `grep`처럼 정규 표현식을 사용하므로 표현력이 높습니다. `replacement`에서 일치한 패턴의 일부를 다시 참조할 수도 있습니다. 잠시 뒤 예를 보겠습니다.

다음은 조건에 맞는 파일을 재귀적으로 찾는 `find`입니다.

```console
missing:~$ find ~/Downloads -type f -name "*.zip" -mtime +30
```

다운로드 디렉터리에서 수정된 지 30일이 넘은 ZIP 파일을 찾습니다.

```console
missing:~$ find ~ -type f -size +100M -exec ls -lh {} \;
```

홈 디렉터리에서 100M보다 큰 파일을 찾아 나열합니다. `-exec`는 독립된 `;`로 끝나는 *명령*을 받습니다. 이 세미콜론은 공백처럼 이스케이프해야 합니다. `find`는 `{}`를 각 검색 결과의 파일 경로로 바꿉니다.

```console
missing:~$ find . -name "*.py" -exec grep -l "TODO" {} \;
```

TODO가 들어 있는 `.py` 파일을 찾습니다.

`find`의 문법은 처음에 어렵게 느껴질 수 있지만, 얼마나 유용한지는 짐작할 수 있을 것입니다.

> 더 편한 사용법을 원하면 `find` 대신 [`fd`](https://github.com/sharkdp/fd)를 사용해 보세요. 다만 이식성은 떨어집니다.

다음은 `sed`처럼 자체 프로그래밍 언어가 있는 `awk`입니다. `sed`가 파일 편집을 위해 만들어졌다면 `awk`는 파싱을 위해 만들어졌습니다. CSV처럼 규칙적인 형식의 데이터에서 각 레코드, 즉 줄의 특정 부분만 추출할 때 가장 많이 사용합니다.

```console
missing:~$ awk '{print $2}' file
```

`file`의 각 줄에서 공백으로 구분된 두 번째 열을 출력합니다. `-F,`를 추가하면 쉼표로 구분된 두 번째 열을 출력합니다. `awk`로는 행 필터링이나 집계 등 훨씬 많은 일을 할 수 있습니다. 연습문제에서 맛보세요.

이 도구들을 조합하면 다음과 같은 일도 가능합니다.

```console
missing:~$ ssh myserver 'journalctl -u sshd -b-1 | grep "Disconnected from"' \
  | sed -E 's/.*Disconnected from .* user (.*) [^ ]+ port.*/\1/' \
  | sort | uniq -c \
  | sort -nk1,1 | tail -n10 \
  | awk '{print $2}' | paste -sd,
postgres,mysql,oracle,dell,ubuntu,inspur,test,admin,user,root
```

원격 서버의 SSH 로그를 가져와(`ssh`는 다음 강의에서 다룹니다), 연결 종료 메시지를 찾고, 각 메시지에서 사용자 이름을 추출한 뒤 가장 많이 나온 사용자 이름 10개를 쉼표로 구분해 출력합니다. 명령 하나로 모두 처리합니다! 각 단계의 의미는 연습문제로 남겨 두겠습니다.

## 셸 언어: bash
{: #the-shell-language-bash}

앞의 예제에는 파이프(`|`)라는 새 개념이 등장했습니다. 한 프로그램의 출력을 다른 프로그램의 입력으로 연결합니다. 대부분의 명령줄 프로그램은 `file` 인자가 없으면 "표준 입력", 즉 보통 키보드 입력이 전달되는 곳에서 데이터를 읽습니다. `|`는 앞쪽 프로그램의 "표준 출력", 즉 보통 터미널에 표시되는 내용을 뒤쪽 프로그램의 표준 입력으로 전달합니다. 이렇게 셸 프로그램을 *조합*할 수 있다는 점이 셸을 생산적인 작업 환경으로 만듭니다.

대부분의 셸은 Python이나 Ruby처럼 완전한 프로그래밍 언어를 구현합니다. bash에도 변수, 조건문, 반복문, 함수가 있습니다. 셸에서 명령을 실행하는 것은 셸이 해석할 짧은 코드를 쓰는 일입니다. 오늘 bash 전체를 배우지는 않지만 특히 유용한 기능 몇 가지를 살펴보겠습니다.

먼저 리다이렉션입니다. `>file`은 프로그램의 표준 출력을 터미널 대신 `file`에 저장하여 나중에 분석하기 쉽게 합니다. `>>file`은 덮어쓰지 않고 덧붙입니다. `<file`은 키보드 대신 `file`에서 프로그램의 표준 입력을 읽도록 합니다.

> `tee`도 알아두세요. `cat`처럼 표준 입력을 표준 출력으로 보내면서, 동시에 파일에도 저장합니다. `verbose cmd | tee verbose.log | grep CRITICAL`을 사용하면 전체 로그는 파일에 남기면서 터미널에는 필요한 내용만 표시할 수 있습니다!

다음은 조건문입니다. `if command1; then command2; command3; fi`는 `command1`을 실행하고 오류 없이 끝나면 `command2`와 `command3`을 실행합니다. `else` 분기를 추가할 수도 있습니다. `command1`에는 `test`가 자주 쓰이며, `[`라는 이름으로도 사용합니다. 파일이 존재하는지(`test -f file` 또는 `[ -f file ]`), 문자열이 같은지(`[ "$var" = "string" ]`) 같은 조건을 검사합니다. bash에는 따옴표 처리에서 예상 밖의 동작이 적은, 더 안전한 내장 문법 `[[ ]]`도 있습니다.

bash에는 `while`과 `for` 반복문이 있습니다. `while command1; do command2; command3; done`은 `if`와 비슷하지만 `command1`이 성공하는 동안 계속 반복합니다. `for varname in a b c d; do command; done`은 `$varname`을 차례로 `a`, `b`, `c`, `d`로 설정하며 `command`를 네 번 실행합니다. 항목을 직접 나열하는 대신 "명령 치환"을 자주 사용합니다.

```bash
for i in $(seq 1 10); do
```

`seq 1 10`은 1부터 10까지 출력합니다. `$()` 전체가 그 출력으로 바뀌므로 10번 반복하는 for 문이 됩니다. 오래된 코드에는 ``for i in `seq 1 10`; do``처럼 백틱을 사용한 경우도 있지만, 중첩할 수 있는 `$()` 형식을 권장합니다.

긴 셸 스크립트를 프롬프트에 직접 쓸 수도 있지만, 보통은 `.sh` 파일로 저장하는 편이 좋습니다. 다음 예제는 백그라운드에서 CPU에 부하를 주며 프로그램이 실패할 때까지 반복 실행하고, 실패한 실행의 출력만 보여 줍니다. 간헐적으로 실패하는 테스트를 재현할 때 유용합니다.

```bash
#!/bin/bash
set -euo pipefail

# Start CPU stress in background
stress --cpu 8 &
STRESS_PID=$!

# Setup log file
LOGFILE="test_runs_$(date +%s).log"
echo "Logging to $LOGFILE"

# Run tests until one fails
RUN=1
while cargo test my_test > "$LOGFILE" 2>&1; do
    echo "Run $RUN passed"
    ((RUN++))
done

# Cleanup and report
kill $STRESS_PID
echo "Test failed on run $RUN"
echo "Last 20 lines of output:"
tail -n 20 "$LOGFILE"
echo "Full log: $LOGFILE"
```

여기에는 새 기능이 여럿 나옵니다. 프로그램을 동시에 실행하는 백그라운드 작업(`&`), 더 복잡한 [셸 리다이렉션](https://www.gnu.org/software/bash/manual/html_node/Redirections.html), [산술 확장](https://www.gnu.org/software/bash/manual/html_node/Arithmetic-Expansion.html) 등 유용한 명령을 작성하는 데 도움이 되므로 시간을 들여 살펴보세요.

첫 두 줄은 짚고 넘어가겠습니다. 첫 줄은 "셰뱅(shebang)"입니다. 셸 스크립트 외의 파일에서도 볼 수 있습니다. `#!/path`로 시작하는 파일을 실행하면 `/path`의 프로그램에 파일을 전달해 처리하게 합니다. 셸 스크립트라면 `/bin/bash`가 내용을 처리하며, `/usr/bin/python`을 셰뱅에 쓴 Python 스크립트도 만들 수 있습니다.

둘째 줄은 bash를 더 엄격하게 만들어 셸 스크립트의 실수 가능성을 줄입니다. `set`에는 여러 인자가 있지만, 간단히 말해 `-e`는 명령이 실패하면 일찍 종료하게 하고, `-u`는 정의되지 않은 변수를 빈 문자열로 취급하지 않고 오류로 처리하게 합니다. `-o pipefail`은 파이프(`|`) 안의 프로그램이 실패했을 때 이를 전체 파이프라인의 실패로 처리하여 스크립트가 종료될 수 있게 합니다.

> 셸 프로그래밍도 다른 언어처럼 깊은 주제입니다. 특히 bash에는 주의할 점이 유난히 많아, 이를 [정리한](https://tldp.org/LDP/abs/html/gotchas.html) [웹사이트](https://mywiki.wooledge.org/BashPitfalls)가 여럿 있을 정도입니다. 스크립트를 작성할 때 [shellcheck](https://www.shellcheck.net/)를 적극 활용하세요. LLM은 셸 스크립트 작성과 디버깅에도 유용하며, 스크립트가 100줄 이상으로 커져 bash로 다루기 어려워졌을 때 Python 같은 범용 언어로 옮기는 데도 도움이 됩니다.

# 다음 단계
{: #next-steps}

이제 셸에서 기본적인 작업을 할 수 있을 만큼 배웠습니다. 필요한 파일을 찾아 이동하고 대부분의 프로그램에서 기본 기능을 사용할 수 있을 것입니다. 다음 강의에서는 셸과 여러 유용한 명령줄 프로그램으로 더 복잡한 작업을 수행하고 자동화하는 법을 다룹니다.

# 연습문제
{: #exercises}

모든 강의에는 연습문제가 있습니다. 구체적인 과제를 제시하는 문제도 있고, "X와 Y 프로그램을 사용해 보세요"처럼 열린 문제도 있습니다. 직접 풀어 보기를 적극 권장합니다.

정답은 따로 작성하지 않았습니다. 막히면 [Discord](https://ossu.dev/#community)의 `#missing-semester-forum`에 글을 올리거나, 지금까지 시도한 내용을 이메일로 보내 주세요. 가능한 한 도와드리겠습니다. 이 문제를 LLM과의 대화를 시작하는 프롬프트로 활용해 주제를 깊이 탐구할 수도 있습니다. 연습문제의 가치는 정답 자체보다 답을 찾아가는 과정에 있습니다. 가장 짧은 풀이만 찾기보다 궁금한 방향으로 더 파고들며 "왜?"라고 질문해 보세요.

1. 이 수업에서는 Bash나 ZSH 같은 Unix 셸이 필요합니다. Linux나 macOS라면 특별한 준비가 필요 없습니다. Windows에서는 cmd.exe나 PowerShell을 쓰고 있지 않은지 확인하세요. [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/)나 Linux 가상 머신으로 Unix 방식의 명령줄 도구를 사용할 수 있습니다. `echo $SHELL`을 실행했을 때 `/bin/bash`나 `/usr/bin/zsh`처럼 나오면 적절한 셸을 사용하고 있는 것입니다.

1. `ls`의 `-l` 플래그는 무엇을 하나요? `ls -l /`을 실행하고 출력을 살펴보세요. 각 줄의 처음 10글자는 무슨 뜻인가요? 힌트: `man ls`.

1. `find ~/Downloads -type f -name "*.zip" -mtime +30`의 `*.zip`은 "글로브(glob)"입니다. 글로브란 무엇인가요? 테스트 디렉터리와 파일을 만들고 `ls *.txt`, `ls file?.txt`, `ls {a,b,c}.txt` 같은 패턴을 실험하세요. Bash 매뉴얼의 [패턴 일치](https://www.gnu.org/software/bash/manual/html_node/Pattern-Matching.html)를 참고하세요.

1. `'single quotes'`, `"double quotes"`, `$'ANSI quotes'`는 어떻게 다른가요? `$`, `!`, 줄바꿈 문자가 들어 있는 문자열을 출력하는 명령을 작성하세요. [인용](https://www.gnu.org/software/bash/manual/html_node/Quoting.html)을 참고하세요.

1. 셸에는 stdin(0), stdout(1), stderr(2)라는 표준 스트림이 있습니다. `ls /nonexistent /tmp`를 실행하며 stdout과 stderr를 서로 다른 파일로 보내세요. 둘 다 같은 파일로 보내려면 어떻게 해야 할까요? [리다이렉션](https://www.gnu.org/software/bash/manual/html_node/Redirections.html)을 참고하세요.

1. `$?`에는 직전 명령의 종료 상태가 담깁니다(0은 성공). `&&`는 앞 명령이 성공했을 때만 다음 명령을 실행하고, `||`는 실패했을 때만 실행합니다. `/tmp/mydir`가 없을 때만 만드는 한 줄짜리 명령을 작성하세요. [종료 상태](https://www.gnu.org/software/bash/manual/html_node/Exit-Status.html)를 참고하세요.

1. `cd`는 왜 독립된 프로그램이 아니라 셸에 내장되어야 할까요? 힌트: 자식 프로세스가 부모 프로세스에 어떤 영향을 줄 수 있고 줄 수 없는지 생각해 보세요.

1. 파일 이름을 인자(`$1`)로 받아 `test -f`나 `[ -f ... ]`로 존재 여부를 확인하고, 결과에 따라 다른 메시지를 출력하는 스크립트를 작성하세요. [Bash 조건식](https://www.gnu.org/software/bash/manual/html_node/Bash-Conditional-Expressions.html)을 참고하세요.

1. 앞의 스크립트를 `check.sh` 같은 파일에 저장하고 `./check.sh somefile`로 실행하세요. 어떻게 되나요? `chmod +x check.sh`를 실행한 다음 다시 시도하세요. 이 단계는 왜 필요한가요? 힌트: `chmod` 전후의 `ls -l check.sh` 결과를 비교하세요.

1. 스크립트의 `set` 플래그에 `-x`를 추가하면 어떻게 되나요? 간단한 스크립트로 실험하고 출력을 확인하세요. [내장 명령 set](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html)을 참고하세요.

1. 파일을 복사하되 오늘 날짜가 들어간 이름으로 백업하는 명령을 작성하세요. 예: `notes.txt` → `notes_2026-01-12.txt`. 힌트: `$(date +%Y-%m-%d)`. [명령 치환](https://www.gnu.org/software/bash/manual/html_node/Command-Substitution.html)을 참고하세요.

1. 강의의 간헐적 실패 테스트 스크립트에서 `cargo test my_test`를 고정해 쓰는 대신, 테스트 명령을 인자로 받도록 바꾸세요. 힌트: `$1` 또는 `$@`. [특수 매개변수](https://www.gnu.org/software/bash/manual/html_node/Special-Parameters.html)를 참고하세요.

1. 파이프로 홈 디렉터리에서 가장 흔한 파일 확장자 5개를 찾으세요. 힌트: `find`, `grep` 또는 `sed` 또는 `awk`, `sort`, `uniq -c`, `head`를 조합하세요.

1. `xargs`는 표준 입력의 줄을 명령 인자로 바꿉니다. `find -exec` 대신 `find`와 `xargs`를 조합하여 디렉터리의 모든 `.sh` 파일을 찾고 `wc -l`로 각각의 줄 수를 세세요. 추가 과제: 공백이 들어간 파일 이름도 처리하세요. 힌트: `-print0`, `-0`. `man xargs`를 참고하세요.

1. `curl`로 강의 사이트(`https://missing.csail.mit.edu/`)의 HTML을 가져오고, `grep`에 파이프로 전달해 나열된 강의 수를 세세요. 힌트: 강의마다 한 번씩 나타나는 패턴을 찾고, `curl -s`로 진행 표시를 숨기세요.

1. [`jq`](https://jqlang.github.io/jq/)는 강력한 JSON 처리 도구입니다. `curl`로 `https://microsoftedge.github.io/Demos/json-dummy-data/64KB.json`의 데이터를 가져와 `jq`로 version이 6보다 큰 사람들의 이름만 추출하세요. 힌트: 먼저 `jq .`로 구조를 보고 `jq '.[] | select(...) | .name'`을 사용해 보세요.

1. `awk`는 열의 값으로 줄을 필터링하고 출력을 가공할 수 있습니다. 예를 들어 `awk '$3 ~ /pattern/ {$4=""; print}'`는 세 번째 열이 `pattern`과 일치하는 줄에서 네 번째 열을 비워 출력합니다. 두 번째 열이 100보다 큰 줄만 출력하고 첫 번째와 세 번째 열을 바꾸는 `awk` 명령을 작성하세요. `printf 'a 50 x\nb 150 y\nc 200 z\n'`로 테스트하세요.

1. 강의의 SSH 로그 파이프라인을 분석하세요. 각 단계는 무엇을 하나요? 비슷한 방식으로 `~/.bash_history` 또는 `~/.zsh_history`에서 가장 자주 쓴 셸 명령을 찾아보세요.
