---
title: Jak se naučit programovat
emoji: 🚀
stages: [trying, learning]
description: Jak začít programovat? Tady máš úvod do programování v podobě rozcestníku na nejlepší a nejefektivnější materiály
template: main_handbook.html
---

{% from 'macros.html' import blockquote_avatar, lead, link_card, engeto_video_card with context %}


# Nauč se základy programování

{% call lead() %}
  Jak začít programovat? Zde najdeš pečlivě nachystané jen to, co pro tebe bude do úplného startu nejlepší a nejefektivnější. Až tím projdeš, můžeš začít [získávat praxi](practice.md).
{% endcall %}

[TOC]

## Co budeš potřebovat    <span id="requirements"></span>

### Vybavení, které musíš mít    <span id="equipment"></span>

Především budeš potřebovat **počítač a internet**. Na mobilu ani tabletu se programovat prakticky nedá a bez připojení nebudeš mít materiály, ani nenajdeš potřebnou pomoc.

Ideální je mít svůj vlastní počítač, nad kterým máš plnou kontrolu a na němž je operační systém Linux, Windows nebo macOS. Pokud máš jiný systém, jako Android nebo ChromeOS, možná se ti povede na něm programování rozjet, ale v praxi je k tomu nikdo nepoužívá a budeš mít velký problém sehnat někoho, kdo ti poradí v případě problémů. Na mobilu můžeš některé věci procvičovat, ale je to jako se v appce učit akordy, vzorečky nebo slovíčka — praktické znalosti tím nezískáš.

{{ engeto_video_card(
  'Vybavení a programy, které budeš potřebovat',
  '5min',
  'https://www.youtube.com/watch?v=Z-r8xiKX6uM&list=PLrsbT5TVJXZa2daxo8_3NagDzPqHjBEpI',
  'K programování se ti bude hodit hned několik věcí – notebook, připojení k internetu nebo třeba programy, ve kterých si můžeš zkusit psát kód.',
) }}

### Sežeň si kamarády    <span id="friends"></span>

Říká se, že **navazování mezilidských vztahů** by mělo vyplňovat pětinu času, který trávíš učením (tzv. [model 70-20-10](https://en.wikipedia.org/wiki/70/20/10_Model_(Learning_and_Development))). Navíc budeš potřebovat **velké množství motivace**. Možná si čteš tento text a přijde ti, že jí máš vrchovatě, ale věř tomu, že už zítra jí bude méně a za týden jí bude polovina. Zvláště pokud neděláš prezenční kurz a chystáš se do toho jít jako samouk, nebudeš mít ani žádné termíny, ani lidi kolem sebe, díky kterým se u učení udržíš. Je snadné další lekci odložit, protože se ti to zrovna nehodí, potom ji odložit znova, a tak dále.

Najdi si proto **studijní skupinu**. Ať už do toho půjdeš s kamarádkou nebo místním zájmovým kroužkem, v partě to prostě odsýpá lépe a máš mnohonásobně, opravdu mnohonásobně vyšší šanci na úspěch. Využít můžeš přímo i [zdejší online klub](../club.md).

### Co je dobré umět předem    <span id="prerequisities"></span>

S programováním můžeš začít úplně v pohodě pouze se **základy ovládání počítače**. Potřebuješ umět vytvořit a najít soubor nebo adresář (složku). Potřebuješ umět nainstalovat nový program.

Dále se ti mohou hodit **základy matematiky ze základky**: třeba co je to dělení se zbytkem nebo obsah čtverce. Detaily nejsou potřeba, vzorečky se dají najít na Wikipedii. Spíš potřebuješ vědět, že když máš pokoj tři krát čtyři metry, tak se tyhle čísla dají nějak zkombinovat a zjistíš výměru podlahy.

Budeš mít výhodu, pokud budeš [**rozumět alespoň psané angličtině**](english.md). Materiály a kurzy pro začátečníky najdeš i v češtině, ale brzy zjistíš, že spoléhat se jen na ně je velmi omezující.

### Kolik to bude stát    <span id="price"></span>

Nemusí to stát **žádné peníze**. Ano, existují placené kurzy, placení mentoři, [placené komunity](../club.md), ale jde to i bez toho. Pokud máš počítač a internet, můžeš se naučit programovat bez jakýchkoliv dalších investic. Některé kurzy dávají své materiály zdarma k dispozici, na problémy můžeš najít řešení v diskuzích na internetu, učební kroužek si můžeš zorganizovat i mezi svými kamarády. Pokud ale nějaké peníze do svého učení investovat můžeš, **mohou tvou cestu usnadnit a urychlit**.

### Kolik času potřebuješ    <span id="time"></span>

Úplně první program vytvoříš v řádu hodin nebo dní, ale pokud chceš mít [základ vhodný pro start kariéry v IT](candidate.md#co-budou-chtit), budeš se tomu potřebovat věnovat **alespoň 3 měsíce po 10 hodinách týdně** (orientační odhad, každý má jiné možnosti, tempo, výdrž…). Je to stejné jako u sportu nebo hry na hudební nástroj: Princip možná pochopíš rychle, ale budeš muset vždy hodně procvičovat, než to budeš umět správně použít v praxi.

Co když **nemáš čas**? „Nemám čas“ znamená „nechci si jej vyhradit, jelikož mám důležitější věci, nebo věci, které mě baví víc“. Možná se ti jen líbí představa, že umíš programovat, ale nechce se ti to doopravdy dělat, stejně jako se spoustě lidem líbí představa, že umí hrát na kytaru, ale nemají chuť si po večerech brnkat a cvičit akordy. Je úplně v pořádku dělat důležitější nebo zábavnější věci, akorát [je dobré si to přiznat](https://twitter.com/mjavorek/status/687386493036396544), vědomě to nechat plavat a nevyčítat si to.

Možná opravdu chceš, ale máš náročnou práci, chodíš domů po večerech a během volna se sotva stíháš zrelaxovat nebo postarat o rodinu. Bohužel, bez času to nejde. Naučit se při tom všem programovat bude velmi těžké. I takoví se ale našli! **Nevzdávej to a zkus vymyslet, jak by šlo tvůj den uspořádat jinak**, jestli by některé povinnosti nemohli dělat jiní lidé, atd. Někdo se učí o víkendech nebo po večerech, když usnou děti. Někdo má prostoje ve svém zaměstnání, tak se učí během nich.

{{ blockquote_avatar(
  'Pracovala jsem už v IT, ale chtěla jsem lepší pozici. I se dvěma dětmi a plným úvazkem to šlo, po večerech jsem dělala vlastní projekty a dálkově studovala. Byl to koníček, nevadilo mi u toho trávit volný čas.',
  'vladlena-benesova.jpg',
  'Vladlena Benešová',
  'Vladlena Benešová, bývalá marketérka, nyní programátorka'
) }}

### Nauč se učit    <span id="learning"></span>

Jakmile se jednou pustíš do programování, nastoupíš do vlaku, jenž už se nikdy nezastaví. Technologie se vyvíjejí rychle a tak je programování, možná více než jiné obory, o neustálém učení. Někdo to dovádí do extrému a hltá hned každou novinku, ale ani **běžný programátor nemůže úplně zaspat a často se téměř každý týden naučí něco nového**, třeba i průběžně během práce.

Neočekávej, že se programování jednou naučíš a vystačíš si s tím. Neměj ale ani hrůzu z toho, že se učíš programovat dva roky a stále toho ještě spoustu neumíš. **Učí se neustále i ti, kteří mají desítky let zkušeností.** Nemá tedy smysl se tím příliš trápit. Najdi si vlastní tempo a způsob, jakým se dokážeš učit efektivně a jak tě to bude nejvíce bavit. Někdo leží v knihách, jiný si pouští návody na YouTube, další si zase nejraději zkouší věci prakticky. Cokoliv z toho je v pořádku, hlavně pokud ti to sedí.

### Co nepotřebuješ    <span id="myths"></span>

O programování [koluje řada mýtů](myths.md). Třeba že se o něj můžeš zajímat jen pokud jsi geniální na matematiku, že se to musí roky studovat na vysoké škole, že to není pro holky, že už je pro tebe pozdě začít. Jsou to pouze předsudky, nenech se jimi odradit! Raději si projdi [příběhy lidí, kteří se programovat naučili](../stories.md) a dnes jim to pomáhá při práci, nebo se tím začali přímo živit.

<small>Rady v této kapitole volně vychází i z [úvodní lekce týmového online kurzu Petra Viktorina](https://naucse.python.cz/2021/online-jaro/adm/intro/), se svolením autora. Díky!</small>


## Proč Python?    <span id="python"></span>

Ať už budeš nakonec dělat cokoliv, začít s programovacím jazykem [Python](https://python.cz) je skvělý tah. Je to nejvhodnější první jazyk.

*   Dobře se učí. Neobsahuje příliš mnoho divných značek, vypadá spíš jako anglická věta.
*   Má přátelskou komunitu lidí, kteří píšou materiály pro začátečníky a pořádají nejrůznější akce.
*   Dobře se hledá pomoc při řešení problémů během učení, a to i v češtině.
*   Je to dnes jeden z nejpoužívanějších a nejoblíbenějších jazyků vůbec.
    *   [InfoTech News: Oficiální jazyk pro výuku ve Francii](https://meterpreter.org/python-will-become-the-official-programming-language-for-french-high-schools/)
    *   [The Economist: Stává se nejoblíbenějším jazykem na světě](https://www.economist.com/graphic-detail/2018/07/26/python-is-becoming-the-worlds-most-popular-coding-language)
    *   [StackOverflow: Jazyk s nejrychleji rostoucí popularitou a druhý nejmilovanější](https://insights.stackoverflow.com/survey/2019)
    *   [Vývoj dat ze StackOverflow: Během 10 let se stal nejoblíbenějším jazykem](https://www.youtube.com/watch?v=cKzP61Gjf00)
    *   [JetBrains: Třetí jazyk, který lidé mají jako hlavní. První, který se nejvíc učí](https://www.jetbrains.com/research/devecosystem-2018/)
    *   [ZDNet: Odhaduje se, že do několika let bude nejpoužívanější na světě](https://www.zdnet.com/article/programming-languages-python-predicted-to-overtake-c-and-java-in-next-4-years/)
*   Je univerzální: tvorba webu, servery, datová analýza, automatizace, vědecké výpočty, …
*   Existuje pro něj [mnoho nabídek práce](http://python.cz/prace).

Co když ale bude nakonec v pracovním inzerátu Java? Důležité je především umět programovat — další jazyk nebo technologie se dá doučit poměrně rychle.

{{ blockquote_avatar(
  'Píšou mi lidi, že se chtějí naučit programovat. Posílám je na kurzy Pythonu.',
  'jakub-mrozek.jpg',
  'Jakub Mrozek',
  'Jakub Mrozek, propagátor jazyka JavaScript'
) }}


## Jak začít    <span id="learn"></span>

Nemusíš se přebírat hromadami možností a přemýšlet, do které se vyplatí investovat. Tyto materiály prošly pečlivým a přísným výběrem. Jsou to ty nejlepší dostupné. Vyber si jeden z následujících materiálů podle toho, jestli ti více vyhovuje kurz nebo kniha, a začni!

<div class="link-cards">
  {{ link_card(
    'Nauč se Python!',
    'https://naucse.python.cz',
    'Nejlepší české textové materiály.',
    badge_icon='layout-text-sidebar-reverse',
    badge_text='Online kurz',
  ) }}

  {{ link_card(
    'Engeto',
    'https://learn.engeto.com/cs/kurz/python-uvod-do-programovani/studium/7vOS92OWQgWOzK6WDxF4cw/uvod-do-programovani/ciselne-hodnoty/komplikace-s-cisly',
    'Jediný plně interaktivní kurz v češtině.',
    badge_icon='layout-text-sidebar-reverse',
    badge_text='Online kurz',
  ) }}

  {{ link_card(
    'Coursera',
    'https://www.coursera.org/learn/python',
    'Profesionálně vedený video kurz University of Michigan.',
    badge_icon='layout-text-sidebar-reverse',
    badge_text='Online kurz',
  ) }}

  {{ link_card(
    'Codecademy',
    'https://www.codecademy.com/learn/learn-python-3',
    'Kurz založený na textu a cvičeních. Rychlejší postup, méně hloubky.',
    badge_icon='layout-text-sidebar-reverse',
    badge_text='Online kurz',
  ) }}

  {% call link_card(
    'Umíme informatiku',
    'https://www.umimeinformatiku.cz',
    badge_icon='list-check',
    badge_text='Cvičení',
  ) -%}
    Uč se skrze cvičení a opakování. [Podloženo výzkumem](https://www.umimeto.org/podlozeno-vyzkumem).
  {%- endcall %}

  {{ link_card(
    'Ponořme se do Pythonu 3',
    'http://diveintopython3.py.cz/index.html',
    'Možná strohá, ale i tak nejlepší kniha přeložená do češtiny.',
    badge_icon='book',
    badge_text='Kniha',
  ) }}

  {{ link_card(
    'Automate the Boring Stuff with Python',
    'https://automatetheboringstuff.com',
    'Nejlepší kniha do startu. Nech nudnou práci dělat počítač!',
    badge_icon='book',
    badge_text='Kniha',
  ) }}
</div>


<!-- {#

Motivace: když koukáš na video, není to reálný odraz práce programátora
https://discord.com/channels/769966886598737931/789045589869461536/825440188858630194

2. Jak si vybrat první jazyk
https://www.youtube.com/watch?v=NE-cOGmaMWs

https://www.youtube.com/watch?v=EkUuXQUByuw

Ebbinghaus observed that each time the newly-learned information was reviewed, the EFC was reset at the starting point, but with a *slower decay curve*.
https://twitter.com/SahilBloom/status/1597940360025899008

- stránka pro úplné začátečníky s code.org a scratchem pak poslat Pavlovi
- Je daleko jednodušší začít v malém při aktuálním fungování, než se pokoušet o něco velkého, co pravděpodobně nevydrží.

Kapitola o mobilech

KSI, neboli Korespondenční seminář z informatiky, je celoroční soutěž organizovaná primárně studenty Fakulty informatiky Masarykovy univerzity. Cílem semináře je seznámit řešitele se zajímavými oblastmi informatiky a procvičit programátorské, matematické a logické myšlení. Seminář je uzpůsoben jak pro úplné začátečníky, kteří si na jednoduchých příkladech procvičí danou problematiku, tak pro zkušenější řešitele, kteří se pokusí pokořit hlavní soutěžní úlohy.
https://ksi.fi.muni.cz/

„Java je ve světě Androidu za zenitem (aspoň v mojí android-sociální bublině). I Google už všude tlačí Kotlin, i když Java je pořád supported, není deprecated. Nový projekty se určitě začínají jen v Kotlinu, tam není nad čím přemýšlet. Občas pracujeme se staršíma codebases, kde je ještě Java, ale většinou se to postupně překlápí na Kotlin. Jeden z velkých problému Javy na Androidu je (krom soudních sporů s Oraclem), že nejsou podporovány nové verze Javy. Teď jde myslím používat Javu 11, ale dlouho to byla 8.“
„Řekl bych, že výhoda to je, protože Android je napsán v Javě. Takže ty jako vývojář sice kódíš aplikaci v Kotlinu, ale používáš vlastně APIs napsané v Javě. Když budeš koukat na implementaci něčeho v Android SDK, tak to bude v Javě. Ten Kotlin je pořád vázanej na tu Javu, takže si myslim, že znát Javu je dobrý.

Asi bych to popsal tak, ze zatimco FE nebo BE je specialista na svuj obor, FS je ferda mravenec, prace vseho druhu, umi vsechno, ale mozna nic tak do hloubky. Takovi univerzalove se hodi a obcas existuji, vetsinou ale mozna se spis nejaky BE nauci trochu React nebo naopak FE se nauci Node.js a pak si rikaji FS, ale realne je to clovek, ktery tu hlubokou znalost ma pouze v jednom z tech dvou oboru. A to nemluvim o tom, ze FE bys mohl rozdelit na FE-JS a FE-vizuál, takze full-full-stack by musel umet veci od optimalizace obrazku a animace SVG po optimalizaci databazovych dotazu, coz podle me nikdo proste neumi a ani umet nemuze. Timto bych dal tu pozici do kontextu, ale mozna to jen vidim moc názorově :)

https://www.freecodecamp.org/news/what-is-web-development-how-to-become-a-web-developer-career-path/

Suma sumárum je to 10 měsíců od chvíle, kdy jsem se rozhodl změnit kariéru z učitele na programátora. Doufám, že vám tohle trochu pomůže a nabudí vás to. Kdyžtak se na cokoliv ptejte.
jak jsem se učil - https://discord.com/channels/769966886598737931/789107031939481641/866373605951537173

https://www.freecodecamp.org/news/what-is-web-development-how-to-become-a-web-developer-career-path/

STRANKA LEARN BY MELA JIT "VIC NA BRANU"
jeste me napadlo,ze tvuj web resi takovy "high level plan" - nauc se to, ziskej praxi a pak hledej praci. Mozna by se hodil i jeste podrobny plan. Kdyz nekdo chce zacit ale vlastne nevi z ktere strany zacit rozmotavat bavlnku. Materialu je hodne - i na tvoji strance. Kurzy, knihy, ruzne online dokumenty.. je toho ale az prilis mnoho. Mozna nejaky kratky clanek co by se melo pred cim a tak precist ci co by pomohlo tem uplne ztracenym. Treba me to prijde desne zamotane. Ja treba jdu jen po tech anglickych materialech a furt nevim kde zacit. Co otevru chce po me hned penize - ale to se mi nelibi, protoze ja nevim jestli to uplne na 100% chci delat. Takze bych chtela neco nacist a vyzkouset na kratkem cviceni pred tim,nez se treba upisu na kurz. Ale tohle jsem nejak nenasla. Na tvych strankach jsem nasla knihu - ale zase cist jen teorii mi prijde naprd :/ nejaka rada? s cim zacit jako prvni? jak se posunout kdyz si stale v te prvni katergorii "nauc se programovat"

Learn learn learn loop
https://twitter.com/OzolinsJanis/status/1420344259367030784

- Why procrastinators procrastinate
- konec prokrastinace
- ADHD

část „zkouším“ v cestě juniora by měla být o code.org a scratchi

jak začít https://overcast.fm/+kY7RkAu9Q

https://exercism.org/tracks/python/concepts
https://www.codecademy.com/code-challenges

https://www.english4it.com/
https://www.bbc.co.uk/learningenglish/english/

https://blog.lewagon.com/skills/programming-language-to-learn/

- Nebal bych se SRE rozepsat slovy, prijde mi to tam jako zbytecna zkratka (navic pro me konkretne stejne z prvni neznama). Coz me privadi na myslenku - na spoustu veci tam mas odkazy k zajimavym clankum. Kdyz bys tady k tem "starer pozicim" neco takovyho nasel, IMO by to byl supr zdroj informaci.

programování v shellu https://www.youtube.com/@LukasBarinka/playlists

operační systémy https://www.udacity.com/course/introduction-to-operating-systems--ud923
linux https://www.abclinuxu.cz/ucebnice/obsah

jak se učit - téma deep work.
Jak se učit - tutorial hell https://youtu.be/jvpXA3aNbak
jak se učit https://www.youtube.com/watch?v=e9RWnQRq2pg&t=186s

nevhodné rady pro začínající vývojáře https://overcast.fm/+U67GNYVtg

Hodně lidí si dělá výpisky a vlastní poznámky - když ty věci přímo píše, mnohem lépe si je zapamatuje. Já jsem na škole vyráběl taháky pro ostatní a díky tomu jsem se látku naučil a tahák nakonec sám nepotřeboval 😀 Nebo https://github.com/aspittel/coding-cheat-sheets takhle myslím začalo. Nechceš to taky nějak zmínit?

jak začít - kurz engeto https://docs.google.com/document/d/19czo7_jGVcA9Zy6nDT6RJRe7W7IS-XxZY-0Ky-GZ3bw/edit#

Command Line Interface Guidelines https://clig.dev/

Popisy pracovních pozic v it jsou užitečné i HR 🤔

Sekce o samotném učení a jak se učit efektivně, o ucicim procesu - Mrozek, atomic habits, Messenger

https://grasshopper.app/

lessons from reddit https://www.reddit.com/r/learnprogramming/comments/itbw45/lessons_for_beginners_and_junior_developers_after/

Ahoj, čtu si tvou novou knihu a velmi mě zaujala kapitola: Existují pozice vhodnější pro začátečníky? To je věc s kterou hodně bojuju při výběru práce. Jen za mě: Já bych ty pozice možná trochu více rozepsal ono začátečník, který nebyl v žádné IT firmě se v tom asi bude ztrácet co takové pozice obnášejí ve skutečnosti. Že bych možná uvedl nějaký pohled z praxe co tak budu nejspíš na dané pozici konkrétně dělat. Obecně to tam teda máš, ale kdybych se chtěl rozhodnout, která by mě bavila více a na kterou use více zaměřovat, tak to z toho moc nepoznám. A potom kdybych byl na pohovoru tak jako začátečník bych asi absolutně nepoznal jestli firma prosazuje opravdové DevOps nebo rychle potřebuje zalepit díru v ruční správě serverů. Ale jinak super ja se třeba na DevOps vůbec nehlásil protože mi přišlo že je to vyloženě seniorní pozice 😄 A že existuje nějaké SRE nebo reliable engineer jsem vůbec netušil. Naopak jsem se pořád hlásil na tech support a sys admin nebo tester, protože jsem měl pocit, že jiná vstupní brána neexistuje. Ale ani jednu jsem nějak moc dělat nechtěl. Možná automatického testera. Měl jsem to tak asi, že Lumír z Ostravy nám říkal, že většina programátorů začínají nejdříve jako testeři.

teach yourself new things efficiently

Jak vybrat programovací jazyk
https://www.itnetwork.cz/jak-vybrat-programovaci-jazyk
https://honzajavorek.cz/blog/proc-se-neucit-python-v-roce-2021/

Jak se ucit react
https://discord.com/channels/769966886598737931/822415540843839488/845202549609857034

https://www.tiobe.com/tiobe-index/

https://ehmatthes.github.io/pcc_3e/

S JavaScriptem vidím několik problémů, které si my pokročilí programátoři často neuvědomujeme: 1) Nenašel jsem pro něj dobré aktuální a ucelené materiály v češtině 2) Má několik oddělených světů a návody pro začátečníky jsou roztříštěné v tom, který zrovna protežují - prohlížeč, Node.js, React, atd. 3) Aby v něm začátečník mohl něco hezkého udělat, potřebuje HTML a ideálně i CSS jako prerekvizity, což v důsledku znamená, že aby šlo s JS začít jako s prvním jazykem, je potřeba už dva jiné jazyky umět. Pro tyto důvody doporučuji začít s Pythonem a potom přejít tam, kam to koho táhne.

celej tenhle thread o materialech na nauceni a prvnich kurzech
https://www.facebook.com/groups/pyonieri/permalink/3125620044116818/

analytik junior je někdo, kdo má silné analytické myšlení a umí rozebrat problém, umí ho zpracovat, dohledat, nastudovat, dát dohromady všechny informace, vyptat od lidí a něco k tomu sám sepsat  senior za mě umí takové lidi vést a nebo umí řešit mnohem komplexnější problémy, nemá se třeba už koho ptát a podobně

jak se učit, jak navrhnout materiály, křivka
https://launchschool.com/pedagogy

kdyz budou na JG povolani, tak pod sebou muzou mit seznam skillu, ale ty vymakanejsi by mohly mit primo "ROADMAP"

https://www.welcometothejungle.com/cs/articles/front-end-developer-cz

Já používám VS Code, ale hodně lidí má oblíbený PyCharm. Záleží, co člověk hledá. Python jde programovat v každém obyčejném editoru (něco jako manuální řízení v autě), a pak jsou tady integrovaná prostředí jako PyCharm, která se snaží pomoct se vším možným (něco jako automat s parkovacím asistentem :)). Každému vyhovuje něco jiného a na výsledek to nemá vliv.

Ponořme se do Pythonu 3 vs Výukový kurz Python 3
Luděk Reif Honza Javorek Četl jsem oboje, a zdá se mi, že co do kvalit je to oboje dobré, co do obsahu i stylu je to docela rozdílné. Obojí má něco do sebe, Ponořme se do Pythonu 3 je méně obsáhlé, jde na to hodně přes příklady, takže člověk si to osahá, ale ne vždycky to všechno pochopí do detailu. Výukový kurz Python 3 má nějaké úvodní seznámení, kde se člověk dozví základy, a pak jde se vším docela do hloubky s tím, že je všechno v kapitole okecané, pak jsou nějaké příklady a pak je nějaké zadání, aby si to člověk vyzkoušel. Je to fajn, ale skoro bych řekl, že to začátečníka na těch dalších kapitolách může odrovnat. Já jsem ji jeden čas odložil a přečetl jedním dechem Ponořme se do Pythonu 3, kde nebylo tolik teorie nebo tolik popisování. Na začátek bych skoro řekl, že by bylo ideální to zkombinovat, dát si jako základ prvních pár lekcí z Výukového kurzu, pak přečíst Ponořme se do Pythonu, a pak dočíst Výukový kurz :)

Front-end Developer Handbook 2019
https://frontendmasters.com/guides/front-end-handbook/2019/

pozice v IT nápady z Discordu
https://discord.com/channels/769966886598737931/769966887055392768/919890459877310474

jQuery
Já osobně bych se dnes už jQuery asi neučil. Možná pro nějaké povědomí, abych to uměl aspoň "přečíst", ale bral bych to spíš jako Python 2 (nebo Python 2 před pár lety): Můžu se s tím ještě setkat, budou v tom nějaké produkční věci, ale budoucnost jde už jinudy.  Pokud chceš mít celou webovku v JavaScriptu, je řešením React (popř. framework jako Next.js) nebo Vue.js apod.  Pokud chceš JavaScriptem jen kořenit svoje HTML, dost dlouho si dnes vystačíš s čistým (tzv. vanilla) JS, protože co dřív nešlo (a díky jQuery to šlo), tak dnes jde přímo v browseru. Zdroje:  https://caniuse.com/ https://htmldom.dev/ https://developer.mozilla.org/en-US/docs/Web/JavaScript

U pozic procentový koláč kolik stráví času čím

The Modern JavaScript Tutorial
https://javascript.info/

Codecademy Go, Encode (Android only), alebo Grasshopper (iOS, Android). Kludne vyber len niektore z nich podla tvojich potrieb. Imho povazujem Sololearn a Mimocode, co si tam uviedol,  za class-leading. I ked som nazoru ako ty, ze ucenie sa na mobile je totalne nahovno.. :D

BI lidi
https://discord.com/channels/769966886598737931/788826407412170752/846461087711756319



JAVA VS KOTLIN
Honza Javorek, [27. 5. 2021 18:22:18]:
@petrnohejl Jak moc je Java na Androidu za zenitem? Dá se to dnes pořád označit za jazyk, ve kterém se vyrábějí mobilní appky, nebo už to není pravda a všichni, co to dnes myslí vážně, jsou na Kotlinu? Pokud jo, znamená to, že Java zůstává zase jenom jako jazyk na velký systémy pro korporátníky?

A když umíš Javu, naučíš se Kotlin rychleji nebo je to úplně jiný jazyk?

@honzajavorek Java je ve světě Androidu za zenitem (aspoň v mojí android-sociální bublině). I Google už všude tlačí Kotlin, i když Java je pořád supported, není deprecated. Nový projekty se určitě začínají jen v Kotlinu, tam není nad čím přemýšlet. Občas pracujeme se staršíma codebases, kde je ještě Java, ale většinou se to postupně překlápí na Kotlin. Jeden z velkých problému Javy na Androidu je (krom soudních sporů s Oraclem), že nejsou podporovány nové verze Javy. Teď jde myslím používat Javu 11, ale dlouho to byla 8.

Petr Nohejl, [27. 5. 2021 21:07:24]:
Řekl bych, že výhoda to je, protože Android je napsán v Javě. Takže ty jako vývojář sice kódíš aplikaci v Kotlinu, ale používáš vlastně APIs napsané v Javě. Když budeš koukat na implementaci něčeho v Android SDK, tak to bude v Javě. Ten Kotlin je pořád vázanej na tu Javu, takže si myslim, že znát Javu je dobrý.

A když se učíš Kotlin jako jazyk a znáš Javu, tak to máš asi jednodušší v tom, že Kotlin je taková vylepšená moderní Java, takže asi snadnějc pochopíš co jak funguje.

Na druhou stranu to může být i kontraproduktivní - můžeš pak psát Kotlin kód s Java mindsetem, což je vlastně taky špatně. Nevyužiješ plnou sílu Kotlinu.

Testeři
https://discord.com/channels/769966886598737931/788826407412170752/846454895199387690

Co je Full Stack
Asi bych to popsal tak, ze zatimco FE nebo BE je specialista na svuj obor, FS je ferda mravenec, prace vseho druhu, umi vsechno, ale mozna nic tak do hloubky. Takovi univerzalove se hodi a obcas existuji, vetsinou ale mozna se spis nejaky BE nauci trochu React nebo naopak FE se nauci Node.js a pak si rikaji FS, ale realne je to clovek, ktery tu hlubokou znalost ma pouze v jednom z tech dvou oboru. A to nemluvim o tom, ze FE bys mohl rozdelit na FE-JS a FE-vizuál, takze full-full-stack by musel umet veci od optimalizace obrazku a animace SVG po optimalizaci databazovych dotazu, coz podle me nikdo proste neumi a ani umet nemuze. Timto bych dal tu pozici do kontextu, ale mozna to jen vidim moc názorově :)
https://discord.com/channels/769966886598737931/811910782664704040/846492496757522433

Jak se učit JS
https://discord.com/channels/769966886598737931/788832177135026197/843210448907796530

jak zacit dobre popsany
https://www.facebook.com/groups/144621756262987/permalink/751143055610851/?comment_id=751238438934646&__cft__[0]=AZVKjm7wAzrkPFDDUggJDx0eNIqmzCaF7csOnAy0GSx2JazUV0KOThy5NvDOtQRMGzmOGKmfIm0DwElpMyqrNpEo5ZCzI8C5q17O5JbyXnwUBJM709tIfEHt7d_haTungS7fLOqNpVTWIpiwRy4s1VSi5mxzeOn5WTLGi-9-qUvLG1BBL9hoKRAtmQIXllHA--pAGi_JfG91C08kq95vPalCR9e7pG6rr8Gg8jRxFN4gGA&__tn__=R]-R

neučit se syntaxi jako slovíčka
https://discord.com/channels/769966886598737931/769966887055392768/815922886321504286

Proč ne JS
https://www.facebook.com/groups/144621756262987/permalink/813286826063140/?comment_id=813500689375087&__cft__[0]=AZXAn_nbuF1kW3AEN7acnei0Y9a82mmOAIoSYwseVuho9hVSZiBaJvMDr2sHAPF5rlq6_zxh1vOXcL2MLwMpB3qbh8cEABSXVe76nsxjUFtsahFPE00-q_HBhYBFln_aN8OIbDjitvSjHGXzhCPGWX8NVBKt4Otwa3wM3fdEk6CPsksxM-CNjFJveQIHaHwIuEQ&__tn__=R]-R

Kontext pro php
https://discord.com/channels/769966886598737931/769966887055392768/878403180290007080


--- https://discord.com/channels/769966886598737931/788826407412170752/1107252558843613215
Návrat k tématu pár dní dozadu, neříká sice nic, co tu nepadlo, ale je to anglicky a video, takže je to určitě pravda. 😅 https://youtube.com/shorts/wyVvOiVFKqo
---


--- https://discord.com/channels/769966886598737931/1105431262702874664/1106638164682092544
Když to **hodně** zjednoduším, tak pokud ti udělá radost, že
1️⃣ přibylo pěkné tlačítko a je správně velké v mobilu i v počítači => jdi dělat frontend
2️⃣ přibyla funkčnost schovaná pod tím tlačítkem => jdi dělat backend
3️⃣ nové tlačítko nezpůsobilo pád všech serverů => jdi dělat SRE
4️⃣ to tlačítko vždy funguje => jdi dělat testera/QA
5️⃣ to tlačítko dělá, co uživatelé potřebují a chápou to => jdi dělat UX
6️⃣ to tlačítko přiměje lidi dělat něco, z čeho má firma peníze => jdi dělat product management
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1105793725608767528
Ještě sem si vzpomněl na tenhle pohled, proč může být dobré zrychlit, proč dřív hledat práci od <@797840210272190514>:
> Práce, kterou jste doteď dělali jako koníčka po večerech najednou děláte přes den a máte za ni zaplaceno. Učíte se 3x rychleji -> nové informace nasáváte jak podvědomě (protože se to na vás valí ze všech stran a chtě nechtě jste součástí), tak vědomě a cíleně (protože máte silnější potřebu a motivaci se učit, už jen pro to, abyste si tu práci udrželi).
zdroj https://discord.com/channels/769966886598737931/788826407412170752/972951035226247258
_(nepíšu to abych někoho přesvědčil, pro spoustu lidí je pomalejší cesta to pravé, jen jeden pohled navíc)_
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1105211320820838500
Ja osobne v prubehu me cesty k prvni praci presel od intenzivniho stylu uceni full time k pomalejsimu stylu. Rozvedu:

V prubehu sabbaticalu jsem zkousel ruzne cesty , kam se v kariere vydat a postupne vykrystalizoval ten hlavni cil, stat se back-end developerem. Mel jsem budget a plan , ze si udelam vlastni coding-camp a do pul roku se naucim , co bude potreba. V tu chvili je asi nejlepsi mit osnovu od nejake treti strany( napr. to co dela CoreSkill).  Ja jel na vlastni pest, coz s sebou neslo uskali, se kterymi jsem nepocital. Sice jsem si urcil nejakou osnovu podle ktere bych chtel jet, jenze jako amater, ktery nebyl v primem kontaktu s nejakym mentorem me potkavali dva hlavni problemy. Kdyz jsem objevil nejaky koncept, napriklad SQL, tak jsem chtel zjisti vic, dalsi video,clanek  idealne kurz a zabredaval jsem hloubeji a hloubeji . Takove rekruze v uceni a nekdy mi trvalo dlouho nez jsem se vratil do te nulte vrsty ,kde je ta osnova. A druhy problem: Protoze, jsem se ucil vse od nuly, tak jsem nedokazal odhadnout, co je for beginners a co ne. Takze jsem v uvodu zabil nejaky cas dekoratory apod, ktere me spis odrazovali od toho ucit se dal. A zjistil jsem ,ze casovej tlak, nauc se to do nejake doby mi brani v dulezitejsi veci, t.j pochop a vyzkousej si. A dalsi aspekt byl, ze pokud jsem byl nucenej se neco naucit a neslo mi to , ztracel jsem chut a mel jsem strach si si programovani znechutim. Protoze jsem byl presvedcenej, ze to je ta spravna cestu(stat se vyvojarem). Nechtel jsem vyhoret hned v procesu uceni, jeste nez si najdu prvni praci v IT.
---


--- https://discord.com/channels/769966886598737931/788826407412170752/859537028081123358
> **Total time spent: ~418+h**
Pro všechny vypíchnu tenhle ⬆️  údaj z https://github.com/NelliaS/development-timeline
---


--- https://discord.com/channels/769966886598737931/789107031939481641/853948221734649876
Je to pořád spíš interní tool, kterej vyžaduje vysvětlení jak fungování, tak obsahu, ale za ty prachy… (zadarmo)
https://your.coreskill.tech
Je to většinou velmi konkrétní. A taky stále nekompletní atd.
A není tam zatím žádný reaktivní framework (Vue.js/React atd.)
---


--- https://discord.com/channels/769966886598737931/769966887055392768/897087048110997584
Vystudovaná škola je irelevantní, fakt. Když pominu procesní části kyberbezpečnosti, kde je stejně dobrý vstup pro právníka, ekonoma jako informatika, tak ty technický části kyberbezpečnosti na škole nic moc neudělají. I na specializovaných školách je to pár profilujících předmětů, navíc (bohužel) ne vždycky valné kvality. Jako juniorní základ bych řekl, že pokud má člověk technické znalosti, aby dokázal přečíst a pochopit Security Engineering od Rosse Andersona https://www.cl.cam.ac.uk/~rja14/book.html (druhá edice je tam elektronicky zdarma), tak je na tom líp než průměrný absolvent oboru kyberbezpečnosti na výšce. Ta vysoká škola s tímhle zaměřením ti dá prostor se tomu věnovat, ale nic negarantuje - můžeš vyjít super nabitej, nebo taky prolézt s tím, že to na tobě nezanechá stop ani v nejmenším.
---


--- https://discord.com/channels/769966886598737931/788826407412170752/884384772669972481
Pokud kamarádka nemá žádné zkušenosti s testováním, doporučuju začít s Czechitas jednodenním *úvod do testování* - vyzkouší si prakticky, jak vypadá práce manuálního testera/ky. Dále se může podívat na zdroje kolem test stacku a Radima Pánka (http://rdpanek.cz/) - témata jsou sice  technická, ale mají i zdroje pro začátečníky v automatizovaném testování.

Pokud se rozhodne jít do toho, doporučuju si najít nějaký kurz. Jsou firmy a neziskovky, které nabízí takové kurzy. Toto bohužel neumím objektivně hodnotit, protože nemám s tím osobní zkušenosti.

Na práci manuálního testera stačí látka z ISTQB zkoušky - https://castb.org/wp-content/uploads/2020/05/ISTQB_CTFL_CZ_3_1_1-6.pdf. Na pohovorech se často ptají na teorii (otázky typu co je boundary analysis, black box versus white box testování, kdy automatizovat testy a proč a kdy neautomatizovat apod.) a také ověřují způsob, jak kandidát/ka přemýšlí - otázky typu jak otestovat žehličku/konvičku/jakýkoliv předmět. Co se ještě hodí umět je Linux a SQL - občas bude potřeba podívat se do logů, zapnout si prostředí nebo vytáhnout nějaká data z databáze. Na pohovorech, jak vím, se na to obvykle neptají, pokud se jedná čistě o manuální testování.
---


--- https://discord.com/channels/769966886598737931/797040163325870092/985220533044002877
Já jsem fanda průzkumu bojem. Zkus to a uvidíš. Jestli nevíš co, tak zkus https://blockly.games/ od začátku pěkně. Jestli tě bude bavit vyřešit i to poslední Maze například. Dej vědět.
---


--- https://discord.com/channels/769966886598737931/769966887055392768/975717126809727006
Přidám se k tomu, co píše <@668226181769986078>  1) koukni na tu přednášku. 2) zkus si manuální testování, ona je to teda, co si budem, trochu blbárna 😄 , ale je jednoduchý se k tomu dostat a stačí ti to dělat chvilku, jen klidně brigádně. Mně to třeba pomohlo jako nakouknutí do testingu obecně a hodilo se to i jako zářez do CV, když jsem se pak ucházela o QA pozici na automatizované testování.
QA jako přestupní stanice k developmentu může a nemusí fungovat. Třeba v Oracle je to úplně cajk, lidi tam z QA na devy přechází nebo mezi těmi pozicemi různě přepínají, podle zájmu. Ale je to proto, že jsou tam ty specializace takto nastavené, že se ty pozice částečně prolínají. V jiných firmách naopak tady ty lidi, co jdou na QA jenom aby mohli být brzy devové, nevidí moc rádi, protože u těch lidí je menší ochota se učit testovací nástroje a celkově je ta oblast vlastně nezajímá. Což je jasný, že takovýho pracovníka úplně nechceš. Záleží tedy právě na tom, jak která firma má ty role nastavené.
Každop. ta vstupní znalostní hranice do QA je níž než do developmentu, protože se hodně liší nástroje, jakými která  firma testing dělá, takže nikdo moc nepředpokládá, že to lidi z venku budou umět (s výjimkou seniorních pozic, když se hledá někdo, kdo to testování bude zavádět). Takže ti defacto stačí umět programovat na úrovni Advent of Code tak do 4. dne 😄
---


--- https://discord.com/channels/769966886598737931/769966887055392768/974647570636886027
Ahoj 👋 Měl jsem to ještě nedávno podobně jako ty. Všechno mě lákalo, a tak jsem skákal z jednoho na druhé, popř. jsem se učil více věcí současně. Buď mi z přemíry informací šla hlava kolem (a donutilo mě to přestat), nebo jsem se naučil trochu tohle, trochu támhleto, ale v závěru jsem nedokázal samostatně tvořit/přinášet nějakou hodnotu. Je to podobné jako s cizími jazyky. Můžeš skákat z jednoho na druhý a umět trochu třeba 10 jazyků na úrovni A1-A2. S cizincem u baru small talk dáš, ale abys mohl v jednom z těch jazyků plně fungovat třeba v práci, která je hodně o aktivním používání toho jazyka, to už je něco úplně jiného. Zjednodušeně podáno 🙂 Je dobrý zkoušet, ale mělo by se to dělat systematicky a mělo by to mít nějaké cíle/meze. Kdybych se toho držel, tak ušetřím spoustu času, energie i peněz. Mně nakonec zachraňuje staré dobré: Vymysli/najdi si větší/menší projekt -> uč se to, co k tomu potřebuješ -> piš, skládej, tvoř. Větší cíle se dají rozložit na menší, tahle série tří kroků se pak může x-krát opakovat. Můžeme dát call, když si o tom budeš chtít ještě popovídat 😉
---


--- https://discord.com/channels/769966886598737931/811910392786845737/970708351174463508
Pro JS jsem právě něco takového viděl na MDN: https://developer.mozilla.org/en-US/docs/Web/JavaScript/A_re-introduction_to_JavaScript
---


--- https://discord.com/channels/769966886598737931/769966887055392768/965701681075589160
**Frontend developer není designér**, jeho rolí není vysloveně designovat, to je role designéra (a je jich hned několik druhů).
Ale protože od designérů dostáváš jejich představy, jak má nějaký web nebo aplikace vypadat, tak je potřeba **rozumět jejich uvažování** a **umět s nimi komunikovat** jejich jazykem. Ta komunikace se často odehrává předáním návrhu, ale nejen tak.

Protože návrhy, ani případné slovní popisy, či videa nemohou 100% web popsat, je to vždy do jisté míry **interpretace a domýšlení detailů** v duchu návrhu. Pokud je designér k dispozici, dá se ho ptát, ale to často není a taky není úplně efektivní to dělat s každou „drobností“, protože pak to trvá dost dlouho.

Není ale jedna úroveň znalosti designu, liší se to podle role, firmy, produktu. Někde stačí umět hlavně programovat v JavaScriptu/TypeScriptu (React developer typicky) a někde seš napůl designer, protože dostáváš jen velmi hrubá zadání. BTW: čím víc to první, tím víc peněz, obvykle.

Cit pro design podle mne neexistuje. Ještě rovnou napíšu, že „design“ není jen jak něco vypadá, ale i to jak to funguje.
Lze se to naučit. Dokonce je potřeba se to učit, zvlášť proces navrhování.
Samozřejmě když tě taková věc zajímá a třeba v okolí vidíš, jak to někdo řeší, jak o tom přemýšlí a/nebo jsi obklopen kvalitním i tím nekvalitním designem a učíš se to vnímat, tak tím získáš ten „cit“.

Protože podklady přebíráš od designérů, kteří je tvoří v těch programech (dnes nejčastěji Figma), tak je potřeba s nimi umět trochu pracovat, aby sis byl schopen prvky přebrat.

Tady odbočím k tomu FE mentoru: to zadání vypadá spíš na JS a API než na CSS, ale ano, je tam i tahle složka. Pokud ale využiješ jen ten JPG a jimi připravené obrázky, tak to nebude v tomto směru blízko praxi. K tomu bys měl využít tu _pro_ verzi s Figmou.

Kromě vysloveně vytahování informací o návrhu se taky hodí umět pracovat s něčím, kde můžeš tvořit a upravovat různé grafické prvky, dnes je to na webu nejčastěji formát SVG pro který doporučuju naučit se trochu pracovat s programem _Inkscape_.
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1100742108870086716
Včera <@771661208007868446> hrozně pěkně mluvil o herním testování, tak jsem si vzpomněl na jeden web, jehož název mluví asi za vše. Kvalitu a kvantitu všech těch informací může posoudit někdo povolanější, ale říkal jsem si, že by se to mohlo někomu líbit/hodit. Já si tam jen něco málo četl a přišlo mi to zajímavý 🎮 https://www.gameindustrycareerguide.com/how-to-break-into-video-game-industry/
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1083076710586658866
Možná jsem to tu už sdílel, ale koukám, že můžu zopakovat
> If you have to google it then it's going to use 1 of your 4 working memory slots.
https://saveall.ai/blog/learning-is-remembering
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1063554627959791687
Toto je post od Software Engineera v google. Je to skor smerovane na juniorov a ake jazyky sa ucit podla toho comu sa chces venovat. https://www.linkedin.com/posts/demitriswan_programming-golang-go-activity-7018701749519601664-rnY1?utm_source=share&utm_medium=member_desktop
---


--- https://discord.com/channels/769966886598737931/1088577532376387705/1091349723937505321
Dokonce ty základy jako cykly, podmínky, proměnné a dokonce i funkce se můžeš naučit bez konkrétního jazyka vizuálně na https://blockly.games/ Sice po vyřešení pak ukazuje „javascriptový kód“, kterým by se to samé naprogramovalo a v pokročilejších lekcích se jde přepnout na psaní kódu, ale pořád to jde řešit těmi bloky, které na začátku zabrání chybám v syntaxi, tedy že ti někde chybí středník, tečka nebo mezera.

U těch komplexnějších věci mi pak už přijde lepší pro začátečníky opravdové programování, protože je snažší zkoumat jak ten kód funguje.
---


--- https://discord.com/channels/769966886598737931/1088577532376387705/1088957232919625728
V podstatě je ta mainstreamová volba z těchto pěti:

<:javascript:842329110293381142> **JavaScript** – na backendu (Node.js) a na webovém frontendu (+ TypeScript) – pokud chceš dělat frontend (React apod.) tak tam jiná volba není.

<:python:842331892091322389> **Python** – „druhý nejlepší jazyk na cokoliv“ (trochu bonmot, ale není to úplně blbost), píše se v něm všechno možné, desktopové programy, backendy všeho druhu (třeba webů), používá se na analýzu dat, ale na některé věci (hry, mobilní appky a další) fakt není dobrá volba

<:csharp:842666113230045224> **C#** – desktopové programy, backendy všeho druhu (třeba webů), hry (Unity), mobilní appky

<:java:1036333651740327966> **Java** – mám asi hrozně stereotypní pohled: jdeš na IT VŠ, programuješ tam hodně v Javě a pak jdeš do korporátu bouchat nějaký složitý systémy (banky, ale nejen), druhá část jsou nativní aplikace pro Android, tam ale na popularitě získává Javě blízký *Kotlin*.

<:php:842331754731274240> **PHP** – v podstatě se v něm píší jen backendy webů, mula a otloukánek webového backendu, jsou názory, že je na ústupu, ale běží na něm asi většina internetu (záleží jak to počítáš)

Můj pohled může být zkreslenej, ale aspoň něco 🙂
---


--- https://discord.com/channels/769966886598737931/1074720669939531776/1075035258044547102
Jsem samouk. Trvalo to dlouho, prvni kod jsem napsal(opsal) v roce 2020. Ale sam jsem si zvolil tuhle cestu. Bylo to pozvolne objevovani programovani a veci s nim spojenymi. Myslim, ze kdybych sel do nejake nalejvarny ala 4 mesicni bootcamp , tak vyhorim a programovani si znechutim. Jel jsem vcelku pohodovym tempem a  mel dlouhodobou vizi. Urcite se z 0 na moji uroven da dostat mnohem rychleji.  A dost  mozna se da prace ziskat i s mensima znalostma. Ja si opravdu pockal a  az na konci lonskeho roku jsem si rekl, ze chci hledat praci, protoze jako samouk jsem mel pocit, ze se posouvam moc pomalu. Nakopl me k tomu pohovor od attacamy.
Kurzy a cestu mam trosku vic v <#788823881024405544> https://discord.com/channels/769966886598737931/788823881024405544/1048280508985000047
---


--- https://discord.com/channels/769966886598737931/1049284297133133854/1050733829196873779
pořadí důležitosti je:
1) rozumět čtené (návody, kurzy, dokumentace, čtení řešení někde na Stackoverflow)
2) umět správně anglicky pojmenovat proměnné a funkce atd.
3) umět se písemně zeptat na problém
4) umět napsat dokumentaci
5) rozumět mluvené (typicky nějaká videa, přednášky apod., tam jdou ale často zapnout titulky, co pomůžou) případně kolegům
6) ta aktivní mluvená, to už jsem psal nahoře
---


--- https://discord.com/channels/769966886598737931/1048500617657712670/1049227809396109312
Můj osobní pohled na závěr:
Pokud si chcete najít co nejrychleji práci na pozici Datový analytik, tak Excel a SQL vám k tomu pomůže nejvíce. Navíc Excel a SQL vás dobře připraví i na ten Python. V Excelu se setkáte s jazykem VBA a učení Pythonu pro vás bude poté jednodušší. SQL vás zase dobře připraví na knihovnu Pandas, kde budete používat groupby, joiny atd..
---


--- https://discord.com/channels/769966886598737931/1029701809809399918/1029723001773633577
Ahoj Terezo, přeji ti hodně štěstí a síly se studiem! 💪 Souhlas s <@652142810291765248> "osmihodinovky" neřeš, spíš si najdi nějaký svůj rytmus a toho se drž. Zkus si den rozdělit na bloky třeba po 2 hodinách a podle toho si i věci plánovat. Vyplatí se ti to ve dnech kdy budeš "dole", nebudeš tomu rozumět, nebudeš schopná přijít na to proč se děje tohle a proč se neděje tohle, budeš unavená, budeš nemocná... Budeš tam pak mít mnohem více prostoru na odpočinek, odstup atd.
Zde jen  pár rad, které jsem za ty 2,5 roku učení se pochytil a aplikuji:
1) Udělej si plán! Nejdřív na celý rok, potom na čtvrtletí, potom na měsíce... Vidím, že chceš začít pracovat na začátku příštího roku, ale i tak je dobré mít naplánovanou i nějakou variantu B.
2) Naplánuj si každý den předem. Kolik chceš projít materiálu, jaké video vidět, o jakém tématu si přečíst... nebudeš pak muset ráno vše vymýšlet a ztrácet čas a motivaci.
3) Choď spát brzy a vstávej brzy... Uvidíš, že se ti začne líbit ten pocit, že je teprve 9 hodin ráno, ale ty už jsi toho tolik stihla. Navíc ráno máš nejvíc energie, tak ji dávej do toho nejdůležitějšího.
4) Nauč se pracovat s Pomodoro systémem. Dvouhodinový cyklus, 4x 25 minut práce + 5 minut na protažení, pití...
5) Piš si deník, sdílej svůj progres nebo jakkoli jinak dokumentuj svou cestu... To je především pro tvou psychiku. Je pěkné se ohlédnout zpět a vidět za sebou kus práce, i když není na první pohled vidět.
6) NEPOROVNÁVEJ SE!!! Nesmírně důležité. Nikdo na planetě nemá stejné podmínky jako ty. Někdo má více času, někdo má méně peněz, někdo je houževnatější... nemá cenu se porovnávat s kýmkoli jiným než jsi ty sama!
7) Pořiď si polohovatelný stůl, u kterého můžeš stát, sportuj a cvič, a dodržuj Pomodoro. Pokud jsi byla zvyklá většinu času v práci stát, a předpokládám, že jako ošetřovatelka jsi byla zvyklá, tak pro tebe několikahodinové sezení bude peklo!
---


--- https://discord.com/channels/769966886598737931/1007330330149126274/1007575709029519400
Díky za odpověď Verčo 😊  v první řadě k tobě budu upřímný. Jestli se chceš naučit Python jen proto, že je jednoduchý, tak to nedělej! Věř mi, já to měl úplně stejné. Myslel jsem si, že jen proto, že ten jazyk je jednoduchý tak se ho naučím a pak už to všechno půjde samo. Obrovská chyba! Taky jsem na to dost doplatil... nic hrozného, ale srážka s realitou přišla 😁
☝ Jestli můžu, tak bych ti poradil následující:
Zkus se nejdřív zamyslet nad tím, co bys jako programátorka ráda dělala. Tzn. chtěla bys dělat webové stránky? Nebo třeba mobilní aplikace? Nebo by tě víc bavila práce s daty? Chtěla by ses spíš zaměřit na práci s vizuální stránkou programu(frontend) nebo na to jak to všechno pracuje "za oponou" (backend - tady je třeba právě Python)? Nebo klidně obojí (fullstack)? Je toho dost a dost. Zkus si nejdřív projít jednotlivé pozice a podívej se co je k nim potřeba umět. Podle toho i uvidíš co by se ti víc mohlo líbit a pak se na to i zaměříš. 😉  Pokud si nebudeš jistá, CodeAcademy má takový jednoduchý kvízek, který by ti mohl pomoci s nasměrováním (nebrat závazně) https://www.codecademy.com/explore/sorting-quiz
Píšu to proto, že Python je rozhodně jednoduchý na naučení a za mě je to skvělý nástroj na pochopení základních principů programování, ale například na frontend, kterému se teď věnuji já, je ze začátku úplně k ničemu. 😁
---


--- https://discord.com/channels/769966886598737931/1005045233614082168/1005045236424261652
Ahoj, mám takový problém… Učím se Javu/Spigot z YT, ale je to takovéto: Opis a rozumíš, ale nedokazes sám použit… Nemá prosím někdo nějakou metodu? Díky moc 🙂🙂
---


--- https://discord.com/channels/769966886598737931/882896792377765898/882939982556311552
před časem jsem se zavázal, že to sepíšu nějak strukturovaně - a bohužel jsem to jen rozepsal, ale chybí mi tam ještě nějaké praktické příklady

draft je tutaj: https://gist.github.com/kokes/49ca2f42edf30d6a1f02e3859ad3f9f2
---


---
Stalubo@ v mailu:
3. "PRŮBĚŽNÉ ZAPOMÍNÁNÍ" - i když se učíte denně, tak než se nachytříte jedno, tak to druhé pomalu začnete zapomínat. Protože to nepoužíváte. A nepoužíváte, protože čas není nafukovací a vy ho věnujete novému tématu. Navíc, to že se to člověk naučil, není nijak odměněno. Naučíte se, udělate test anebo si jenom odškrtnete a zatleskáte, ale za měsíc už si z toho pamatujete sotva polovinu. A to máte za sebou jen HTML, CSS a 40% SQL a čeká vás Python a GIt-Github.
; Člověk by už potřeboval dostávat malé "honorované" úkoly, aby získával jistotu, že to není jen učení do šuplíku. Kde netvoří žádné hodnoty. Něco, co by za ním zůstávalo. Když se necháte zaměstnat na part-time do Alberta k pokladně, tak je to sice "málo duchaplná práce", ale někdo vám za ni zaplatí. Když se učíte IT, tak "duchaplná práce", ale nevíte, jestli vám někdo někdy za ni bude ochoten zaplatit (jestli vydržíte, aby jste dosáhl toho stádia).

4. "PŮL NA PŮL" - shledávám velice obtížně rozdělit den na polovinu, kdy se učím a polovinu, kdy dělám jiné povinnosti. Vždy to sklouzne k tomu, že buď dělám celý den jedno anebo celý den druhé. Když se do něčeho zakoncentruju, tak se mi to už žádá dokončit a nikdy se mi to nepovede v tom původně naplánovaném 4 hodinovém čase.
A najednou zjistíte, že jste 2 dny nenapsal ani čárku kódu.
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1123350431255515287
Sice pro tvůrce, ale jsou tam dobré tipy vlastně pro kohokoliv, kdo se učí něco nového 🧑‍🎓 „Bez toho, abyste si na zahrádce ušpinili ruce nikdy nic nevypěstujete!“ https://overcast.fm/+9-bVhiVy8
---


--- https://discord.com/channels/769966886598737931/1150824903000465564/1150824903000465564
Ahoj, byl jsem požádán o recenzi... <:PauseChamp:1002659089664442401>

Tak jsem se rozhodl, že ok dám to.
Už tři roky mám PRO účet na SOLOLEARN.
Ano platím si to.
Myslel jsem, že se jedná o aplikaci na procvičování, ale reálně se jedná o výukovou platformu.

Jazyky nejsou v celém rozsahu, ale je tam HTML, Python, C++, JavaScript, SQL...

SOLOLEARN je teda jako appka a je to i na web.

Jde trochu gamifikace ve formě sbírání achievmentu, ale za splnění kurzů je možno získat certifikát.

Kurzy jsou rozděleny do úrovní a ty pak na kapitoly a kapitoly na jednotlivé funkce.

Každý kurz má teoretickou část, pak kvízovou část a taky i testovou část a hlavně je super praktická část ta má dvě úrovně free a PRO.

V každé praktické části a i každá otázka a kvíz má kolonku komentáře od lidí - najdete nápovědy a taky řešení, ale doporučuji se tomu vyhnout.

Pak praktické části kurzu v PRO verzi od cca 6 měsíce tohoto roku nabízejí využití AI při řešení úkolu -> je možnost si nechat vysvětlit kód, nechat si poslat řadu, zkontrolovat kde mám chybu a nebo vymýšlet komplet řešení.

Hodně cool funkce.
Nicméně každý splněný úkol a kapitola dává expy které se pak počítají do leaderboardu - možnost soutěžit s ostatními dle země, skupiny, apod...

Celé to prodražilo letos a stojí to na jeden rok 1700,- což ale v tom množství úkolů vychází slušně.

Profil dovoluje ukládat své varianty kódu - každý kurz totiža svůj kompilátor a každý kód lze uložit pro pozdější prohlídnutí, je tam i možnost s ostatními sdílet nápady (trochu spam a bordel) a taky možnost fóra, ale to není tak záživné číst.

Nevýhodou SOLOLEARN ke že na mobilu se to chová jinak než na webu v PC, ale to se dá čekat.

No každopádně pro začátečníky a pro lidi co se chtějí i přiučit angličtině tak dávám doporučení.

No pokud jsem na něco zapomněl tak napište a já zodpovím.

Díky, co dočetli tu hrůzu až sem.
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1206229649546543174
O učení: https://twitter.com/karpathy/status/1756380066580455557#m
---


--- https://discord.com/channels/769966886598737931/811910782664704040/1212103644778856568
MDN spustilo vlastní vzdělávací materiály https://developer.mozilla.org/en-US/curriculum/
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1210520377952829440
> You can ask stupid questions of ChatGPT anytime you like and it can help guide you through to the right answer.
>
> ...
>
> I've had real life teaching assistants who super smart, really great, help you with a bunch of things and on a few things they're stubbornly wrong.
>
> If you want to get good at learning, one of the things you have to do is you have to be able to consult multiple sources and have a sort of sceptical eye.
>
> Be aware that there is no teacher on earth who knows everything and never makes any mistakes.
https://simonwillison.net/2024/Jan/17/oxide-and-friends/#llms-for-learning
---


--- https://discord.com/channels/769966886598737931/788832177135026197/894840146845925427
https://www.codecademy.com/resources/docs

Blog post k tomu https://www.codecademy.com/resources/blog/introducing-docs/

Samozřejmě jsou jiné existující zdroje, ale tady je to hodně stručně, takže to začátečníci asi ocení.
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1055146186413187102
Doufal jsem, že sem taky budu moct jednou napsat, že jsem konečně v klubu a našel jsem práci. A stalo se to ! Od února se budu podílet na softwaru v automobilech v Pythonu. 🤩

Od začátku utekly dva roky, kolik jsem oslovil firem přesně nevím, ale mohlo to být kolem dvaceti. Hlavně bych ale chtěl říct, že na začátku není důležité někam spěchat - což se mi také stalo. Pak jsem si uvědomil, že stihnout to za pár měsíců souběžně s prací a rodinou je blbost. A tak jsem v klidnějším tempu pokračoval k cíli.

Pár slov a odkazů k cestě, na začátku za mě nejlepší start na https://www.umimeinformatiku.cz/programovani-v-pythonu , to mi pomohlo nejvíc a je to hlavně zábavnou formou příkladů. Pak jsem si vybral projekt od https://www.techwithtim.net/ , který má super tutorialy na Youtube a zakončil jsem to projektem s Corey Schafer také na Youtube, nicméně ty už jsou pro pokročilejší.

U pohovoru také dost pomohl GitHub, který doporučuji si založit hned první den. Jednak mě motivoval ten kalendář příspěvků udělat něco pokud možno alespoň každý druhý den. A poté je vidět jak dlouho už se člověk tématem zabývá. 🙂

Hodně zdaru, sil a velký dík Honzovi, že to tu založil a spravuje <:dk:842727526736068609> 🥳
---


--- https://discord.com/channels/769966886598737931/1217738430713430080/1217767457964429313
Za mě je dobré vyzkoušet si to. Věnovat třeba 10 hodin čistého času tomu, začít s každou specializací, abys viděl prakticky, co to znamená.
Tedy opravdu začít nějakej kurzík a to nejlépe něco, kde to budeš sám dělat, ne se jen koukat na YT, jak to někdo dělá.
A taky si třeba zkusit o té specializaci něco vyhledat, případně se zeptat tady.

Ty základní směry jsou zhruba tyto
- testing
- backend (a devops), jazyků celá řada
- frontend (HTML, CSS, JS)
- mobilní aplikace (kde ale už dominují frontendové technologie)
- data (datová analýza, engineering atd.)
- cybersecurity (bezpečnost)
---


--- https://discord.com/channels/769966886598737931/1217738430713430080/1217771487792992347
# Plán
Máš v podstatě tady https://junior.guru/handbook/

První si vyzkoušej, co tě nejvíc láká, kde si umíš představit, že bys chtěl skončit a až si budeš myslet, že to víš, tak se do toho zakousni. Pořád bych radši začal s online kurzy zdarma/levně než bych se pustil do něčeho většího.

Je to mentálně hodně náročné, takže i když lidi nemají nic jiného na práci, tak obvykle nedají víc než 18–22 hodin týdně čistého času se tomu věnovat. To je fulltime. Krátkodobě jde samozřejmě víc, ale protože potřebuješ cca 400–600 hodin, aby ses dostal na úroveň, kdy má smysl hledat práci, tak je potřeba to vydržet měsíce a nepřepálit start.
---


--- https://discord.com/channels/769966886598737931/797040163325870092/1221400946928652339
OK, tak možná ať si zkusí projet tohle https://blockly.games/?lang=en používáme to i s dospělými, co nikdy neprogramovali, aby si rozvičili mozky tím správným směrem, než začnou psát kód (i když trochu kódu se píše i tam ke konci) (a třeba malování želvou mě jednou chytlo tak, že jsem u toho seděl pár hodin 😅)
---


--- https://discord.com/channels/769966886598737931/797040163325870092/1221394579811471391
To hodně záleží, co by přesně ráda dělala. V zásadě jsou 2 možnosti pro "programování her" - tvořit engine, kde se pak vše vykresluje (extrémně náročné na výkon, spousta matematiky a optimalizací), nebo řešit scriptování her (jak se třeba chovají postavy, jak reaguje prostředí atd.).

Jsou to 2 dost odlišné věci, kdy ta první vyžaduje typicky precizní znalost algoritmů, matematiky a nízkoúrovňových jazyků (C / C++).
Ta druhá je naopak nějaký scriptovací jazyk a k tomu (dnes už) grafické rozhraní na spojování tzv. nodes. Tam se hodí spíš jazyky typu Lua, JavaScript, případně C#.

Doporučím se podívat na **Nauč mě IT** 🧠 přednášku o hrách (byť zaměřeno na 3D tvorbu charakterů).
https://youtu.be/LTBGnZun8dc

Kdyby pak byl zájem dál, můžu propojit s přednášejícím a ten by určitě věděl, na jakého programátora se obrátit, aby dal bližší informace.
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1271768679297843230
Dneska jsem narazila na skvělý článek o učení se:
> When I talk to software developers today, the situation is always the same: high anxiety and imposter syndrome with a touch of depression. They feel lost and confused about what to learn and to what degree to learn it. The overt bombardment of “You are not good enough to be a real software developer” comes at them from every angle. Training courses, conferences, articles, tweets, and peer pressure reinforces their fear that what they know is not good enough. The fear of missing out hits our colleagues who are self-taught or fresh out of code school the hardest. The industry makes them feel inadequate and worthless, all for the sake of pushing the thinly veiled agenda of “Learn our technologies so that people know we’re the best tech company.”
https://neilonsoftware.com/articles/how-to-keep-up-to-date-with-technologies-as-a-software-developer/
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1325501165542178936
Zajímavý článek:

- pozor na dopamin,
- pozor na motivační videa a vzory, které měly úplně jinou cestu než vy,
- pozor na „action faking“ (tady často říkáme „tutorial hell“),
- pozor na zanedbávání sebe a osobního života na úkor „musím bušit víc“,
- pozor na příliš megalomanské cíle,
- pozor na dělání věcí jen proto, abyste se zalíbili ostatním,
- pozor na to být hlavou pořád jen v budoucnosti na úkor přítomného momentu.

https://vesecky-adam.medium.com/major-pitfalls-of-self-development-50c470ee0bf2
---


--- https://discord.com/channels/769966886598737931/1410161605232033832/1410161605232033832
Ahojte, jdu si pro radu nebo spíš pro tipy jak se efektivně učit v dnešní době.

Zajímalo by mě jak se učíte novou technologii nebo cokoliv jiného, máte nějakou osvědčenou metodu nebo prostě si to jen tak zkoušíte ?

• **Máte nějakou placenou platformu, která vám udává nějakou pevnou osnovu?** (Boot.dev, codecademy, Hyperskill…)

• **Nebo používáte chatbota jako mentora?** (ChatGPT, Claude…), popřípadě platíte si Pro verzi?

• **Píšete si poznámky?** - mě tohle asi nikdy nefungovalo, nikdy se k ním nevracím, tak si spíš píšu komentáře přímo do kódu.

• **Projektíky, větší projekty** - Asi se všichni shodneme, že nejlepší co můžeme udělat, je něco tvořit, ale někdy je to těžké uchopit a začít.

Já mám s tímto problém jak to celé uchopit a nastavit si nějaký studijní plán, který bude efektivní a k něčemu, jsem v tomto trochu autista a potřebuju to mít všechno pěkně rozepsané a nachystané a sledovat svůj pokrok. Chci ty koncepty umět, znát a rozumět tomu. Dnes koukám na videa, kde týpci ukazují jak se učit a že ti stačí AI, v podstatě kopíruji kód do IDE a to prokládají za učení se…tohle nechci, tím se nic nenaučím (alespoň já).

Jak to máte vy? Děkuju moc 🙏🏻
---


--- https://discord.com/channels/769966886598737931/788832177135026197/1415258347069902868
Jak se učit https://www.youtube.com/shorts/uU-1T3qKSBA
---


#} -->
