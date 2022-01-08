---
title: Proč mít a jak si vyladit LinkedIn profil
description: Proč by měl mít každý junior v IT profil na síti LinkedIn? Jak jej vyladit, aby ti pomohl s hledáním práce?
template: main_handbook.html
---

{% from 'macros.html' import lead, note, blockquote_avatar with context %}

# Profil na LinkedIn

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }} Tuto stránku Honza právě přepisuje. Za pár dní tady bude jiný text, lepší, voňavější, nápomocnější.
{% endcall %}

<!-- {% call lead() %}
  Bla bla
{% endcall %} -->

Základem v dnešní době je mít **co nejlépe vyplněný [profil na LinkedIn](https://www.linkedin.com/in/honzajavorek)**. Většinou stačí poslat odkaz na svůj LinkedIn a krátký průvodní dopis — není potřeba přikládat ještě zvlášť sepsaný životopis ve Wordu nebo v PDF. Zajímavým doplňkem životopisu může být tvůj [osobní web](../candidate-handbook.md#osobni-web-a-blog).

**Životopis piš anglicky, česká verze je zbytečná.** Větší firmy mají buď přímo mezinárodní kolektiv, nebo i tak vyžadují nějakou úroveň znalosti angličtiny. Ani ryze české firmy s angličtinou nebudou mít problém, v IT je to standard.

**Hledej na internetu klíčovou frázi „[Killer CV](https://www.google.cz/search?q=killer%20cv)“**. Pod tímto pojmem najdeš spousty článků i videí o tom, jak napsat životopis, který rozhodně nezapadne. Jsou sice o klasických CV, ale většinu rad lze snadno použít i na LinkedIn. Další dobré tipy jsou i v [Tech Interview Handbook](https://yangshun.github.io/tech-interview-handbook/resume) nebo na [prace.rovnou.cz](https://prace.rovnou.cz/jak-zivotopis.html).

Jedna z těch zásadnějších rad je **začít jasným shrnutím**: _„I am a recent graduate of the [PyLadies](https://pyladies.cz/) beginner course, currently contributing to [Česko.Digital](https://cesko.digital/) with their open source projects. My focus is on Python, which I would like to apply in Data Science.“_ Dalším dobrým tipem je mít u každé minulé pozice na čem přesně se pracovalo, naučené dovednosti a největší úspěchy. Ovšem pozor — životopis není seznam všeho, co máš za sebou od střední školy, ale **letáček, který tě má prodat jako zajímavého kandidáta**.

{% call blockquote_avatar(
  'Pro recruitery je hlavní se hned zorientovat. Klíčový je souhrn — co umíš za technologie? Jaké tě baví? Kam směřuješ? Potom seznam pozic a na čem jsi pracoval.',
  'pavel-brozek.jpg',
  'Pavel Brožek'
) %}
  Pavel Brožek, recruiter v [dreamBIG](https://www.dreambig.cz/)
{% endcall %}

**[Projekty](cv.md#6-projekty) jsou pro juniora nejdůležitější věc hned po kontaktních údajích a úvodu**, tak ať jsou hezky vysoko a viditelně. Zmínka o GitHub profilu nestačí, uveď konkrétní projekty, kterými se chceš pochlubit, trochu je popiš, přidej odkaz na každý z nich.

**Drž se pravdy.** Pokud máš přečtené tři články o [MongoDB](https://cs.wikipedia.org/wiki/MongoDB), napiš, že víš co to je, ale netvrď, že s tím umíš pracovat. Jestliže něco přibarvíš, na pohovoru se na to vždy snadno a rychle přijde. Budeš akorát působit nevěrohodně.

{% call blockquote_avatar(
  'Někdo se chlubí: Scala, Groovy, Kotlin. Nadchne mě to, ovšem hned dostanu studenou sprchu, protože neví, jaký je mezi nimi rozdíl.',
  'lubos-racansky.jpg',
  'Luboš Račanský'
) %}
  Luboš Račanský, profesionální programátor, autor článku [O náboru juniorů](https://blog.zvestov.cz/software%20development/2018/01/26/o-naboru-junioru.html)
{% endcall %}

<small>Rady v této podkapitole volně vychází mimo jiné i ze [článku recruiterky Simony Liptákové](https://research.redhat.com/blogs_cpt/how-to-hack-your-cv-7-useful-tips-for-students-with-no-work-experience/). Díky!</small>

<!--
Ja bych si dovolila nesouhlasit. Ja mám LinkedIn jen velmi stručný a životopis VŽDY šíji na míru dané pozici. Nemyslím si, že jeden životopis je aplikovatelný na více pozic. Toto bych osobně doporučila všem.

Ahoj, když nemám žádné předchozí zkušenost v IT, zatím jsem dělal jen to CNC, tak má cenu si vůbec zakládat Linkedin účet? Resp. chápu takový profily u zkušenějších lidí, co třeba přechází z jiné firmy na vyšší pozici v rámci IT, ale když jsem absolutní junior, má vůbec cenu si ten profil zakládat, pokud si hledám první práci v IT?

LinkedIn profil je jako CVčko. Můžeš si ho založit i kdybys byl kuchař a není to nic proti ničemu, akorát že na LI nebude možná moc restauratérů, tak to nebude mít valný efekt v tom, že by ti tam zrovna denně chodily nabídky práce.
Obecně založení profilu juniorovi nestačí, je potřeba nějak networkovat, přidávat si lidi, atd., aby na ten profil někdo vůbec narazil. Je to jako FB profil bez kamarádů, založit si ho můžeš, ale moc parády s tím neuděláš.
Pokud jde o to, zda má smysl se bez zkušeností se softwarovým vývojem začít ucházet o práci vývojáře, to smysl moc nemá. Je dobrý se nejdřív něco naučit, pak si to na něčem vyzkoušet (vlastní projekt) a pak teprve hledat práci. Nevím, v jaké fázi přesně jsi, ale něco mi říká, že tahle moje příručka by se ti mohla hodit pročíst https://junior.guru/candidate-handbook/, případně v kondenzované podobě v článcích zde https://www.heroine.cz/clanky/autor/70000223-honza-javorek

z osobní zkušenosti někoho, kdo těch firem prolezl fakt hodně - v prvním odstavci jsou sice krásné ideály, ale ani místní HR z velké většiny LinkedIn profily neumějí číst - nebo prostě ze své arogance to nemají za potřebí. Studii o tom sepsal už Pavel Šimerda, odborník na LinkedIn HR to IT komunikaci.

Jinak ad LI - je super to mít pěkně vyplněné, ale jakmile stáhneš LI profil jako pdf, je to strašlivé ošklivé a imho nereprezentativni.  Doporučuju urcite udržovat i samostatnou verzi CV.

jako doporuceni bych jeste uvedl aby to byl jen stazeny LinkedIn profil do PDF ale aby to melo trochu lepsi formu, idealne i lepsi styl nez jen strohy Word dokument

Zaujímali by ma ešte nejaké tipy ako prilákať recruiterov na LinkedIne, aby ma oslovovali s relevantnými ponukami. Je mi jasné, že je to všeobecný boj, ostatne o tom už boli snáď nejaké diskusie aj tu ak si dobre spomínam. Momentálne mám nastavené “Open to work” a mám tam vybraté Junior frontend/software/react engineer/developer, aj tak mi však chodia ponuky takmer výhradne na Senior Python QA 🙂 To, o čom hovoril Honza vyššie mi dáva zmysel v CV, ale CV je predsa len trochu súkromnejšie ako LinkedIn profil, kde mať hneď pod menom inú rolu ako má človek v súčasnosti a uvidí to celá jeho firma… V “About” sekcii mám momentálne iba odkaz na GitHub, ale nie som si úplne istá, či sa recruiteri pri scrollovaní dostanú až tak ďaleko, takže ten Headline bude asi jediná možnosť 🤔 Čo pomohlo vám dostávať relevantné ponuky ak ste boli v rovnakej situácii?

A to vadí? Pokud tam nechceš zůstat (a to bych s Kiwi a jeho „specifickou“ firemní kulturou docela čekal a asi i doporučoval zkusit to jinde, už jen pro srovnání), tak je to asi jedno. Maximálně si tě budou snažit udržet a nabídnou ti místo ve vývoji nebo víc peněz. 🤷‍♂️

Myslím, že recruiteři takto píšou asi hlavně zkušenějším lidem, případně je to ten typ, co posílá „všechno všem“. Asi mě napadá jen vyhlednout si konkrétní firmy, kde by se ti líbilo pracovat, najít jejich interní recruitery na LI, přímo si je přidat a případně jim přímo i napsat, ze hledas a jestli něco nemají.

Do About sekce bych napsal tu úvodní větu z CV. I kdybych měl na LI svou aktuální pozici, ta úvodní věta by měla dávat najevo, co je moje ambice do budoucna.

Mám pocit (ale nevím to jistě), že lepší nabídky na LI dostaneš až v souvislosti s tím, že tvůj bývalý kolega/spolužák nastoupí jinam a doporučí tě, nebo jejich recruiter tě  najde v jeho kontaktech. Nebo že jsi v nějaké zajímavé množině, např. čerstvých absolventů FITu.

Mně začaly nabídky chodit až s určitým zpožděním poté, co jsem si vyrobila profil. Podezřívám nastavení LinkedInu - dá se tam naklikat, že jsi otevřená/viditelná pro recruitery nebo tak něco. Poté, co jsem toto povolila, se komunikace zvýšila. A samozřejmě asi i čím víc spojení si uděláš, tím víc lidí tě vidí...

- právě z toho důvodu moc nepoužívám LI... všude cringe... asi bych měla pročistit seznam přátel 😀
- Nic se nevyrábí hůř než starý LinkedIn. Já bych doporučil každému a zejména juniorům/juniorkám jeho založení a udržování.
- já ho udržuju, akorát nemám moc příspěvků ani se nezapojuju do konverzací. dřív mi LI přišel jako skvělá profesionální síť, pak mě přidala spousta life coachu do přátel a já všechny akceptuju, tak mám samy spam na úvodní stránce 🙈 samý toxic positivity
- guilty as charged, ale holt jsem zjistil ze to funguje a otevira to byznysove prilezisosti 😦 nez jsem mel JG, tak jsem vubec nechapal ze nekdo neco na LI pise nebo tam komentuje, prislo mi to jako uplne ulet divnej svet plnej presne jak pises, toxic positivity
- https://twitter.com/yablko/status/1329013868149043201
- Já nepropaguju žádný LinkedIn oversharing nebo selfbranding atd - má to svoje hodnoty, není to pro každýho a je to docela otrava.
Co je ale zásadní minimum je mít LinkedIn aktualizovaný (co dělám, kde, co umím ) - a já jako bonus ještě doporučím, co se mi osvědčilo fakt hodně: Používat LI jako vizitkovník. Kdykoliv se s někým profesně potkám (klidně i krátce), tak místo výměny vizitek se pak ozvu na LinkedInu. A ten jediný cíl je - chytřejší vizitkovník. Pomůže mi to, když se o pár let později chci na něco zeptat nebo když hledám lidi (nebo práci) - a neuškodí to. Samozřejmě za předpokladu, že nezačnu po úspěšném "spojení" zkoušet ekvivalent podomního prodeje hrnců na nejlepší a revoluční produkt nebo tak něco.
Ale typicky, když hledám lidi, tak z inzerátů jich chodí minimum - většina jde přes přímé doporučení a ta druhá největší kategorie jsou lidi, který buď já nebo ten kdo pro mě dělá recruiting aktivně najde na LinkedInu. A typicky problém s juniorními lidmi (nula až třeba tři roky zkušeností) je, že jsou nevyhledatelní. Jsou buď na škole nebo v první práci kterou nějak našli - ale není způsob jak je najít a oslovit.
- Mám LI v podstatě jen jako vizitku právě a už jen to stáří účtu, respektive doba u pracovních pozic je takovým prvním vodítkem pro HR, kterých tam chodí opravdu mnoho. Mám nabídky do seniorních SEO pozic prakticky obden. hodně i ze zahraničí na IČO. A to mám prostě jen 5+ let v oboru.
- Podobně to mám taky. Proto si nepřidávám lidi, co mě jen kontaktujou tam, protože i takhle mám často problém si vzpomenout, kde jsem k tomu kontaktu přišel.
- Dělal jsem to stejně, dokud jsem nezačal vyrábět JG. Potom jsem přešel do módu „každý je můj kamarád“, protože pak mají moje statusy impact.
-->
