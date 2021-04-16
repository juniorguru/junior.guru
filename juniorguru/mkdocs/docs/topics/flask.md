---
title: Flask mentoring
topic_name: flask
---
{% from 'topic.html' import intro, mentions, members_roll with context %}

{% call intro('Nech si poradit s Flaskem') %}
  Učíš se Flask? Hledáš někoho zkušenějšího, kdo ti poradí, když se zasekneš? Kdo ti ukáže správné postupy a nasměruje tě na kvalitní návody nebo kurzy?
{% endcall %}

{{ mentions(topic, 'Flasku') }}

{{ members_roll(members, members_total_count) }}
