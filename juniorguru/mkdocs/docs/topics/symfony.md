---
title: Symfony mentoring
template: main_legacy.html
topic_name: symfony
topic_link_text: Symfony
description: Učíš se Symfony? Hledáš někoho zkušenějšího, kdo ti poradí, když se zasekneš? Kdo ti ukáže správné postupy a nasměruje tě na kvalitní návody nebo kurzy?
---
{% from 'topic.html' import intro, mentions, members_roll with context %}

{{ intro('Nech si poradit se Symfony', page.meta.description) }}

{{ mentions(topic, 'Symfony') }}

{{ members_roll(pages, members, members_total_count, club_elapsed_months) }}
