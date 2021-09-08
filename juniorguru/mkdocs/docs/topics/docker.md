---
title: Docker mentoring
template: main_legacy.html
topic_name: docker
topic_link_text: Docker
description: Učíš se Docker? Hledáš někoho zkušenějšího, kdo ti poradí, když se zasekneš? Kdo ti ukáže správné postupy a nasměruje tě na kvalitní návody nebo kurzy?
---
{% from 'topic.html' import intro, mentions, members_roll with context %}

{{ intro('Nech si poradit s Dockerem', page.meta.description) }}

{{ mentions(topic, 'Dockeru') }}

{{ members_roll(pages, members, members_total_count, club_elapsed_months) }}
