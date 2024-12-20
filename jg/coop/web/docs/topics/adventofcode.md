---
title: Diskutuj o Advent of Code
template: main_legacy.html
topic_name: adventofcode
topic_link_text: Advent of Code
description: Chystáš se řešit Advent of Code? Hledáš kamarády, se kterými se budeš hecovat a kterým se můžeš pochlubit svým řešením? Chceš jednotlivé dny probrat s někým zkušenějším?
thumbnail_button_link: junior.guru/club
thumbnail_button_icon: chat-heart
---
{% from 'macros_topic.html' import intro, mentions with context %}

{% call intro('Řešit Advent of Code sám je nuda') %}
  Chystáš se řešit Advent of Code {{ now.year }}? Hledáš kamarády, se kterými se budeš hecovat a kterým se můžeš pochlubit svým řešením? Chceš jednotlivé dny probrat s někým zkušenějším?
{% endcall %}

{{ mentions(topic, 'Advent of Code') }}

<p class="button-compartment">
  <a href="{{ pages|docs_url('club.md')|url }}" class="button">
    Přidej se&nbsp;k&nbsp;nám
  </a>
</p>
