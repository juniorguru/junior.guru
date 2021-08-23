---
title: Zkušenosti s Udemy
template: main_legacy.html
topic_name: udemy
topic_link_text: Udemy
description: Hledáš někoho, kdo má zkušenosti s Udemy? Má smysl hlásit se na jejich kurzy? Vyplatí se certifikace?
---
{% from 'topic.html' import intro, mentions, members_roll %}

{{ intro('Recenze na Udemy', page.meta.description) }}

{{ mentions(topic, 'Udemy') }}

{{ members_roll(pages, members, members_total_count, club_elapsed_months) }}
