---
title: Jak přežít cestu juniora po psychické stránce
emoji: 💆
stages: [learning, preparing, applying, onboarding]
description: Cesta do IT může být náročná životní změna. Vysoké nároky na sebe sama, srovnávání se s ostatními, nedostatek odpočinku, nejistota. Přečti si, jak se to dá zvládat.
template: main_handbook.html
---

{% from 'macros.html' import guarantor, lead, illustration, link_card, video_card, blockquote with context %}

# Psychika na cestě do IT

{% call lead() %}
  Říká se, že všechno je to v hlavě. Mysl ti může být skvělým spojencem – zdrojem motivace, odvahy a vytrvalosti. Stejně tak ti ale může cestu do IT i pěkně znesnadnit. Nejeden junior se utápí v nadměrných pochybách, má na sebe příliš velké nároky a cítí se pod tlakem. Jak se nenechat brzdit, ale mít svou psychiku za spojence?
{% endcall %}

[TOC]

{{ illustration('static/illustrations/mental-health.webp') }}

{% call guarantor('Nela Slezáková', 'avatars-participants/nela-slezakova.jpg', url='https://www.nelaprovazi.cz/', standout=True) %}
  Jak psycholožka, tak programátorka. Rozumí tomu, jak funguje lidská psychika a sama si zažila, co obnáší dostat se do IT po vlastní ose. Ve vlastní praxi pomáhá lidem v IT anebo do IT. S otázkami kolem duševního zdraví juniorům pomáhá i ve [zdejším klubu](../club.md).
{% endcall %}

## Správné načasování

Jako první zvaž, zda je právě nyní vhodný čas na kariérní změnu do IT. Podobně jako je v případě horské túry důležité odhadnout dobře své síly. Není totiž nic horšího, než uprostřed cesty zjistit, že už to dál nepůjde.

První aspekt, který pečlivě promysli, je **zdraví**. Pokud se necítíš dlouhodobě psychicky či fyzicky v pořádku, nemusíš mít dost sil extra zátěž dlouhodobě ustát. Obzvláště riskantní počin je snažit se o kariérní změnu na pokraji vyhoření, když už není odkud brát energii. Možná si aktuálně potřebuješ spíš oddychnout, dát se do pořádku a pokusit se o změnu ve vhodnější čas.

Druhým aspektem jsou **peníze**. Kurzy něco stojí a hledání práce se může oproti původním odhadům docela protáhnout. Sledovat ztenčující se finanční rezervu a stále nemít nabídku práce je extrémně stresující. Možná si aktuálně potřebuješ spíš vytvořit finanční polštář a poté se o změnu pokusit s čistou hlavou.

{% call blockquote(
  'Chci být k dispozici dceři, než trochu doroste a zvykne si ve školce. Takže jsem byla ráda, když jsem dostala příležitost pracovat u nás ve městě na zámku. Budu mít jistý příjem, stabilitu a čas na postupné vzdělávání. Najít si práci v IT mám pořád v plánu.'
) %}
  Katka
{% endcall %}

Pak je tady **čas**. Kolik času můžeš věnovat učení a zároveň nevyškrtat ze svého diáře všechen odpočinek? Možná je nejdříve potřeba zamyslet se, jaké povinnosti a aktivity můžeš zrušit, zkrátit si úvazek, anebo i počkat na vhodnější životní období.

A nakonec, máš dostatečnou **podporu okolí**? Může být velmi náročné potýkat se s vlastními obavami, zároveň se nemít o koho opřít, a nad to ještě rozhánět pochyby své rodiny a přátel. Možná si chceš nejprve najít nějaké spojence. Co třeba v [klubu na junior.guru](../club.md)?

## Duševní hygiena pro juniory

Vybav se pro začátek 5 zásadami, díky kterým můžeš svou cestu do IT zvládnout ve větší duševní pohodě a udržitelně. V přednášce se mimo jiné dozvíš, jak stát nohama víc na zemi, proč je důležité přijímat se i se svými limity anebo jak získat nadhled.

{% set event = events|selectattr("id", "equalto", 18)|first %}
{{ video_card(
  event.get_full_title(),
  event.public_recording_duration_s|hours,
  event.public_recording_url,
  thumbnail_url="static/" + event.plain_poster_path,
  note='Záznamy [klubových přednášek](../events.md) bývají dostupné jen pro členy, ale tento jsme zveřejnili, ať pomáhá všem.'
) }}

## Impostor syndrom

Znáš ten pocit, když **dosáhneš úspěchu, ale místo radosti ti hlavou víří pochybnosti a obavy**, že tvůj úspěch je spíše výsledkem náhody než tvého skutečného talentu?

Možná zažíváš [syndrom podvodníka](https://cs.wikipedia.org/wiki/Syndrom_podvodn%C3%ADka), anglicky _impostor syndrom_. Definují ho pocity vlastní neschopnosti, kdy úspěch vnímáš jako nezasloužený. Je doprovázený **strachem z toho, že jednoho dne ostatní prohlédnou, že ve toho skutečnosti toho tolik neumíš**. Že svoje znalosti jen předstíráš.

Možná se to nezdá, ale impostor syndrom je poměrně častý. Co s tím? Začni si nadměrných obav všímat, ověřuj si pravidělně svoje vidění s okolím (a ber vážně to, co říkají), anebo zkus psychoterapii.

Docela dobře funguje **deníček, kam si zapisuješ svou cestu**. Pomůže ti ohlédnout se a uvědomit si, jak velký kus cesty už máš za sebou. Ve [zdejším klubu](../club.md) si lidi přesně takové deníčky píšou.

<div class="link-cards">
  {{ link_card(
    'Syndrom podvodnice v IT',
    'https://www.heroine.cz/zeny-it/6341-syndrom-podvodnice-vas-pri-praci-v-it-snadno-dozene-jak-proti-nemu-bojovat',
    'Zpověď manažerky kybernetické bezpečnosti o vlastním impostor syndromu.',
  ) }}

  {{ link_card(
    'You are not an impostor',
    'https://www.youtube.com/watch?v=l_Vqp1dPuPo',
    'Přednáška o imposter syndromu a způsobech, jak změnit svůj přístup.',
  ) }}

  {{ link_card(
    'Většinu jobů jsem neuměl udělat',
    'https://www.youtube.com/watch?v=S3NKRswt1d0',
    'Yablko o tom, proč je OK ze začátku úkolu vůbec nevědět, jak začít.',
  ) }}
</div>

## Sokratovo „vím, že nic nevím“

Jako většině juniorů se ti nejspíš nevyhne onen opojný stav, kdy do sebe všechno jakoby zapadne. Proměnné, cykly, podmínky i funkce už nejsou žádnou výzvou a od teď už to bude jen lehčí!

Jak bolestné je zjistit, že **za horizontem se tyčí další hory a velehory**, které je potřeba zdolat. Že šíře poznání a dovedností v IT se rozpíná jako vesmír a nikde nemá hranice.

Nenech se tím zviklat! Vědět, že víš fakt málo, je **známkou toho, že už něco umíš**, a je to zcela normální.

<div class="link-cards">
  {{ link_card(
    'Co je Dunning-Kruger efekt?',
    'https://www.youtube.com/watch?v=H01nrHnqUfI',
    'Vědět, že nic nevíte, je lepší, než si myslet, že víte všechno.',
  ) }}
</div>

## Juniory často sužují obavy a pochybnosti

Z naší ankety s více než 200 juniory (květen až červen 2023) vyplynulo:

- 44 % se bojí, že ostat­ní při­jdou na to, že jsou k ni­čemu,
- 70 % z těch, kdo hle­da­jí práci, má strach, zda si vů­bec ně­ja­kou na­jdou,
- 55 % z těch, kdo už pra­cu­jí, má po­cit, že jsou ne­schop­ní.

To nejsou vůbec líbivá čísla. V přednášce „Jak se jako ajťák/čka zbavit pochyb a pocitu, že nejsem dost” se můžeš seznámit s kompletními výsledky z ankety a ujistit se, že vůbec nejsi sám/sama, kdo se tolik obává. V druhé části přednášky najdeš tipy jak pracovat s nadměrnými pochybami v kontextu IT.

{% set event = events|selectattr("id", "equalto", 36)|first %}
{{ video_card(
  event.get_full_title(),
  event.public_recording_duration_s|hours,
  event.public_recording_url + '&t=613',
  'Nadměrné obavy v IT jsou denním chlebem velké části juniorů na cestě do IT i během prvních let v oboru. Seznam se s výsledky ankety a s 11 tipy, jak s pochybami zatočit.',
  thumbnail_url="static/" + event.plain_poster_path,
  note='Záznamy [klubových přednášek](../events.md) bývají dostupné jen pro členy, ale tento jsme zveřejnili, ať pomáhá všem.'
) }}

## Rozcestník pomoci

Rozeznat moment, ve kterém už je dobré si říct o pomoc, je někdy náročné. Sleduj především tyto dva signály:

- Psychicky se **dlouhodobě** necítíš dobře, tzn. obtíže v řádu měsíců neustupují.
- Tvé problémy jsou **intenzivní** a začínají ti proto **způsobovat problémy v každodenním životě**. Je kvůli nim např. obtížnější odvádět výkon v práci, či udržovat spokojené vztahy.

Je taky výhodné dát na **upozornění našeho okolí**, které je schopné někdy lépe registrovat pozvolné změny v našem stavu. Samozřejmě neváhej, pokud cítíš, že **situace není udržitelná**. Národní ústav duševního zdraví (NÚDZ) nabízí [dotazníky](https://www.opatruj.se/otestujte-se), kterými můžeš svůj aktuální stav otestovat.

### Když je krize

Existují situace, které nesnesou odkladu. Pokud tě zaplaví velmi silné emoce a nevíš si s nimi rady anebo cítíš, že prostě takhle už dál nemůžeš, nechej si s tím pomoct.

**Aplikace Nepanikař** obsahuje tipy na základní a rychlou sebepomoc, řízená dechová cvičení, i kontakty na odborníky.

**Telefonní krizové linky** ti umožňují rychlý kontakt s odborníkem. Hovor by ti měl přinést jak okamžitou úlevu, tak doporučení na to, jak postupovat dál.

**Krizové centrum** nabízí nejvíce komplexní pomoc v krizi. Můžeš tam přijít bez objednání a s odborníkem do hloubky probrat svoji životní situaci. Některá centra fungují dokonce nonstop. Návštěva ti pomůže se zklidnit a naplánovat další kroky.

<div class="link-cards">
  {{ link_card(
    'Nepanikař',
    'https://nepanikar.eu/aplikace-nepanikar/',
    'Mobilní aplikace na rychlou první sebepomoc.',
  ) }}

  {{ link_card(
    'Telefonní linky',
    'https://mv.gov.cz/clanek/adresar-pomoci-telefonni-informacni-a-krizove-linky-a-online-pomoc-v-ceske-republice.aspx',
    'Linka první psychické pomoci, linky důvěry, a další.',
  ) }}

  {{ link_card(
    'Krizová centra',
    'https://www.mapotic.com/mapa-psychicke-pomoci',
    'Mapa míst, kam můžeš zajít, když už si nevíš rady.',
  ) }}
</div>

### Psychoterapie

V méně akutních případech můžeš vyhledat jednoho ze dvou odborníků: klinického psychologa, nebo psychoterapeuta na přímou platbu.

Psychoterapie jsou, zjednodušeně řečeno, **rozhovory s psychoterapeutem** o tématech, které tě tíží. Postupně ventiluješ emoce, chápeš lépe sebe i svou situaci, získáváš nadhled. Hlavně ale přicházíš na způsoby, jakými své problémy řešit.

Terapeuti své služby dnes už běžně nabízí **jak osobně, tak online**. Existují i specializované platformy nabízející terapii výhradně přes videohovor.

Pokud po pár sezeních necítíš významné zlepšení, nevěš hlavu, **chce to čas**. Je běžné cítit se o něco lépe už po pár týdnech, či měsících, ale rovněž je normální zažít i dočasný výkyv k horšímu. Celé to může trvat i víc než rok.

#### Klinický psycholog

Absolventi postgraduálního specializačního vzdělávání v oboru klinické psychologie mohou poskytovat psychoterapii a zhodnocovat tvůj psychický stav (psychodiagnostika). Sice ti **vše uhradí pojišťovna**, ale protože klinických psychologů není mnoho, tak mívají plno, nebo nabízejí dlouhé objednací lhůty.

<div class="link-cards">
  {{ link_card(
    'Mapa zdravotní péče',
    'https://www.nzip.cz/vyhledavaci-mapy',
    'Najdi klinického psychologa ve svém okolí.',
  ) }}
</div>

#### Psychoterapeut na přímou platbu

Psychoterapeut je někdo, kdo má započatý či úspěšně zakončený psychoterapeutický výcvik. Součástí psychoterapeutických výcviků jsou stovky hodin vzdělávání a desítky hodin nácviků, supervizí a poznávání sebe sama na psychoterapii. Člověk se na takovém výcviku naučí, jak dělat dobrou terapii v praxi. Pokud je navíc vysokoškolsky vzdělaný v psychologii, zná i teorii o fungování lidské psychiky.

Existuje řada adresářů psychoterapeutů. Největší je asi ten od [České asociace pro psychoterapii (ČAP)](https://www.czap.cz/adresar). Můžeš ale zkusit i vyhledávání přes internet, specializované platformy, nebo se ptát známých. Nakonec je nejlepší vybrat někoho sympatického blízko tvému bydlišti či práci a pak zhodnotit, jak jste si sedli a jak ti spolupráce vyhovuje, případně zkusit někoho jiného. Pamatuj, že terapie plní svůj účel pouze pokud na ní panuje přijímající a chápající atmosféra, ve které můžeš mluvit o čemkoliv, aniž by tě někdo bral na lehkou váhu anebo tě zesměšňoval.

Výcviky mají určité **specializace** a různý styl práce, takže i typ výcviku může být vodítkem při výběru. V základu jsou ovšem pro výkon psychoterapie všechny stejně dobré. Každý terapeut by měl mít na webu napsáno, jaký má výcvik.

Hodina sezení tě zpravidla vyjde na 1000-1200 Kč, ale mnozí poskytují **slevy pro studenty, nebo znevýhodněné skupiny**. Od pandemie covidu-19 začaly navíc na terapii přispívat skoro všechny **zdravotní pojišťovny**. Většinou mají na webu postup, jak příspěvek získat, a seznam terapeutů, u kterých jej můžeš čerpat.

<div class="link-cards">
  {{ link_card(
    'ČRo: Psychoterapie prakticky',
    'https://www.irozhlas.cz/zpravy-domov/dostupnost-psychoterapie-terapie-cena-sezeni-data-regiony-pojistovny-vzp_2212200600_jab',
    'Co očekávat od psychoterapie, jak vybrat psychoterapeuta, kolik to stojí a jak je účinná.',
  ) }}

  {{ link_card(
    'Seznam psychoterapeutů ČAP',
    'https://www.czap.cz/adresar',
    'Adresář psychoterapeutů od České asociace pro psychoterapii.',
  ) }}

  {{ link_card(
    'Nela provází',
    'https://www.nelaprovazi.cz/',
    'Nabízí psychologickou podporu na cestě do IT.',
    badge_icon='star',
    badge_text='Autorka této kapitoly',
    class='highlighted',
  ) }}
</div>

### Psychiatr

Adekvátně hloubce problému se může míra prožívaných obtíží jevit až neúnosně. Ve chvíli, kdy ti **základní nároky každodenního života připomínají výstup na Everest**, může být na místě konzultovat tvůj stav s psychiatrem, tedy lékařem. Říká se, že pro psychoterapii potřebuje být člověk alespoň trochu „v kondici“, aby měl energii posvítit si na příčiny svých problémů a započít tak proces úzdravy.

Psychiatr tě vyslechne, proberete tvůj stav, a pak ti nabídne pomoc. Může ti nabídnout **vyladění režimu** (např. spánku, každodenních rutin…), doporučit **doplňky stravy** podporující zlepšení tvého stavu, nebo předepsat **léky (tzv. psychofarmaka)** zaměřené na konkrétní obtíže. Cílem je překlenout náročné životní období (snížit úzkosti, zvýšit tvou životní energii…) a dostat tě do kondice pro psychoterapii. Pokud se vám to podaří s pomocí psychofarmak, typicky se časem můžete s lékařem domluvit, že léky zase vysadíte.

<div class="link-cards">
  {{ link_card(
    'Otestuj svůj psychický stav',
    'https://www.opatruj.se/otestujte-se',
    'Orientační diagnostika psychického zdraví.',
  ) }}

  {{ link_card(
    'Návštěva psychiatra',
    'https://www.ulekare.cz/clanek/psychiatricke-vysetreni-1176',
    'Co čekat od konzultace s psychiatrem.',
  ) }}

  {{ link_card(
    'Mapa zdravotní péče',
    'https://www.nzip.cz/vyhledavaci-mapy',
    'Najdi psychiatra ve svém okolí.',
  ) }}
</div>

### Koučink

Pokud **toužíš dosáhnout určitého stavu nebo cíle**, můžeš zkusit koučink. Jde o krátkodobější a rychlejší řešení, které spočívá v provádění konkrétních změn ve tvém životě.

Koučink nejde do hloubky a nezabývá se příliš emocemi, takže se nejedná o léčebný nástroj vhodný k řešení psychických obtíží, jakými jsou úzkosti nebo deprese.

Kouč ti dává otevřené otázky a provádí tě procesem, při kterém si uvědomíš, čeho chceš vlastně dosáhnout, jaká je situace a jak to celé uděláš (model GROW).

Kouč je někdo, kdo absolvoval dlouhodobý a ideálně i akreditovaný koučovací výcvik, díky kterému je odborníkem na metodu koučování. Spolupráce s koučem se točí kolem konkrétních změn, a tak bývá rychlejší a za vyšší sazby, než je běžné u psychoterapie.

<div class="link-cards">
  {{ link_card(
    'Koučování',
    'https://cs.wikipedia.org/wiki/Kou%C4%8Dov%C3%A1n%C3%AD',
    'Co je to koučink.',
  ) }}

  {{ link_card(
    'Koučovací metoda GROW',
    'https://cs.wikipedia.org/wiki/GROW_(kou%C4%8Dink)',
    'Specifika nejrozšířenější koučovací metody.',
  ) }}

  {{ link_card(
    'Nela provází',
    'https://www.nelaprovazi.cz/',
    'Akreditovaná koučka, zaměřuje se na IT.',
    badge_icon='star',
    badge_text='Autorka této kapitoly',
    class='highlighted',
  ) }}
</div>


<!-- {#

Přemýšlím, že se vrátím na šachtu, tam jsem měl prázdnou hlavu. Teď chodím z práce domů, vole, a furt nad něčím přemýšlím, furt mám něco v hlavě, vole, něco tě napadne, musím si ku**a zapnout komp, ty p**o. Mně se zdálo o závorkách - složené závorky, dvě složené závorky, ty p**o, jak to tam mám dát?
https://zpravy.aktualne.cz/domaci/tomas-hisem-z-hornika-programatorem/r~927d3882bc9a11ebaedf0cc47ab5f122/

Je ťažké učiť sa programovať? - yablko vysvětluje jak vznikají jeho kurzy a že nepíše kód takhle rychle z hlavy
https://www.youtube.com/watch?v=Fkvx5fOOHLw&list=PLhB6F20C-jTPITEXEHus6fVZDfNxzRbv_&index=6

Produktivita
https://www.youtube.com/watch?v=VJpJOiVLXro

Manuál duševního zdraví vysokoškoláka
https://www.elsa.cvut.cz/wp-content/uploads/2022/11/manual-dusevniho-zdravi-vysokoskolaka.pdf

Podcast s Nelou
https://www.programhrovani.cz/1843229/13207355-dev-stories-9-nela-slezakova-flowerchecker-o-programovani-a-psychologii

Balanc - Bůh je mrtev a na jeho trůn jsme posadili práci. Jak moc je pro vás práce důležitá a co v ní hledáte?
https://www.mujrozhlas.cz/balanc/buh-je-mrtev-na-jeho-trun-jsme-posadili-praci-jak-moc-je-pro-vas-prace-dulezita-co-v-ni

D-K
https://blog.gardeviance.org/2008/04/three-stages-of-expertise.html?m=1
https://mastodonczech.cz/@brohrer@recsys.social/112558203075404703
https://medium.com/geekculture/dunning-kruger-effect-and-journey-of-a-software-engineer-a35f2ff18f1a

--- https://discord.com/channels/769966886598737931/864434067968360459/1275071860479885334
Vyšly videa z PyCon CZ 2023, a s nimi i moje "Prohřešky (juniorních) ajťáků proti psychickému zdraví" https://youtu.be/FuHr7a6M980?si=AP_NHLVizmL_jtCk
---


--- https://discord.com/channels/769966886598737931/1260632853193162794/1260658117339910306
Ve své první práci jsem pravidelně min. jednou týdně brečela u kódu s tím (když jsem zrovna měla HO), že na to nemám. Po nocích jsem se snažila tásky dodělávát, to mi ale samozřejmě vůbec nepomohlo a asi bylo mnohem efektivnější odpočívat a ráno mít čistou hlavu.
Ten stres jsem si vytvářela sama, nikdo ode mě nic velkého neočekával, nic špatného mi neřekl, jen já jsem měla pocit, že  musím něco dodávat.
Doporučuju se aktivně ptát a mít nastavené, co od tebe firma očekává a co od tebe chtějí, říkej si o zpětnou vazbu. Málokdo jí dává sám od sebe. Ať si představy netvoříš sama podle domněnek, které nejsou pravdivé a jen si připadáš hůř. Jo a hodně pomáhá chodit na meetupy, ať slyšíš i problémy ostatních, najednou zjistíš, že v tom nejsi sama a že i senioři řeší stejné problémy.

Jsi tam jen pár dní, v některých firmách za tu dobu ani pořádně  nerozjedeš projekt a prostředí 😆 takže klid, bude to lepší
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1247634603473113109
Tohle je přesný 🙂 Schválně to nedávám do <#797040163325870092>, protože je to hodně relevantní k učení 📈
---


--- https://discord.com/channels/769966886598737931/864434067968360459/1311027460728553543
Tenhle text se mi moc líbí. Myslím, že je hodně právě o lidech jako my tady - co dobrovolně nejdou v životě těmi nejsnadnějšími cestami, protože by to (mimo jiné) byla nuda 🙂
https://www.respekt.cz/tydenik/2024/48/kdyz-mate-pocit-ze-se-v-zivote-jen-placate-mozna-je-cas-vyrazit-za-dobrodruzstvim?gift=d2pxst5fco
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1310282688082612236
Ahoj, kdo byste si chtěl přečíst o Imposter syndromu a o nízkém sebevědomí v IT, přidávám článek  🙂
https://zivotdevky.cz/2024/11/24/neumis-to-mas-jenom-stesti-aka-imposter-syndrom/
---


--- https://discord.com/channels/769966886598737931/864434067968360459/1342058393287786536
Jak se vypořádat s impostor syndromem, tipy od <@362921539613622273> (video, 2min). Lidem jsem dost doporučoval psát si deníček s úspěchy a číst si ho zpětně, ale má tam i další tipy, na které jsem ještě nikdy nenarazil. https://www.linkedin.com/posts/terezia-palascakova_impostor-videoedit-tvorbaobsahu-activity-7298251940923133953-4eAD?utm_source=share&utm_medium=member_desktop&rcm=ACoAAACB93ABHHj4UI2winetGMZHboHlZIZojJA
---


--- https://discord.com/channels/769966886598737931/864434067968360459/1366319025608462406
https://denikn.cz/1715495/nedostatecni-mozna-nejsme-my-ale-system-podivejme-se-konecne-na-syndrom-podvodnika-jinak/?ref=tit
---


--- https://discord.com/channels/769966886598737931/864434067968360459/1440967489088520192
komu to vcera nevyslo na Pyvo <:pyvo:935796907127754812> , ale tiez sa chce nieco spytat ako som to mal s tym burnoutom, intro k talku mam na https://peter.hozak.info/burnout/
---


#} -->
