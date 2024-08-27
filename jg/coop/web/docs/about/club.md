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
