---
layout: lecture
title: "버전 관리와 Git"
description: >
  Git의 데이터 모델을 이해하고 버전 관리와 협업에 활용하는 법을 배웁니다.
thumbnail: /static/assets/thumbnails/2026/lec5.png
date: 2026-01-16
ready: true
translation_status: ai-draft
human_review: pending
translation_source: 1d695c94ccafdce3f06d6b9dfe3e6f106097693a
video:
  aspect: 56.25
  id: 9K8lB61dl3Y
---

버전 관리 시스템(VCS)은 소스 코드나 파일·폴더 집합의 변경을 추적하는 도구입니다. 변경 이력을 유지하고 협업을 돕습니다. 논리적으로는 최상위 디렉터리 안의 파일과 폴더 전체 상태를 담은 *스냅샷*을 연속해서 기록합니다. 각 스냅샷의 작성자와 메시지 같은 메타데이터도 관리합니다.

혼자 작업하더라도 이전 프로젝트 상태를 보고, 변경 이유를 기록하고, 여러 개발 브랜치에서 병렬로 작업할 수 있습니다. 함께 작업할 때는 다른 사람의 변경을 확인하고 충돌을 해결하는 데 없어서는 안 될 도구입니다.

현대적인 VCS는 다음 질문에도 쉽게, 때로는 자동으로 답해 줍니다.

- 이 모듈은 누가 작성했나요?
- 이 파일의 이 줄은 언제, 누가, 왜 수정했나요?
- 최근 1,000개 버전 중 어느 시점에, 왜 특정 단위 테스트가 실패하기 시작했나요?

다른 VCS도 있지만 **Git**이 사실상의 표준입니다. [이 XKCD 만화](https://xkcd.com/1597/)는 Git의 평판을 잘 보여 줍니다.

![xkcd 1597](https://imgs.xkcd.com/comics/git.png)

Git의 인터페이스는 내부 구조를 완전히 감추지 못하는 추상화이므로, 명령줄 인터페이스부터 위에서 아래로 배우면 혼란스러울 수 있습니다. 몇 가지 명령을 주문처럼 외우고, 문제가 생길 때마다 만화의 방법을 따르게 되기도 합니다.

인터페이스는 복잡하지만 기저의 설계와 아이디어는 명료합니다. 복잡한 인터페이스는 *외워야* 하지만 좋은 설계는 *이해할 수* 있습니다. 따라서 데이터 모델부터 시작해 명령줄로 올라오는 방식으로 설명하겠습니다. 모델을 이해하면 각 명령이 데이터를 어떻게 바꾸는지로 동작을 이해할 수 있습니다.

# Git의 데이터 모델
{: #gits-data-model}

Git의 핵심은 이력 관리, 브랜치, 협업을 가능하게 하는 잘 설계된 데이터 모델입니다.

## 스냅샷
{: #snapshots}

Git은 최상위 디렉터리 안의 파일·폴더 이력을 스냅샷의 연속으로 표현합니다. 파일은 바이트의 모음인 "블롭(blob)", 디렉터리는 이름을 블롭이나 다른 트리에 연결하는 "트리(tree)"입니다. 스냅샷은 추적하는 최상위 트리입니다. 예를 들어 다음과 같습니다.

```
<root> (tree)
|
+- foo (tree)
|  |
|  + bar.txt (blob, contents = "hello world")
|
+- baz.txt (blob, contents = "git is wonderful")
```

최상위 트리에는 `foo` 트리와 `baz.txt` 블롭이 있습니다. `foo` 안에는 `bar.txt` 블롭 하나가 있습니다.

## 이력 모델링: 스냅샷 연결
{: #modeling-history-relating-snapshots}

스냅샷은 어떻게 연결하면 좋을까요? 시간순 목록으로 만드는 선형 이력이 가장 단순하지만 Git은 여러 이유로 이 모델을 사용하지 않습니다.

Git의 이력은 스냅샷의 방향성 비순환 그래프(DAG)입니다. 어려운 수학 용어처럼 들리지만, 각 스냅샷이 자신보다 앞선 "부모" 스냅샷들을 참조한다는 뜻입니다. 부모가 하나가 아니라 집합인 이유는 병렬로 개발한 브랜치 두 개를 병합하는 경우처럼 여러 부모에서 파생될 수 있기 때문입니다.

Git은 이런 스냅샷을 "커밋(commit)"이라고 부릅니다. 이력을 그리면 다음과 같습니다.

```
o <-- o <-- o <-- o
            ^
             \
              --- o <-- o
```

`o` 하나가 커밋, 즉 스냅샷 하나입니다. 화살표는 각 커밋의 부모를 가리킵니다. "다음"이 아니라 "이전"을 가리킨다는 점에 주의하세요. 세 번째 커밋 뒤에 이력이 둘로 나뉩니다. 예를 들어 두 기능을 독립적으로 개발하는 상황입니다. 나중에 두 기능을 모두 포함하는 스냅샷으로 병합할 수 있습니다. 새 병합 커밋을 굵게 표시하면 다음과 같습니다.

<pre class="highlight">
<code>
o <-- o <-- o <-- o <---- <strong>o</strong>
            ^            /
             \          v
              --- o <-- o
</code>
</pre>

Git의 커밋은 불변입니다. 실수를 고칠 수 없다는 뜻은 아닙니다. 이력을 "수정"할 때는 실제로 새 커밋을 만들고, 아래에서 설명할 참조가 새 커밋을 가리키도록 바꿉니다.

## 의사 코드로 보는 데이터 모델
{: #data-model-as-pseudocode}

다음과 같이 나타낼 수 있습니다.

```
// a file is a bunch of bytes
type blob = array<byte>

// a directory contains named files and directories
type tree = map<string, tree | blob>

// a commit has parents, metadata, and the top-level tree
type commit = struct {
    parents: array<commit>
    author: string
    message: string
    snapshot: tree
}
```

간단하고 명료한 이력 모델입니다.

## 객체와 내용 주소 지정
{: #objects-and-content-addressing}

"객체(object)"는 블롭, 트리 또는 커밋입니다.

```
type object = blob | tree | commit
```

Git의 저장소에서는 객체의 [SHA-1 해시](https://en.wikipedia.org/wiki/SHA-1)를 주소로 사용합니다.

```
objects = map<string, object>

def store(object):
    id = sha1(object)
    objects[id] = object

def load(id):
    return objects[id]
```

블롭·트리·커밋은 모두 객체라는 개념으로 통일됩니다. 다른 객체를 참조할 때 디스크에 그 내용을 중첩해서 저장하는 것이 아니라 해시로 가리킵니다.

[앞의](#snapshots) 디렉터리 트리를 `git cat-file -p 698281bc680d1995c5f4caaf3359721a5a58d48d`로 보면 다음과 같습니다.

```
100644 blob 4448adbf7ecd394f42ae135bbeed9676e894af85    baz.txt
040000 tree c68d233a33c5c06e0340e4c224f0afca87c8ce87    foo
```

트리는 `baz.txt` 블롭과 `foo` 트리를 가리킵니다. `git cat-file -p 4448adbf7ecd394f42ae135bbeed9676e894af85`로 `baz.txt`의 내용을 읽으면 다음과 같습니다.

```
git is wonderful
```

## 참조
{: #references}

모든 스냅샷을 SHA-1 해시로 구분할 수 있지만, 사람은 40자리 16진수 문자열을 기억하기 어렵습니다.

Git은 해시에 사람이 읽을 수 있는 이름을 붙인 "참조(reference)"로 이를 해결합니다. 참조는 커밋을 가리키는 포인터입니다. 불변 객체와 달리 참조는 새 커밋을 가리키도록 바꿀 수 있습니다. 예를 들어 `master`는 보통 주 개발 브랜치의 최신 커밋을 가리킵니다.

```
references = map<string, string>

def update_reference(name, id):
    references[name] = id

def read_reference(name):
    return references[name]

def load_reference(name_or_id):
    if name_or_id in references:
        return load(references[name_or_id])
    else:
        return load(name_or_id)
```

이제 긴 16진수 대신 `master` 같은 이름으로 이력의 특정 스냅샷을 가리킬 수 있습니다.

새 스냅샷을 만들 때 무엇을 기준으로 하는지, 즉 커밋의 `parents`를 어떻게 정할지 알아야 하므로 "현재 위치"도 필요합니다. 이를 나타내는 특별한 참조가 `HEAD`입니다.

## 저장소
{: #repositories}

Git *저장소(repository)*는 대략 `objects`와 `references`라는 데이터로 정의할 수 있습니다.

Git이 디스크에 저장하는 것은 객체와 참조이며, 이것이 데이터 모델의 전부입니다. 모든 `git` 명령은 객체를 추가하거나 참조를 추가·갱신하여 커밋 DAG를 조작합니다.

명령을 입력할 때마다 그래프가 어떻게 바뀌는지 생각하세요. 반대로 "커밋하지 않은 변경을 버리고 `master`가 `5d83f9e`를 가리키게 한다" 같은 변화가 필요하다면 해당 명령이 있을 것입니다. 이 경우에는 `git checkout master; git reset --hard 5d83f9e`입니다.

# 스테이징 영역
{: #staging-area}

스테이징 영역은 데이터 모델과 별개이지만 커밋을 만드는 인터페이스의 일부입니다.

스냅샷 생성 명령이 작업 디렉터리의 *현재 상태*를 그대로 저장하도록 만들 수도 있습니다. 일부 VCS는 그렇게 하지만 Git은 다릅니다. 정돈된 스냅샷을 원할 때 현재 상태 전체를 저장하는 것이 적절하지 않을 수 있기 때문입니다. 서로 다른 기능 두 개를 구현한 뒤 각각 별도 커밋으로 나누고 싶을 수도 있고, 디버깅 출력문과 버그 수정이 섞여 있을 때 수정만 커밋하고 출력문은 버리고 싶을 수도 있습니다.

Git은 "스테이징 영역"으로 다음 스냅샷에 포함할 변경을 지정하게 합니다.

# Git 명령줄 인터페이스
{: #git-command-line-interface}

중복 설명을 피하기 위해 아래 명령을 자세히 풀지는 않습니다. 강의 영상을 보거나, 적극 권장하는 [Pro Git](https://git-scm.com/book/en/v2)을 참고하세요.

## 기본
{: #basics}

- `git help <command>`: 명령의 도움말을 봅니다.
- `git init`: `.git`에 데이터를 저장하는 새 저장소를 만듭니다.
- `git status`: 현재 상태를 봅니다.
- `git add <filename>`: 파일을 스테이징 영역에 추가합니다.
- `git commit`: 새 커밋을 만듭니다. [좋은 커밋 메시지 작성법](https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html)과 [그 중요성에 관한 글](https://chris.beams.io/posts/git-commit/)도 읽어보세요.
- `git log`: 이력을 일렬로 표시합니다.
- `git log --all --graph --decorate`: 이력을 DAG로 시각화합니다.
- `git diff <filename>`: 스테이징 영역과 비교해 작업 파일의 변경을 봅니다.
- `git diff <revision> <filename>`: 스냅샷 사이의 파일 차이를 봅니다.
- `git checkout <revision>`: HEAD를 갱신합니다. 브랜치를 체크아웃하면 현재 브랜치도 바뀝니다.

## 브랜치와 병합
{: #branching-and-merging}

- `git branch`: 브랜치를 나열합니다.
- `git branch <name>`: 브랜치를 만듭니다.
- `git switch <name>`: 브랜치로 전환합니다.
- `git checkout -b <name>`: 브랜치를 만들고 전환합니다. `git branch <name>; git switch <name>`과 같습니다.
- `git merge <revision>`: 현재 브랜치에 병합합니다.
- `git mergetool`: 도구로 병합 충돌을 해결합니다.
- `git rebase`: 변경 묶음을 새로운 기준 커밋 위에 다시 적용합니다.

## 원격 저장소
{: #remotes}

- `git remote`: 원격 저장소를 나열합니다.
- `git remote add <name> <url>`: 원격 저장소를 추가합니다.
- `git push <remote> <local branch>:<remote branch>`: 객체를 보내고 원격 참조를 갱신합니다.
- `git branch --set-upstream-to=<remote>/<remote branch>`: 로컬·원격 브랜치의 추적 관계를 설정합니다.
- `git fetch`: 원격의 객체와 참조를 가져옵니다.
- `git pull`: `git fetch; git merge`와 같습니다.
- `git clone`: 원격 저장소를 내려받습니다.

## 되돌리기
{: #undo}

- `git commit --amend`: 마지막 커밋의 내용이나 메시지를 수정합니다.
- `git reset <file>`: 파일의 스테이징을 취소합니다.
- `git restore`: 작업 파일의 변경을 버립니다.

# 고급 Git
{: #advanced-git}

- `git config`: Git은 [다양하게 설정](https://git-scm.com/docs/git-config)할 수 있습니다.
- `git clone --depth=1`: 전체 이력 없이 얕게 클론합니다.
- `git add -p`: 변경 조각을 대화형으로 스테이징합니다.
- `git rebase -i`: 대화형으로 리베이스합니다.
- `git blame`: 각 줄을 마지막으로 수정한 사람을 봅니다.
- `git stash`: 작업 디렉터리의 변경을 임시로 보관하고 치웁니다.
- `git bisect`: 회귀 버그 등을 찾기 위해 이력을 이진 탐색합니다.
- `git revert`: 이전 커밋의 효과를 되돌리는 새 커밋을 만듭니다.
- `git worktree`: 여러 브랜치를 동시에 체크아웃합니다.
- `.gitignore`: 추적하지 않을 파일을 [지정](https://git-scm.com/docs/gitignore)합니다.

# 기타
{: #miscellaneous}

- **GUI**: 다양한 [GUI 클라이언트](https://git-scm.com/downloads/guis)가 있습니다. 강사진은 명령줄을 사용합니다.
- **셸 통합**: 프롬프트에 Git 상태를 표시하면 편리합니다([zsh](https://github.com/olivierverdier/zsh-git-prompt), [bash](https://github.com/magicmonty/bash-git-prompt)). [Oh My Zsh](https://github.com/ohmyzsh/ohmyzsh) 같은 프레임워크에 포함되기도 합니다.
- **편집기 통합**: 편집기에서도 다양한 통합 기능을 사용할 수 있습니다. Vim에서는 [fugitive.vim](https://github.com/tpope/vim-fugitive)이 대표적입니다.
- **작업 방식**: 여기서는 데이터 모델과 기본 명령을 배웠습니다. 큰 프로젝트에서 따를 규칙에는 [여러](https://nvie.com/posts/a-successful-git-branching-model/) [서로 다른](https://www.endoflineblog.com/gitflow-considered-harmful) [접근](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)이 있습니다.
- **GitHub**: Git과 GitHub는 다릅니다. GitHub에서는 [풀 리퀘스트](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests)로 다른 프로젝트에 기여합니다.
- **다른 호스팅 서비스**: GitHub 외에도 [GitLab](https://about.gitlab.com/), [BitBucket](https://bitbucket.org/) 등 여러 Git 저장소 호스팅 서비스가 있습니다.

# 참고 자료
{: #resources}

- [Pro Git](https://git-scm.com/book/en/v2)을 **적극 권장합니다**. 데이터 모델을 이해한 상태에서 1~5장을 읽으면 능숙한 사용에 필요한 대부분을 배울 수 있습니다. 뒤에는 흥미로운 고급 내용도 있습니다.
- [Oh Shit, Git!?!](https://ohshitgit.com/): 흔한 실수에서 복구하는 짧은 안내서.
- [Git for Computer Scientists](https://eagain.net/articles/git-for-computer-scientists/): 의사 코드는 적고 그림은 더 많은 데이터 모델 설명.
- [Git from the Bottom Up](https://jwiegley.github.io/git-from-the-bottom-up/): 데이터 모델을 넘어 구현 세부 사항까지 설명합니다.
- [쉬운 말로 Git 설명하기](https://smusamashah.github.io/blog/2017/10/14/explain-git-in-simple-words)
- [Learn Git Branching](https://learngitbranching.js.org/): 브라우저에서 Git을 배우는 게임.

# 연습문제
{: #exercises}

1. 처음 배운다면 [Pro Git](https://git-scm.com/book/en/v2)의 앞부분이나 [Learn Git Branching](https://learngitbranching.js.org/)을 진행하세요. 각 명령을 데이터 모델과 연결해서 이해하세요.
1. [강의 사이트 저장소](https://github.com/missing-semester/missing-semester)를 클론하세요.
   1. 이력을 그래프로 시각화해 탐색하세요.
   1. `README.md`를 마지막으로 수정한 사람은 누구인가요? 힌트: `git log`에 인자를 전달하세요.
   1. `_config.yml`의 `collections:` 줄을 마지막으로 수정한 커밋의 메시지는 무엇인가요? 힌트: `git blame`, `git show`.
1. Git으로 관리하면 안 되는 큰 파일이나 민감한 정보를 커밋하는 것은 흔한 실수입니다. 연습용 파일을 추가하고 커밋을 몇 개 만든 뒤, 최신 커밋뿐 아니라 *전체 이력*에서 삭제해 보세요. [이 안내](https://help.github.com/articles/removing-sensitive-data-from-a-repository/)를 참고할 수 있습니다.
1. GitHub 저장소를 클론해 기존 파일 하나를 수정하세요. `git stash`를 실행하면 어떻게 되나요? `git log --all --oneline`에는 무엇이 보이나요? `git stash pop`으로 변경을 복원하세요. 어떤 상황에서 유용할까요?
1. `~/.gitconfig`에 별칭을 만들어 `git graph`가 `git log --all --graph --decorate --oneline`을 실행하게 하세요. 파일을 직접 [수정](https://git-scm.com/docs/git-config#Documentation/git-config.txt-alias)하거나 `git config`를 사용할 수 있습니다. [별칭 설명](https://git-scm.com/book/en/v2/Git-Basics-Git-Aliases)을 참고하세요.
1. `git config --global core.excludesfile ~/.gitignore_global`로 전역 무시 파일 위치를 지정하고, 해당 파일은 직접 만드세요. `.DS_Store` 같은 운영체제·편집기의 임시 파일을 무시하도록 설정하세요.
1. [강의 사이트 저장소](https://github.com/missing-semester/missing-semester)를 포크하고, 오타나 개선점을 찾아 GitHub에 풀 리퀘스트를 보내세요. [첫 기여 안내](https://github.com/firstcontributions/first-contributions)가 도움이 될 수 있습니다. 유용한 PR만 보내 주세요. 개선점을 못 찾았다면 이 문제는 건너뛰어도 됩니다.
1. 협업 상황을 흉내 내며 병합 충돌을 해결하세요.
   1. `git init`으로 저장소를 만들고 `recipe.txt`에 간단한 조리법 등 몇 줄을 씁니다.
   1. 커밋하고 `git branch salty`, `git branch sweet`로 두 브랜치를 만듭니다.
   1. `salty`에서 "1 cup sugar"를 "1 cup salt"로 바꾸는 식으로 한 줄을 수정하고 커밋합니다.
   1. `sweet`에서 같은 줄을 "2 cups sugar"처럼 다르게 수정하고 커밋합니다.
   1. `master`로 돌아가 `git merge salty`, `git merge sweet`를 차례로 실행합니다. 무슨 일이 생기나요? 파일의 `<<<<<<<`, `=======`, `>>>>>>>` 표시는 무엇인가요?
   1. 원하는 내용만 남기고 충돌 표시를 지운 뒤 `git add`와 `git commit` 또는 `git merge --continue`로 마무리하세요. `git mergetool`로 그래픽·터미널 도구를 써도 됩니다.
   1. `git log --graph --oneline`으로 만든 이력을 확인하세요.
