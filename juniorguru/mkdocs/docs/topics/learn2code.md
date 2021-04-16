---
title: Zkušenosti s Learn2Code
topic_name: learn2code
---
{% from 'topic.html' import intro, mentions, members_roll with context %}

{% call intro('Recenze na Learn2Code') %}
  Hledáš někoho, kdo má zkušenosti s Learn2Code? Má smysl hlásit se na jejich kurzy? Je Webrebel, kde učí yablko, opravdu tak dobrý, jak se říká? Vyplatí se roční předplatné?
{% endcall %}

{{ mentions(topic, 'Learn2Code') }}

{{ members_roll(members, members_total_count) }}
