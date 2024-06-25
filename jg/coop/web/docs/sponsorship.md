---
title: Sponzoruj junior.guru
description: Líbí se ti tento web? Pošli LOVE! Podpoř finančně junior.guru, jako jednotlivec, nebo jako firma.
template: main_sponsorship.html
---

{% from 'macros.html' import lead, note with context %}

# Pošli LOVE

{% call lead() %}
  Líbí se ti tento web? Ukázal ti cestu k pro­gra­mo­vá­ní? K lepší práci? Pomohl vaší firmě najmout super lidi? Chcete jako firma podpořit juniory v jejich snažení? Aby mohlo junior.guru dál existovat a pomáhat co nejvíce lidem, potřebuje peníze na provoz.
{% endcall %}

### GitHub Sponsors

- Pokud zaškrtneš, že podporuješ veřejně, objeví se tvůj avatar na [úvodní stránce](index.jinja)
- Platba kartou

<p>
  <a class="btn btn-dark" href="https://github.com/sponsors/honzajavorek/" target="_blank" rel="noopener">
    {{ 'github'|icon }}
    od {{ github_sponsors_czk }} Kč/měs
  </a>
  {% set sponsors_count = sponsors_github|length %}
  {% if sponsors_count %}
  <small class="ms-3">
    jako už {{ sponsors_count }}+ sponzo
    {%- if sponsors_count == 1 -%}
      r
    {%- elif sponsors_count <= 4 -%}
      ři
    {%- else -%}
      rů
    {%- endif -%}
  </small>
  {% endif %}
</p>

### Členství v klubu

- Normální členství v [klubu](club.md) pro 1 člověka
- Můžeš do klubu házet promo, pozvánky, pracovní inzeráty
- 2 týdny zdarma na zkoušku, potom platba kartou

<p>
  <a class="btn btn-primary" href="https://juniorguru.memberful.com/checkout?plan=89511" target="_blank" rel="noopener">
    {{ 'person-circle'|icon }}
    199 Kč/měs
  </a>
  <small class="ms-3">jako už {{ members_total_count }} členů</small>
</p>

{% for tier in sponsor_tiers %}
### Tarif „{{ tier.name }}“ {: #{{ tier.anchor }} }

{% if tier.slug == "supporting" %}
{% set btn = "success" %}
{% set icon = "heart-fill" %}

- Logo na [úvodní stránce](index.jinja)
- Skupinové členství v [klubu](club.md) pro 15 lidí
- Láskyplné uvítání sponzora příspěvkem v klubu
- Platba kartou nebo na fakturu

{% elif tier.slug == "providing_courses" %}
{% set btn = "secondary" %}
{% set icon = "star-fill" %}

- Všechno co předchozí tarif
- Zvýrazněný zápis v [katalogu kurzů](courses.md) s logem a odkazem, který nemá _nofollow_ (zlepší vaše SEO)
- Možnost poslat do klubu studenty za {{ tier.member_price }} Kč/měs/os
- Platba kartou nebo na fakturu

{% elif tier.slug == "building_brand" %}
{% set btn = "danger" %}
{% set icon = "shield-fill" %}

- Všechno co předchozí tarify
- Logo i na [příručce](handbook/index.md)
- Omezené množství, maximálně 4 firmy
- Platba kartou nebo na fakturu

{% else %}
{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }} Tady něco má být, ale není to tu. Napiš prosím na {{ 'honza@junior.guru'|email_link }}
{% endcall %}
{% endif %}

<p>
  <a class="btn btn-{{ btn }}" href="{{ tier.plan_url }}" target="_blank" rel="noopener">
    {{ icon|icon }}
    {{ tier.price|thousands }} Kč/rok
  </a>
  {% set sponsors_count = tier.list_sponsors|length %}
  {% if sponsors_count %}
  <small class="ms-3">
    jako už {{ sponsors_count }} sponzo
    {%- if sponsors_count == 1 -%}
      r
    {%- elif sponsors_count <= 4 -%}
      ři
    {%- else -%}
      rů
    {%- endif -%}
  </small>
  {% endif %}
</p>
{% endfor %}

## Na co přispíváš

<!--
https://web.archive.org/web/20220127081903/https://junior.guru/donate/
https://docs.google.com/document/d/1CIKQKQ9eTpS8LmdxGqppOSim4gYOpoRcekqmPpnyLEI/edit
-->

## Komu přispíváš

<!--
nejsem neziskovka, ale myslím to upřímně
Projekt junior.guru provozuje Honza Javorek. Příspěvky nelze odečíst z daní jako dar.
-->

## Kdo přispívá, nebo dřív přispíval

Spousta jednotlivců i firem! Současné i bývalé sponzory najdeš na [stránce, kde je transparentně i vše ostatní](open.md) o tomto projektu.

## Jak přidat pracovní inzerát

<!--
inzerce práce - zdarma - založte si účet v klubu a dejte to ručně do fóra, nebo inzerujte na nějakém portálu a náš robot si to automaticky stáhne
-->

## Jak se pozvat

<!--
 do podcastu nebo na přednášku
- návštěva podcastu - nelze koupit, zveme si
- přednášení v klubu - nelze koupit, zveme si
-->


<!--
TODO přidat social proof (kolik je na jakém tarifu)
TODO přidat ty samotné tarify v Memberful a prolinkovat
TODO přidat lenertovou do sponzorů
-->
