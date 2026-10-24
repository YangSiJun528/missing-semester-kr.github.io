---
layout: page
title: 이전 강의
description: >
  Missing Semester의 지난 강의를 모두 찾아볼 수 있습니다.
---

{% comment %} pop to remove default "posts" collection {% endcomment %}
{% assign sorted_collections = site.collections | sort: 'label' | pop | reverse %}
<ul>
{% for collection in sorted_collections %}
    <li><a href="/{{ collection.label }}/">{{ collection.label }}</a></li>
{% endfor %}
</ul>

각 연도의 강의는 서로 독립적으로 수강할 수 있습니다. 가장 최신 자료로 시작하는 것을 권합니다. 해마다 다루는 주제가 조금씩 다르므로 이전 강의의 노트와 영상도 계속 제공합니다.
