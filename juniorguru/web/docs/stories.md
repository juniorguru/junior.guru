---
title: Inspirativní příběhy
description: Příběhy těch, kdo se rekvalifikovali do IT, nebo jim nějak programování pomáhá
---

{% from 'macros.html' import lead, link_card, blockquote_avatar, news_card, note with context %}

<nav aria-label="breadcrumb">
  <ol class="breadcrumb">
    <li class="breadcrumb-item">
      <a href="{{ (page|parent_page).url|url }}">
        {{ (page|parent_page).title }}
      </a>
    </li>
    <li class="breadcrumb-item active" aria-current="page">
      Příběhy
    </li>
  </ol>
</nav>

# Příběhy

{% call lead() %}
Inspirativní příbehy lidí jako ty, kteří se bez předchozí znalosti naučili programovat, programování jim v něčem pomohlo, nebo si v IT dokonce našli i práci.
{% endcall %}

## Nesrovnávej se!

Jako **inspirace a motivace** jsou příběhy fajn.
A je důležité, abychom je měli.
Když malá holka uvidí úspěšné vědkyně a programátorky, nenechá si namluvit, že holky do IT nepatří.
Když si Rom všimne, že jinému se povedlo programování vystudovat, nebude mu už hlas v hlavě říkat: „Ty na to nemáš, žádný jiný Rom to nedokázal“.
To samé horník, když ve filmu uvidí [Tomáše Hisema](#z-hornika-programatorem).

Snadno se však může stát, že se s příběhy začneš **srovnávat**.
Nedělej to, pro tvou psychiku je to strašně nezdravé.
**Srovnávej se pouze se sebou a svými předešlými výkony.**

Úkolem příběhů není ukázat, že všichni to budou mít takto snadné, ale zafungovat jako vzor, že něco jde.
Že pro určitou skupinu lidí není vyloučeno něco dokázat, a že existují různé cesty, jak k tomu dojít.

Většině příběhů ale chybí informace o tom, co proběhlo v zákulisí.
Někdo se čtyřmi dětmi změní kariéru, jenže se už nikde nedočteš, že má prarodiče v bytě naproti a každý den jim hlídají.
Každý má zcela jiné výchozí podmínky a i když jsou navenek zdánlivě podobné, většinou prostě stejné nejsou a fakt nemá smysl se srovnávat a bičovat se za to, že někdo něco dokázal a já (ještě) ne.

{% call blockquote_avatar(
  'Poutavě odvyprávěné příběhy slavných lidí nebo třeba obětí zločinů a katastrof vynechávají řadu informací a záměrně nebo mimoděk manipulují s publikem, což sice vede k větší atraktivitě a přístupnosti, ale také to snižuje důvěryhodnost sdělení.',
  'matous-hrdina.jpg',
  'Matouš Hrdina'
) %}
  Matouš Hrdina, ve [vydání newsletteru Pod čarou o storytellingu](https://seznam-zpravy.u.mailkit.eu/mc/VVQIVPEI/IFFILXQQDLFARYLJIY/CQMCWMIUIPV)
{% endcall %}

Aby příběhy inspirovaly a někdo se o ně zajímal, musí být výsledkem [storytellingu](https://en.wikipedia.org/wiki/Storytelling), [cherry pickingu](https://en.wikipedia.org/wiki/Cherry_picking) a [survivorship biasu](https://en.wikipedia.org/wiki/Survivorship_bias).
James Bond se taky nikdy nejde ve filmu vyčůrat.
Pokud to není důležité pro příběh, je zbytečné to sdělovat.
Že někdo probrečel večery s hlavou v dlaních možná důležité pro příběh je, ale zase by se to moc nevyjímalo v _success story_ na stránkách kurzu.
A možná to ten člověk ani nechce takto sdílet, je to osobní.

Je to tedy na tobě.
Stejně jako při scrollování na instáči, kde mají všichni nejlepší dovolenou a nejlepší zadek.
Inspirovat se kam zajet na dovolenou? Jasně!
Ale uvědomovat si, že možná měli v kuchyni šváby, možná se pohádali, možná mají jiné geny, bohaté rodiče, a možná je to fotka z vhodně vybraného úhlu.

Pokud víš, že se s druhými srovnávat nemáš, ale stejně si neumíš pomoci, projdi si kapitolu [Psychika na cestě do IT](handbook/mental-health.md).

## Příběhy z junior.guru

Děláme rozhovory s členy zdejšího [klubu](club.md).
Cílem je nejen ilustrovat hodnotu klubu pro juniory, ale taky snaha popsat cestu do IT co nejautentičtějším způsobem.

Co pro ně bylo těžké a nedařilo se to?
Kdy chtěli všeho vzdát a jen brečet v koutě?
Jak to nakonec překonali?
Co by poradili ostatním?
Nejen že se nebojíme o nepříjemnostech psát, my se na ně přímo ptáme!

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }} Tady něco bude.
{% endcall %}

## Z horníka programátorem

V roce 2020 vznikl o rekvalifikaci do IT český film [Nová šichta](https://www.csfd.cz/film/892942-nova-sichta/).
Dokument sleduje Tomáše, který se rozhodl stát se programátorem po tom, co strávil 25 let pod zemí jako horník na Ostravsku.
Film realisticky popisuje nejen úspěchy, ale i těžkosti celé Tomášovy cesty.

<div class="link-cards">
  {{ link_card(
    'Nová šichta na dafilms.cz',
    'https://dafilms.cz/film/12793-nova-sichta',
    'Tady si můžeš film legálně pustit, nebo i stáhnout.',
    badge_icon='play-circle-fill',
    badge_text='65 Kč',
  ) }}

  {{ link_card(
    'Nová šichta na KVIFF.TV',
    'https://kviff.tv/katalog/nova-sichta',
    'Tady si můžeš film legálně pustit, nebo i stáhnout.',
    badge_icon='play-circle-fill',
    badge_text='70 Kč',
  ) }}

  {{ link_card(
    'Rozhovor v DVTV',
    'https://video.aktualne.cz/dvtv/z-hornika-programatorem-uz-jsem-to-vzdaval-narazel-jsem-na-n/r~fbb04576cfa811ebbc3f0cc47ab5f122/',
    'Tomáš Hisem a režisér Jindřich Andrš u Martina Veselovského.',
  ) }}
</div>

## Příběhy odjinud

Sbíráme je z různých koutů českého a slovenského internetu, stejně jako když v 19. století zapisovali Němcová s Erbenem lidovou slovesnost.

Víš o dalších?
Tipy můžeš poslat na {{ 'honza@junior.guru'|email_link }}.
Jedinou podmínkou je, že musí být publikovány na „neutrální půdě“.
Každá vzdělávací agentura si dává na web _success stories_, které ukazují, jak jsou jejich kurzy úžasné a absolventi úspěšní.
Záměrem tohoto seznamu je vytvářet nezávislou protiváhu a ukazovat, že:

-   Programování se lze učit i jinde než v kurzu.
-   Ne vždy je vše sluníčkové.
    Ne vždy to skončí tak, jak si člověk naplánuje.
    Ne vždy to zvládne sám a levou zadní.
-   Cesta většiny lidí je spletitá.
    Zkouší různé způsoby studia, různé kurzy, různé materiály.
-   Programování je obecná, užitečná dovednost, která se hodí i pokud se člověk neplánuje rekvalifikovat do IT.

{% for story in stories %}
  {# {% set small %}
    {{ story.publisher }} &mdash; {{ '{:%-d.%-m.%Y}'.format() }}
  {% endset %} #}
  {{ news_card(
    story.title,
    story.url,
    story.image_path,
    'Doprovodná fotka k příběhu',
    subtitle=story.name,
    category=story.publisher,
    date=story.date,
    external=true)
  }}
{% endfor %}
