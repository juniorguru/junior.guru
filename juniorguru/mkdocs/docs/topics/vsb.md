---
title: Zkušenosti s rekvalifikačními kurzy na VŠB
topic_name: vsb
---
{% from 'topic.html' import intro, mentions, members_roll with context %}

{% call intro('Recenze na rekvalifikační kurzy VŠB') %}
  Hledáš někoho, kdo má zkušenosti s rekvalifikačními počítačovými kurzy na VŠB-TU? Má smysl se na ně hlásit?
{% endcall %}

{{ mentions(topic, 'VŠB') }}

{{ members_roll(members, members_total_count) }}
