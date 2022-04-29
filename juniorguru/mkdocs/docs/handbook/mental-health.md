---
title: Jak přežít cestu juniora po psychické stránce
description: Cesta do IT může být náročná životní změna. Vysoké nároky na sebe sama, srovnávání se s ostatními, nedostatek odpočinku, nejistota. Přečti si, jak se to dá zvládat.
template: main_handbook.html
---

{% from 'macros.html' import guarantor, lead, note, video_card, link_card, md with context %}

# Psychika na cestě do IT

{% call lead() %}
  Cesta do IT může pro psychiku představovat velkou výzvu. Vysoké nároky, obavy a málo odpočinku potká na své cestě nejeden junior. Jak se s tím můžeš vyrovnat?
{% endcall %}

{% call guarantor('Nela Slezáková', 'images/avatars-participants/nela-slezakova.jpg', url='https://www.nelaprovazi.cz/', standout=True) %}
  Jak psycholožka, tak i programátorka. Do IT se dostala po vlastní ose a díky tomu sama dobře ví, co cesta juniora dělá s lidskou psychikou. S otázkami kolem duševního zdraví juniorům pomáhá i ve [zdejším klubu](../club.md).
{% endcall %}

## Pět zásad

Jako úvod do tématu ti poslouží přednáška o pěti zásadách, díky kterým můžeš svou cestu do IT zvládnout ve větší duševní pohodě: Zakotvi se v realitě, přijmi svoje limity, buď svůj fanklub, sežeň si podporu, získej nadhled.

{{ video_card(
  'Nela Slezáková: Jak přežít cestu juniora po psychické stránce',
  '40min',
  'youtube.com!watch!v=6G4TKGQICw0.jpg',
  'https://www.youtube.com/watch?v=6G4TKGQICw0',
  'Pět zásad a ke každé z nich praktické tipy, díky kterým můžeš svou cestu do IT zvládnout udržitelně.',
  note='Záznamy [klubových přednášek](/events/) bývají dostupné jen pro členy, ale tento jsme zveřejnili, ať pomáhá všem.',
) }}

## Když je krize

V akutních případech si stáhni mobilní aplikaci, obrať se na telefonní krizovou pomoc, nebo se stav do nejbližsího krizového centra. Tam si můžeš přijít popovídat s odborníkem, zdarma a bez předchozího objednání, někde dokonce 24 hodin denně.

<div class="link-cards">
  {{ link_card(
    'Nepanikař',
    'nepanikar.eu!aplikace-nepanikar.jpg',
    'https://nepanikar.eu/aplikace-nepanikar/',
    'Mobilní aplikace na rychlou první sebepomoc.',
  ) }}

  {{ link_card(
    'Telefonní linky',
    'mvcr.cz!clanek!adresar-pomoci-telefonni-informacni-a-krizove-linky-a-online-pomoc-v-ceske-republice..jpg',
    'https://www.mvcr.cz/clanek/adresar-pomoci-telefonni-informacni-a-krizove-linky-a-online-pomoc-v-ceske-republice.aspx',
    'Linka první psychické pomoci, linky důvěry, a další.',
  ) }}

  {{ link_card(
    'Krizová centra',
    'nepanikar.eu!mapa-pomoci-krizova-centra.jpg',
    'https://nepanikar.eu/mapa-pomoci-krizova-centra/',
    'Mapa míst, kam můžeš zajít, když už si nevíš rady.',
  ) }}
</div>

## Dlouhodobější terapie

V méně akutních případech se objednej na psychoterapii. Můžeš se zkusit dostat ke **klinickému psychologovi**, který v rámci svého vzdělávání absolvoval terapeutický výcvik. Jejich služby pojišťovny plně proplácí, ale mnohdy nemají volné kapacity, nebo jsou objednací lhůty několikaměsíční.

Další variantou je využít **příspěvek na terapii**. Během pandemie covidu-19 jej začaly poskytovat všechny větší zdravotní pojišťovny. Zjisti si na webu té svojí jak postupovat. Většinou se setkáš s nabídkou konkrétních odborníků, na jejichž služby pojišťovna příspěvek vyplácí.

Taky máš možnost najít si libovolného **psychoterapeuta na přímou platbu**. Pokud se ti nehodí na terapii docházet osobně, existují i specializované platformy, které zprostředkovávají terapii online.

<div class="link-cards">
  {{ link_card(
    'Nela provází',
    'nelaprovazi.cz.jpg',
    'https://www.nelaprovazi.cz/',
    'Psycholožka a programátorka. Pomáhá lidem v IT anebo do IT.',
    badge_icon='star',
    badge_text='Autorka této kapitoly',
    highlighted=True,
  ) }}

  {{ link_card(
    'Hedepy',
    'hedepy.cz.jpg',
    'https://hedepy.cz/',
    '... (nevím, jak se liší od terapio)',
    badge_icon='headset',
    badge_text='Online terapie',
  ) }}

  {{ link_card(
    'Terapio',
    'terap.io.jpg',
    'https://terap.io/',
    '... (nevím, jak se liší od hedepy)',
    badge_icon='headset',
    badge_text='Online terapie',
  ) }}

  {{ link_card(
    'Nevypusť duši: Infografiky',
    'nevypustdusi.cz!infografika.jpg',
    'https://nevypustdusi.cz/infografika/',
    'Vysvětlení pojmů, tipy, nebo jak pomoci sobě či blízkému.',
    badge_icon='info-circle',
    badge_text='Info',
  ) }}

  {{ link_card(
    'Příspěvek VZP',
    'dusevnizdravi.vzp.cz.jpg',
    'https://dusevnizdravi.vzp.cz',
    'Jak na příspěvek u nejrozšířenější pojišťovny?',
    badge_icon='info-circle',
    badge_text='Info',
  ) }}
</div>

## Jak vybírat terapeuty

Úspěch dlouhodobější terapie hodně závisí na tom, jak si sedneš se svou terapeutkou nebo terapeutem. Pohlídej si hlavně **typ a délku psychoterapeutického výcviku**. Pokud výcvik nemá, není to terapeut!

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }} Tady Nela ještě něco doplní. Nějaký odstavec, kde bude asi odkaz [sem na Wikipedii](https://cs.wikipedia.org/wiki/Psychoterapie#Psychoterapeutick%C3%A9_%C5%A1koly) a co s tím maj lidi udělat. Ještě bych do toho odstavce někam zakomponoval větu „S jakými obtížemi má zkušenosti?“ či podobné sdělení, protože tahle věta byla v původním seznamu a Honza ji zatím vyhodil, jelikož tuší, že tenhle budoucí odstavec to nějak pokryje.
{% endcall %}

Poptej se známých na doporučení a zkušenosti, ale pamatuj, že **každému sedne někdo jiný**. Každý máme své téma, sedí nám jiný typ práce, jsou nám sympatičtí jiní lidé. Takže pokud ti první terapeut nesedne, nevěš hlavu! Vyzkoušej někoho jiného.
