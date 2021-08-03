---
title: Zkušenosti s Green Fox Academy
template: main_legacy.html
topic_name: greenfox
topic_link_text: Green Fox Academy
description: Hledáš někoho, kdo má zkušenosti s Green Fox Academy? Má smysl hlásit se na jejich kurzy? Vyplatí se ti učit se programování na kurzu typu bootcamp? Když neprojdeš jejich přijímacím řízením s kognitivním testem a psycholožkou, znamená to, že se nehodíš do IT? Jak funguje záruka pracovního umístění?
---
{% from 'topic.html' import intro, mentions, members_roll %}

{{ intro('Recenze na Green Fox Academy', page.meta.description) }}

{{ mentions(topic, 'Green Foxu') }}

{{ members_roll(pages, members, members_total_count, club_elapsed_months) }}
