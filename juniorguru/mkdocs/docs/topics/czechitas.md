---
title: Zkušenosti s Czechitas
topic_name: czechitas
---
{% from 'topic.html' import intro, mentions, members_roll with context %}

{% call intro('Recenze na Czechitas') %}
  Hledáš někoho, kdo má zkušenosti s Czechitas? Má smysl hlásit se na jejich kurzy? Vyplatí se datová akademie?
{% endcall %}

{{ mentions(topic, 'Czechitas') }}

{{ members_roll(members, members_total_count) }}
