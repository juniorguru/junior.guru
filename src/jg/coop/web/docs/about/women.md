---
title: Jak junior.guru podporuje ženy v IT
template: main_about.html
---

{% from 'macros.html' import lead, note with context %}

# Podpora žen v IT

{% call lead() %}
Od svého vzniku je junior.guru pevně spjato s podporou žen v IT. Bez [PyLadies](https://pyladies.cz/) by tento projekt ani nevznikl. Následující grafy měří zastoupení žen ve všem, co junior.guru dělá, aby šlo ověřovat, jak si v této věci projekt reálně vede.
{% endcall %}

[TOC]

## Kontext

Podle [analýz ČSÚ](https://csu.gov.cz/produkty/ict-specialistky-berou-o-16-tisic-mene-nez-muzi) je v českém IT dlouhodobě pouze 10 % žen. Tento podíl se od [roku 2018](https://csu.gov.cz/rychle-informace/ict-odbornici-v-ceske-republice-a-jejich-mzdy-2018) nijak nezlepšil, naopak nás postupně předběhly úplně všechny ostatní státy v Evropě, takže jsme poslední a nejhorší.

## Vedlejší aktivity

Nad rámec toho, co by bylo nutné, spolupracuje junior.guru aktivně s PyLadies, Czechitas, ReactGirls, nebo CyberLadies. V letech 2021–2022 vyšlo v online vydání časopisu Heroine [pět článků](https://www.heroine.cz/clanky/autor/70000223-honza-javorek) založených na radách z junior.guru.

## Metodika měření

Nejde o žádnou přesnou metriku. Nikdo nikde nevyplňuje, zda je žena. Pro účely statistik se to určuje jen odhadem podle křestního jména a tvaru příjmení.

## Podíl žen v klubu

Graf zobrazuje procentuální podíl žen na počtu členů [klubu](../club.md). Aktuálně je to **{{ charts.members_women_today|round|int }} %**.

{% call note() %}
  {{ 'trash'|icon }} V létě 2024 se změnila metodika ukládání dat ohledně členství v klubu. Starší data bohužel nejsou k dispozici.
{% endcall %}

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts.members_women_labels,
        'datasets': [
            {
                'label': '% žen v klubu',
                'data': charts.members_women,
                'borderColor': '#dc3545',
                'borderWidth': 2,
            },
        ]
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'min': 0, 'suggestedMax': 50}},
        'plugins': {'annotation': charts.members_women_annotations},
    }|tojson|forceescape }}"
    data-chart-milestones-offset-ptc="0"></canvas></div></div>

## Podíl žen mezi přednášejícími

Graf zobrazuje procentuální podíl žen na počtu [přednášejících](../events.md) za posledních 12 měsíců (TTM, _trailing twelve months_).

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts.events_women_labels,
        'datasets': [
            {
                'label': '% přednášejících žen TTM',
                'data': charts.events_women,
                'borderColor': '#dc3545',
                'borderWidth': 2,
            },
        ]
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'min': 0, 'suggestedMax': 50}},
    }|tojson|forceescape }}"></canvas></div></div>

## Podíl žen mezi hosty podcastu

Graf zobrazuje procentuální podíl žen na počtu hostů [podcastu](../podcast.md) za posledních 12 měsíců (TTM, _trailing twelve months_).

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts.podcast_women_labels,
        'datasets': [
            {
                'label': '% žen v podcastu TTM',
                'data': charts.podcast_women,
                'borderColor': '#dc3545',
                'borderWidth': 2,
            },
        ]
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'min': 0, 'suggestedMax': 50}},
    }|tojson|forceescape }}"></canvas></div></div>
