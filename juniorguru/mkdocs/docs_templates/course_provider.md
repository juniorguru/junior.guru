{% from 'macros.html' import link_card, note, lead, img with context %}

{% set active_partnership = course_provider.active_partnership() %}


# Kurzy od {{ course_provider.name }}

{% call lead() %}
  {{ course_provider.page_lead }}
  <!-- TODO Tady je aspoň základní info, které ti pomůže s rozhodováním. -->
{% endcall %}

{% if active_partnership %}
  {{ link_card(course_provider.name, course_provider.url, highlighted=True,
               badge_icon='star', badge_text='Partner') }}
{% else %}
  {{ link_card(course_provider.name, course_provider.url, nofollow=True) }}
{% endif %}

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }}
  Zatím tady chybí základní info.
  Pokud o {{ course_provider.name }} něco víš, napiš prosím na {{ 'honza@junior.guru'|email_link }}.
  Umíš s GitHubem?
  [Pošli Pull Request]({{ course_provider.edit_url }})!
{% endcall %}

## Recenze

Nějaké recenze najdeš na místním Discordu.
{% if topic.mentions_count > 5 -%}
  Vyloženě o {{ course_provider.name }} tam je už **{{ topic.mentions_count|thousands }} zmínek**.
{%- endif %}
Dojmy absolventů ti mohou pomoci poodhalit celkovou kvalitu, ale čti je s rezervou.
Nevíš, s jakými očekáváními si kurz vybrali.

Jak zjistíš, zda je vzdělávání u {{ course_provider.name }} vhodné zrovna pro tebe?
Vždy záleží v jaké jsi konkrétní situaci a co zrovna potřebuješ.
A přesně takové věci se na tom našem Discordu taky probírají.
Poradíme!

<div class="text-center mt-4">
  <a class="btn btn-lg btn-primary mb-4" href="{{ pages|docs_url('club.md')|url }}">
    Přidej se do klubu
  </a>
  <div>
    <span class="members mb-0">
    {% for member in members|sample(10) %}
      {{ img('static/' + member.avatar_path, 'Profilovka člena klubu', 50, 50, lazy=False) }}
    {% endfor %}
    </span>
  </div>
</div>

{% if active_partnership %}
## Partnerství s junior.guru

{{ course_provider.name }} si tady platí zvýraznění.
Neznamená to nutně, že jsou nejlepší, nebo že je junior.guru doporučuje.
Vše kolem partnerství je transparentní, takže klidně [mrkni na detaily]({{ pages|docs_url(active_partnership.page_url)|url }}).
{% endif %}
