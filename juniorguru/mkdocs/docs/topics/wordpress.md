---
title: WordPress mentoring
topic_name: wordpress
---
{% from 'topic.html' import intro, mentions, members_roll with context %}

{% call intro('Nech si poradit s WordPressem') %}
  Učíš se WordPress? Hledáš někoho zkušenějšího, kdo ti poradí, když se zasekneš? Kdo ti ukáže správné postupy a nasměruje tě na kvalitní návody nebo kurzy?
{% endcall %}

{{ mentions(topic, 'WordPressu') }}

{{ members_roll(members, members_total_count) }}
