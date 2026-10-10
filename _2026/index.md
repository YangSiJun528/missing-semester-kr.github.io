---
layout: page
title: "2026년 강의"
description: >
  MIT IAP 2026 Missing Semester의 강의 노트와 영상입니다.
permalink: /2026/
phony: true
---

<ul class="double-spaced">
  {% assign lectures = site['2026'] | sort: 'date' %}
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

녹화된 강의 영상은 [YouTube](https://www.youtube.com/playlist?list=PLyzOVJj3bHQunmnnTXrNbZnBaCA-ieK4L)에서 볼 수 있습니다.

# MIT 밖으로

더 많은 사람이 이 자료를 활용할 수 있도록 MIT 밖에도 수업을 공개했습니다. 아래에서 관련 글과 토론을 볼 수 있습니다.

- [Hacker News](https://news.ycombinator.com/item?id=47124171)
- [Lobsters](https://lobste.rs/s/q4ykw7/missing_semester_your_cs_education_2026)
- [r/learnprogramming](https://www.reddit.com/r/learnprogramming/comments/1r93yk6/the_missing_semester_of_your_cs_education_2026/)
- [X](https://x.com/anishathalye/status/2024521145777848588)
- [Bluesky](https://bsky.app/profile/jonhoo.eu/post/3mfa2bhyuj22i)
- [Mastodon](https://fosstodon.org/@jonhoo/116098318361854057)
- [LinkedIn](https://www.linkedin.com/posts/anishathalye_i-returned-to-mit-during-iap-january-term-activity-7430285026933522433-Ehr9)
- [YouTube](https://www.youtube.com/playlist?list=PLyzOVJj3bHQunmnnTXrNbZnBaCA-ieK4L)

# 감사의 말

강의 영상 녹화를 도와준 Elaine Mello와 [MIT Open Learning](https://openlearning.mit.edu/)에 감사드립니다. 이 수업을 [SIPB IAP 2026](https://sipb.mit.edu/iap/)의 일부로 지원한 Luis Turino와 [SIPB](https://sipb.mit.edu/)에도 감사드립니다.
