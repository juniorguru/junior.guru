---
title: Jak se daří provozovat junior.guru?
template: main.html
description: Čísla, statistiky, grafy. Jak se Honzovi daří provozovat junior.guru?
---

- Aktuální čistý zisk: {{ profit_ttm|thousands }} Kč měsíčně

<div class="progress">
    {% set progress_max = 40000 %}
    {% set progress_ptc = ((profit_ttm * 100) / progress_max)|round|int %}
    <div class="progress-bar" role="progressbar" style="width: {{ progress_ptc }}%" aria-valuenow="{{ progress_ptc }}" aria-valuemin="0" aria-valuemax="{{ progress_max }}">
    {{ progress_ptc }} % ze {{ progress_max|thousands }} Kč
    </div>
</div>

<canvas
    class="chart" width="400" height="200"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts_labels,
        'datasets': [
            {
                'label': 'výnosy',
                'data': charts_revenue,
                'borderColor': '#1755d1',
                'borderWidth': 2,
            },
            {
                'label': 'výnosy TTM/12',
                'data': charts_revenue_ttm,
                'borderColor': '#1755d1',
                'borderWidth': 1,
            },
            {
                'label': 'náklady',
                'data': charts_cost,
                'borderColor': '#dc3545',
                'borderWidth': 2,
            },
            {
                'label': 'náklady TTM/12',
                'data': charts_cost_ttm,
                'borderColor': '#dc3545',
                'borderWidth': 1,
            },
        ]
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'}
    }|tojson|forceescape }}"></canvas>

<canvas
    class="chart" width="400" height="200"
    data-chart-type="bar"
    data-chart="{{ {
        'labels': charts_labels,
        'datasets': [
            {
                'label': 'dobrovolné příspěvky',
                'data': charts_revenue_breakdown.pop('donations'),
                'backgroundColor': '#02CABB',
            },
            {
                'label': 'individuální členství',
                'data': charts_revenue_breakdown.pop('memberships'),
                'backgroundColor': '#1755d1',
            },
            {
                'label': 'firemní členství',
                'data': charts_revenue_breakdown.pop('partnerships'),
                'backgroundColor': '#638CDD',
            },
            {
                'label': 'inzerce nabídek práce ',
                'data': charts_revenue_breakdown.pop('jobs'),
                'backgroundColor': '#421BD4',
            },
        ],
    }|tojson|forceescape }}"
    {{ charts_revenue_breakdown.keys()|list|assert_empty }}
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'x': {'stacked': True}, 'y': {'stacked': True}}
    }|tojson|forceescape }}"></canvas>

<canvas
    class="chart" width="400" height="200"
    data-chart-type="bar"
    data-chart="{{ {
        'labels': charts_labels,
        'datasets': [
            {
                'label': 'daně a pojištění',
                'data': charts_cost_breakdown.pop('tax'),
                'backgroundColor': '#ddd',
            },
            {
                'label': 'různé',
                'data': charts_cost_breakdown.pop('miscellaneous'),
                'backgroundColor': '#dc3545',
            },
            {
                'label': 'právnička',
                'data': charts_cost_breakdown.pop('lawyer'),
                'backgroundColor': '#801515',
            },
            {
                'label': 'marketing',
                'data': charts_cost_breakdown.pop('marketing'),
                'backgroundColor': '#550000',
            },
            {
                'label': 'memberful.com',
                'data': charts_cost_breakdown.pop('memberful'),
                'backgroundColor': '#EF704F',
            },
            {
                'label': 'discord.com',
                'data': charts_cost_breakdown.pop('discord'),
                'backgroundColor': '#5865f2',
            },
        ],
    }|tojson|forceescape }}"
    {{ charts_cost_breakdown.keys()|list|assert_empty }}
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'x': {'stacked': True}, 'y': {'stacked': True}}
    }|tojson|forceescape }}"></canvas>

https://simpleanalytics.com/junior.guru
