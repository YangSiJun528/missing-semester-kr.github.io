---
layout: lecture
title: "데이터 가공"
lang: ko
presenter: Jon
date: 2019-01-17
order: 2
video:
  aspect: 56.25
  id: VW2jn9Okjhw
---

텍스트가 잔뜩 있는데 이를 가공하고 싶었던 적이 있나요? 바로 그런 작업이 데이터 가공(data wrangling)입니다. 원하는 결과를 얻을 때까지 데이터를 한 형식에서 다른 형식으로 바꾸는 과정입니다.

이미 간단한 예를 봤습니다. `journalctl | grep -i intel`입니다.

- 대소문자를 구분하지 않고 Intel을 언급한 시스템 로그를 모두 찾습니다.
- 데이터 가공의 상당 부분은 어떤 도구가 있는지 알고, 이를 어떻게 조합할지 이해하는 데 달려 있습니다.

처음부터 시작해 봅시다. 데이터의 출처와 할 일이 필요합니다. 로그는 좋은 예입니다. 조사할 일이 많지만 전체를 읽기는 어렵기 때문입니다. 제 서버에 누가 로그인하려 하는지 로그로 알아보겠습니다.

```bash
ssh myserver journalctl
```

출력이 너무 많습니다. SSH 관련 내용만 남겨 봅시다.

```bash
ssh myserver journalctl | grep sshd
```

파이프로 *원격* 데이터를 로컬 컴퓨터의 `grep`에 보내고 있습니다! SSH로 이런 일도 할 수 있습니다. 그래도 여전히 출력이 많고 읽기 어렵습니다. 더 좁혀 봅시다.

```bash
ssh myserver journalctl | grep sshd | grep "Disconnected from"
```

불필요한 내용이 아직 많습니다. 이를 없애는 방법은 여러 가지지만, 강력한 도구 중 하나인 `sed`를 살펴보겠습니다.

`sed`는 오래된 편집기 `ed`를 바탕으로 한 "스트림 편집기"입니다. 내용을 직접 편집하기보다는 어떻게 수정할지 짧은 명령으로 지정합니다. 명령은 많지만 가장 흔히 쓰는 것 중 하나가 치환 명령 `s`입니다.

아래 예제들은 파이프의 단계를 보기 쉽도록 여러 줄로 나눠 표시했습니다. 셸에서 실행할 때는 한 줄로 이어 쓰거나, 줄 끝에 `\`를 붙여 다음 줄로 이어야 합니다.

```bash
ssh myserver journalctl
 | grep sshd
 | grep "Disconnected from"
 | sed 's/.*Disconnected from //'
```

여기서 사용한 것은 간단한 *정규 표현식*입니다. 텍스트가 특정 패턴과 일치하는지 찾는 강력한 표현 방법입니다. `s` 명령은 `s/REGEX/SUBSTITUTION/` 형태입니다. `REGEX`는 찾을 정규 표현식이고, `SUBSTITUTION`은 일치한 부분을 바꿀 텍스트입니다.

## 정규 표현식
{: id="regular-expressions"}

정규 표현식은 자주 쓰이고 유용하므로 시간을 들여 원리를 알아둘 만합니다. 앞서 사용한 `/.*Disconnected from /`을 살펴봅시다. 정규 표현식은 흔히 `/`로 감싸지만 항상 그런 것은 아닙니다. 대부분의 ASCII 문자는 그대로 그 문자와 일치합니다. 일부 문자는 특별한 의미가 있습니다. 구현마다 세부 문법이 달라 혼란스럽기도 합니다. 흔히 사용하는 패턴은 다음과 같습니다.

- `.`: 줄바꿈을 제외한 임의의 한 문자
- `*`: 바로 앞 패턴을 0번 이상 반복
- `+`: 바로 앞 패턴을 1번 이상 반복
- `[abc]`: `a`, `b`, `c` 중 한 문자
- `(RX1|RX2)`: `RX1` 또는 `RX2`와 일치하는 부분
- `^`: 줄 시작
- `$`: 줄 끝

`sed`의 기본 정규 표현식에서는 괄호 같은 일부 기호 앞에 `\`를 붙여야 특별한 의미가 생깁니다. `-E` 옵션으로 확장 정규 표현식을 사용할 수도 있습니다.

`/.*Disconnected from /`으로 돌아가 봅시다. 임의의 문자가 0개 이상 나온 뒤 문자 그대로 `Disconnected from `이 이어지는 부분과 일치합니다. 원하는 동작처럼 보입니다. 하지만 정규 표현식은 주의해서 써야 합니다. 누군가 사용자 이름을 "Disconnected from"으로 지정해 로그인을 시도하면 어떨까요?

```
Jan 17 03:13:00 thesquareplanet.com sshd[2631]: Disconnected from invalid user Disconnected from 46.97.239.16 port 55920 [preauth]
```

어떤 결과가 나올까요? `*`와 `+`는 기본적으로 "탐욕적"입니다. 가능한 한 많은 문자와 일치하려고 합니다. 따라서 결과는 다음만 남습니다.

```
46.97.239.16 port 55920 [preauth]
```

원했던 결과가 아닐 수 있습니다. 일부 정규 표현식 구현에서는 `*`나 `+` 뒤에 `?`를 붙여 비탐욕적으로 만들 수 있지만, `sed`는 이를 지원하지 않습니다. 이를 지원하는 Perl의 명령줄 모드를 쓸 수는 있습니다.

```bash
perl -pe 's/.*?Disconnected from //'
```

그래도 나머지 설명에서는 이런 작업에 널리 쓰이는 `sed`를 계속 사용하겠습니다. `sed`는 특정 패턴 다음 줄을 출력하거나, 한 번에 여러 치환을 수행하거나, 텍스트를 찾는 등 여러 기능을 제공합니다. 자세히 다루지는 않겠습니다. `sed`만으로도 강의 하나가 될 만큼 내용이 많고, 작업에 따라 더 나은 도구도 있습니다.

줄 뒤쪽에서 지우고 싶은 부분도 있습니다. 어떻게 할까요? 사용자 이름에 공백 등이 들어갈 수 있다면 그 뒤의 텍스트만 찾기가 까다롭습니다. 이럴 때는 줄 *전체*와 일치하는 패턴을 만들면 됩니다.

```bash
 | sed -E 's/.*Disconnected from (invalid |authenticating )?user .* [^ ]+ port [0-9]+( \[preauth\])?$//'
```

[정규 표현식 디버거](https://regex101.com/r/qqbZqh/2)로 동작을 살펴봅시다. 앞부분은 이전과 같습니다. 다음은 `user` 앞에 올 수 있는 두 가지 접두사를 처리합니다. 사용자 이름 자리에는 임의의 문자열을 허용합니다. 그 뒤에는 공백이 아닌 문자가 하나 이상인 `[^ ]+`, 즉 단어 하나가 옵니다. 이어서 `port`와 숫자들이 나오고, 선택적으로 ` [preauth]`가 붙은 다음 줄이 끝납니다.

이제 사용자 이름이 "Disconnected from"이어도 혼동하지 않습니다. 왜 그런지 알겠나요?

하지만 문제가 있습니다. 일치하는 로그 줄 전체가 빈 문자열로 바뀝니다. 사용자 이름은 *남겨야* 합니다. 이때 "캡처 그룹"을 사용합니다. 괄호로 감싼 정규 표현식과 일치한 텍스트는 번호가 붙은 그룹에 저장됩니다. 치환할 문자열에서 `\1`, `\2`, `\3` 등으로 참조할 수 있습니다. 일부 정규 표현식 엔진은 검색 패턴 안에서도 참조할 수 있습니다.

```bash
 | sed -E 's/.*Disconnected from (invalid |authenticating )?user (.*) [^ ]+ port [0-9]+( \[preauth\])?$/\2/'
```

상상할 수 있듯 정규 표현식은 *매우* 복잡해질 수 있습니다. [이메일 주소와 일치하는 패턴](https://www.regular-expressions.info/email.html)을 만드는 글을 보세요. [쉽지 않은 문제](https://web.archive.org/web/20221223174323/http://emailregex.com/)입니다. [관련 논의](https://stackoverflow.com/questions/201323/how-to-validate-an-email-address-using-a-regular-expression/1917982)도 많고, [테스트](https://fightingforalostcause.net/content/misc/2006/compare-email-regex.php)와 [테스트 비교표](https://mathiasbynens.be/demo/url-regex)도 있습니다. 어떤 수가 [소수인지 확인하는 정규 표현식](https://www.noulakaz.net/2007/03/18/a-regular-expression-to-check-for-prime-numbers/)까지 만들 수 있습니다.

정규 표현식은 정확하게 작성하기 어렵기로 유명하지만, 알아두면 무척 유용한 도구입니다.

## 다시 데이터 가공으로
{: id="back-to-data-wrangling"}

지금까지 만든 명령은 다음과 같습니다.

```bash
ssh myserver journalctl
 | grep sshd
 | grep "Disconnected from"
 | sed -E 's/.*Disconnected from (invalid |authenticating )?user (.*) [^ ]+ port [0-9]+( \[preauth\])?$/\2/'
```

`sed`만으로도 할 수 있습니다. 왜 굳이 그렇게 할까요? 재미로 해 봅시다.

```bash
ssh myserver journalctl
 | sed -E
   -e '/Disconnected from/!d'
   -e 's/.*Disconnected from (invalid |authenticating )?user (.*) [^ ]+ port [0-9]+( \[preauth\])?$/\2/'
```

`sed`의 몇 가지 기능을 보여 주는 예입니다. `i`로 텍스트를 삽입하거나, `p`로 줄을 명시적으로 출력하거나, 줄 번호로 대상을 선택하는 등 여러 작업을 할 수 있습니다. `man sed`를 살펴보세요.

지금은 로그인을 시도한 모든 사용자 이름을 얻었습니다. 하지만 이 목록만으로는 그다지 유용하지 않습니다. 자주 등장하는 이름을 찾아봅시다.

```bash
ssh myserver journalctl
 | grep sshd
 | grep "Disconnected from"
 | sed -E 's/.*Disconnected from (invalid |authenticating )?user (.*) [^ ]+ port [0-9]+( \[preauth\])?$/\2/'
 | sort | uniq -c
```

`sort`는 입력을 정렬합니다. `uniq -c`는 연속해서 반복되는 같은 줄을 하나로 합치고 앞에 등장 횟수를 붙입니다. 이 결과도 정렬해 가장 자주 등장하는 이름만 남겨 봅시다.

```bash
ssh myserver journalctl
 | grep sshd
 | grep "Disconnected from"
 | sed -E 's/.*Disconnected from (invalid |authenticating )?user (.*) [^ ]+ port [0-9]+( \[preauth\])?$/\2/'
 | sort | uniq -c
 | sort -nk1,1 | tail -n10
```

`sort -n`은 사전순 대신 숫자 크기로 정렬합니다. `-k1,1`은 공백으로 구분한 첫 번째 필드만 정렬 기준으로 삼는다는 뜻입니다. 쉼표 뒤의 번호는 정렬 키가 끝나는 필드를 지정하며, 생략하면 줄 끝까지 사용합니다. 이 예에서는 줄 전체를 기준으로 해도 결과에 큰 차이가 없지만, 옵션을 배워 두면 좋습니다.

가장 드문 이름을 보려면 `tail` 대신 `head`를 사용하면 됩니다. 역순으로 정렬하는 `sort -r`도 있습니다.

사용자 이름만 출력하고, 한 줄에 하나씩 대신 다른 형식으로 표시하고 싶다면 어떻게 할까요?

```bash
ssh myserver journalctl
 | grep sshd
 | grep "Disconnected from"
 | sed -E 's/.*Disconnected from (invalid |authenticating )?user (.*) [^ ]+ port [0-9]+( \[preauth\])?$/\2/'
 | sort | uniq -c
 | sort -nk1,1 | tail -n10
 | awk '{print $2}' | paste -sd,
```

먼저 `paste`는 지정한 한 글자 구분자(`-d`)로 여러 줄을 하나로 이어 붙입니다(`-s`). 그러면 `awk`는 무엇일까요?

## awk — 또 다른 편집 도구
{: id="awk--another-editor"}

`awk`는 텍스트 스트림 처리에 특히 강한 프로그래밍 언어입니다. 제대로 배우려면 내용이 많지만, 여기서는 기본만 살펴보겠습니다.

`{print $2}`는 무엇을 할까요? `awk` 프로그램은 선택적인 패턴과, 줄이 패턴에 일치할 때 실행할 코드 블록으로 구성됩니다. 위처럼 패턴을 생략하면 모든 줄에 적용됩니다. 블록 안에서 `$0`은 줄 전체이고, `$1`부터 `$n`까지는 각 *필드*입니다. 기본 필드 구분자는 공백 문자이며 `-F`로 바꿀 수 있습니다. 여기서는 줄마다 두 번째 필드인 사용자 이름을 출력합니다.

조금 더 복잡한 작업을 해 봅시다. 단 한 번 등장하며 `c`로 시작하고 `e`로 끝나는 사용자 이름의 개수를 세겠습니다.

```bash
 | awk '$1 == 1 && $2 ~ /^c[^ ]*e$/ { print $2 }' | wc -l
```

이번에는 `{...}` 앞에 패턴이 있습니다. 첫 번째 필드, 즉 `uniq -c`로 센 횟수가 1이고, 두 번째 필드가 주어진 정규 표현식과 일치해야 합니다. 코드 블록은 사용자 이름을 출력합니다. 마지막으로 `wc -l`이 출력 줄 수를 셉니다.

하지만 `awk` 자체가 프로그래밍 언어라는 점을 기억하세요.

```awk
BEGIN { rows = 0 }
$1 == 1 && $2 ~ /^c[^ ]*e$/ { rows += $1 }
END { print rows }
```

`BEGIN` 블록은 입력을 읽기 전에, `END` 블록은 입력을 모두 읽은 뒤 실행됩니다. 각 줄에서는 첫 번째 필드의 횟수를 더하고, 마지막에 합계를 출력합니다. 이 예에서는 더하는 값이 항상 1입니다. 사실 `awk`로 [이 모든 작업](https://web.archive.org/web/20251210045942/https://backreference.org/2010/02/10/idiomatic-awk/)을 할 수 있어서 `grep`과 `sed`를 없앨 수도 있습니다. 직접 연습해 보세요.

## 데이터 분석
{: id="analyzing-data"}

계산도 할 수 있습니다.

```bash
 | paste -sd+ | bc -l
```

```bash
echo "2*($(data | paste -sd+))" | bc -l
```

통계를 구하는 방법도 다양합니다. [`st`](https://github.com/nferraz/st)도 유용하지만, 이미 R이 있다면 다음처럼 사용할 수 있습니다.

```bash
ssh myserver journalctl
 | grep sshd
 | grep "Disconnected from"
 | sed -E 's/.*Disconnected from (invalid |authenticating )?user (.*) [^ ]+ port [0-9]+( \[preauth\])?$/\2/'
 | sort | uniq -c
 | awk '{print $1}' | R --slave -e 'x <- scan(file="stdin", quiet=TRUE); summary(x)'
```

R은 데이터 분석과 [그래프 그리기](https://ggplot2.tidyverse.org/)에 적합한 또 다른 프로그래밍 언어입니다. 자세히 다루지는 않겠습니다. 여기서는 입력 스트림을 숫자 벡터로 읽은 뒤 `summary`로 요약 통계를 출력합니다. 이렇게 원하는 통계를 얻을 수 있습니다.

간단한 그래프만 필요하다면 `gnuplot`을 사용해 보세요.

```bash
ssh myserver journalctl
 | grep sshd
 | grep "Disconnected from"
 | sed -E 's/.*Disconnected from (invalid |authenticating )?user (.*) [^ ]+ port [0-9]+( \[preauth\])?$/\2/'
 | sort | uniq -c
 | sort -nk1,1 | tail -n10
 | gnuplot -p -e 'set boxwidth 0.5; plot "-" using 1:xtic(2) with boxes'
```

## 데이터를 가공해 명령 인자 만들기
{: id="data-wrangling-to-make-arguments"}

긴 목록을 가공해 설치하거나 제거할 항목을 고르고 싶을 때도 있습니다. 앞서 배운 데이터 가공에 `xargs`를 조합하면 강력한 작업을 할 수 있습니다.

```bash
rustup toolchain list | grep nightly | grep -vE "nightly-x86|01-17" | sed 's/-x86.*//' | xargs rustup toolchain uninstall
```

# 연습 문제
{: id="exercises"}

1. 정규 표현식에 익숙하지 않다면 기본적인 내용을 다루는 [대화형 튜토리얼](https://regexone.com/)을 풀어 보세요.
1. `sed s/REGEX/SUBSTITUTION/g`는 `g`가 없을 때와 어떻게 다른가요? `/I`나 `/m`은 어떤가요?
1. 파일 자체를 수정하려고 `sed s/REGEX/SUBSTITUTION/ input.txt > input.txt`를 쓰고 싶을 수 있습니다. 하지만 잘못된 방법입니다. 이유는 무엇인가요? `sed`에만 해당하는 문제인가요?
1. 익숙한 언어에서 정규 표현식을 사용해 간단한 `grep`을 구현하세요. 출력에 색을 넣고 싶다면 ANSI 색상 이스케이프 시퀀스를 찾아보세요.
1. 여러 파일의 이름을 바꾸는 작업은 `mv`만으로 처리하기 번거로울 수 있습니다. `sed`와 비슷한 문법을 사용하는 `rename` 구현을 써 보세요. 이름에 공백이 있는 파일을 여러 개 만들고 `rename`으로 공백을 밑줄로 바꾸세요.
1. 최근 세 번의 부팅에서 *공통으로 나타나지 않는* 메시지를 찾으세요. `journalctl`의 `-b` 옵션을 참고하세요. 부팅 로그를 파일 하나에 모으면 편할 수 있습니다.
1. 다음 로그 메시지들의 타임스탬프를 이용해 최근 10번의 시스템 부팅 시간에 대한 통계를 구하세요.

   ```
   Logs begin at ...
   ```

    그리고 다음 메시지를 사용하세요.

   ```
   systemd[577]: Startup finished in ...
   ```

1. `/usr/share/dict/words`에서 `a`가 적어도 세 번 나오고 `'s`로 끝나지 않는 단어의 개수를 구하세요. 해당 단어들의 마지막 두 글자 조합 중 가장 흔한 세 가지는 무엇인가요? 대소문자를 구분하지 않으려면 `sed`의 `y` 명령이나 `tr`이 도움이 될 수 있습니다. 두 글자 조합은 모두 몇 가지인가요? 더 어려운 문제로, 한 번도 나오지 않은 조합도 찾아보세요.
1. [위키백과 통계](https://commons.wikimedia.org/wiki/Data:Wikipedia_statistics/data.tab)나 [범죄 통계](https://ucr.fbi.gov/crime-in-the-u.s/2016/crime-in-the-u.s.-2016/topic-pages/tables/table-1) 같은 온라인 데이터셋을 찾으세요. [공개 데이터셋 목록](https://www.springboard.com/blog/data-science/free-public-data-sets-data-science-project/)에서 찾아도 됩니다. `curl`로 내려받고 숫자 열 두 개만 추출하세요. HTML에는 [`pup`](https://github.com/EricChiang/pup), JSON에는 [`jq`](https://stedolan.github.io/jq/)가 도움이 될 수 있습니다. 한 명령으로 한 열의 최솟값과 최댓값을 구하고, 다른 명령으로 두 열의 차이를 합산하세요.
