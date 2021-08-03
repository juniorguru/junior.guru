---
title: CSS mentoring
template: main_legacy.html
topic_name: css
topic_link_text: CSS
description: Učíš se CSS? Hledáš někoho zkušenějšího, kdo ti poradí, když se zasekneš? Kdo ti ukáže správné postupy a nasměruje tě na kvalitní návody nebo kurzy?
---
{% from 'topic.html' import intro, mentions, members_roll %}

{{ intro('Nech si poradit s CSS', page.meta.description) }}

{{ mentions(topic, 'CSS') }}

{{ members_roll(pages, members, members_total_count, club_elapsed_months) }}
