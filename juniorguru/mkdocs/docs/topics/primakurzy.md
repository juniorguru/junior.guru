---
title: Zkušenosti s PrimaKurzy
topic_name: primakurzy
---
{% from 'topic.html' import intro, mentions, members_roll with context %}

{% call intro('Recenze na PrimaKurzy') %}
  Hledáš někoho, kdo má zkušenosti s PrimaKurzy? Vyplatí se jít na jejich akreditované IT kurzy?
{% endcall %}

{{ mentions(topic, 'PrimaKurzy') }}

{{ members_roll(members, members_total_count) }}
