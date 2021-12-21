---
title: Jak se daří provozovat junior.guru?
thumbnail_badge: 109 Kč/měs
template: main.html
description: Čísla, statistiky, grafy. Jak se Honzovi daří provozovat junior.guru?
---

Příjmy

```
{{ incomes_breakdown|pprint }}
```

```
{{ incomes_breakdown|money_breakdown_ptc|pprint }}
```

```
{{ incomes_breakdown|money_breakdown_ptc|incomes|pprint }}
```

Výdaje

```
{{ expenses_breakdown|pprint }}
```
