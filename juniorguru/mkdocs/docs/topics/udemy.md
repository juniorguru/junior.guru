---
title: Zkušenosti s Udemy
topic_name: udemy
description: Hledáš někoho, kdo má zkušenosti s Udemy? Má smysl hlásit se na jejich kurzy? Vyplatí se certifikace?
---
{% from 'topic.html' import intro, mentions, members_roll with context %}

{{ intro('Recenze na Udemy', description) }}

{{ mentions(topic, 'Udemy') }}

{{ members_roll(members, members_total_count) }}
