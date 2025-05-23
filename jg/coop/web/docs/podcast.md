---
title: Podcast o programování a kariéře v IT
description: Jak začít s programováním? Jak najít práci v IT? Přinášíme odpovědi, inspiraci, motivaci.
template: main_podcast.html
---

{% from 'macros.html' import lead, markdown, img, news_card with context %}

# Podcast

{% call lead() %}
Podcast pro juniory v IT! Jak začít s programováním? Jak najít práci v IT? Přinášíme odpovědi, inspiraci, motivaci.
{% endcall %}

<div class="standout">
  <a class="brand-button youtube" target="_blank" rel="noopener" href="https://www.youtube.com/channel/UCp-dlEJLFPaNExzYX079gCA">{{ 'youtube'|icon }} YouTube</a>
  <a class="brand-button spotify" target="_blank" rel="noopener" href="https://open.spotify.com/show/12w93IKRzfCsgo7XrGEVw4">{{ 'spotify'|icon }} Spotify</a>
  <a class="brand-button apple" target="_blank" rel="noopener" href="https://podcasts.apple.com/cz/podcast/junior-guru-podcast/id1603653549">{{ 'apple'|icon }} Apple</a>
  <a class="brand-button rss" target="_blank" rel="noopener" href="https://junior.guru/api/podcast.xml">{{ 'rss-fill'|icon }} RSS</a>
  <a class="brand-button email" href="{{ pages|docs_url('news.jinja')|url }}">{{ 'envelope-paper-fill'|icon }} Newsletter</a>
</div>

<div class="team">
<h2 class="visually-hidden">Tým</h2>
<div class="team-member">
  {{ img('static/avatars-participants/pavlina-fronkova.jpg', 'Pája Froňková', 100, 100, lazy=False, class='team-member-photo') }}
  <div class="team-member-body">
    <h3>
      Pája Froňková
      <a class="team-member-link" href="https://www.linkedin.com/in/pavlinafronkova/" target="_blank" rel="noopener">
        {{ 'linkedin'|icon }}
        <span class="visually-hidden">LinkedIn</span>
      </a>
    </h3>
    {% call markdown() -%}
      Autorka podcastu, datová analytička, PyLady. Vymýšlí témata, zve hosty, moderuje. Natáčí a stříhá epizody.
    {%- endcall %}
  </div>
</div>
<div class="team-member">
  {{ img('static/avatars-participants/honza-javorek.jpg', 'Honza Javorek', 100, 100, lazy=False, class='team-member-photo') }}
  <div class="team-member-body">
    <h3>
      Honza Javorek
      <a class="team-member-link" href="https://www.linkedin.com/in/honzajavorek/" target="_blank" rel="noopener">
        {{ 'linkedin'|icon }}
        <span class="visually-hidden">LinkedIn</span>
      </a>
    </h3>
    {% call markdown() -%}
      Autor projektu junior.guru. Pomáhá shánět hosty, stará se o technické zázemí a propagaci podcastu.
    {%- endcall %}
  </div>
</div>
</div>

## Epizody

Poučky praví, že podcast se stává kvalitním a slavným, až když se autoři zajedou a vymluví, což trvá přibližně 100 epizod. Chceme vydávat zhruba **jednu epizodu měsíčně**, takže špičkové kvality a věčné slávy plánujeme dosáhnout kolem roku 2030. Znělku nám na míru složil [Patrik Veltruský](https://veltrusky.net/), děkujeme!

{% for podcast_episode in podcast_episodes %}
  {{
    news_card(
      category="Epizoda " ~ podcast_episode.number,
      **podcast_episode.to_card(),
    )
  }}
{% endfor %}
