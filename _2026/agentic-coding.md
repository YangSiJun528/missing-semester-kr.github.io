---
layout: lecture
title: "에이전트 코딩"
description: >
  소프트웨어 개발 작업에 AI 코딩 에이전트를 효과적으로 사용하는 법을 배웁니다.
thumbnail: /static/assets/thumbnails/2026/lec7.png
date: 2026-01-21
ready: true
video:
  aspect: 56.25
  id: sTdz6PZoAnw
---

코딩 에이전트는 파일 읽기·쓰기, 웹 검색, 셸 명령 실행 같은 도구에 접근할 수 있는 대화형 AI 모델입니다. IDE 안에서 또는 독립적인 명령줄·GUI 도구로 실행됩니다. 자율성이 높고 강력해 다양한 작업에 활용할 수 있습니다.

이번 강의는 [개발 환경과 도구](/2026/development-environment/)의 AI 개발 내용을 바탕으로 합니다. [AI를 활용한 개발](/2026/development-environment/#ai-powered-development)에서 만든 예제를 이어서 보겠습니다.

```python
from urllib.request import urlopen

def download_contents(url: str) -> str:
    with urlopen(url) as response:
        return response.read().decode('utf-8')

def extract(content: str) -> list[str]:
    import re
    pattern = r'\[.*?\]\((.*?)\)'
    return re.findall(pattern, content)

print(extract(download_contents("https://raw.githubusercontent.com/missing-semester/missing-semester/refs/heads/master/_2026/development-environment.md")))
```

에이전트에게 "argparse로 인자를 파싱하는 제대로 된 명령줄 프로그램으로 바꾸고, 타입 표기를 추가해 타입 검사를 통과하게 해 줘"라고 요청할 수 있습니다.

```
Turn this into a proper command-line program, with argparse for argument parsing. Add type annotations, and make sure the program passes type checking.
```

에이전트는 파일을 읽고 이해한 다음 수정하고, 타입 검사기로 확인합니다. 검사에 실패하면 보통 다시 수정합니다. 이 예는 단순해 실패할 가능성이 낮습니다. 에이전트의 도구는 유해한 결과도 낼 수 있으므로, 실행 환경인 하네스(harness)는 기본적으로 도구 호출을 사용자에게 확인받게 하곤 합니다.

> 예를 들어 `$PATH`에 `mypy`가 직접 있는데 에이전트가 `python -m mypy`를 실행해 실패한다면, 텍스트로 알려 주어 방향을 수정할 수 있습니다.

여러 차례 대화하며 작업을 발전시킬 수 있고, 잘못된 방향으로 가면 중단시킬 수도 있습니다. 인턴을 관리하는 상황을 떠올리면 이해하기 쉽습니다. 세부 작업을 맡기되 지침을 주고, 때로는 잘못된 결과를 바로잡아야 합니다.

> 결과 스크립트를 실행하라고 후속 요청을 해 보세요. 출력을 확인하고 절대 URL만 포함하도록 하는 등 변경도 요청해 보세요.

# AI 모델과 에이전트의 작동 원리
{: #how-ai-models-and-agents-work}

현대 [대규모 언어 모델(LLM)](https://en.wikipedia.org/wiki/Large_language_model)과 에이전트 하네스의 내부를 모두 설명하는 것은 이 수업의 범위를 벗어납니다. 하지만 핵심 개념을 알면 최신 기술을 효과적으로 *사용*하고 한계를 이해하는 데 도움이 됩니다.

LLM은 입력인 프롬프트 문자열이 주어졌을 때 출력 문자열의 확률 분포를 모델링한다고 볼 수 있습니다. 대화형 앱에 질문할 때 수행되는 추론은 이 분포에서 출력을 *샘플링*합니다. 입력과 출력의 최대 길이에 해당하는 *컨텍스트 창*도 정해져 있습니다.

{% comment %}
수식으로는 프롬프트 $x$에 대한 출력 $y$의 분포 $\pi_\theta$에서 $\hat{y} \sim \pi_\theta(\cdot \mid x)$를 샘플링합니다.
{% endcomment %}

채팅 앱과 코딩 에이전트는 이 기능 위에 만들어집니다. 여러 차례 대화하려면 발화 구분자를 사용해 새 사용자 입력 때마다 전체 대화 기록을 프롬프트로 넣고 추론합니다. 도구 호출 에이전트에서는 하네스가 특정 출력을 도구 실행 요청으로 해석하고, 실행 결과를 다시 프롬프트에 넣습니다. 따라서 도구를 호출하고 응답을 받을 때마다 추론이 다시 수행됩니다. 이 핵심 구조는 [200줄 코드로도 구현](https://www.mihaileric.com/The-Emperor-Has-No-Clothes/)할 수 있습니다.

## 개인정보와 데이터
{: #privacy}

대부분의 AI 코딩 도구는 기본 설정에서 많은 데이터를 클라우드로 보냅니다. 하네스만 로컬에서 돌고 추론은 클라우드에서 실행되기도 하며, 더 많은 구성 요소가 클라우드에 있기도 합니다. 서비스 제공자가 전체 저장소와 모든 상호작용의 사본을 사실상 받는 경우도 있습니다.

성능이 상당한 오픈 소스 도구와 모델도 있지만, 독점 모델에는 다소 못 미칩니다. 현재 대부분의 사용자는 하드웨어의 한계로 인해 최신 공개 LLM을 로컬에서 실행하기 어렵습니다.

# 활용 사례
{: #use-cases}

다양한 작업에 사용할 수 있습니다.

- **새 기능 구현**: 앞의 예처럼 기능을 요청합니다. 좋은 명세 작성에는 경험이 필요합니다. 원하는 방향으로 가기에 충분히 구체적이어야 하지만, 설명하느라 직접 구현하는 것만큼 일할 필요는 없습니다. 테스트 주도 개발이 특히 효과적일 수 있습니다. 테스트를 직접 쓰거나 에이전트의 도움으로 작성하고, 의도를 제대로 검증하는지 검토한 뒤 구현을 맡기세요. 모델은 계속 좋아지므로 가능한 작업에 대한 감각도 갱신해야 합니다.

  > 강의 사이트의 Tufte식 곁주석은 Claude Code로 [구현](https://github.com/missing-semester/missing-semester/pull/345)했습니다.

- **오류 수정**: 컴파일러, 린터, 타입 검사기, 테스트 오류를 고치게 할 수 있습니다. 예를 들어 "mypy 오류를 고쳐 줘"라고 요청합니다. 모델이 실패한 검사를 직접 실행하고 반복하도록 피드백 경로를 마련하면 특히 효과적입니다. 어렵다면 결과를 수동으로 알려 주세요.

  > 저장소의 [f552b55](https://github.com/missing-semester/missing-semester/commit/f552b5523462b22b8893a8404d2110c4e59613dd)에서 Claude Code에 에이전트 코딩 강의의 오타와 문법 문제를 검토하고 수정하도록 요청했습니다. 결과는 [f1e1c41](https://github.com/missing-semester/missing-semester/commit/f1e1c417adba6b4149f7eef91ff5624de40dc637)에 커밋했습니다.

- **리팩터링**: [코드 분석 도구](/2026/development-environment/#code-intelligence-and-language-servers)로도 가능한 메서드 이름 변경부터 기능을 별도 모듈로 분리하는 복잡한 작업까지 맡길 수 있습니다.

  > 에이전트 코딩 내용을 독립된 강의로 [분리](https://github.com/missing-semester/missing-semester/pull/344)할 때 Claude Code를 사용했습니다.

- **코드 리뷰**: "아직 커밋하지 않은 최신 변경을 검토해 줘"처럼 요청할 수 있습니다. 웹 내용을 가져올 수 있거나 [GitHub CLI](https://cli.github.com/)가 설치되어 있다면 "이 풀 리퀘스트를 검토해 줘: {링크}"만으로도 진행할 수 있습니다.
- **코드 이해**: 코드베이스에 관해 질문할 수 있습니다. 새 프로젝트에 익숙해질 때 특히 유용합니다.
- **셸처럼 사용**: "find로 30일보다 오래된 파일을 찾아 줘", "mogrify로 모든 jpg를 원래 크기의 50%로 줄여 줘"처럼 자연어로 도구를 실행하게 할 수 있습니다.
- **바이브 코딩**: 직접 코드를 한 줄도 쓰지 않고 일부 애플리케이션을 만들 수 있을 만큼 강력합니다.

  > 강사진 한 명이 실제로 바이브 코딩으로 만든 [프로젝트 예](https://github.com/cleanlab/office-presence-dashboard)입니다.

# 에이전트 고급 활용
{: #advanced-agents}

더 발전된 기능과 사용 패턴을 간단히 살펴봅니다.

- **재사용 프롬프트**: 특정 방식의 코드 리뷰처럼 상세한 지시를 템플릿으로 저장해 반복 사용합니다.

  > 도구는 빠르게 변합니다. 독립적인 재사용 프롬프트 기능을 폐기한 도구도 있습니다. Codex와 Claude Code에서는 이 기능이 [스킬에](https://developers.openai.com/codex/custom-prompts) [통합](https://code.claude.com/docs/en/skills)되었습니다.

- **병렬 에이전트**: 한 작업에 수십 분이 걸릴 수 있습니다. 여러 에이전트를 동시에 실행해 같은 작업을 시도하고 가장 좋은 결과를 고르거나(LLM은 확률적으로 동작합니다), 겹치지 않는 두 기능을 나눠 구현할 수 있습니다. 변경이 서로 방해하지 않도록 [버전 관리 강의](/2026/version-control/)의 [Git worktree](https://git-scm.com/docs/git-worktree)를 사용할 수 있습니다.
- **MCP**: *Model Context Protocol*은 에이전트에 도구를 연결하는 공개 프로토콜입니다. [Notion MCP 서버](https://github.com/makenotion/notion-mcp-server)를 연결하면 "이 Notion 문서의 명세를 읽고, 새 페이지에 구현 계획을 쓴 뒤, 프로토타입을 구현해 줘" 같은 작업이 가능합니다. [Pulse](https://www.pulsemcp.com/servers), [Glama](https://glama.ai/mcp/servers)에서 서버를 찾을 수 있습니다.
- **컨텍스트 관리**: [앞서](#how-ai-models-and-agents-work) 설명했듯 컨텍스트 창은 유한합니다. 필요한 정보는 주되 불필요한 정보로 채우지 않아야 합니다. 한도를 넘지 않아도 컨텍스트가 커지면 성능이 떨어지곤 합니다. 하네스가 일부를 자동 관리하지만 사용자에게 남은 제어도 많습니다.
  - **컨텍스트 비우기**: 관련 없는 질문에는 새 대화를 시작하세요.
  - **대화 되돌리기**: 일부 에이전트는 이전 단계를 취소할 수 있습니다. 후속 지시를 덧붙이는 것보다 되돌리는 편이 맞는 상황에서는 컨텍스트도 더 효율적으로 관리됩니다.
  - **압축**: 대화가 너무 길어지면 LLM으로 앞부분을 요약하고 그 기록을 요약문으로 대체합니다. 일부 도구는 사용자가 원하는 때에 압축할 수 있습니다.
  - **llms.txt**: `/llms.txt`는 추론 시 LLM이 읽을 문서의 위치로 제안된 [표준](https://llmstxt.org/)입니다. [Cursor](https://cursor.com/llms.txt) 같은 제품, [Pydantic AI](https://ai.pydantic.dev/llms.txt) 같은 라이브러리, [Apify](https://apify.com/llms.txt) 같은 API가 제공하기도 합니다. HTML보다 토큰당 정보 밀도가 높아 컨텍스트를 절약합니다. 모델의 지식 기준일 이후에 나온 라이브러리처럼 내장 지식이 없는 의존성을 다룰 때 외부 문서가 유용합니다.
  - **AGENTS.md**: 많은 에이전트가 [AGENTS.md](https://agents.md/)나 유사 파일을 에이전트용 README로 읽습니다. Claude Code는 `CLAUDE.md`를 사용합니다. 시작할 때 내용을 컨텍스트에 넣으므로, 코드 변경 후 타입 검사를 하라는 지시, 단위 테스트 실행법, 외부 문서 링크 등 여러 세션에 공통된 정보를 담을 수 있습니다. Claude Code의 `/init`처럼 자동 생성 기능도 있습니다. [실제 예](https://github.com/pydantic/pydantic-ai/blob/main/CLAUDE.md)를 참고하세요.
  - **스킬**: `AGENTS.md` 전체는 항상 컨텍스트에 들어갑니다. 스킬은 이름과 설명만 먼저 제공하고, 필요할 때 본문을 열어 읽게 하여 컨텍스트가 불필요하게 커지는 것을 줄입니다.
  - **하위 에이전트**: 특정 작업을 맡는 에이전트를 정의하고 상위 에이전트가 호출할 수 있는 도구도 있습니다. 상위 에이전트는 하위 에이전트가 본 모든 내용을 받아들일 필요가 없고, 하위 에이전트는 필요한 정보만 받으므로 각각 컨텍스트를 관리하기 쉽습니다. 웹 조사 하위 에이전트라면 질문을 받아 검색·페이지 수집·분석을 수행하고 답만 돌려줍니다. 상위 컨텍스트에 모든 웹페이지가 들어오지 않고, 하위 컨텍스트에도 상위 대화 전체가 들어오지 않습니다.

스킬이나 하위 에이전트처럼 프롬프트를 작성하는 기능은 LLM으로 초안을 만들 수 있습니다. 이를 내장한 도구도 있습니다. 예를 들어 Claude Code의 `/agents`에서 새 에이전트를 만들며 "마지막 Git 커밋 이후 바뀐 파일을 mypy와 ruff로 타입 검사·린트·서식 검사하는 Python 코드 검사 에이전트"라고 요청해 보세요.

```
A Python code checking agent that uses `mypy` and `ruff` to type-check, lint, and format *check* any files that have been modified from the last git commit.
```

이후 상위 에이전트에 "코드 검사 하위 에이전트를 사용해 줘"라고 요청할 수 있습니다. Python 파일 변경 후처럼 적절한 시점에 자동 호출하도록 설정할 수도 있습니다.

# 주의할 점
{: #what-to-watch-out-for}

AI 도구도 실수합니다. 바탕이 되는 LLM은 확률적인 다음 토큰 예측 모델이며 사람과 같은 방식으로 "지능적"이지 않습니다. 결과의 정확성과 보안 오류를 검토하세요. 코드를 검증하는 일이 직접 작성하는 것보다 어려울 때도 있으므로 중요한 코드는 직접 작성하는 방안을 고려하세요. AI가 잘못된 방향으로 계속 파고들거나 틀린 설명을 확신하며 반복할 수 있으니 디버깅이 끝없이 맴도는 상황에 주의하세요. AI에 의존해 이해를 얕게 유지하지 마세요. 아직 수행하지 못하는 프로그래밍 작업도 많으며, 컴퓨팅 사고력은 여전히 중요합니다.

# 권장 소프트웨어
{: #recommended-software}

많은 IDE와 AI 코딩 확장에 에이전트가 포함되어 있습니다([개발 환경 강의](/2026/development-environment/) 참고). 다른 대표 도구로 Anthropic의 [Claude Code](https://www.claude.com/product/claude-code), OpenAI의 [Codex](https://openai.com/codex/), 오픈 소스 [opencode](https://github.com/anomalyco/opencode)가 있습니다.

# 연습문제
{: #exercises}

1. 같은 작업을 직접 작성, AI 자동 완성, 인라인 채팅, 에이전트로 각각 수행하고 경험을 비교하세요. 작업 중인 프로젝트의 작은 기능이 좋습니다. GitHub의 "good first issue", [Advent of Code](https://adventofcode.com/), [LeetCode](https://leetcode.com/) 문제도 가능합니다.
1. 익숙하지 않은 코드베이스를 에이전트로 탐색하세요. 관심 있는 프로젝트의 디버깅이나 기능 추가를 목표로 하면 좋습니다. 떠오르는 프로젝트가 없다면 [opencode](https://github.com/anomalyco/opencode)의 보안 관련 기능을 이해해 보세요.
1. 작은 앱을 처음부터 바이브 코딩으로 만드세요. 직접 코드는 한 줄도 쓰지 마세요.
1. 선택한 에이전트용 `AGENTS.md` 또는 `CLAUDE.md`, 스킬([Claude Code](https://code.claude.com/docs/en/skills), [Codex](https://developers.openai.com/codex/skills/)), 하위 에이전트([Claude Code](https://code.claude.com/docs/en/sub-agents))를 만들고 시험하세요. 각각 언제 적합한지 생각해 보세요. 지원하지 않는 기능은 건너뛰거나 다른 도구에서 시도하세요.
1. [코드 품질 강의](/2026/code-quality/)의 Markdown 목록 정규 표현식 문제를 에이전트로 해결하세요. 파일을 직접 편집하나요? 이 방법의 단점과 한계는 무엇인가요? 직접 편집하지 않고 해결하게 할 프롬프트를 찾아보세요. 힌트: [첫 강의](/2026/course-shell/)의 명령줄 도구를 사용하도록 요청하세요.
1. 대부분의 에이전트는 Claude Code의 `--dangerously-skip-permissions` 같은 "yolo 모드"를 지원합니다. 그대로 쓰는 것은 안전하지 않지만, VM이나 컨테이너에 격리한 뒤 자율 실행하는 것은 허용할 만한 상황이 있을 수 있습니다. 이런 환경을 구성해 보세요. [Claude Code 개발 컨테이너](https://code.claude.com/docs/en/devcontainer), [Docker Sandboxes의 Claude Code](https://docs.docker.com/ai/sandboxes/agents/claude-code/) 문서를 참고할 수 있으며 방법은 여러 가지입니다.
