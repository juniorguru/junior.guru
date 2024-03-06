---
title: Jak na Git a GitHub
emoji: 🔀
stages: [learning, creating, preparing]
description: Co je Git a k čemu se používá? Jaký je rozdíl mezi Gitem a GitHubem? Jak začít s Gitem?
template: main_handbook.html
---

{% from 'macros.html' import blockquote_avatar, link_card, note with context %}

# Git a GitHub

Git je **nástroj, který ti umožňuje sledovat historii změn v kódu, ale kromě toho jej také sdílet s dalšími lidmi**. Je to program, který nainstaluješ do svého počítače a pracuješ s ním v příkazové řádce, nebo jej ovládáš např. prostřednictvím svého editoru. Git se dnes používá skoro v každé firmě. I když jeho výhody nejvíc oceníš při práci ve dvou a více lidech, může ti pomoci i jako jednotlivci: Zálohovat kód svých projektů jinam, synchronizovat jej mezi vlastním počítačem a internetem, na dálku jej někomu ukázat.

## GitHub

[GitHub](https://github.com/) je **úložiště kódu a sociální síť pro programátory**. Kód tam lze poslat pomocí Gitu. GitHub není jediným takovým úložištěm, další jsou např. GitLab nebo BitBucket, ale je nejoblíbenějším pro [open source](practice.md#zkus-open-source), takže tam najdeš nejvíce projektů a lidí.

## Neboj se ukázat kód!    <span id="showoff"></span>

U začátečníků rozhodně platí, že **nemají co schovávat a měli by světu ukázat co nejvíce toho, co dokázali vytvořit, nebo co zkoušeli řešit**. Můžeš tím jenom získat. GitHub je příhodné místo, kam všechny své projekty a pokusy nahrávat. Zároveň je to místo, kde mají své projekty i všichni ostatní a kde lze spolupracovat s lidmi z celého světa.

Nenech se omezovat strachem, že někdo uvidí tvůj kód a pomyslí si, že nic neumíš. Neboj se mít svůj kód veřejně a ukazovat ho druhým! Tato obava je zbytečnou překážkou ve tvém rozjezdu. Programování je o spolupráci a **GitHub je hřiště pro programátory, kde si každý experimentuje na čem chce.** Čím více tam toho máš, tím lépe. Nejen že se naučíš lépe ovládat Git, ale hlavně budeš moci svůj kód ukázat, když budeš potřebovat [pomoc na dálku](help.md). Pokud tě někdo straší, že si tvůj GitHub budou procházet náboráři, [nenech se tím zmást, je to trochu jinak](cv.md#6-projekty).

## Jak se naučit Git a GitHub    <span id="howto-git-github"></span>

<div class="link-cards">
  {{ link_card(
    'Git a GitHub od základov',
    'https://www.youtube.com/watch?v=0v5K4GvK4Gs',
    'YouTube kurz Gitu a GitHubu od <a href="http://robweb.sk">yablka</a>.'
  ) }}

  {{ link_card(
    'Nauč se Python',
    'https://naucse.python.cz/course/pyladies/git/basics/',
    'Nauč se Git z nejznámějších českých materiálů pro Python.'
  ) }}

  {{ link_card(
    'The Missing Semester',
    'https://missing.csail.mit.edu/2020/version-control/',
    'Git podle materiálů z americké univerzity MIT.'
  ) }}
</div>

## Projekty

Na inzerát bytu k pronájmu, u kterého nejsou fotky, nikdo odpovídat nebude. Stejně je to i s kandidáty. **Potřebuješ ukázat, že umíš něco vyrobit, dotáhnout do konce, že máš na něčem otestované základní zkušenosti z kurzů a knížek.** K tomu slouží [projekty](practice.md#najdi-si-projekt). Pokud nemáš vysokou školu s IT zaměřením, kompenzuješ svými projekty i chybějící vzdělání. Snažíš se jimi říct: „Sice nemám školu, ale koukejte, když dokážu vytvořit toto, tak je to asi jedno, ne?“

Říká se, že kód na GitHubu je u programátorů stejně důležitý, ne-li důležitější, než životopis. Není to tak úplně pravda. U zkušených profesionálů je to ve skutečnosti [velmi špatné měřítko dovedností](https://www.benfrederickson.com/github-wont-help-with-hiring/). Náboráři se na GitHub nedívají, maximálně jej přepošlou programátorům ve firmě. Přijímací procesy mají většinou i jiný způsob, jak si ověřit tvé znalosti, např. domácí úkol nebo test. **Zajímavý projekt s veřejným kódem ti ale může pomoci přijímací proces doplnit nebo přeskočit.** Dokazuje totiž, že umíš něco vytvořit, že umíš s Gitem, a tví budoucí kolegové si mohou rovnou omrknout tvůj kód. Člověk s projekty skoro jistě dostane přednost před někým, kdo nemá co ukázat, zvlášť pokud ani jeden nebudou mít formální vzdělání v oboru.

Konkrétně GitHub s tím ale nesouvisí. Stejný efekt má, pokud kód vystavíš na BitBucket nebo pošleš jako přílohu v e-mailu. Když někdo říká, že „máš mít GitHub“, myslí tím hlavně to, že máš mít [prokazatelnou praxi na projektech](practice.md#najdi-si-projekt). GitHub je akorát příhodné místo, kam všechny své projekty a pokusy nahrávat. **Nahrávej tam vše a nestyď se za to,** ať už jsou to jen řešení [úloh z Codewars](practice.md#procvicuj) nebo něco většího, třeba [tvůj osobní web](candidate.md#osobni-web-a-blog). Nikdo od tebe neočekává skládání symfonií, potřebují ale mít aspoň trochu realistickou představu, jak zvládáš základní akordy. Budou díky tomu vědět, co tě mají naučit.

Pokud se za nějaký starý kód vyloženě stydíš, můžeš repozitář s ním [archivovat](https://docs.github.com/en/repositories/archiving-a-github-repository/archiving-repositories). Jestliže se chceš nějakými repozitáři pochlubit na svém profilu, můžeš si je tam [přišpendlit](https://github.blog/2016-06-16-pin-repositories-to-your-github-profile/). Výhodou je, že přišpendlit jde i cizí repozitáře, do kterých pouze přispíváš.

{% call blockquote_avatar(
  'Na pohovoru mě nezajímá, co kdo vystudoval, ale jak přemýšlí a jaké má vlastní projekty. Nemusí být nijak světoborné, je to však praxe, kterou ani čerstvý inženýr často nemá.',
  'josef-skladanka.jpg',
  'Josef Skládanka'
) %}
  Josef Skládanka, profesionální programátor
{% endcall %}

Máš-li za sebou nějakou vysokou školu z oboru, ukaž svou bakalářku nebo diplomku. Je to něco, co je výsledkem tvé dlouhodobé, intenzivní práce. Pochlub se s tím!

## README

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }} Kapitola se teprve připravuje.
{% endcall %}



<!-- {#

https://dariagrudzien.com/posts/the-one-about-your-github-account/
https://dev.to/yuridevat/how-to-create-a-stunning-github-profile-2mh5

https://www.reddit.com/r/cscareerquestions/comments/13otqke/why_ask_for_github_profile_url/

Těm projektům na Githubu chybí třeba popis, co to vlastně je, jak to funguje, a odkaz na nasazenou verzi, ale asi na tom ještě pracuješ. Bude se to hodit, až/pokud se těmito projekty a svým Github profilem budeš prezentovat při hledání práce.

gitleaks projdou kod a oznami vsechno co vypada jako token atd.

GitHub je tvoje osobní polička. Až když na něj dáš odkaz do svého CV a pošleš firmám, stává se z něj vitrínka 🙂

Ber to tak, že na GitHub ti nikdo nekouká, i když je to veřejné, dokud mu k tomu nedáš hodně dobrý důvod. Těch profilů je tam milion a dá velkou práci způsobit, aby se tam někdo na něco koukal, když chceš 🙂

{% call blockquote_avatar(
  'GitHub vyčistit, _polishnout_, upravit. Stejně jako CVčko je to věc, která vás má prodat. Projekty, kterými se chlubit nechceš, radši skryj.',
  'jiri-psotka.jpg',
  'Jiří Psotka'
) %}
  Jiří Psotka, recruiter v [Red Hatu](https://red.ht/juniorguru) v [prvním dílu podcastu junior.guru](../podcast/1.jinja)
{% endcall %}

Repozitáře na GitHubu, které nepovažujete za reprezentativní, můžete archivovat. Budou jen pro čtení a žlutý proužek návštěvníkům řekne, že už na nich nepracujete. Projekty, kterými se chlubit chcete, můžete zviditelnit na svém profilu jako „pinned“.

dobrá, upravím to podle toho co jste mi napsal, zdá se to celkem i rozumné, a jsem rád za nějakou zpětnou vazbu od někoho kdo se tomu aktivně věnuje, mohl bych se ještě zeptat jak by měl vypadat ideálně github? většina projektu mam převážně ve azure devops, a jen nějaké vybrané jsem si dal do nového github učtu https://github.com/LukePavelka
jedno zadaní od firmy, které jsem vypracoval, jsem si dal taky na github, kritickou chybu nejspiš vidim v tom že jsem udělal jeden velky commit až pak když jsem to měl skoro hotové

Líbí se mi, že projekty maji README, ze kterého jde pochopit, o co jde. Kód samotný úplně neposoudím, ale jinak mi to přijde v pohodě. Jestli je někde jeden velký commit, s tím nic nenaděláš, pokud by se tě na to ptali u pohovoru, tak řekneš, že si to uvědomuješ a že se holt učíš, tak už víš, že se to má dělat jinak. Ale ani jeden velký commit, pokud je na začátku projektu, není úplně chyba. Typicky „initial commit“ v repozitáři může být dost velký, protože před tím, než byl kód Open Source na GitHubu, mohl vzniknout někde vedle a tímto commitem se vše teprve dostalo do repozitáře.

Vpravo nahoře se dá u jednotlivých projektů kdyžtak dopsat jedna větička o projektu a přidat případně odkaz, pokud projekt třeba jede někde spuštěný a má svou webovku.

Zaujalo mě, že některé projekty mají dva contributors, podle jména si vyvozuji, že máš dva GitHub účty. Je pro to nějaký důvod? Přijde mi škoda dělit svou aktivitu na dva účty, pokud ten jeden nepoužíváš na nějakou podvratnou činnost nebo jej nechceš spojovat s vážnou prací (ale jak vidíš, tím že tam má commity, tak se na něj stejně doklikám). Pokud jeden účet nepoužíváš, repozitáře lze přesunout mezi uživateli. Commity na účty GitHub páruje podle e-mailů, takže stačí starý účet smazat a e-mail, pod kterým jsou commity vytvořeny, si přidat k tomu účtu, který chceš používat (GitHub účet může být spárovaný na více e-mailů).

Jinak tady můžou být tzv. „pinned repositories“, můžeš si vybrat, co tam půjde vidět a v jakém pořadí. Pokud těm repozitářům dáš i ty jednovětné popisky (viz výše), budou se tam zobrazovat, takhle se v tom nedá moc snadno orientovat, co je co. Když si otevřu tvůj profil, uvidím sice repa, ale z těch názvů moudrý nebudu, ta jedna věta popisku by se šikla.

Výhodou těch pinned repositories je, že tam můžeš dát i repa odjinud, pokud jsi někam přispíval, nejen repa z tvého profilu. Já tam mám třeba Dredd, který mi nepatří (je v organizaci apiaryio), ale kde jsem hodně přispíval, takže mi stojí za to jej zmínit: https://github.com/honzajavorek/

Tip navíc, pokud by sis s tím chtěl supr vyhrát, můžeš mít na profilu i text, obrázky, atd., pomocí tzv. „profile README“ https://simonwillison.net/2020/Jul/10/self-updating-profile-readme/ Ale to je jen taková blbinka, rozhodně si nemyslím, že to musí mít každý a je to nějakou podmínkou pro to, aby si někdo sehnal práci, to vůbec 🙂

Já mám celkem asi 50 repo, ale většinu mám jako soukromé, protože to byly různá dílčí cvičení konkrétních dílčích algoritmů bez ladu a skladu a netvořily ucelený projekt nebo jsou nedokončené. Jako veřejné mám tedy dokončené a takové, které mi tvoří ucelený výstup a k těm mám pak třeba i odkaz, kde vidí výsledek. Ale to je jen můj pohled, jak to mám já. 🙂

Taky přihodím můj příspěvek. GitHub je super, ale mnohdy pracujete na confidental projektech, které nemůžete/nesmíte zveřejnit. Je fajn mít nějaké osobní projekty, ale ne každý po 8 hodinch v práci programuje potom i doma. (Y) Samozřejmě, tam je to úplně jiný příběh.
Tohle se ale týká lidí, co hledají první práci. Ti nemají důvod mít nic tajného a naopak sakra hodně potřebují ukázat, že umí aspoň něco udělat. CV je maximálně vizitka pro orientaci.
Testy považuju za nesmyslnej opruz pro všechny strany.
Zadání práce na doma mi dává smysl jen pokud není kód, nad kterým se můžu s kandidátem bavit a když ten kód je, ideálně bez práce dostupný na GitHubu, tak nemá cenu je zadávat.
A na pohovoru se budu (kromě samotné náplně práce) bavit právě o tom kódu… Ne každý si může dovolit mít projekty, ale pořád je to mnohem víc lidí, než si může dovolit studovat VŠ.

Kdo už má confidential projekty nebo jakoukoliv work experience, tak u něj platí jiná pravidla, což píšu i tady https://junior.guru/handbook/candidate/#projects
Pro juniory je podle mě GitHub fajn, protože nemají co skrývat, naučí se s gitem, GitHubem (což je sice proprietární věc, ale funguje na tom OSS a zároveň se z toho pak dá pochopit i GitLab nebo BitBucket atd., cokoliv co firmy používají), jejich projekty jdou vidět a mohou na ně tak dostat jednodušeji feedback třeba od mentora (ne-li přímo Pull Request s opravou, než aby si to posílali po e-mailech) a na pohovoru na to mohou mrknout při náboru a udělat si představu, co ten člověk zvládne vyrobit a co jej potřebují doučit.
Souhlasím, že dělat nějaké projekty navíc po večerech by nemělo být nutnou podmínkou, ale u juniorů to tak bohužel je, a to především u těch, kteří usilují o career switch a musí tím kompenzovat chybějící formální vzdělání nebo prostě jakoukoliv jinou praxi.

Procházet něčí GitHub je brutální opruz. I kdyby tam měl nejhezčí kód na světě, stejně potřebuju slyšet, jak k němu došel, proč něco udělal tak nebo tak. Kódy mě nezajímaj. Chci s tim člověkem mluvit. Daniel Srb, jestli myslíš začátečníky s nulovou praxí, tak s těmi jsem se nesetkal. Se začátečníky třeba s roční praxí ano. Ale asi úplně nevidim rozdíl mezi tim, proč by mě mělo bavit koukat na kód traineeho a nemělo na kód seniora. U obou mě zajímá, co maj v hlavě, ne na GitHubu. Protože tím rychle a dostatečně přesně zjistím, kdo z těch lidí je úplně (důraz na to úplně) mimo úroveň, kterou zrovna hledám a nebudu plýtvat jejich i mým časem na pohovoru nebo zadáváním a vyhodnocováním úkolů. U někoho s více lety praxe to už smysl nemá, navíc většina jejich práce nebude veřejně dostupná.
Když jsme u toho, tak sice říkáme GitHub a veřejně, ale ve skutečnosti prostě chci vidět kód a pokud je vystavený takhle, tak je to prostě pohodlné, nic víc.

Jestli mohu z druhé strany, tak naučit se sám s Githubem je pro mě dost složité. Snažím se ho používat. Nedokážu si ale pořádně ujasnit, jak ho správně používat a k čemu by to mělo vést (asi tím, že to, co občas napíšu, jsou maličkaté věci). A bez zpětné vazby vlastně ani nedokážu posoudit, jestli jdu správným směrem.

Mrkni na https://www.makeareadme.com/ jsou tam dobré tipy na to, jak a co napsat.
Taky využij funkce GitHubu a doplň popisy těch projektů. Radši dobrou češtinou než špatnou angličtinou.
Nicméně v kódu je asi lepší angličtina pro názvy proměnných i když upřímně je to to poslední, co bych při zkoumání toho, jak někdo přemýšlí řešil. To už by mě víc zajímalo, jestli ty názvy opravdu popisují to, co obsahují nebo co funkce dělají…

A taky jde srovnat ty repa ručně, umístit si na tu svoji homepage ta nejzajímavější tam, kde většina z nás začíná číst, tedy vlevo nahoru, teď máš nejnovější repo vpravo dole a první je přes rok netknutý kód.

Taky mrkni na .gitignore a přidej si tam složku .idea.

Mnohdy ani github nestačí, ale chápu že tohle je extrém poslat na nějakou nabídku CV bez kousku svého kodu. Tomáš Balbinder GitHub s nečím, co nejsou základní cvičení.

Lidi neví jak používat GitHub - sekce?

https://git-scm.com/book/cs/v2

https://twitter.com/simonw/status/1281435464474324993
Made myself a self-updating GitHub personal README! It uses a GitHub Action to update itself with my latest GitHub releases, blog entries and TILs https://github.com/simonw
https://simonwillison.net/2020/Apr/20/self-rewriting-readme/
https://simonwillison.net/2020/Jul/10/self-updating-profile-readme/

https://www.honeybadger.io/blog/git-tricks/

Já osobně jej používal hlavně jako přenos rozpracovaného projektu mezi prací, kde jsem na něm sem tam dělal a domovem. Až docela nedávno jsem se dozvěděl o merge requestech, a jak by se vlastně mělo pushovat. Mít nějaký "návod" jak s ním pracovat (všeobecně s GITem) byl bylo super. Když vemu přímo GITHub, líbí se mi jeho desktopová aplikace, je dost user friendly a pěkně se s ní pracuje...

Používám GitHub na dvě věci:
1. mám v něm dvě větve, kde na jedné mám stabilní verzi a na druhé můžu vyzkoušet cokoliv
2. přenos rozpracovaných projektů

Na základní věci mi přijde docela jednoduchý. Nepamatuju si všechny příkazy, tak občas musím něco vygooglit (řešila jsem třeba několikrát případ, že jsem přidala gitignore a nefungoval), ale na stack overflow je najít úplně všechno, co se týká základní práce s GITem.

Pokud připravuješ manuál, doporučuju vytvořit nějaký workflow, např. rozdíl mezi slovy add a commit není úplně intuitivní pro začátečníka.

Git je těžkej, ale někde určitě dobrej návod existuje.
Pro lidi v CoreSkillu používám tyhle (odkazy na úvodní info, ale samozřejmě jsou tam i ty další věci)
https://guides.github.com/introduction/git-handbook/
https://www.atlassian.com/git/tutorials/what-is-version-control
https://www.codecademy.com/courses/learn-git/lessons/git-workflow/
+ článek o konfliktech https://github.blog/2018-08-22-merge-conflicts-in-the-classroom/
dál spíš kdo narazí nebo má zájem, určitě není základ (většina)
+ tenhle o aliasech https://githowto.com/aliases
+ https://ohshitgit.com/
+ https://github.blog/2015-06-08-how-to-undo-almost-anything-with-git/
s tím, že tohle je seznam toho, co je potřeba a jak to navazuje (1 must have, 5 nice to have a zbytek mezi tím)
https://coreskill.github.io/csss/git.html
+ věci z githubu/labu
https://coreskill.github.io/csss/github-and-gitlab.html

Co vidím hned na první pohled je, že lidem automaticky splývá Git a GitHub (což se není co divit). A GitHub se hodně vyvíjí ohledně toho, co tam jde všechno vyrobit. Třeba nedávno tam jde udělat i vlastní homepage, která se může i sama aktualizovat: https://simonwillison.net/2020/Jul/10/self-updating-profile-readme/

To už jsou velké haluze, ale jde mi o to, že GitHub už je tak složitý, že kdo zná i půlku jeho fičur, je vlastně power user.

Bylo by fajn v tom CV k MealPalu dát nějaký testovací login. Ne každému se bude chtít registrovat, aby viděl funkcionalitu uvnitř a venku jí tolik k vidění není a to je velká škoda!

Vše, co jsem nenapsal mi přijde fakt fajn 👍 , máš u všeho na GH popisky, readme (u jednoho ne, ale to je nějakej cvičnej Czechitas projektík, možná bych ho schoval), url atd. Máš i pořádnej velkej projekt a tak dále. Držím palce.

Firmy používají na uložení Git repozitářů všechno možné, GitLab, BitBucket, možná by se dalo zmínit aspoň povrchně nějak i to. Samozřejmě na GitHubu je zase veškerý Open Source, tak se hodí to umět.

GitHub mám, ale projektov nemám veľa, sú skôr menšie a momentálne pracujem na jednom rozsiahlom, na ktorom to celé sebaprezentovanie tak nejak staviam. Tiež som si vzala k srdcu rady ohľadom GitHubu a pomaly dokončujem popisy a Readme ku všetkým projektom, takže keď to budem mať hotové, tak to určite zazdieľam do
cv-github-linkedin a poprosím o spätnú väzbu, na to sa už dosť teším 🙂

Na GitHubu hlavně příspívám do open source projektů a chci ho začít víc využívat jako "showcase". Základní workflow mi dnes nedělá potíže. Občas po jednoduchost používám editor přímo v GitHubu, který udělá celou tu práci na pozadí místo mě.
Ze začátků si vybavuji hlavně konfigurační problémy (někdy těžko odlišit, co je Git a co GitHub):
- nastavení SSH klíčů, abych nemusela pokaždé zadávat login a heslo (magic!),
- čachry s remotes, abych posílala změny na správná místa (origin, můj fork, všechny ty branche - jak se v tom orientovat?),
- pokusy o "hezkou historii", čili jak v tom repozitáři neprasit každou chvíli merge commity - to bych se teď ráda naučila, když už umím základy,
- nespočetkrát: ups, commit se omylem poslal do čela branche master, jak se teď toho zbavit, abych připravila změny k poslání na GH.
Jedna kolaborativní, která nesouvisí tolik s GH, jako s nastavením open source projektů: otevřeš PR se změnami, někdo se na něho podívá a schválí (review). A co teď? Máš si to začlenit (zmáčknout button Merge), pokud máš na to právo na projektu, nebo počkat na další schválení? Kolik těch schválení má proběhnout, než to bude OK? Nebo bys to prostě nikdy neměl sám začleňovat, i když se někdo vyjádřil souhlasně ke změnám?
Dále jsem se zatím nenaučila pořádně vyhledávat v GitHubu. Například, chci najít různé projekty, které obsahují "django_secret_key" v souboru settings.py.
Boty, Actions, webovky ani nezmiňují, k GH ekosystému jsem se zatím pořádně nedostala.

Ještě závěrem, zajímalo by mě, zda je možné někomu vysvětlit GitHub, aniž by se musel instalovat Git a dělat kolečko změn, tak aby Git nebyl brzda pro maličké změny, typicky třeba úpravy kurzů na Pyladies.cz.
PS. Pardon my esej 😄

K některým věcem by se dal napsat nebo natočit návod, některé jsou zapeklité už jen proto, že názory lidí se na věc liší, a každý ti řekne něco jiného (hezká historie). Podobně je to u té kolaborace. Může být nějaký standard, ale v důsledku to má každý projekt trochu jinak. Každopádně všechno super témata.

Jo no, ale je to fakt hodně častý a viděl jsem, že se to plete i zkušenějším programátorům. Musím říct, že GitHub dělá dobrou práci, docílili fakt toho, že pro spoustu lidí je prostě mezi nimi a Gitem rovnítko :)) Což jako není z určitého úhlu pohledu tak mimo, protože oni se už roky silně zapojují do vývoje Gitu, hostují ten projekt, jeho web, myslím že jsou v tom nějak zapečení i finančně, organizačně, atd. Ale je jasný, že je dobrý to rozlišovat.

    Dále jsem se zatím nenaučila pořádně vyhledávat v GitHubu. Například, chci najít různé projekty, které obsahují "django_secret_key" v souboru settings.py.

Oceňuji takové vyhledávání 😄 Ale já jsem se na GitHubu taky zatím vyhledávat nenaučil. Vzhledem k tomu, že vznikají různý "3rd party" vyhledávače, tak skoro začínám mít pocit, že to není mnou 🙂

Možná by mohlo pomoci třeba grep.app, koukej: https://grep.app/search?q=django_secret_key&filter[path.pattern][0]=settings.py

Jinak pokud bys chtěl ještě víc zdůraznit, že https://github.com/spaze/libini-djgpp je jen pro archivní účely, můžeš teď na GH repo přímo označit jako archivované, což dá návštěvníkům na první pohled jasnou message. Je to repo > settings > dole dole dole danger zone > Archive this repository

Díky toolingu ty začátky nemusej bejt tak hrozný. Když má Github tužtičku a webovej editor + CI systém, tak pro jednoduché změny člověk nemusí mít rozjeté lokální prostředí (a jak trefně pronesl @Honza Javorek jednou na Pyvu - díky "verified commit" člověk pozná, kdo používá tužtičku, protože prakticky nikdo neumí/nechce/nepotřebuje nastavit podepisování commitů 😁 ).

Ta věta zněla vlastně jako něco víc, než to ve skutečnosti je 😄 Upravuji projekty české Pythonní komunity, a to i tak většinou jde o obsah; postupně ale, jak ty projekty pročítám (web PyLadies, zpětnovazebník), cítím se jistější i co se týče kódu. Těm malým změnám vděčím pochopení kolaborativního workflow GH. Asi to bude trochu tak, že bariera nové ("mám beginner programovací skill") + nové (GitHub) je na začátku až moc. Přispění něčím, co umím líp (text, obsah, ...) v novém prostředí (GH) nepůsobí až tak děsivě. To mi nepřijde jako málo 🙂 Super. Takže tomu rozumím správně, že pro tebe cestou k OSS byla komunita kolem PyLadies, kde jsi v podstatě zjistila na co mrknout, kde můžeš přispět a případně i dostala radu jak a co udělat?

https://simonwillison.net/2020/Jul/10/self-updating-profile-readme/
https://dariagrudzien.com/posts/the-one-about-your-github-account/

Přednáška o GitHub Profilu

- [ ] Co je GitHub - dává se tam kód, lidi spolupracují na komunitních projektech https://github.com/
- [ ] Naučit se Git a GitHub?
    - [ ] yablko https://www.youtube.com/watch?v=0v5K4GvK4Gs
    - [ ] MIT The Missing Semester https://missing.csail.mit.edu/2020/version-control/
    - [ ] Nauč se Python https://naucse.python.cz/course/pyladies/sessions/foss/
- [ ] GitHub profil https://github.com/honzajavorek
    - [ ] není to CV, není to LinkedIn https://www.linkedin.com/in/honzajavorek/
    - [ ] je to jen a pouze místo, kam si odkládám projekty, experimenty
        - [ ] https://github.com/honzajavorek?tab=repositories&q=&type=source&language=
        - [ ] mám tam web https://github.com/honzajavorek/honzajavorek.cz
        - [ ] záznam přednášky https://github.com/honzajavorek/become-mentor
        - [ ] bakalářka https://github.com/honzajavorek/trekmap
        - [ ] svatební web https://github.com/honzajavorek/toztedasvatba.cz
        - [ ] pokusy na Advent of Code https://github.com/honzajavorek/aoc
        - [ ] forky různých repozitářů, do kterých jsem přispěl, klidně i jedno písmenko
    - [ ] nikdo mi nemá co mluvit do toho, co tam mám
    - [ ] pokud není důvod něco mít private, dávám to public
    - [ ] neměl bych tam dávat citlivé údaje (hesla, tokeny...)
- [ ] čtverečky
    - [ ] někdo to bere jako soutěž, ale není to soutěž, víc zelených čtverečků není víc adidas
    - [ ] přispívání do OSS nic nevypovídá o vašich skutečných zkušenostech ani hodnotě na trhu
    - [ ] dělat na OSS ve volném čase není ničí povinnost, work-life balance
    - [ ] je to hezký bonus a příležitost pro někoho, kdo začíná a zatím nemá pracovní zkušenost
- [ ] recruiteři se na profil nedívají (pro ně je CV, LinkedIn), ale technicky založení lidé ano
    - [ ] není od věci si nahrát nějaký obrázek, nemusí být fotka
    - [ ] téma k hovoru na pohovoru, možnost ukázat konkrétní vlastní projekt
    - [ ] možnost ukázat kód mentorovi, získat zpětnou vazbu, dostat pomoc přes Pull Request
    - [ ] udělají si lepší představu o tom, co už umíš, co se musíš doučit
- [ ] triky
    - [ ] pokud chci něco vypíchnout, pinned (může být pak i z jiných orgs)
    - [ ] pokud chci něco upozadit, archived
    - [ ] pokud si chci pohrát, mohu mít osobní README
        - [ ] https://docs.github.com/en/github/setting-up-and-managing-your-github-profile/managing-your-profile-readme
        - [ ] https://simonwillison.net/2020/Jul/10/self-updating-profile-readme/
        - [ ] https://github.com/simonw/

neni to linkedin
kosticky neresit
svoboda konani
pokud neco neni aktualni, lze archivovat
pokud chci neco vypichnout, existuje pin
nahrat obrazek / fotku
takové to README osobní
yablko návod na github a git, naučse návod na git

https://docs.github.com/en/github/setting-up-and-managing-your-github-profile/managing-your-profile-readme
https://www.gitkraken.com/learn/git/tutorials

Projekty jsem si nahrál na GitHub - vysvětlit workflow a styl práce na GitHubu?

https://ohmygit.org/

základní pitfalls k tomu, co lidi řeší s projekty na githubu
https://discord.com/channels/769966886598737931/789107031939481641/836969346403926096

Kdysi tady byla taková hravější verze: https://ohmygit.org/ ale po nějaké době používání musím říct, že je to poměrně chudé ve vysvětlování.

https://learngitbranching.js.org/

https://www.gitkraken.com/learn/git/tutorials

https://github.com/firstcontributions/first-contributions

https://www.drmaciver.com/2015/04/its-ok-for-your-open-source-library-to-be-a-bit-shitty/

A recent trick I discovered to learning this is to pick an open source project written by developers you like and start writing docs and tests.
https://twitter.com/hamelhusain/status/1296601185470709760

Talk to maintainers
https://twitter.com/simonw/status/1293017371536265221

https://dariagrudzien.com/posts/the-one-about-your-github-account/

--- https://discord.com/channels/769966886598737931/769966887055392768/974294385242017842
Ahoj, chci se zeptat ohledne 'projektu', kterymi se clovek muze prezentovat pri pripadnym hledani prace. Jste zastanci toho, aby clovek ukladal treba na GitHub kazdou vec co naprogramuje i treba v ramci nejakeho kurzu, anebo toho mit malo, a to veci, ktere primo souvisi s tim, co chci delat? Proc?
Ted jak jsem to napsala, tak mi z toho vychazi spis druha moznost, ale i tak si chci precist, jak o tom uvazujete. (Asi je to hodne zakladni otazka, pravdepodobne se to tu nekde resilo, jen se spatne vyhledava podle klicovych slov.)
---


--- https://discord.com/channels/769966886598737931/769966887055392768/974298717454737408
Já si tam teď ukládam skoro všechno. Třeba i krátká řešení z Codewars, kterýma se prezentovat nebudu, ale jejich ukládání na GitHub mi pomáhá s pravidelností a je to pro mě přehledné. Repozitáře můžeš "připnout" ->  Takové se budou na profilu zobrazovat vždycky jako první  😉  To se může hodit pro projekt/y, kterým/i se chceš prezentovat.
---


--- https://discord.com/channels/769966886598737931/769966887055392768/974343605437206548
Mít každý, i malý projekt, v gitu není špatný nápad, zvykat si s tím pracovat je důležité.

Jestli to pak chceš poslat i na GitHub je na tobě. Je to tvůj GitHub a je ok tam mít i nějaké rozpracované nebo banální věci veřejně.

Ale! Pokud hledáš první práci, mysli ale na to, že ten GitHub tě reprezentuje a pokud už se na něj bude někdo dívat, tak nebude mít moc času ani motivace to procházet všechno. Proto si myslím, že je lepší tam mít 2-5 tvých nejlepších projektů a ostatní skrýt, protože pokud se tam někdo dostane, může si udělat mylný dojem o tom, jak komplexní věci už zvládáš.
Jasně, odkážeš na ně z CV přímo, ale nikdy nevíš, kdo a jak se kam dostane…
---


--- https://discord.com/channels/769966886598737931/769966887055392768/974683976184778822
Souhlas s <@614870427931770900> . Někdo nerad na GitHub dává věci, které nejsou reprezentativní a bojí se, že mu to zhorší pozici. Vím, že <@652142810291765248> je spíš zastáncem toho si GitHub „čistit“, pokud je člověk junior, a mít ty věci spíš private, protože proč ne. Já jsem zastáncem toho, že GitHub není CV a každý má právo si tam dávat úplně co chce. S touto myšlenkou GitHub vznikl, je to prostě odkladiště kódu. Nakonec málokdo si lidi lustruje tak, že by procházel vše, co je na GitHubu, dělá se to spíš z nouze, když je nenasměruješ na něco konkrétního, co chceš ukázat. Takže bych na GitHub dával cokoliv a do CV dal odkaz na konkrétní projekt, na který jsi hrdá, ani nemusíš dávat odkaz na celý profil.
---


--- https://discord.com/channels/769966886598737931/788832177135026197/946040086108205087
[GitHub] Pokud byste rádi trochu interaktivnější výuku práce s Gitem <:git:900831000567902229>  a GitHubem <:github:842685206095724554> , tak https://lab.github.com/ je zdrojem spousty zábavy stylem **learning-by-doing** 🧑‍🎓
---


--- https://discord.com/channels/769966886598737931/769966887055392768/935558014327468032
<@!477895566085324801> K tématu "psaní commit messages" mohu doporučit následující článek: https://cbea.ms/git-commit/ - řeší se v něm forma i co by dobrá commit message měla (či naopak neměla) obsahovat.
---


--- https://discord.com/channels/769966886598737931/788832177135026197/909083706793279549
Má to i českou verzi! 🙂 sprostou https://ohshitgit.com/cs a slušnou https://dangitgit.com/cs 😄
---


--- https://discord.com/channels/769966886598737931/789087476072710174/1068139247799902238
Udělátor, co simuluje a vizualizuje příkazy v gitu, dokážu si představit, že by to mohlo být užitečné lidem co si třeba ještě nejsou úplně jistí jak git funguje: https://github.com/initialcommit-com/git-sim
---


--- https://discord.com/channels/769966886598737931/788832177135026197/1062732102237437973
Pěkný materiál pro prvo-přispěvatele/ky na GitHubu: https://github.com/firstcontributions/first-contributions
---


--- https://discord.com/channels/769966886598737931/1090649291804135485/1090912862542766121
Pokud ti to pomůže, tak je to asi nejčastější chyba začátečníků. Možná bych to měl mít někde napsané, až budu mít v příručce hezkou stránku o projektech 🤔
---


--- https://discord.com/channels/769966886598737931/1082249171278512151/1083785079702163496
Na GitHubu může být ještě detailnější, ale tam nebude koukat recruiter, ten mrkne CV, řekne si, hele má nějakou appku, něco dělá, to pošlu dál. Na GH zase kouká spíš ten technickej člověk, co to posuzuje, mrkne na README, mrkne na kód.
---


--- https://discord.com/channels/769966886598737931/1082316811703427102/1082316817424466000
Ahoj, na začátek předesílám, že příručku jsem přečetla a neustále se k ní vracím (mimochodem tam ještě nedávno byla nějaká formulka, že kdo si tam chce přečíst o GitHubu, má se hlásit, aby <@668226181769986078> měl motivaci něco napsat - tak se hlásím!, a ano, vím, že teď už tam něco je), zdejší příklady jsem zkoukla, e-kurz o Githubu od Yablka vyslechla, a stejně se budu ptát na úplný úplný základy:

Mám nějaké vlastní drobné "projekty" a ráda bych je na GitHub dala jako ukázku práce, hlavně přímo kvůli hledání práce, kvůli komunitnímu hodokvasu a poznámkám ani ne 🙂 A teď.

Mám například aplikaci v shiny (dělám v Rku). Takže na GH nahraju kód a do readme dám odkaz na tu apku na webu, kde je možné ji vyzkoušet? Obdobně, když mám script (je to správně použitá terminologie?), kde jsem zpracovala data (u kterých si ani nejsem jistá, jestli bych je mohla publikovat, nejsou moje) a dělám tam klasifikátor - udělám to tak, že nahraju do GH kód, popíšu v readme, co ten script dělá a pak tam například někam nahraju grafy nebo screenshoty úspěšnosti, které z toho klasifikátoru na konci vypadly? Pochopila jsem to správně?

Jde mi o to, že je mi vlastně nepříjemný, že si uživatel/nahlížející nemůže ten kód pustit, aby viděl, jak to funguje. Ani mi nepřišlo, že by to nějak šlo, ale možná jen špatně koukám a hledám. Taky tam cpát ta zdrojová data mi nepřipadá úplně dobré, z vícero důvodů.

Vlastně tápu, jak to udělat elegantně, aby to mělo hlavu a patu a nějakou formu. Ta moje verze mi tak nepřipadá, ale nějak nevím, jak to udělat líp.
---


--- https://discord.com/channels/769966886598737931/1062006092571361320/1062018181654380605
Na mě to nepůsobí dobře a přesně jak to Martin popsal „vlastně nemám žádnou fotku, tak tam dám něco 5 let starýho“ 🤷‍♂️
Když už fotku, tak něco lehce profesionálnějšího, tedy pro situaci hledám první práci. Dělám nějakej dojem.
Ale to jsem já.
---


--- https://discord.com/channels/769966886598737931/1061663829353844907/1061680592074326056
pro priste: https://ohshitgit.com/#magic-time-machine 🙂
---


--- https://discord.com/channels/769966886598737931/1027275076355231754/1027276811190665226
https://learngitbranching.js.org/
---


--- https://discord.com/channels/769966886598737931/1017008201427845153/1017377812602179594
K tomu readme: syntaxe Markdownu
https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax
Něco k tomu jak je psát
https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes
https://www.makeareadme.com/
---


--- https://discord.com/channels/769966886598737931/983615979881906197/983618508460011580
Klidně začni tím, že si připravíš CV, GitHub a LinkedIn profil.
K CV tady https://junior.guru/handbook/cv/

<:linkedin:915267970752712734> uděláš podle toho CV

Na <:github:842685206095724554> si prosím dej nějakou profilovku, nemusí být tvoje fotka, ale ten default maj jen lidi, co to moc nepoužívaj, špatnej signál.
Schovej projekty, které jsou k ničemu, jako piškvorky.
K ostatním projektům doplň informace přímo na GitHubu i do README.md a někam je nasaď, statické jdou přímo na GitHubu.
Mrkni třeba na https://github.com/hankaEsha jak to má udělané.
4 vypíchlé projekty, popsané, nasazené.
---


--- https://discord.com/channels/769966886598737931/806621830383271937/1121055030825472060
[GitHub] Ani jsem netušila, že se dá GitHub takhle tunit. Hned jsem několik věcí vyzkoušela.
https://dev.to/supritha/how-to-have-an-awesome-github-profile-1969
---


https://www.linkedin.com/posts/ebandersen_programming-jobsearch-softwareengineering-activity-7097932834782289920-F2fx/


https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile


--- https://discord.com/channels/769966886598737931/789087476072710174/1205512562809110578
Ale jinak si přečti naši kapitolu o Gitu, je tam všechno podstatné, včetně kompletní příručky ke Gitu.

Najdeš na webu **Nauč mě IT** 🧠
https://naucme.it/chapter/qa-08
---


--- https://discord.com/channels/769966886598737931/1205441444291022889/1205441444291022889
Programováním se sice už nějakou chvíli živím, přesto Git/Github považuji za svoji velmi slabou stránku. Prošel jsem si v minulosti různými systémy (TFS, SVN, VS Online) a obávám se, že ve mně zanechaly kontraproduktivní návyky, které mi teď brání k plnému pochopení Gitu jako konceptu. Nebo se Git ve firmách, kde jsem dělal používal nějakým nestandardním způsobem, což opět vedlo k tomu, že mám spoustu otázek a pochybností. Potřeboval bych si věci ujasnit, osvojit si nějaké „best practices“ a zodpovědět například:
•    Musí se do veřejného repositáře přispívat pomocí forků a pull requestů, nebo je to možné nějakou přímočařejší metodou. Co je technicky možné, a co je doporučené?
•    Mohou kodéři commitovat přímo do master větve, nebo na sebemenší úkol musí vytvořit vlastní větev a u té pak dělat merge? Opět – co je možné, co je doporučené.
•    Liší se nějak Github a Gitlab?
•    Je možné si v Githubu vynutit revizi větve před merge do master?
•    Jak je to se spouštěním testů – kde se to nastaví, je to zadarmo?
•    Zkušenosti s nasazováním do více prostředí (testovací, produkční)
Bohužel všechny tutoriály, které jsem našel jen popisují, jak ovládat Git z příkazové řádky, všechno je takové sterilní, bez reálných konfliktů v kódu. Je to o tom jak, ne proč.
Vím, že toto se nedá snadno sepsat, tak mě zajímá, jestli by byl někdo ochotný mi otazníky výše objasnit v rámci nějakého mentoringu, případně jestli by se diskuse o zkušenostech s Gitem nemohla stát tématem některého z pondělních srazů. Díky.
---


https://opensource.net/why-single-vendor-is-the-new-proprietary/

That approach led to a lot of excesses, especially as Microsoft decided to exploit that dominant position. Openly-developed Open Source software grew in the 90s in reaction to this evil proprietary approach. In this model, software is produced as a commons by a community of organizations and individuals openly collaborating, and value is shared among the participants in the community. This is all made possible thanks to free and Open Source licenses which guarantee a number of freedoms, like the freedom to build on it without asking for permission, and the freedom to use it for any purpose, including making money.


Don't contribute to open source
https://www.youtube.com/watch?v=5nY_cy8zcO4


#} -->
