---
title: Zkušenosti s ReactGirls
template: main_legacy.html
topic_name: reactgirls
topic_link_text: ReactGirls
description: Hledáš někoho, kdo má zkušenosti s ReactGirls? Má smysl účastnit se jejich akademie? Vyplatí se jimi nabízený mentoring?
---
{% from 'topic.html' import intro, mentions, members_roll %}

{{ intro('Recenze na ReactGirls', page.meta.description) }}

{{ mentions(topic, 'ReactGirls') }}

{{ members_roll(pages, members, members_total_count, club_elapsed_months) }}
