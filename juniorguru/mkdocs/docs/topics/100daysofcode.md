---
title: Diskutuj o \#100daysofcode
topic_name: 100daysofcode
---
{% from 'topic.html' import intro, mentions, members_roll with context %}

{% call intro('Řešit #100daysofcode sám je nuda') %}
  Chystáš se pracovat na #100daysofcode? Hledáš kamarády, se kterými se budeš hecovat a kterým se můžeš pochlubit svým řešením? Chceš jednotlivé výtvory probrat s někým zkušenějším?
{% endcall %}

{{ mentions(topic, '#100daysofcode') }}

{{ members_roll(members, members_total_count) }}
