---
layout: page
title: 여러분의 CS 교육에서 누락된 학기
description: >
  컴퓨터 과학자와 프로그래머의 생산성을 높여 주는 강력한 도구를 배웁니다.
# subtitle: IAP 2026
subtitle: "2026"
nositetitle: true
---

CS 교과과정에서는 운영체제부터 기계학습까지 고급 주제를 배우지만, 정작 거의 다루지 않아 학생들이 스스로 익혀야 하는 중요한 주제가 있습니다. 바로 도구를 능숙하게 사용하는 법입니다. 이 수업에서는 명령줄을 자유롭게 다루는 법, 강력한 텍스트 편집기를 사용하는 법, 버전 관리 시스템의 다양한 기능을 활용하는 법 등을 배웁니다.

학생들은 학업 중에 이런 도구를 수백 시간 사용하고, 실무에서는 수천 시간 사용합니다. 도구를 쓰는 과정이 매끄러울수록 좋습니다. 도구를 익혀 두면 원하는 작업을 수행하는 방법을 알아내는 시간을 줄일 수 있고, 이전에는 너무 복잡해 보였던 문제도 해결할 수 있습니다.

최근에는 AI를 활용하는 도구와 작업 방식이 도입되면서 소프트웨어 공학의 여러 영역이 변화하고 있습니다. 한계를 이해하고 적절하게 사용하면 실무에 큰 도움이 되므로, 사용법을 익혀 둘 가치가 있습니다. AI는 여러 분야에 걸쳐 활용되므로 별도의 AI 개론 강의를 두기보다는 각 강의에 관련된 최신 AI 도구와 기법을 포함했습니다.

[이 수업을 만든 이유](/about/)를 읽어보세요.

{% comment %}
# Registration

Sign up for the IAP 2026 class by filling out this [registration form](https://forms.gle/j2wMzi7qeiZmzEWy9).
{% endcomment %}

# 강의 일정

{% comment %}
**Lecture**: [35-225](https://whereis.mit.edu/?go=35), 1:30--2:30pm (_exception_: 3--4pm on Friday 1/16)<br>
**Discussion**: [OSSU Discord](https://ossu.dev/#community) (use `#missing-semester-forum` like you would use Piazza, and `#missing-semester` to chat with the class/instructors)
{% endcomment %}

<ul>
{% assign lectures = site['2026'] | sort: 'date' %}
{% for lecture in lectures %}
    {% if lecture.phony != true %}
        <li>
        <strong>{{ lecture.date | date: '%-m/%-d/%y' }}</strong>:
        {% if lecture.ready %}
            <a href="{{ lecture.url }}">{{ lecture.title }}</a>
        {% else %}
            {{ lecture.title }} {% if lecture.noclass %}[휴강]{% endif %}
        {% endif %}
        </li>
    {% endif %}
{% endfor %}
</ul>

## 이전 강의의 특별 주제

강의 주제는 해마다 달라집니다. 지금까지 다룬 모든 주제를 공부하고 싶은 분들을 위해, 이전 강의에서 다뤘지만 2026년에는 다루지 않은 주제를 모았습니다.

{% comment %} pop to remove default "posts" collection {% endcomment %}
{% assign sorted_collections = site.collections | sort: 'label' | pop | reverse %}
<ul>
{% for collection in sorted_collections %}
    {% assign grouped_lectures = site[collection.label] | group_by: 'date' | sort: 'name' %}
    {% for group in grouped_lectures %}
        {% assign sorted_lectures = group.items | sort: 'order' %}
        {% for lecture in sorted_lectures %}
            {% if lecture.special == true %}
                <li>
                    <strong>{{ lecture.date | date: '%-m/%-d/%y' }}</strong>:
                    <a href="{{ lecture.url }}">{{ lecture.title }}</a>
                </li>
            {% endif %}
        {% endfor %}
    {% endfor %}
{% endfor %}
</ul>

{% comment %}
Lecture videos will be made available to MIT students immediately after lecture (via Panopto). The system has a limitation that only those with an MIT Kerberos can access the raw lecture videos. We are working on editing lecture videos and uploading them to YouTube. A couple have been uploaded already; we expect the rest to be uploaded by mid-February.

If you can't wait until January 2026, you can also take a look at the lectures
from the [previous offering of the course](/2020/), which covers many of the
same topics.
{% endcomment %}

# 수업 안내

**강사진**: [Anish](https://anish.io/), [Jon](https://thesquareplanet.com/), [Jose](https://josejg.com/)가 함께 가르칩니다.<br>
**문의**: [missing-semester@mit.edu](mailto:missing-semester@mit.edu)로 이메일을 보내세요.<br>
**토론**: [OSSU Discord](https://ossu.dev/#community)의 `#missing-semester-forum`은 Piazza 같은 질문 게시판으로, `#missing-semester`는 수강생·강사진과 대화하는 채널로 사용하세요.

# MIT 밖으로

더 많은 사람이 이 자료를 활용할 수 있도록 MIT 밖에도 수업을 공개했습니다. 아래에서 관련 글과 토론을 볼 수 있습니다.

 - Hacker News ([2026](https://news.ycombinator.com/item?id=47124171), [2020](https://news.ycombinator.com/item?id=22226380), [2019](https://news.ycombinator.com/item?id=19078281))
 - Lobsters ([2026](https://lobste.rs/s/q4ykw7/missing_semester_your_cs_education_2026), [2020](https://lobste.rs/s/ti1k98/missing_semester_your_cs_education_mit), [2019](https://lobste.rs/s/h6157x/mit_hacker_tools_lecture_series_on))
 - r/learnprogramming ([2026](https://www.reddit.com/r/learnprogramming/comments/1r93yk6/the_missing_semester_of_your_cs_education_2026/), [2020](https://www.reddit.com/r/learnprogramming/comments/eyagda/the_missing_semester_of_your_cs_education_mit/), [2019](https://www.reddit.com/r/learnprogramming/comments/an42uu/mit_hacker_tools_a_lecture_series_on_programmer/))
 - r/programming ([2020](https://www.reddit.com/r/programming/comments/eyagcd/the_missing_semester_of_your_cs_education_mit/), [2019](https://www.reddit.com/r/programming/comments/an3xki/mit_hacker_tools_a_lecture_series_on_programmer/))
 - X ([2026](https://x.com/anishathalye/status/2024521145777848588), [2020](https://twitter.com/jonhoo/status/1224383452591509507), [2019](https://x.com/jonhoo/status/1090323977766137858))
 - Bluesky ([2026](https://bsky.app/profile/jonhoo.eu/post/3mfa2bhyuj22i))
 - Mastodon ([2026](https://fosstodon.org/@jonhoo/116098318361854057))
 - LinkedIn ([2026](https://www.linkedin.com/posts/anishathalye_i-returned-to-mit-during-iap-january-term-activity-7430285026933522433-Ehr9))
 - YouTube ([2026](https://www.youtube.com/playlist?list=PLyzOVJj3bHQunmnnTXrNbZnBaCA-ieK4L), [2020](https://www.youtube.com/playlist?list=PLyzOVJj3bHQuloKGG59rS43e29ro7I57J), [2019](https://www.youtube.com/playlist?list=PLyzOVJj3bHQuiujH1lpn8cA9dsyulbYRv))

# 다른 언어 번역

{% comment %} keep these in alphabetical order {% endcomment %}

- [아랍어](https://missing-semester-ar.github.io/)
- [벵골어](https://missing-semester-bn.github.io/)
- [버마어](https://missing-semester-my.github.io/)
- [중국어(간체)](https://missing-semester-cn.github.io/)
- [중국어(번체, 대만)](https://missing-semester-tw.github.io/)
- [독일어](https://missing-semester-de.github.io/)
- [이탈리아어](https://missing-semester-it.github.io/)
- [일본어](https://missing-semester-jp.github.io/)
- [칸나다어](https://missing-semester-kn.github.io/)
- [한국어](https://missing-semester-kr.github.io/)
- [몽골어](https://missing-semester-mn.github.io)
- [페르시아어](https://missing-semester-fa.github.io/)
- [포르투갈어](https://missing-semester-pt.github.io/)
- [러시아어](https://missing-semester-rus.github.io/)
- [세르비아어](https://netboxify.com/missing-semester/)
- [스페인어](https://missing-semester-esp.github.io/)
- [스웨덴어](https://den-saknade-terminen.l10n.se/)
- [태국어](https://missing-semester-th.github.io/)
- [튀르키예어](https://missing-semester-tr.github.io/)
- [베트남어](https://missing-semester-vn.github.io/)

참고: 커뮤니티 번역으로 연결되는 외부 링크입니다. 원 강사진이 번역 내용을 검증한 것은 아닙니다.

강의 노트를 번역하셨나요? 목록에 추가할 수 있도록 영문 원본 저장소에 [풀 리퀘스트](https://github.com/missing-semester/missing-semester/pulls)를 보내 주세요.

## 감사의 말

{% comment %}
2026 acks; previous years' acks are on their respective pages
{% endcomment %}

강의 영상 녹화를 도와준 Elaine Mello와 [MIT Open Learning](https://openlearning.mit.edu/)에 감사드립니다. 이 수업을 [SIPB IAP 2026](https://sipb.mit.edu/iap/)의 일부로 지원한 Luis Turino와 [SIPB](https://sipb.mit.edu/)에도 감사드립니다.

---

<div class="small center">
<p><a href="https://github.com/missing-semester/missing-semester">원본 코드</a>.</p>
<p>CC BY-NC-SA 라이선스를 따릅니다.</p>
<p><a href="/license/">기여 및 번역 지침</a>을 참고하세요.</p>
</div>
