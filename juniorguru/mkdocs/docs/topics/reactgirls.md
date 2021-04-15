---
title: Zkušenosti s ReactGirls
topic_name: reactgirls
---
{% from 'topic.html' import intro, mentions, members_roll with context %}

{% call intro('Recenze na ReactGirls') %}
  Hledáš někoho, kdo má zkušenosti s ReactGirls? Má smysl účastnit se jejich akademie? Vyplatí se jimi nabízený mentoring?
{% endcall %}

{{ mentions(topic, 'ReactGirls') }}

{{ members_roll(members, members_total_count) }}
