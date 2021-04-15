---
title: Zkušenosti s Engeto
topic_name: engeto
---
{% from 'topic.html' import intro, mentions, members_roll with context %}

{% call intro('Recenze na Engeto') %}
  Hledáš někoho, kdo má zkušenosti s Engeto Academy? Má smysl hlásit se na jejich kurzy? Vyplatí se Engeto Pro?
{% endcall %}

{{ mentions(topic, 'Engetu') }}

{{ members_roll(members, members_total_count) }}
