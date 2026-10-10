---
layout: lecture
title: "이 수업을 만든 이유"
---

일반적인 컴퓨터 과학 교육에서는 운영체제, 프로그래밍 언어, 기계학습 등 고급 주제를 다루는 수업을 많이 듣습니다. 하지만 여러 교육기관에서 거의 가르치지 않고 학생들이 알아서 익히도록 남겨 두는 필수 주제가 있습니다. 바로 컴퓨팅 생태계를 이해하고 활용하는 능력입니다.

우리는 여러 해 동안 MIT의 여러 수업에서 가르치는 일을 도우며, 많은 학생이 자신이 쓸 수 있는 도구를 충분히 알지 못한다는 사실을 반복해서 확인했습니다. 컴퓨터는 수작업을 자동화하기 위해 만들어졌지만, 학생들은 반복 작업을 손으로 하거나 버전 관리와 텍스트 편집기 같은 강력한 도구를 충분히 활용하지 못하곤 합니다. 가볍게는 비효율과 시간 낭비로 끝나지만, 심하면 데이터를 잃거나 필요한 작업을 끝내지 못하기도 합니다.

대학 교과과정에서는 이런 주제를 다루지 않습니다. 도구를 사용하는 법, 적어도 효율적으로 사용하는 법을 배우지 못한 학생들은 간단해야 할 일에 시간과 노력을 낭비합니다. 표준 CS 교과과정에는 학생들의 생활을 훨씬 편하게 만들어 줄 컴퓨팅 생태계의 중요한 주제들이 빠져 있습니다.

# 여러분의 CS 교육에서 누락된 학기

이 공백을 메우고자, 유능한 컴퓨터 과학자와 프로그래머가 되는 데 중요하다고 생각하는 주제를 모아 수업을 만들었습니다. 실용적인 수업으로, 여러분이 마주칠 여러 상황에 바로 적용할 수 있는 도구와 기법을 직접 사용해 봅니다. 자료를 크게 개편한 최신 수업은 2026년 1월 MIT의 독립 활동 기간(Independent Activities Period)에 진행됩니다. 학생들이 운영하는 짧은 수업들로 구성된 한 달짜리 학기입니다. 현장 강의에는 MIT 구성원만 참여할 수 있지만, 모든 강의 자료와 녹화 영상은 공개합니다.

관심이 생겼다면, 이 수업에서 무엇을 배우는지 구체적인 예를 살펴보세요.

## 명령 셸

별칭, 스크립트, 빌드 시스템으로 흔히 하는 반복 작업을 자동화합니다. 텍스트 문서에서 명령어를 복사해 붙여 넣거나, 명령어 15개를 순서대로 실행할 필요가 없어집니다. 명령어나 인자를 빠뜨려 생기는 실수도 줄일 수 있습니다.

예를 들어 명령어 기록을 빠르게 검색하면 시간을 크게 절약할 수 있습니다. 아래에서는 셸 기록에서 `convert` 명령을 찾는 여러 요령을 보여 줍니다.

<video autoplay="autoplay" loop="loop" controls muted playsinline oncontextmenu="return false;" preload="auto" class="demo">
  <source src="/static/media/demos/history.mp4" type="video/mp4">
</video>

## 버전 관리

버전 관리를 *제대로* 활용하여 실수에 대비하고, 다른 사람과 협업하고, 문제를 일으킨 변경을 빠르게 찾아 분리하는 법을 배웁니다. `rm -rf; git clone`으로 처음부터 다시 시작하거나, 많은 코드를 주석 처리해 남겨 둘 필요가 없습니다. 병합 충돌도 줄일 수 있습니다. 무엇 때문에 코드가 망가졌는지, 잘 작동하던 코드를 지워 버린 것은 아닌지 걱정할 일도 줄어듭니다. 풀 리퀘스트로 다른 사람의 프로젝트에 기여하는 법도 배웁니다.

아래에서는 `git bisect`로 단위 테스트를 망가뜨린 커밋을 찾고 `git revert`로 되돌립니다.

<video autoplay="autoplay" loop="loop" controls muted playsinline oncontextmenu="return false;" preload="auto" class="demo">
  <source src="/static/media/demos/git.mp4" type="video/mp4">
</video>

## 텍스트 편집

로컬과 원격 환경의 명령줄에서 파일을 효율적으로 편집하고, 편집기의 고급 기능을 활용하는 법을 배웁니다. 파일을 이리저리 복사하거나 같은 편집을 반복하지 않아도 됩니다.

Vim의 강력한 기능 중 하나는 매크로입니다. 아래에서는 중첩된 Vim 매크로로 HTML 표를 CSV 형식으로 빠르게 변환합니다.

<video autoplay="autoplay" loop="loop" controls muted playsinline oncontextmenu="return false;" preload="auto" class="demo">
  <source src="/static/media/demos/vim.mp4" type="video/mp4">
</video>

## 원격 컴퓨터

SSH 키와 터미널 멀티플렉싱으로 원격 컴퓨터에서 편하게 작업하는 법을 배웁니다. 명령 두 개를 동시에 실행하려고 터미널을 여러 개 띄우거나, 접속할 때마다 비밀번호를 입력할 필요가 없습니다. 인터넷 연결이 끊기거나 노트북을 재부팅했다고 작업을 모두 잃을 일도 없습니다.

아래에서는 `tmux`로 원격 서버의 세션을 유지하고, `mosh`로 네트워크 전환과 연결 끊김에 대응합니다.

<video autoplay="autoplay" loop="loop" controls muted playsinline oncontextmenu="return false;" preload="auto" class="demo">
  <source src="/static/media/demos/ssh.mp4" type="video/mp4">
</video>

## 파일 찾기

필요한 파일을 빠르게 찾는 법을 배웁니다. 원하는 코드가 나올 때까지 프로젝트의 파일을 하나씩 클릭할 필요가 없습니다.

아래에서는 `fd`로 파일을, `rg`로 코드 조각을 빠르게 찾습니다. `fasd`를 사용해 최근에 사용했거나 자주 사용하는 파일과 폴더를 `cd`와 `vim`으로 바로 엽니다.

<video autoplay="autoplay" loop="loop" controls muted playsinline oncontextmenu="return false;" preload="auto" class="demo">
  <source src="/static/media/demos/find.mp4" type="video/mp4">
</video>

## 데이터 가공

명령줄에서 데이터와 파일을 빠르게 수정하고, 살펴보고, 파싱하고, 그래프로 그리고, 계산하는 법을 배웁니다. 로그 파일에서 복사해 붙여 넣거나, 통계를 손으로 계산하거나, 그래프를 그리려고 스프레드시트를 열 필요가 없습니다.

## 코드 품질과 지속적 통합

자동 서식 지정, 린트, 테스트, 코드 커버리지 도구로 코드 품질을 높이는 법을 배웁니다. 읽기 어려운 코드, 다시 나타나는 버그, 내 컴퓨터에서만 작동하는 코드를 줄일 수 있습니다.

## 코드 밖의 일

좋은 문서를 쓰고, 오픈 소스 유지보수자와 명확하게 소통하고, 해결에 도움이 되는 이슈를 작성하고, 병합할 수 있는 풀 리퀘스트를 만드는 법을 배웁니다. 사용자가 시작 방법을 몰라 헤매거나 유지보수자에게 답변을 받지 못하는 일을 줄일 수 있습니다.

# 마무리

이런 주제를 비롯한 여러 내용을 9개 강의에서 다룹니다. 각 강의에는 스스로 도구에 익숙해질 수 있는 연습문제가 있습니다. 2026년 1월까지 기다릴 수 없다면, 비슷한 주제를 많이 다룬 [이전 강의](/2020/)를 먼저 살펴보세요.

1월에 온라인으로든 현장에서든 만나기를 바랍니다!

즐겁게 해킹하세요.<br>
[Anish](https://anish.io/), [Jon](https://thesquareplanet.com/), [Jose](https://josejg.com/)
