---
layout: lecture
title: "명령줄 환경"
description: >
  입출력 스트림, 환경 변수, SSH 원격 접속을 통해 명령줄 프로그램의 동작을 배웁니다.
thumbnail: /static/assets/thumbnails/2026/lec2.png
date: 2026-01-13
ready: true
video:
  aspect: 56.25
  id: ccBGsPedE9Q
---

앞 강의에서 보았듯이 대부분의 셸은 프로그램을 실행하는 도구에 그치지 않고, 공통적인 패턴과 추상화를 갖춘 완전한 프로그래밍 언어를 제공합니다. 다만 일반적인 언어와 달리 셸 스크립트의 모든 요소는 프로그램을 실행하고 서로 간단하고 효율적으로 통신하게 하는 데 맞춰져 있습니다.

특히 셸 스크립트에서는 *관례*가 중요합니다. 명령줄 인터페이스(CLI) 프로그램이 셸 환경의 다른 요소와 잘 어울리려면 공통 패턴을 따라야 합니다. 이번 강의에서는 명령줄 프로그램의 동작을 이해하는 데 필요한 개념과, 사용·설정에 널리 쓰이는 관례를 살펴봅니다.

# 명령줄 인터페이스
{: #the-command-line-interface}

대부분의 언어에서 함수는 다음과 같이 작성합니다.

```
def add(x: int, y: int) -> int:
    return x + y
```

입력과 출력이 명확히 드러납니다. 반면 셸 스크립트는 첫눈에 상당히 달라 보입니다.

```shell
#!/usr/bin/env bash

if [[ -f $1 ]]; then
    echo "Target file already exists"
    exit 1
else
    if $DEBUG; then
        grep 'error' - | tee $1
    else
        grep 'error' - > $1
    fi
    exit 0
fi
```

이런 스크립트를 이해하려면 셸 프로그램끼리, 또는 셸 환경과 통신할 때 자주 등장하는 개념을 알아야 합니다.

- 인자
- 스트림
- 환경 변수
- 종료 코드
- 시그널

## 인자
{: #arguments}

셸 프로그램은 실행될 때 인자 목록을 받습니다. 인자는 단순한 문자열이며 해석 방법은 프로그램이 정합니다. 예를 들어 `ls -l folder/`는 `/bin/ls`를 `['-l', 'folder/']`라는 인자로 실행합니다.

셸 스크립트에서는 특수 문법으로 인자에 접근합니다. 첫 인자는 `$1`, 둘째는 `$2`이며 `$9`까지 같은 방식입니다. 전체 인자 목록은 `$@`, 인자 수는 `$#`, 프로그램 이름은 `$0`으로 확인합니다.

대부분의 프로그램은 *플래그*와 일반 문자열을 섞어 인자로 받습니다. 플래그 앞에는 대시 하나(`-`) 또는 둘(`--`)이 붙습니다. 보통 선택 사항이며 프로그램의 동작을 바꿉니다. 예를 들어 `ls -l`은 `ls`의 출력 형식을 바꿉니다.

`--all`처럼 긴 이름에는 대시 둘을, `-a`처럼 보통 한 글자인 이름에는 대시 하나를 사용합니다. 같은 옵션을 두 형태로 제공하기도 합니다. `ls -a`와 `ls --all`은 같습니다. 짧은 플래그는 묶을 수 있어 `ls -l -a`와 `ls -la`도 같습니다. 순서도 대개 중요하지 않아 `ls -la`와 `ls -al`은 같은 결과를 냅니다. 셸에 익숙해지면 `--help`, `--verbose`, `--version`처럼 흔한 플래그는 자연스럽게 사용하게 됩니다.

> 플래그는 셸의 관례를 보여 주는 첫 사례입니다. 셸 언어가 `-`나 `--`를 이렇게 쓰도록 강제하지는 않습니다. `myprogram +myoption myfile` 같은 문법을 만들 수도 있지만, 사용자는 대시를 예상하므로 혼란스러울 것입니다. 실제로 대부분의 언어에는 대시 문법의 인자를 파싱하는 라이브러리가 있습니다. Python의 `argparse`가 한 예입니다.

같은 종류의 인자를 여러 개 받아 각각에 같은 작업을 수행하는 것도 흔한 CLI 관례입니다.

```shell
mkdir src
mkdir docs
# is equivalent to
mkdir src docs
```

처음에는 불필요한 문법적 편의처럼 보이지만, *글로빙(globbing)*과 결합하면 강력해집니다. 글로브는 프로그램 호출 전에 셸이 확장하는 특수 패턴입니다.

현재 폴더의 `.py` 파일을 하위 디렉터리까지 내려가지 않고 모두 지운다고 합시다. 앞 강의에서 배운 내용으로는 다음과 같이 할 수 있습니다.

```shell
for file in $(ls | grep -P '\.py$'); do
    rm "$file"
done
```

하지만 `rm *.py`만으로도 됩니다!

`rm *.py`를 입력하면 셸은 `/bin/rm`에 `['*.py']`를 그대로 전달하지 않습니다. `*`가 0개 이상의 임의의 문자와 일치한다는 규칙에 따라 현재 폴더에서 `*.py`에 맞는 파일을 찾습니다. `main.py`와 `utils.py`가 있다면 `rm`은 `['main.py', 'utils.py']`를 받습니다.

자주 쓰는 패턴은 `*`(0개 이상의 임의의 문자), `?`(정확히 한 문자), 중괄호입니다. 중괄호 `{}`는 쉼표로 구분된 패턴 목록을 여러 인자로 확장합니다. 예제로 보면 이해하기 쉽습니다.

```shell
touch folder/{a,b,c}.py
# Will expand to
touch folder/a.py folder/b.py folder/c.py

convert image.{png,jpg}
# Will expand to
convert image.png image.jpg

cp /path/to/project/{setup,build,deploy}.sh /newpath
# Will expand to
cp /path/to/project/setup.sh /path/to/project/build.sh /path/to/project/deploy.sh /newpath

# Globbing techniques can also be combined
mv *{.py,.sh} folder
# Will move all *.py and *.sh files
```

> zsh 등 일부 셸은 재귀 경로까지 확장하는 `**` 같은 고급 글로빙도 지원합니다. `rm **/*.py`는 하위 디렉터리까지 `.py` 파일을 삭제합니다.

## 스트림
{: #streams}

다음과 같은 파이프라인을 실행하면 `grep`이 `cat`, `uniq`와 각각 통신합니다.

```shell
cat myfile | grep -P '\d+' | uniq -c
```

중요한 점은 세 프로그램이 *동시에* 실행된다는 것입니다. 셸이 `cat`, `grep`, `uniq`를 차례로 실행하고 종료를 기다리는 것이 아닙니다. 셋을 모두 시작하고 `cat`의 출력을 `grep`의 입력에, `grep`의 출력을 `uniq`의 입력에 연결합니다. 파이프 연산자 `|`는 프로그램 사이를 흐르는 데이터 스트림을 연결합니다.

다음 예제로 파이프라인의 명령이 즉시 시작되는 것을 확인할 수 있습니다.

```console
$ (sleep 15 && cat numbers.txt) | grep -P '^\d$' | sort | uniq  &
[1] 12345
$ ps | grep -P '(sleep|cat|grep|sort|uniq)'
  32930 pts/1    00:00:00 sleep
  32931 pts/1    00:00:00 grep
  32932 pts/1    00:00:00 sort
  32933 pts/1    00:00:00 uniq
  32948 pts/1    00:00:00 grep
```

`cat`을 제외한 프로세스가 바로 실행됩니다. 셸은 어느 프로세스도 끝나기 전에 모두 시작하고 스트림을 연결합니다. `cat`은 `sleep`이 끝나야 실행되며, 그 출력은 `grep`으로 이어집니다.

모든 프로그램에는 stdin(표준 입력)이라는 입력 스트림이 있습니다. 파이프에서는 자동으로 연결됩니다. 많은 프로그램은 파일 이름으로 `-`를 받으면 "표준 입력에서 읽기"로 해석합니다.

```shell
# These are equivalent when data comes from a pipe
echo "hello" | grep "hello"
echo "hello" | grep "hello" -
```

출력 스트림은 stdout과 stderr 두 개입니다. 표준 출력(stdout)은 가장 흔히 보게 되는 출력이며, 파이프에서 다음 명령으로 전달됩니다. 표준 오류(stderr)는 경고나 문제를 알리는 별도 스트림으로, 이 내용이 다음 명령의 데이터로 파싱되지 않게 합니다.

```console
$ ls /nonexistent
ls: cannot access '/nonexistent': No such file or directory
$ ls /nonexistent | grep "pattern"
ls: cannot access '/nonexistent': No such file or directory
# The error message still appears because stderr is not piped
$ ls /nonexistent 2>/dev/null
# No output - stderr was redirected to /dev/null
```

셸에는 스트림을 리다이렉트하는 문법이 있습니다. 다음 예제를 보세요.

```shell
# Redirect stdout to a file (overwrite)
echo "hello" > output.txt

# Redirect stdout to a file (append)
echo "world" >> output.txt

# Redirect stderr to a file
ls foobar 2> errors.txt

# Redirect both stdout and stderr to the same file
ls foobar &> all_output.txt

# Redirect stdin from a file
grep "pattern" < input.txt

# Discard output by redirecting to /dev/null
cmd > /dev/null 2>&1
```

퍼지 검색 도구 [`fzf`](https://github.com/junegunn/fzf)도 Unix 철학을 잘 보여 줍니다. 표준 입력에서 줄을 읽고, 대화형 인터페이스로 필터링하고 선택하게 합니다.

```console
$ ls | fzf
$ cat ~/.bash_history | fzf
```

`fzf`는 여러 셸 작업과 통합할 수 있습니다. 셸 설정을 다룰 때 다른 활용법도 보겠습니다.

## 환경 변수
{: #environment-variables}

bash에서 변수에 값을 넣는 문법은 `foo=bar`이며, 값은 `$foo`로 읽습니다. `foo = bar`는 변수 대입이 아닙니다. 셸은 `foo` 프로그램에 `['=', 'bar']`를 전달하는 명령으로 해석합니다. 셸 스크립트에서 공백은 인자를 나누므로 이 동작을 기억하세요.

셸 변수는 기본적으로 문자열로 취급됩니다. 문자열을 쓸 때 작은따옴표와 큰따옴표는 서로 바꿔 쓸 수 없습니다. `'` 안의 문자열은 그대로 유지되어 변수 확장, 명령 치환, 이스케이프 처리가 일어나지 않지만, `"` 안에서는 변수 확장과 명령 치환 등이 일어납니다.

```shell
foo=bar
echo "$foo"
# prints bar
echo '$foo'
# prints $foo
```

명령의 출력을 변수에 저장하려면 *명령 치환*을 사용합니다.

```shell
files=$(ls)
echo "$files" | grep README
echo "$files" | grep ".py"
```

`ls`의 표준 출력이 `files` 변수에 담깁니다. 줄바꿈도 포함되므로 `grep` 같은 프로그램은 각 항목을 별도로 처리할 수 있습니다.

비슷하지만 덜 알려진 기능은 *프로세스 치환*입니다. `<( CMD )`는 `CMD`를 실행하고, 그 출력을 파일처럼 읽을 수 있는 경로로 `<()`를 바꿉니다. 표준 입력 대신 파일을 받는 명령에 유용합니다. 예를 들어 `diff <(ls src) <(ls docs)`는 `src`와 `docs`의 파일 목록 차이를 보여 줍니다.

셸 프로그램이 다른 프로그램을 호출하면 *환경 변수*라고 부르는 변수 집합을 전달합니다. 현재 환경 변수는 `printenv`로 확인합니다. 명령 앞에 변수 대입을 붙이면 해당 명령에 환경 변수를 명시적으로 전달할 수 있습니다.

> 환경 변수에는 보통 `HOME`, `PATH`, `DEBUG`처럼 대문자를 사용합니다. 기술적 요구 사항은 아니지만, 보통 소문자로 쓰는 지역 셸 변수와 구분하기 쉽습니다.

```shell
TZ=Asia/Tokyo date  # prints the current time in Tokyo
echo $TZ  # this will be empty, since TZ was only set for the child command
```

내장 명령 `export`로 현재 환경을 바꾸면 이후의 모든 자식 프로세스가 변수를 상속합니다.

```shell
export DEBUG=1
# All programs from this point onwards will have DEBUG=1 in their environment
bash -c 'echo $DEBUG'
# prints 1
```

변수를 삭제하려면 `unset DEBUG`처럼 내장 명령 `unset`을 사용합니다.

> 환경 변수도 관례입니다. 프로그램에 매번 옵션을 명시하지 않고 동작을 바꿀 수 있습니다. 예를 들어 셸은 `$HOME`에 현재 사용자의 홈 경로를 설정합니다. 프로그램은 `--home /home/alice` 같은 인자를 요구하는 대신 이 값을 읽습니다. `$TZ`도 흔한 예로, 많은 프로그램이 지정한 시간대에 맞춰 날짜와 시각을 표시할 때 사용합니다.

## 종료 코드
{: #return-codes}

앞에서 보았듯 셸 프로그램의 주요 결과는 stdout·stderr와 파일 시스템의 변경으로 전달됩니다.

종료 코드 0은 성공을, 0이 아닌 값은 문제가 생겼음을 나타내는 것이 관례입니다. `exit NUM`으로 종료 코드를 명시할 수 있습니다. 마지막 명령의 종료 코드는 특수 변수 `$?`로 읽습니다.

셸의 `&&`와 `||`는 각각 AND와 OR 연산을 하지만, 일반적인 언어와 달리 프로그램의 종료 코드를 대상으로 합니다. 둘 다 [단락 평가](https://en.wikipedia.org/wiki/Short-circuit_evaluation)를 하므로, 앞 명령의 성공이나 실패에 따라 다음 명령을 실행할 수 있습니다. 성공 여부는 종료 코드가 0인지로 판단합니다.

```shell
# echo will only run if grep succeeds (finds a match)
grep -q "pattern" file.txt && echo "Pattern found"

# echo will only run if grep fails (no match)
grep -q "pattern" file.txt || echo "Pattern not found"

# true is a shell program that always succeeds
true && echo "This will always print"

# and false is a shell program that always fails
false || echo "This will always print"
```

`if`와 `while`도 종료 코드로 판단합니다.

```shell
# if uses the return code of the condition command (0 = true, nonzero = false)
if grep -q "pattern" file.txt; then
    echo "Found"
fi

# while loops continue as long as the command returns 0
while read line; do
    echo "$line"
done < file.txt
```

## 시그널
{: #signals}

명령이 너무 오래 걸리는 등 실행 중인 프로그램을 중단해야 할 때가 있습니다. 가장 간단한 방법은 `Ctrl-C`이며, 대개 명령이 멈춥니다. 어떻게 작동하며, 어떤 때는 왜 멈추지 않을까요?

```console
$ sleep 100
^C
$
```

> `^C`는 터미널에서 `Ctrl-C`를 표시하는 방식입니다.

여기서 일어난 과정은 다음과 같습니다.

1. `Ctrl-C`를 눌렀습니다.
2. 터미널이 특수 키 조합을 인식했습니다.
3. `sleep` 프로세스에 SIGINT 시그널이 전달됐습니다.
4. 시그널이 `sleep`의 실행을 중단했습니다.

시그널은 특수한 통신 수단입니다. 프로세스는 시그널을 받으면 하던 일을 잠시 멈추고 시그널을 처리하며, 전달된 정보에 따라 실행 흐름이 바뀔 수 있습니다. 그래서 시그널을 *소프트웨어 인터럽트*라고도 합니다.

`Ctrl-C`는 프로세스에 `SIGINT`를 전달합니다. 다음 Python 예제는 `SIGINT`를 잡아 무시하므로 더 이상 멈추지 않습니다. 이 프로그램은 `Ctrl-\`로 `SIGQUIT`를 보내 종료할 수 있습니다.

```python
#!/usr/bin/env python
import signal, time

def handler(signum, time):
    print("\nI got a SIGINT, but I am not stopping")

signal.signal(signal.SIGINT, handler)
i = 0
while True:
    time.sleep(.1)
    print("\r{}".format(i), end="")
    i += 1
```

`SIGINT`를 두 번 보낸 뒤 `SIGQUIT`를 보내면 다음과 같습니다. `^`는 터미널에서 `Ctrl`을 표시합니다.

```console
$ python sigint.py
24^C
I got a SIGINT, but I am not stopping
26^C
I got a SIGINT, but I am not stopping
30^\[1]    39913 quit       python sigint.py
```

`SIGINT`와 `SIGQUIT`는 대개 터미널 요청과 관련이 있습니다. 프로세스에 정상 종료를 요청할 때 더 일반적으로 쓰는 시그널은 `SIGTERM`입니다. [`kill`](https://www.man7.org/linux/man-pages/man1/kill.1.html)을 `kill -TERM <PID>` 형식으로 실행하면 됩니다.

시그널은 종료 이외의 일도 합니다. `SIGSTOP`은 프로세스를 일시 정지합니다. 터미널에서 `Ctrl-Z`를 누르면 Terminal Stop의 약자인 `SIGTSTP`가 전달됩니다. 터미널에서 사용하는 정지 시그널입니다.

정지한 작업은 [`fg`](https://www.man7.org/linux/man-pages/man1/fg.1p.html)로 포그라운드에서, [`bg`](https://man7.org/linux/man-pages/man1/bg.1p.html)로 백그라운드에서 다시 실행할 수 있습니다.

[`jobs`](https://www.man7.org/linux/man-pages/man1/jobs.1p.html)는 현재 터미널 세션에서 아직 끝나지 않은 작업을 나열합니다. 작업은 PID로 참조할 수 있으며, PID는 [`pgrep`](https://www.man7.org/linux/man-pages/man1/pgrep.1.html)으로 찾을 수 있습니다. 더 직관적으로는 `%` 뒤에 `jobs`가 보여 주는 작업 번호를 붙여 참조할 수 있습니다. 마지막으로 백그라운드에서 실행한 작업은 `$!`로 참조합니다.

명령 끝에 `&`를 붙이면 백그라운드에서 실행하며 프롬프트를 돌려줍니다. 여전히 셸의 표준 출력에 내용을 표시하므로 불편하면 리다이렉션을 쓰세요. 실행 중인 프로그램은 `Ctrl-Z` 다음 `bg`를 입력해 백그라운드로 보낼 수 있습니다.

백그라운드 프로세스도 터미널의 자식 프로세스이므로, 터미널을 닫을 때 `SIGHUP`이 전달되어 종료될 수 있습니다. 이를 막으려면 `SIGHUP`을 무시하는 래퍼인 [`nohup`](https://www.man7.org/linux/man-pages/man1/nohup.1.html)으로 실행하거나, 이미 실행 중이라면 `disown`을 사용하세요. 뒤에서 볼 터미널 멀티플렉서도 방법입니다.

다음 세션에서 몇 가지 개념을 확인할 수 있습니다.

```
$ sleep 1000
^Z
[1]  + 18653 suspended  sleep 1000

$ nohup sleep 2000 &
[2] 18745
appending output to nohup.out

$ jobs
[1]  + suspended  sleep 1000
[2]  - running    nohup sleep 2000

$ kill -SIGHUP %1
[1]  + 18653 hangup     sleep 1000

$ kill -SIGHUP %2   # nohup protects from SIGHUP

$ jobs
[2]  + running    nohup sleep 2000

$ kill %2
[2]  + 18745 terminated  nohup sleep 2000
```

`SIGKILL`은 프로세스가 잡아서 처리할 수 없으며 즉시 종료시키는 특별한 시그널입니다. 다만 자식 프로세스를 고아 프로세스로 남기는 등의 부작용이 있을 수 있습니다.

다른 시그널까지 자세히 알아보려면 [시그널 설명](https://en.wikipedia.org/wiki/Signal_(IPC)), [`man signal`](https://www.man7.org/linux/man-pages/man7/signal.7.html), `kill -l`을 참고하세요.

셸 스크립트에서는 내장 명령 `trap`으로 시그널을 받았을 때 실행할 명령을 지정합니다. 정리 작업에 유용합니다.

```shell
#!/usr/bin/env bash
cleanup() {
    echo "Cleaning up temporary files..."
    rm -f /tmp/mytemp.*
}
trap cleanup EXIT  # Run cleanup when script exits
trap cleanup SIGINT SIGTERM  # Also on Ctrl-C or kill
```

{% comment %}
### 사용자, 파일, 권한

프로그램은 파일을 통해서도 간접적으로 통신합니다. 파일과 폴더를 읽고 쓰고 삭제하려면 파일 권한이 해당 작업을 허용해야 합니다.

```console
$ ls -l notes.txt
-rw-r--r--  1 alice  users  12693 Jan 11 23:05 notes.txt
```

소유자는 `alice`, 그룹은 `users`입니다. `rw-r--r--`은 권한을 줄여 쓴 것으로, `alice`에게는 읽기·쓰기 권한(`rw-`), 그룹과 나머지 사용자에게는 읽기 권한만 있습니다.

```console
$ ./script.sh
# permission denied
$ chmod +x script.sh
$ ls -l script.sh
-rwxr-xr-x  1 alice  users  3125 Jan 11 23:07 script.sh
$ ./script.sh
```

스크립트를 실행하려면 실행 권한이 필요하므로 `chmod`(change mode)를 사용합니다. 처음에는 문법이 낯설 수 있습니다. 예제로 배우는 편을 좋아한다면 `tldr`를 먼저 설치해 사용하세요.

```console
❯ tldr chmod
  Change the access permissions of a file or directory.
  More information: <https://www.gnu.org/software/coreutils/chmod>.

  Give the [u]ser who owns a file the right to e[x]ecute it:

      chmod u+x path/to/file

  Give the [u]ser rights to [r]ead and [w]rite to a file/directory:

      chmod u+rw path/to/file_or_directory

  Give [a]ll users rights to [r]ead and e[x]ecute:

      chmod a+rx path/to/file
```

` tldr chmod`를 실행하면 재귀 작업과 그룹 권한 등 더 많은 예제를 볼 수 있습니다.

> `command not found: tldr`가 나온다면 아직 설치되지 않은 것입니다. 대부분의 시스템에는 기본 설치되어 있지 않습니다. [command-not-found.com](https://command-not-found.com)에서 운영체제별로 많은 CLI 도구의 설치 방법을 찾을 수 있습니다.

모든 프로그램은 특정 사용자로 실행됩니다. `whoami`는 사용자 이름을, `id -u`는 운영체제가 부여한 정수 식별자인 UID를 보여 줍니다.

`sudo command`는 대부분의 권한 제한을 우회할 수 있는 루트 사용자로 명령을 실행합니다. `sudo whoami`, `sudo id -u`로 결과를 비교하세요. 비밀번호를 요구할 수 있습니다. 파일·폴더의 소유자는 `chown`으로 바꿉니다.

[Unix 파일 권한](https://en.wikipedia.org/wiki/File-system_permissions#Traditional_Unix_permissions)을 더 알아보세요. 지금까지는 로컬 컴퓨터에 집중했지만, 원격 서버에서는 이 기술이 더 유용해집니다.
{% endcomment %}

# 원격 컴퓨터
{: #remote-machines}

프로그래머가 일상적으로 원격 서버에서 작업하는 일이 점점 흔해집니다. 가장 일반적인 도구는 SSH(Secure Shell)입니다. 원격 서버에 접속해 익숙한 셸 인터페이스를 사용할 수 있습니다.

```bash
ssh alice@server.mit.edu
```

`server.mit.edu` 서버에 사용자 `alice`로 접속합니다.

자주 놓치는 `ssh` 기능은 비대화형 명령 실행입니다. 명령의 stdin 전송과 stdout 수신을 처리하므로 다른 명령과 조합할 수 있습니다.

```shell
# here ls runs in the remote, and wc runs locally
ssh alice@server ls | wc -l

# here both ls and wc run in the server
ssh alice@server 'ls | wc -l'

```

> 연결 끊김, 절전 진입·해제, 네트워크 전환, 높은 지연에 대응하는 SSH 대안 [Mosh](https://mosh.org/)도 사용해 보세요.

원격 서버에서 명령을 실행하려면 권한을 증명해야 합니다. 비밀번호나 SSH 키를 사용할 수 있습니다. 키 인증은 공개 키 암호로 비밀인 개인 키를 공개하지 않고도 소유 사실을 증명합니다. 더 편리하고 안전하므로 키 인증을 권장합니다. 개인 키(흔히 `~/.ssh/id_rsa`, 최근에는 `~/.ssh/id_ed25519`)는 사실상 비밀번호이므로 내용을 공유하지 마세요.

키 쌍은 [`ssh-keygen`](https://www.man7.org/linux/man-pages/man1/ssh-keygen.1.html)으로 생성합니다.

```bash
ssh-keygen -a 100 -t ed25519 -f ~/.ssh/id_ed25519
```

GitHub 푸시를 위해 SSH 키를 설정했다면 [이 절차](https://help.github.com/articles/connecting-to-github-with-ssh/)를 이미 따라 했을 수 있습니다. `ssh-keygen -y -f /path/to/key`로 암호문구 설정 여부와 유효성을 확인할 수 있습니다.

서버는 `.ssh/authorized_keys`를 보고 접속을 허용할 클라이언트를 결정합니다. 공개 키를 복사하려면 다음 명령을 사용합니다.

```bash
cat .ssh/id_ed25519.pub | ssh alice@remote 'cat >> ~/.ssh/authorized_keys'

# or more simply (if ssh-copy-id is available)

ssh-copy-id -i .ssh/id_ed25519 alice@remote
```

SSH 연결로 파일도 안전하게 주고받을 수 있습니다. 전통적인 도구는 [`scp`](https://www.man7.org/linux/man-pages/man1/scp.1.html)이며, 문법은 `scp path/to/local_file remote_host:path/to/remote_file`입니다. [`rsync`](https://www.man7.org/linux/man-pages/man1/rsync.1.html)는 로컬과 원격에서 같은 파일을 감지해 다시 복사하지 않습니다. 심볼릭 링크와 권한을 더 세밀하게 다루고, 중단된 복사를 이어갈 수 있게 하는 `--partial` 등의 기능도 제공합니다. 문법은 `scp`와 비슷합니다.

SSH 클라이언트 설정 파일 `~/.ssh/config`에는 호스트와 기본 설정을 선언할 수 있습니다. `ssh`뿐 아니라 `scp`, `rsync`, `mosh` 등도 이 파일을 읽습니다.

```bash
Host vm
    User alice
    HostName 172.16.174.141
    Port 2222
    IdentityFile ~/.ssh/id_ed25519

# Configs can also take wildcards
Host *.mit.edu
    User alice
```

# 터미널 멀티플렉서
{: #terminal-multiplexers}

명령줄에서 편집기와 프로그램을 나란히 실행하는 등 여러 작업을 동시에 하고 싶을 때가 많습니다. 터미널 창을 새로 열 수도 있지만, 터미널 멀티플렉서는 더 유연한 해결책입니다.

[`tmux`](https://www.man7.org/linux/man-pages/man1/tmux.1.html) 같은 도구는 탭과 분할 창으로 여러 셸 세션을 효율적으로 다룹니다. 현재 터미널 세션에서 분리했다가 나중에 다시 연결할 수도 있습니다. 원격 컴퓨터에서 특히 편리하며, `nohup` 같은 방법을 따로 쓸 필요가 없습니다.

널리 쓰이는 [`tmux`](https://www.man7.org/linux/man-pages/man1/tmux.1.html)는 설정이 다양하며, 단축키로 탭과 분할 창을 만들고 빠르게 이동합니다.

단축키의 `<C-b> x`는 (1) `Ctrl+b`를 누르고, (2) 손을 뗀 뒤, (3) `x`를 누르라는 뜻입니다. `tmux`의 구조는 다음과 같습니다.

- **세션**: 창을 하나 이상 가진 독립된 작업 공간입니다.
  - `tmux`: 새 세션을 시작합니다.
  - `tmux new -s NAME`: 이름을 지정해 시작합니다.
  - `tmux ls`: 현재 세션을 나열합니다.
  - `<C-b> d`: 현재 세션에서 분리합니다.
  - `tmux a`: 마지막 세션에 다시 연결합니다. `-t`로 세션을 지정할 수 있습니다.
- **창**: 편집기나 브라우저의 탭처럼 같은 세션 안에서 시각적으로 구분됩니다.
  - `<C-b> c`: 새 창을 만듭니다. `<C-d>`로 셸을 종료하면 닫을 수 있습니다.
  - `<C-b> N`: 번호가 *N*인 창으로 이동합니다.
  - `<C-b> p`, `<C-b> n`: 이전·다음 창으로 이동합니다.
  - `<C-b> ,`: 현재 창의 이름을 바꿉니다.
  - `<C-b> w`: 창 목록을 봅니다.
- **분할 창(pane)**: Vim의 분할 화면처럼 한 화면에 여러 셸을 보여 줍니다.
  - `<C-b> "`: 현재 영역을 가로 경계로 나눕니다.
  - `<C-b> %`: 현재 영역을 세로 경계로 나눕니다.
  - `<C-b> <방향키>`: 해당 방향의 영역으로 이동합니다.
  - `<C-b> z`: 현재 영역의 확대를 켜거나 끕니다.
  - `<C-b> [`: 스크롤 모드로 들어갑니다. `<space>`로 선택을 시작하고 `<enter>`로 복사합니다.
  - `<C-b> <space>`: 분할 배치를 순환합니다.

> [간단한 튜토리얼](https://www.hamvocke.com/blog/a-quick-and-easy-guide-to-tmux/)과 [더 자세한 설명](https://linuxcommand.org/lc3_adv_termmux.php)도 참고하세요.

tmux와 SSH를 갖췄다면 어느 컴퓨터에서든 익숙한 환경으로 작업하고 싶을 것입니다. 이를 위해 셸을 설정해 봅시다.

# 셸 설정하기
{: #customizing-the-shell}

많은 명령줄 프로그램은 *닷파일(dotfile)*이라는 일반 텍스트 파일로 설정합니다. `~/.vimrc`처럼 이름이 `.`으로 시작해 기본 `ls` 목록에서 숨겨지기 때문에 붙은 이름입니다.

> 이름 앞의 점으로 목록에서 숨기는 것도 셸 환경의 관례입니다.

셸도 이런 파일을 사용합니다. 시작할 때 여러 파일을 읽어 설정을 불러옵니다. 셸 종류와 로그인·대화형 세션 여부에 따라 과정이 복잡해질 수 있습니다. [이 자료](https://web.archive.org/web/20260329133158/https://blog.flowblok.id.au/2013-02/shell-startup-scripts.html)가 잘 설명합니다.

bash는 대부분의 시스템에서 `.bashrc`나 `.bash_profile`을 수정하면 됩니다. 다른 예는 다음과 같습니다.

- `bash`: `~/.bashrc`, `~/.bash_profile`
- `git`: `~/.gitconfig`
- `vim`: `~/.vimrc`, `~/.vim` 폴더
- `ssh`: `~/.ssh/config`
- `tmux`: `~/.tmux.conf`

프로그램 검색 경로를 추가하는 것은 흔한 설정입니다. 소프트웨어를 설치할 때 자주 보게 됩니다.

```shell
export PATH="$PATH:path/to/append"
```

기존 `$PATH`에 새 경로를 붙이고 모든 자식 프로세스가 그 값을 상속하게 합니다. 이제 자식 프로세스도 `path/to/append`의 프로그램을 찾을 수 있습니다.

셸을 꾸미다 보면 새 명령줄 도구도 설치하게 됩니다. 패키지 관리자는 다운로드·설치·업데이트를 처리합니다. macOS는 [Homebrew](https://brew.sh/), Ubuntu/Debian은 `apt`, Fedora는 `dnf`, Arch는 `pacman`을 사용합니다. 코드 배포 강의에서 더 자세히 다룹니다.

macOS의 Homebrew로 유용한 도구 두 개를 설치하는 예입니다.

```shell
# ripgrep: a faster grep with better defaults
brew install ripgrep

# fd: a faster, user-friendly find
brew install fd
```

설치하면 `grep` 대신 `rg`, `find` 대신 `fd`를 사용할 수 있습니다.

> **`curl | bash` 주의**: 설치 안내에서 `curl -fsSL https://example.com/install.sh | bash`를 자주 봅니다. 다운로드한 스크립트를 즉시 실행하므로 편리하지만, 내용을 확인하지 않은 코드를 실행한다는 위험이 있습니다. 먼저 다운로드하고 검토한 뒤 실행하는 편이 안전합니다.
> ```shell
> curl -fsSL https://example.com/install.sh -o install.sh
> less install.sh  # review the script
> bash install.sh
> ```
> 일부 설치 도구는 `/bin/bash -c "$(curl -fsSL https://url)"`을 사용합니다. 적어도 현재 셸 대신 bash가 스크립트를 해석하도록 보장하는 변형입니다.

설치하지 않은 명령을 실행하면 `command not found`가 나옵니다. [command-not-found.com](https://command-not-found.com)에서 배포판과 패키지 관리자별 설치법을 찾을 수 있습니다.

[`tldr`](https://tldr.sh/)는 예제 중심으로 간소화한 매뉴얼을 제공합니다. 긴 문서를 읽지 않고도 흔한 사용법을 빠르게 볼 수 있습니다.

```console
$ tldr fd
  An alternative to find.
  Aims to be faster and easier to use than find.

  Recursively find files matching a pattern in the current directory:
      fd "pattern"

  Find files that begin with "foo":
      fd "^foo"

  Find files with a specific extension:
      fd --extension txt
```

새 프로그램 대신 특정 플래그가 붙은 명령의 단축형만 필요할 때는 별칭을 사용합니다. 내장 명령 `alias`로 만들 수 있습니다. 셸은 명령을 해석하기 전에 별칭을 원래 명령으로 바꿉니다. bash에서는 다음 형식입니다.

```bash
alias alias_name="command_to_alias arg1 arg2"
```

> [`alias`](https://www.man7.org/linux/man-pages/man1/alias.1p.html)는 이 정의를 하나의 인자로 받는 셸 명령이므로 `=` 양옆에 공백을 넣지 않습니다.

별칭은 여러 상황에서 편리합니다.

```bash
# Make shorthands for common flags
alias ll="ls -lh"

# Save a lot of typing for common commands
alias gs="git status"
alias gc="git commit"

# Save you from mistyping
alias sl=ls

# Overwrite existing commands for better defaults
alias mv="mv -i"           # -i prompts before overwrite
alias mkdir="mkdir -p"     # -p make parent dirs as needed
alias df="df -h"           # -h prints human readable format

# Alias can be composed
alias la="ls -A"
alias lla="la -l"

# To ignore an alias run it prepended with \
\ls
# Or disable an alias altogether with unalias
unalias la

# To get an alias definition just call it with alias
alias ll
# Will print ll='ls -lh'
```

다만 별칭은 명령 중간에 인자를 받지 못합니다. 더 복잡한 동작에는 셸 함수를 사용하세요.

대부분의 셸은 `Ctrl-R`로 명령 기록을 역방향 검색합니다. 키를 누르고 입력을 시작하면 됩니다. 앞서 본 `fzf`의 셸 통합을 설정하면 `Ctrl-R`이 전체 기록을 대화형으로 퍼지 검색하는 더 강력한 기능이 됩니다.

닷파일은 별도 폴더에서 버전 관리하고, 스크립트로 필요한 위치에 **심볼릭 링크**를 만드는 것이 좋습니다. 장점은 다음과 같습니다.

- **간편한 설치**: 새 컴퓨터에 로그인해도 잠깐이면 설정을 적용할 수 있습니다.
- **이식성**: 어디서든 도구를 같은 방식으로 사용합니다.
- **동기화**: 어느 컴퓨터에서든 설정을 바꾸고 동기화할 수 있습니다.
- **변경 추적**: 프로그래머로 일하는 내내 관리할 수 있으므로, 오랫동안 유지하는 프로젝트처럼 버전 기록이 유용합니다.

어떤 설정을 넣으면 좋을까요? 온라인 문서나 [매뉴얼 페이지](https://en.wikipedia.org/wiki/Man_page)를 읽고, 프로그램별 설정을 소개하는 블로그를 찾아보세요. 다른 사람의 닷파일도 배울 거리가 많습니다. GitHub에는 [닷파일 저장소](https://github.com/search?o=desc&q=dotfiles&s=stars&type=Repositories)가 많으며 [이 저장소](https://github.com/mathiasbynens/dotfiles)가 특히 인기가 있습니다. 다만 설정을 무작정 복사하지는 마세요. [이 사이트](https://dotfiles.github.io/)도 참고할 만합니다.

강사진의 닷파일도 공개되어 있습니다: [Anish](https://github.com/anishathalye/dotfiles), [Jon](https://github.com/jonhoo/configs), [Jose](https://github.com/jjgo/dotfiles).

**프레임워크와 플러그인**으로 셸을 개선할 수도 있습니다. 종합 프레임워크로 [prezto](https://github.com/sorin-ionescu/prezto), [oh-my-zsh](https://ohmyz.sh/)가 있으며, 특정 기능을 제공하는 플러그인도 있습니다.

- [zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting): 입력 중 명령의 유효 여부를 색으로 표시합니다.
- [zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions): 입력에 맞춰 기록의 명령을 제안합니다.
- [zsh-completions](https://github.com/zsh-users/zsh-completions): 자동 완성 정의를 추가합니다.
- [zsh-history-substring-search](https://github.com/zsh-users/zsh-history-substring-search): fish 방식의 기록 검색을 제공합니다.
- [powerlevel10k](https://github.com/romkatv/powerlevel10k): 빠르고 설정 가능한 프롬프트 테마입니다.

[fish](https://fishshell.com/) 같은 셸에는 많은 기능이 기본으로 포함됩니다.

> 이런 기능에 반드시 oh-my-zsh 같은 큰 프레임워크가 필요한 것은 아닙니다. 플러그인을 따로 설치하는 편이 더 빠르고 세밀하게 제어하기 쉽습니다. 큰 프레임워크는 셸 시작을 느리게 할 수 있으므로 실제로 쓰는 것만 설치하는 방법도 고려하세요.

# 셸에서 AI 활용하기
{: #ai-in-the-shell}

셸에 AI 도구를 통합하는 방법은 다양합니다. 통합 수준별로 몇 가지 예를 살펴보겠습니다.

**명령 생성**: [`simonw/llm`](https://github.com/simonw/llm) 같은 도구는 자연어 설명에서 셸 명령을 만들 수 있습니다.

```console
$ llm cmd "find all python files modified in the last week"
find . -name "*.py" -mtime -7
```

**파이프라인 통합**: LLM을 파이프라인에 넣어 데이터를 처리하고 변환할 수 있습니다. 특히 형식이 제각각이어서 정규 표현식으로 추출하기 번거로운 데이터에 유용합니다.

```console
$ cat users.txt
Contact: john.doe@example.com
User 'alice_smith' logged in at 3pm
Posted by: @bob_jones on Twitter
Author: Jane Doe (jdoe)
Message from mike_wilson yesterday
Submitted by user: sarah.connor
$ INSTRUCTIONS="Extract just the username from each line, one per line, nothing else"
$ llm "$INSTRUCTIONS" < users.txt
john.doe
alice_smith
bob_jones
jdoe
mike_wilson
sarah.connor
```

변수에 공백이 있으므로 `"$INSTRUCTIONS"`에 따옴표를 썼고, `< users.txt`로 파일 내용을 표준 입력에 전달했다는 점을 보세요.

**AI 셸**: [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 같은 도구는 자연어 명령을 셸 작업, 파일 편집, 여러 단계의 복잡한 작업으로 바꾸는 메타 셸처럼 동작합니다.

# 터미널 에뮬레이터
{: #terminal-emulators}

셸 설정뿐 아니라 **터미널 에뮬레이터**의 선택과 설정에도 시간을 들일 가치가 있습니다. 터미널 에뮬레이터는 셸이 실행되는 텍스트 인터페이스를 제공하는 GUI 프로그램이며, 종류가 다양합니다.

터미널에서 수백~수천 시간을 보낼 수 있으므로 다음과 같은 설정을 살펴보세요.

- 글꼴
- 색 구성
- 키보드 단축키
- 탭·분할 창 지원
- 이전 출력 스크롤 설정
- 성능: [Alacritty](https://github.com/alacritty/alacritty), [Ghostty](https://ghostty.org/) 같은 최신 터미널은 GPU 가속을 제공합니다.

# 연습문제
{: #exercises}

## 인자와 글로브
{: #arguments-and-globs}

1. `cmd --flag -- --notaflag`에서 `--`는 플래그 해석을 끝내라는 특수 인자입니다. 그 뒤는 모두 위치 인자로 처리합니다. 왜 유용할까요? `touch -- -myfile`을 실행한 뒤 `--` 없이 지워 보세요.

1. [`man ls`](https://www.man7.org/linux/man-pages/man1/ls.1.html)를 읽고 숨김 파일을 포함한 모든 파일을, 읽기 쉬운 크기(예: 454279954 대신 454M)로, 최근 수정 순서로, 색을 사용해 출력하는 `ls` 명령을 작성하세요. 예시는 다음과 같습니다.

    ```
    -rw-r--r--   1 user group 1.1M Jan 14 09:53 baz
    drwxr-xr-x   5 user group  160 Jan 14 09:53 .
    -rw-r--r--   1 user group  514 Jan 14 06:42 bar
    -rw-r--r--   1 user group 106M Jan 13 12:12 foo
    drwx------+ 47 user group 1.5K Jan 12 18:08 ..
    ```

{% comment %}
ls -lath --color=auto
{% endcomment %}

1. 프로세스 치환 `<(command)`으로 명령 출력을 파일처럼 사용할 수 있습니다. `diff`와 프로세스 치환으로 `printenv`와 `export`의 출력을 비교하세요. 왜 다를까요? 힌트: `diff <(printenv | sort) <(export | sort)`.

## 환경 변수
{: #environment-variables-1}

1. bash 함수 `marco`와 `polo`를 작성하세요. `marco`는 현재 작업 디렉터리를 저장하고, `polo`는 어디에서 실행하든 그 디렉터리로 `cd`해야 합니다. `marco.sh`에 작성하고 `source marco.sh`로 정의를 다시 불러오면 디버깅하기 편합니다.

{% comment %}
marco() {
    export MARCO=$(pwd)
}
polo() {
    cd "$MARCO"
}
{% endcomment %}

## 종료 코드
{: #return-codes-1}

1. 드물게 실패하는 명령을 디버깅하려면 출력을 확보해야 하지만 실패를 기다리는 데 시간이 걸립니다. 다음 스크립트가 실패할 때까지 실행하고, 표준 출력과 표준 오류를 파일에 저장한 뒤 마지막에 모두 출력하는 bash 스크립트를 작성하세요. 실패까지 실행한 횟수도 출력하면 좋습니다.

    ```bash
    #!/usr/bin/env bash

    n=$(( RANDOM % 100 ))

    if [[ $n -eq 42 ]]; then
       echo "Something went wrong"
       >&2 echo "The error was using magic numbers"
       exit 1
    fi

    echo "Everything went according to plan"
    ```

{% comment %}
#!/usr/bin/env bash
count=0
until [[ "$?" -ne 0 ]];
do
  count=$((count+1))
  ./random.sh &> out.txt
done
echo "found error after $count runs"
cat out.txt
{% endcomment %}

## 시그널과 작업 제어
{: #signals-and-job-control}

1. 터미널에서 `sleep 10000`을 실행하고 `Ctrl-Z`로 정지한 뒤 `bg`로 백그라운드에서 재개하세요. [`pgrep`](https://www.man7.org/linux/man-pages/man1/pgrep.1.html)으로 PID를 찾고, PID를 직접 입력하지 않고 [`pkill`](https://man7.org/linux/man-pages/man1/pgrep.1.html)로 종료하세요. 힌트: `-lf` 플래그.

1. 다른 프로세스가 끝난 뒤에만 새 프로세스를 시작하려면 어떻게 할까요? 기다릴 프로세스로 `sleep 60 &`를 사용합니다. [`wait`](https://www.man7.org/linux/man-pages/man1/wait.1p.html)를 사용해 `ls`가 백그라운드 프로세스 종료를 기다리도록 해 보세요.

   `wait`는 자식 프로세스에만 적용되므로 다른 bash 세션에서는 이 방법이 통하지 않습니다. `kill`은 성공하면 0, 실패하면 0이 아닌 종료 코드를 반환합니다. `kill -0`은 시그널을 보내지 않지만 프로세스가 없으면 실패합니다. PID를 받아 해당 프로세스가 끝날 때까지 기다리는 `pidwait` 함수를 작성하세요. CPU를 낭비하지 않도록 `sleep`을 사용하세요.

## 파일과 권한
{: #files-and-permissions}

1. (심화) 디렉터리에서 가장 최근에 수정된 파일을 재귀적으로 찾는 명령이나 스크립트를 작성하세요. 더 일반적으로 모든 파일을 최근 수정 순서로 나열할 수 있나요?

## 터미널 멀티플렉서
{: #terminal-multiplexers-1}

1. [tmux 튜토리얼](https://www.hamvocke.com/blog/a-quick-and-easy-guide-to-tmux/)을 따라 한 뒤, [설정 안내](https://www.hamvocke.com/blog/a-guide-to-customizing-your-tmux-conf/)로 기본적인 사용자 설정을 배워 보세요.

## 별칭과 닷파일
{: #aliases-and-dotfiles}

1. 오타에 대비해 `dc`를 `cd`로 바꾸는 별칭을 만드세요.
1. `history | awk '{$1="";print substr($0,2)}' | sort | uniq -c | sort -n | tail -n 10`으로 자주 쓴 명령 10개를 찾고 짧은 별칭을 만들어 보세요. Bash용 명령이므로 ZSH에서는 `history` 대신 `history 1`을 사용하세요.
1. 닷파일 폴더를 만들고 버전 관리를 시작하세요.
1. 셸 등 최소 한 프로그램의 설정을 추가하세요. 처음에는 `$PS1`로 프롬프트를 바꾸는 정도도 좋습니다.
1. 새 컴퓨터에 수작업 없이 빠르게 설정을 설치할 방법을 마련하세요. 각 파일에 `ln -s`를 실행하는 스크립트나 [전용 도구](https://dotfiles.github.io/utilities/)를 사용할 수 있습니다.
1. 새 가상 머신에서 설치 스크립트를 시험하세요.
1. 현재 사용하는 도구 설정을 모두 닷파일 저장소로 옮기세요.
1. 닷파일을 GitHub에 공개하세요.

## 원격 컴퓨터: SSH
{: #remote-machines-ssh}

Linux 가상 머신을 설치하거나 기존 머신을 사용하세요. 익숙하지 않다면 [이 설치 튜토리얼](https://hibbard.eu/install-ubuntu-virtual-box/)을 참고하세요.

1. `~/.ssh/`에 SSH 키 쌍이 있는지 확인하세요. 없다면 `ssh-keygen -a 100 -t ed25519`로 생성하세요. 암호문구와 `ssh-agent` 사용을 권장합니다. [자세한 설명](https://www.ssh.com/ssh/agent)을 참고하세요.
1. `.ssh/config`에 다음 항목을 추가하세요.

    ```bash
    Host vm
        User username_goes_here
        HostName ip_goes_here
        IdentityFile ~/.ssh/id_ed25519
        LocalForward 9999 localhost:8888
    ```

1. `ssh-copy-id vm`으로 공개 키를 서버에 복사하세요.
1. VM에서 `python -m http.server 8888`로 웹 서버를 시작하고, 로컬 컴퓨터의 `http://localhost:9999`로 접속하세요.
1. `sudo vim /etc/ssh/sshd_config`로 서버 설정을 열고 `PasswordAuthentication`을 바꿔 비밀번호 인증을 끄세요. `PermitRootLogin`으로 루트 로그인을 끄세요. `sudo service sshd restart`로 서비스를 재시작한 뒤 다시 SSH 접속을 해 보세요.
1. (도전) VM에 [`mosh`](https://mosh.org/)를 설치해 접속하고, 서버나 VM의 네트워크 어댑터 연결을 끊으세요. mosh가 연결을 복구하나요?
1. (도전) `ssh`의 `-N`, `-f` 플래그를 알아보고 백그라운드 포트 포워딩 명령을 작성하세요.
