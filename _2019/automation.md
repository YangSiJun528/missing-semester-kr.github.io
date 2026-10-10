---
layout: lecture
title: "자동화"
lang: ko
presenter: Jose
date: 2019-01-24
order: 3
video:
  aspect: 56.25
  id: BaLlAaHz-1k
special: true
---

백업처럼 어떤 스크립트를 주기적으로 실행하고 싶을 때가 있습니다. 백그라운드에서 기다리다가 일정 시간마다 실행하는 임시방편을 직접 만들 수도 있습니다. 하지만 대부분의 유닉스 시스템에는 간단한 규칙으로 작업을 예약하고 최소 1분 간격으로 실행할 수 있는 cron 데몬이 있습니다.

많은 유닉스 시스템에서 cron 데몬인 `crond`는 기본으로 실행됩니다. `ps aux | grep crond`로 확인할 수 있습니다.

## crontab
{: #the-crontab}

cron 설정은 `crontab -l`로 확인하고 `crontab -e`로 편집합니다. 시간은 공백으로 구분된 다섯 필드로 지정하며, 사용자와 실행할 명령도 함께 적습니다.

- **minute**: 매시간 몇 분에 실행할지 지정합니다. 범위는 0~59입니다.
- **hour**: 몇 시에 실행할지 24시간제로 지정합니다. 범위는 0~23이며, 0은 자정입니다.
- **dom**: 날짜(day of month)를 지정합니다. 예를 들어 매월 19일에 실행하려면 19를 씁니다.
- **month**: 실행할 월을 0~12의 숫자나 `May` 같은 월 이름으로 지정합니다.
- **dow**: 요일(day of week)을 0~7의 숫자나 `sun` 같은 이름으로 지정합니다.
- **user**: 명령을 실행할 사용자입니다.
- **command**: 실행할 명령입니다. 여러 단어나 공백이 들어갈 수 있습니다.

별표 `*`는 가능한 모든 값을 뜻합니다. 별표 뒤에 `/`와 숫자를 붙이면 해당 필드에서 그 수만큼 간격을 둡니다. 예를 들어 분 필드의 `*/5`는 5분마다 실행한다는 뜻입니다.

```shell
*/5   *    *   *   *       # Every five minutes
  0   *    *   *   *       # Every hour at o'clock
  0   9    *   *   *       # Every day at 9:00 am
  0   9-17 *   *   *       # Every hour between 9:00am and 5:00pm
  0   0    *   *   5       # Every Friday at 12:00 am
  0   0    1   */2 *       # Every other month, the first day, 12:00am
```

자주 쓰는 일정의 예시는 [crontab.guru](https://crontab.guru/examples.html)에서 더 찾아볼 수 있습니다.

## 셸 환경과 로그
{: #shell-environment-and-logging}

cron을 사용할 때 흔히 겪는 문제는 `.bashrc`, `.zshrc`처럼 대화형 셸이 읽는 환경 설정 파일을 똑같이 읽지 않는다는 점입니다. 출력도 기본적으로 로그 파일에 저장되지 않습니다. 실행 간격도 최소 1분이라 처음에는 스크립트를 디버깅하기가 번거로울 수 있습니다.

실행 환경 문제를 줄이려면 스크립트에서 절대 경로를 사용하고, `PATH` 같은 환경 변수를 필요한 값으로 설정하세요. 로그를 쉽게 남기려면 crontab을 다음과 같은 형식으로 작성하는 것이 좋습니다.

```shell
* * * * *   user  /path/to/cronscripts/every_minute.sh >> /tmp/cron_every_minute.log 2>&1
```

스크립트 본문은 별도 파일에 작성합니다. `>>`는 파일 끝에 내용을 덧붙이고, `2>&1`은 표준 오류(`stderr`)를 표준 출력(`stdout`)과 같은 곳으로 보냅니다. 필요하면 두 출력을 따로 저장해도 됩니다.

## anacron
{: #anacron}

cron 작업을 실행할 시각에 컴퓨터가 꺼져 있거나 절전 상태라면 해당 작업은 실행되지 않습니다. 자주 실행하는 작업이라면 괜찮을 수 있지만, 드물게 실행하는 작업은 빠뜨리지 않도록 해야 할 수 있습니다. [anacron](https://linux.die.net/man/8/anacron)은 cron과 비슷하지만 주기를 일 단위로 지정합니다. 컴퓨터가 계속 켜져 있다고 가정하지 않으므로, 하루 24시간 실행하지 않는 컴퓨터에서도 일별·주별·월별 작업을 관리할 수 있습니다.

## 연습 문제
{: #exercises}

1. 매분 다운로드 폴더에서 이미지 파일을 찾아 사진 폴더로 옮기는 스크립트를 작성하세요. [MIME 형식](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types)을 확인하거나, 흔한 이미지 확장자를 정규 표현식으로 찾을 수 있습니다.

1. 매주 시스템에서 오래된 패키지를 확인하고 업데이트를 요청하거나 자동으로 업데이트하는 cron 스크립트를 작성하세요.

{% comment %}
추가 주제:

- [fswatch](https://github.com/emcrisostomo/fswatch)
- GUI 자동화(pyautogui): [Automate the Boring Stuff 18장](https://automatetheboringstuff.com/chapter18/)
- Ansible/puppet/chef
- https://xkcd.com/1205/
- https://xkcd.com/1319/
{% endcomment %}
