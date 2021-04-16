---
title: Laravel mentoring
topic_name: laravel
---
{% from 'topic.html' import intro, mentions, members_roll with context %}

{% call intro('Nech si poradit s Laravelem') %}
  Učíš se Laravel? Hledáš někoho zkušenějšího, kdo ti poradí, když se zasekneš? Kdo ti ukáže správné postupy a nasměruje tě na kvalitní návody nebo kurzy?
{% endcall %}

{{ mentions(topic, 'Laravelu') }}

{{ members_roll(members, members_total_count) }}
