---
title: O příručce na junior.guru
template: main_about.html
---

{% from 'macros.html' import lead, note with context %}

# Vše o příručce

{% call lead() %}
Informace a čísla o [příručce pro juniory](handbook/index.md).
{% endcall %}

[TOC]

## Počty impresí

Pokud si sponzor [zaplatí nejvyšší tarif](../love.jinja), má logo na příručce.
Hodí se vědět, kolikrát se takové logo lidem zobrazí.

<figure class="figure"><div class="chart-figure"><canvas
    class="chart" width="400" height="230"
    data-chart-type="bar"
    data-chart="{{ {
        'labels': {
            'home': 'úvodní stránka',
            'courses': 'katalog kurzů',
            'handbook': 'příručka',
        }|mapping(charts.logo_impressions_breakdown.keys()),
        'datasets': [
            {
                'label': 'průměrný počet impresí měsíčně',
                'data': charts.logo_impressions_breakdown.values()|list,
                'backgroundColor': '#1755d1',
            },
        ],
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'beginAtZero': true}},
    }|tojson|forceescape }}"></canvas></div></figure>

## Práce na příručce

Všechny soubory spadající pod příručku mají aktuálně **{{ handbook_total_size|thousands }}** znaků.
Počítání znaků v souborech, kde se míchají Markdown a Jinja značky, má spoustu vad, ale aspoň něco.
[Podle Wikipedie](https://cs.wikipedia.org/wiki/Diplomov%C3%A1_pr%C3%A1ce) je 180.000 znaků doporučovaná velikost disertační práce (titul Ph.D.).

Když chce Honza na nějaké stránce něco doplnit, dělá si na jejím konci HTML komentář a do něj si ukládá nepříliš strukturované poznámky.
Ty se taky započítají do celkové velikosti, ale v grafu je jejich velikost zobrazena šedě, aby šlo vidět, jaký je poměr a kde ještě čeká kolik práce.

Příliš velké stránky bych měly být kratší, nebo by se měly rozdělit do více menších.
Ideální stránka příručky by měla pouze modrý sloupeček a ten by nesahal výše než k červené čáře.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="300"
    data-chart-type="bar"
    data-chart="{{ {
        'labels': charts.handbook_labels,
        'datasets': [
            {
                'label': 'znaků TODO',
                'data': charts.handbook_notes,
                'backgroundColor': '#a9a9a9',
            },
            {
                'label': 'znaků obsahu',
                'data': charts.handbook,
                'backgroundColor': '#1755d1',
            },
        ],
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'x': {'stacked': true}},
        'plugins': {
            'annotation': {
                'common': {'drawTime': 'beforeDatasetsDraw'},
                'annotations': {
                    'threshold': {
                        'value': 20000,
                        'scaleID': 'y',
                        'type': 'line',
                        'borderColor': '#dc3545',
                        'borderWidth': 1,
                    }
                },
            }
        },
    }|tojson|forceescape }}"
    data-chart-milestones-offset-ptc="0"></canvas></div></div>
