---
title: Vše o junior.guru
description: Čísla, statistiky, grafy, kontext. Jak se Honzovi daří provozovat junior.guru?
template: main_about.html
---

{% from 'macros.html' import lead, note with context %}

# Vše o projektu

{% call lead() %}
Projekt junior.guru provozuje jednotlivec jménem Honza Javorek.
Čísla a grafy stejně potřebuje pro svou potřebu, takže proč je v rámci transparentnosti nemít rovnou na webu, že?
{% endcall %}

[TOC]

## Proč existuje junior.guru

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }} Tady něco teprve bude.
{% endcall %}

## Kdo to provozuje

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }} Tady něco teprve bude.
{% endcall %}

## Týdenní poznámky

Od května 2020 Honza píše na svůj osobní blog týdenní poznámky, ve kterých popisuje, jak maká na junior.guru.
Pomáhá mu to s páteční psychikou a zároveň si u toho uspořádá myšlenky.
Tady je posledních pět článků:

{% for blog_article in blog[:5] %}
-   [{{ blog_article.title }}]({{ blog_article.url }}), {{ '{:%-d.%-m.%Y}'.format(blog_article.published_on) }}
{% endfor %}

## Milníky

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }} Tady něco teprve bude.
{% endcall %}
