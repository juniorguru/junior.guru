---
title: Jak na Git a GitHub
emoji: 🔀
stages: [learning, creating, preparing]
description: Co je Git a k čemu se používá? Jaký je rozdíl mezi Gitem a GitHubem? Jak začít s Gitem?
template: main_handbook.html
---

{% from 'macros.html' import illustration, note, lead, link_card, figure, github_profile_form with context %}

# Git a GitHub

{% call lead() %}
  Když děláš s kódem, bez Gitu se dnes nepohneš. Působí složitě, ale pro začátek stačí chápat, k čemu je, a ovládat pár příkazů. Ujasni si rozdíl mezi Gitem a GitHubem a osvoj si základy, které využiješ nejen při spolupráci s dalšími lidmi, ale i na vlastních projektech.
{% endcall %}

{{ illustration('static/illustrations/git.webp') }}

[TOC]

## Co je Git

Git je **nástroj, který ti umožňuje sledovat historii změn v kódu a sdílet kód s dalšími lidmi**. Je to program, který nainstaluješ do svého počítače a pracuješ s ním v příkazové řádce, nebo jej ovládáš např. prostřednictvím svého editoru.

{% call note() %}
  {{ 'lightbulb'|icon }} Nejde o zkratku, takže se název píše opravdu Git a ne GIT. Není to zkratka. Slovo „git” v britské angličtině hovorově znamená „blbec”.
{% endcall %}

Git se dnes **používá skoro v každé firmě**. Nejvíc jeho funkce vyniknou při práci ve dvou a více lidech, ale hodit se mohou i jednotlivcům:

- **Historie a záloha:** Když si rozdrbeš kód, můžeš se s Gitem bezpečně vrátit k přechozí, funkční verzi.
- **Sdílení:** Díky GitHubu můžeš kód někomu na dálku ukázat, třeba aby ti dal zpětnou vazbu a poradil.
- **Synchronizace:** S Gitem jde kód bezpečně nahrávat, stahovat a měnit z různých počítačů.

{% call figure('static/figures/git-home.webp', 'webovka Gitu') %}
  Webovka nástroje Git
{% endcall %}

## Jak se učit Git

Git je objektivně dost složitý a jeho příkazy nejsou moc intuitivní. **I profíci si z hlavy běžně pamatují nanejvýš pět příkazů, které používají denně**, ale u zbytku už musí hledat, jak se to správně používá. Stačí ti tedy pochopit, co vlastně Git dělá a možná i trochu jak to dělá, a potom zvládat aspoň pár příkazů.

**Začni postupně**, zatímco pracuješ na nějakém vlastním [projektu](projects.md). Po každé fungující změně si **ulož verzi kódu jako commit**. Klidně týdny dělej jen tohle. Pak se nauč, jak se dá vrátit k předchozím verzím.

Až budeš mít projekt trochu hotový, nahraj ho jako **repozitář na GitHub** a nauč se tam nahrávat další změny. Pak si zkus stáhnout cizí repozitář. A až potom koukej na **větve a _Pull Requesty_**. To stačí, nic víc se od juniorů neočekává.

Následující odkazy by ti měly dát dobrý základ. Něco jsou kurzy na YouTube, něco interaktivní hračky, které tě s Gitem naučí prakticky. A nakonec i kniha, ve které je úplně všechno.

Když budeš chtít pochopit nějakou konkrétní věc, třeba jak řešit _merge conflict_ nebo co je _.gitignore_, tak **si to nech vysvětlit od AI**, nebo **hledej klíčová slova na YouTube**.

<div class="link-cards">
  {{ link_card(
    'Git a GitHub od základov',
    'https://www.youtube.com/watch?v=0v5K4GvK4Gs',
    'Srandovní kurz Gitu a GitHubu od yablka.',
    badge_icon='play-circle-fill',
    badge_text='Kurz',
  ) }}

  {{ link_card(
    'Kurz Gitu s Mišom',
    'https://youtube.com/playlist?list=PLNAMH_0HgWT-ey31hQqrmi_Rgr4OVWgH3',
    'Kurz Gitu na Informatika s Mišom.',
    badge_icon='play-circle-fill',
    badge_text='Kurz',
  ) }}

  {{ link_card(
    'Version Control and Git',
    'https://missing.csail.mit.edu/2026/version-control/',
    'Lekce o Gitu z lekce The Missing Semester na MIT.',
    badge_icon='play-circle-fill',
    badge_text='Kurz',
  ) }}

  {{ link_card(
    'Oh My Git!',
    'https://ohmygit.org/',
    'Hra, která ti pomůže pochopit vztahy mezi commity a větvemi.',
    badge_icon='hand-index-thumb-fill',
    badge_text='Cvičení',
  ) }}

  {{ link_card(
    'Learn Git Branching',
    'https://learngitbranching.js.org/',
    'Interaktivní vizualizace, kde si osaháš větve, merge i rebase.',
    badge_icon='hand-index-thumb-fill',
    badge_text='Cvičení',
  ) }}

  {{ link_card(
    'Gitworking',
    'https://naucse.python.cz/course/gitworking/',
    'České materiály k celodennímu workshopu pro začátečníky.',
  ) }}

  {{ link_card(
    'How to Write a Git Commit Message',
    'https://chris.beams.io/git-commit',
    'Nauč se psát užitečné popisky ke commitům.',
  ) }}

  {{ link_card(
    'Pro Git',
    'https://git-scm.com/book/cs',
    'Bible o Gitu, zdarma online, částečně přeložená do češtiny.',
    badge_icon='book-fill',
    badge_text='Kniha',
  ) }}
</div>

## Ovládání Gitu

Git jde ovládat přes **příkazovou řádku** nebo přes nějaké **klikací rozhraní**. Prakticky každý editor na kód má na Git už něco zabudovaného v sobě, nebo si to můžeš snadno doinstalovat. Na ovládání Gitu klikáním není nic špatného ani neprofesionálního.

Počítej ale s tím, že **příkazová řádka je „společný jazyk“ všech návodů**. Klikací rozhraní každé vypadá a chová se trochu jinak. Když se však řekne `git pull origin main` nebo `git commit --amend --no-edit`, tak to všem funguje stejně.

A takovou jednoznačnost oceníš především když budeš hledat řešení svých problémů, ať už u AI, nebo člověka, který umí s Gitem, ale nezná tvůj konkrétní editor.

## Řešení problémů s Gitem

Asi neexistuje člověk, který někdy pracoval s Gitem a nikdy se do něj nezamotal. **Je to úplně běžné a stává se to i zkušenějším.**

Pokud se ti to stane, **nech si poradit od AI**. Vysvětli situaci a krok za krokem dojděte k nápravě. Ze zájmu si můžeš klidně projít **Oh Shit, Git!?!**, stránku, která zachránila několik generací, ale pokud něco zrovna řešíš, AI ti dnes už poradí úplně na míru pro tvou situaci.

<div class="link-cards">
  {{ link_card(
    'Oh Shit, Git!?!',
    'https://ohshitgit.com/cs',
    'Jak se vymotat z různých situací s Gitem.'
  ) }}

  {{ link_card(
    'Confusing git terminology',
    'https://jvns.ca/blog/2023/11/01/confusing-git-terminology/',
    'Vysvětlení všech tajemných názvů, které Git používá.'
  ) }}
</div>

## Co je GitHub

GitHub je **úložiště kódu a něco jako sociální síť pro programátory**. Kód tam jde poslat pomocí Gitu.

Od roku 2018 patří GitHub pod Microsoft. Další podobná úložiště jsou např. GitLab nebo Atlassian Bitbucket, a existují i řešení, která si může kdokoliv zprovoznit sám, jako Forgejo nebo Gitea. Všechny fungují na podobném principu:

- **Samotný Git server.** Dá se k němu na dálku Gitem připojit a kód tam poslat, nebo si ho stáhnout. Můžeš tam nahrát něco svého, nebo si stáhnout kód někoho jiného, kdo si tam na server veřejně odložil svůj repozitář se složkami a soubory.
- **Klikací rozhraní ke Gitu.** Máš možnost si repozitář prohlížet na webu. Vidíš i další věci z Gitu, jako historie změn, větve, commity, atd. Někdy můžeš přes prohlížeč posílat i změny. Mačkáš sice tlačítka, ale na pozadí se vlastně jen spouští příkazy z Gitu.
- **Všechno kolem.** _Issues_ na to, aby někdo mohl nahlásit chybu, nebo sdílet nápad. Komentáře. _Pull Requesty_ (někde se říká _Merge Requesty_), aby šlo poslat návrh na změnu kódu i do cizího repozitáře. Projekty… Možnost hostovat si tam statický web… Spouštění všelijakých automatizovaných testů… Tlačítko na vyžehlení prádla…

Historicky je GitHub nejoblíbenějším místem pro [open source](collaboration.md), takže **tam najdeš nejvíc projektů a lidí**. Většina kódu knihoven a frameworků, na kterých se staví software, se nachází právě tam. To má i své nevýhody. Když zrovna GitHub nejede, mnohdy si mohou programátoři udělat tak akorát procházku do parku.

{% call figure('static/figures/github-repo.webp', 'repozitář na GitHubu') %}
  Repozitář junior.guru na GitHubu, ve kterém je veřejně kód i této stránky
{% endcall %}

## Jak se učit GitHub

Na GitHubu je **milion funkcí a tlačítek**. Lidé, kteří jsou v oboru už dekádu nebo dvě, se v něm orientují dobře jen díky tomu, že jim to pod rukama rostlo postupně. Je přirozené, pokud tobě to přijde zahlcující a nepřehledné.

Je to ale podobné jako s Gitem. **Nikdo neočekává, že budeš hned znát všechno.** Pro začátek stačí [vytvořit si profil](github-profile.md), umět založit _repozitář_ a nahrát tam kód svého projektu, vědět co jsou _Issues_, co je _Pull Request_, a jak je vytvořit. Pokud se budeš umět popasovat i s _code review_, tak to je příjemný bonus.

Když budeš chtít pochopit nějakou konkrétní věc, **nech si to vysvětlit od AI**, nebo **hledej klíčová slova na YouTube**. Pro tyhle případy se ti bude hodit vědět, že způsob přispívání do projektů na GitHubu se označuje souhrnným názvem _GitHub Flow_. Najdi si to a zkus to pochopit.

Pokud se dostaneš do firmy, kde se nepoužívá konkrétně GitHub, znalost těchto konceptů se ti bude hodit i pro libovolný podobný systém.

<div class="link-cards">
  {{ link_card(
    'Git a GitHub od základov',
    'https://www.youtube.com/watch?v=0v5K4GvK4Gs',
    'Srandovní kurz Gitu a GitHubu od yablka.',
    badge_icon='play-circle-fill',
    badge_text='Kurz',
  ) }}

  {{ link_card(
    'The One About Your GitHub Account',
    'https://dariagrudzien.com/posts/the-one-about-your-github-account/',
    'Jak přistupovat ke svým projektům a profilu na GitHubu'
  ) }}
</div>

## Dávej kód na GitHub

U začátečníků platí, že **nemají co schovávat** a měli by světu **ukázat co nejvíce toho, co dokázali vytvořit, nebo co zkoušeli řešit**. Můžeš tím jen získat.

No a GitHub je příhodné místo, kam všechny své projekty a pokusy nahrávat. Zároveň tam mají své projekty i všichni ostatní a jde tam spolupracovat s lidmi z celého světa. Je to **hřiště pro programátory, kde si každý experimentuje na čem chce.**

Takže si [vytvoř profil](github-profile.md) a všechno naházej do repozitářů. Naučíš se lépe ovládat Git a budeš moci svůj kód ukázat, když budeš chtít zpětnou vazbu, nebo potřebovat [pomoc na dálku](help.md).

Máš **strach, že někdo tvůj kód uvidí a pomyslí si, že nic neumíš?** Přečti si [GitHub jako polička v dílně](github-profile.md#github-jako-policka-v-dilne), snad to rozptýlí tvoje obavy.

## Čti kód na GitHubu

Většina otevřeného kódu na světě je na GitHubu. **Využívej jeho vyhledávání a pokukuj po inspiraci**, jak se dá co řešit.

Můžeš koukat pod ruce různým projektům a organizacím, třeba [datovým novinářům z Českého Rozhlasu](https://github.com/DataRozhlas), [Hlídači Státu](https://github.com/HlidacStatu), [české Python komunitě](https://github.com/pyvec/), nebo třeba i [junior.guru](https://github.com/juniorguru/).

Když vyhledáš vhodný výraz, můžeš se třeba podívat, jak někdo jiný používá konkrétní framework, knihovnu, funkci. Nebo hledat [nezabezpečené projekty jiných lidí](https://github.com/search?q=django_secret_key&type=code) a připadat si jako velký hacke… ehm, upozorňovat je, že by si to měli opravit.

Pamatuj ale na to, že **najdeš i spoustu nekvalitního kódu**, takže vždycky zvaž, jestli se tím, co vidíš, chceš opravdu inspirovat. Když najdeš něco, čemu nerozumíš, konzultuj to v [komunitách](community.md), nebo aspoň s AI.

No a nemusíš jen koukat, do **open source** projektů [můžeš i přispět](collaboration.md)! To, že jsi na začátku, neznamená, že nemůžeš objevit chybu nebo opravit větu v dokumentaci. A odvaha být v tomto směru aktivní se u juniorů dost cení.

{% call figure('static/figures/github-data-rozhlas.webp', 'organizace na GitHubu') %}
  Projekty datového týmu Českého Rozhlasu s veřejným kódem na GitHubu
{% endcall %}

## GitHub a pohovory

Pokud tě někdo straší, že si tvůj GitHub budou procházet náboráři a máš jej proto mít sterilně dokonalý, nenech se tím zmást. **Recruiteři kód nečtou.**

Manažeři a senioři občas ano, ale podstatné je, jestli jim dáš v CVčku pod nos **konkrétní projekty, kterými se chceš chlubit**, nebo jim předhodíš jen tak celý profil a necháš je tápat.

Sekce [GitHub jako vitrínka](github-profile.md#github-jako-vitrinka) v návodu na GitHub profil nebo [Projekty](cv.md#6-projekty) v návodu na CV ti dají praktické tipy, jak GitHub používat jako dílnu a zároveň zajistit, že pohovorující nebudou zakopávát o nepořádek.

{{ github_profile_form() }}
