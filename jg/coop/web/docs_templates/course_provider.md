{% from 'macros.html' import club_teaser, figure, lead, link_card, note with context %}

<nav aria-label="breadcrumb">
  <ol class="breadcrumb">
    <li class="breadcrumb-item">
      <a href="{{ (page|parent_page).url|url }}">
        {{ (page|parent_page).title }}
      </a>
    </li>
    <li class="breadcrumb-item active" aria-current="page">
      {{ course_provider.name }}
    </li>
  </ol>
</nav>

# Kurzy od {{ course_provider.name }}

{% call lead() %}
  {{ course_provider.page_lead }}
  {% if course_provider.usp_description %}Tady je aspoň základní info, které ti pomůže s rozhodováním.{% endif %}
{% endcall %}

{% if course_provider.group == "highlighted" %}
<div class="course-provider-header">
  {{ link_card(course_provider.name, course_provider.url, class='highlighted') }}
  {{ figure('static/' + course_provider.organization.logo_path, 'logo ' + course_provider.name, 200, 100, lazy=False, class='course-provider-logo') }}
</div>
{% else %}
  {{ link_card(course_provider.name, course_provider.url, nofollow=True) }}
{% endif %}

{% if course_provider.usp_description %}
{{ course_provider.usp_description }}

<small>
Pokud tento popis umíš nějak doplnit, napiš prosím na {{ 'honza@junior.guru'|email_link }}.
Umíš s GitHubem? [Pošli Pull Request]({{ course_provider.edit_url }})!
</small>
{% else %}
{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }}
  Zatím tady chybí základní info.
  Pokud o {{ course_provider.name }} něco víš, napiš prosím na {{ 'honza@junior.guru'|email_link }}.
  Umíš s GitHubem? [Pošli Pull Request]({{ course_provider.edit_url }})!
{% endcall %}
{% endif %}

## Recenze

Nějaké recenze najdeš na místním Discordu.
{% if topic.mentions_count > 5 -%}
  Vyloženě o {{ course_provider.name }} tam je **{{ topic.mentions_count|thousands }} zmínek**.
{%- endif %}
Dojmy absolventů ti mohou pomoci poodhalit celkovou kvalitu, ale čti je s rezervou.
Nevíš, s jakými očekáváními si kurz vybrali.

Jak zjistíš, zda je vzdělávání u {{ course_provider.name }} vhodné zrovna pro tebe?
Vždy záleží v jaké jsi konkrétní situaci a co zrovna potřebuješ.
A přesně takové věci se na tom našem Discordu taky probírají.
Poradíme!

{{ club_teaser("Hledej recenze v klubu") }}

## Úřad práce

Úřad práce ČR přispívá na kurzy, které má ve svém katalogu [Jsem v kurzu](https://www.mpsv.cz/jsem-v-kurzu).
{%- if course_provider.list_courses_up|length %}
Provozovatel {{ course_provider.name }} tam nabízí tyto kurzy:
{% for course in course_provider.list_courses_up %}
- [{{ course.name }}]({{ course.url }})
{% endfor %}
{% else %}
{{ course_provider.name }} tam žádné kurzy nenabízí.
{% endif %}

{% if course_provider.group == "partners" %}
## Spolupráce s junior.guru

{{ course_provider.name }} spolupracuje s junior.guru. Vztah s junior.guru je v interních záznamech popsán následovně:

„{{ course_provider.organization.note }}“

Není v možnostech junior.guru ověřovat kvalitu kurzů, ale takováto spolupráce se asi dá brát jako známka toho, že jde o něco důvěryhodného.
{% elif course_provider.group == "highlighted" %}
## Sponzorství junior.guru

{{ course_provider.name }} sponzoruje junior.guru a díky tomu tady má zvýraznění.
Neznamená to, že jsou nejlepší, že je kurz nějak ověřený, nebo že je junior.guru doporučuje.
Budiž jim však ke cti, že podporují tento projekt.
{% else %}
## Vztah s junior.guru

Kurzy od {{ course_provider.name }} jsou tady v rámci seznamu všech míst, kde se můžeš učit programovat.
Neznamená to, že jsou dobré, ověřené, nebo že je junior.guru doporučuje.
{% endif %}

<div class="pagination">
  <div class="pagination-control">
    <a href="{{ (page|parent_page).url|url }}" class="pagination-button">
      {{ 'arrow-left'|icon }}
      Všechny kurzy
    </a>
  </div>
</div>
