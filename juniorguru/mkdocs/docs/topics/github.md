---
title: GitHub mentoring
topic_name: github
---
{% from 'topic.html' import intro, mentions, members_roll with context %}

{% call intro('Nech si poradit s GitHubem') %}
  Nevyznáš se na GitHubu? Hledáš někoho zkušenějšího, kdo ti poradí, když se zasekneš? Kdo ti ukáže správné postupy a nasměruje tě na kvalitní návody nebo kurzy?
{% endcall %}

{{ mentions(topic, 'GitHubu') }}

{{ members_roll(members, members_total_count) }}
