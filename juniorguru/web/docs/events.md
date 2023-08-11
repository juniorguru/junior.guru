---
title: Online akce pro začátečníky v programování
template: main_news.html
description: Online akce pro členy klubu junior.guru. Seznam akcí proběhlých i budoucích. Přednášky, Q&A, AMA, webináře, a další.
---

{% from 'macros.html' import lead, markdown, img, partner_link with context %}


# Klubové akce

{% call lead() %}
Přednášky a další akce pro členy klubu junior.guru. Seznam akcí proběhlých i budoucích.
{% endcall %}

## Jak to funguje?

Večerní tematické přednášky jsou vždy předem oznámeny na konkrétní datum a čas. Pokud chceš přednášku slyšet, připoj se v ten čas do hlasové místnosti #přednášky. Po skončení přednášky není žádný další oficiální program. Cílem je, aby přednášky byly spíše rychlé a časté, než plánované do celovečerních bloků. Tak nezaberou příliš mnoho času a můžeš se připojit, i když máš nabitý den, nebo prostě jen nechceš trávit celý večer na nějakém srazu.

Nepořizujeme profesionální záznam, ale snažíme se alespoň nahrát obrazovku, aby si přednášku mohli pustit i členové, kteří v čas přednášky nemají čas. Nedáváme žádnou záruku na existenci záznamu ani jeho kvalitu. Pokud existuje, je členům k dispozici skrze tajný odkaz na YouTube. Odkaz na video veřejně prosím nesdílej, ale kamarádům jej klidně pošli – asi stejně jako když pro známé odemykáš placený článek v novinách.

## Plánované

{% if events_planned|length %}
  <h3>{{ event.title }}<a class="headerlink" href="#{{ event.slug }}" title="Odkaz na tuto akci">#</a></h3>
  {% if event.partner %}
  <p>
    <span class="badge text-bg-primary">Spolupráce</span>
    <small>
    Akce vzniká v rámci
    {% set active_partnership = event.partner.active_partnership() %}
    {% if active_partnership %}
      <a href="{{ pages|docs_url(active_partnership.page_url)|url }}">placeného partnerství</a>
    {% else %}
      placeného partnerství
    {% endif %}
    s firmou {{ partner_link(event.partner.name, event.partner.url, 'podcast') }}
    </small>
  </p>
  {% endif %}
  <p>
    <strong>{{ '{:%-d.%-m.%Y}'.format(event.start_at) }}</strong>
    —
    {{ event.start_at|local_time }} online v klubovně</strong>{% if event.recording_url %},
    <a href="{{ event.recording_url }}">záznam pro členy</a>{% endif %}{% if event.public_recording_url %},
    <a href="{{ event.public_recording_url }}">veřejný záznam</a>{% endif %}
  </p>
  {{ event.description|md }}
  {{ img('static/' + event.avatar_path, event.title, 100, 100, class='podcast-episode-image') }}
  <p>
    <strong>{{ event.bio_name }}:</strong> {{ event.bio|md|remove_p }}
  </p>
{% else %}
<p>Příští akce ještě nebyly oznámeny.</p>
{% endif %}

## Archiv

{% for event in events_archive %}
<div id="{{ event.slug }}" class="podcast-episode">
  <h3>{{ event.title }}<a class="headerlink" href="#{{ event.slug }}" title="Odkaz na tuto akci">#</a></h3>
  {% if event.partner %}
  <p>
    <span class="badge text-bg-primary">Spolupráce</span>
    <small>
    Akce vznikla v rámci
    {% set active_partnership = event.partner.active_partnership() %}
    {% if active_partnership %}
      <a href="{{ pages|docs_url(active_partnership.page_url)|url }}">placeného partnerství</a>
    {% else %}
      placeného partnerství
    {% endif %}
    s firmou {{ partner_link(event.partner.name, event.partner.url, 'podcast') }}
    </small>
  </p>
  {% endif %}
  <p>
    <strong>{{ '{:%-d.%-m.%Y}'.format(event.start_at) }}</strong>
    —
    {{ event.start_at|local_time }} online v klubovně</strong>{% if event.recording_url %},
    <a href="{{ event.recording_url }}">záznam pro členy</a>{% endif %}{% if event.public_recording_url %},
    <a href="{{ event.public_recording_url }}">veřejný záznam</a>{% endif %}
  </p>
  {{ event.description|md }}
  {{ img('static/' + event.avatar_path, event.title, 100, 100, class='podcast-episode-image') }}
  <p>
    <strong>{{ event.bio_name }}:</strong> {{ event.bio|md|remove_p }}
  </p>
</div>
{% endfor %}
