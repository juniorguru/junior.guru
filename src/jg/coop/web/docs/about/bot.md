---
title: Co umí kuře, klubový Discord bot
template: main_about.html
---

{% from 'macros.html' import lead with context %}

# Kuře, klubový Discord bot

{% call lead() %}
Spoustu věcí v [klubu pro juniory](../club.md) dělá Discord bot, který se jmenuje kuře. Jo, prostě kuře. Tohle je jeho dokumentace.
{% endcall %}

[TOC]

## Co umí rychlé kuře

Je schopno reagovat okamžitě:

- **Vytváří vlákna** - Když někdo napíše zprávu do kanálů #ahoj, #past-vedle-pasti, nebo #můj-dnešní-objev, kuře pod to okamžitě vytvoří vlákno k diskuzi.
- **Vítá** - V kanálu #ahoj do vlákna ještě hned přidává každému uvítání v klubu se základními informacemi. Do vlákna přidá lidi, kteří se dobrovolně přihlásili k vítání nováčků.
- **Reaguje** - Když někdo vloží ručně inzerát do #práce-inzeráty, kuře reaguje „ĎK“. Když někdo napíše do #práce-hledám, kuře reaguje 👍
- **Dává zpětnou vazbu na GitHub profil** - Když někdo v #cv-github-linkedin vytvoří nové vlákno, tak se kuře podívá, co v něm je. Když tam najde CVčko nebo LinkedIn profil, napíše k tomu zprávu se základními informacemi a poprosí ostatní členy, aby se na to podívali. Pokud tam najde odkaz na GitHub profil, spustí [nástroj](https://github.com/juniorguru/hen), který to umí projít a poskytnout zpětnou vazbu. Tu do Discord vlákna přepošle barevně naformátovanou.

## Co umí pomalé kuře

Spouští se zhruba jednou denně. Kód „pomalého kuřete“ se prolíná se vším ostatním, co je kolem junior.guru automatizováno. Věci, které nějak souvisí s Discordem jsou tyto:

- **Vytváří týdenní souhrny** - Každý týden do #oznámení pošle zprávu, která se snaží upozornit na nejzajímavější věci, které se v klubu řešily.
- **Vytváří nápovědu a pomáhá se zaučením nováčků** - Podle předpřipravených souborů vytváří a udržuje kanál #klub-tipy, kde je nápověda na používání klubu. Nováčci v klubu mají tajný kanál, do kterého kuře jednou denně postupně posílá jednotlivé tipy, aby si je přečetli.
- **Upozorňuje na přednášky** - Když je naplánována klubová akce, do #oznámení kuře na akci posílá pozvánku. Nejdřív týden před akcí, pak den před akcí, pak v den akce.
- **Spravuje průvodce serverem** - V Discordovém průvodci je několik kanálů, které kuře spravuje. Do jednoho vypisuje základní informace a rozcestník, do dalšího seznam odkazů na záznamy klubových akcí, do dalšího seznam sponzorů junior.guru, do dalšího nápovědu k rolím.
- **Vytváří vlákna pro týdenní plány** - Každé pondělí založí nové vlákno do #týdenní-plány s označením aktuálního týdne, aby tam členové mohli psát svoje plány.
- **Spravuje některé role** - Kuře automaticky přiděluje hromadu rolí, ať už podle toho, jaké mají předplatné, nebo jestli jsou v klubu dlouho, nebo jestli hodně pomáhají (přepočítává, kolik člověk v poslední době dostal pozitivních reakcí na svoje příspěvky).
- **Spravuje zájmové skupinky** - Když si někdo v _Kanály a role_ navolí, že ho baví třeba JavaScript, dostane od Discordu odpovídající roli, např. „Zajímá mě: JavaScript“. Kuře pak projde #skupinky a lidi podle jejich zájmů přidá do vláken, které by je mohly zajímat. Pokud se následně sami odeberou, už je nepřidává.
- **Informuje v místních skupinkách o srazech** - Kuře si ze [scraperů](https://github.com/juniorguru/plucker), které běží na [Apify](https://apify.com/), stahuje informace o plánovaných programátorských srazech a jiných živých akcích. Ty pak třídí podle místa a dává o nich hezky naformátovanou správou vědět do místních skupinek. Každá skupinka si rozhoduje o tom, jaká místa odebírá, např. Pardubice odebírají akce i z Hradce.
- **Třídí pracovní inzeráty a posílá je do klubu** - Kuře si ze [scraperů](https://github.com/juniorguru/plucker), které běží na [Apify](https://apify.com/), stáhne pracovní inzeráty, pročistí data a přes LLM je vytřídí, aby zbyly ty vhodné pouze pro juniory. Co zbude nechá zobrazit na webu a naposílá to hezky naformátované na Discord do #práce-inzeráty. Protože Discord má omezený počet štítků, přepočítává je (slučuje podobné technologie pod jeden štítek). Sbírá počty reakcí a komentářů pod inzeráty, aby šly zobrazit na webu. Do tajného kanálu Honzovi dává náhodný vzorek vyřazených inzerátů, aby to mohl kontrolovat.
- **Eviduje ručně vložené inzeráty** - Pokud někdo ručně vložil pracovní inzerát do #práce-inzeráty, kuře je vede v patrnosti a upravuje připnutý příspěvek tak, aby na všechny aktuální odkazoval. Díky tomu (snad) nezapadnou v záplavě automaticky stahovaných inzerátů.
- **Seskládává newsletter a dává o něm vědět v klubu** - Pomocí LLM kuře dělá shrnutí toho, co se za poslední měsíc probíralo v klubu. Pak vezme spoustu dalších věcí a připraví z toho v [Buttondown](https://buttondown.com/) jednou za měsíc newsletter. Honza si přečte výsledek, udělá úpravy a odkline odeslání. Odeslaný newsletter kuře archivuje a dává o něm vědět do #oznámení na Discordu.
- **Seskládává podcast a dává o něm vědět v klubu** - Kuře eviduje vydané epizody podcastu. Když vyjde nová, dává o ní vědět do #oznámení na Discordu.
- **Upozorňuje na Pondělní povídání** - Každé pondělí píše zprávu do #oznámení, kde lidi upzorňuje na Pondělní povídání.
- **Spravuje špendlíky** - Pokud někdo dá na nějaký příspěvek reakci 📌, pomalé kuře mu tento příspěvek uloží do soukromé zprávy.
- **Vítá** - Když někdo napíše zprávu do kanálu #ahoj a ještě pod tím není vítací vlákno, pomalé kuře jej vytvoří a člověka uvítá zprávou se základními informacemi. Do vlákna přidá lidi, kteří se dobrovolně přihlásili k vítání nováčků. Když kuře vidí, že do klubu přišel člověk, který už v něm předtím byl, dá na zprávu o jeho příchodu reakce, aby na to upozornilo.
- **Upravuje trvanlivost vláken v klubu** - U všech fór v klubu automaticky prodlužuje tzv. _auto archive duration_ na co nejdelší, aby se jednotlivá vlákna archivovala až za týden a ne třeba za den, což je výchozí chování Discordu.
- **Reportuje Honzovi** - Do tajného kanálu kuře Honzovi píše, že někdo přišel do klubu a co napsal do políčka „odkud přicházíš“. Nebo že někdo ruší předplatné a co uvedl jako důvod.

## Infrastruktura kuřete

Backend našeho Discord bota je dvojí:

- **Rychlé kuře** - Mrňavá appka s [vlastním repozitářem](https://github.com/juniorguru/chick/), která [neustále běží](https://juniorguru-chick.fly.dev/) na [Fly](https://fly.io/) a má na starosti pár věcí, kde je potřeba okamžitá odezva. Je to skutečný bot, který se jako kuře připojí na Discord a reaguje na věci, které se tam napíšou. Tento kód ale nic nepřepočitává, nic nikam neukládá a neeviduje si žádný stav čehokoliv. Prostě jen reaguje na skutečnosti: zakládá vlákna, rozdává emoji…
- **Pomalé kuře** - Minimálně jednou denně v noci, nebo pokaždé, když Honza udělá `git push` do [hlavního repozitáře s kódem](https://github.com/juniorguru/junior.guru), se spustí [build na CircleCI](https://app.circleci.com/pipelines/github/juniorguru/junior.guru?branch=main). V rámci něj proběhnou desítky skriptů, které něco stahují, synchronizují, přepočítávají, vše uloží do SQLite a nakonec z těch dat vybuildí celou junior.guru MkDocs webovku, kterou si právě čteš. Skripty, které něco dělají na Discordu, se tam připojují a navenek tváří jako kuře.

## Proč jsou rychlé a pomalé kuře zvlášť

Celé junior.guru je navrženo tak, aby jej Honza mohl provozovat v jednom člověku. Jenže každou aplikaci, která má běžící _runtime_, je potřeba monitorovat, a když spadne, je potřeba řešit, proč spadla, a nahodit ji, aby služby a funkce, které na ní závisí, fungovaly.

V tomto směru je z hlediska _work-life balance_ lepší noční přepočet. Buď se vše povede, nebo to spadne, ale pak má člověk spoustu času to opravit. Webovka je statická a běží, i když třeba v mírně neaktualizované verzi. Fungování klubu není krátkodobě závislé na tom, jestli někde spadl nějaký složitý skript. Když začně _nightly build_ o víkendu padat, Honza to opraví v pondělí, pohoda.

Dříve ani rychlé kuře neexistovalo, klub si vystačil s pomalým. Časem ale Honza uznal, že UX by v některých věcech byla o dost lepší, kdyby se odehrály okamžitě. A tak vzniklo rychlé kuře, které sice jede pořád a může kdykoliv spadnout, ale zase je dost jednoduché na to, aby nebylo obtížné jej restartovat, nebo rychle opravit. A když na pár dní spadne pomalé kuře, základní UX v klubu tím není zasaženo.

## Co ještě se tváří jako kuře

Robotickou identitu kuřete si propůjčují i jiné systémy, které komunikují s členy klubu. Například pro správu uživatelských účtu a placení se používá systém [Memberful](https://memberful.com/). Ten posílá různé e-maily, např. že vyprší členství, nebo že se nepovedlo strhnout platbu z karty. Tyto jsou psány jako „Ahoj, tady kuře“, aby se rozlišilo, že jsou automatické a nepíše je přímo Honza, ale s kódem Discord bota nemají vlastně nic společného.
