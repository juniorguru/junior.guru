---
title: Jak se daří provozovat junior.guru
description: Čísla, statistiky, grafy. Jak se Honzovi daří provozovat junior.guru?
template: main_about.html
---

{% from 'macros.html' import lead with context %}

# Vše o projektu

{% call lead() %}
Jmenuji se Honza Javorek a provozuji junior.guru. Tuto stránku jsem vytvořil po vzoru [jiných otevřených projektů](https://openstartuplist.com/). Čísla a grafy stejně potřebuji pro svou vlastní potřebu, takže proč je v rámci transparentnosti nemít rovnou na webu, že?
{% endcall %}

## Týdenní poznámky

Od května 2020 píšu na svůj osobní blog týdenní poznámky, ve kterých popisuji, jak makám na junior.guru.
Pomáhá mi to s páteční psychikou a zároveň si u toho uspořádám myšlenky.
Tady je posledních pět článků:

{% for blog_article in blog[:5] %}
-   [{{ blog_article.title }}]({{ blog_article.url }}), {{ '{:%-d.%-m.%Y}'.format(blog_article.published_on) }}
{% endfor %}
