---
title: Zkušenosti s Django Girls
topic_name: djangogirls
---
{% from 'topic.html' import intro, mentions, members_roll with context %}

{% call intro('Recenze na Django Girls') %}
  Hledáš někoho, kdo má zkušenosti s Django Girls? Má smysl účastnit se jejich workshopů? Učíš se podle jejich návodů a hledáš někoho zkušenějšího, kdo ti poradí, když se zasekneš?
{% endcall %}

{{ mentions(topic, 'Django Girls') }}

{{ members_roll(members, members_total_count) }}
