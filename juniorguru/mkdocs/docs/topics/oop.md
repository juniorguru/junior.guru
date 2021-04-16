---
title: OOP mentoring
topic_name: oop
---
{% from 'topic.html' import intro, mentions, members_roll with context %}

{% call intro('Nech si poradit s OOP') %}
  Učíš se objektově orientované programování? Hledáš někoho zkušenějšího, kdo ti poradí, když se zasekneš? Kdo ti ukáže správné postupy a nasměruje tě na kvalitní návody nebo kurzy?
{% endcall %}

{{ mentions(topic, 'OOP') }}

{{ members_roll(members, members_total_count) }}
