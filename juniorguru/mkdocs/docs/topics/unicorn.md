---
title: Zkušenosti s Unicorn University
template: main_legacy.html
topic_name: unicorn
topic_link_text: Unicorn University
description: Hledáš někoho, kdo má zkušenosti s Unicorn University? Má smysl hlásit se k nim? Jak moc je to pouze o technologiích firmy Unicorn? Jak je to s kurzem Hatchery, po kterém ti mohou nabídnout práci? Jaký typ otázek můžeš čekat na jejich testech?
---
{% from 'topic.html' import intro, mentions, members_roll %}

{{ intro('Recenze na Unicorn University', page.meta.description) }}

{{ mentions(topic, 'Unicornu') }}

{{ members_roll(members, members_total_count, club_elapsed_months) }}
