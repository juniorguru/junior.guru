---
title: O klubu na junior.guru
template: main_about.html
---

{% from 'macros.html' import lead, note with context %}

# Vše o klubu

{% call lead() %}
Informace o [klubu pro juniory](../club.md). Záměr a hodnoty, se kterými je provozován. K tomu ještě pár zajímavých statistik.
{% endcall %}

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }} Tady něco teprve bude.
{% endcall %}

## Počet členů

Klub má teď **{{ members_total_count }} členů** celkem. Z nich si to **{{ charts.members_individuals[-1] }} platí ze svého**.

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

- V grafu není celá historie, data jsou jen za rok zpětně. Některé kanály se nezapočítávají, např. „volná zábava“. Nejde o kompletní _engagement_, protože lidi se mohou v klubu projevovat různě, např. reagováním pomocí emoji.
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

## Odkud jsou platící členové

O členech junior.guru neuchovává žádné informace, ze kterých by šlo zjistit, odkud jsou.
Platební systém Stripe ale umožňuje zjistit, v jaké zemi byla vydána jejich karta.
Díky tomu lze odhadnout, kolik lidí není z Česka.

Honza to potřebuje sledovat, aby věděl, jestli nepřesáhl limit pro [One Stop Shop](https://vat-one-stop-shop.ec.europa.eu/one-stop-shop/declare-and-pay-oss_en). Ten je {{ charts.countries.oss_limit_eur|thousands }}€/rok, což je {{ charts.countries.oss_limit_czk|thousands }} Kč/rok, což je {{ charts.countries.oss_limit_czk_monthly|thousands }}/měsíc.

Z individuálních členství minulý měsíc vydělal {{ charts.countries.revenue_memberships|thousands }} Kč celkem.
Když se použijí procenta z grafu níže, odhadem by mělo být {{ charts.countries.revenue_memberships_non_cz|thousands }} Kč odjinud než z Česka. {% if charts.countries.oss_limit_czk_monthly > charts.countries.revenue_memberships_non_cz %}**Takže asi dobrý.**{% endif %}

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="bar"
    data-chart="{{ {
        'labels': [
            'Česko',
            'Slovensko',
            'jinde',
        ],
        'datasets': [
            {
                'axis': 'y',
                'label': '% členů',
                'data': [
                    charts.countries.breakdown.pop('CZ'),
                    charts.countries.breakdown.pop('SK'),
                    charts.countries.breakdown.pop('other'),
                ],
                'backgroundColor': '#1755d1',
            },
        ],
    }|tojson|forceescape }}"
    {{ charts.countries.breakdown.keys()|list|assert_empty }}
    data-chart-options="{{ {
        'indexAxis': 'y',
        'interaction': {'mode': 'index'},
        'scales': {'y': {'min': 0, 'suggestedMax': 100}},
    }|tojson|forceescape }}"></canvas></div></div>
