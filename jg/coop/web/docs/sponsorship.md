---
title: Sponzoruj junior.guru
description: Líbí se ti tento web? Pošli LOVE! Podpoř finančně junior.guru, jako jednotlivec, nebo jako firma.
template: main_sponsorship.html
---

{% from 'macros.html' import lead, img, logo with context %}

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
  <small class="ms-3">jako už {{ sponsors_github|length }}+ sponzorů</small>
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

### Tarif „Sponzorujeme“

- Logo na [úvodní stránce](index.jinja)
- Skupinové členství v [klubu](club.md) pro 15 lidí
- Láskyplné uvítání sponzora příspěvkem v klubu
- Platba kartou nebo na fakturu

<p>
  <a class="btn btn-success" href="{{ pages|docs_url('sponsorship.md')|url }}" target="_blank" rel="noopener">
    {{ 'heart-fill'|icon }}
    15.000 Kč/rok
  </a>
  <small class="ms-3">jako už X sponzorů</small>
</p>

### Tarif „Poskytujeme kurzy“

- Všechno co předchozí tarif
- Zvýrazněný zápis v [katalogu kurzů](courses.md) s logem a odkazem, který nemá _nofollow_ (zlepší vaše SEO)
- Možnost poslat do klubu studenty za 100 Kč/měs/os
- Platba kartou nebo na fakturu

<p>
  <a class="btn btn-secondary" href="{{ pages|docs_url('sponsorship.md')|url }}" target="_blank" rel="noopener">
    {{ 'star-fill'|icon }}
    40.000 Kč/rok
  </a>
  <small class="ms-3">jako už X sponzorů</small>
</p>

### Tarif „Budujeme brand“

- Všechno co předchozí tarify
- Logo i na [příručce](handbook/index.md)
- Omezené množství, maximálně 4 firmy
- Platba kartou nebo na fakturu

<p>
  <a class="btn btn-danger" href="{{ pages|docs_url('sponsorship.md')|url }}" target="_blank" rel="noopener">
    {{ 'shield-fill'|icon }}
    80.000 Kč/rok
  </a>
  <small class="ms-3">jako už X sponzorů</small>
</p>

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
