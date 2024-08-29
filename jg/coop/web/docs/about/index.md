---
title: Vše o junior.guru
description: Čísla, statistiky, grafy, kontext. Jak se Honzovi daří provozovat junior.guru?
template: main_about.html
---

{% from 'macros.html' import lead, note with context %}

# Vše o projektu

{% call lead() %}
Projekt junior.guru provozuje Honza Javorek.
Čísla a grafy stejně potřebuje pro svou potřebu, takže proč je v rámci transparentnosti nemít rovnou na webu, že?
{% endcall %}

[TOC]

## Kontakt

Junior Guru, stylizovaně „junior.guru“<br>
**Jan Javorek**<br>
fyzická osoba podnikající dle živnostenského zákona nezapsaná v obchodním rejstříku<br>
se sídlem Lupáčova 375/24, 130 00 Praha<br>
IČO: [74279858](https://ares.gov.cz/ekonomicke-subjekty?ico=74279858),<br>
neplátce DPH,<br>
E-mail: [honza@junior.guru](mailto:honza@junior.guru)<br>

## Provozovatel

Projekt provozuje **Honza Javorek**, obyčejný programátor. Více se o něm dovíš na jeho [osobním webu](https://honzajavorek.cz) nebo na [LinkedIn](https://www.linkedin.com/in/honzajavorek/). Původně je z Karviné, dlouho bydlel v Brně, teď žije v Praze.

Díky dobrovolným aktivitám se dostal k pomáhání začátečníkům, a to ho hodně bavilo. Časem mu přišlo, že chybí jedno místo, kde by byly všechny pracovní nabídky pro juniory, nezávislé informace a základní praktické rady.

V roce 2019 odešel z korporátu a založil tento projekt. Provozuje jej jako podnikatel na volné noze bez ambice rozjíždět firmu. Cílem je vydělat si tak akorát, aby se dobře žilo jeho rodině.

<p class="text-center">
  <a href="{{ pages|docs_url("love.jinja")|url }}" class="love-button pulse">Pošli LOVE</a>
</p>

## Týdenní poznámky

Od května 2020 Honza píše na svůj osobní blog týdenní poznámky, ve kterých popisuje, jak maká na junior.guru.
Pomáhá mu to s páteční psychikou a zároveň si u toho uspořádá myšlenky.
Tady je posledních pět článků:

{% for blog_article in blog[:5] %}
-   [{{ blog_article.title }}]({{ blog_article.url }}), {{ '{:%-d.%-m.%Y}'.format(blog_article.published_on) }}
{% endfor %}

## Tým

Je pouhou iluzí, že by šlo celé junior.guru dělat v jednom člověku. Tady jsou všichni, kteří se nějakou větší měrou podílí na úspěchu projektu – ať už jde o dobrovolníky, nebo kontraktory.

<table class="table">
  <tr>
    <td><a href="https://coreskill.tech/">Dan Srb</a></td>
    <td>moderování klubu a rady kolem CVček</td>
  </tr>
  <tr>
    <td><a href="https://www.linkedin.com/in/miloslav-jezek/">Miloslav Ježek</a></td>
    <td>moderování klubu a hybná síla za klubovými aktivitami</td>
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
    <td><a href="https://www.linkedin.com/in/madrvojtech/">Vojta Mádr</a></td>
    <td>moderování klubu</td>
  </tr>
  <tr>
    <td><a href="https://www.linkedin.com/in/patrik-brnusak-cz/">Patrik Brnušák</a></td>
    <td>produkce video záznamů</td>
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
    <td><a href="https://www.linkedin.com/in/fusatytata/">Šimon Kořený</a></td>
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
    <td><a href="https://www.linkedin.com/in/lonikroman/">Roman Loník</a></td>
    <td>hybná síla za klubovými aktivitami kolem projektového učení</td>
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

## Mise

Cílem junior.guru je, aby co nejvíc lidí v Česku a na Slovensku mělo příležitost naučit se programovat.
Aby každý Luďan z Mostu, každá puberťačka, každý vědec nebo každá máma na rodičovské měli po ruce návod, jak s tím začít.

A je jedno, jestli chtějí programovat pro zábavu, plánují si něco automatizovat, nebo touží po kariéře v IT.
Jestli jsou z velkého města s širokými možnostmi, nebo z odlehlé vesnice.
Jestli jsou žena, muž, stará, mladý.
Jestli mají kůži růžovou nebo hnědou.

Když zjistí, že i jako samouci si mohou sehnat práci v oboru, je smyslem junior.guru zajistit, aby jejich cesta nebyla past vedle pasti.
Aby k tomu měli kultivovanou podpůrnou komunitu, kde budou vítaní a mezi svými.
Aby měli nezávislé informace o poskytovatelích kurzů a aby se mohli snadno propojit s firmami, kam by mohli nastoupit.

Bez keců o tom, jak firmy berou každého, peníze se budou jen sypat, a programovat se naučí za měsíc.
Na junior.guru se doví, co doopravdy očekávat, aby se na to mohli adekvátně připravit.

## Hodnoty

Toto jsou hlavní hodnoty, které se snaží Honza vtisknout do DNA klubu pro juniory a celého junior.guru:

- **Porozumění:** Máme empatii. Víme, že cesta juniora je těžká, chápeme tvou situaci. Než odpovídáme, tak se ptáme na kontext. Než něco vytvoříme, tak se zamyslíme nad tím, jak se to bude používat nejen v Praze, ale i v Karviné. Jak to bude vyhovovat nejen klukům, ale i holkám…
- **Otevřenost:** Lidi mohou Honzovi koukat pod ruce, aby měli důvěru v to, co dělá a proč to dělá. Veřejné jsou [finanční výsledky](./finances.md), [motivace sponzorů](./sponsors-partners.md), [metriky klubu](./club.md). [Otevřené](https://cs.wikipedia.org/wiki/Otev%C5%99en%C3%BD_software) jsou ale i licence textů či veškerého kódu. Otevřené je i know-how ohledně toho, jak to všechno vzniká.
- **Rovnost:** Tykáme si. Nerozlišujeme, kdo je junior a kdo senior, jestli je někdo muž, nebo žena, jestli je LGBT+, nebo na mateřské. Platí rovnost před [pravidly](../coc.md). Když Honza udělá něco špatně, tak i on se omluví.
- **Upřímnost:** Na nic si nehrajem. Jsme jenom lidi a jsme, jací jsme. Máme chyby a nebojíme se je přiznat. O realitě na trhu práce se bavíme bez růžových brýli, neslibujeme si hory doly a upozorňujeme na výzvy, které na cestě čekají. Honza se snaží podnikat tak, aby při tom nikoho nezneužíval a nepodílel na ničem neetickém.
- **Škálovatelnost:** Honza nerozprodává své hodiny na 1:1 konzultace, ale vytváří a rozvíjí platformu, která v dostatečně dobré kvalitě pomůže velkému množství lidí. Neprovozujeme kurzy a neučíme lidi programovat, ale snažíme se pomocí junior.guru pokrýt veškerý ostatní servis, který je k úspěšné rekvalifikaci potřeba. Honza neorganizuje srazy a nevytváří obsah, ale dělá kurátora, který upozorňuje na to dobré, co už existuje.
- **Pro juniory:** I přes různá firemní partnerství je junior.guru službou především pro juniory. Ti na trhu tahají za kratší konec provazu a toto je jedno z mála míst, kde jejich zájem dostává vždy přednost.

## Logo a barvy

Všechno by mělo být na [logo.junior.guru](https://logo.junior.guru/), ale už dlouho to nebylo aktualizované, takže raději napište e-mail.
