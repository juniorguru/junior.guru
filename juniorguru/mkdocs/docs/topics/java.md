---
title: Java mentoring
template: main_legacy.html
topic_name: java
topic_link_text: Java
description: Učíš se Javu? Hledáš někoho zkušenějšího, kdo ti poradí, když se zasekneš? Kdo ti ukáže správné postupy a nasměruje tě na kvalitní návody nebo kurzy?
---
{% from 'topic.html' import intro, mentions, members_roll with context %}

{{ intro('Nech si poradit s Javou', page.meta.description) }}

{{ mentions(topic, 'Javě') }}

{{ members_roll(pages, members, members_total_count, club_elapsed_months) }}
