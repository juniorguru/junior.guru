---
title: Spolupráce při programování
emoji: 👯
stages: [learning, creating]
description: Programátoři pracují v týmech. Zkus si to ještě předtím, než budeš mít svou první práci v IT
template: main_handbook.html
---

{% from 'macros.html' import blockquote_avatar, illustration, lead, link_card with context %}


# Jak se naučit pracovat v týmu

{% call lead() %}
  Programátoři pracují v týmech.
  Když si spolupráci aspoň vyzkoušíš, nejen že budeš mít před ostatními náskok, ale taky tě to ohromně posune.
  Ve skupině je vše veselejší, učení rychlejší, motivace nezlomnější.
{% endcall %}

{{ illustration('static/illustrations/collaboration.webp') }}

[TOC]

## Zkus „hackathon“

[Hackathon](https://cs.wikipedia.org/wiki/Hackathon) je akce, kde se sejdou lidi se zájmem o nějaké téma, utvoří smíšené týmy (zkušení i začínající programátoři, designéři) a v daném čase vymyslí a zpracují nějaké řešení. Nejlepší někdy dostanou ceny. Pro lepší představu si přečti [článek od účastnice Michaely](https://medium.com/@misasebestova/m%C5%AFj-prvn%C3%AD-datov%C3%BD-hackathon-6f753a4730cf).

<div class="link-cards">
  {{ link_card(
    'Hackathony v Česku',
    'https://www.facebook.com/groups/hackathony.cz/',
    'Největší koncentrace tipů na hackhathony v Česku.
        <small>Někdy ale může být nejlepší prostě
        <a href="https://www.google.cz/search?q=hackathon%20ostrava">hledat</a>.
        </small>'
  ) }}

  {{ link_card(
    'Hackathony - co a jak',
    'https://docs.google.com/presentation/d/1reYrzFy3E3LS-jNzQecLbkf6Qq7iIEjWvXCyvbw389E/',
    'Všechny základní informace o hackathonech na jednom místě.'
  ) }}
</div>

{% call blockquote_avatar(
  'Moji největší bariérou byl strach. Obava, že nebudu tak dobrá jako ostatní a že tam budu úplně mimo. Nakonec jsem zjistila, že to bylo úplně zbytečné.',
  'michaela-sebestova.jpg',
  'Michaela Šebestová',
) %}
  Michaela Šebestová, absolvetnka kurzu [PyLadies](https://pyladies.cz/) a [účastnice hackhatonu Sreality.cz](https://medium.com/@misasebestova/m%C5%AFj-prvn%C3%AD-datov%C3%BD-hackathon-6f753a4730cf)
{% endcall %}


## Zkus „open source“

[Open-source software](https://cs.wikipedia.org/wiki/Otev%C5%99en%C3%BD_software) (OSS) jsou projekty s kódem, na který se může kdokoliv podívat, a které lze většinou využívat zdarma — například [Linux](https://cs.wikipedia.org/wiki/Linux) nebo [LibreOffice](https://cs.wikipedia.org/wiki/LibreOffice). Pokud si [dáš svůj projekt na GitHub](git.md), kde jeho kód mohou číst další lidé, máš taky takový maličký open source. I tyto webové stránky [jsou open source](https://github.com/juniorguru/junior.guru).

Existují tisíce open source projektů uveřejněných pro dobro všech, některé více či méně užitečné, některé vytvářené ve volném čase lidí, jiné zaštiťované organizacemi. Je to obrovský fenomén a když se do něj člověk zapojí, může získat mnoho zkušeností, cenných kontaktů i nových přátel.

### Nemusíš jen programovat

Open source není jen o programování. Pokud se zatím necítíš na psaní kódu, [je i hodně jiných způsobů, jak můžeš přiložit ruku k dílu](https://opensource.guide/how-to-contribute/#what-it-means-to-contribute). Např. psaním dokumentace, psaním článků, navrhováním grafiky nebo „procházením GitHub Issues“ (anglicky _triaging_, hezky popsáno v článku [How to fix a bug in open source software](https://opensource.com/life/16/8/how-get-bugs-fixed-open-source-software)).

### Open source jako inspirace

Do open source nemusíš hned přispívat. Ze začátku se můžeš hodně naučit i pouhým pozorováním, čtením cizího kódu, hledáním inspirace. Můžeš se např. podívat, [jak jiní lidé naprogramovali piškvorky v Pythonu](https://github.com/search?l=Python&q=tic-tac-toe).

### Jak začít?

Začátky s open source nejsou přímočaré. Většinou na něm lidé pracují ve volném čase. Nováčci jsou vítáni, ale jen málo projektů má sílu aktivně nabízet [mentorování](mentoring.md). Nejsnazší cesta vede přes různé programy a stáže, jako např. [Google Summer of Code](https://summerofcode.withgoogle.com/), ale nejčastěji se lidé k open source dostanou posloupností „vidím rozbitou věc, spravím, pošlu opravu“.

{% call blockquote_avatar(
  'Stáž na veřejném softwarovém projektu přes Outreachy mi změnila život. Učící křivka byla strmá, ale pomoc komunity kolem projektu byla ohromná. Naučila jsem se všechny běžné postupy, jak se co správně dělá, jak se komunikuje.',
  'lenka-segura.jpg',
  'Lenka Segura',
) %}
  Lenka Segura v [rozhovoru pro CyberMagnolia](https://web.archive.org/web/20221204155402/https://cybermagnolia.com/blog/page/2/), bývalá agrochemička
{% endcall %}

{% call blockquote_avatar(
  'Moje začátky se nesly v duchu: Vidím rozbitou věc, spravím, pošlu opravu. Tím si člověk vybuduje jméno. Stačí jen otevřít GitHub, všechno je rozbitý.',
  'tomas-janousek.jpg',
  'Tomáš Janoušek',
) %}
  Tomáš Janoušek, profesionální programátor, ve [svém tweetu](https://twitter.com/Liskni_si/status/1224359360517877762)
{% endcall %}

<div class="link-cards">
  {{ link_card(
    'Open Source Guides',
    'https://opensource.guide/',
    'Přečti si vše o tom, jak OSS funguje, a jak začít.'
  ) }}

  {{ link_card(
    'Česko.Digital',
    'https://www.cesko.digital/',
    'Přidej se do sdružení dobrovolníků okolo OSS projektů s pozitivním dopadem na Česko.'
  ) }}

  {{ link_card(
    'GISMentors',
    'https://gismentors.cz/',
    'Účastni se kurzů nebo školení na OSS související s geografií.'
  ) }}

  {{ link_card(
    'Outreachy',
    'https://www.outreachy.org/',
    'Získej stáž na OSS pro znevýhodněné skupiny.',
    badge_icon='door-open',
    badge_text='Pro znevýhodněné',
  ) }}

  {{ link_card(
    'Google Summer of Code',
    'https://summerofcode.withgoogle.com/',
    'Pracuj na OSS při studiu, během letních prázdnin.',
    badge_icon='pen',
    badge_text='Pro studenty',
  ) }}

  {{ link_card(
    'Google Code-in',
    'https://codein.withgoogle.com/',
    'Účastni se úvodu do OSS pro mládež, vyhraj ceny.',
    badge_icon='pen',
    badge_text='Pro studenty',
  ) }}

  {{ link_card(
    'Rails Girls SoC',
    'https://railsgirlssummerofcode.org/',
    'Přihlaš svůj tým a po několik měsíců pracuj na OSS.',
    badge_icon='gender-female',
    badge_text='Pro ženy',
  ) }}

  {{ link_card(
    'CodeTriage',
    'https://www.codetriage.com/',
    'Najdi rozbitou věc, oprav ji, pošli opravu autorům.'
  ) }}

  {{ link_card(
    'Awesome OSS Mentors',
    'https://github.com/lenadroid/awesome-oss-mentors#readme',
    'Kontaktuj někoho z těch, kdo se sami nabízí zaučovat nováčky na OSS projektech.'
  ) }}
</div>


<!-- {#

https://github.com/firstcontributions/first-contributions

A recent trick I discovered to learning this is to pick an open source project written by developers you like and start writing docs and tests.
https://twitter.com/hamelhusain/status/1296601185470709760

Talk to maintainers
https://twitter.com/simonw/status/1293017371536265221

--- https://discord.com/channels/769966886598737931/788832177135026197/1062732102237437973
Pěkný materiál pro prvo-přispěvatele/ky na GitHubu: https://github.com/firstcontributions/first-contributions
---

https://opensource.net/why-single-vendor-is-the-new-proprietary/
That approach led to a lot of excesses, especially as Microsoft decided to exploit that dominant position. Openly-developed Open Source software grew in the 90s in reaction to this evil proprietary approach. In this model, software is produced as a commons by a community of organizations and individuals openly collaborating, and value is shared among the participants in the community. This is all made possible thanks to free and Open Source licenses which guarantee a number of freedoms, like the freedom to build on it without asking for permission, and the freedom to use it for any purpose, including making money.

Don't contribute to open source
https://www.youtube.com/watch?v=5nY_cy8zcO4


https://davidism.com/school-assignment-open-source/

--- https://discord.com/channels/769966886598737931/1401948283361955940/1504830281608204459
Největší slabiny juniorních projektů oproti praxi jsou:

- malá nekomplexní neprodukční codebase
- a nula zkušeností s prací, organizací práce a komunikací v týmu.

Junior ale nemůže udělat víc, než si zajistit nějaké vlastní projekty, takže to firmy berou jako dobrý začátek. Pokud má někdo zkušenost se spoluprací v týmu nebo na větší codebase, třeba na open sourcu nebo nějakém dobrovolnickém projektu, je to velký a významný bonus, ale je tak těžké se kolem něčeho takového vyskytovat, že to po lidech nelze vyžadovat a nastavovat takhle laťku.

A moje pointa: Ani jedno z toho ti AI nedá. Takže podle mě ti to nijak nepomůže obejít komerční praxi. Jasně, můžeš vyrobit vlastní funkční produkt a nahodit ho, ale to je vlastně jiná disciplína, než práce programátora 🙂 To se bavíme o nějakém produktovém nebo podnikatelském myšlení. Pokud to někde ocení, bude to plus, ale pro práci programátora v tradičním slova smyslu to je podle mě bonusová věc do boku, ne něco, u čeho by si při náboru řekli: „jo tak když si dokázal udělat vlastní appku a na app storu ji už používá 10 lidí, tak to asi zvládne pracovat na našem produktu o 400.000 LOC (lines of code) a komunikovat v týmu 10 lidí přes Slack, Jiru, a koordinovat se s kolegama...“, to podle mě nefunguje.
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1478343159615455243
👋 Ahoj komunito!
Jdu sem ukázat, co děláme a co si myslím, že je docela cool :)) 

## Začátek 
Učil jsem v Czechitas testování na API vrstvě a chyběla mi nějaká aplikace, na které bych to dokázal dobře ilustrovat - aby tam byl frontend a byly ta možné základní operace - bez přihlášení, po přihlášení. A tak jsem po večer začal bastlit Czechibank - appka, kde si můžeš posílat mezi sebou Czechitokeny, vytvářet bankovní účty, swagger dokumentace included. Odučil jsem první rok na tom a viděl jsem, že to potřebuje dopilovat, že dokumentace neodpovídala úplně realitě atd..

## Nápad
A tak mě napadlo, že zkusím nabrat lidi do vývoje a QA. A že z toho udělám další projekt, kde se lidi můžou učit. Učit procesy, mít reálný projekt, který opravují, vyvíjejí, testují něco, co se reálně bude používat (byť zase na učení). A tak jsem založil JIRA, github organizaci, Discord server a nadhodil to v Czechitas discordu, že kdo chce, tak se může takhle vzdělávat a já můžu dát feedback. 

## Jak to funguje?
Máme tým devs a QA, já zajišťuju mentoring a pozici PO. V dev týmu máme zkušenou vývojářku, já dělám QA už cca 10 let, tak pomáhám zase tam (byť dělám hlavně vývoj na Czbank). A jedeme Kanban, žádný stres, prostě na co máš čas, to uděláš. Každý říká, kolik hodin tomu může dát týdně, ale ve výsledku je to mnohem méně (máme vždy velké oči na začátku :)) ). V backlogu máme nějaké tickety, které se mají udělat (třeba opravit dokumentaci, nové features, devops věci, prostě to, na co jste zvyklí z SW vývoje). Vývojář si ticket vezme, udělá, následuje code review jiného vývojáře a pak si ticket převezmou QA lidi a otestují (chceme mít Preview appky, ale zatím bojujeme s Coolify a Better-auth). 
QA má taky Zephyr v JIRA na testcasy, takže máme sadu testů na FE, tak na API. 

Víc ve vlákně:  🧵
---


#} -->
