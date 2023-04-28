{% from 'macros.html' import link_card, note, lead, img with context %}


# Kurzy od {{ course_provider.name }}

{% call lead() %}
  {{ course_provider.page_lead }}
  <!-- TODO Tady je aspoň základní info, které ti pomůže s rozhodováním. -->
{% endcall %}

{{ link_card(course_provider.name, course_provider.url, nofollow=True) }}

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }}
  Zatím tady chybí základní info.
  Pokud o {{ course_provider.name }} něco víš, napiš prosím na {{ 'honza@junior.guru'|email_link }}.
  Umíš s GitHubem?
  [Pošli Pull Request]({{ course_provider.edit_url }})!
{% endcall %}

## Recenze

{% call lead() %}
Nějaké recenze najdeš na zdejším Discordu.
Dojmy absolventů ti mohou pomoci poodhalit celkovou kvalitu, ale čti je s rezervou.
Nevíš, s jakými očekáváními si kurz vybrali.

Jak zjistíš, zda je vzdělávání u {{ course_provider.name }} vhodné zrovna pro tebe?
Vždy záleží v jaké jsi konkrétní situaci a co zrovna potřebuješ.
A přesně takové věci se na tom našem Discordu taky probírají.
{% if topic.mentions_count > 5 -%}
  Vyloženě o {{ course_provider.name }} tam máme už **{{ topic.mentions_count|thousands }} zmínek**.
{%- endif %}
Poradíme!
{% endcall %}

<div class="standout text-center">
  <a class="btn btn-lg btn-primary mb-4" href="{{ pages|docs_url('club.md')|url }}">
    Přidej se do klubu
  </a>
  <div>
    <span class="members">
    {% for member in members|sample(10) %}
      {{ img('static/' + member.avatar_path, 'Profilovka člena klubu', 50, 50, lazy=False) }}
    {% endfor %}
    </span>
  </div>
</div>
