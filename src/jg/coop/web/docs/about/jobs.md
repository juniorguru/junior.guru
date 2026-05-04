---
title: O inzerátech na junior.guru
template: main_about.html
---

{% from 'macros.html' import lead, note with context %}

# Vše o inzerátech

{% call lead() %}
Informace o [inzerátech pro juniory](../jobs.jinja). Záměr a hodnoty, se kterými je to provozováno. K tomu ještě pár zajímavých statistik.
{% endcall %}

[TOC]

## Vznik

Pracovní nabídky jsou na webu od jeho vzniku. Původně to měl být způsob, jak bude junior.guru vydělávat na svůj provoz, ale brzy se ukázalo, že to není dostatečně nosný zdroj příjmů. Inzerátů zadaných přímo přes junior.guru bylo jen pár, tak se časem zrodil systém, kdy se stahují nabídky z různých jiných portálů a pak třídí, aby zbyly jen ty vyloženě pro juniory.

Třídění bylo původně naprogramováno ručně a šlo zhruba o 20.000 řádků kódu. V roce 2024 systém přešel na analýzu pomocí AI. Stahování a třídění je náročné provozovat, ale juniorům je výsledek přístupný zdarma na webu.

Členové klubu mají inzeráty k dispozici v rámci Discordu, mohou tam o nich diskutovat a dovědět se okamžitě o přidávání nových.

## Počet inzerátů

Kolik inzerátů bylo v jednotlivých měsících uveřejněno na portálu a kolik inzerátů k tomu přidali ručně členové klubu na Discordu. Data vycházejí z týdenních záznamů agregovaných po měsících.

{% call note() %}
  {{ 'trash'|icon }} I když inzeráty na junior.guru existují od roku 2019, před červnem 2025 se o nich neukládala žádná dlouhodobá data.
{% endcall %}

{% if charts.jobs_count_listed_discord_labels -%}
<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="300"
    data-chart-type="bar"
    data-chart="{{ {
        'labels': charts.jobs_count_listed_discord_labels,
        'datasets': [
            {
                'label': 'stažené odjunud',
                'data': charts.jobs_count_listed_discord.pop('listed'),
                'backgroundColor': '#1755d1',
            },
            {
                'label': 'ručně přidané',
                'data': charts.jobs_count_listed_discord.pop('discord'),
                'backgroundColor': '#638cdd',
            },
        ],
    }|tojson|forceescape }}"
    {{ charts.jobs_count_listed_discord.keys()|list|assert_empty }}
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'x': {'stacked': True}, 'y': {'stacked': True, 'beginAtZero': true}},
        'plugins': {'annotation': charts.jobs_count_listed_discord_annotations},
    }|tojson|forceescape }}"></canvas></div></div>
{% else %}
  {% call note() -%}
    {{ 'cloud-rain'|icon }} Graf je momentálně rozbitý.
  {%- endcall %}
{% endif %}

## Stažené a uveřejněné inzeráty

Každý den robot stáhne stovky inzerátů z několika jiných pracovních portálů a potom je třídí pomocí AI, aby zbyly pouze ty opravdu juniorní. Na grafu je vidět poměr uveřejněných a zahozených inzerátů.

Nelze jej ovšem vykládat jako podíl juniorních inzerátů na trhu, protože počet všech stažených inzerátů není o ničem vypovídající. Řídí technickými možnostmi a omezeními samotného stahování. Někdy např. lze už před stahováním pracovní nabídky vhodně předfiltrovat, jindy to nejde jinak, než stáhnout spoustu „smetí“ a filtrovat to dodatečně.

{% call note() %}
  {{ 'trash'|icon }} I když inzeráty na junior.guru existují od roku 2019, před červnem 2025 se o nich neukládala žádná dlouhodobá data.
{% endcall %}

{% if charts.jobs_count_listed_dropped_labels -%}
<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="300"
    data-chart-type="bar"
    data-chart="{{ {
        'labels': charts.jobs_count_listed_dropped_labels,
        'datasets': [
            {
                'label': 'uveřejněné',
                'data': charts.jobs_count_listed_dropped.pop('listed'),
                'backgroundColor': '#1755d1',
            },
            {
                'label': 'zahozené',
                'data': charts.jobs_count_listed_dropped.pop('dropped'),
                'backgroundColor': '#a9a9a9',
            },
        ],
    }|tojson|forceescape }}"
    {{ charts.jobs_count_listed_dropped.keys()|list|assert_empty }}
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'x': {'stacked': True}, 'y': {'stacked': True, 'beginAtZero': true}},
        'plugins': {'annotation': charts.jobs_count_listed_dropped_annotations},
    }|tojson|forceescape }}"></canvas></div></div>
{% else %}
  {% call note() -%}
    {{ 'cloud-rain'|icon }} Graf je momentálně rozbitý.
  {%- endcall %}
{% endif %}

## Uveřejněné inzeráty (% ze všech stažených)

V podstatě totéž co předchozí graf, akorát ne jako absolutní čísla, ale jako procenta. Opět platí, že graf nelze vykládat jako podíl juniorních inzerátů na trhu, protože počet všech stažených inzerátů není o ničem vypovídající.

{% call note() %}
  {{ 'trash'|icon }} I když inzeráty na junior.guru existují od roku 2019, před červnem 2025 se o nich neukládala žádná dlouhodobá data.
{% endcall %}

{% if charts.jobs_listed_ptc_labels -%}
<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts.jobs_listed_ptc_labels,
        'datasets': [
            {
                'label': '% uveřejněných inzerátů',
                'data': charts.jobs_listed_ptc,
                'borderColor': '#1755d1',
                'borderWidth': 2,
            },
        ]
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'min': 0}},
        'plugins': {'annotation': charts.jobs_listed_ptc_annotations},
    }|tojson|forceescape }}"></canvas></div></div>
{% else %}
  {% call note() -%}
    {{ 'cloud-rain'|icon }} Graf je momentálně rozbitý.
  {%- endcall %}
{% endif %}
