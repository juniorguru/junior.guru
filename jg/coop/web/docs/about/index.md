---
title: Vše o junior.guru
description: Čísla, statistiky, grafy, kontext. Jak se Honzovi daří provozovat junior.guru?
template: main_about.html
---

{% from 'macros.html' import lead, markdown with context %}

# Vše o projektu

{% call lead() %}
Čísla a grafy jsou pro provoz junior.guru stejně potřeba, takže proč je v rámci transparentnosti nemít rovnou na webu, že?
{% endcall %}

<div class="standout-top"><div class="topics topics-grid">
{% call markdown() %}
- [{{ 'person-circle'|icon }} Kdo tvoří junior.guru](./contact.md)
- [{{ 'currency-exchange'|icon }} Finanční výsledky](./finances.md)
- [{{ 'people-fill'|icon }} Klubové statistiky](./club.md)
- [{{ 'gift-fill'|icon }} Sponzoři a partneři](./sponsors-partners.md)
- [{{ 'bar-chart-line-fill'|icon }} Návštěvnost webu](./web-usage.md)
- [{{ 'person-standing-dress'|icon }} Podpora žen v IT](./women.md)
{% endcall %}
</div></div>
