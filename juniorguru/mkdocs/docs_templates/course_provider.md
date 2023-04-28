{% from 'macros.html' import link_card, note with context %}


# Kurzy od {{ course_provider.name }}

{{ link_card(course_provider.name, course_provider.url, nofollow=True) }}

## Základní info

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }} O těchto kurzech zatím chybí základní informace.
{% endcall %}

<div class="standout text-center">
  <a class="btn btn-lg btn-outline-primary" href="{{ course_provider.edit_url }}">
    Doplnit informace
  </a>
</div>


## Recenze na {{ course_provider.name }}

Hledáš někoho, kdo má zkušenosti s {{ course_provider.name }}?
Vyplatí se tyhle kurzy?
V klubu tady na junior.guru se přesně takové věci probírají.
Dostaneš informace, motivaci, rady.
Kromě toho ale i parťáky, podporu, kontakty a pracovní nabídky.

<!-- Diskutuj v klubu pro začátečníky, kde najdeš pomoc, motivaci, kamarády, práci. -->

<div>
{% if topic.mentions_count %}
  V klubu máme
  {% if topic.mentions_count == 1 %}
    zatím jen jednu zmínku
  {% elif topic.mentions_count < 5 %}
    už {{ topic.mentions_count }} zmínky
  {% else %}
    už {{ topic.mentions_count }} zmínek
  {% endif %}
  o {{ course_provider.name }}.
  {% if topic.topic_channels_messages_count %}
    Dokonce máme na toto téma i celou místnost, kam jsme napsali {{ topic.topic_channels_messages_count }} zpráv.
  {% endif %}
  {% if topic.mentions_count > 1 %}
    Poradíme ti!
  {% else %}
    Pojďme to probrat!
  {% endif %}
{% else %}
  V klubu máme o {{ course_provider.name }} celou místnost, kam jsme už napsali {{ topic.topic_channels_messages_count }} zpráv.
  Poradíme ti!
{% endif %}
</div>

<div class="standout text-center">
  <a class="btn btn-lg btn-outline-primary" href="{{ pages|docs_url('club.md')|url }}">
    Přidej se k nám
  </a>
</div>
