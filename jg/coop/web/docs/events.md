---
title: Online akce pro začátečníky v programování
description: Online akce pro členy klubu junior.guru. Seznam akcí proběhlých i budoucích. Přednášky, streamy, Q&A, AMA, webináře, a další.
template: main_subnav.html
---

{% from 'macros.html' import lead, link_card, markdown, img with context %}

# Klubové akce

{% call lead() %}
Online přednášky a další akce pořádané junior.guru klubem.
Zveme si profíky na témata kolem programování nebo shánění první práce v oboru.
Pojetí akcí je vždy vyloženě pro začátečníky.
Žádná záplava odborných „termitů“, které ti nikdo nevysvětlil!
{% endcall %}

<div class="standout">
  <a class="brand-button youtube" target="_blank" rel="noopener" href="https://www.youtube.com/channel/UCp-dlEJLFPaNExzYX079gCA">{{ 'youtube'|icon }} YouTube</a>
  <a class="brand-button email" href="{{ pages|docs_url('news.jinja')|url }}">{{ 'envelope-paper-fill'|icon }} Newsletter</a>

  {#
  <a class="brand-button icalendar" target="_blank" rel="noopener" href="https://junior.guru/api/events.ics">{{ 'calendar-event'|icon }} iCalendar</a>
  <a class="brand-button rss" target="_blank" rel="noopener" href="https://junior.guru/api/events.xml">{{ 'rss-fill'|icon }} RSS</a>
  #}
</div>

{#
<h2 class="visually-hidden">Autoři</h2>
<div class="podcast-author">
  {{ img('static/avatars-participants/honza-javorek.jpg', 'Honza Javorek', 100, 100, lazy=False, class='podcast-author-photo') }}
  <div class="podcast-author-body">
    <h3>Honza Javorek</h3>
    {% call markdown() -%}
      Autor projektu junior.guru. Shání hosty, stará se o propagaci, moderuje akce.
    {%- endcall %}
  </div>
</div>
<div class="podcast-author">
  {{ img('static/avatars-participants/pavlina-fronkova.jpg', 'Táňa Váchová', 100, 100, lazy=False, class='podcast-author-photo') }}
  <div class="podcast-author-body">
    <h3>Táňa Váchová</h3>
    {% call markdown() -%}
      Stará se o domlouvání termínů a veškerou administrativu kolem přípravy přednášek.
    {%- endcall %}
  </div>
</div>
<div class="podcast-author">
  {{ img('static/avatars-participants/pavlina-fronkova.jpg', 'Patrik Brnušák', 100, 100, lazy=False, class='podcast-author-photo') }}
  <div class="podcast-author-body">
    <h3>Patrik Brnušák</h3>
    {% call markdown() -%}
      Stará se o nahrávání záznamů.
    {%- endcall %}
  </div>
</div>
#}

{% if events_planned|length %}
## Plánované akce

<div class="link-cards">
  {% for event in events_planned %}
    {{ link_card(
      event.title,
      pages|docs_url(event.page_url)|url,
      caption=event.bio_name,
      thumbnail_url=("static/" + event.avatar_path)|url,
      badge_icon='bell-fill',
      badge_text='{:%-d.%-m.}'.format(event.start_at),
    ) }}
  {% endfor %}
</div>
{% endif %}

## Proběhlé akce

<div class="link-cards">
{% for event in events_archive %}
  {{ link_card(
    event.title,
    pages|docs_url(event.page_url)|url,
    caption=event.bio_name,
    thumbnail_url=("static/" + event.avatar_path)|url,
    badge_icon='unlock-fill' if event.public_recording_url else none,
    badge_text='Veřejný záznam' if event.public_recording_url else none,
  ) }}
{% endfor %}
</div>
