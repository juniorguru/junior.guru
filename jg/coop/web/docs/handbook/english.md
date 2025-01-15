---
title: Angličtina pro programátory
emoji: 🇬🇧
stages: [learning, preparing, onboarding, working]
description: Proč by měl programátor umět anglicky? Jak dobrá angličtina stačí? Jak se efektivně angličtinu učit, nebo si ji zlepšit?
template: main_handbook.html
---

{% from 'macros.html' import lead, link_card with context %}

# Angličtina pro programátory

{% call lead() %}
  Mnohem více než matematika je při programování potřeba angličtina. Materiály pro začačínající programátory občas existují i v češtině, ale potom už se bez schopnosti alespoň rozumět anglicky obejít nelze.
{% endcall %}

## Jak si zlepšit angličtinu

<div class="link-cards">
  {{ link_card(
    'italki',
    'https://www.italki.com/',
    'Videohovory s učiteli kdekoliv na světě.',
    badge_icon='headset',
    badge_text='Živé lekce',
  ) }}

  {{ link_card(
    'Broňa',
    'https://www.youtube.com/@BronislavSobotka',
    'Video každé úterý. Možná trochu střelený, ale <a href="https://video.aktualne.cz/dvtv/nadseny-ucitel-anglictiny-jazyk-se-nauci-kazdy-lide-ale-maji/r~f94af27a9e4c11e9970a0cc47ab5f122/">nadšený</a>!',
    badge_icon='youtube',
    badge_text='YouTube',
  ) }}

  {{ link_card(
    'Help for English',
    'https://www.helpforenglish.cz',
    'Bezplatné kvalitní materiály, testy, cvičení.',
    badge_icon='layout-text-sidebar-reverse',
    badge_text='Materiály',
  ) }}

  {{ link_card(
    'Duolingo',
    'https://cs.duolingo.com/',
    'Uč se hrou v mobilu, 5 min denně, kdykoliv, kdekoliv.',
    badge_icon='phone',
    badge_text='Mobilní appka',
  ) }}

  {% call link_card(
    'Umíme anglicky',
    'https://www.umimeanglicky.cz',
    badge_icon='list-check',
    badge_text='Cvičení',
  ) -%}
    Systém učení skrze cvičení a opakování. [Podloženo výzkumem](https://www.umimeto.org/podlozeno-vyzkumem).
  {%- endcall %}

  {{ link_card(
    'ONLINE jazyky',
    'https://www.onlinejazyky.cz',
    'Kurzy pro každou úroveň. 20 min denně.',
    badge_icon='layout-text-sidebar-reverse',
    badge_text='Kurzy',
  ) }}

  {{ link_card(
    'Meetup',
    'https://www.meetup.com/find/?source=EVENTS&location=cz--Pardubice&distance=hundredMiles&categoryId=622&keywords=english',
    'Snaž se mluvit s reálnými lidmi. Začni klidně „rukama nohama“<br>
        <small>Další setkání hledej na
        <a href="https://www.facebook.com/search/events/?q=english">FB</a>,
        <a href="https://www.foreigners.cz/meetup">foreigners.cz</a>,
        <a href="https://www.couchsurfing.com/events/search?placeid=ChIJQ4Ld14-UC0cRb1jb03UcZvg&amp;search_query=Czechia">couchsurfing.com</a>
        </small>',
    badge_icon='people',
    badge_text='Živá setkání',
  ) }}
</div>

## Jak to neflákat

Pro začátek je důležitá motivace.
Musíš pochopit, že **bez angličtiny se neobejdeš.**
Je to klíč ke dveřím do celého světa.
Vybíráš ze dvou českých mentorů, ze tří českých online kurzů, z pár lokálních firem?
S angličtinou vybíráš ze stovek mentorů, desítek kurzů.
Oslovit můžeš i mezinárodní a zahraniční firmy.

**Chybějící angličtina je v IT jako bolavý zub.** Chvíli s ním vydržíš, ale když to nezačneš řešit včas, budeš hodně litovat. Nauč se ji aspoň pasivně — pokud zvládáš číst anglický text, pochopit v něm zadání a učit se z něj nové věci, pro start to stačí.

<div class="link-cards">
  {{ link_card(
    'Jak se opravdu naučit anglicky',
    'https://www.youtube.com/watch?v=Xt7QIgzyxLk',
    'Praktický návod jak <strong>opravdu</strong> začít od <a href="https://www.youtube.com/user/BBSobotka">Broni</a>.'
  ) }}
</div>

Angličtina je důležitá, ale **i s omezenou, pasivní angličtinou se dá začít**. Pokud zvládáš číst anglický text, pochopit v něm zadání a učit se z něj nové věci, pro start to stačí.


<!-- {#

Honzovy instrukce pro Veroniku:

- Očekávaný obsah stránky viz "description": Proč by měl programátor umět anglicky? Jak dobrá angličtina stačí? Jak se efektivně angličtinu učit, nebo si ji zlepšit?
- Výsledek bude mít podobnou formu jako mental-health.md, kde je napsáno, že obsah stránky garantuje Nela, a za to je tam na ni "reklama", ale obsah je obecně použitelný.
- Cílem je lidem pomoci s tím, kde začít: Nasměrovat, vysvětlit kontext. Není cílem přepisovat něco, co už jinde na internetu je, pokud to nenapíšeme unikátně lépe. Raději odkážu, že tam a tam je dobrý materiál. Není cílem dělat dlouhé seznamy „zajímavých“ odkazů, ale vybrat jednotky těch nejlepších, nebo nejvhodnějších do startu, snížit rozhodovací paralýzu.
- Na stránce je aktuálně to, co už na JG bylo. Nemyslím si, že je to dobré, a proto vytváříme novou stránku společně. Lze to tedy všechno změnit, je to žádoucí. Podstatný je text, neřeš screenshoty atd. Stejně všemu udělám korekturu, poedituju formátování, zamyslím se nad sekcemi, apod. Nemusíš to psát sem, klidně to dej do Google Docs.
- Níže jsou moje poznámky, mnohé mají odkaz na konverzaci z klubu, kterou může být záhodno přečíst. Jak bych na této stránce pracoval já? Přečetl bych si všechny poznámky níže a pročetl odkázané klubové konverzace. Pak bych si v hlavě sesumíroval, co se mezi lidmi opakuje za otázky a jak na ně chci odpovědět. Podle toho bych strukturoval stránku a začal doplňovat jednotlivé sekce.
- Zásadní informace, která aktuálně na JG chybí a chci, aby tu byla, je, že se lidi nemají bát, pokud nemají dokonalou angličtinu. Že stačí špatná angličtina a problém je především žádná nebo velmi špatná angličtina. Ale chtěl bych v lidech vygumovat pocit, že pokud nemají nějakou BBC English, tak nemá smysl IT ani zkoušet. Nebo že potřebují certifikace, aby se dostali do mezinárodní firmy nebo startupu, což je blbost.
- Výsledek nemusí být dokonalý. Vytvoř něco, co bude jen o kousíček lepší, než co je na JG teď, a pojďme to okamžitě dát na web. Hned získáme zpětnou vazbu a hned budeme mít něco hotovo. Pak můžeme jít a zase to o kousek zlepšit. Je to lepší, než něco „tajně“ tvořit čtyři měsíce, to je strašně únavné.



https://www.youtube.com/watch?v=gv21O_A5X2k

--- https://discord.com/channels/769966886598737931/788826407412170752/1001957868565696632
<@788486062430355497>  Nevím kde jsi se ptala na tu angličtinu, ale napíšu to sem, tady to bude asi nejvíc namístě:

Z angličtiny používané ve firmách, které mají pobočku v Česku a pracují v ní převážně Češi, není potřeba mít stres.
Z mých zkušeností (ne jedné) se komunikuje na úrovni basic English s odbornou slovní zásobou, která ale čítá tak 20 základních výrazů. Žádné košaté větné struktury nikdo nevyrábí  a skvostnou oxfordskou výslovností taky trpí málokdo 🙂
Tu slovní zásobu pobereš po prvních pár meetech od kolegů. Většinu toho už budeš znát pasivně  z různých tutorálů, které kolem tebe prošly.
Jestli se základně domluvíš a jsi schopna složit větu, tak bych se angličtinou speciálně netrápila a brousila ji až za pochodu 🙂
---


---
nejvíc jsem tam postrádal  "co dělat" sekci pro lidi kteří fakt mají skoro nulovou angličtinu, tzn je problém složit i základní větu. Myslím že jich je překvapivě hodně a může být pro ně zajímavé že se na ně junior guru nevyprdlo, I když je třeba otázka jestli s IT kariérou vůbec zacnou
---


---
na co potrebuju anglictinu v it
https://discord.com/channels/769966886598737931/788826407412170752/866750581644722186
---


---
Jak je to s angličtinou, certifikáty
https://discord.com/channels/769966886598737931/769966887055392768/857365013886271488
---


---
anglictina pro IT specialisty
Nenapsal jsi, odkud jsi a jaký typ kurzu chceš, ale našla jsem nějaké kurzy zaměřené na IT, posílám níže. Jinak, ty specifické kurzy (třeba business angličtina) jsou většinou na úrovni B2-C1, když už umíš mluvit, ale potřebuješ se naučit nová slova, tak nevím, jestli to bude pro tebe užitečné.
- Brno VUT - https://www.fit.vut.cz/study/course/13867/.cs? Oni jedou dle https://www.vutbr.cz/en/rad/results/detail?vav_id=161791...
- online - https://www.onlinejazyky.cz/eshop-anglictina-v...
- online - http://www.jazykybieb.cz/anglictina_pro_it_specialisty.htmlNejefektivnější jsou individuální kurzy, ale také i nejdražší.
---


---
vyslovnost - https://www.youtube.com/@anglickavyslovnostsirenou9070, https://elsaspeak.com/
bronovy tipy?
italki
---


--- https://discord.com/channels/769966886598737931/806621830383271937/1202405712442040431
AI language learning app - Praktika AI https://praktika.ai/
To tak na me vyskoci reklama na instaci a dopadne to tak, ze si 2 hodiny povidam s AI v anglictine o svych koniccich a programovani a jeste me u toho opravuje chyby. 😁 Asi mam noveho kamarada.
---


--- https://discord.com/channels/769966886598737931/1149377645834948659/1154504124948303902
Oficiální jazyk špatná angličtina zní velmi roztomile. 😅
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1154498105362878535
V tématu <#1149377645834948659> napsal <@995699985368752178>
> Ano angličtina je potřeba pro svět IT, ale myslím že není podmínkou, nebo pokud se pletu tak mi to dejte vědět a nezbývá mi nic jiného se rozloučit. 😭
A myslím, že bude zajímavé to probrat v širší společnosti, poslechnout si více názorů.
---


--- https://discord.com/channels/769966886598737931/1154498105362878535/1154528728894947489
Za sebe můžu říct, že jsem na angličtinu sral. Pro vstup do IT stačí základy, ale jak člověk roste, musí růst i jeho angličtina. A já si to uvědomil hrozně pozdě. Protože:

a) když nevíš, googlíš. A když chceš plnohodnotný výsledek, musíš se zeptat anglicky
b) musíš to umět přečíst. Jasně, i základy stačí, ale…
c) že jsem v prdeli a svoji EN kariéru jsem posral jsem si uvědomil, když jsem došel do firmy a po pár seznámeních v češtině přišlo "Hi Kiril, this is our new frontend developer Martin" a já byl v p…, úplně, já nevěděl co říct. A od té doby… (FYI Kiril byl majitel…)
d) platit si už skoro 5 let v kuse člověka, se kterým si každý týden hodinu povídám v angličtině, je to nejlepší, do čeho jsem se v růstu dokopal
e) pak ti v životě odpadne spousta stresu. Poslechnout si prezentaci je jedna věc, ale hodit pak dotaz v angličtině, na to už má koule málokdo. A hlavně si začneš trošku věřit, nemáš problém, když potkáš cizince, si s ním povídat třeba 2 hodiny. Nemáš problém cestovat…
f) spousta kvalitního obsahu je v angličtině. A na to už základy prostě nestačí.

Já bych to uzavřel tím, že jak jsem psal, pro vstup do IT stačí základy. Ale jak rosteš, musíš růst i se svojí angličtinou. Jinak se angličtina stane tvojí slabinou a ani perfektní češtinou to nikdy nedoženeš.
---


--- https://discord.com/channels/769966886598737931/806621830383271937/1128573618541051904
Zda se učit v angličtině nebo dát přednost češtině nechám na vás, ale objevila jsem rozšíření Chromu - duální titulky pro Youtube, ale třeba i pro Udemy, takže se  zobrazují anglické titulky, ale i české. Pro mě obrovské plus, obzvlášť u složitějších témat, kdy prostě už tu angličtinu nestíhám.
https://chrome.google.com/webstore/detail/youtube-dual-subtitles/hkbdddpiemdeibjoknnofflfgbgnebcm/related?hl=cs
---


---
anglictina: https://www.deepl.com/translator
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1118637273576112128
Nový projekt „angličtina pro ajťáky“. Na první pohled něco, co na trhu podle mě trochu chybí https://geekpower.cz/
---


--- https://discord.com/channels/769966886598737931/1010552267612631132/1011571611654176829
S angličtinou doplním, ze v IT většinou stačí úroveň, která nějak dostačuje na běžnou komunikaci a umožňuje ti rozumět a umožňuje jiným lidem ti rozumět. Na bohatost slovní zásoby nebo dokonalou výslovnost se moc nepřihlíží. Takže ano, angličtina je velmi důležitá, ale není potřeba to s ni přehánět a představovat si za tím plynuly projev moderátorů z BBC.
---


--- https://discord.com/channels/769966886598737931/1089542061910413345/1089650948328136865
🇬🇧 Dodám, že slabší angličtina je v IT samozřejmě mínus, na druhou stranu **není potřeba nějaký zázrak**, nějaké porozumění psanému textu může stačit.
Co třeba tenhle text (je to úvod k jednomu kurzu), je to pro tebe nesrozumitelné?

> Simply put, computer programming is a way to make computers do different tasks. It is a process of writing a set of instructions (also known as code) that a machine can understand and making the machine follow them. The end goal might be to solve a mathematical equation, automate a boring task, or create a web page, a piece of software, a mobile app, or a whole game.
>
> Computer programming requires technical skills and creative thinking. Some call it science, some call it art.
>
> To have a full picture of what computer programming is, we need to highlight two points in the definition: "make computers do tasks" and "writing a set of instructions that a machine can understand". Let’s talk about the instructions first.
---


--- https://discord.com/channels/769966886598737931/789092262965280778/945632592810639380
Ahoj, Brno je plny cizincu, kteri se vidaji - staci mrknout na FB.
-https://www.facebook.com/callofthewoods -cizinci co jezdi na vylety. Vim, ze se poradali i pub meetingy, ale nemuzu najit odkaz.
-10 způsobů jak se rozmluvit anglicky od me oblibene lektorky - https://ninaenglish.cz/blog/10-zpusobu-jak-se-rozmluvit-anglicky/
-a mne osobne hodne pomohlo chozeni do Toasmasters - https://www.facebook.com/BrnoBusiness Jsou ceske i anglicke kluby. Toto je dobry i na ziskani sebejistoty v prezentaci 😄 Sice obcas cl musi udelat velky krok mimo komfortni zonu, ale stoji to za to!
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1001957868565696632
<@788486062430355497>  Nevím kde jsi se ptala na tu angličtinu, ale napíšu to sem, tady to bude asi nejvíc namístě:

Z angličtiny používané ve firmách, které mají pobočku v Česku a pracují v ní převážně Češi, není potřeba mít stres.
Z mých zkušeností (ne jedné) se komunikuje na úrovni basic English s odbornou slovní zásobou, která ale čítá tak 20 základních výrazů. Žádné košaté větné struktury nikdo nevyrábí  a skvostnou oxfordskou výslovností taky trpí málokdo 🙂
Tu slovní zásobu pobereš po prvních pár meetech od kolegů. Většinu toho už budeš znát pasivně  z různých tutorálů, které kolem tebe prošly.
Jestli se základně domluvíš a jsi schopna složit větu, tak bych se angličtinou speciálně netrápila a brousila ji až za pochodu 🙂
---


--- https://discord.com/channels/769966886598737931/789092262965280778/1038373495291269130
Na youtube mi přijde fajn tento kanál: https://www.youtube.com/c/PerfectWorldjazykovka

Jinak nedávno jsem narazil na zajímavou aplikaci k učení slovíček pomocí paměťové techniky: https://www.2000slovicek.cz/
---

Jak si zlepšit angličtinu: přidej se do klubu

#} -->
