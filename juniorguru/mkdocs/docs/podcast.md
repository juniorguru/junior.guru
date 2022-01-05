---
title: Junior Guru podcast
description: Jsme tu pro všechny juniory v IT! Jak začít s programováním? Jak najít práci v IT? Přinášíme odpovědi, inspiraci, motivaci.
---

# Junior Guru podcast

Ajaj! Tato stránka se teprve připravuje. Epizody:

<ul>
{% for episode in podcast_episodes %}
<li id="{{ episode.slug }}">
{{ episode.title }}
</li>
{% endfor %}
</ul>
