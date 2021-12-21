---
title: Jak se daří provozovat junior.guru?
template: main.html
description: Čísla, statistiky, grafy. Jak se Honzovi daří provozovat junior.guru?
---

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
