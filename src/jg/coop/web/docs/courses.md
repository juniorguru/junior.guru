---
title: Katalog kurzů programování a testování
---

{% from 'macros.html' import link_card, note, lead with context %}


# Kurzy programování a testování

{% call lead() %}
  Seznam všech míst, kde se můžeš učit programovat nebo testovat.
  Umístění na seznam neznamená, že jde o kurzy dobré, ověřené, nebo že je junior.guru doporučuje.
{% endcall %}

{% call note(standout=true) %}
  {{ 'plus-circle'|icon }} Pokud víš o kurzech, které tady chybí, piš na {{ 'honza@junior.guru'|email_link }}
{% endcall %}

[TOC]

{% for group, course_providers in course_providers_by_group %}
  {% if group == "highlighted" %}

## Sponzoři
Vybrali si [tarif z ceníku](love.jinja) a poslali finanční prostředky na provoz junior.guru. Neznamená to, že jsou nejlepší, ale budiž jim ke cti, že podporují tento projekt.

  {% elif group == "partners" %}

## Partneři
Komunity a malé subjekty, s nimiž má junior.guru domluvenou nějakou oboustrannou nefinanční výpomoc. Není v možnostech junior.guru ověřovat kvalitu, ale takováto spolupráce se asi dá brát jako známka toho, že jde o něco důvěryhodného. Na každé podstránce je detailní popis spolupráce.

  {% elif group == "graveyard" %}

## Hřbitov
Subjekty, které v minulosti kurzy poskytovaly, ale dnes už neposkytují. V katalogu jsou jen pro úplnost, kdyby je někdo ještě hledal.

  {% else %}

## Ostatní
Abecední seznam ostatních poskytovatelů kurzů.

  {% endif %}

  <div class="link-cards">
    {% for course_provider in course_providers %}
      {% if course_provider.group == "highlighted" %}
        {{ link_card(
          course_provider.name,
          pages|docs_url(course_provider.page_url)|url,
          screenshot_source_url=course_provider.url,
          class='highlighted',
        ) }}
      {% else %}
        {{ link_card(
          course_provider.name,
          pages|docs_url(course_provider.page_url)|url,
          screenshot_source_url=course_provider.url,
        ) }}
      {% endif %}
    {% endfor %}
  </div>
{% endfor %}
