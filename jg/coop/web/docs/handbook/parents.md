---
title: Rodiče v IT
emoji: 👶
stages: [thinking, preparing, applying]
description: Jak na kariéru v IT během rodičovství? Mateřská, rodičovská, částečný úvazek, programování s dětmi a mnoho dalšího.
template: main_handbook.html
---

{% from 'macros.html' import lead, link_card, note, blockquote_avatar with context %}

# Rodičovství a kariéra v IT

{% call lead() %}
Jak se dá s programováním kombinovat mateřská nebo rodičovská?
Je těžké najít v IT práci na částečný pracovní úvazek?
Jak prezentovat péči o děti v životopisu?
A mohou programovat i děti?
{% endcall %}

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }} Kapitola se teprve připravuje.
{% endcall %}

## Programování pro děti

Proč učit děti programovat? Jak začít? Kdy začít?
Přečti si [článek Luboše Račanského](https://www.heroine.cz/zeny-it/7677-u-budoucich-ajtaku-je-nejdulezitejsi-touha-nespokojit-se-s-prvnim-resenim-rika-lektor-programovani-pro-deti), který to celé krásně vysvětluje.

{% call blockquote_avatar(
  'Z dítěte se základy programování může být jednou šikovný soustružník, který si na pomoc vezme CNC stroj. Nebo umělec – jako sochař Michal Trpák, který vytváří 3D tisk z betonu. Nebo zemědělec, který bude chtít použít co nejméně hnojiv a co nejlépe zacílit zavlažování. Případně politik, který se v době pandemie bude muset rozhodovat na základě obrovské sady dat.',
  'lubos-racansky.jpg',
  'Luboš Račanský'
) %}
  Luboš Račanský, lektor kroužku pro děti a autor článku [U budoucích ajťáků je nejdůležitější touha nespokojit se s prvním řešením, říká lektor programování pro děti](https://www.heroine.cz/zeny-it/7677-u-budoucich-ajtaku-je-nejdulezitejsi-touha-nespokojit-se-s-prvnim-resenim-rika-lektor-programovani-pro-deti)
{% endcall %}

Pokud tě láká to zkusit a trénovat s dětmi [informatické myšlení](https://cs.wikipedia.org/wiki/Informatick%C3%A9_my%C5%A1len%C3%AD), následující odkazy tě nasměrují na stránky, které jsou vhodnější než junior.guru. I když je v názvu tohoto webu slovo _junior_, není pro děti.
Slovem junior se označují začátečníci na pracovním trhu a tento web ukazuje cestu k programování a kariéře v IT dospělým, případně dospívajícím lidem.

### Kde začít

Programování pro děti se odehrává v **barevném prostředí, kde jde s dětmi vytvářet zábavné příběhy, hry, animace**. Rozhodně by nemělo spočívat v psaní písmenek na černou obrazovku nebo v práci s Wordem.

<div class="link-cards">
  {{ link_card(
    'Code.org',
    'https://code.org/',
    'Programování, které zvládne každý rodič, kroužek, družina.'
  ) }}

  {{ link_card(
    'ScratchJr',
    'https://www.scratchjr.org/',
    'V mobilu nebo na tabletu, pro nejmenší děti.'
  ) }}

  {{ link_card(
    'Scratch',
    'https://scratch.mit.edu/',
    'Vytvoř hru nebo příběh a sdílej je s kamarády.'
  ) }}
</div>

### Pro nadšence

Zkusili jste s dětmi programování a fakt hodně vás to baví?
Možná by z tebe mohl být nadšenec!
Tady máš pár odkazů, které by tě mohly inspirovat.

<div class="link-cards">
  {{ link_card(
    'Proč a jak učit děti programovat',
    'https://www.youtube.com/watch?v=WHwD8AgpQG8',
    'Iva a Martin Javorkovi o svých začátcích s kroužkem programování.',
    badge_icon='play-circle-fill',
    badge_text='Přednáška',
  ) }}

  {{ link_card(
    'Lubošův kroužek programování',
    'https://blog.zvestov.cz/tag/krou%C5%BEek-programov%C3%A1n%C3%AD/',
    'Články o tom, jak Luboš Račanský rozjel a provozuje kroužek programování.',
    badge_icon='book',
    badge_text='Blog',
  ) }}

  {{ link_card(
    'Příručka pro pedagogy a rodiče',
    'https://github.com/xsuchy/programovani_pro_deti/#readme',
    'Mirek Suchý sesbíral do jednoho dokumentu vše, co šlo.',
    badge_icon='book',
    badge_text='Příručka',
  ) }}
</div>


<!-- {#

děti https://www.coderebels.cz/
(nepřesunout do parents.md?)
https://twitter.com/programohrajeme/status/1462698199001489411

- Magda https://mail.google.com/mail/u/0/#inbox/KtbxLrjGQcnLHJfGrPfPsPdVzHDfvDThLB

https://imysleni.cz/ucebnice/zaklady-programovani-v-jazyce-python-pro-stredni-skoly

Privydelek na materske
- vpp na mateřské
- OSVČ sám/sama prozovovat znamená přijít o podporu v mateřství
- https://aperio.cz/vydelecna-cinnost-behem-materske-rodicovske-dovolene/
- https://mail.google.com/mail/u/0/#inbox/KtbxLrjGQcnLHJfGrPfPsPdVzHDfvDThLB

Mateřská do CVčka
https://www.facebook.com/groups/344184902617292/?multi_permalinks=1416009175434854&hoisted_section_header_type=recently_seen&__cft__[0]=AZX4mzGVPa_P2Iuqw8iBcu51l11OI8YNPC2j94QuZ7XlKAbbAZmGGVvygoehieSM2S8L4KvqMJ7Lnr32RKwQs0EoCROhY15hIGqSCvc7Cn3ZAioPYC2ekaS6YDWwpN39x89rrUtAxXFxi32aTG2JcCs3EWaQuLoTdkaBChAcmqoRxtk3a8c4OoiNO5FhmS8IS4Y&__tn__=%2CO%2CP-R

https://www.bbc.com/worklife/article/20210617-does-motherhood-belong-on-a-resume

rady ohledně děr v CV a mateřské
https://www.linkedin.com/posts/honzajavorek_%C4%8Dl%C3%A1nek-na-bbc-rozeb%C3%ADr%C3%A1-zda-pat%C5%99%C3%AD-p%C3%A9%C4%8De-o-activity-6851398868228198400-y6fc

co říkají matkám na pohovorech
https://www.facebook.com/groups/123305571039874/?multi_permalinks=4856613921042325&hoisted_section_header_type=recently_seen

https://zpravy.aktualne.cz/ekonomika/vodafone-nabidne-u-vsech-pozic-castecny-uvazek-cesko-s-flexi/r~40c55cf6c47c11ebbc3f0cc47ab5f122/

https://www.linkedin.com/in/kaitlynchang/
(featured) https://www.linkedin.com/feed/update/urn:li:activity:6854922239847006208/

- zalohy nemusis platit kdyz jsi na materske nebo student, Zmínila bych ještě rozdíl mezi podnikáním jako hlavní a jako vedlejší činnost.
- https://twitter.com/_hospa/status/1333552886853357569
- https://www.facebook.com/groups/junior.guru/permalink/502624567327822/?comment_id=502647810658831
- https://marter.cz/
- https://medium.com/@lenka.stawarczyk/pro%C4%8D-si-%C5%BEeny-p%C5%99i-hled%C3%A1n%C3%AD-pr%C3%A1ce-nev%C4%9B%C5%99%C3%AD-a-nejsou-sp%C3%AD%C5%A1-jen-vyb%C3%ADrav%C3%A9-a50c936fb805
- https://www.linkedin.com/posts/femme-palette_weve-released-a-new-e-book-about-balancing-activity-7018836400825376768-A6R8
- https://projekty.heroine.cz/zeny-it

„Většina matek chce dál pokračovat. Často se samy ozvou, jestli pro ně něco máme, a vždycky máme. Pokaždé existuje nějaký malý projekt, který jim můžeme dát. Nebo chodí školit juniory. Ony jsou nadšené, my jsme nadšení,“
https://denikn.cz/279531/koncici-sefka-slevomatu-muzi-si-me-na-jednanich-pletli-s-obsluhou-zeny-se-podcenuji-a-boji-se-selhani/?cst=91370c7fe392f469f161d9e86d3e151e0e237c39

https://mamajob.online/

--- https://discord.com/channels/769966886598737931/788832177135026197/990538199308853278
Dneska na mě facebook vyhodil Strojové učení pro děti:
https://www.donio.cz/ucebnice-umele-inteligence-pro-deti?fbclid=IwAR3_mBSfWFSQYHnGUEhNm0sDopBkZGOQwmZaCi3IvyRvOK7eOiij1YeGFtE

Myslím, že tohle potřebuju 😄 Kromě toho že to je Strojové učení pro děti, chápete, jako vysvětlený pro děti, 😁  , tak to am podle všeho dělaj ve Scratchi 😄
---


--- https://discord.com/channels/769966886598737931/769966887055392768/982900261263646821
<@933738477449785384> Mateřská mi funguje 24/7/365. <:lolpain:859017227515854879> Mám tři velice aktivní kluky 23 měsíců, 4 roky a 6 let. Škola nám teď naštěstí teprve začne, to ještě bude tóčo. Hlídání nulové, jen když se manžel občas zapojí o víkendu. Večer nic nedělám, protože chci aspoň ten večer chvíli strávit s manželem, pokud mě teda nezabaví na celý večer nejmladší a neusnu s ním. 😄

A kdy se tedy učím? Když jsou starší dva kluci ve školce a nejmladšího uspim po obědě. (Bohužel zrovna teď nastal čas, kdy mi po obědě nechce už moc spát.) A zbytek o víkendech, případně v týdnu navečer chvilky a výjimečně když se děti na chvíli něčím zabaví. "Hlídání" televizí odmítám, protože kluci pak akorát víc zlobí, takže tam používám časovač na televizi, abych to nemusela sledovat (přičemž vím, na co se koukají a je okolo toho hodně debat, co povolím) a někdy tak získám taky chvilku - aspoň od starších, nejmladšímu nic ještě nepouštím.

Teď, jak začnu pracovat, tak se budu muset s manželem už domluvit, aby mě od dětí odstínil pravidelně, jestli to nemám dělat večer a víkendy, když mi nejmladší háže vidle do toho spaní. Manžel sám mi na začátku tvrdil, že si to představuju moc jednoduše, jak se dostanu do IT, takže chápe, že když už tam jsem, že to mé úsilí k něčemu je a je zapotřebí.
---

http://www.zasnem.cz/2023/04/26/maly-hacker/
https://cc.cz/matkam-a-firmam-pomaha-skloubit-praci-a-rodinny-zivot-vetsina-manazeru-svym-lidem-neveri-rika/

--- https://discord.com/channels/769966886598737931/788826407412170752/1209840122757914644
💪
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1223179054039961711
Co si přesně představit, když v inzerátu vidím jako jeden z benefitů: "pro-rodinný přistup" a podobné mutace téhož? Je mi jasný, kam asi míří, ale zajímalo by mě, jak to potom funguje prakticky (Jsou posunuté core hours, aby všichni stihli zajet do školky? Nejsou core hours vůbec? Výplaty jsou ve formě kindr vajec? 🤔)

P.S. Nemůžu teď dohledat ten konkrétní inzeráta, velmi výjimečně na to narazím a jaksi přirozeně to se mnou rezonuje.
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1222146790460231710
Když se tady říká part time, tak se neříká se jak moc „part“: 80 % vs. 60 % vs. 20 % je velký rozdíl.
Taky je rozdíl, jestli někdo pracuje každý den, jen kratší dobu nebo jsou celé dny, kdy tam není. Stejně tak může být ok, že je někdo dostupný jen 4 hodiny dopoledne a jinde je zase lepší, když je dostupný 2 hodiny dopoledne a 2 hodiny odpoledne.
Samozřejmě záleží na typu práce a tom, jak je to kde organizované.
---


--- https://discord.com/channels/769966886598737931/797040163325870092/1221400946928652339
OK, tak možná ať si zkusí projet tohle https://blockly.games/?lang=en používáme to i s dospělými, co nikdy neprogramovali, aby si rozvičili mozky tím správným směrem, než začnou psát kód (i když trochu kódu se píše i tam ke konci) (a třeba malování želvou mě jednou chytlo tak, že jsem u toho seděl pár hodin 😅)
---


https://www.linkedin.com/company/mamajob/
https://www.aperio.cz/clanky/navrat-do-zamestnani-po-materske-rodicovske-dovolene


#} -->
