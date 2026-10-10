---
layout: lecture
title: "버전 관리"
lang: ko
presenter: Jon
date: 2019-01-22
order: 2
video:
  aspect: 56.25
  id: 3fig2Vz8QXs
---

시간이 지나면서 바뀌는 무언가를 다룰 때는 변경을 *추적*할 수 있으면 유용합니다. 무엇이 바뀌었고, 어떻게 되돌릴 수 있으며, 누가 바꿨고, 가능하다면 왜 바꿨는지도 알 수 있기 때문입니다. 버전 관리 시스템(VCS)은 이런 기능을 제공합니다. 파일의 변경 사항을 설명과 함께 *커밋*하고, 과거의 변경을 살펴보거나 되돌릴 수 있습니다.

대부분의 VCS는 여러 사용자 사이에 커밋 이력을 공유할 수 있습니다. 서로의 변경을 확인하며 편리하게 협업할 수 있습니다. VCS는 *변경*을 추적하므로, 수정한 부분이 겹치지 않는다면 서로의 작업을 자동으로 합칠 수 있는 경우가 많습니다. 항상 가능한 것은 아닙니다.

VCS의 [종류는 매우 많고](https://en.wikipedia.org/wiki/Comparison_of_version-control_software), 지원 기능과 동작 방식, 사용법도 다릅니다. 여기서는 널리 쓰이는 [Git](https://git-scm.com/)에 집중하지만, [Mercurial](https://www.mercurial-scm.org/)도 살펴보길 권합니다.

이제 핵심 내용을 정리해 보겠습니다.

## Git은 이해할 수 없는 마법일까요?
{: id="is-git-dark-magic"}

그렇지는 않습니다. 데이터 모델을 이해해야 합니다. 세부 사항 일부는 생략하겠지만, Git의 핵심 단위는 커밋입니다.

- 모든 커밋에는 "리비전 해시"라는 고유한 이름이 있습니다.
  - `998622294a6c520db718867354bf98348ae3c7e2`처럼 긴 해시입니다.
  - 다른 커밋과 구별할 수 있는 `9986222` 같은 짧은 접두사로 줄여 쓰기도 합니다.
- 커밋에는 작성자와 커밋 메시지가 있습니다.
- *부모 커밋*의 해시도 들어 있습니다. 보통은 직전 커밋 하나입니다.
- 커밋과 부모를 비교하면 *diff*, 즉 변경 사항을 얻습니다. 특정 줄 삭제, 새 줄 추가, 파일 이름 변경 등을 나타냅니다.
  - 실제로 Git은 변경 목록만 저장하는 것이 아니라 각 커밋의 파일 상태, 즉 스냅숏을 표현합니다.
  - 자주 바뀌는 큰 파일은 일반적인 Git 저장소에 넣지 않는 편이 좋습니다.

처음에는 *저장소*, 즉 대략 Git이 관리하는 디렉터리에 내용도 커밋도 없습니다. 저장소를 만들어 봅시다.

```console
$ git init hackers
$ cd hackers
$ git status
```

이 출력은 좋은 출발점입니다. 각 항목의 뜻을 살펴봅시다.

먼저 `On branch master`입니다.

- 매번 해시를 쓰고 싶지는 않을 것입니다.
- 브랜치는 커밋 해시를 가리키는 이름입니다.
- `master`는 전통적으로 기본 브랜치에 사용하던 이름입니다. 그 브랜치에서 새 커밋을 만들면 `master`가 새 커밋을 가리킵니다.
- 특별한 이름 `HEAD`는 현재 체크아웃한 위치를 나타내며, 보통 현재 브랜치를 가리킵니다.
- `git branch`나 `git tag`로 다른 이름을 만들 수도 있습니다. 뒤에서 살펴보겠습니다.

`No commits yet`는 아직 커밋이 없다는 뜻 그대로이므로 넘어가겠습니다.

다음은 `nothing to commit`입니다.

- 커밋 간 차이에는 변경 사항이 들어갑니다. 그렇다면 어떤 변경을 커밋에 넣을지는 어떻게 정할까요?
- 마지막 커밋 이후의 변경을 항상 *전부* 넣을 수도 있습니다.
  - 하지만 일부만 커밋하고 싶을 수 있습니다. 예를 들어 임시 `TODO`는 빼고 싶을 수 있습니다.
  - 하나의 작업을 여러 커밋으로 나누고 각각 메시지를 작성하고 싶을 수도 있습니다.
- Git에서는 변경을 *스테이징*해 다음 커밋을 구성합니다.
  - `git add`에 파일 경로를 전달해 해당 변경을 스테이징합니다.
    - `git add -p`는 파일 안의 변경 일부만 선택합니다.
    - 인자 없이 실행한 `git add`는 "알려진 모든 파일"에 적용됩니다.
  - `git rm`은 파일을 지우고 삭제를 스테이징합니다.
  - `git reset`은 스테이징을 취소합니다.
    - 작업 중인 파일의 내용은 바뀌지 않습니다. 다음 커밋에 포함할 변경만 비웁니다.
    - 일부만 취소하려면 `git reset FILE`이나 `git reset -p`를 사용합니다.
  - `git diff --staged`로 스테이징한 변경을 확인합니다.
  - `git diff`로 아직 스테이징하지 않은 변경을 확인합니다.
  - 준비가 됐다면 `git commit`으로 커밋합니다.
    - 모든 변경을 커밋하려면 `git commit -a`를 사용합니다.
    - `git help add`에 더 많은 설명이 있습니다.

위 명령을 사용하면서 `git status`를 자주 실행해 보세요. Git이 현재 상태를 어떻게 보고 있는지 알려 주므로 유용합니다.

## 커밋을 만들었습니다. 그다음은요?
{: id="a-commit-you-say"}

커밋을 만들었다면 무엇을 할 수 있을까요?

- `git log`나 `git log --oneline`으로 최근 이력을 봅니다.
- `git log -p`로 각 커밋의 변경 내용까지 봅니다.
- `git show master`로 특정 커밋을 확인합니다.
  - `-p`로 패치 출력도 지정할 수 있습니다.
- `git checkout NAME`으로 해당 커밋의 상태를 가져옵니다.
  - `NAME`에 커밋 해시를 지정하면 Git은 "detached" 상태라고 알려 줍니다. 이 커밋을 가리키는 이름이 없다는 뜻이므로, 여기서 새 커밋을 만들면 아무도 그 커밋을 알지 못합니다.
- `git revert NAME`은 해당 커밋의 변경을 반대로 적용하는 새 커밋을 만듭니다.
- `git diff NAME..`으로 해당 버전과 현재 커밋을 비교합니다.
  - `a..b`는 커밋의 *범위*입니다. 한쪽을 생략하면 `HEAD`를 뜻합니다.
- `git log NAME..`으로 그 사이의 모든 커밋을 봅니다.
  - 여기에도 `-p`를 쓸 수 있습니다.
- `git reset NAME`으로 현재 브랜치, 예를 들어 `master`가 특정 커밋을 가리키도록 바꿀 수 있습니다.
  - `reset`은 스테이징한 변경을 바꾸는 명령이 아니었나요? 지정한 이름이 가리키는 커밋으로 `HEAD`를 옮기는 두 번째 형식도 있습니다. `git help reset`을 참고하세요.
  - 파일은 바뀌지 않았습니다. 이제 `git diff`는 사실상 `git diff NAME..`의 결과를 보여 줍니다.

## 이름에 담긴 의미
{: id="whats-in-a-name"}

Git에서 이름은 중요합니다. Git의 여러 동작을 이해하는 열쇠이기도 합니다. 지금까지 커밋 해시, `master`, `HEAD`를 봤지만 더 있습니다.

- `git branch b`로 `master` 같은 새 브랜치를 만듭니다.
  - `HEAD`의 커밋을 가리키는 이름 `b`를 만듭니다.
  - 아직 현재 브랜치는 `master`입니다. 이 상태에서 새 커밋을 만들면 `master`만 이동하고 `b`는 그대로입니다.
  - `git checkout b`로 브랜치를 전환합니다.
    - 이제 새 커밋을 만들면 `b`가 이동합니다.
    - `git checkout master`로 돌아가면 `b`에 커밋한 변경은 현재 작업 트리에서 보이지 않습니다.
    - 변경을 별도로 시험하기에 편리한 방법입니다.
- 태그도 이름의 한 종류로, 변하지 않으며 자체 메시지를 갖습니다. 릴리스와 변경 내역을 표시할 때 자주 씁니다.
- `NAME^`는 "`NAME` 이전의 커밋"을 뜻합니다.
  - `NAME^^^`처럼 반복할 수 있습니다.
  - 몇 세대 이전 커밋을 뜻하고 싶다면 `~`가 편리합니다.
    - `~`는 시간 순서를 따르고, `^`는 조상을 따라갑니다.
    - `~~`와 `^^`는 같습니다.
    - `X~3`은 "`X`보다 세 커밋 이전"을 뜻합니다.
    - 이때 `^3`을 쓰면 안 됩니다.
  - `git diff HEAD^`로 이전 커밋과 작업 상태를 비교할 수 있습니다.
- 브랜치를 전환할 때 `-`는 직전에 체크아웃한 위치를 뜻합니다.
- 많은 명령은 별도 대상을 지정하지 않으면 `HEAD`를 기준으로 동작합니다.

## 커밋 이력 정리하기
{: id="clean-up-your-mess"}

커밋 이력이 다음처럼 쌓이기 쉽습니다.

- `기능 x 추가` — 메시지에 기능 설명까지 적었을 수도 있습니다.
- `빠뜨린 파일 추가`
- `버그 수정`
- `오타`
- `오타2`
- `이번에는 진짜 수정`
- `이번에는 정말로 수정`
- `테스트 통과`
- `예제 코드 수정`
- `오타`
- `x`
- `x`
- `x`
- `x`

Git 입장에서는 문제없지만, 미래의 자신이나 변경 이유를 알고 싶은 사람에게는 별로 도움이 되지 않습니다. Git으로 이런 이력을 정리할 수 있습니다.

- `git commit --amend`: 스테이징한 변경을 이전 커밋에 합칩니다.
  - 이전 커밋을 바꾸므로 새로운 해시가 생깁니다.
- `git rebase -i HEAD~13`: 최근 13개 커밋을 어떻게 처리할지 지정합니다.
  - 기본값 `pick`: 커밋을 그대로 적용합니다.
  - `r`: 커밋 메시지를 바꿉니다.
  - `e`: 멈춰서 파일 추가·삭제 등 커밋 내용을 수정합니다.
  - `s`: 앞 커밋과 합치고 메시지를 편집합니다.
  - `f`: fixup. 앞 커밋과 합치고 이 커밋의 메시지는 버립니다.
  - 끝나면 `HEAD`는 정리된 마지막 커밋을 가리킵니다.
  - 커밋을 합치는 작업은 흔히 *스쿼시(squash)*라고 부릅니다.
  - 실제로는 시작 지점으로 돌아간 뒤, 지정한 방식에 따라 커밋을 차례로 다시 적용합니다.
- `git reset --hard NAME`: 모든 파일의 상태를 `NAME` 상태로 되돌립니다. 이름을 생략하면 `HEAD`가 기준입니다. 변경을 취소할 때 편리합니다.

## 다른 사람과 저장소 공유하기
{: id="playing-with-others"}

버전 관리는 여러 사람이 같은 파일들을 수정하면서 서로의 작업을 방해하지 않도록 돕습니다. 수정이 겹치더라도 조용히 덮어쓰지 않고 확인할 수 있게 합니다.

Git은 *분산형* VCS입니다. 각자 저장소의 사본과 공유된 이력을 로컬에 보관합니다. 반면 Subversion 같은 *중앙 집중형* VCS에서는 서버가 커밋 이력을 보관하고 클라이언트는 주로 체크아웃한 파일을 갖습니다. 다른 과거 상태가 필요하면 서버에 요청합니다.

Git 저장소의 다른 사본은 "원격 저장소(remote)"로 등록할 수 있습니다. `git init` 대신 `git clone ADDRESS`로 기존 저장소를 복제하면, `ADDRESS`를 가리키는 *origin* 원격 저장소가 생깁니다. `git fetch REMOTE`로 원격 브랜치 정보와 커밋을 가져옵니다. 원격 추적 브랜치는 `REMOTE/NAME`처럼 참조하며 로컬 이름과 비슷하게 사용할 수 있습니다.

원격 저장소에 쓰기 권한이 있다면 `git push`로 원격 브랜치가 자신이 만든 커밋을 가리키게 할 수 있습니다. 예를 들어 `origin`의 `master`를 로컬 `master`와 같게 만듭니다.

- `git push origin master:master`
- `-u`를 붙이면 `origin/master`를 현재 브랜치의 업스트림으로 설정할 수 있습니다. 이후 기본 푸시 대상을 정하는 데 사용됩니다.
- `git push origin master:HEAD^`는 무엇을 하는 명령일까요? 생각해 보세요.

원격 저장소로 GitHub, GitLab, Bitbucket 등을 쓰는 경우가 많습니다. Git의 관점에서는 특별할 것이 없습니다. 이름과 커밋을 주고받는 것입니다. 누군가 `master`를 수정해 원격 브랜치를 갱신했다면, `github`이라는 이름으로 등록한 원격 저장소에서 `git fetch github`을 실행하고 `git log github/master`로 변경을 볼 수 있습니다.

## 함께 작업하기
{: id="working-with-others"}

지금까지만 보면 브랜치가 별로 쓸모없어 보일 수 있습니다. 브랜치에서 작업한 뒤 결국 `master`가 그 커밋을 가리키게 하면 끝 아닌가요?

- 큰 기능을 개발하는 도중 급한 수정이 필요하면 어떨까요?
- 그사이에 다른 사람이 `master`를 수정했다면요?

자신이 만든 변경이든 다른 사람이 만든 변경이든, 언젠가는 브랜치 사이의 변경을 *병합*해야 합니다. `git merge NAME`을 사용합니다. 다음 과정으로 병합합니다.

- `HEAD`와 `NAME`의 공통 조상, 즉 갈라진 지점을 찾습니다.
- 양쪽의 변경을 현재 상태에 합치려고 시도합니다.
- 변경을 합친 커밋을 만듭니다. 두 브랜치의 끝 커밋을 부모로 기록합니다.
- 현재 브랜치와 `HEAD`가 병합 결과를 가리키게 합니다.

큰 기능이 완성되면 그 브랜치를 `master`에 병합할 수 있습니다. Git은 어느 브랜치의 변경도 잃지 않도록 해 줍니다.

Git을 써 봤다면 `merge`를 다른 이름인 `pull`로 알고 있을 수도 있습니다. `git pull REMOTE BRANCH`는 다음 과정에 해당합니다.

- `git fetch REMOTE`
- `git merge REMOTE/BRANCH`
- `push`처럼 `REMOTE`와 `BRANCH`를 생략하고 추적 중인 원격 브랜치를 사용할 수 있습니다. 앞서 나온 `-u`를 기억하세요.

서로 다른 부분을 수정했다면 보통 잘 동작합니다. 같은 부분을 수정했다면 *병합 충돌*이 날 수 있습니다. 이름만 보면 무섭지만, 의미는 단순합니다.

- Git이 최종 결과를 스스로 결정할 수 없다는 뜻입니다.
- 병합을 멈추고 사용자가 결과를 정리해 스테이징하기를 기다립니다.
- 충돌한 파일을 열고 `<<<<<<<` 같은 표시를 찾으세요. `=======` 위는 현재 `HEAD` 쪽 내용이고, 아래는 병합하려는 `NAME` 쪽 내용입니다.
- `git mergetool`은 차이를 비교하는 편집기를 열어 줍니다.
- 최종 파일 내용을 결정해 충돌을 *해결*한 다음 `git add`로 스테이징합니다.
- 모든 충돌을 해결했다면 `git commit`으로 마칩니다.
  - 포기하려면 `git merge --abort`를 사용합니다.

이렇게 병합 충돌을 해결할 수 있습니다. 완성된 변경을 공유하려면 `git push`를 사용합니다.

## 원격 변경과 내 변경이 엇갈릴 때
{: id="when-worlds-collide"}

`push`할 때 Git은 원격 브랜치를 바꿔도 다른 사람의 작업을 잃지 않는지 확인합니다. 원격 브랜치의 현재 커밋이 푸시할 커밋의 조상인지 검사합니다. 그렇다면 이름이 가리키는 위치만 앞으로 옮길 수 있습니다. 이를 *빨리 감기(fast-forward)*라고 합니다. 그렇지 않다면 원격 브랜치 갱신을 거부하고 다른 변경이 있음을 알립니다.

푸시가 거부되면 어떻게 할까요?

- `git pull`로 원격 변경을 병합합니다. 즉, `fetch`와 `merge`를 수행합니다.
- `--force`로 강제 푸시할 수도 있지만, 원격 브랜치에서 다른 사람의 변경을 사라지게 할 수 있습니다.
  - `--force-with-lease`는 마지막으로 가져온 뒤 원격 이름이 바뀌지 않았을 때만 강제로 갱신합니다. 훨씬 안전합니다.
  - 이미 푸시한 커밋을 리베이스해 이력을 바꿨다면 강제 푸시가 필요할 수 있습니다. 공유한 이력을 바꾸기 전에 영향을 고려하세요. 왜 일반 푸시로는 안 되는지도 생각해 보세요.
- 원격 변경 위에 자신의 변경을 다시 적용할 수 있습니다.
  - 바로 *리베이스(rebase)*입니다.
    - 공통 조상 이후의 로컬 커밋을 잠시 걷어냅니다.
    - 원격 브랜치의 커밋을 새 시작점으로 삼습니다.
    - 로컬 커밋을 순서대로 다시 적용합니다.
      - 충돌이 나면 직접 해결해야 합니다.
      - `git rebase --continue`로 계속하거나 `--abort`로 취소합니다.
    - [리베이스 설명](https://git-scm.com/book/en/v2/Git-Branching-Rebasing)을 참고하세요.
  - `git pull --rebase`로 이 과정을 시작할 수 있습니다.
  - 병합과 리베이스 중 무엇을 쓸지는 자주 논의되는 주제입니다. 다음 글을 읽어 보세요.
    - [병합과 리베이스 비교](https://www.atlassian.com/git/tutorials/merging-vs-rebasing)
    - [언제 병합하고 언제 리베이스할까](https://web.archive.org/web/20210106220723/https://derekgourlay.com/blog/git-when-to-merge-vs-when-to-rebase/)
    - [git merge 대신 git rebase를 쓰는 경우](https://stackoverflow.com/questions/804115/when-do-you-use-git-rebase-instead-of-git-merge)

# 더 읽을거리
{: id="further-reading"}

[![Git에 관한 XKCD 만화](https://imgs.xkcd.com/comics/git.png)](https://xkcd.com/1597/)

- [브랜치 연습: Learn Git Branching](https://learngitbranching.js.org/)
- [쉬운 말로 Git 설명하기](https://smusamashah.github.io/blog/2017/10/14/explain-git-in-simple-words)
- [밑바닥부터 이해하는 Git](https://jwiegley.github.io/git-from-the-bottom-up/)
- [컴퓨터 과학자를 위한 Git](https://eagain.net/articles/git-for-computer-scientists/)
- [Oh shit, git!](https://ohshitgit.com/)
- [Pro Git 책](https://git-scm.com/book/en/v2)

# 연습 문제
{: id="exercises"}

1. 저장소의 기존 파일을 수정하고 `git stash`를 실행해 보세요. 어떤 일이 생기나요? `git log --all --oneline`에는 무엇이 보이나요? `git stash pop`으로 저장해 둔 변경을 다시 적용하세요. 어떤 상황에 유용할까요?

1. Git을 배울 때 흔한 실수로, 관리하면 안 되는 큰 파일이나 민감한 정보를 커밋하는 일이 있습니다. 실습 저장소에 파일을 추가하고 몇 번 커밋한 뒤, 해당 파일을 이력에서 지워 보세요. [민감한 데이터 제거 안내](https://help.github.com/articles/removing-sensitive-data-from-a-repository/)를 참고할 수 있습니다. 큰 파일을 Git과 함께 관리하고 싶다면 [Git LFS](https://git-lfs.github.com/)도 살펴보세요.

1. Git은 변경을 되돌릴 때 편리하지만 여러 복구 방법을 알아둬야 합니다.
    1. 잘못 수정한 커밋은 `git revert`로 되돌릴 수 있습니다. 하지만 커밋에 여러 변경이 섞여 있다면 최선의 방법이 아닐 수 있습니다. `git checkout`으로 특정 커밋의 파일 하나만 복구하려면 어떻게 할까요?
    1. 브랜치를 만들고 커밋한 다음 브랜치를 지워 보세요. 커밋을 복구할 수 있나요? `git reflog`를 살펴보세요. 아무 참조도 없는 커밋은 나중에 자동 정리될 수 있으므로 복구는 빨리 해야 합니다.
    1. `git reset` 대신 `git reset --hard`를 무심코 쓰면 변경을 잃을 수 있습니다. 스테이징했던 내용은 복구할 여지가 있습니다. `git fsck --lost-found`와 `.git/lost-found`를 살펴보세요.

1. 저장소의 `.git/hooks`에는 `.sample`로 끝나는 스크립트가 있습니다. 실행 권한을 확인하고 이름에서 `.sample`을 지우면 해당 시점에 실행할 수 있습니다. 예를 들어 `pre-commit`은 커밋 전에 실행됩니다. 직접 시험해 보세요.

1. 다른 명령줄 도구처럼 Git에도 `~/.gitconfig`라는 설정 파일이 있습니다. `git graph`를 실행하면 `git log --oneline --decorate --all --graph`가 실행되도록 별칭을 만드세요. 커밋 그래프를 빠르게 확인할 때 유용합니다.

1. Git에서는 `~/.gitignore_global`에 전역 파일 제외 패턴을 정의할 수 있습니다. RSA 키를 실수로 추가하는 등의 흔한 오류를 방지하는 데 유용합니다. `~/.gitignore_global` 파일을 만들고 `*rsa` 패턴을 추가한 뒤, 저장소에서 동작하는지 확인하세요.

1. Git에 익숙해지면 `.gitignore` 편집 같은 작업을 반복하게 됩니다. [git extras](https://github.com/tj/git-extras/blob/master/Commands.md)는 Git과 함께 쓰는 작은 도구 모음입니다. 예를 들어 `git ignore PATTERN`은 저장소의 `.gitignore`에 패턴을 추가하고, `git ignore-io LANGUAGE`는 [gitignore.io](https://www.gitignore.io)에서 해당 언어의 제외 패턴을 가져옵니다. `git extras`를 설치하고 `git alias`, `git ignore` 등을 써 보세요.

1. GUI 도구도 유용할 때가 있습니다. 저장소에서 [gitk](https://git-scm.com/docs/gitk)를 실행하고 화면의 각 부분을 살펴보세요. `gitk --all`로 실행하면 무엇이 달라지나요?

1. 명령줄에 익숙해지면 GUI 도구가 번거롭고 무겁게 느껴질 수 있습니다. ncurses 기반 도구는 터미널에서 조작하면서도 대화형 화면을 제공하는 절충안입니다. Git에는 [tig](https://github.com/jonas/tig)가 있습니다. 설치해 저장소에서 실행하고, [사용 예](https://www.atlassian.com/blog/git/git-tig)를 참고하세요.

{% comment %}

 - forced push + `--force-with-lease`
 - git merge/rebase --abort
 - git blame
 - exercise about why rebasing public commits is bad

{% endcomment %}
