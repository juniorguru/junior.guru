---
title: Open source mentoring
template: main_legacy.html
topic_name: opensource
topic_link_text: open source
description: Nevyznáš se v open source? Hledáš někoho zkušenějšího, kdo ti poradí a pomůže se zorientovat? Jak někam přispět, kde najít projekt, jak používat GitHub? Kdo ti ukáže správné postupy a nasměruje tě na kvalitní návody nebo kurzy?
---
{% from 'topic.html' import intro, mentions, members_roll %}

{{ intro('Nech si poradit s open source', description) }}

{{ mentions(topic, 'open source') }}

{{ members_roll(members, members_total_count, club_elapsed_months) }}
