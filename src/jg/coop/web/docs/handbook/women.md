---
title: Ženy v IT
emoji: 👩
stages: [thinking, preparing, applying]
description: Je IT pro ženy? Existují vůbec nějaké programátorky? Jak do oboru prorazit jako žena? Co očekávat? A co ti může na cestě pomoci?
template: main_handbook.html
---

{% from 'macros.html' import lead, blockquote_avatar, link_card, note with context %}

# Ženy a kariéra v IT

{% call lead() %}
Je IT pro ženy?
Existují vůbec nějaké programátorky?
Jak do oboru prorazit jako žena?
Co očekávat?
A co ti může na cestě pomoci?
{% endcall %}

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }} Kapitola se teprve připravuje.
{% endcall %}

Žen je v IT málo — v Evropských státech je to mezi 10 až 30 %. [Česko je na tom se svými 10 % hůř než Turecko](https://www.ceskovdatech.cz/clanek/128-neni-ajtak-jako-ajtak/), takže existují aktivity, které se snaží ženám cestu do IT usnadnit.

{% call blockquote_avatar(
  'Po několika kurzech programování jsem si uvědomila, že mě to baví víc než laboratoř. Šlo to dělat kdykoliv a kdekoliv, v noci, z hřiště, během kojení…',
  'lenka-segura.jpg',
  'Lenka Segura',
) %}
  Lenka Segura v [rozhovoru pro CyberMagnolia](https://web.archive.org/web/20221204155402/https://cybermagnolia.com/blog/page/2/), bývalá agrochemička
{% endcall %}

<div class="link-cards">
  {{ link_card(
    'PyLadies',
    'https://pyladies.cz',
    'Komunitní půlroční kurzy programování a navazující workshopy.'
  ) }}

  {{ link_card(
    'Czechitas',
    'https://www.czechitas.cz',
    'Česká neziskovka otevírající IT ženám skrze workshopy, kurzy a další akce.'
  ) }}

  {{ link_card(
    'Aj Ty v IT',
    'https://ajtyvit.sk',
    'Slovenská neziskovka otevírající IT ženám skrze workshopy, kurzy a další akce.'
  ) }}

  {{ link_card(
    'ReactGirls',
    'https://reactgirls.com/',
    'Komunitní jednodenní workshop tvorby webu v JavaScriptu.'
  ) }}

  {{ link_card(
    'Django Girls',
    'https://djangogirls.org/',
    'Komunitní jednorázový startovací workshop tvorby webu v Pythonu.'
  ) }}

  {{ link_card(
    'Rails Girls',
    'https://railsgirls.com/',
    'Komunitní jednorázový startovací workshop tvorby webu v Ruby.'
  ) }}
</div>


<!-- {#

https://web.archive.org/web/20230322060142/https://cybermagnolia.com/blog/the-money-talk-meetup/

- https://www.heroine.cz/zeny-it/7701-zeny-jsou-z-it-trhu-vytlacovany-rika-vedouci-analytik-lmc-tomas-dombrovsky
- ženy v it stránka přímo v příručce kde jsou heroine články atd. a třeba i díl moderná firma o ženách nebo motherhood atd.
- Vytvořit stránku ženy v IT, kde odkazu heroine a klidně i každý článek odtamtud, moje označené, potom odkazy, potom vysvětlit pro kazdyho proč ženy v it a proč se to hodí dělat a FAQ ala garáž (Brusel a EU atd)
- https://www.heroine.cz/clanky/autor/70000223-honza-javorek
- https://girlsday.cz/
- Důležité svátky - Girls day, women in tech, etc.
- https://robime.it/?s=rozhovory
- https://www.root.cz/market-voice/mezinarodni-vyzkum-ukazal-ze-zen-v-it-pribyva-zdaleka-to-nejsou-jen-programatorky/
- https://womenwill.google/
- https://developers.google.com/womentechmakers
- https://medium.com/@lenka.stawarczyk/pro%C4%8D-si-%C5%BEeny-p%C5%99i-hled%C3%A1n%C3%AD-pr%C3%A1ce-nev%C4%9B%C5%99%C3%AD-a-nejsou-sp%C3%AD%C5%A1-jen-vyb%C3%ADrav%C3%A9-a50c936fb805
- https://projekty.heroine.cz/zeny-it
- https://www.facebook.com/groups/holkyzit

https://hbr.org/2014/06/why-women-dont-negotiate-their-job-offers

Skvěle napsaný a velmi přínosný článek demýtizující tzv. confidence gap: Že mužům stačí splnit 60 % požadavků v pracovním inzerátu a už se hlásí, zatímco ženy se nepřihlásí, dokud nemají 100 %. Text poskytuje zdroj statistiky, podrobnější rozbor problému, návrhy toho, co mohou firmy dělat. Ženy „…jsou trochu soudnější a zdrženlivější než muži. Nechtějí trávit čas a energii někde, kde nevěří, že můžou uspět.” Budu muset opravit příručku! Mnoho z věcí zmíněných v článku navíc platí i pro juniory v IT. Například popsat jasně a jednoznačně věci, které firma vyžaduje, a které jsou bonus, to je problém většiny juniorních nabídek.
https://medium.com/@lenka.stawarczyk/pro%C4%8D-si-%C5%BEeny-p%C5%99i-hled%C3%A1n%C3%AD-pr%C3%A1ce-nev%C4%9B%C5%99%C3%AD-a-nejsou-sp%C3%AD%C5%A1-jen-vyb%C3%ADrav%C3%A9-a50c936fb805

https://www.youtube.com/watch?v=X0iyjV9aEM8
https://www.heroine.cz/zeny-it/11329-nemam-skolu-a-nejsem-technicky-typ-nejcastejsi-povery-ktere-zeny-odrazuji-od-prace-v-it

--- https://discord.com/channels/769966886598737931/788826407412170752/1209840122757914644
💪
---


https://mastodonczech.cz/@SmudgeTheInsultCat@mas.to/112225723955493154
https://mas.to/@SmudgeTheInsultCat/112225723796627574


--- https://discord.com/channels/769966886598737931/769966887055392768/1296409124849848340
Další rozhovor do ouška 👂tentokrát s <@1275834407470497985> 
👉 https://www.youtube.com/watch?v=5J1SgIo0KBY
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1266001455534575637
https://csu.gov.cz/produkty/ict-specialistky-berou-o-16-tisic-mene-nez-muzi
---


#} -->
