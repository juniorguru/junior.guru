---
title: Zkušenosti s Django Girls
template: main_legacy.html
topic_name: djangogirls
topic_link_text: Django Girls
description: Hledáš někoho, kdo má zkušenosti s Django Girls? Má smysl účastnit se jejich workshopů? Učíš se podle jejich návodů a hledáš někoho zkušenějšího, kdo ti poradí, když se zasekneš?
---
{% from 'topic.html' import intro, mentions, members_roll %}

{{ intro('Recenze na Django Girls', page.meta.description) }}

{{ mentions(topic, 'Django Girls') }}

{{ members_roll(pages, members, members_total_count, club_elapsed_months) }}
