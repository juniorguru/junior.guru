---
title: Zkušenosti s ENGETO Academy
template: main_legacy.html
topic_name: engeto
topic_link_text: ENGETO Academy
description: Hledáš někoho, kdo má zkušenosti s ENGETO Academy? Má smysl hlásit se na jejich kurzy? Vyplatí se ENGETO Pro?
---
{% from 'macros_topic.html' import intro, mentions, members_roll with context %}

{{ intro('Recenze na ENGETO Academy', page.meta.description) }}

{{ mentions(topic, 'Engetu') }}

{{ members_roll(pages, members, members_total_count, club_elapsed_months) }}
