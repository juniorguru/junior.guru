---
title: O provozovateli junior.guru
template: main_about.html
---

{% from 'macros.html' import contact, lead with context %}

# Provozovatel

{% call lead() %}
Celé junior.guru vytváří a provozuje jediný člověk, programátor jménem Honza Javorek.
S některými úkoly mu pomáhá tým dobrovolníků a kontraktorů.
{% endcall %}

[TOC]

## Kontakt

{{ contact() }}

## Kdo je Honza

Projekt provozuje **Honza Javorek**, obyčejný programátor. Více se o něm dovíš na jeho [osobním webu](https://honzajavorek.cz) nebo na [LinkedIn](https://www.linkedin.com/in/honzajavorek/). Původně je z Karviné, dlouho bydlel v Brně, teď žije v Praze.

Díky dobrovolným aktivitám se dostal k pomáhání začátečníkům, a to ho hodně bavilo. Časem mu přišlo, že chybí jedno místo, kde by byly všechny pracovní nabídky pro juniory, nezávislé informace a základní praktické rady.

V roce 2019 odešel z korporátu a založil tento projekt. Provozuje jej jako podnikatel na volné noze bez ambice rozjíždět firmu. Cílem je vydělat si tak akorát, aby se dobře žilo jeho rodině.

<p class="text-center">
  <a href="{{ pages|docs_url("love.jinja")|url }}" class="love-button pulse">{{ 'heart-fill'|icon }} Pošli LOVE</a>
</p>

## Týdenní poznámky

Od května 2020 Honza píše na svůj osobní blog týdenní poznámky, ve kterých popisuje, jak maká na junior.guru.
Pomáhá mu to s páteční psychikou a zároveň si u toho uspořádá myšlenky.
Tady je posledních pět článků:

{% for blog_article in blog[:5] %}
-   [{{ blog_article.title }}]({{ blog_article.url }}), {{ '{:%-d.%-m.%Y}'.format(blog_article.published_on) }}
{% endfor %}

## Tým pomocníků

Je pouhou iluzí, že by šlo celé junior.guru dělat v jednom člověku. Tady jsou všichni, kteří se nějakou větší měrou podílí, nebo historicky podíleli na úspěchu projektu – ať už jde o dobrovolníky, nebo kontraktory.

<table class="table">
  <tr>
    <td><a href="https://coreskill.tech/">Dan Srb</a></td>
    <td>moderování klubu a rady kolem CVček</td>
  </tr>
  <tr>
    <td><a href="https://www.linkedin.com/in/veronika-%C4%8Damborov%C3%A1/">Veronika Čamborová</a></td>
    <td>moderování klubu</td>
  </tr>
  <tr>
    <td><a href="https://www.linkedin.com/in/berankova-pavla/">Pavla Beránková</a></td>
    <td>moderování klubu</td>
  </tr>
  <tr>
    <td><a href="https://nelaprovazi.cz/">Nela
        Slezáková</a></td>
    <td>moderování klubu a klubová psycholožka</td>
  </tr>
  <tr>
    <td><a href="https://www.linkedin.com/in/fusatytata/">Šimon Kořený</a></td>
    <td>moderování klubu a vítání klubových nováčků</td>
  </tr>
  <tr>
    <td><a href="https://www.linkedin.com/in/t%C3%A1%C5%88a-v%C3%A1chov%C3%A1-512981330/">Táňa Váchová</a></td>
    <td>virtuální asistentka – produkce online akcí, rozhovorů, aj.</td>
  </tr>
  <tr>
    <td>Tinuki</td>
    <td>produkce videozáznamů</td>
  </tr>
  <tr>
    <td><a href="https://www.linkedin.com/in/patrik-brnusak-cz/">Patrik Brnušák</a></td>
    <td>produkce videozáznamů</td>
  </tr>
  <tr>
    <td><a href="https://www.linkedin.com/in/pavlinafronkova/">Pavlína Froňková</a></td>
    <td>produkce podcastu</td>
  </tr>
  <tr>
    <td>Radka Slezáčková</td>
    <td>vítání klubových nováčků</td>
  </tr>
  <tr>
    <td><a href="https://www.linkedin.com/in/tom%C3%A1%C5%A1-k%C3%A1ra-81b2111a1/">Tomáš Kára</a></td>
    <td>vítání klubových nováčků</td>
  </tr>
  <tr>
    <td><a href="https://geekpower.cz/">Veronika Rychlá</a>
    </td>
    <td>výuka angličtiny v klubu</td>
  </tr>
  <tr>
    <td>Vítězslav Irein</td>
    <td>účetnictví</td>
  </tr>
  <tr>
    <td><a href="http://popitchimentoring.cz">Terézia Palaščáková</a></td>
    <td>copywriting a marketingové konzultace</td>
  </tr>
  <tr>
    <td><a href="https://www.linkedin.com/in/dolejsovajana/">Jana Dolejšová</a></td>
    <td>marketingové konzultace</td>
  </tr>
  <tr>
    <td><a href="https://www.linkedin.com/in/adelapavlun/">Adéla Pavlun</a></td>
    <td>produkce rozhovorů</td>
  </tr>
  <tr>
    <td><a href="https://www.obrjen.net/">Anna Obrjen</a>
    </td>
    <td>právní služby</td>
  </tr>
</table>
