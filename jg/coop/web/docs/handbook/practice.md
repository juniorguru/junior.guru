---
title: Jak procvičovat programování
emoji: 🏋️
stages: [learning, creating]
description: Znáš základy, ale na větší projekt si ještě netroufáš? Procvičuj programování na malých úkolech a rozšiřuj si znalosti
template: main_handbook.html
---

{% from 'macros.html' import lead, link_card with context %}


# Jak procvičovat a rozšiřovat si znalosti

{% call lead() %}
  Dokážeš napsat pár řádků kódu, ale na větší projekt si ještě netroufáš?
  Pomůže ti procvičování a postupné posouvání znalostí řešením malých úkolů.
{% endcall %}

## Procvičuj

<div class="link-cards">
  {{ link_card(
    'Exercism',
    'https://exercism.io/',
    'Řeš malé úlohy, dostaň zpětnou vazbu od mentora, uč se z řešení druhých.'
  ) }}

  {{ link_card(
    'Codewars',
    'https://www.codewars.com/',
    'Řeš malé úlohy přímo v prohlížeči, uč se z řešení druhých.'
  ) }}

  {{ link_card(
    'CheckiO',
    'https://checkio.org/',
    'Procházej online hru pomocí programovacích úloh, uč se od druhých.'
  ) }}

  {% call link_card(
    'Umíme informatiku',
    'https://www.umimeinformatiku.cz',
  ) -%}
    Uč se skrze cvičení a opakování. [Podloženo výzkumem](https://www.umimeto.org/podlozeno-vyzkumem).
  {%- endcall %}

  {{ link_card(
    'HackerRank',
    'https://www.hackerrank.com',
    'Soutěž řešením zapeklitých úloh. Propojeno s nabídkami práce.'
  ) }}

  {{ link_card(
    'Project Euler',
    'https://projecteuler.net/',
    'Řeš matematické úlohy pomocí programování.',
    badge_icon='calculator',
    badge_text='Pro matematiky',
  ) }}
</div>


## Rozšiřuj si znalosti    <span id="skills"></span>

Umět programovat např. v Pythonu je dobrý základ, ale pro plnohodnotnou práci to nestačí. S prvními pokusy se uplatnit zjistíš, že by se ti hodilo aspoň trochu znát Git, HTML, SQL, JavaScript, … Pro každou takovou technologii existují kurzy, workshopy, knihy.

Vždy, když narazíš na nový pojem nebo zkratku, přečti si alespoň co to je a k čemu se to používá. Pokud o tom uslyšíš poněkolikáté, zkus si najít víc a pochopit základy.

### Základy    <span id="basics"></span>

<div class="link-cards">
  {{ link_card(
    'BaseCS',
    'https://medium.com/basecs',
    'Základy informatiky od <a href="https://twitter.com/vaidehijoshi">Vaidehi Joshi</a>.
        Existuje i jako
        <a href="https://dev.to/vaidehijoshi/linked-lists--basecs-video-series--2le8">video</a>
        a
        <a href="https://www.codenewbie.org/basecs">podcast</a>.'
  ) }}

  {{ link_card(
    'MIT: The Missing Semester',
    'https://missing.csail.mit.edu/',
    'Úvod do všeho možného, co se ti bude v začátku hodit. Příkazová řádka, Git, editor…'
  ) }}
</div>


<!-- {#

Lenertova doporucuje:
https://app.finxter.com/learn/computer/science/

ChatGPT
https://www.linkedin.com/posts/marketa-willis_junior%C5%AFm-bych-nedoporu%C4%8Dila-pou%C5%BE%C3%ADvat-chatgpt-activity-7176515147228663808-pODd?utm_source=share&utm_medium=member_desktop

— Zvládnout psané návody a zdroje v angličtině. Bez ní se v IT funguje jen velmi těžko. Není potřeba mluvit, psát vysloveně bez chyb apod. většinu toho stejně ani nepíšou rodilí mluvčí. Ale přečíst si nějaký text a vědět o čem je, třeba: _By default, browsers separate paragraphs with a single blank line. Alternate separation methods, such as first-line indentation, can be achieved with CSS._ je skoro nutnost. Měl jsem klientku, která si hodně pomáhala automatickým překladačem a nějak to zvládla ale ideálně bys na angličtině měl zároveň pracovat, aby sis ji zlepšil. Za půl roku můžeš mít viditelné pokroky a rozhodně se ti to neztratí.
A to, že je alespoň nějaká angličtina v podstatě nutnost vědí i ve firmách. Takže když tam pošleš CV s tím, že umíš velmi málo, tak už si tím snižuješ šance i kdyby ta firma byla plná lidí, kteří mluví česky. Protože i v takové firmě je většinou zvykem psát třeba komentáře a další texty okolo kódu v angličtině.

algoritmy http://jeffe.cs.illinois.edu/teaching/algorithms/

https://www.manning.com/books/grokking-algorithms

DOM events https://domevents.dev/

assumptions, predpoklady - https://medium.com/@peter.hozak/krkolomn%C3%A9-predpoklady-6f658f552de4

Hafo se řeší jak odinstalovat Linux k Windows

teoreticka informatika - https://bigmachine.io/products/the-imposters-handbook/ a https://en.wikipedia.org/wiki/The_Pragmatic_Programmer

network programming https://beej.us/guide/bgnet/html/

MARKDOWN JAK FUNGUJE, ANALOGIE
Je to jako když jsi autor knihy a píšeš článek na psacím stroji - když chceš někde udělat nadpis, použiješ k tomu # apod. nebo to podtrhnes, když chceš udělat caru, tak uděláš spoustu - za sebou. Pak ten papír das vydavateli a tam to vezme sazeč a udělá z toho pěknou barevnou knihu. Tak Markdown je ten psací stroj a sazec je jakýkoliv program, který bere MD (strojopis) a produkuje HTML (barevnou knihu)
Jako autor mas na barvu obálky a font nadpisu v knize minimální nebo zcela žádný vliv
Ale můžeš dat sazeči vědět, kde je nadpis a kde je seznam

https://12factor.net/

https://www.freecodecamp.org/news/what-is-web-development-how-to-become-a-web-developer-career-path/

Learn learn learn loop
https://twitter.com/OzolinsJanis/status/1420344259367030784

koľko HODÍN DENNE musím PROGRAMOVAŤ? (programátor radí) https://www.youtube.com/watch?app=desktop&v=LG-d_BOZE6k

https://www.facebook.com/groups/pyonieri/posts/5247478988597569/?comment_id=5249157481763053&reply_comment_id=5249165655095569
Teď měj radost, že jsi to nakonec vyřešil 💪 Netrap se tím, že to bylo obtížné. To znamená, že ses u toho hodně naučil. Pokud je to tvůj první pokus aplikovat naučené znalosti na praktickém projektu, není divu, že to šlo obtížně, protože tohle, to přemýšlení kolem toho, rozsekávání problému na podproblémy, debugování, apod., tohle je na celém tom programování to ono, co je největší skok od laika a sledovače tutoriálů k člověku, který dokáže něco reálně naprogramovat.
Mnoho lidí jen točí tutoriály a diví se, že pak nic nedokážou vytvořit. Ty už jsi dál! 🙂
A neboj, už třeba za měsíc se na ten svůj teď těžce vydřený kód budeš dívat a zasměješ se mu.


univerzální technologie, které potřebuješ všude https://twitter.com/vboykis/status/1451985733867216898

https://exercism.org/tracks/python/concepts
https://www.codecademy.com/code-challenges

nandtetris https://www.nand2tetris.org/

https://ivet1987.wz.cz/2020/03/koucovani-na-pyladies-kurzech/

https://regexcrossword.com/
https://refrf.dev/

UX - https://www.designui.cz/hledame-designera
UX http://www.asociaceux.cz/zacinate-s-user-experience

challenge https://www.trywilco.com/

fyzika, animace v javascriptu - https://thecodingtrain.com/, https://natureofcode.com/

matika pro vyvojare https://youtu.be/bOCHTHkBoAs

zaklady bezpecnosti - odkazy na dobre veci jsou na poslednim slajdu kayly prednasky pro klub

data science - My "data science is different now" post has Data Reddit asking questions already answered by my post.
https://twitter.com/vboykis/status/1419302245854818306

https://nemil.com/categories/notes-to-a-young-software-engineer/

- Tereza podcast skvela citace na vliv a výhody komunit
- https://www.pythonistacafe.com/

https://www.mjt.me.uk/posts/falsehoods-programmers-believe-about-addresses/

testování - Pánek má spoustu materiálů k automatizaci: https://www.youtube.com/watch?v=OnpOwlp8Hrg&list=PLZaZq-LUymhx3Lip30OGmsMPdAVoNl45i&index=5

Tak mě napadá, jestli by zdejší mozkový trust nedokázal dát dohromady typická spojení obor + programovací jazyk. Ve smyslu v jakém jazyce se nejčastěji programuje v konkrétních oborech. To by bylo další ze skvelých vodítek pro switchery, když se rozhodují, do jakého jazyka se pustit.
Už jsem tady ten hypreskill.org (od JetBrains) dával víckrát, mám pocit, že to tam celkem mají. Je nutno si kliknout na *open original*, je to dost velkej screenshot…  (rozbalil jsem na ukázku OOP)

Zkus hyperskill.org od JetBrains. Jsou tam algoritmy, matika, obecny veci (kamarad s nedostudovanym matfyzem a dostudovanym Bc. na CVUT FIT rikal, ze mu prijde, ze je tam toho az az co se tyka tech algoritmu a matiky, takze bych se netyral se vsim, ja to bohuzel neposoudim, sem v tomhle pastevec). A myslim, ze by mohl byt nejakej trial mesicni nebo tak neco, abys videl, ze to stoji za to nebo ne.

Zmínit Sifrovacky jako způsob jak si s tím hrát ve volném case

Complete Introduction to the 30 Most Essential Data Structures & Algorithms - DEV
https://dev.to/iuliagroza/complete-introduction-to-the-30-most-essential-data-structures-algorithms-43kd

https://dr-knz.net/programming-levels.html
CEFR https://www.linkedin.com/feed/update/urn:li:activity:6832917085660725248/?commentUrn=urn%3Ali%3Acomment%3A(activity%3A6832917085660725248%2C6832968938511458304)
CEFR Radek Holý
Už se to potřetí snažím přečíst celý, ale nemám na to morál. Nicméně ty kusy, co jsem viděl, vypadaj super. Moc se mi to líbí.
Jen mám pocit, že tam chybí totéž, co řešíme i u nás ve firmě. Soft skills. Jo, je to takový zaklínadlo, ale ukazuje se, že tak nějak podvědomě člověk bere v potaz při povyšování i tuhle stránku. Hlavně co se týče týmové spolupráce a komunikace s klientem/businessem. To v té tabulce zohledněné nevidím.

https://naucse.python.cz/2020/linux-admin/
https://www.edx.org/course/fundamentals-of-red-hat-enterprise-linux

Toto je na procvičení úplně nej: https://ksi.fi.muni.cz/ a nejlepší Python videa má na YouTube Corey Schafer.

https://wizardzines.com/comics/

Prozkoumat tohleto od Radka - https://www.codingame.com/start

https://codingcompetitions.withgoogle.com/codejam
https://adventofcode.com

testování - co to je https://www.youtube.com/watch?v=LQcKWKJ68ps
testování jak na to - https://discord.com/channels/769966886598737931/788826407412170752/884384772669972481

jak na security https://discord.com/channels/769966886598737931/769966887055392768/897087048110997584

8-Bits of Advice for New Programmers (The stuff they don't teach you in school!) https://www.youtube.com/watch?v=vVRCJ52g5m4

Objektove programovani v pythone https://www.youtube.com/playlist?list=PLITREQqtwnOkN5VZv-pD3vm7eBDp7zVcn

Data a social justice https://ehmatthes.github.io/pcc_2e/challenges/coding_for_social_justice/
samizdat

https://wiki.provyvojare.cz/

I am of the opinion that every developer needs to have a solid foundation in computer science/IT
to be successful. If you're a bootcamp or self taught developer, take the time to learn CS concepts like how CPUs,OSes, memory, filesystems, & networks  work, you'll be better for it
https://twitter.com/terrameijar/status/1309999684413521921

PETR A ALGORITMY
- Jak by sis to vlastne teda konkretne predstavoval? Kdyz potkam nekoho, kdo by chtel o algoritmech neco vedet, mam ho poslat za tebou s tim, ze chces vytvorit materialy na toto tema nebo ze je to naucis?
- Můžeš, nebo jen dej vědět že je zájem. Od juniorů nebo i z druhé strany – kdyby si někdo stěžoval že to junioři z JG neumí.

Skills
https://github.com/juniorguru/junior.guru/issues/3

SQL
Především toto: http://sqlzoo.net a případně http://www.w3schools.com/sql/trysql.asp?filename=trysql_select_all
https://mail.google.com/mail/u/0/#inbox/FMfcgxwDrlfqmHRzCLJsKHHFDHbbwrJF

design systems
https://adele.uxpin.com/
http://styleguides.io/

The Most Important Non-Programming Skills for Programmers
https://welearncode.com/most-important-nonprogramming/

proč třídy
https://www.reddit.com/r/learnpython/comments/f0ir0x/i_have_a_demon_i_consider_myself_a_decent_python/?utm_source=share&utm_medium=ios_app&utm_name=iossmf

pridat neco o data analyticich? https://veekaybee.github.io/2019/02/13/data-science-is-different/

linux kernel https://linux-kernel-labs.github.io/refs/heads/master/index.html

Máme selektuju.cz a jakpsatsql.cz ale je to zatím stavěný na snowflake s predpripravenyma datama a dost punkový. Asi by tam šel přidat návod, jak data v trialce naimportovat.
https://github.com/czechitas/da-data-jakpsatsql

CZECH TESTERS GROUP (Prague, Czech Republic)
https://www.meetup.com/ProfessionalTesting/

https://regex101.com/

API - Frontend backend apis https://discord.com/channels/769966886598737931/788826407412170752/916448465817600001

JAK SE NAUČIT JINÝ JAZYK - CELÁ NOVÁ STRÁNKA
přidávám cheat sheet, který porovnává syntaxy pythonu a JS, což člověku dá rychlý náhled jak něco napsat v JS (nebo obráceně). https://github.com/LambdaSchool/CS-Wiki/wiki/Javascript-Python-cheatsheet a https://sayazamurai.github.io/python-vs-javascript/
learn x in x minutes https://twitter.com/nbashaw/status/1187779382628081664

Data science playground https://www.kaggle.com/

Knihy https://learntocodewith.me/posts/programming-books/

JAK SI VYBRAT JAZYK
Ptáš se, jaké auto je nejlepší na to, aby ses naučil řídit. Odpověď je, že nejlepší je jakékoliv, které můžeš zkoušet řídit a nejlépe takové, ve kterém ti to půjde dobře a bude tě to bavit.
Odpověď je, že je jedno, jaký programovací jazyk si vybereš, pokud tě bude bavit a pokud tě napadá, co si v něm pro sebe vytvoříš jako první projekt. Klidně PHP nebo HTML, pokud to má být webovka, klidně C#, pokud hra, je to jedno. Jestliže vůbec nevíš, tak si vyber Python, protože je to dobrá univerzální první volba, dobře se učí a používá se v mnoha oborech, takže si můžeš vybrat později, kdy už tomu budeš lépe rozumět.
Ptáš se, jaké auto je nejlepší na to, aby ses stal profi řidičem. Jenže profi řidičů je spousta druhů a my nevíme, co budeš chtít potom dělat. Řídit autobus (MHD řidič), kamion (mezinárodní dopravce), motorku (kurýr), limuzínu (řidič a bodyguard v jednom 　 )? Každé z toho bude vyžadovat trochu jinou praxi.
Odpověď je, že každý jazyk se hodí na něco trochu jiného. Pokud jsi si jistý, že chceš profesionálně programovat mobilní aplikace, asi nemá smysl ti doporučovat něco jiného, než Kotlin (Android) nebo Swift (iOS). Pokud si ničím tak úplně jistý nejsi, tak si vyber Python, protože je to dobrá univerzální volba, používá se v praxi v mnoha oborech, takže se i pouze s ním (dokonce bez znalosti HTML a dalších) lze uplatnit a najít si svou první práci. Každý další programovací jazyk pro tebe už bude snazší se naučit, takže pokud nevíš, moc to neřeš, v budoucnu se snadno cokoliv doučíš nebo přeučíš, až vědět budeš.
Víc o tom píšu tady: https://junior.guru/learn/

https://www.learnpython.org/
https://github.com/ronreiter/interactive-tutorials

Nauč sa matiku
https://www.elea.sk/
Elea je historicky prvý projekt s matematickými výukovými videami v SR a ČR. Nájdete tu kvalitné a zrozumiteľné materiály úplne zdarma.

My Favorite Free Resources for New Programmers
https://welearncode.com/favorite-free-resources/

The OSSU curriculum is a complete education in computer science using online materials. It's not merely for career training or professional development. It's for those who want a proper, well-rounded grounding in concepts fundamental to all computing disciplines, and for those who have the discipline, will, and (most importantly!) good habits to obtain this education largely on their own, but with support from a worldwide community of fellow learners.
https://github.com/ossu/computer-science

Podobný cíl jako OSSU má i "Teach Yourself Computer Science". Slovy autorů: "You don’t need yet another “200+ Free Online Courses” listicle. You need answers to these questions: Which subjects should you learn, and why? What is the best book or video lecture series for each subject? This guide is our attempt to definitively answer these questions." https://teachyourselfcs.com/

Parádní příspěvek o algoritmech
https://discord.com/channels/769966886598737931/769966887055392768/906583738140467271

Unity
Za uložení na později stojí i Brackeys na YT. Kanál narvanej úplně vším co tě okolo tvorby her v Unity napadne. K prasknutí. Má pak i discord komunitu, početnou a aktivní. https://www.youtube.com/c/Brackeys

Morsels exercise
https://twitter.com/obiskywalker/status/1278665773523898368

Kateřina Shine Churanová Kniha Fluent Python od O'Reilly. Asi nejlíp zpracovaná učebnice Python pro pokročilé.

sítě
https://www.libordos.eu/Prednasky/

If you want to start learning Python programming with a focus on data analysis (for journalism) this is the best starter course I've ever encountered https://t.co/jkmx3tjAM3— Simon Willison (@simonw) March 21, 2020
https://twitter.com/simonw/status/1241403850788982784

This is a series of books diving deep into the core mechanisms of the JavaScript language. This is the second edition of the book series:
https://github.com/getify/You-Dont-Know-JS

deeplearning
https://www.facebook.com/groups/pyonieri/permalink/3292652264080261/
https://deeplizard.com/learn/playlist/PLZbbT5o_s2xq7LwI2y8_QtvuXZedL6tQU
https://www.mff.cuni.cz/en

datovy povolani - Kokes:
ty role se rok od roku mění, ale ta nějak dlouhodobě to vnímám takhle- data analyst - tohle vzniká z těch různých digitálních akademií, databázovejch tréninků atd., zejména deskriptivní analýzy, reporting atd.
- data scientist - taková všehochuť, všichni to chtěj, nikdo neví co to vlastně je, a každej kdo prošel jednou Kaggle competition si to píše do CV
- data engineer - infrastrukturní/orchestrační support pro ty dvě role výše - moc firem je nemá, často jsou (částečně) nahrazovaný nějakou službou/infrastrukturou/kontraktoremco se týče hlášení - tak na analysty se hlásí juniornější lidi, kteří se chtěji dostat do oboru, na scientisty se hlásí skoro všichni a na engineery skoro nikdo
https://gist.github.com/kokes/49ca2f42edf30d6a1f02e3859ad3f9f2

https://www.fullstackpython.com/

Alois Tomasek za me nejlepsi zdroj kterej rad davam je tenhle https://krokodata.vse.cz/ .... k pochopeni SQL je dobry odkaz treba O modelování -> tutorial analyzy -> vztahy

The old age problem of junior sysadmin or programmer pic.twitter.com/OALNV1Xgij— The Best Linux Blog In the Unixverse (@nixcraft) November 26, 2018
https://twitter.com/nixcraft/status/1066903824634384386

MeetUp-ing like a Boss
https://medium.com/le-wagon/meetup-ing-like-a-boss-1a4493d75fa6

Mapa technologií
https://discord.com/channels/769966886598737931/811910782664704040/847778860928860170

OOP bez blbostí
https://www.reddit.com/r/learnpython/comments/lkaffj/looking_for_a_tutorial_on_classes_that_isnt_about/?utm_source=share&utm_medium=ios_app&utm_name=iossmf

DNS, sítě https://twitter.com/simonw/status/1364356791954366464

nejlepsi kurz na OS https://www.udacity.com/course/introduction-to-operating-systems--ud923

Jak vysvětlit OOP https://www.reddit.com/r/learnprogramming/comments/m6yb5z/how_would_you_explain_what_object_oriented/

design patterns overused
https://twitter.com/ericnormand/status/1364595203420479494
https://trello.com/c/eSNJQTCe/2273-design-patterns
K návrhovým vzorům – rozdělil bych je takto 🙂  - takové, na které selským rozumem přijdete (např. zmíněný adapter), ale je fajn mít nějakou terminologii (a bohužel i buzeraci na pohovorech). - pak takové, které řeší nějaký konkrétní problém v konkrétním jazyce (typicky Java, C++), a třeba nedávají smysl v Pythonu - např. singleton - a vzory, které vám pomohou vyřešit nějaký hlubší problém a selským rozumem byste na ně přicházeli dlouho nebo by vás ani nenapadlo je použít - dataloader, data mapper, unit of work, activerecord, idempotence, immutable typy, job queue...

Junior frontend CLI:  hlavně se toho nebát, za mě tohle (+-): ls, pwd, cd, mkdir, touch, ls -a, ls -l, ls -alt (jako ukázka kombinace parametrů), cp, mv, rm, *, ** (globstar), >, |, sort, grep, doplňování, historie příkazů a hledání v historii + základní použití gitu na CLI, curl, bash profile

dataři https://www.kaggle.com/ plus pripnute odkazy na diskuzi
https://discord.com/channels/769966886598737931/769966887055392768/836998750182047804

debata o čistém kódu
https://discord.com/channels/769966886598737931/789107031939481641/838469696663322625

VYSVĚTLIT KONCEPT SLOŽEK A ADRESÁŘŮ A PROJEKTŮ, META JAKOŽE
Já právě v tom roce 2017, jeden den dělali jednoduchou HTML stránku (index.html) a když sem druhej den řekl: otevřete si tu stránku a budeme pokračovat, tak byl problém.
„Nevím kde to je“. Protože při vytváření vůbec nemyslela na lokaci, prostě se to udělá a je to. A pak to dala do spotlightu… index.html je na MacOS zjevně dostkrát…
https://www.theverge.com/22684730/students-file-folder-directory-structure-education-gen-z


--- https://discord.com/channels/769966886598737931/769966887055392768/1106993630209638500
ahoj, mam dotaz, nevim jestli bych to měl psát do poradny, ale já se v těch kategoriích tak nevyznám :

MATEMATIKA pro Developery?
Takže, jsem spokojeně zaměstnanej rok mám víc peněz a nějak stíhám (takže pohoda) a uvažuju o tom že bych ve volném čase kouknul po nějaké matematice pro programátory. Hlavní důvod že mě na základce matematika dost bavila. Studoval jsem sice gympl, ale tenkrát jsem nějak nestíhal chodit do školy 😄 😄  tak ze středoškolský matematiky už skoro nic nevím a co jsem věděl, jsem zapomněl po testu. Každopádně, nic mě do toho nenutí, hrozně rád bych se tím ve volným čase prokousával a vytvořil si alespoň nějaké základy. Jednou začas si k tomu sednu a prokousávám se Khan academy. Přesto budu moc rád za jakékoliv tipy na "základy" plus pokročilé - např. jaké kurzy jsou fakt dobré a tak podobně. Je to takovej geekovskej "kink" se naučit nějakou matematiku, nevím jak moc mě to chytne a nedělám si iluze o tom jak náročnej je to obor. Ale když už se na to podívám, mohl bych to spojit s nějakou matikou užitečnou pro developery :))
---


--- https://discord.com/channels/769966886598737931/788826407412170752/901412010410008577
Pánek má spoustu materiálů k automatizaci: https://www.youtube.com/watch?v=OnpOwlp8Hrg&list=PLZaZq-LUymhx3Lip30OGmsMPdAVoNl45i&index=5
---


--- https://discord.com/channels/769966886598737931/769966887055392768/897087048110997584
Vystudovaná škola je irelevantní, fakt. Když pominu procesní části kyberbezpečnosti, kde je stejně dobrý vstup pro právníka, ekonoma jako informatika, tak ty technický části kyberbezpečnosti na škole nic moc neudělají. I na specializovaných školách je to pár profilujících předmětů, navíc (bohužel) ne vždycky valné kvality. Jako juniorní základ bych řekl, že pokud má člověk technické znalosti, aby dokázal přečíst a pochopit Security Engineering od Rosse Andersona https://www.cl.cam.ac.uk/~rja14/book.html (druhá edice je tam elektronicky zdarma), tak je na tom líp než průměrný absolvent oboru kyberbezpečnosti na výšce. Ta vysoká škola s tímhle zaměřením ti dá prostor se tomu věnovat, ale nic negarantuje - můžeš vyjít super nabitej, nebo taky prolézt s tím, že to na tobě nezanechá stop ani v nejmenším.
---


--- https://discord.com/channels/769966886598737931/811910782664704040/892875350655262773
Nedávno jsem narazil na knihu Refactoring UI (https://www.refactoringui.com/book). Rozebírá tam velmi hrubě základní teorii barev, volbu písem, jak pracovat s bílým místem atd. Je ale hlavně o tom řemeslu a systematičnosti - ukazuje, jakým způsobem postupovat, aby výsledek vypadal dobře. Celá kniha se nese v duchu "redukce možností" - radí například, jak si poskládat paletu barev a jejich odstínů. Když pak člověk vybírá vhodnou barvu pro tlačítko a má 20 možností, tak se trefí spíš, než když jich má 16 milionů (celé RGB). V knížce je i spousta praktických tipů na práci s kontrastem, obrázky, stíny...
---


--- https://discord.com/channels/769966886598737931/788826190692483082/884015212573904916
Zkusil jsem něco dát dohromady, postupně to asi budu vylepšovat: https://itsrazy.cz/
Chybí vám tam kdyžtak nějaký meetup?
---


--- https://discord.com/channels/769966886598737931/788832177135026197/883236495060783114
Motivován debatou jinde, jestli je lepší CZ nebo US rozložení klávesnice pro vývojáře jsem aktualizoval „tahák“ na klávesnici. Třeba by se i tady mohl někomu hodit.

**EDIT: verze aktualizovaná  podle připomínek**
PNG (1920×1080 px) https://coreskill.tech/downloads/klavesnice-cz-en.png
SVG https://coreskill.tech/downloads/klavesnice-cz-en.svg
PDF (A4 pro tisk) https://coreskill.tech/downloads/klavesnice-cz-en.pdf
---


--- https://discord.com/channels/769966886598737931/788832177135026197/877136649933455360
YouTube algoritmus mi po čase doporučil dobré video. Pro ty, kteří baží po přehledném vysvětlení OOP https://www.youtube.com/watch?v=m_MQYyJpIjg
---


--- https://discord.com/channels/769966886598737931/788832177135026197/870253808037552168
Je to devops focused, ale i tak je to sada dobrejch rad, kde ty hlavní jsou: 1) koncepty se napříč technologiema tolik neliší, takže je hlavní pochopit ty, 2) je dobrý mít rozhled, i když jste "jen" programátor, protože pak můžete dělat lepší architektonický rozhodnutí https://www.youtube.com/watch?v=d8X4Nd5gswU
---


--- https://discord.com/channels/769966886598737931/788832177135026197/867726165561049129
Ahoj, posílám zdroje, které jsem já používala:

* toto je super úvod do DB, sice tam používá SQLite a Python, ale začíná s ukládáním dat do Google sheets a uvidíš, jaký je rozdíl a proč jsou DB užitečné, takový krok za krokem, jak jsme se dostali k DB: https://www.youtube.com/watch?v=Wb0DM9I8RDo
* k procvičování SQL doporučuju Murder Mystery, je to hrozně zajímavé: http://mystery.knightlab.com/
* k modelování jsem používala krokodýlovy databáze: https://krokodata.vse.cz/DM/DMDB
* MUNI má materiály k DM online: https://www.fi.muni.cz/~xdohnal/lectures/PB154/czech/

EDIT: když už mám několik špendlíků, zkusila jsem vygooglit další zajímavé zdroje:
* ELI5 (explain like I were 5) o databázích, první dvě odpovědi: https://www.reddit.com/r/explainlikeimfive/comments/jht6he/eli5_what_are_databases_and_how_do_they_work/
* ELI5 o tom, jak ukládat velké množství dat do DB: https://www.reddit.com/r/explainlikeimfive/comments/78ppdo/eli5_how_does_a_database_handle_1_billion_users/
* SQL tutorial: https://www.w3schools.com/sql/default.asp
* SQL joins visualizer: https://sql-joins.leopard.in.ua/
* Vennůvy diagramy, ze kterých vychází SQL joiny: https://www.mathsisfun.com/sets/venn-diagrams.html
---


--- https://discord.com/channels/769966886598737931/788832177135026197/867285980209348628
Tohle nemusí být špatný čtení (díky <@!739821357503742042> , že to na LI lajkla https://blog.oliverjumpertz.dev/the-10-most-valuable-lessons-i-learned-as-a-developer)
---


--- https://discord.com/channels/769966886598737931/789092262965280778/1035308642427228221
https://www.smashingmagazine.com/2020/09/figma-developers-guide/
Ještě článek 😉
---


--- https://discord.com/channels/769966886598737931/797040163325870092/1015688999676936252
https://mystery.knightlab.com/ Kdo je vrah? :))
---


--- https://discord.com/channels/769966886598737931/916339896963190785/1014539554952314901
Tohle je ultimátní YT kanál na tohle téma: https://www.youtube.com/c/professormesser
Má to rozházený po playlistech na certifikace od firmy CompTIA (A+ je obecné IT, NET+ jsou sítě a Security+ je IT bezpečnost)
Sjel bych to přesně v tomhle pořadí 🙂
Pokud bys radši česky, tak sítě jsou super napsaný třeba tady od Peterky: https://www.earchiv.cz/l226/index.php3
Dobrý a vtipný YT kanál od jednoho síťaře: https://www.youtube.com/c/NetworkChuck
Penetrační testování: https://www.hackthebox.com/
Python začni klidně tady, kde jsem začal i já 🙂 https://pyladies.cz/course.html
---


--- https://discord.com/channels/769966886598737931/788832177135026197/1007554087887314944
skvělý materiál na téma, jak fungují web servery

https://ruslanspivak.com/lsbaws-part1/
---


--- https://discord.com/channels/769966886598737931/789092262965280778/1000826851050131537
Teoreticky bys měla umět javascript, a ten se používá i na backendu. Backendistu/fullstack z tebe nebude dělat znalost dalsiho jazyka (i když to se hodí), ale znalost databází, ORM, testování, API, queues (async/background zpracovávání), devops, logování, debugování… vše klidně v javascriptu/typescriptu. Nebo v tom javascriptu aspoň můžeš začít, ať vidíš, jestli se ti to líbí, bez toho, abys nejdřív marnila čas učením se dalšího jazyka. Nebo se můžeš učit typescript, pokud ho zatím neovládáš.
---


--- https://discord.com/channels/769966886598737931/788832177135026197/985177771284262962
20 hodin týdně 2 roky.
https://twitter.com/kondrej/status/1535586323461033984
https://twitter.com/svpino/status/1535230313315508224
https://github.com/ossu/computer-science
---


--- https://discord.com/channels/769966886598737931/806215364379148348/981836438893101066
Tohle není moc o zadání, ale o tom, "jak se orientovat v kodu". Když se teď bavím s těmi, které mám třeba na starosti a dělají vlastní první větší projekty, sami se ptají: "když se dostanu k reálnému projektu, který je velký, jak v tom pracovat?"
---


--- https://discord.com/channels/769966886598737931/769966887055392768/974691777820905502
Trochu navážu i na diskuzi výše, že je podle mě dobré dělat si _přehled_, tedy zkoumat věci do šířky (čím víc, tím líp), ale povrchně. Vědět, že existují, tušit, co dělají. A potom mít jednu dvě věci, které se opravdu _učím_. Díky přehledu se pak mohu lépe rozhodovat o tom, co se chci učit. Nesmí se to ale přehnat, aby se místo získávání přehledu (= pustím si pár YT videí o té věci nebo přečtu jeden článek) nestalo učení všeho (= dokončím kurz na to téma).
---


--- https://discord.com/channels/769966886598737931/811910392786845737/968592246209388615
zaujímavé python výzvy na učenie https://www.practiceprobs.com/
---


--- https://discord.com/channels/769966886598737931/769966887055392768/968070061183082536
Dávnejšie som si pre klientov/rodinu/kamarátov a začiatočnícke Czechitas kurzy napísala IT slovník základných pojmov, ktoré pred nimi používam, aby mi rozumeli a lepšie sa v IT zorientovali - https://kompilator.medium.com/it-slovn%C3%ADk-7b71b75d6099 . Celé som sa to snažila napísať svojimi slovami a dala som tam aj čo ma navyše sem-tam napadlo.
---


--- https://discord.com/channels/769966886598737931/811910782664704040/966976515856273428
b) Ty dvě věci, kromě toho, že obě souvisí s JavaScriptem, jsou vlastně úplně něco jiného.

**Next.js je framework postavený na Reactu.**
Je to React + nějaká hromada kódu k tomu + dokumentace a usnadní ti to dělání webů na Reactu, protože už je tam dost věcí, který bys jinak musel dělat sám, vyřešenejch.

**Node.js je „JavaScript runtime“**, tedy běhové prostředí, to je něco, co umí spustit JavaScript na počítači. Ať už je to tvůj notebook nebo nějaký server a musíš si to na něj nainstalovat a pak tam můžeš spouštět programy v JS.
To samé se dělá pro Python a některé další jazyky.
---


--- https://discord.com/channels/769966886598737931/811910782664704040/965681036157653022
jo, rozhodně zkus. Na tom se naučíš řešit problém v jakéomkoli programovacím jazyce. Codewars je asi nejlepší, protože jsou tam přehledně seřazená řešení od jiných lidí - podle kvality kódu a taky se dá filtrovat podle jazyka. Takže až si to napíšeš sám, koukneš, jak to udělali "mistři". A nebo koukneš, když fakt nevíš. A začíná to úplně lehkýma úlohama. Hackerrank je o něco těžší mi přijde. Na druhou stranu u Hackerranku byly k některým úlohám dost kvalitní diskuse, ze kterých se člověk taky ledacos dozvěděl.
---


--- https://discord.com/channels/769966886598737931/916339236721004595/957246070864363520
Pěkný článek, jak funguje OAuth2 pro začátečníky 🙂 (mě to hodně pomohlo, když jsem se to snažil před lety pochopit) - http://agileanswer.blogspot.com/2012/08/oauth-20-for-my-ninth-grader.html
---


--- https://discord.com/channels/769966886598737931/769966887055392768/945383885531930785
článek k tomu: https://digichef.cz/otazky
---


--- https://discord.com/channels/769966886598737931/806621830383271937/939241551681425448
Není jen JS Fiddle, existuje i SQL Fiddle 😱 🙂 http://www.sqlfiddle.com/#!3/002f1/2
---


--- https://discord.com/channels/769966886598737931/811910782664704040/937839936424509500
https://github.com/kettanaito/naming-cheatsheet
---


--- https://discord.com/channels/769966886598737931/789087476072710174/934111300798271529
<:vscode:628587870273142795>  https://vscodecandothat.com/
---


--- https://discord.com/channels/769966886598737931/916346318048337960/930759930904993834
Pokud ti jde o úplný základy syntaxe, tak doporučju hostovaný tutoriály jako je https://sqlzoo.net/wiki/SQL_Tutorial, bude jich jistě víc (tipuju, že repl.it něco má). Pokud bys pak chtěl vlastní data, tak doporučuju SQLite s nějakým rozhraním - já mám rád mnohokrát zmiňovaný TablePlus (jen mu dáš cestu k databázi na disku a jedeš)
---


--- https://discord.com/channels/769966886598737931/806621830383271937/930220329031307285
[sítě] objevil jsem Cisco Packet Tracer https://www.netacad.com/courses/packet-tracer - docela pěkná hračka k pochopení sítí. Jde tam snadno poskládat libovolná síť a pak pozorovat, kudy a jak data tečou, krok za krokem...
---


--- https://discord.com/channels/769966886598737931/788832177135026197/919699123081449543
Asi to tu ještě nebylo zmíněno, tak to sem dávám – super tool na prohledávání modulů a funkcí ve standardních knihovnách různých jazyků (a sem tam i dalších knihoven). Podporuje i offline režim.
https://devdocs.io/
---


--- https://discord.com/channels/769966886598737931/788832177135026197/913331018864414751
Mě pomohl až Lumír 🙂 https://youtu.be/1UPTK8OTdeg
---


--- https://discord.com/channels/769966886598737931/788832177135026197/910436103838912532
Kdyby chtěl někdo něco programovat 😉
<:python:842331892091322389> <:javascript:842329110293381142> <:java:847749733664555018>
Vypadá, že to je zadarmo.
https://www.codecademy.com/code-challenges
> With technical interviews, practice makes perfect. Now, you can practice real code challenges from actual interviews to see how your skills stack up. If you get stuck, we’ll point you to what you still need to learn.
Nevím, jestli se v českém prostředí tohle objevuje u pohovorů, ale jako cvičení to pro někoho může být zajímavý.
---


--- https://discord.com/channels/769966886598737931/769966887055392768/906580836185428020
K algoritmům obecně třeba tohle: https://knihy.nic.cz/files/edice/pruvodce_labyrintem_algoritmu.pdf
---


--- https://discord.com/channels/769966886598737931/788832177135026197/1099057039549927534
Průlet matematikou, která se někdy hodí většině programátorům. Nemusíte ji umět, ale chcete vědět, jak se to jmenuje a co to je, abyste si to uměli aspoň vygooglit, až to budete potřebovat 🔢 https://youtu.be/bOCHTHkBoAs
---


--- https://discord.com/channels/769966886598737931/1075541542669922424/1098976769509445653
ad materialy, z hlavy:
* surrounded by idiots - jak se lidi chovají a proč se chovají tak, jak se chovají
* how to win friends and influence people - nejlepší kniha ever o lidech a o tom, jak udělat takový dojem, že tě lidi budou mít rádi
* how to present on ted talk - o prezentačních dovednostech, do hloubky a na profi úrovni, přímo od zakladatele ted talků
* the subtle art of not giving a fuck - právě čtu, ale má to dobré hodnocení
* radical candor - o dávání zpětné vazby, užitečné pro ty, co se jí bojí
* https://www.youtube.com/watch?v=Ks-_Mh1QhMc - nejlepší talk ever o sebevědomí a imposter syndromu
* https://www.youtube.com/watch?v=H14bBuluwB8 - o disciplíně a její vlivu na úspěch
---


--- https://discord.com/channels/769966886598737931/788826928147857439/1085251519496073368
Byste někdo kdo se těch Pyv účastníte mohl sepsat, jak to celé probíhá. Pro nás co jsme na podobné akci nikdy nebyli. Mě osobně se to těžko představuje. Bývá to v hospodě, zároveň je tam přednáška...někdy popis v angličtině někdy v češtině. Už z těchto informací mě napadá několik dotazů...komunikuje se tam v angličtině nebo je jen přednáška v angličtině? Sedí se tam po nějakých skupinkách u stolů nebo v řadách jako na přednášce? Je tam nějaký tlak na nově příchozí aby se představili nebo je naopak všichni přehlíží dokud se sami někam neuvedou?
---


--- https://discord.com/channels/769966886598737931/806621830383271937/1065341778682712105
MDO https://www.trywilco.com/
---


--- https://discord.com/channels/769966886598737931/1002976022486057020/1004009895634403479
Ten dotaz je hodně do široka, ale v začátku bych se, jak píše Honza, soustředil na to, abych uměl problém rozložit na podproblémy a hlavně abych dokázal projít takovým tím kolečkem řešení problému:

1. Dostanu zadání (převodník z římských na arabská čísla)
2. Zjistím si všechno o problému který řeším, udělám základní rešerši (přečtu Wikipedii o římských číslech, zjistím kolik mají maximálně znaků, jak se strukturují, jaké mají speciální případy, atd.)
3. Až poté se zamyslím, jak nejlépe věc řešit. Navrhnu řešení. To znamená zamyslím se, jestli už něco neexistuje co můžu použít, jestli to vůbec musím programovat, kouknu se na balíčky, na standardní knihovnu, googlím jestli to někdo už neřešil přede mnou, pak si řeknu ok, asi to opravdu naprogramuju, tak a tak. Rozložím velký úkol na menší úkoly (načtení vstupu, převod textu s římskými čísly do arabských čísel, vypsání výsledku...).
4. Až v tuto chvíli jdu psát první kód.

Někdy je dobré smíchat trochu 3 a 4, čemuž se říká prototypování. Zkoušíš různé věci a to ti pomáhá lépe vymyslet finální řešení.

Toto je podle mě největší úkol pro začátečníka a na toto by se začátečník měl soustředit, aby si to osvojil a ideálně na praktických úkolech.
---


--- https://discord.com/channels/769966886598737931/993478147355971684/993479121483075684
pre ludi co nemaju OOP skusenosti mozem odporucit pozret si nejaky clanok k SOLID principom, napr. https://www.digitalocean.com/community/conceptual_articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design a zapamatat si zo 2 vety k aspon 3 z 5 bodov, to by malo stacit na 99% interview o OOP pre zaciatocnikov, aby clovek nedostal cerveny bod (povedat, ze nemam skusenosti, ale cital som clanok o SOLID a zapamatal som si z toho xxx)
---


--- https://discord.com/channels/769966886598737931/789087476072710174/1112727311347875922
https://cron-ai.vercel.app/
---


--- https://discord.com/channels/769966886598737931/789087476072710174/1112726378677272628
Máš odkaz? Já znám jen https://crontab.guru/ (teda „jen“ bych dal do závorek, už tohle mi přijde hodně užitečné 😄 )
---


--- https://discord.com/channels/769966886598737931/789087476072710174/1111723379028922418
Regulární výrazy. Napíšete a máte. https://www.autoregex.xyz/
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1115564713242271854
Ještě jsem našel tento seznam backend challenges. https://github.com/CollabCodeTech/backend-challenges
---


--- https://discord.com/channels/769966886598737931/1117785793533071450/1117787037794324570
Ano, syntaxí, které jsou všechny markdown, ale mají nějaké speciální vlastnosti nebo s v některých detailech chovají jinak, je plno. Nicméně to, co je tady na Discordu jsou jen základní věci, takže se asi užijí všude, kde se to jmenuje Markdown.
---


---
Stalubo@ v mailu:
3. "PRŮBĚŽNÉ ZAPOMÍNÁNÍ" - i když se učíte denně, tak než se nachytříte jedno, tak to druhé pomalu začnete zapomínat. Protože to nepoužíváte. A nepoužíváte, protože čas není nafukovací a vy ho věnujete novému tématu. Navíc, to že se to člověk naučil, není nijak odměněno. Naučíte se, udělate test anebo si jenom odškrtnete a zatleskáte, ale za měsíc už si z toho pamatujete sotva polovinu. A to máte za sebou jen HTML, CSS a 40% SQL a čeká vás Python a GIt-Github.
; Člověk by už potřeboval dostávat malé "honorované" úkoly, aby získával jistotu, že to není jen učení do šuplíku. Kde netvoří žádné hodnoty. Něco, co by za ním zůstávalo. Když se necháte zaměstnat na part-time do Alberta k pokladně, tak je to sice "málo duchaplná práce", ale někdo vám za ni zaplatí. Když se učíte IT, tak "duchaplná práce", ale nevíte, jestli vám někdo někdy za ni bude ochoten zaplatit (jestli vydržíte, aby jste dosáhl toho stádia).
---


--- https://discord.com/channels/769966886598737931/1113873887445397564/1113931127531520050
Junior guru je skvělá příručka. Nauč se základy , udělej alespoň jeden velkej projekt, vymazli github -cv. Následoval jsem tyhle kroky a fungovalo to. Ale nemůžeš vynechat ten projekt. Musíš si prostě tim ušpinit ruce a zaměstnat hlavu. Když si vymyslíš svůj, bude tě to více bavit. Ale musíš vytvářet. A googlit ,jak na ty dílči kroky, ne procházet něčí osnovu. Protože to tě nenutí tolik přemýšlet. člověk  nesmí skončit u piškvorek z návodu, musí přidat něco svého co ho donutí se posunout. A bude to nepříjemné, když se zasekneě. Stalo se mi to hodněkrát. Celý den jsem strávil na tom , jak udělat jednu věc, kterou senior napíše za  20 minut.  Bylo to peklo, říkal jsem si , tohle už je můj limit.  Ale pak jsem to vždy nějak napsal a fungovalo to. Po třech měsích v práci se stydím, za svůj projekt, se kterým jsem se o tu práci ucházel. Ale podle mě bylo to co zaměstnavatele přimělo mě vyzkoušet. To , že se pokusím udělat to co jsem si dal za úkol i když to je náročné. Protože ten projekt je  pro začátečníka podle mě náročnější než kurz.  Ale zábavnější. A určitě tě vědomí toho, že si to dokázal vyrobit, naplní víc, než certifikát.
Nechci hodnotit výše zmíněné kurzy,  určitě mohou pomoci získat znalosti. Ale upřímně si polož otázku, jestli ty nepotřebuješ jen aplikovat a procvičit to, co už si minimálně jednou slyšel. Fandím ti. Máš výdrž a když nepolevíš, tak se ti ten cíl splní. Sleduji tě už dlouho a opravdu držím palce. Kdyby si měl pocit, že se chceš na něco z mé cesty zeptat, klidně napiš. Ale opravdu, zkus jít za tu hranu, toho, co se ti třeba nechce..tam tě totiž čeká to ,co chceš 🙂
---


--- https://discord.com/channels/769966886598737931/1084817360352989294/1120426048308379831
Bohužel mám příliš mnoho dobrovolnických aktivit, takže se nemůžu věnovat mentoringu. Nicméně mám jednu univerzální radu, která vás může zásadně posunout. Používejte statickou analýzu kódu https://blog.zvestov.cz/software%20development/2023/06/19/enum-a-staticka-analyza-kodu.html?utm_source=juniorguru
---


--- https://discord.com/channels/769966886598737931/789087476072710174/1137689798589554688
Tohle mi zrovna přistálo na timeline na Twitteru a když si vzpomenu na svoji první práci a cizí repo, může to tu podle mě někomu přijít vhod - jak se seznámit s existující / cizí codebase?
---


--- https://discord.com/channels/769966886598737931/811910782664704040/1136264122506416148
Nová stránka na procvičování kódění a programování! 🤩
Je to dost podobné jako FrontendMentor akorát jsou tam daily challenges jako na CodeWars. Plus může to člověk kódit přímo v prohlížeči (jako Scrimba 💜 ) a nemusí si nic stahovat.
https://icodethis.com/
---


--- https://discord.com/channels/769966886598737931/916346318048337960/1129327666290507827
Na vejsce jsme procvičovali na tomhle : https://sqltutor.fsv.cvut.cz/cgi-bin/sqltutor je to absolutně super přesně na biflovani základních selectu - některý datasety jsou triviální (nobelisti a Přemyslovci, některé jako třeba vodočty a tramvaje už vyžadovali vnořené selecty a složitější  kombinování tabulek 😀, takže se dá vybrat co zrovna chceš procvičit. Nejsou to velká data, ale to je na selecty téměř jedno.

Btw měli jsme na vejsce jednu slečnu, co se zvládla na zapoctak naučit všechny ty úlohy zpaměti... 😅🤦
---


--- https://discord.com/channels/769966886598737931/811910392786845737/1127896694323949619
Zajímavý článek o tom, jak použít GitHub API a najít zajímavé nové projekty v Pythonu za účelem toho, že by do nich mohl člověk třeba i přispět v rámci open source: https://mostlypython.substack.com/p/exploring-recent-python-repositories
---


--- https://discord.com/channels/769966886598737931/789087476072710174/1127897372047986709
„What if you could easily get a visual picture of how any Git command would impact your local repo, without interrupting your dev workflow?“ Nezkoušel jsem, ale vypadá to pěkně. Nástroj, který umí vizualizovat co se stane s vaším git repozitářem, když nad ním pustíte nějaký git příkaz https://initialcommit.com/blog/git-sim
---


--- https://discord.com/channels/769966886598737931/789087476072710174/1143045188885942314
Taky jste v záčátku hledali kde ja jaký znak?
https://klavesnice.czechitas-podklady.cz/

A moje frontendová verze v PDF ke stažení https://discord.com/channels/769966886598737931/789087476072710174/1090957362438869092
(založena na pythonní https://pyvec.github.io/cheatsheets/keyboard/keyboard-cs.pdf)
---


Security challenges:
- https://discord.com/channels/769966886598737931/769966887055392768/898300896868433931
- https://www.thecatch.cz/
- https://ctftime.org/
- https://ecsc.eu/


https://m.youtube.com/watch?v=LG-d_BOZE6k


--- https://discord.com/channels/769966886598737931/788832177135026197/1163098667738218586
Pro začátečníky možná až moc podrobnej článek o Unicode, ale zase pokud vás to zajímá, tak si počtete https://tonsky.me/blog/unicode/
---


--- https://discord.com/channels/769966886598737931/788832177135026197/1159450058194948138
Takové pozorování. I jako testeři budete potřebovat základy obsluhy linuxu. A když to budete umět předem, tak můžete zabodovat 😉 Typicky `ssh`, `cd`, `ls` a pak si přečíst logy třeba přes `less`.  Ne všechno a všude bude klikací v grafaně. https://www.thegeekstuff.com/2010/02/unix-less-command-10-tips-for-effective-navigation/
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1157220299658493963
<@544187409026252800> dal na LI pěkný příspěvek o networkingu (jak na to) https://www.linkedin.com/posts/david-rajnoha-a62453168_pyconcz-velvetinnovation-edufestival-activity-7113409610085974016-phRH?utm_source=share&utm_medium=member_ios
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1153399676817653840
Advice to beginners | Ned Batchelder

https://nedbatchelder.com/blog/202309/advice_to_beginners.html
---


--- https://discord.com/channels/769966886598737931/788832177135026197/1148913024577581148
Menší sbírka videí o konceptech kolem programování, poměrně nezávislá na použitém jazyce. https://www.youtube.com/@CodeAesthetic
---


--- https://discord.com/channels/769966886598737931/1184491871637078077/1184812245281165363
Ahoj, datová věda je pomerne široká oblasť. Z toho čo píšeš mi to znie že sa aktuálne formuješ ako datový analytik. Možno by som do tvojho rozhodovacieho stromu pridal ešte zamyslenie nad tým, do akej oblasti by si chcela ísť pracovať.

V tradičných korporátoch napríklad typu banka, kde pracujem aj ja, je dnes datová analýza postavená hlavne na SQL a PowerBI. Pokiaľ by si sa ale rada venovala aj nqpr. datařine v pythone tak si postráž na pohovore aby v tejto firme vôbec existovala podpora pre tento jazyk. Zároveň sa ti môže stať, že ťahúňom v rozvoji python riešení budeš práve ty - to nemusí vyhovovať ľuďom, ktorý vyžadujú silné seniorné vedenie.

V technickejšie zameraných firmách už dnes často datový analytik znamená aj SQL a python - tu ale často býva väčši presah do ďalších oblastí - modelovanie, machine learning atď. a často menší dôraz na tvorbu reportov a vizualizácií.

Jeden spoločný menovateľ je zjavný - vedieť dobre SQL je obrovské plus, nejde ani tak o fancy príkazy ako o schopnosť zorientovať sa v rôznych dátových zdrojoch, tieto dáta pospájať a získať požadovaný výsledok.

Ak by ti PowerBI nevyhovovalo, pretože máš radšej programátorskejší ako klikací prístup, python obsahuje veľké množstvo knižníc kde sa môžeš realizovať. Ja pracujem s knižcou Plotly Dash a naviazanými vizualizáciami v Plotly - u nás v banke ho používame ako alternatívu k PowerBI. Ak by si si chcela spraviť základný prehľad tak k workshopu na pycone som napísal aj rozsiahly návod pre datařov, ktorý by s dashom radi začali: https://github.com/martin2097/pycon-prague-2023-dash-workshop
---


--- https://discord.com/channels/769966886598737931/788832177135026197/1184824550324719616
Já se tady zjevím vždycky jen jednou za čas (hlavně v prosinci, náhoda?), tak aspoň (nejspíš opět) přidám tip na jeden z nejlepších malinko pokročilejších kurzů, který vám pomůže pochopit, jak vlastně počítač funguje a co se v něm děje. A je to zábava 🙂

https://www.nand2tetris.org/, resp. https://www.coursera.org/learn/build-a-computer
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1182391116629286923
Do nedávna byla při programování klíčová schopnost efektivně googlit. Může to vypadat banálně ale umět efektivně googlit se člověk učil roky. Teď bude při programování klíčová schopnost efektivně využívat AI.
---


--- https://discord.com/channels/769966886598737931/788832177135026197/1180500106303242322
Ahoj, nedoporučili byste někdo nějaké kvalitní výukové materiály pro regulární výrazy?
Když tak vidím letošní Advent of Code, které mě tentokrát dokázalo demotivovat v jakýchkoli dalších snahách, asi bych se s nimi měla konečně začít kamarádit. 🙃
---


--- https://discord.com/channels/769966886598737931/806621830383271937/1179302149537140836
<:python:842331892091322389> Mnozí se už přesvědčili, že AI může být extrémně nápomocné, ale zároveň je to občas boj, aby dělalo to, co chceme. Tady je nejen skvěle popsáno, jak toto konkrétní GPTs tvořili, ale hlavně je to zaměřené na pomoc a vysvětlování Pythonu. <:python:842331892091322389>

https://www.linkedin.com/posts/nancyebain_meet-pypilot-a-customgpt-case-study-activity-7134904613622706176-eZ_W
---


--- https://discord.com/channels/769966886598737931/1170648798532489226/1170850238823661678
Angličtina.


Vidím asi 3 možné výjimky:
1. začátečníci na úplném začátku, pokud jim to pomáhá s pochopením toho, co dělají
2. lidi v týmu mají tak špatnou angličtinu, že jejich pojmenování brání chápání kódu těm, kteří ji mají lepší
3. to co už tu padlo, zvážil bych to tam, kde jde o termíny, které jdou blbě přeložit a stejně nikdo nebude vědět, co to znamená
---


--- https://discord.com/channels/769966886598737931/864434067968360459/1169910594497953812
Jaký je podel vás smysl či podstat komunikace a dobré komunikace obzvlášť?
---


--- https://discord.com/channels/769966886598737931/797040163325870092/1170063959508926565
Tady nějaký seznam, který jsem náhodně vygooglil https://github.com/kdeldycke/awesome-falsehood
---


--- https://discord.com/channels/769966886598737931/916339896963190785/1192738348998082611
Pokud používáte nějakého AI asistenta při psaní kódu, tak je jistá šance, že bude méně bezpečný a zároveň budete věřit, že je bezpečnější než kdybyste AI nepoužívali https://arxiv.org/abs/2211.03622
---


--- https://discord.com/channels/769966886598737931/1191365076188397591/1192218179880095764
U te diskuze ohledne AI bych vicemene souhlasil se vsemi zucastnenymi.
Ano, jeji podstatou je efektivita. Ta ale v kazde fazi znamena neco jineho.
Kdyz se ucim stavarinu, ochotne mi poradi, jak vypada cihla, proc malta lepi a jak tuhne beton. Odstranim zaseky, kdy nevim jak dal a zvysim efektivitu UCENI. Netroufl bych si ji ale jeste pozadat navrhnout cely dum.
Kdyz uz ale vim, jak se chova cihla, malta a beton, pomuze mi poskladat modulove patrove domy. Odstrani hodiny skladani a pocitani cihel a betonovych konstrukci. Zase to bude efektivita, ale uz efektivita PRACE
---


--- https://discord.com/channels/769966886598737931/789087476072710174/1194549501982163057
Jen tak na okraj kdo je STUDENT? Nebo dokonce i učitel, tak má COPILOT z GITHUBU ZADARMO!!! Šiřte to dál.
https://github.blog/2022-09-08-github-copilot-now-available-for-teachers/
---


https://cpu.land/
https://osveta.nukib.cz/local/dashboard/
https://www.fakturoid.cz/almanach/osobni-rozvoj/jak-pouzivat-chatgpt
https://www.marketawillis.com/blog/prakticke-programatorske-aktivity
https://www.youtube.com/watch?v=44sJQChy8g0

--- https://discord.com/channels/769966886598737931/797040163325870092/1198884862405386240
Dobré ráno 🙂 pondělní dávka motivace pro všechna kuřata 🐤
https://youtu.be/QG3C1uwuloM?si=wDfZpfewKdenSb7i
---


POVOLÁNÍ
https://www.careerexplorer.com/careers/database-architect/
https://lucietvrdikova.cz/it-tester-pozice/


--- https://discord.com/channels/769966886598737931/806621830383271937/1202873695417401404
Dobré ráno. Na mastodonu někdo sdílel tenhle anglický materiál o networkingu (počítačů, ne lidí) pro lidi, co o tom nic moc nevědí, ale umí v Pythonu. https://beej.us/guide/bgnet0/
---


--- https://discord.com/channels/769966886598737931/788832177135026197/1206557180996747294
Je to sice už trochu mimo zaměření JG, ale jen trochu.
Klára Scholleová sepsala návod „Jak do UX“
http://bit.ly/klary-jak-do-UX

<@668226181769986078> skoro si říkám, jestli bys na to nemohl odkázat někde strategicky v tvojí příručce 🙂
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1212864059591098438
Dalo mi celkem problém pochopit, jak se to vůbec hraje 😅 Ale třeba jsem teď při nemoci jen „pomalejší“. Zkuste! Hra, která by vás měla naučit reguláry. https://regexcrossword.com/
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1212779118647574538
Nedá mi to nezmínit tuhle klasiku :)) https://videacesky.cz/video/problem-s-casovymi-pasmy
Dívali jsme se na ní s kolegy před lety když jsme řešili časová pásma a posílal jsem to kolegům nedávno co pracovali na google calendar integraci 😁
---


--- https://discord.com/channels/769966886598737931/1176897784302014565/1211723120290037790
https://refactoring.guru
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


I regret to say it, but it's true: most of today's programming consists of regurgitating the same things in slightly different forms. High levels of reasoning are not required. LLMs are quite good at doing this, although they remain strongly limited by the maximum size of their context. This should really make programmers think. Is it worth writing programs of this kind? Sure, you get paid, and quite handsomely, but if an LLM can do part of it, maybe it's not the best place to be in five or ten years.
...
Finally, what sense does it make today not to use LLMs for programming? Asking LLMs the right questions is a fundamental skill. The less it is practiced, the less one will be able to improve their work thanks to AI. And then, developing a descriptive ability of problems is also useful when talking to other human beings. LLMs are not the only ones who sometimes don't understand what we want to say. Communicating poorly is a great limitation, and many programmers communicate very poorly despite being very capable in their specific field. And now Google is unusable: using LLMs even just as a compressed form of documentation is a good idea. For my part, I will continue to make extensive use of them. I have never loved learning the details of an obscure communication protocol or the convoluted methods of a library written by someone who wants to show how good they are. It seems like "junk knowledge" to me. LLMs save me from all this more and more every day.
http://antirez.com/news/140


https://twitter.com/kondrej/status/1535586323461033984


--- https://discord.com/channels/769966886598737931/1211759227320803449/1211965435420090393
Včera jsem konečně dojel dvoudílnou nalejvárnu od <@1002301544496119838> a <@1118626383183237200> právě o testingu. Od vstupních požadavků oboru až po zkušenosti přímo z pracovních pozic. Nic lepšího jsem na tohle téma ještě neviděl. To určitě doporučuju zkouknout https://www.youtube.com/watch?v=1efZbhcYY4g + https://www.youtube.com/watch?v=QUWbs_vqSbs
---


--- https://discord.com/channels/769966886598737931/789087476072710174/1215932558286782474
Super nástroj - rozloží URL na kousky a pojmenuje ty kousky https://url-parts.glitch.me/
---


--- https://discord.com/channels/769966886598737931/789087476072710174/1215242926485929994
Návod, jak používat ChatGPT jako svého mentora: https://realpython.com/chatgpt-coding-mentor-python/
---


--- https://discord.com/channels/769966886598737931/916339896963190785/1217392184572117083
Ahoj, za mě osobně jak už psala Kayla, TryHackMe je super start. Interaktivní forma, spousta roomek je i ve free tieru, ideální forma jak se IT bezpečnosti podívat pod pokličku <:meowthumbsup:842730599906279494> . Pokud tě to chytne a zajímala by tě nějaká teorie, tak doporučuju další free zdroj: https://www.youtube.com/watch?v=KiEptGbnEBc&list=PLG49S3nxzAnl4QDVqK-hOnoqcSKEIDDuv. Pokud by tě zajímal obsah ohledně kariéry v IT bezpečnosti, potom můžu osobně doporučit https://www.youtube.com/@UnixGuy/videos. Pokud bys do toho joooo chtěl jít, tak je super Google CyberSecurity cert https://www.coursera.org/professional-certificates/google-cybersecurity. Stojí tě to akorát předplatné Coursery, po splnění dostaneš certifikát, který mi přijde, že je na start úplně super, protože tam v labech děláš i věci, který ti mohou posoužit jako nějaká forma portfolia (Python skripty, SQL query, atd.). Lepší cert je potom Security+, ale prvně bych si asi udělal ten od Googlu <:meowthumbsup:842730599906279494> . Co se těch kariérních směrů týče, dělám IT bezpečnost už třetím rokem a pořád nevím, kam se budu chtít směřovat, takže bych to na začátku asi moc neřešil <:exactly:1100463303190396968> . Není to samozřejmostí samozřejmě, ale entry-level job v IT bezpečnosti je stejně SOC Analytik/IT Security analytik, takže je to hodně o data analýze, SIEMu, EDR, síťařině, atd. Pokud by tě ještě něco zajímalo, tak se ptej <:meowthumbsup:842730599906279494>
---


--- https://discord.com/channels/769966886598737931/916339896963190785/1217218996747767848
Ahoj, pokud začínáš se cybersecurity z nuly a ještě nevíš, tak fajn je https://www.tryhackme.com - je to v podstatě interaktivní učebnice mnoha podob cybersecurity a jsou tam různé průchody.

Pokud tě zajímá bezpečnost frontendu, tak základ je OWASP a takový interaktivní OWASP pro programátory najdeš na https://www.hacksplaining.com
---



Ano, je to právě o praxi, o nekonečném cyklu "napíšu kód" -> "v něčem nevyhovuje, tak ho zkusím zlepšit" -> "ze změny odvodím nějaký obecný závěr, který mohu příště aplikovat v podobných situacích" -> "napíšu další kód" ...  Někomu to jde samozřejmě lépe, někomu hůře, ale každý si tím musí projít.

Když už se v programování člověk trochu orientuje, tak znám dvě "zkratky", jak je možné se samostatně hodně zlepšit v relativně krátkém čase:
1. Číst kód jiných, zkušenějších - najít si třeba nějakou open-source knihovnu, procházet její kód a všímat si, jak je strukturovaný, jaké jsou použité konstrukce apod. Bude to lépe fungovat pro knihovny, které spravuje primárně jednotlivec či menší tým, který na kvalitu hodně dbá - to bohužel nelze na první pohled poznat, lze se trochu orientovat množstvím uživatelů (více = lépe) a množstvím přispívajících (méně = lépe). V PHP mohu doporučit např. Nette, kde David Grudl drží laťku poměrně vysoko. V Pythonu má dobrý kód například knihovna requests, za kterou stojí Kenneth Reitz (a lze kouknout i na další projekty tohoto autora).
2. Nastudovat si odbornou knížku na toto téma a znalosti ihned zkusit aplikovat na své projekty - knížka v bude fungovat asi nejlépe, protože prošla náročným procesem korektur a revize a nakonec někomu stálo za to, aby jí vydal. Navíc hodně pomáhá rychle listovat mezi jednotlivými sekcemi, což je snadné zvlášť u fyzické knihy. V češtině vyšla například kniha Čistý kód od Roberta C. Martina (tu už asi bude problém sehnat). V angličtině mohu doporučit knihu Refactoring od Martina Fowlera. Na pozoru bych byl v případě knih od Packt Publishing, u nich pozoruji hodně kolísající kvalitu - vždy se rozhoduji podle negativnách recenzí. Kniha nejspíš bude uvádět příklady v jiném programovacím jazyce, než na který jste zvyklí, typicky ale stačí jen velmi malá znalost daného jazyka a naprostá většina tipů je přenositelná i do jiných jazyků.


--- https://discord.com/channels/769966886598737931/769966887055392768/1221027991480700978
A jak pojmenovávate proměnné a funkce vy?
https://github.com/kettanaito/naming-cheatsheet
Jak známo
> There are 2 hard problems in computer science: cache invalidation, naming things, and off‑by‑1 errors.
---


--- https://discord.com/channels/769966886598737931/1084817360352989294/1220016270125301820
teďka už pár týdnů zkouším https://codegym.cc/ a zatím můžu doporučit! Těším až se proklikám k pokročilejším částem jako jsou Core Java (lets see) a multithreading, - nedá se úplně otestovat a přeskočit tak si to procházím od píky :))
---


--- https://discord.com/channels/769966886598737931/1217484087065968684/1219223656895348797
Tak jsem se Devin AI podíval pořádně na zoubek a zatím bych se držel Copilota a ChatGPT. 🙂

Věřím, že průměrný junior tady odsud by podával lepší výsledky než DevinAI!

Tady je o tom příspěvek, lajkujte, sdílejte dle libosti. 🙂
https://www.linkedin.com/posts/bleedingdev_problems-with-devinai-activity-7175429487478603776-5CCS
---


--- https://discord.com/channels/769966886598737931/789107031939481641/1235975819755786310
A přesně pro tyhle případy mám v **Nauč mě IT** 🧠  super zdroj na učení KONCEPTŮ, abys pochopil principy napříč frameworky. Tady se učí tak, abys chápal všechny 3 hlavní. 🙂

https://unicorn-utterances.com/collections/framework-field-guide
---


--- https://discord.com/channels/769966886598737931/1237340412545339392/1238050805739683901
Já bych tam zahrnul klidně i ty cvičné příklady k certifikaci. Samozřejmě bych u nich viditelně uvedl o co jde a v rámci čeho jsi je dělal. Počítej s tím, že budou mít daleko menší váhu, než nějaký reálný projekt, na kterém pracuješ. Osobně si myslím, že ten jeden projekt stačit klidně může. Bude dělat lepší dojem, když budeš mít jeden projekt, který máš rád, dává ti smysl, víš o něm první poslední a vyzkoušel sis na něm vše co ses naučil. Uchazečů s vypracovanou tisící kalkulačkou a úkolníčkem (nejčastější mikroprojekty na internetu v portfoliích začátečníků) bude doslova plný pytel. Těch jako ty, s nějakým komplexním projektem s osobní vazbou, zase tolik nebude. Ve finále právě díky těm pohovorům se dozvíš, jaká je ta reálná poptávka, jaký stack bys měl asi tak mít a kam směřovat. Abys s každým dalším pohovorem byl lepší a žádanější.
---


--- https://discord.com/channels/769966886598737931/788832177135026197/1236340466665132133
Našiel na nete, možno sa to niekomu zíde. https://andreasbm.github.io/web-skills/
---


--- https://discord.com/channels/769966886598737931/1233369095236354109/1233372219833450527
Stáhni Unity (nebo teď už možná radši Godot), otevři dokumentaci k enginu i k C# a začni. Víc nepotřebuješ. Už vůbec nepotřebuješ začínat Cčkem. Tím, že tu hru děláš, se učíš nejrychleji. A vůbec nevadí, že tvoje první hra bude mít špagety kód. Spousta úspěšných indie her má hrozně zprasenej kód, ale pro jejich potřeby funguje.

Udělej kostičku, nauč jí pohyb, pak jí nauč kolidovat s jinou kostičkou, nauč se interakci s prostředím, animaci, textury, level design. Klidně začni s freebies modely a prostředími z Asset Store a uč se na nich. Jakmile uděláš něco funkčního, budeš z toho mít radost a budeš se učit ani nevíš jak 🙂 Později se pak rozhodneš, jestli chceš dělat celou hru a nebo se zaměříš na konkrétní disciplíny toho celýho procesu.

Hlavně začni dělat nějakou hru, klidně jednoduchou. Jestli se teď zaboříš do nějakého C, tak v něm budeš plavat dny, týdny, měsíce aniž bys začal na hře vůbec dělat a tvůj entusiasmus je fuč. Jako takovýho malýho průvodce tvorbou první hry od startu do konce můžeš brát tenhle manuál https://develop.games/#nav-skills. Probírá všechny aspekty herního vývoje hodně jednoduše, ale jasně.
---


--- https://discord.com/channels/769966886598737931/788832177135026197/1232629397971009608
Kdybyste se chtěli učit regulární výrazy https://regexone.com/
---


--- https://discord.com/channels/769966886598737931/788832177135026197/1234430460851916831
Python pro matematiky 🙂 https://vknight.org/pfm/cover.html
---


AI: https://www.linkedin.com/posts/marketa-willis_je-opravdu-ai-takov%C3%BD-pomocn%C3%ADk-v-programov%C3%A1n%C3%AD-activity-7215986228007989248-Sh-p?utm_source=share&utm_medium=member_desktop


--- https://discord.com/channels/769966886598737931/789087476072710174/1297821423875653676
Když už jsme u databází, narazil jsem dnes na databázi databází! Takže až na vás někdo vytáhne něco jako „my to hážem do DuckDB 🦆 “, nemusíte jen nepřítomně mrkat a přemýšlet, jestli si dělá srandu, nebo fakt existuje nějaká kačeno-databáze. Můžete si to tady najít a něco si o tom přečíst: https://dbdb.io/
---


--- https://discord.com/channels/769966886598737931/811910782664704040/1288801642489053218
První díl tohohle seriálu jsem sem už dával (na jiný kanál) a původně jsem neměl záměr spamovat s tím, že vyšel další skvělý díl téhož seriálu, nicméně vzhledem k tomu, že ten dnešní se zaměřuje na nejdůležitější věcí kolem písem na webu, tak to sem přece jenom hodím. Je tam za mě celá řada věcí, o kterých se domnívám, že by měly být univerzálně přijímány a používány (a bohužel nejsou), ale přihodím jenom jednu citaci:

*„Na obrazovku nepatří absolutní jednotky. Žádné body nebo pixely. Sice už není pravda, že takto definovanou velikost písma nelze v prohlížeči zvětšit či zmenšit, ale pořád platí, že o jeho prostředí nic nevíte. Proto je rozumné držet se jednotek rem a em. Ta první odpovídá výchozí velikosti písma prohlížeče. Lze předpokládat, že uživatel v ní má hodnotu, která mu vyhovuje. Většina si nechá tu, která zde byla po instalaci, ale pokud uživateli výrazně nesedí, nejspíš si ji upravil podle své potřeby.“*

https://www.root.cz/clanky/pisma-na-webu-rodina-je-zaklad-pisma/
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1285194129495560192
Na LinkedInu, u svých studentů nebo i tady často vidím, jak se lidé dostávají do problémů, jako je tutorial hell, porovnávání s ostatními, učení všeho nazpaměť, nevytváření vlastního projektu. A ve výsledku to pak často vzdají.

Ale řekla bych, že v poslední době vede tutorial hell (společně s nedostatkem sebedůvěry), a nemusí se jednat jen o kurzy typu Udemy, ale i různé intenzivní kurzy.

Jelikož už je to doba, co jsem tento problém řešila u sebe, co byste doporučili lidem, kteří se dostali do takové pasti?

A pokud byste měli chuť, před nějakou dobou jsem na toto téma natočila video. https://www.youtube.com/watch?v=I2s2BtrHw3I
---


--- https://discord.com/channels/769966886598737931/1279530837452263435/1279531421178007633
A práve preto si myslím, že tu môžu excelovať aj začínajúci programátori - je to totiž znova viac o premýšľaní a soft skilloch ako o hard skilloch - tie sa začnú do popredia dostávať až za pár rokov, až obor maturuje a bude jasné, čo je potrebné a čo nie - dnes to jasné nie je, môžeme iba hádať.

Pokiaľ by sa do toho teda chcel niekto pustiť, tu je pár tipov čo si pridať do portfólia - a pozor, tu si myslím, že tieto úlohy dokážu pomôcť aj u iných pozícii nielen u AI specialistov. Niektoré firmy dnes na AI proste počujú. Skúsim to popísať čo najviac jazykovo neutrálne ale najfrekventovanejší jazyk v AI svete je asi python a sám z toho sveta pochádzam, preto si dovolím túto skupinu aj tagnúť <@&1085220736957947905> .
- prečítajte si niečo o písaní technických promptov, u všetkých úloh budete model inštruovať, čo má robiť. Nevenujte tomu ale priveľa času. Inšpirujte sa ako to robia iný - existujú napr leaknute system prompty od Applu, oficálne ich publikuje aj spoločnosť Anthropic.
- osahajte si OpenAI API - dnes to už skoro nič nestojí, do začiatku dostanete aj nejaký budget na voľné testovanie
- následne sa pozrite na to, ako sa dnes stavajú konverzácie - aký je rozdiel medzi správou uživateľa a asistenta, čo sú to systémové správy - a následne si nejaké konverzácie sami postavte
- a teraz sa dostávame k prvému veľkému pojmu sveta AI: RAG (Retrieval-augmented generation). Pozrite sa na to, čo to je, ako to funguje.
- naimplementovať RAG bola kedysi zložitá úloha. Vy sa ale pozriete na to, ako využiť OpenAI API pre asistentov - konkrétne funkcionalitu Vector Stores
- keď už budete skúmať API pre asistentov pozrite sa aj na ostatné funkcionality - code interpreter a function calling
---


--- https://discord.com/channels/769966886598737931/1279530837452263435/1279531508931100694
Tieto funkcionality boli ešte rok a pol dozadu celý programátorský tým a tisícky riadkov kódu. Dnes je to jedno API, jeden balíček v Pythone alebo inom jazyku. Postavte si na tomto svoje portfólio projektov a skúste demonštrovať rôzne využitia týchto funkcií v svete, ktorý poznáte. Príklady:
- unstructured to structured - stiahnite si sadu nejakých neštruktúrovaných formátov dát - články z internetu, texty atď - preveďte tieto dáta do štruktúrovanej podoby - nechajte AI určiť titulok, zakategorizovať, vyťiahnuť osoby, miesta, určiť sentiment atď. Tieto úlohy sú veľmi populárne a užitočné
- vymyslite jednoduchú automatizáciu procesu na ktorej demonštrujete svoju komplexitu - na vstupe máte nejaký formát, ten môžete nejako transformovať, niečo z toho programaticky vybrať, nechať to spracovať modelom a následne dostať nejaký pekný výstup - napr. sledujete obľúbené newslattery ale nemáte čas všetko čítať - preto by ste chceli pocníka, ktorý to prečíta za vás a vyberie 5 pre vás najrelevantnejších informácii. Na môžete demonštrovať, že si dokáže scrappnuť stránku, nastaviť prompt a celé to poskladať dokopy.
- postavte si chatbota alebo asistenta - zamerajte ho na niečo, vytvorte si vektorovú databázu - napr. máte vlastné recepty v 50 rôznych PDF. Vytvorte si asistenta, ktorý vám bude navrhovať recepty na základe surovín a vďaka RAGu bude poznať aj tie vaše :).
- nefixujte sa iba na chatbotov - ako sa ukazuje prázdne chatovacie okno je vlastne veľmi špatný frontend pre väčšinu use casov - väčšina ľudí netuší čo tam zadať. Pripravte funkciu, ktorá na vstupe dostane text a na výstupe vráti sumarizáciu. Ako parametre príjma dĺžku sumarizácie (stručná/podrobná), tón (formálna/neformálna), typ (súvislý text, v bodoch) atď. Pokiaľ vás bavia maličké aplikácie vytvorte si jednoduchý frontext napr v dashi alebo streamlite.
---


--- https://discord.com/channels/769966886598737931/811910782664704040/1282974118387388477
Asi nejlidštější vysvětlení CORS https://jakearchibald.com/2021/cors/
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1282439742184624129
ja som si trénoval Python na týchto cvičeniach:
https://www.hackinscience.org/
(spravuje to jeden Francúz, python-core-developer

resp. tento menší tým:
https://www.hackinscience.org/team/
)
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1279530837452263435
Ahojte,
vopred sa ospravedlňujem, tento post bude dlhý. Dúfam ale, že to dá podrobnejší vhľad do AI ako oboru v IT. Mám za sebou 2 mesiace od momentu, keď som svoju kariéru poslal all in do segmentu AI. Mojou prácou sa stalo hľadanie hodnoty rôznych AI riešení pre našu banku a ich privádzanie k životu. Už dlhšie som tu chcel spísať svoje myšlienky a hlavne svoje myšlienky k otázke: **Som ašpirujúci junior v IT, čo pre mňa znamená smerovať svoju kariéru do oboru AI a má to zmysel?**

Hneď na začiatok by som rád poďakoval <@668226181769986078>, vďaka ktorému som objavil Simona Willisona, ktorý o AI veľa píše a veľa hovorí a to čo píše a hovorí je veľmi rozumné :). A okrem toho prednášal aj na PyConUS:
https://youtu.be/P1-KQZZarpc?feature=shared&t=247.
Ak sa chcete dozvedieť, kde sa obor umelej inteligencie nachádzal v květnu 2024 (+- je to stále platné aj pre srpen 2024) dajte si tento talk, je to pre ľudí z IT, ktorý sa ale AI nevenujú, ten najlepší status ktorý som zatiaľ našiel.

Prečo na to odkazujem? Pretože sú to závery veľmi podobné tým, ktoré aktuálne vyvodzujeme aj my v banke. Za prvé je vďaka tomu možné vyvodzovať, čo by sa ašpirujúci junior potreboval naučiť (o tom neskôr) a za druhé, je dôležité uvedomiť si, že pokiaľ sa dostanete do tém, ktoré je možné zhrnúť v 40 minútovom talku, budete patriť medzi 5% najlepších v obore :). Na prvý pohľad odvážne tvrdenie, treba si ale uvedomiť o akom obore sa bavíme.

Keď sa dnes budete baviť s ľuďmi, ktorý o sebe deklarujú, že sa venujú alebo zaujímajú o AI dozviete sa pravdepodobne: Že používajú ChatGPT, že im naplánoval výlet, pripravil recept alebo zhrnul novinový článok. Z pohľadu práce sa možno dozviete o tom, že im zosumarizoval alebo napísal email, preložil text alebo pomohol vybrainstormovať názov udalosti. A tieto odpovede boli u väčšiny ľudí rovnaké mesiac po tom, čo ChatGPT vyšiel a dnes. Existujú ale aj use casy, ktoré prinášajú obrovskú hodnotu a tu môžete aj ako junior excelovať.

A viac vo vlákne 🙂
---


--- https://discord.com/channels/769966886598737931/806621830383271937/1268489379798716497
Dobra stranka na rychle vyskusanie si jinja templatov  https://j2live.ttl255.com/
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1250701548015849492
Mám tady dvě věci na věčné téma AI a programování. Jedna je tenhle krátký příspěvek: https://mamot.fr/@ploum/112591341366625479
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1250701886185672774
Druhá je strašně dlouhý článek, který má argumentovat, že ne, AI fakt programátory nenahradí. Ale ještě jsem ho nestihl celý přečíst. https://stackoverflow.blog/2024/06/10/generative-ai-is-not-going-to-build-your-engineering-team-for-you/
---


--- https://discord.com/channels/769966886598737931/916339896963190785/1326828578570108930
Ahoj, já pracuji jako SOC analytik pro jednu z předních českých bank. Vzhledem k tomu, že práci SOC analytika vnímám jako vstupní bránu do světa IT bezpečnosti, níže sepsané se bude primárně aplikovat na tuto roli. Zároveň dodávám, že nemám patent na rozum a určitě je mnoho jiných cest, moje tipy jsou tipy, které fungovali konkrétně mě, třeba mě někdo doplní, nebo opraví. Pro vstup do IT bezpečnosti je ideální mít nějaké znalosti ze síťařiny a nějaký úvod do IT bezpečnosti se také hodí. Osobně kdybych v oboru začínal dnes, udělal bych si Google Cybersecurity Professional Certificate, kde dostaneš do povědomí základní koncepty, mají tam skvelé laby a praktická cvičení včetně skriptování v Pythonu. Stojí tě to měsíční členství na Courseře, nečeká tě žádný závěrečný (zpoplatněný) test navíc, jen dílčí testy. Odkaz: https://www.coursera.org/professional-certificates/google-cybersecurity. Pak bych si vyzkoušel TryHackMe, což je v podstatě gamifikované učení IT security a věcí kolem. Mají laby, vlastní virtuálky, je tam toho spoustu, mají věci zadarmo, ale pokud tě to chytne, předplať si, teď ještě běží nějaká akce na 25% slevu. Odkaz: https://tryhackme.com/. Podobného ranku je i HackTheBox, což je spíš ofenzivní bezpečnost, ale pro případ, že by jsi se chtěla vydat cestou penetračního testování, tak je to asi lepší varianta, ale tam nemám zkušenost. Odkaz: https://www.hackthebox.com/. Kdyby tě cokoliv zajímalo, dej vědět a odpovím 🙂
---


--- https://discord.com/channels/769966886598737931/916339236721004595/1318873426735140875
Advent of Docker 🐳🎄
https://adventofdocker.com/
(možno sa niekomu zíde)
---


--- https://discord.com/channels/769966886598737931/1317108571586035772/1317108571586035772
https://www.debugdecember.com/intro
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1316522462015651842
Ahoj,
tohle jsem adresoval pro <@1160890913900474439>, který taky musel jít cross-framework a je na to skvělý portál:
https://playfulprogramming.com/collections/framework-field-guide-fundamentals
---


--- https://discord.com/channels/769966886598737931/1177266646579163246/1312718422425079810
Odpověď na rebelskou otázku je za mě, že to musíš umět, abys ses mohla správně ptát AI a kontrolovat/vybírat z toho, co ti vytváří. U věcí, kde na tom nezáleží a nerozumím tomu (jednoduchá automatizace v PowerShellu), klidně nechám AI vygenerovat v podstatě všechno, ale když se bavíme o produkčním kódu, tak tomu rozumět dost pomáhá.
A ne, není špatně odpovídat na řečnické otázky. 😉
---


--- https://discord.com/channels/769966886598737931/806621830383271937/1307261443393060965
Perfektne na cvicenie a ucenie sa pracovat s gitom... Neviem ci to tu je, ale mozno zaciatocnikom to moze pomoct 🙂 a mozno to je blbost 😄 ale mna to ohurilo...
https://learngitbranching.js.org/
---


--- https://discord.com/channels/769966886598737931/788832177135026197/1336405349883707504
Během Q&A s <@377398623777980418> padl tip na tenhle skvělý zdroj informací o DevOps, cloudu, apod. Neznal jsem! https://www.youtube.com/channel/UCdngmbVKX1Tgre699-XLlUA
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1341174664692498553
> We’re trading deep understanding for quick fixes, and while it feels great in the moment, we’re going to pay for this later.
https://nmn.gl/blog/ai-and-learning
---


--- https://discord.com/channels/769966886598737931/806621830383271937/1337160739550527548
Hraju si s AI a mapováním codebase a musím říct, že jsem fakt mile překvapen, jak rychle se jeden může dneska dostat do projektu, když použije AI.

1. Konvertujte repozitář na *AI friendly formát*, např. pomocí Repomix (https://repomix.com/)
2. Použijte Gemini 2.0 Pro na AI Studio (https://aistudio.google.com/)
3. Vložte celý markdown vaší codebase. Limit je **až 2 miliony tokenů**, což je fakt dost (pro srovnání ChatGPT má 10x méně!)
4. Ptejte se.

Kdyby se někdo chtěl podívat na příklad, tak tady je (snad vám půjde načíst konverzace s Gemini - nejspíš musíte být přihlášeni).
https://drive.google.com/file/d/1DgGLqlgjHVbS-tcHYbDYe6yE5Jeddqu-/view?usp=sharing
https://aistudio.google.com/app/prompts?state=%7B%22ids%22:%5B%221TIN5E3Tjyd-oDVaUHwu1w0Ks-nAAPTdS%22%5D,%22action%22:%22open%22,%22userId%22:%22116194854355489944248%22,%22resourceKeys%22:%7B%7D%7D&usp=sharing
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1327169918596157440
Jestli se chceš věnovat bezpečnosti, navrhuji začít třeba s coursera Cryptography I, ať víš, do čeho jdeš 😉  https://www.coursera.org/learn/crypto případně knihu (zatím jsem nečetl, ale Manning je záruka kvality) https://www.manning.com/books/real-world-cryptography
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1327170061894418452
> While AI-Assisted coding can get you 70% of the way there (great for prototypes or MVPs), the final 30% requires significant human intervention for quality and maintainability.
https://addyo.substack.com/p/the-70-problem-hard-truths-about
---


--- https://discord.com/channels/769966886598737931/1347227383240986766/1349032743731990601
Ja si prihreju polivcicku - https://www.youtube.com/watch?v=02XHM_XvsWs

Za me je u DevOps nejdulezitejsi Infrastructure as Code (IaC), udelal jsem si prednasku pro zacatecniky na tema, jak ma vypadat novy projekt (v Pythonu, ale je to aplikovatelne na cokoliv) z pohledu DevOps
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1348749488185147463
🎮 Brácha <@1061399828552241204> slyšel díl podcastu [Technicky vzato](http://www.vutbr.cz/podcast) (#36 – Kdy se z Česka stane tahoun na poli videoher? [mp3 zde](https://www.buzzsprout.com/1279862/episodes/16518248-36-kdy-se-z-ceska-stane-tahoun-na-poli-videoher.mp3)) a prý tam povídala o nějakém komunitním centru pro game vývojáře, indie vývojáře, alternativní scénu a tak: https://www.gamebaze.cz/ Je to v Brně. Nevíte o tom někdo něco? Máte někdo nějakou zkušenost? Možná by to mohlo být zajímavé pro lidi, které láká game dev.
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1394319792726605907
Hele hele 🙂 https://medium.com/@kt149/github-ceo-says-the-smartest-companies-will-hire-more-software-engineers-not-less-as-ai-develops-17d157bdd992
---


--- https://discord.com/channels/769966886598737931/788832177135026197/1393694955767201893
Chcete si pohrát s DNS záznamy? Prakticky je to poměrně těžké a zdlouhavé, ale tady je „pískoviště“, které to umožňuje zkoušet snadno a rychle https://messwithdns.net/
---


--- https://discord.com/channels/769966886598737931/788832177135026197/1390795782306660575
Jak promptovat ChatGPT, aby vás učilo 🧑‍🏫 https://gist.github.com/Dowwie/5a66cd8df639e4c98043fc7f507dab9e
---


--- https://discord.com/channels/769966886598737931/806621830383271937/1388172079383183441
Kdo má rád problem-solving, logické úlohy, matiku, AI
https://brilliant.org/
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1381720088364712039
Me pomohly tyto materialy 🙂  se od piky v tom vyznat https://youtube.com/playlist?list=PLFt-PM7J_H3HNjtAXCCeQPyRioItF1egJ&si=BOb4FhUlaEz_sd2j
---


--- https://discord.com/channels/769966886598737931/789087476072710174/1379089534985310278
Tak za mě supr, ale dokumentace to moc není, ono to projede celý commit, sepíše co se událo, rozepíše všechny stránky, layouty, komponenty, store, objekty a jejich typizace, input validátory,  parsování, použité nástroje jako Eslint atd., dokonce i package.json verze jeho balíčků, dokonce i dotazy na DB, no úplně komplet !   😄  A na všechno vytvoří recenzi = doporučení zlepšení, zabezpečení ( XSS zranitelnosti )  ukázky vylepšení kódů, wow. Vlastně takový validátor celého projektu. Popravdě je toho tuna na co bych se měl podívat a vše vypadá aspoň za zkouknutí, nejsou to úplné blbosti.
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1372863264756596756
Je pravda, že v poslední době když tam jdu něco hledat, tak jsou tam otázky i odpovědi zpravidla 3, 5, nebo dokonce 10 let staré, ale aktuálnějšího často nic nenajdu 🫤 https://blog.pragmaticengineer.com/stack-overflow-is-almost-dead/
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1363734255531987084
Čert aby se v tom vyznal 😀 Jeden tvrdí to, druhej něco jiného. Jeden podporuje juniory, druhý je odrazuje kvůli AI, atd. Tak alespoň jeden povzbuzující článek po ránu 🙂 https://www.vzhurudolu.cz/blog/258-ai-programovani-psani
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1361396017810898975
https://www.joshwcomeau.com/blog/the-post-developer-era/
---


--- https://discord.com/channels/769966886598737931/788832177135026197/1356688906950676592
Za mě top jsou tyhle materiály:
https://sqlzap.com/
https://datalemur.com/sql-tutorial

A pak bych se ještě podíval na Zacha Wilsona (ex-Airbnb a ex-Netflix) a taky na Alex the Analyst. 🙂

Případně ti ještě něco může doporučit <@642430988332302347> .
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1360212807135789106
Zajímavý článek o AI a potřebě programátorů.
Zaujal mě Jevons Paradox, ten jsem nikdy neslyšel. Je to ekonomické pravidlo, že vyšší efektivita využívání zdroje vede paradoxně k vyšší, spíše než nižší spotřebě.
A tady se mluví o spotřebě vývojářů <:meowthumbsup:842730599906279494> 

https://www.infoworld.com/article/3955073/ai-will-require-more-software-developers-not-fewer.html
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1356184716683907092
🎙️ Kdo jste ještě neslyšel <@668226181769986078> na Lupa, tak šup https://www.lupa.cz/clanky/honza-javorek-junior-guru-jenom-clovek-vam-rekne-co-chatgpt-poradil-spatne
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1401950840411132035
Raději sem hodím tohle, co mi poslal <@156884455628341249> jako námět k plánovanému https://discord.com/channels/769966886598737931/1375466381801291918: OpenAI má nově mód na studium https://simonwillison.net/2025/Jul/29/openai-introducing-study-mode/
---


#} -->
