---
title: Online akce pro začátečníky v programování
description: Online akce pro členy klubu junior.guru. Seznam akcí proběhlých i budoucích. Přednášky, Q&A, AMA, webináře, a další.
template: main_news.html
---

{% from 'macros.html' import lead, news_card with context %}


# Klubové akce

{% call lead() %}
Přednášky a další akce pro členy klubu junior.guru. Seznam akcí proběhlých i budoucích.
{% endcall %}

## Jak to funguje?

Večerní tematické přednášky jsou vždy předem oznámeny na konkrétní datum a čas. Pokud chceš přednášku slyšet, připoj se v ten čas do hlasové místnosti #přednášky. Po skončení přednášky není žádný další oficiální program. Cílem je, aby přednášky byly spíše rychlé a časté, než plánované do celovečerních bloků. Tak nezaberou příliš mnoho času a můžeš se připojit, i když máš nabitý den, nebo prostě jen nechceš trávit celý večer na nějakém srazu.

Nepořizujeme profesionální záznam, ale snažíme se alespoň nahrát obrazovku, aby si přednášku mohli pustit i členové, kteří v čas přednášky nemají čas. Nedáváme žádnou záruku na existenci záznamu ani jeho kvalitu. Pokud existuje, je členům k dispozici skrze tajný odkaz na YouTube. Odkaz na video veřejně prosím nesdílej, ale kamarádům jej klidně pošli – asi stejně jako když pro známé odemykáš placený článek v novinách.

## Plánované

{% if events_planned|length %}
  {% for event in events_planned %}
    <div id="{{ event.slug }}">
      {{ news_card(
        event.title,
        pages|docs_url(event.page_url)|url,
        event.avatar_path,
        event.bio_name,
        subtitle=event.bio_name,
        small='{:%-d.%-m.%Y}'.format(event.start_at))
      }}
    </div>
  {% endfor %}
{% else %}
<p>Příští akce ještě nebyly oznámeny.</p>
{% endif %}

## Archiv

{% for event in events_archive %}
  <div id="{{ event.slug }}">
    {{ news_card(
      event.title,
      pages|docs_url(event.page_url)|url,
      event.avatar_path,
      event.bio_name,
      subtitle=event.bio_name,
      small='{:%-d.%-m.%Y}'.format(event.start_at))
    }}
  </div>
{% endfor %}
