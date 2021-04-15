---
title: Zkušenosti s ITnetwork
topic_name: itnetwork
---
{% from 'topic.html' import intro, mentions, members_roll with context %}

{% call intro('Recenze na ITnetwork') %}
  Hledáš někoho, kdo má zkušenosti s kurzy na ITnetwork? Vyplatí se koupit si je? Jsou dostatečně kvalitní a aktuální?
{% endcall %}

{{ mentions(topic, 'ITnetwork') }}

{{ members_roll(members, members_total_count) }}
