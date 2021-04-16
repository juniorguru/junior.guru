---
title: Django mentoring
topic_name: django
---
{% from 'topic.html' import intro, mentions, members_roll with context %}

{% call intro('Nech si poradit s Djangem') %}
  Učíš se Django? Hledáš někoho zkušenějšího, kdo ti poradí, když se zasekneš? Kdo ti ukáže správné postupy a nasměruje tě na kvalitní návody nebo kurzy?
{% endcall %}

{{ mentions(topic, 'Djangu') }}

{{ members_roll(members, members_total_count) }}
