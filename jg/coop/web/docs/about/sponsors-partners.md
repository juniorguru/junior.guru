---
title: Sponzoři a partneři junior.guru
template: main_about.html
---

{% from 'macros.html' import lead, note, utm_link, img with context %}

# Sponzoři a partneři

{% call lead() %}
Část příjmů junior.guru plyne ze sponzorství. Pokud chceš junior.guru podpořit, ať už jako firma, nebo jako jednotlivec, mrkni na [Pošli LOVE](../love.jinja). Partneři jsou subjekty, se kterými je nějaká nepeněžní dohoda.
{% endcall %}

[TOC]

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
      <td style="width: 200px">
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
      <td style="width: 200px">
        {{ img('static/' + sponsor.avatar_path, sponsor.name, 50, 50) }}
      </td>
    </tr>
  {% endfor %}
</table></div>

## Bývalí sponzoři

{% for sponsor in sponsors_past %}{{ utm_link(sponsor.name, sponsor.url, "about", sponsor.utm_campaign) }}{% if not loop.last %}, {% endif %}{% endfor %}.

**GitHub Sponsors:** {% for sponsor in sponsors_github_past %}[@{{ sponsor.slug }}]({{ sponsor.url }}){% if not loop.last %}, {% endif %}{% endfor %}.

**Patreon:** Tomáš Ehrlich, Tomáš Jeřábek, Vojta Tranta, Petr Viktorin.

A další neveřejně, někteří přes GitHub Sponsors, někteří přímo na účet.

## Partneři

Aktuálně junior.guru spolupracuje s **{{ partners|length }} partnery**.

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
      <td style="width: 200px">
        {{ img('static/' + partner.logo_path, partner.name, 130, 60) }}
      </td>
    </tr>
  {% endfor %}
</table></div>
