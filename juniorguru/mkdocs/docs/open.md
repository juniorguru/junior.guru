---
title: Jak se daří provozovat junior.guru?
template: main.html
description: Čísla, statistiky, grafy. Jak se Honzovi daří provozovat junior.guru?
---

<canvas
    class="chart" width="400" height="200"
    data-chart-type="line"

    {% set chart = {
        'labels': charts_ranges.today|map('string')|list,
        'datasets': [
            {
                'label': 'příjmy',
                'data': charts_ranges.today|map_function(transactions.revenue_monthly),
                'borderColor': '#1755d1',
                'borderWidth': 2,
            },
            {
                'label': 'výdaje',
                'data': charts_ranges.today|map_function(transactions.cost_monthly),
                'borderColor': '#DA3C6C',
                'borderWidth': 2,
            },
            {
                'label': 'MRR',
                'data': charts_ranges.today|map_function(transactions.recurring_revenue_monthly),
                'borderColor': '#6ED79F',
                'borderWidth': 2,
            }
        ]
    } %}
    data-chart="{{ chart|tojson|forceescape }}"
>
</canvas>


{#
        return {
            'labels': [f'{data_point:%Y-%m-%d}' for data_point in data_points],
            'datasets': {
                'revenue': ,
            },
        }
        return {
            'labels': labels,
            'datasets': [{
                'label': 'blabla',
                'data': data,
                'borderColor': '#1755d1',
                'borderWidth': 3
            }]
        }
#}

- Revenue/mo {{ transactions.revenue_monthly() }}
- MRR {{ transactions.recurring_revenue_monthly() }}
- Profit/mo {{ transactions.profit_monthly() }}

Příjmy

```
{{ transactions.incomes_breakdown()|pprint }}
```

```
{{ transactions.incomes_breakdown()|money_breakdown_ptc|pprint }}
```

```
{{ transactions.incomes_breakdown()|money_breakdown_ptc|incomes|pprint }}
```

Výdaje

```
{{ transactions.expenses_breakdown()|pprint }}
```
