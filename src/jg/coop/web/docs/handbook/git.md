---
title: Jak na Git a GitHub
emoji: 🔀
stages: [learning, creating, preparing]
description: Co je Git a k čemu se používá? Jaký je rozdíl mezi Gitem a GitHubem? Jak začít s Gitem?
template: main_handbook.html
---

{% from 'macros.html' import blockquote_avatar, link_card, note with context %}

# Git a GitHub

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }} Kapitola se teprve připravuje.
{% endcall %}

Git je **nástroj, který ti umožňuje sledovat historii změn v kódu a sdílet kód s dalšími lidmi**. Je to program, který nainstaluješ do svého počítače a pracuješ s ním v příkazové řádce, nebo jej ovládáš např. prostřednictvím svého editoru. Git se dnes používá skoro v každé firmě. I když jeho výhody nejvíc oceníš při práci ve dvou a více lidech, může ti pomoci i jako jednotlivci: Zálohovat kód svých projektů jinam, synchronizovat jej mezi vlastním počítačem a internetem, na dálku jej někomu ukázat.

## GitHub

[GitHub](https://github.com/) je **úložiště kódu a něco jako sociální síť pro programátory**. Kód tam lze poslat pomocí Gitu. GitHub není jediným takovým úložištěm, další jsou např. GitLab nebo BitBucket. GitHub je ale nejoblíbenějším pro [open source](collaboration.md), takže tam najdeš nejvíc projektů a lidí.

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

## README

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }} Kapitola se teprve připravuje.
{% endcall %}


<!-- {#

https://dariagrudzien.com/posts/the-one-about-your-github-account/

- [ ] Co je GitHub - dává se tam kód, lidi spolupracují na komunitních projektech https://github.com/
- [ ] Naučit se Git a GitHub?
- [ ] yablko https://www.youtube.com/watch?v=0v5K4GvK4Gs
- [ ] MIT The Missing Semester https://missing.csail.mit.edu/2020/version-control/
- [ ] Nauč se Python https://naucse.python.cz/course/pyladies/sessions/foss/

https://git-scm.com/book/cs/v2
https://www.honeybadger.io/blog/git-tricks/

{% call blockquote_avatar(
  'GitHub vyčistit, _polishnout_, upravit. Stejně jako CVčko je to věc, která vás má prodat. Projekty, kterými se chlubit nechceš, radši skryj.',
  'jiri-psotka.jpg',
  'Jiří Psotka'
) %}
  Jiří Psotka, recruiter v [Red Hatu](https://www.redhat.com/en/jobs) v [prvním dílu podcastu junior.guru](../podcast/1.jinja)
{% endcall %}

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

Firmy používají na uložení Git repozitářů všechno možné, GitLab, BitBucket, možná by se dalo zmínit aspoň povrchně nějak i to. Samozřejmě na GitHubu je zase veškerý Open Source, tak se hodí to umět.

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

Díky toolingu ty začátky nemusej bejt tak hrozný. Když má Github tužtičku a webovej editor + CI systém, tak pro jednoduché změny člověk nemusí mít rozjeté lokální prostředí (a jak trefně pronesl @Honza Javorek jednou na Pyvu - díky "verified commit" člověk pozná, kdo používá tužtičku, protože prakticky nikdo neumí/nechce/nepotřebuje nastavit podepisování commitů 😁 ).

Ta věta zněla vlastně jako něco víc, než to ve skutečnosti je 😄 Upravuji projekty české Pythonní komunity, a to i tak většinou jde o obsah; postupně ale, jak ty projekty pročítám (web PyLadies, zpětnovazebník), cítím se jistější i co se týče kódu. Těm malým změnám vděčím pochopení kolaborativního workflow GH. Asi to bude trochu tak, že bariera nové ("mám beginner programovací skill") + nové (GitHub) je na začátku až moc. Přispění něčím, co umím líp (text, obsah, ...) v novém prostředí (GH) nepůsobí až tak děsivě. To mi nepřijde jako málo 🙂 Super. Takže tomu rozumím správně, že pro tebe cestou k OSS byla komunita kolem PyLadies, kde jsi v podstatě zjistila na co mrknout, kde můžeš přispět a případně i dostala radu jak a co udělat?

https://www.gitkraken.com/learn/git/tutorials

https://ohmygit.org/
https://learngitbranching.js.org/
Kdysi tady byla taková hravější verze: https://ohmygit.org/ ale po nějaké době používání musím říct, že je to poměrně chudé ve vysvětlování.

základní pitfalls k tomu, co lidi řeší s projekty na githubu
https://discord.com/channels/769966886598737931/789107031939481641/836969346403926096


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


--- https://discord.com/channels/769966886598737931/1061663829353844907/1061680592074326056
pro priste: https://ohshitgit.com/#magic-time-machine 🙂
---


--- https://discord.com/channels/769966886598737931/1027275076355231754/1027276811190665226
https://learngitbranching.js.org/
---


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


--- https://discord.com/channels/769966886598737931/789087476072710174/1215216528543453214
Ještě je dobré: https://ohshitgit.com
---


--- https://discord.com/channels/769966886598737931/789087476072710174/1214224330427207710
Slovníček na Git https://jvns.ca/blog/2023/11/01/confusing-git-terminology/
---


Jestli mohu z druhé strany, tak naučit se sám s Githubem je pro mě dost složité. Snažím se ho používat. Nedokážu si ale pořádně ujasnit, jak ho správně používat a k čemu by to mělo vést (asi tím, že to, co občas napíšu, jsou maličkaté věci). A bez zpětné vazby vlastně ani nedokážu posoudit, jestli jdu správným směrem.


--- https://discord.com/channels/769966886598737931/1241051418153058394/1241257870486671392
GitHub (a další podobné služby) se dají shrnout do toho, že jde o 2 části:
1) část, která je opravdu **git**, tedy to co máš i u sebe na disku v repository (tedy ta složka, kde si dala `git init` nebo sis to tam naklonovala přes `git clone`) a který leží i někde na jejich serveru (a je vyřešeno jak se tam připojíš po internetu)
2) všechny ty nadstavby kolem, ať už jde o prohlížení repa, jeho editaci přímo v prohlížeči, komentáře, issues, PR, projekty, hostování statických webů a hromada dalšího)

A samozřejmě při některých těch operacích vlastně GitHub za tebe píše příkazy Gitu, takže commity, merge atd. Jen to tam je trochu skryté tím, že jen zmáčkneš tlačítko. Ale stane se to a potom je potřeba `git pull` abys ty změny dostala k sobě.
---


#} -->
