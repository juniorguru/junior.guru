---
title: Git mentoring
template: main_legacy.html
topic_name: git
topic_link_text: Git
description: Učíš se Git? Hledáš někoho zkušenějšího, kdo ti poradí, když se zasekneš? Kdo ti ukáže správné postupy a nasměruje tě na kvalitní návody nebo kurzy?
---
{% from 'topic.html' import intro, mentions, members_roll with context %}

{{ intro('Nech si poradit s Gitem', page.meta.description) }}

{{ mentions(topic, 'Gitu') }}

{{ members_roll(pages, members, members_total_count, club_elapsed_months) }}
