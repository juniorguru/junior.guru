---
title: Jak na životopis pro juniory v IT
description: Co dát do životopisu, když nemáš praxi? Když jsi student? Jak můžeš i jako junior bez praxe připravit CV, které tě dostane na pohovor?
template: main_handbook.html
---

{% from 'macros.html' import lead, note, blockquote_avatar with context %}

# Juniorní CV

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }} Tuto stránku Honza právě přepisuje. Je velmi pravděpodobné, že za pár dní tady bude jiný text, lepší, voňavější, nápomocnější.
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

**[Projekty](#projekty) jsou pro juniora nejdůležitější věc hned po kontaktních údajích a úvodu**, tak ať jsou hezky vysoko a viditelně. Zmínka o GitHub profilu nestačí, uveď konkrétní projekty, kterými se chceš pochlubit, trochu je popiš, přidej odkaz na každý z nich.

**Drž se pravdy.** Pokud máš přečtené tři články o [MongoDB](https://cs.wikipedia.org/wiki/MongoDB), napiš, že víš co to je, ale netvrď, že s tím umíš pracovat. Jestliže něco přibarvíš, na pohovoru se na to vždy snadno a rychle přijde. Budeš akorát působit nevěrohodně.

{% call blockquote_avatar(
  'Někdo se chlubí: Scala, Groovy, Kotlin. Nadchne mě to, ovšem hned dostanu studenou sprchu, protože neví, jaký je mezi nimi rozdíl.',
  'lubos-racansky.jpg',
  'Luboš Račanský'
) %}
  Luboš Račanský, profesionální programátor, autor článku [O náboru juniorů](https://blog.zvestov.cz/software%20development/2018/01/26/o-naboru-junioru.html)
{% endcall %}

<small>Rady v této podkapitole volně vychází mimo jiné i ze [článku recruiterky Simony Liptákové](https://research.redhat.com/blogs_cpt/how-to-hack-your-cv-7-useful-tips-for-students-with-no-work-experience/). Díky!</small>

## Projekty

Na inzerát bytu k pronájmu, u kterého nejsou fotky, nikdo odpovídat nebude. Stejně je to i s kandidáty. **Potřebuješ ukázat, že umíš něco vyrobit, dotáhnout do konce, že máš na něčem otestované základní zkušenosti z kurzů a knížek.** K tomu slouží [projekty](../practice.md#najdi-si-projekt). Pokud nemáš vysokou školu s IT zaměřením, kompenzuješ svými projekty i chybějící vzdělání. Snažíš se jimi říct: „Sice nemám školu, ale koukejte, když dokážu vytvořit toto, tak je to asi jedno, ne?“

Říká se, že [kód na GitHubu](git.md) je u programátorů stejně důležitý, ne-li důležitější, než životopis. Není to tak úplně pravda. U zkušených profesionálů je to ve skutečnosti [velmi špatné měřítko dovedností](https://www.benfrederickson.com/github-wont-help-with-hiring/). Náboráři se na GitHub nedívají, maximálně jej přepošlou programátorům ve firmě. Přijímací procesy mají většinou i jiný způsob, jak si ověřit tvé znalosti, např. domácí úkol nebo test. **Zajímavý projekt s veřejným kódem ti ale může pomoci přijímací proces doplnit nebo přeskočit.** Dokazuje totiž, že umíš něco vytvořit, že umíš s Gitem, a tví budoucí kolegové si mohou rovnou omrknout tvůj kód. Člověk s projekty skoro jistě dostane přednost před někým, kdo nemá co ukázat, zvlášť pokud ani jeden nebudou mít formální vzdělání v oboru.

Konkrétně GitHub s tím ale nesouvisí. Stejný efekt má, pokud kód vystavíš na BitBucket nebo pošleš jako přílohu v e-mailu. Když někdo říká, že „máš mít GitHub“, myslí tím hlavně to, že máš mít [prokazatelnou praxi na projektech](../practice.md#najdi-si-projekt). GitHub je akorát příhodné místo, kam všechny své projekty a pokusy nahrávat. **Nahrávej tam vše a nestyď se za to,** ať už jsou to jen řešení [úloh z Codewars](../practice.md#procvicuj) nebo něco většího, třeba [tvůj osobní web](../candidate-handbook.md#osobni-web-a-blog). Nikdo od tebe neočekává skládání symfonií, potřebují ale mít aspoň trochu realistickou představu, jak zvládáš základní akordy. Budou díky tomu vědět, co tě mají naučit.

Pokud se za nějaký starý kód vyloženě stydíš, můžeš repozitář s ním [archivovat](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/archiving-repositories). Jestliže se chceš nějakými repozitáři pochlubit na svém profilu, můžeš si je tam [přišpendlit](https://github.blog/2016-06-16-pin-repositories-to-your-github-profile/). Výhodou je, že přišpendlit jde i cizí repozitáře, do kterých pouze přispíváš.

{% call blockquote_avatar(
  'Na pohovoru mě nezajímá, co kdo vystudoval, ale jak přemýšlí a jaké má vlastní projekty. Nemusí být nijak světoborné, je to však praxe, kterou ani čerstvý inženýr často nemá.',
  'josef-skladanka.jpg',
  'Josef Skládanka'
) %}
  Josef Skládanka, profesionální programátor
{% endcall %}

Máš-li za sebou nějakou vysokou školu z oboru, ukaž svou bakalářku nebo diplomku. Je to něco, co je výsledkem tvé dlouhodobé, intenzivní práce. Pochlub se s tím!

## Zkušenosti získané mimo IT

Otevřeně přiznej **všechny zkušenosti, které máš.** Že jsi původně zubařka? Pro firmu, která vytváří software pro nemocnice, může být i toto zajímavá informace. A co si budeme povídat, málokdo viděl tolik _[technical debt](https://en.wikipedia.org/wiki/Technical_debt)_ a _[legacy code](https://en.wikipedia.org/wiki/Legacy_code)_ jako zubaři. Nepodceňuj, co z tvé minulosti může zaměstnavatele zaujmout. Tvoje zkušenosti mimo IT přispívají k tomu, kdo jsi. **Firma může usoudit, že právě díky znalosti jiného oboru můžeš přispět něčím, co ještě nemají**, ať už je to vědecký pohled, lidský přístup, nebo pečlivost účetního. Stalo se i to, že při pohovoru ocenili manažerské dovednosti prokázané při hraní online her (viz [Wired](https://www.wired.com/2006/04/learn/), [CNN](https://money.cnn.com/2014/06/19/technology/world-of-warcraft-resume/index.html)). Pokud najdeš **práci, která kombinuje tvoje předchozí zkušenosti a programování**, budeš mít velký náskok před kýmkoliv jiným. Nepodceňuj své předchozí zkušenosti a neignoruj je — místo toho přemýšlej, jak je můžeš prodat! Ze stejného důvodu může mít smysl zmínit i koníčky.
