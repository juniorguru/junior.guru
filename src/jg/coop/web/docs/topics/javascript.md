---
title: JavaScript mentoring
template: main.html
topic_name: javascript
topic_link_text: JavaScript
description: Učíš se JavaScript? Hledáš někoho zkušenějšího, kdo ti poradí, když se zasekneš? Kdo ti ukáže správné postupy a nasměruje tě na kvalitní návody nebo kurzy?
thumbnail_button_link: junior.guru/club
thumbnail_button_icon: chat-heart
---
{% from 'macros_topic.html' import intro, mentions with context %}

{{ intro('Nech si poradit s JavaScriptem', page.meta.description) }}

{{ mentions(topic, 'JavaScriptu') }}

<p class="text-center my-5">
  <a href="{{ pages|docs_url('club.md')|url }}" class="btn btn-primary btn-lg">
    Přidej se&nbsp;k&nbsp;nám
  </a>
</p>
