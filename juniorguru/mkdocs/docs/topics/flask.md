---
title: Flask mentoring
template: main_legacy.html
topic_name: flask
topic_link_text: Flask
description: Učíš se Flask? Hledáš někoho zkušenějšího, kdo ti poradí, když se zasekneš? Kdo ti ukáže správné postupy a nasměruje tě na kvalitní návody nebo kurzy?
---
{% from 'topic.html' import intro, mentions, members_roll with context %}

{{ intro('Nech si poradit s Flaskem', page.meta.description) }}

{{ mentions(topic, 'Flasku') }}

{{ members_roll(pages, members, members_total_count, club_elapsed_months) }}
