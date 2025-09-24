{% from 'macros.html' import club_teaser, img, lead, note with context %}

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

{% set screenshot_image_url = course_provider.url|screenshot_url %}
<div class="standout details {{ course_provider.group }}"
  data-screenshot-source-url="{{ course_provider.url }}"
  data-screenshot-image-url="{{ screenshot_image_url }}">
  {% if course_provider.group == "highlighted" %}
    <div class="details-header">
      {{ img('static/' + course_provider.organization.logo_path, 'logo ' + course_provider.name, 200, 100, class='details-logo', lazy=False) }}
    </div>
  {% endif %}
  <div class="details-info">
    <div class="details-image">
      {{ img(screenshot_image_url, title, 640, 360, class='details-thumbnail', lazy=False) }}
    </div>
    <div class="details-body">
      <ul class="details-items">
        <li class="details-item">
          <strong>Název:</strong>
          {{ course_provider.name }}
        </li>
        <li class="details-item">
          <strong>Web:</strong>
          <a href="{{ course_provider.url }}" target="_blank"
            {% if course_provider.group != "highlighted" %}rel="nofollow noopener"{% endif -%}
          >
            {{ course_provider.url|nice_url }}
          </a>
        </li>
      </ul>
      {% if course_provider.cz_business_id %}
      <h5 class="details-heading">Provozovatel v Česku</h5>
      <ul class="details-items compact">
        {% if course_provider.cz_name %}
        <li class="details-item">
          {{ course_provider.cz_name }}
        </li>
        {% endif %}
        {% if course_provider.cz_legal_form %}
        <li class="details-item">
          <strong>Forma:</strong>
          {{ course_provider.cz_legal_form }}
        </li>
        {% endif %}
        <li class="details-item">
          <strong>IČO:</strong>
          {{ '{:08d}'.format(course_provider.cz_business_id) }}
        </li>
        {% if course_provider.cz_years_in_business %}
        <li class="details-item">
          <strong>Funguje:</strong>
          {{ course_provider.cz_years_in_business }}
          {{ course_provider.cz_years_in_business|nplurals("rok", "roky", "let") }}
        </li>
        {% endif %}
      </ul>
      {% endif %}
      {% if course_provider.sk_business_id %}
      <h5 class="details-heading">Provozovatel na Slovensku</h5>
      <ul class="details-items compact">
        {% if course_provider.sk_name %}
        <li class="details-item">
          {{ course_provider.sk_name }}
        </li>
        {% endif %}
        {% if course_provider.sk_legal_form %}
        <li class="details-item">
          <strong>Forma:</strong>
          {{ course_provider.sk_legal_form }}
        </li>
        {% endif %}
        <li class="details-item">
          <strong>IČO:</strong>
          {{ '{:08d}'.format(course_provider.sk_business_id) }}
        </li>
        {% if course_provider.sk_years_in_business %}
        <li class="details-item">
          <strong>Funguje:</strong>
          {{ course_provider.sk_years_in_business }}
          {{ course_provider.sk_years_in_business|nplurals("rok", "roky", "let") }}
        </li>
        {% endif %}
      </ul>
      {% endif %}
    </div>
    {% if course_provider.cz_business_id or course_provider.sk_business_id %}
      <p class="details-note">
        {{ 'info-circle'|icon }}
        Imper pro junior.guru zdarma poskytl údaje ze své <a href="https://www.merk.cz/?utm_source=junior.guru&utm_medium=web&utm_campaign=catalog" rel="noopener" target="_blank">databáze firem Merk</a>. Děkujeme!
      </p>
    {% endif %}
  </div>
</div>

[TOC]

## Popis
{% if course_provider.usp_description %}
{{ course_provider.usp_description }}

<small>
Pokud tento popis umíš nějak doplnit, napiš prosím na {{ 'honza@junior.guru'|email_link }}.
Umíš s GitHubem? [Pošli Pull Request]({{ course_provider.edit_url }})!
</small>
{% else %}
{% call note() %}
  {{ 'exclamation-circle'|icon }}
  Zatím tady chybí popis.
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

{% set courses_up = course_provider.list_courses_up|list %}

Úřad práce ČR přispívá na kurzy, které má ve svém katalogu [Jsem v kurzu](https://www.mpsv.cz/jsem-v-kurzu).
{%- if courses_up %}
Provozovatel {{ course_provider.name }} tam nabízí tyto kurzy:
<table class="table">
{% for course in courses_up %}
  <tr>
    <td>
      <a href="{{ course.url }}" rel="nofollow noopener" target="_blank">
        {{ course.name }}
      </a>
    </td>
  </tr>
{% endfor %}
</table>
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
Neznamená to ale, že junior.guru tvrdí, že jsou dobré, ověřené, nebo je doporučuje.
Budiž jim však ke cti, že podporují tento projekt.
{% else %}
## Vztah s junior.guru

Kurzy od {{ course_provider.name }} jsou tady v rámci seznamu všech míst, kde se můžeš učit programovat.
Neznamená to, že junior.guru tvrdí, že jsou dobré, ověřené, nebo je doporučuje.
{% endif %}

<div class="pagination">
  <div class="pagination-control">
    <a href="{{ (page|parent_page).url|url }}" class="pagination-button">
      {{ 'arrow-left'|icon }}
      Všechny kurzy
    </a>
  </div>
</div>
