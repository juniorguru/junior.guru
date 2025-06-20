---
title: Sponzoři a partneři junior.guru
template: main_about.html
---

{% from 'macros.html' import img, lead, utm_link with context %}

# Sponzoři a partneři

{% call lead() %}
Část příjmů junior.guru plyne ze sponzorství. Podpořit junior.guru mohou jak firmy, tak jednotlivci. Partneři jsou subjekty, se kterými je nějaká nepeněžní dohoda.
{% endcall %}

[TOC]

## Proč má junior.guru sponzory

Protože **peníze od juniorů nestačí na provoz**, viz [finanční výsledky](./finances.md).
Díky sponzorům může být členství v klubu pro juniory levnější.

Také je žádoucí, aby junior.guru **stálo na pomezí firem a juniorů a vyvažovalo diskuzi na obě strany**, ne aby mazalo med kolem pusy jedné z nich a stavělo ji proti druhé.
Rozložení příjmů junior.guru mezi juniory i firmy je způsob, jak to zajistit.

Honza se ale nakonec vždy **snaží mít na prvním místě dobro samotných juniorů**.
Ačkoliv dělá obchody s firmami, zachovává si nezávislost a nenechává se ovlivnit ve prospěch konkrétního produktu.

<p class="text-center">
  <a href="{{ pages|docs_url("love.jinja")|url }}" class="love-button pulse">{{ 'heart-fill'|icon }} Pošli LOVE</a>
</p>

{% for tier, sponsors in sponsors_by_tier %}
## Tarif „{{ tier.name }}“

Sponzoři, kteří zaplatili za tarif číslo {{ tier.priority + 1 }} (vyšší je lepší) z přehledu na [Pošli LOVE](../love.jinja).

<div class="table-responsive"><table class="table align-middle">
  {% for sponsor in sponsors %}
    <tr>
      <td>
        {{ utm_link(sponsor.name, sponsor.url, 'about', sponsor.utm_campaign) }}
        {% if sponsor.note %}
        <br><small>{{ sponsor.note|md }}</small>
        {% endif %}
      </td>
      <td style="width: 5rem">
        {{ sponsor.members_count }}<br>
        <small>{{ sponsor.members_count|nplurals("člen", "členové", "členů") }}</small>
      </td>
      <td style="width: 5rem">
        <span {% if sponsor.days_until_renew() < 30 %}
        class="problem-very-soon"
      {% elif sponsor.days_until_renew() < 60 %}
        class="problem-soon"
      {%- endif %}>
          {{ sponsor.days_until_renew() }} dní<br>
          <small>zbývá</small>
        </span>
      </td>
      <td style="width: 200px" class="table-logo">
        {{ img('static/' + sponsor.logo_path, sponsor.name, 130, 60) }}
      </td>
    </tr>
  {% endfor %}
</table></div>
{% endfor %}

## GitHub Sponsors

Sponzoři, kteří využívají [GitHub Sponsors](https://github.com/sponsors/honzajavorek/). Převážně jednotlivci, ale i firmy.

<div class="table-responsive"><table class="table">
  {% for sponsor in sponsors_github %}
    <tr>
      <td>
        <a href="{{ sponsor.url }}" target="_blank" rel="noopener">@{{ sponsor.slug }}</a>
        {% if sponsor.name %}<br><small>{{ sponsor.name }}</small>{% endif %}
      </td>
      <td style="width: 200px" class="table-image">
        {{ img('static/' + sponsor.avatar_path, sponsor.name, 50, 50) }}
      </td>
    </tr>
  {% endfor %}
</table></div>

## Bývalí sponzoři

{% for sponsor in sponsors_past -%}
  {% if sponsor.url %}
    {{- utm_link(sponsor.name, sponsor.url, "about", sponsor.utm_campaign) -}}
  {% else %}
    †{{- sponsor.name -}}
  {% endif %}
  {%- if not loop.last %}, {% endif -%}
{%- endfor %}.

**GitHub Sponsors:** {% for sponsor in sponsors_github_past %}[@{{ sponsor.slug }}]({{ sponsor.url }}){% if not loop.last %}, {% endif %}{% endfor %}.

**Patreon:** Tomáš Ehrlich, Tomáš Jeřábek, Vojta Tranta, Petr Viktorin.

A další neveřejně, někteří přes GitHub Sponsors, někteří přímo na účet.

## Sponzoři a klub

Sponzoři mají přístup do klubu. Mohou vyhlížet talentované juniory, promovat ve vyhrazených kanálech své aktivity, poskytovat slevy na své produkty. Mohou se zapojit do diskuzí a radit, nebo poskytovat pohled z druhé strany. Mohou spolu s klubem vymýšlet různé způsoby vzájemné podpory, ať už jde o propagaci, slevy, nebo tvorbu společných článků, podcastů, videí.

Je na firmě, jak to uchopí, a co z toho „vyždíme“. Už jen tím, že svými financemi podpoří existenci junior.guru a bude vidět její logo, si **buduje dobré jméno** jak mezi lidmi z nastupující generace vývojářů, tak mezi zainteresovanými profíky.

## Poskytovatelé kurzů jako sponzoři

Sponzory mohou být i poskytovatelé kurzů, což **staví junior.guru do konfliktu zájmů**.
Na této stránce je proto transparentně zdokumentována každá dohoda, aby nebylo pochyb, že junior.guru je nestranné.

Firmy i přes své sponzorství respektují, že junior.guru a klub jsou místa, kde se o nabídce kurzů **diskutuje na neutrální půdě, lidé si sdílí zkušenosti a porovnávají**.
Recenze členů v klubu jsou subjektivním hodnocením konkrétních lidí a firmy nemají možnost do něj zasahovat.
Pokud chce poskytovatel kurzů propagovat své produkty, může tak činit ve vyhrazených místech v klubu.

Honza si dává pozor na to, aby **žádný konkrétní kurz sám neprotežoval** a aby aktivity v rámci sponzorství nezasahovaly do nestrannosti junior.guru.

## Partneři

Aktuálně junior.guru spolupracuje s **{{ partners|length }} partnery**. Partneři jsou komunity a malé subjekty, s nimiž má junior.guru domluvenou nějakou oboustrannou nefinanční výpomoc.

<div class="table-responsive"><table class="table align-middle">
  {% for partner in partners %}
    <tr>
      <td>
        {{ utm_link(partner.name, partner.url, 'about', partner.utm_campaign) }}
        <br><small>{{ partner.note|md }}</small>
      </td>
      <td style="width: 5rem">
        {{ partner.members_count }}<br>
        <small>{{ partner.members_count|nplurals("člen", "členové", "členů") }}</small>
      </td>
      <td style="width: 200px" class="table-logo">
        {{ img('static/' + partner.logo_path, partner.name, 130, 60) }}
      </td>
    </tr>
  {% endfor %}
</table></div>

## Partnerství s komunitami

Organizátoři komunit, které jsou partnery junior.guru, mají přístup do klubu. Mohou v něm promovat svoje aktivity. Mohou spolu s klubem vymýšlet různé způsoby vzájemné podpory, ať už jde o propagaci, slevy, nebo tvorbu společných článků, podcastů, videí.

Je na lidech z partnerské komunity, jak to uchopí, a co z toho „vyždímou“. Spolupráce by ale neměla být samoúčelná, měla by vždy vyústit **něco, co bude především sloužit samotným juniorům**.
