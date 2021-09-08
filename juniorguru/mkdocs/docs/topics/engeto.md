---
title: Zkušenosti s Engeto
template: main_legacy.html
topic_name: engeto
topic_link_text: Engeto
description: Hledáš někoho, kdo má zkušenosti s Engeto Academy? Má smysl hlásit se na jejich kurzy? Vyplatí se Engeto Pro?
---
{% from 'topic.html' import intro, mentions, members_roll with context %}

{{ intro('Recenze na Engeto', page.meta.description) }}

{{ mentions(topic, 'Engetu') }}

{{ members_roll(pages, members, members_total_count, club_elapsed_months) }}
