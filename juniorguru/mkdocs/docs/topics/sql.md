---
title: SQL mentoring
template: main_legacy.html
topic_name: sql
topic_link_text: SQL
description: Učíš se MySQL, SQLite, PostgreSQL? Hledáš někoho zkušenějšího, kdo ti poradí, když se zasekneš? Kdo ti ukáže správné postupy a nasměruje tě na kvalitní návody nebo kurzy?
---
{% from 'topic.html' import intro, mentions, members_roll with context %}

{{ intro('Nech si poradit s SQL', page.meta.description) }}

{{ mentions(topic, 'SQL') }}

{{ members_roll(pages, members, members_total_count, club_elapsed_months) }}
