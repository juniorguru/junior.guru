---
title: Kurzy programování
thumbnail_title: Katalog kurzů programování
---

{% from 'macros.html' import link_card with context %}


# Kurzy programování

<div class="link-cards">
  {% for course_provider in course_providers %}
    {{ link_card(course_provider.name, course_provider.url, nofollow=True) }}
  {% endfor %}
</div>

<small>Tento seznam je v abecedním pořadí. Pokud víš o dalším webu s kurzy, piš na {{ 'honza@junior.guru'|email_link }}.</small>
