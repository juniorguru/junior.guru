---
title: Zkušenosti s IT STEP
template: main_legacy.html
topic_name: step
topic_link_text: STEP
description: Hledáš někoho, kdo má zkušenosti s počítačovou akademií STEP? Vyplatí se jejich kurzy?
---
{% from 'topic.html' import intro, mentions, members_roll %}

{{ intro('Recenze na STEP', description) }}

{{ mentions(topic, 'STEP') }}

{{ members_roll(members, members_total_count, club_elapsed_months) }}
