---
title: O klubu na junior.guru
template: main_about.html
---

{% from 'macros.html' import lead, note with context %}

# Vše o klubu

{% call lead() %}
Informace o [klubu pro juniory](../club.md). Záměr a hodnoty, se kterými je provozován. K tomu ještě pár zajímavých statistik.
{% endcall %}

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }} Tady něco teprve bude.
{% endcall %}
