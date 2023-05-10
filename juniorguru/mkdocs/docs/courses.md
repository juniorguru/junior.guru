---
title: Kurzy programování
thumbnail_title: Katalog kurzů programování
---

{% from 'macros.html' import link_card, note, lead with context %}


# Kurzy programování

{% call lead() %}
  Seznam míst, kde se můžeš učit programovat.
  Kurzy, které zaplatily za zvýraznění, jsou v přehledu první.
  Neznamená to nutně, že jsou nejlepší, nebo že je junior.guru doporučuje.
  Jinak je seznam abecedně.
{% endcall %}

<div class="link-cards">
  {% for course_provider in course_providers %}
    {% if course_provider.active_partnership() %}
      {{ link_card(
        course_provider.name,
        pages|docs_url(course_provider.page_url)|url,
        screenshot_source_url=course_provider.url,
        highlighted=True,
        badge_icon='star',
        badge_text='Partner',
      ) }}
    {% else %}
      {{ link_card(
        course_provider.name,
        pages|docs_url(course_provider.page_url)|url,
        screenshot_source_url=course_provider.url,
        nofollow=True,
      ) }}
    {% endif %}
  {% endfor %}
</div>

{% call note() %}
  {{ 'plus-circle'|icon }} Pokud víš o dalších kurzech, piš na {{ 'honza@junior.guru'|email_link }}
{% endcall %}
