---
title: Podcast pro juniory v IT
template: main_podcast.html
description: Jak začít s programováním? Jak najít práci v IT? Přinášíme odpovědi, inspiraci, motivaci.
---

{% from 'macros.html' import lead, markdown, img with context %}


# Podcast

{% call lead() %}
Podcast pro juniory v IT! Jak začít s programováním? Jak najít práci v IT? Přinášíme odpovědi, inspiraci, motivaci.
{% endcall %}

<div class="standout">
  <a class="podcast-button spotify" href="https://open.spotify.com/show/12w93IKRzfCsgo7XrGEVw4">{{ 'spotify'|icon }} Spotify</a>
  <!-- <a class="podcast-button google" href="#">{{ 'google'|icon }} Google</a> -->
  <a class="podcast-button apple" href="https://podcasts.apple.com/cz/podcast/junior-guru-podcast/id1603653549">{{ 'apple'|icon }} Apple</a>
  <a class="podcast-button youtube" href="https://www.youtube.com/channel/UCp-dlEJLFPaNExzYX079gCA">{{ 'youtube'|icon }} YouTube</a>
  <a class="podcast-button rss" href="https://junior.guru/api/podcast.xml">{{ 'rss-fill'|icon }} RSS</a>
</div>

<h2 class="visually-hidden">Autoři</h2>
<div class="podcast-author">
  {{ img('static/images/paja.jpg', 'Pája Froňková', 100, 100, lazy=False, class='podcast-author-photo') }}
  <div class="podcast-author-body">
    <h3>Pája Froňková</h3>
    {% call markdown() -%}
      Autorka podcastu, datová analytička, PyLady. [Svou cestu do IT](https://medium.com/productboard-engineering/making-data-accessible-to-everyone-at-productboard-an-interview-with-p%C3%A1ja-fronkova-7940ecc6aa35) má ještě čerstvě v paměti. Vymýšlí témata, zve hosty, moderuje. Natáčí a stříhá epizody.
    {%- endcall %}
  </div>
</div>
<div class="podcast-author">
  {{ img('static/images/honza.jpg', 'Honza Javorek', 100, 100, lazy=False, class='podcast-author-photo') }}
  <div class="podcast-author-body">
    <h3>Honza Javorek</h3>
    {% call markdown() -%}
      Autor projektu junior.guru. Pomáhá shánět hosty, stará se o technické zázemí podcastu a propagaci epizod.
    {%- endcall %}
  </div>
</div>

## Epizody

Pája je aktuálně na rodičovské a Honza má s junior.guru i tak práce dost, takže jsme se rozhodli pro pohodové tempo. Chceme vydávat zhruba **jednu epizodu měsíčně**.

{% for episode in podcast_episodes %}
### {{ episode.title_numbered }}    <span id="{{ episode.slug }}"></span>

**{{ episode.publish_on.day }}.{{ episode.publish_on.month }}.{{ episode.publish_on.year }}** — {{ episode.description }}

<audio controls preload="metadata">
  <source src="{{ episode.media_url }}" type="audio/mpeg">
  <a class="btn btn-primary" href="{{ episode.media_url }}" role="button">{{ 'play-circle-fill'|icon }} {{ episode.media_duration_s // 60 }}min</a>
</audio>
{% endfor %}
