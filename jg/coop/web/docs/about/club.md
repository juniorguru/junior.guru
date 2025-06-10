---
title: O klubu na junior.guru
template: main_about.html
---

{% from 'macros.html' import lead, note with context %}

# Vše o klubu

{% call lead() %}
Informace o [klubu pro juniory](../club.md). Záměr a hodnoty, se kterými je provozován. K tomu ještě pár zajímavých statistik.
{% endcall %}

[TOC]

## Vznik

Na junior.guru byla původně pouze příručka a pracovní nabídky. Placená komunita vznikla až v roce 2021. Honza tenkrát svou motivaci a veškeré okolnosti vzniku klubu otevřeně popsal v [rozsáhlém článku na svém blogu](https://honzajavorek.cz/blog/spoustim-klub/).

## Počet členů

Klub má teď **{{ members_total_count }} členů** celkem. Z nich si to **{{ charts.members_individuals_today }} platí ze svého**, tj. {{ charts.members_individuals_today_ptc|round|int }} %.

{% call note() %}
  {{ 'trash'|icon }} V létě 2024 se změnila metodika ukládání dat ohledně členství v klubu. Starší data bohužel nejsou k dispozici.
{% endcall %}

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="300"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts.members_labels,
        'datasets': [
            {
                'label': 'všechna členství',
                'data': charts.members,
                'borderColor': '#1755d1',
                'borderWidth': 2,
            },
            {
                'label': 'všechna individuální členství',
                'data': charts.members_individuals,
                'borderColor': '#1755d1',
                'borderWidth': 1,
            },
        ],
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'beginAtZero': true}},
        'plugins': {'annotation': charts.members_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

## Typy členství

Ke členství v klubu lze přijít různými způsoby. Každý nově příchozí má v klubu dva týdny zdarma na vyzkoušení. Někteří lidé dostávají vstup do klubu zdarma jako poděkování za dobrovolné příspěvky (takže to zdarma ani není), za přednášku v klubu, jako stipendium, nebo ze strategických důvodů. Část lidí je v klubu díky [sponzorům či partnerům](./sponsors-partners.md).

{% call note() %}
  {{ 'trash'|icon }} V létě 2024 se změnila metodika ukládání dat ohledně členství v klubu. Starší data bohužel nejsou k dispozici.
{% endcall %}

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="300"
    data-chart-type="bar"
    data-chart="{{ {
        'labels': charts.subscription_types_breakdown_labels,
        'datasets': [
            {
                'label': 'neplatí členství',
                'data': charts.subscription_types_breakdown.pop('free'),
                'backgroundColor': '#ddd',
            },
            {
                'label': 'dva týdny zdarma',
                'data': charts.subscription_types_breakdown.pop('trial'),
                'backgroundColor': '#a9a9a9',
            },
            {
                'label': 'mají stipendium',
                'data': charts.subscription_types_breakdown.pop('finaid'),
                'backgroundColor': '#02cabb',
            },
            {
                'label': 'členství zajistil partner',
                'data': charts.subscription_types_breakdown.pop('partner'),
                'backgroundColor': '#00b7eb',
            },
            {
                'label': 'členství platí firma',
                'data': charts.subscription_types_breakdown.pop('sponsor'),
                'backgroundColor': '#083284',
            },
            {
                'label': 'členství si platí sami, ročně',
                'data': charts.subscription_types_breakdown.pop('yearly'),
                'backgroundColor': '#638cdd',
            },
            {
                'label': 'členství si platí sami, měsíčně',
                'data': charts.subscription_types_breakdown.pop('monthly'),
                'backgroundColor': '#1755d1',
            },
        ],
    }|tojson|forceescape }}"
    {{ charts.subscription_types_breakdown.keys()|list|assert_empty }}
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'x': {'stacked': True}, 'y': {'stacked': True}},
        'plugins': {'annotation': charts.subscription_types_breakdown_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

## Počet znaků napsaných na Discordu

Aktivita na Discordu je sezónní. V létě se moc nepíše, v zimě se píše hodně. Celé je to ale pouze orientační metrika:

- V grafu není celá historie, data jsou jen za rok zpětně. Některé kanály se nezapočítávají. Nejde o kompletní _engagement_, protože lidi se mohou v klubu projevovat různě, např. reagováním pomocí emoji.
- Není správné sledovat a glorifikovat _engagement_, protože lidi mají z klubu úplně v pohodě hodnotu i pokud si jej pouze čtou. K tématu např. [Stop Measuring Community Engagement](https://rosie.land/posts/stop-measuring-community-engagement/).

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts.club_content_labels,
        'datasets': [
            {
                'label': 'počet znaků napsaných na Discordu',
                'data': charts.club_content,
                'borderColor': '#1755d1',
                'borderWidth': 2,
            },
        ]
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'beginAtZero': true}},
        'plugins': {'annotation': charts.club_content_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

## Počet online akcí v klubu

Bylo by fajn mít v klubu v průměru aspoň jednu [oficiální online akci](../events.md) měsíčně. Do grafu se nezapočítávají doplňkové akce, jako jsou například pravidelná Pondělní povídání.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts.events_labels,
        'datasets': [
            {
                'label': 'počet oficiálních akcí',
                'data': charts.events,
                'borderColor': '#1755d1',
                'borderWidth': 2,
            },
            {
                'label': 'počet oficiálních akcí TTM/12',
                'data': charts.events_ttm,
                'borderColor': '#1755d1',
                'borderWidth': 1,
            },
        ]
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'beginAtZero': true}},
        'plugins': {'annotation': charts.events_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

## Konverze dvou týdnů na zkoušku

Nově registrovaní mají v klubu dva týdny zdarma na zkoušku, tzv. _trial_.
Jejich členství není nijak omezeno, mohou dělat všechno, co ostatní členové.
Po dvou týdnech buď vyplní kartu a začnou platit, nebo je jim členství zrušeno.
Graf ukazuje konverzi _trialů_.

{% call note() %}
  {{ 'trash'|icon }} V létě 2024 se změnila metodika ukládání dat ohledně členství v klubu. Starší data bohužel nejsou k dispozici.
{% endcall %}

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts.trials_conversion_labels,
        'datasets': [
            {
                'label': '% konverze trialu',
                'data': charts.trials_conversion,
                'borderColor': '#1755d1',
                'borderWidth': 2,
            },
        ]
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'beginAtZero': true}},
        'plugins': {'annotation': charts.trials_conversion_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

## Příchody a odchody

Graf s **příchody** ukazuje počet členů, kteří v daném měsíci přešli na individuální placení. Graf s **odchody** ukazuje počet členů, kteří už za klub něco ze svého zaplatili a v daném měsíci platit přestali.

{% call note() %}
  {{ 'trash'|icon }} V létě 2024 se změnila metodika ukládání dat ohledně členství v klubu. Starší data bohužel nejsou k dispozici.
{% endcall %}

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts.signups_labels,
        'datasets': [
            {
                'label': 'nová individuální členství',
                'data': charts.signups,
                'borderColor': '#1755d1',
                'borderWidth': 2,
            },
            {
                'label': 'odchody individuálních členů',
                'data': charts.quits,
                'borderColor': '#dc3545',
                'borderWidth': 2,
            },
        ]
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'beginAtZero': true}},
        'plugins': {'annotation': charts.signups_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

## Retence klubu

Procento členů, kteří si klub platí ze svého a odcházejí, neboli _churn_.

{% call note() %}
  {{ 'trash'|icon }} V létě 2024 se změnila metodika ukládání dat ohledně členství v klubu. Starší data bohužel nejsou k dispozici.
{% endcall %}

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts.churn_labels,
        'datasets': [
            {
                'label': '% úbytku individuálních členů',
                'data': charts.churn,
                'borderColor': '#dc3545',
                'borderWidth': 2,
            },
        ]
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'beginAtZero': true}},
        'plugins': {'annotation': charts.churn_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

## Důvody odchodu

Když někdo ukončuje členství v klubu, může sdělit důvod, proč tak činí.
Data jsou celkem od **{{ charts.cancellations_breakdown_count }}** lidí.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="300"
    data-chart-type="bar"
    data-chart="{{ {
        'labels': charts.cancellations_breakdown_labels,
        'datasets': [
            {
                'label': '% neudali důvod',
                'data': charts.cancellations_breakdown.pop('unknown'),
                'backgroundColor': '#ddd',
            },
            {
                'label': '% jiný důvod',
                'data': charts.cancellations_breakdown.pop('other'),
                'backgroundColor': '#a9a9a9',
            },
            {
                'label': '% klub už nepotřebuju',
                'data': charts.cancellations_breakdown.pop('necessity'),
                'backgroundColor': '#1755d1',
            },
            {
                'label': '% potřeboval(a) jsem klub na omezenou dobu',
                'data': charts.cancellations_breakdown.pop('temporary_use'),
                'backgroundColor': '#02cabb',
            },
            {
                'label': '% vybral(a) jsem jinou službu, která mi vyhovuje víc',
                'data': charts.cancellations_breakdown.pop('competition'),
                'backgroundColor': '#083284',
            },
            {
                'label': '% klub nesplnil moje očekávání',
                'data': charts.cancellations_breakdown.pop('misunderstood'),
                'backgroundColor': '#00b7eb',
            },
            {
                'label': '% klub je moc drahý',
                'data': charts.cancellations_breakdown.pop('affordability'),
                'backgroundColor': '#dc3545',
            },
        ],
    }|tojson|forceescape }}"
    {{ charts.cancellations_breakdown.keys()|list|assert_empty }}
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'x': {'stacked': True}, 'y': {'stacked': True, 'beginAtZero': true, 'max': 100}},
        'plugins': {'annotation': charts.cancellations_breakdown_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

## Důvody odchodu za celou historii

Celkový poměr důvodů odchodu za celou historii, po kterou se sbírá tento typ zpětné vazby.
Data jsou celkem od **{{ charts.total_cancellations_breakdown_count }}** lidí.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="pie"
    data-chart="{{ {
        'labels': {
            'unknown': '% neudali důvod',
            'other': '% jiný důvod',
            'necessity': '% klub už nepotřebuju',
            'temporary_use': '% potřeboval(a) jsem klub na omezenou dobu',
            'competition': '% vybral(a) jsem jinou službu, která mi vyhovuje víc',
            'misunderstood': '% klub nesplnil moje očekávání',
            'affordability': '% klub je moc drahý',
        }|mapping(charts.total_cancellations_breakdown.keys()),
        'datasets': [
            {
                'data': charts.total_cancellations_breakdown.values()|list,
                'backgroundColor': {
                    'unknown': '#ddd',
                    'other': '#a9a9a9',
                    'necessity': '#1755d1',
                    'temporary_use': '#02cabb',
                    'competition': '#083284',
                    'misunderstood': '#00b7eb',
                    'affordability': '#dc3545',
                }|mapping(charts.total_cancellations_breakdown.keys())
            },
        ],
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'scales': None,
        'aspectRatio': 2,
    }|tojson|forceescape }}"
    data-chart-milestones-offset-ptc="0"></canvas></div></div>
