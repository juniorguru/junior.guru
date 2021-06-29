---
title: Zkušenosti se Software Development Academy
template: main_legacy.html
topic_name: sdacademy
topic_link_text: SDAcademy
description: Hledáš někoho, kdo má zkušenosti se Software Development Academy? Vyplatí se jejich kurzy?
---
{% from 'topic.html' import intro, mentions, members_roll %}

{{ intro('Recenze na SDAcademy', page.meta.description) }}

{{ mentions(topic, 'SDA') }}

{{ members_roll(members, members_total_count, club_elapsed_months) }}
