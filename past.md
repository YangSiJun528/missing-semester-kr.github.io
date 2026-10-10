---
layout: page
title: 지난 강의
description: >
  연도별 Missing Semester 강의를 찾아볼 수 있습니다.
---

{% comment %} pop to remove default "posts" collection {% endcomment %}
{% assign sorted_collections = site.collections | sort: 'label' | pop | reverse %}
<ul>
{% for collection in sorted_collections %}
    <li><a href="/{{ collection.label }}/">{{ collection.label }}</a></li>
{% endfor %}
</ul>

각 연도의 강의는 그 자체로 완결된 과정입니다. 가장 최근 자료부터 시작하는 것을 권장합니다. 해마다 다루는 주제가 달라 이전 강의의 노트와 영상도 계속 제공합니다.
