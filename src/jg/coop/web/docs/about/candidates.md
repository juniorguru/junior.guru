---
title: O kandidátech na junior.guru
template: main_about.html
---

{% from 'macros.html' import lead, note with context %}

# Vše o kandidátech

{% call lead() %}
Informace o [seznamu juniorních kandidátů](../candidates.jinja) a o kontrolách GitHub profilů. Záměr a hodnoty, se kterými je to provozováno. K tomu ještě pár zajímavých statistik.
{% endcall %}

[TOC]

## Vznik

Seznam kandidátů vznikl v roce 2025 jako reakce na otočku trhu, který začal být zdrženlivější a bylo stále těžší prosadit juniory do firem. Kandidáti se mohou do seznamu přidat zdarma, firmy mohou seznam zdarma používat. Pokud si kandidát platí za klub, tak je zvýrazněný.

Cílem je podpořit nábor juniorů ve firmách a odprezentovat juniory v tom nejlepším světle. Aby kandidáti měli určitou minimální laťku, je na seznam napojený systém denních kontrol. Pokud kandidát přestane laťku splňovat, spadne na konec seznamu a zobrazí se poloprůhledně.

Junioři si mohou z úvodní stránky junior.guru kdykoliv sami a zdarma spustit zpětnou vazbu na svůj profil, což by mělo sloužit jako zpětná vazba, jestli jsou už připraveni hledat si první práci.

## Počet kandidátů

Tlustá čára ukazuje, kolik kandidátů se na portálu prezentovalo v jednotlivých měsících. Tenké čáry ještě zvlášť vypichují určité zajímavé skupiny, které se ale prolínají.

{% call note() %}
  {{ 'trash'|icon }} V prvním půlroce provozu seznamu kandidátů se nesbírala data o jejich počtu, takže v grafu chybí.
{% endcall %}

{% if charts.candidates_listed_breakdown_labels -%}
<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts.candidates_listed_breakdown_labels,
        'datasets': [
            {
                'label': 'všichni',
                'data': charts.candidates_listed_breakdown.pop('listed_total'),
                'borderColor': '#1755d1',
                'borderWidth': 2,
            },
            {
                'label': 'dostatečně připravení',
                'data': charts.candidates_listed_breakdown.pop('listed_ready'),
                'borderColor': '#4c73bf',
                'borderWidth': 1,
            },
            {
                'label': 'členové klubu',
                'data': charts.candidates_listed_breakdown.pop('listed_members'),
                'borderColor': '#02cabb',
                'borderWidth': 1,
            },
            {
                'label': 'ženy',
                'data': charts.candidates_listed_breakdown.pop('listed_feminine'),
                'borderColor': '#dc3545',
                'borderWidth': 1,
            },
        ],
    }|tojson|forceescape }}"
    {{ charts.candidates_listed_breakdown.keys()|list|assert_empty }}
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'beginAtZero': true}},
        'plugins': {'annotation': charts.candidates_listed_breakdown_annotations},
    }|tojson|forceescape }}"></canvas></div></div>
{% else %}
  {% call note() -%}
    {{ 'cloud-rain'|icon }} Graf je momentálně rozbitý.
  {%- endcall %}
{% endif %}

## Typy kandidátů (% z celku)

Vývoj určitých zajímavých skupin kandidátů, podobně jako v předchozím grafu, akorát jako procento z celku.

{% if charts.candidates_listed_breakdown_ptc_labels -%}
<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts.candidates_listed_breakdown_ptc_labels,
        'datasets': [
            {
                'label': '% dostatečně připravení',
                'data': charts.candidates_listed_breakdown_ptc.pop('listed_ready'),
                'borderColor': '#1755d1',
                'borderWidth': 2,
            },
            {
                'label': '% členové klubu',
                'data': charts.candidates_listed_breakdown_ptc.pop('listed_members'),
                'borderColor': '#02cabb',
                'borderWidth': 2,
            },
            {
                'label': '% ženy',
                'data': charts.candidates_listed_breakdown_ptc.pop('listed_feminine'),
                'borderColor': '#dc3545',
                'borderWidth': 2,
            },
        ],
    }|tojson|forceescape }}"
    {{ charts.candidates_listed_breakdown_ptc.keys()|list|assert_empty }}
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'min': 0}},
        'plugins': {'annotation': charts.candidates_listed_breakdown_ptc_annotations},
    }|tojson|forceescape }}"></canvas></div></div>
{% else %}
  {% call note() -%}
    {{ 'cloud-rain'|icon }} Graf je momentálně rozbitý.
  {%- endcall %}
{% endif %}

## Počet kontrol GitHub profilů

Počet spuštěných zpětných vazeb na GitHub profily v jednotlivých měsících. V podstatě je to [tenhle filtr](https://github.com/juniorguru/eggtray/issues?q=is%3Aissue%20label%3Acheck) převedený do grafu. V samém počátku existence kontrol jich bylo skoro 50 za měsíc, protože se hodně testovalo, jestli to vůbec funguje 😀 Ty další měsíce jsou už reálný provoz.

{% if charts.candidates_github_checks_labels -%}
<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts.candidates_github_checks_labels,
        'datasets': [
            {
                'label': 'kontroly',
                'data': charts.candidates_github_checks,
                'borderColor': '#1755d1',
                'borderWidth': 2,
            },
        ],
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'beginAtZero': true}},
        'plugins': {'annotation': charts.candidates_github_checks_annotations},
    }|tojson|forceescape }}"></canvas></div></div>
{% else %}
  {% call note() -%}
    {{ 'cloud-rain'|icon }} Graf je momentálně rozbitý.
  {%- endcall %}
{% endif %}
