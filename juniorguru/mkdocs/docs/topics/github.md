---
title: GitHub mentoring
template: main_legacy.html
topic_name: github
topic_link_text: GitHub
description: Nevyznáš se na GitHubu? Hledáš někoho zkušenějšího, kdo ti poradí, když se zasekneš? Kdo ti ukáže správné postupy a nasměruje tě na kvalitní návody nebo kurzy?
---
{% from 'topic.html' import intro, mentions, members_roll %}

{{ intro('Nech si poradit s GitHubem', page.meta.description) }}

{{ mentions(topic, 'GitHubu') }}

{{ members_roll(pages, members, members_total_count, club_elapsed_months) }}
