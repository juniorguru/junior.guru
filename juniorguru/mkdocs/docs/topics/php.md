---
title: PHP mentoring
template: main_legacy.html
topic_name: php
topic_link_text: PHP
description: Učíš se PHP? Hledáš někoho zkušenějšího, kdo ti poradí, když se zasekneš? Kdo ti ukáže správné postupy a nasměruje tě na kvalitní návody nebo kurzy?
---
{% from 'macros_topic.html' import intro, mentions, members_roll with context %}

{{ intro('Nech si poradit s PHP', page.meta.description) }}

{{ mentions(topic, 'PHP') }}

{{ members_roll(pages, members, members_total_count, club_elapsed_months) }}
