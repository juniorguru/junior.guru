---
title: Zkušenosti se Software Development Academy
topic_name: sdacademy
---
{% from 'topic.html' import intro, mentions, members_roll with context %}

{% call intro('Recenze na SDAcademy') %}
  Hledáš někoho, kdo má zkušenosti se Software Development Academy? Vyplatí se jejich kurzy?
{% endcall %}

{{ mentions(topic, 'SDA') }}

{{ members_roll(members, members_total_count) }}
