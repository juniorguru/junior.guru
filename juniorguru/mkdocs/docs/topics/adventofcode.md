---
title: Diskutuj o Advent of Code
topic_name: adventofcode
description: Chystáš se řešit Advent of Code? Hledáš kamarády, se kterými se budeš hecovat a kterým se můžeš pochlubit svým řešením? Chceš jednotlivé dny probrat s někým zkušenějším?
---
{% from 'topic.html' import intro, mentions, members_roll with context %}

{% call intro('Řešit Advent of Code sám je nuda') %}
  Chystáš se řešit Advent of Code {{ now.year }}? Hledáš kamarády, se kterými se budeš hecovat a kterým se můžeš pochlubit svým řešením? Chceš jednotlivé dny probrat s někým zkušenějším?
{% endcall %}

{{ mentions(topic, 'Advent of Code') }}

{{ members_roll(members, members_total_count) }}
