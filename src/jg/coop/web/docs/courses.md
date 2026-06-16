---
title: Katalog poskytovatelů kurzů programování a testování
---

{% from 'macros.html' import link_card, note, lead with context %}


# Kurzy programování a testování

{% call lead() %}
  Nevybírej si kurzy programování nebo testování podle reklam, ale podle serióznosti provozovatelů a podle recenzí lidí, kteří je absolvovali.
{% endcall %}

{% call note(standout=true) %}
  {{ 'plus-circle'|icon }} Pokud víš o kurzech, které tady chybí, piš na {{ 'honza@junior.guru'|email_link }}
{% endcall %}

[TOC]

{% for group, course_providers in course_providers_by_group %}
  {% if group == "highlighted" %}

## Sponzoři
Vybrali si [tarif z ceníku](love.jinja) a poslali finanční prostředky na provoz junior.guru. Neznamená to, že jsou nejlepší, ale budiž jim ke cti, že podporují tento projekt.
{% set card_class = 'highlighted' %}

  {% elif group == "partners" %}

## Partneři
Komunity a malé subjekty, s nimiž má junior.guru domluvenou nějakou oboustrannou nefinanční výpomoc. Není v možnostech junior.guru ověřovat kvalitu, ale takováto spolupráce se asi dá brát jako známka toho, že jde o něco důvěryhodného. Na každé podstránce je detailní popis spolupráce.
{% set card_class = '' %}

  {% elif group == "graveyard" %}

## Hřbitov
Subjekty, které v minulosti kurzy poskytovaly, ale dnes už neposkytují. V katalogu jsou jen pro úplnost, kdyby je někdo ještě hledal.
{% set card_class = 'grayscale' %}

  {% else %}

## Ostatní
Abecední seznam ostatních poskytovatelů kurzů.
{% set card_class = '' %}

  {% endif %}

<div class="link-cards">
  {% for course_provider in course_providers %}
    {{ link_card(
      course_provider.name,
      pages|docs_url(course_provider.page_url)|url,
      screenshot_source_url=course_provider.url,
      class=card_class,
    ) }}
  {% endfor %}
</div>

{% endfor %}
