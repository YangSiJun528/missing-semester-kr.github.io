---
layout: page
title: 이전의 수업
description: >
  Find all past offerings of Missing Semester.
---

{% comment %} pop to remove default "posts" collection {% endcomment %}
{% assign sorted_collections = site.collections | sort: 'label' | pop | reverse %}
<ul>
{% for collection in sorted_collections %}
    <li><a href="/{{ collection.label }}/">{{ collection.label }}</a></li>
{% endfor %}
</ul>

매년 실시하는 강의는 완전히 독립되어 있으며, 가장 최신 버전의 자료를 따르는 것을 추천합니다. 다루는 주제가 약간 차이가 있기 때문에 본 수업의 이전 버전에 대한 노트와 비디오는 계속 제공합니다.
