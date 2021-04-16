---
title: Zkušenosti s Udemy
topic_name: udemy
---
{% from 'topic.html' import intro, mentions, members_roll with context %}

{% call intro('Recenze na Udemy') %}
  Hledáš někoho, kdo má zkušenosti s Udemy? Má smysl hlásit se na jejich kurzy? Vyplatí se certifikace?
{% endcall %}

{{ mentions(topic, 'Udemy') }}

{{ members_roll(members, members_total_count) }}
