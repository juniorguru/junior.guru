---
title: Jak přežít cestu juniora po psychické stránce
emoji: 💆
stages: [learning, preparing, applying, onboarding]
description: Cesta do IT může být náročná životní změna. Vysoké nároky na sebe sama, srovnávání se s ostatními, nedostatek odpočinku, nejistota. Přečti si, jak se to dá zvládat.
template: main_handbook.html
---

{% from 'macros.html' import guarantor, lead, link_card, video_card with context %}

# Psychika na cestě do IT

{% call lead() %}
  Říká se, že všechno je to v hlavě. Mysl ti může být skvělým spojencem – zdrojem motivace, odvahy a vytrvalosti. Stejně tak ti ale může cestu do IT i pěkně znesnadnit. Nejeden junior se utápí v nadměrných pochybách, má na sebe příliš velké nároky a cítí se pod tlakem. Jak se nenechat brzdit, ale mít svou psychiku za spojence?
{% endcall %}

{% call guarantor('Nela Slezáková', 'avatars-participants/nela-slezakova.jpg', url='https://www.nelaprovazi.cz/', standout=True) %}
  Jak psycholožka, tak programátorka. Rozumí tomu, jak funguje lidská psychika a sama si zažila, co obnáší dostat se do IT po vlastní ose. Ve vlastní praxi pomáhá lidem v IT anebo do IT. S otázkami kolem duševního zdraví juniorům pomáhá i ve [zdejším klubu](/club.md).
{% endcall %}

## Správné načasování

Jako první zvaž, zda je právě nyní vhodný čas na kariérní změnu do IT. Podobně jako je v případě horské túry důležité odhadnout dobře své síly. Není totiž nic horšího, než uprostřed cesty zjistit, že už to dál nepůjde.

První aspekt, který pečlivě promysli, je **zdraví**. Pokud se necítíš dlouhodobě psychicky či fyzicky v pořádku, nemusíš mít dost sil extra zátěž dlouhodobě ustát. Obzvláště riskantní počin je snažit se o kariérní změnu na pokraji vyhoření, když už není odkud brát energii. Možná si aktuálně potřebuješ spíš oddychnout, dát se do pořádku a pokusit se o změnu ve vhodnější čas.

Druhým aspektem jsou **peníze**. Kurzy něco stojí a hledání práce se může oproti původním odhadům docela protáhnout. Sledovat ztenčující se finanční rezervu a stále nemít nabídku práce je extrémně stresující. Možná si aktuálně potřebuješ spíš vytvořit finanční polštář a poté se o změnu pokusit s čistou hlavou.

<!-- napsal jsem Katce mail, jestli by byla OK s takovým citátem v příručce -->

{% call blockquote(
  'Chci být k dispozici dceři, než trochu doroste a zvykne si ve školce. Takže jsem byla ráda, když jsem dostala příležitost pracovat u nás ve městě na zámku. Budu mít jistý příjem, stabilitu a čas na postupné vzdělávání. Najít si práci v IT mám pořád v plánu.'
) %}
  Katka
{% endcall %}

Pak je tady **čas**. Kolik času můžeš věnovat učení a zároveň nevyškrtat ze svého diáře všechen odpočinek? Možná je nejdříve potřeba zamyslet se, jaké povinnosti a aktivity můžeš zrušit, zkrátit si úvazek, anebo i počkat na vhodnější životní období.

A nakonec, máš dostatečnou **podporu okolí**? Může být velmi náročné potýkat se s vlastními obavami, zároveň se nemít o koho opřít, a nad to ještě rozhánět pochyby své rodiny a přátel. Možná si chceš nejprve najít nějaké spojence. Co třeba v [klubu na junior.guru](../club.md)?

## Duševní hygiena pro juniory

Vybav se pro začátek 5 zásadami, díky kterým můžeš svou cestu do IT zvládnout ve větší duševní pohodě a udržitelně. V přednášce se mimo jiné dozvíš, jak stát nohama víc na zemi, proč je důležité přijímat se i se svými limity anebo jak získat nadhled.

{{ video_card(
  'Nela Slezáková: Jak přežít cestu juniora po psychické stránce',
  '40min',
  'https://www.youtube.com/watch?v=6G4TKGQICw0',
  'Pět zásad a ke každé z nich praktické tipy, díky kterým můžeš svou cestu do IT zvládnout udržitelně.',
  note='Záznamy [klubových přednášek](/events.md) bývají dostupné jen pro členy, ale tento jsme zveřejnili, ať pomáhá všem.',
) }}

## Impostor syndrom

Znáš ten pocit, když dosáhneš úspěchu, ale místo radosti ti hlavou víří pochybnosti a obavy, že tvůj úspěch je spíše výsledkem náhody než tvého skutečného talentu?

Možná zažíváš [syndrom podvodníka](https://cs.wikipedia.org/wiki/Syndrom_podvodn%C3%ADka), anglicky _impostor syndrom_. Definují ho pocity vlastní neschopnosti, kdy úspěch vnímáš jako nezasloužený. Je doprovázený strachem z toho, že jednoho dne ostatní prohlédnou, že ve toho skutečnosti toho tolik neumíš. Že svoje znalosti jen předstíráš.

Možná se to nezdá, ale impostor syndrom je poměrně častý. Co s tím? Začni si nadměrných obav všímat, ověřuj si pravidělně svoje vidění s okolím (a ber vážně to, co říkají), anebo zkus psychoterapii.

<!-- tady bych napsal, že může pomoct zapisovat si úspěchy a po čase si to pročíst a uvědomit si, jakou cestu člověk už ušel? -->

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

## Juniory často sužují obavy a pochybnosti

Z naší ankety s více než 200 juniory (květen až červen 2023) vyplynulo:

- 44 % se bojí, že ostat­ní při­jdou na to, že jsou k ni­čemu,
- 70 % z těch, kdo hle­da­jí práci, má strach, zda si vů­bec ně­ja­kou na­jdou,
- 55 % z těch, kdo už pra­cu­jí, má po­cit, že jsou ne­schop­ní.

To nejsou vůbec líbivá čísla. V přednášce „Jak se jako ajťák/čka zbavit pochyb a pocitu, že nejsem dost” se můžeš seznámit s kompletními výsledky z ankety a ujistit se, že vůbec nejsi sám/sama, kdo se tolik obává. V druhé části přednášky najdeš tipy jak pracovat s nadměrnými pochybami v kontextu IT.

{{ video_card(
  'Nela Slezáková: Jak se jako ajťák/čka zbavit pochyb a pocitu, že nejsem dost',
  '45min',
  'https://youtu.be/FIijszEVQHY?si=XLLrdo2Nn1goBejm&t=613',
  'Nadměrné obavy v IT jsou denním chlebem velké části juniorů na cestě do IT i během prvních let v oboru. Seznam se s výsledky ankety a s 11 tipy, jak s pochybami zatočit.',
  note='Záznamy [klubových přednášek](../events.md) bývají dostupné jen pro členy, ale tento jsme zveřejnili, ať pomáhá všem.',
) }}

## Rozcestník pomoci

Rozeznat moment, ve kterém už je dobré si říct o pomoc, je někdy náročné. Sleduj především tyto dva signály:

- Psychicky se **dlouhodobě** necítíš dobře, tzn. obtíže v řádu měsíců neustupují.
- Tvé problémy jsou **intenzivní** a začínají ti proto **způsobovat problémy v každodenním životě**. Je kvůli nim např. obtížnější odvádět výkon v práci, či udržovat spokojené vztahy.

Je taky výhodné dát na **upozornění našeho okolí**, které je schopné někdy lépe registrovat pozvolné změny v našem stavu. Samozřejmě neváhej, pokud cítíš, že **situace není udržitelná**. [Národní ústav duševního zdraví](https://www.nudz.cz/) nabízí dotazníky, kterými můžeš svůj aktuální stav otestovat.

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
    'https://www.mvcr.cz/clanek/adresar-pomoci-telefonni-informacni-a-krizove-linky-a-online-pomoc-v-ceske-republice.aspx',
    'Linka první psychické pomoci, linky důvěry, a další.',
  ) }}

  {{ link_card(
    'Krizová centra',
    'https://nepanikar.eu/mapa-pomoci-krizova-centra/',
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

### Když psychoterapie nestačí

Pokud ti potíže významně zasahují do života, nebo jsou hodně intenzivní a terapie nezabírá, je dobré **konzultovat tvůj stav s psychiatrem**, tedy lékařem. Nejspíš to doporučí i tvůj terapeut, obzvlášť pokud máš v rodině příbuzné s psychickými obtížemi.

Návštěva u psychiatra neznamená, že automaticky odejdeš s diagnózou a hromadou léků! Psychiatr tě vyslechne, proberete tvůj stav a pak může nabídnout předepsání léků, ale také nemusí. Ty navíc nemusí být nutné brát doživotně, **mohou ti pouze pomoci dočasně překlenout náročné životní období**. Až odezní, můžete se domluvit, že léky vysadíte.

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

feedback na stránku https://discord.com/channels/769966886598737931/789046675247333397/1025450055999692910

Don’t compare yourself
https://twitter.com/traversymedia/status/1298585427016908801

6, 8 - nepropadej panice
https://www.youtube.com/playlist?list=PLhB6F20C-jTPITEXEHus6fVZDfNxzRbv_

workoholismus
https://discord.com/channels/769966886598737931/864434067968360459/900281705246633995

Ahoj :-) tohle mi připadá supr! Sám jsem tím trpěl, teď už tolik ne. A věřím, že spousta juniorů a zvlášť juniorek má tenhle syndrom. Tak jsem si říkal, že by tě to mohlo zaujmout... https://www.youtube.com/watch?v=l_Vqp1dPuPo

Produktivita
https://discord.com/channels/769966886598737931/864434067968360459/901243092856889384

--- https://discord.com/channels/769966886598737931/789107031939481641/999239037187534898
Na "jak zvýšit psychickou odolnost" jsou psaný celý knížky 😄 ale já osobně jsem spíš zastánce toho, že tě zocelují náročné životní situace, které jsi překonal. Je rozdíl mezi eustresem a distresem, eustres je mírný a nabudí tě k lepšímu výkonu, distres už je za hranou a tvůj výkon zhorší. Můj tip na snížení stresu je určitě nácvik. Kognitivně behaviorální terapie vystavování se podnětům, které způsobují úzkost hodně propaguje, a funguje to. Takže poprosit někoho blízkého, ať se mnou simuluje pohovorovou situaci může snížit stres při samotném pohovoru.
---


--- https://discord.com/channels/769966886598737931/864434067968360459/997241498452111441
Teď jsem narazil na velice zajímavou myšlenku, která by mohla rozproudit diskuzi. Čtu zrovna knihu Psychologie peněz (všiml jsem si ze téma financí se tu někde nedávno řešilo) a velice mě tam zaujala myšlenka toho, že pokud člověk zjistí, že chce najednou dělat něco nového (třeba nastartovat kariéru v IT jako asi většina z nás) tak má tendenci se na to až nezdravě soustředit. Plus ho k tomu ještě svírá lítost, že obětoval tolik času něčemu jinému co zrovna opouští a takovéto “kéž bych začal dřív” mu může dost ublížit. Co vy na to? Znáte to? Já osobně jsem s tímhle pocitem bojoval dost dlouhou dobu. Jednou za čas mě to přepadne, ale naučil jsem se s tím pracovat a soustředit se na fakt, že vše v životě má své opodstatnění a vše má svůj čas. Proto taky třeba tolik nespěchám na učení a je to pro mě až na druhém místě za rodinou. 😊
---


--- https://discord.com/channels/769966886598737931/788826407412170752/972950345863028737
Strach a vzrušení před prvním zveřejněním životopisu…, před prvním pohovorem…, před nástupem do práce… Už vím, že mě chtějí, mám domluvenou pozici i mzdu, a přece se to první pracovní ráno cítím jako kdybych šla k maturitě. Sevřená nervozitou, plná očekávání. Co se bude dít první den? A co ty dny další?
Obecně je nástupní den hlavně o setkání a poznání prostředí, vyřízení administrace, předání notebooku a mobilu, přidělení práv a přístupů, absolvování prvních „školení“ o firmě, práci, režimu, atd. Informace jsem hltala možná až moc vehementně, nevím proč jsem si myslela, že musím nasadit vražedné tempo a všechno si hned zapamatovat… Měla jsem toho tak plnou hlavu, že jsem v noci neusnula.
Druhý den jsem nastoupila na projekt do jiné společnosti. Takže stejné kolečko co předchozí den: další nové prostředí, setkání, administrace, notebook, školení… někdy jste na tom tak dobře, že přijdete, první den dostanete notebook a smlouvu, druhý den vám zařídí přístupy a vysvětlí práci, a třetí den už přispíváte jako plnohodnotný člen týmu. Mně se ty dny změnily v týdny (slabina korporátů), takže třeba první měsíc jsem dost intenzivně bojovala se strachem z vyhazovu a s pocitem, že jsem tam k ničemu, protože „nic neprogramuji a jen čtu dokumentaci“ k projektu. Ale v týmu se vědělo, že jsem úplný nováček a zaškoluji se na nových technologiích, takže všichni byli klidní, nápomocní a já se postupně uklidňovala taky… Hlavně díky rozhovorům v kuchyňkách a na obědech (které vřele doporučuji), protože jsem se dozvěděla, že i mým kolegům trval proces rozkoukávání dlouho, že je to normální, pochopitelné, že není kam spěchat, mám být v klidu a pokud budou mít pocit, že bych „měla zrychlit“, určitě to jasně řeknou – opadly tak moje obavy, že bych ze dne na den dostala smsku, ať už do práce nechodím. Postupně jsem začala psát kód a těšilo mě, že byl schvalován bez připomínek a s pochvalou, že mi to jde. Takže nevzdávejte to!
---


--- https://discord.com/channels/769966886598737931/1089542061910413345/1089645111840886836
Ahoj Jamébo, vítej v klubu.
Máš tedy v životě aktuálně řádně naloženo, ne že ne. 😓
Jsme sice stejně staří a už sem taky nějakou tou krizí prošel, ale jako bezdětný, si tohle neumím moc představit. 😮

Co si představit umím, je to, co je potřeba pro změnu kariéry do IT, protože posledních několik let tím lidi provázím.

Ne všem se to povede a ty důvody jsou v naprosté většině stejné:
🪫 nejsou na tom psychicky dobře, vyhoření, deprese, rozpad vztahu, to všechno je často bohužel smrtelná rána téhle snaze, prostě už nemáš energii
💸 nemají dost finančních rezerv: není to levné, místo práce se učit, platit kurzy, hledání práce taky trvá, nástupní peníze v IT nejsou žádná výhra (pořád není výjimkou 30 hrubého za fulltime) i když to samozřejmě stoupá relativně rychle
🫂 chybí podpora partnerů / rodiny / okolí: tohle je trochu propojené s těmi předchozími, okolí ti to může financovat, hlídat děti a vůbec ten pocit, že ti někdo blízký říká, že to zvládneš je taky dost důležitej.

A teď když se touhle optikou dívám na tvoji situaci, jak ji tu popisuješ, tak kromě odhodlání, které z toho cítím (respekt!), tam vidím i dost rizik. Trh aktuálně taky není na tvé straně, poněkud to vychladlo a je potřeba umět víc a práci juniorům trvá najít déle než třeba před rokem.

Nerad bych tě tím demotivoval, ale v tvé situaci asi nemůžeš moc riskovat a jít do toho po hlavě bez ohledu na šance a je proto na místě spíš opatrnější přístup. ☹️

Zkusme přijít na nějakou cestu, jak by to mohlo jít. 🤔
---




--- https://discord.com/channels/769966886598737931/864434067968360459/1108854118119919667
Zajímavá pomůcka 🙂 https://www.starterstory.com/how-to-say-no
---


--- https://discord.com/channels/769966886598737931/864434067968360459/1111537040358654012
Vykouklo na mě na <:facebook:976201141924802580>: https://www.elsa.cvut.cz/wp-content/uploads/2022/11/manual-dusevniho-zdravi-vysokoskolaka.pdf
---


--- https://discord.com/channels/769966886598737931/916339896963190785/1118274720081641662

---


--- https://discord.com/channels/769966886598737931/864434067968360459/1128945673409134642
Můj první podcast! 😅 Povídáme si (nečekaně) o juniorech, na cestě za první prací v IT a juniorech v novém zaměstnání. A Vojtěch Mádr a Šárka Kousalová ze mě mámí řadu tipů, "Co dělat když...". Dotkla jsem se tak i témat, které jsem zatím v přednáškách nepokryla. Příjemný poslech 😉

https://bit.ly/43kQTxx
---


https://overcast.fm/+sSMxujIAI


https://www.facebook.com/groups/karieroviporadci/posts/1313279362724110/?comment_id=1313335772718469&reply_comment_id=1314594812592565&__cft__[0]=AZWMcRq7AQKxLajYQRUHc8KUh12uhBk86ogWa5bGWQ1G6owkzUnl2Y0mXj1vTgE04JaFMruyABkKAJuJO9Yzmnmm0VmInArKa9GB-uHnlb-o1V3HdvfPjPHQoLgUW6bzgMoNBUMhCuoes3nXwBJFemEK&__tn__=R]-R
Řešíme téma zvládání změn, zpracované je v jedné z kapitol knize "Cesta za horizont kariérového poradenství" (je ke stažení na našem webu: https://ekskurzy.cz/cs/nase-publikace) a k ní jsou navázané dvě prezentace, které máme na youtube kanálu:[ https://youtu.be/wihsODx3TqY?si=5UiMKge0YqbvnRK](https://youtu.be/wihsODx3TqY?si=5UiMKge0YqbvnRK "‌") a https://youtu.be/L18b9qJeS6A?si=-MAoJX8JtipvZQVv Kurz jsme měli jen v rámci projektu, aktuálně je možnost téma podrobněji řešit v rámci individuální konzultace.
Případně ještě kniha k posilování odolnosti "Životem s lehkostí", také zdarma na našem webu


--- https://discord.com/channels/769966886598737931/864434067968360459/1182021718919872522
Impostor syndrom. Je to vlákno, po rozkliknutí byste měli vidět navazující příspěvky. https://jawns.club/@skyfaller/111531328646480058
---


https://blog.gardeviance.org/2008/04/three-stages-of-expertise.html?m=1
https://mastodonczech.cz/@brohrer@recsys.social/112558203075404703


#} -->
