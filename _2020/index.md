---
layout: page
title: "2020년 강의"
description: >
  MIT IAP 2020 Missing Semester의 강의 노트와 영상입니다.
permalink: /2020/
phony: true
---

<ul class="double-spaced">
  {% assign lectures = site['2020'] | sort: 'date' %}
  {% for lecture in lectures %}
    {% if lecture.phony != true %}
      <li>
        <strong>{{ lecture.date | date: '%-m/%-d' }}</strong>:
        {% if lecture.ready %}
          <a href="{{ lecture.url }}">{{ lecture.title }}</a>
        {% elsif lecture.noclass %}
          {{ lecture.title }} [휴강]
        {% else %}
          {{ lecture.title }} [공개 예정]
        {% endif %}
        {% if lecture.details %}
          <br>
          ({{ lecture.details }})
        {% endif %}
      </li>
    {% endif %}
  {% endfor %}
</ul>

녹화된 강의 영상은 [YouTube](https://www.youtube.com/playlist?list=PLyzOVJj3bHQuloKGG59rS43e29ro7I57J)에서 볼 수 있습니다.

# MIT 밖으로

더 많은 사람이 이 자료를 활용할 수 있도록 MIT 밖에도 수업을 공개했습니다. 아래에서 관련 글과 토론을 볼 수 있습니다.

 - [Hacker News](https://news.ycombinator.com/item?id=22226380)
 - [Lobsters](https://lobste.rs/s/ti1k98/missing_semester_your_cs_education_mit)
 - [r/learnprogramming](https://www.reddit.com/r/learnprogramming/comments/eyagda/the_missing_semester_of_your_cs_education_mit/)
 - [r/programming](https://www.reddit.com/r/programming/comments/eyagcd/the_missing_semester_of_your_cs_education_mit/)
 - [Twitter](https://twitter.com/jonhoo/status/1224383452591509507)
 - [YouTube](https://www.youtube.com/playlist?list=PLyzOVJj3bHQuloKGG59rS43e29ro7I57J)

{% comment %}
Some more URLs:

- https://news.ycombinator.com/item?id=27154577
- https://news.ycombinator.com/item?id=34934216
- https://www.reddit.com/r/learnprogramming/comments/nca1v3/mit_the_missing_semester_of_your_cs_education/
- https://www.reddit.com/r/compsci/comments/eyywv8/the_missing_semester_of_your_cs_education_from_mit/
- https://www.reddit.com/r/programming/comments/io7nq3/the_missing_semester_of_your_cs_education_mit/
- https://twitter.com/MIT_CSAIL/status/1349766980413263873
- https://twitter.com/MIT_CSAIL/status/1481676163491659780
- https://twitter.com/MIT_CSAIL/status/1581313961093484545
{% endcomment %}

# 감사의 말

강의 영상 녹화를 도와준 Elaine Mello, Jim Cain, [MIT Open Learning](https://openlearning.mit.edu/), 시청각 장비를 지원한 Anthony Zolnik과 [MIT AeroAstro](https://aeroastro.mit.edu/), 수업을 지원한 Brandi Adams와 [MIT EECS](https://www.eecs.mit.edu/)에 감사드립니다.
