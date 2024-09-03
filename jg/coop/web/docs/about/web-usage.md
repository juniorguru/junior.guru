---
title: Návštěvnost webu junior.guru
template: main_about.html
---

{% from 'macros.html' import lead, note with context %}

# Návštěvnost webu

{% call lead() %}
Na junior.guru se měří návštěvnost pomocí Simple Analytics, které nesledují uživatele, nepoužívají cookies a odpovídají všem zákonným i etickým normám. Všechny grafy níže zobrazují trend pouze zpětně za jeden rok, protože to tak Honzovi stačí.
{% endcall %}

[TOC]

## Otevřená data o návštěvnosti

Na této stránce jsou jen grafy, které by se ručně špatně naklikávaly na [Simple Analytics](https://simpleanalytics.com/junior.guru). Kompletní data o návštěvnosti jsou veřejně přístupná tam.

## Proč Simple Analytics

Rozhraní Google Analytics bylo komplikované a nepřehledné. Jejich skripty zpomalují načítání stránek. Google sleduje lidi a junior.guru by muselo mít cookie lištu.

Lidi na web junior.guru zavítají mnohokrát, než se pak rozhodnou, že půjdou do klubu zkusí jej.
Lze měřit, kolik jich projde od objednávky do Discordu, ale… V jednom člověku a v byznysu, který nemá jasnou cestu od načtení stránky po nákup, Honzovi stačí vidět to nahrubo a pocitově.
Pokročilé měření je zbytečné, stačí počítadlo.

Simple Analytics jsou přehledné a splňují veškeré zákonné i etické normy.
Nijak nenarušují soukromí návštěvníků webu, nezpomalují načítání, nevyžadují cookie lištu.

## Celková návštěvnost

Většinou je nejvyšší v lednu a nejnižší v létě.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts.web_usage_total_labels,
        'datasets': [
            {
                'label': 'celková návštěvnost',
                'data': charts.web_usage_total,
                'borderColor': '#1755d1',
                'borderWidth': 2,
            },
        ]
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'beginAtZero': true}},
        'plugins': {'annotation': charts.web_usage_total_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

## Souhrnná návštěvnost podle produktů

Nad jednotlivými částmi junior.guru Honza přemýšlí jako nad produkty.
Graf mu pomáhá zjistit, jak velkou návštěvnost přitahuje každý z nich.
Při čtení grafu je ale dobré si uvědomit, že návštěvnost není vše.
Například klub nebo podcast mají „to hlavní“ jinde než na webu.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts.web_usage_breakdown_labels,
        'datasets': [
            {
                'label': 'úvodní stránka',
                'data': charts.web_usage_breakdown.pop('home'),
                'borderColor': '#1755d1',
                'borderWidth': 2,
            },
            {
                'label': 'prodejní stránka klubu',
                'data': charts.web_usage_breakdown.pop('club'),
                'borderColor': '#dc3545',
                'borderWidth': 1,
            },
            {
                'label': 'příručka',
                'data': charts.web_usage_breakdown.pop('handbook'),
                'borderColor': '#02cabb',
                'borderWidth': 1,
            },
            {
                'label': 'katalog kurzů',
                'data': charts.web_usage_breakdown.pop('courses'),
                'borderColor': '#00b7eb',
                'borderWidth': 1,
            },
            {
                'label': 'pracovní inzeráty',
                'data': charts.web_usage_breakdown.pop('jobs'),
                'borderColor': '#638cdd',
                'borderWidth': 1,
            },
            {
                'label': 'stránka s podcastem',
                'data': charts.web_usage_breakdown.pop('podcast'),
                'borderColor': '#872ec4',
                'borderWidth': 1,
            },
        ],
    }|tojson|forceescape }}"
    {{ charts.web_usage_breakdown.keys()|list|assert_empty }}
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'beginAtZero': true}},
        'plugins': {'annotation': charts.web_usage_breakdown_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

## Konverze klubové prodejní stránky

Vývoj poměru mezi počtem zobrazení [klubové prodejní stránky](../club.md) a počtem dvou týdnů na zkoušku.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts.web_club_conversion_labels,
        'datasets': [
            {
                'label': '% konverze',
                'data': charts.web_club_conversion,
                'borderColor': '#1755d1',
                'borderWidth': 2,
            },
        ]
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'min': 0}},
        'plugins': {'annotation': charts.web_club_conversion_annotations},
    }|tojson|forceescape }}"
    data-chart-milestones-offset-ptc="0"></canvas></div></div>

## Registrace do klubu podle předchozí stránky

Když se někdo registruje do klubu, systém si uloží [referrer](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referer), tzn. z jaké webové stránky přišel.
{% if charts.total_internal_referrer_breakdown_count -%}
Procenta nejsou podíl ze všech příchozích, ale z **{{ charts.total_internal_referrer_breakdown_count }}** lidí, kteří měli za poslední půlrok _referrer_ z junior.guru.
Tzv. _long tail_ je z grafu uříznutý.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="300"
    data-chart-type="bar"
    data-chart="{{ {
        'labels': charts.total_internal_referrer_breakdown.keys()|list,
        'datasets': [
            {
                'axis': 'y',
                'label': '% členů',
                'data': charts.total_internal_referrer_breakdown.values()|list,
                'backgroundColor': '#1755d1',
            },
        ],
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'indexAxis': 'y',
        'interaction': {'mode': 'index'},
        'scales': {'y': {'beginAtZero': true}},
    }|tojson|forceescape }}"></canvas></div></div>
{% else %}
  {% call note() -%}
    {{ 'cloud-rain'|icon }} Graf je momentálně rozbitý.
  {%- endcall %}
{% endif %}

## Peníze za členství v klubu podle předchozí stránky

Když se někdo registruje do klubu, systém si uloží [referrer](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referer), tzn. z jaké webové stránky přišel.
Graf ukazuje, kolik takhle jednotlivé stránky skrze klub přinesly peněz.
{% if charts.total_spend_internal_referrer_breakdown_count -%}
Procenta nejsou podíl ze všech příchozích, ale z **{{ charts.total_spend_internal_referrer_breakdown_count }}** lidí, kteří měli za poslední půlrok _referrer_ z junior.guru.
Tzv. _long tail_ je z grafu uříznutý.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="300"
    data-chart-type="bar"
    data-chart="{{ {
        'labels': charts.total_spend_internal_referrer_breakdown.keys()|list,
        'datasets': [
            {
                'axis': 'y',
                'label': '% členů',
                'data': charts.total_spend_internal_referrer_breakdown.values()|list,
                'backgroundColor': '#638cdd',
            },
        ],
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'indexAxis': 'y',
        'interaction': {'mode': 'index'},
        'scales': {'y': {'beginAtZero': true}},
    }|tojson|forceescape }}"></canvas></div></div>
{% else %}
  {% call note() -%}
    {{ 'cloud-rain'|icon }} Graf je momentálně rozbitý.
  {%- endcall %}
{% endif %}
