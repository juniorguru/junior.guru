---
title: OOP mentoring
template: main_legacy.html
topic_name: oop
topic_link_text: OOP
description: Učíš se objektově orientované programování? Hledáš někoho zkušenějšího, kdo ti poradí, když se zasekneš? Kdo ti ukáže správné postupy a nasměruje tě na kvalitní návody nebo kurzy?
---
{% from 'topic.html' import intro, mentions, members_roll %}

{{ intro('Nech si poradit s OOP', page.meta.description) }}

{{ mentions(topic, 'OOP') }}

{{ members_roll(pages, members, members_total_count, club_elapsed_months) }}
