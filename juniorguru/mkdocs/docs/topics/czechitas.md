---
title: Zkušenosti s Czechitas
template: main_legacy.html
topic_name: czechitas
topic_link_text: Czechitas
description: Hledáš někoho, kdo má zkušenosti s Czechitas? Má smysl hlásit se na jejich kurzy? Vyplatí se datová akademie?
---
{% from 'topic.html' import intro, mentions, members_roll %}

{{ intro('Recenze na Czechitas', page.meta.description) }}

{{ mentions(topic, 'Czechitas') }}

{{ members_roll(pages, members, members_total_count, club_elapsed_months) }}
