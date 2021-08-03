---
title: WordPress mentoring
template: main_legacy.html
topic_name: wordpress
topic_link_text: WordPress
description: Učíš se WordPress? Hledáš někoho zkušenějšího, kdo ti poradí, když se zasekneš? Kdo ti ukáže správné postupy a nasměruje tě na kvalitní návody nebo kurzy?
---
{% from 'topic.html' import intro, mentions, members_roll %}

{{ intro('Nech si poradit s WordPressem', page.meta.description) }}

{{ mentions(topic, 'WordPressu') }}

{{ members_roll(pages, members, members_total_count, club_elapsed_months) }}
