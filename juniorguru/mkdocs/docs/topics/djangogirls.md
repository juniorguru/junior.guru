---
title: Zkušenosti s Django Girls
topic_name: djangogirls
description: Hledáš někoho, kdo má zkušenosti s Django Girls? Má smysl účastnit se jejich workshopů? Učíš se podle jejich návodů a hledáš někoho zkušenějšího, kdo ti poradí, když se zasekneš?
---
{% from 'topic.html' import intro, mentions, members_roll with context %}

{{ intro('Recenze na Django Girls', description) }}

{{ mentions(topic, 'Django Girls') }}

{{ members_roll(members, members_total_count) }}
