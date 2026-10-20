---
layout: page
title: 여러분의 CS 교육에서 누락된 학기
description: >
  Master powerful tools that will make you a more productive computer scientist and programmer.
# subtitle: IAP 2026
subtitle: "2026"
nositetitle: true
---

CS 교과과정은 운영체제에서 기계학습에 이르기까지 CS 내의 고급 주제에 대해 모두 가르쳐 주지만, 거의 다루지 않는 중요한 한 가지 과목이 있으며,
대신 학생들이 스스로 알아내야 하는 툴의 숙련도가 있습니다. 이 수업에서 우리는 여러분에게 command line을 마스터하는 방법, 강력한 text editor 사용, 
version control system의 화려한 기능 사용 방법 등을 가르쳐 줄 것입니다!

학생들은 교육 과정 동안 이러한 툴을 사용하여 수백 시간을 보내므로, 가능한 한 유연하고 마찰이 없는 경험을 하는 것이 이치에 맞습니다.
이러한 툴들을 마스터하게 되면 자유자재로 툴을 알맞게 사용하는 방법을 알아가는 시간을 덜 쓸 수 있을 뿐만 아니라 이전에 불가능할 정도로 복잡해 보였던 문제들을 해결할 수 있습니다.

요즘은 AI를 활용한 도구와 작업 방식이 도입되면서 소프트웨어 엔지니어링의 여러 측면도 변화하고 있습니다.
한계를 인식하고 적절하게 사용하면 컴퓨터 과학 분야의 실무에 상당한 이점을 줄 수 있으므로, 이를 활용하는 지식을 익힐 만한 가치가 있습니다.
AI는 여러 분야에 걸쳐 활용되는 기술이므로 별도의 AI 강의를 두지 않았습니다. 대신 각 강의에 적용할 수 있는 최신 AI 도구와 기법을 직접 포함했습니다.

이 [수업의 동기](/about/)에 대해 읽어보세요.

{% comment %}
# Registration

Sign up for the IAP 2026 class by filling out this [registration form](https://forms.gle/j2wMzi7qeiZmzEWy9).
{% endcomment %}

# 강의 계획

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
            {{ lecture.title }} {% if lecture.noclass %}[no class]{% endif %}
        {% endif %}
        </li>
    {% endif %}
{% endfor %}
</ul>

## 이전 수업의 특별 주제

수업에서 다루는 주제는 해마다 다릅니다. 지금까지 다룬 모든 주제에 관심 있는 학생들을 위해, 이전 수업에서 다루었지만 2026년에는 다루지 않은 주제를 소개합니다.

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

# 일반 안내

**Staff**: 이 수업은 [Anish](https://anish.io/), [Jon](https://thesquareplanet.com/), 그리고 [Jose](https://josejg.com/)가 함께 가르칩니다.<br>
**Questions**: [missing-semester@mit.edu](mailto:missing-semester@mit.edu)로 Email을 보내주시면 됩니다.<br>
**Discussion**: [OSSU Discord](https://ossu.dev/#community) (`#missing-semester-forum`은 Piazza처럼 사용하고, `#missing-semester`에서는 수강생 및 강사와 대화할 수 있습니다).

# Beyond MIT

또한 우리는 다른 이들이 이런 자료로부터 이익을 얻을 수 있기 바라면서 MIT를 뿐만 아니라 외부와 이 수업을 공유해 왔습니다. 이 수업에 대한 게시물과 토론은 아래와 같습니다:

 - Hacker News ([2026](https://news.ycombinator.com/item?id=47124171), [2020](https://news.ycombinator.com/item?id=22226380), [2019](https://news.ycombinator.com/item?id=19078281))
 - Lobsters ([2026](https://lobste.rs/s/q4ykw7/missing_semester_your_cs_education_2026), [2020](https://lobste.rs/s/ti1k98/missing_semester_your_cs_education_mit), [2019](https://lobste.rs/s/h6157x/mit_hacker_tools_lecture_series_on))
 - r/learnprogramming ([2026](https://www.reddit.com/r/learnprogramming/comments/1r93yk6/the_missing_semester_of_your_cs_education_2026/), [2020](https://www.reddit.com/r/learnprogramming/comments/eyagda/the_missing_semester_of_your_cs_education_mit/), [2019](https://www.reddit.com/r/learnprogramming/comments/an42uu/mit_hacker_tools_a_lecture_series_on_programmer/))
 - r/programming ([2020](https://www.reddit.com/r/programming/comments/eyagcd/the_missing_semester_of_your_cs_education_mit/), [2019](https://www.reddit.com/r/programming/comments/an3xki/mit_hacker_tools_a_lecture_series_on_programmer/))
 - X ([2026](https://x.com/anishathalye/status/2024521145777848588), [2020](https://twitter.com/jonhoo/status/1224383452591509507), [2019](https://x.com/jonhoo/status/1090323977766137858))
 - Bluesky ([2026](https://bsky.app/profile/jonhoo.eu/post/3mfa2bhyuj22i))
 - Mastodon ([2026](https://fosstodon.org/@jonhoo/116098318361854057))
 - LinkedIn ([2026](https://www.linkedin.com/posts/anishathalye_i-returned-to-mit-during-iap-january-term-activity-7430285026933522433-Ehr9))
 - YouTube ([2026](https://www.youtube.com/playlist?list=PLyzOVJj3bHQunmnnTXrNbZnBaCA-ieK4L), [2020](https://www.youtube.com/playlist?list=PLyzOVJj3bHQuloKGG59rS43e29ro7I57J), [2019](https://www.youtube.com/playlist?list=PLyzOVJj3bHQuiujH1lpn8cA9dsyulbYRv))

## Acknowledgments

{% comment %}
2026 acks; previous years' acks are on their respective pages
{% endcomment %}

이 수업의 비디오를 녹화할 수 있게 도와준 Elaine Mello와 [MIT Open Learning](https://openlearning.mit.edu/)에 감사드립니다. [SIPB IAP 2026](https://sipb.mit.edu/iap/)의 일부로 이 수업을 지원한 Luis Turino / [SIPB](https://sipb.mit.edu/)에 감사드립니다.

---

<div class="small center">
<p><a href="https://github.com/missing-semester/missing-semester">원본 코드</a>.</p>
<p>CC BY-NC-SA에 따라 라이센스를 부여합니다</p>
<p>기여 &amp; 번역 지침은 <a href="/license/">여기</a>를 참조하세요.</p>
</div>
