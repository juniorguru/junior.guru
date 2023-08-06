---
title: Projekty
emoji: 🏗️
description: TODO
template: main_handbook.html
noindex: true
---

{% from 'macros.html' import note with context %}

# Projekty

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }} Tuto stránku Honza právě připravuje. Brzy tady něco bude.
{% endcall %}


<!-- {#

kam veřejně napsat, že tady chybí https://junior.guru/handbook/practice/#najdi-si-projekt info o tom, že projekt nemusí být unikátní? že to může klidně být todolist
protože mám pocit, že si to tak 2/3 lidí myslí, možná i víc

https://free-for.dev/

Challenging projects every programmer should try - Austin Z. Henley
https://austinhenley.com/blog/challengingprojects.html

https://www.frontendmentor.io/

https://codingcompetitions.withgoogle.com/codejam
https://adventofcode.com

Prozkoumat tohleto od Radka - https://www.codingame.com/start

ODKAZ + Oficiálna windows calkulacka je napisana v C++, open source tu https://github.com/microsoft/calculator Kalkulačky napísané v pythone nájdete tu https://github.com/topics/calculator-python

Návrhy na menší projekty, které si začínající programátor může zkusit udělat

Zen advice about code ownership
https://twitter.com/vboykis/status/1325972944636567553

jak na projekty https://discord.com/channels/769966886598737931/769966887055392768/897411691321643018

projekty: hypotecni kalkulacka, bot na CI o pocasi, git scraper, ...

nápady na "domácí projekty"

projekty vs zadání na pohovory

č.d jako projekt https://discord.com/channels/769966886598737931/769966887055392768/809182650497105930

Jak na projekty
https://docs.google.com/document/d/1gk-sER2SHuW6T9sJZyYg5nMUaKNh0w2_-5HCGiF9zxs/edit
https://discord.com/channels/769966886598737931/769966887055392768/817042156581421086

https://blog.cesko.digital/2021/06/zkuste-open-source

tipy na projekty - č.d nebo okopírovat věc (spotify, yablko kurz viz link)
https://www.linkedin.com/feed/update/urn:li:activity:6796762431776403456/
https://www.codementor.io/projects

https://www.heroine.cz/zeny-it/7047-jak-si-vybudovat-portfolio-a-ukazat-co-uz-v-it-umite

koľko HODÍN DENNE musím PROGRAMOVAŤ? (programátor radí) https://www.youtube.com/watch?app=desktop&v=LG-d_BOZE6k

big book of small python projects https://nostarch.com/big-book-small-python-projects, https://overcast.fm/+YStfd8vYo


https://www.facebook.com/groups/frontendistiprace/posts/3175112979423874

Jak tady už lidi radí, kurz nestačí - i kdyby ti to na kurzu nastokrát opakovali 🙂 Pár takových kurzů se blíží k tomu, aby to stačilo, ale i tak někdy pochybuju. Až se něco naučíš, potřebuješ si to pak sám na něčem vyzkoušet a dokázat tím sobě a později na pohovoru ostatním, že nabyté znalosti dokážeš samostatně aplikovat. Samostatně neznamená, že ti nesmí nikdo radit, to vůbec, ale že sám postupuješ a postupně něco tvoříš, debuguješ, hledáš řešení, vybíráš řešení, aplikuješ rady, analyzuješ problém, rozvrhneš si práci.

Takže přesně jak tady padlo, udělat appku na počítání slepic. Nejdřív jen HTML a CSS, pak něco rozhýbat přes JS. Pak přidat počítání bobků slepic. Pak přidat uložení do localstorage. Pak přidat možnost lajkovat slepice. Pak vylepšit design. Pak to třeba přepsat do nějakého frameworku. Tohle si po večerech ladit, ptát se všech okolo když se na něčem zasekneš, získávat sebedůvěru a učit se při tom další věci, které při tom samy vyplynou (Git, API, atd.) a budeš potřebovat je pochopit.

V průběhu to někam nahrát a ukazovat lidem, ať si do toho klikají a počítají slepice. Třeba ti i napíšou, že to nefunguje dobře na mobilu, nebo něco poradí. Nemusí to být hotové, protože to nebude hotové nikdy. Kód nahraješ třeba na ten GitHub a do CV dáš na oboje odkaz - na kód i výsledek. Vyladíš CV a už v průběhu, co vylepšuješ kalkulačku na slepice, začneš CVčko posílat na juniorní nabídky, nebo sem napíšeš znovu a nabídneš se, ale už s něčím v ruce. Jak by vypadal tvůj status tady, kdyby k němu byl odkaz na kalkulačku slepic? 😃 Jako zní to vtipně, ale já si myslím, že bys pár nabídek práce už i dostal.

Přes vlastní projekt máš šanci kompenzovat neformální vzdělání, které máš díky kurzu, rozšířit si vzdělání o další praktické věci, upevnit svoje sebevědomí a mít v ruce něco, co ukážeš na pohovoru. Pokud se budeš v průběhu tvorby projektu ptát a chodit na srazy Frontendistů a networkovat, najdeš si už i nějaké kámoše v oboru, kteří ti poradí, nebo něco dohodí.

Já tohle lidem radím na https://junior.guru/handbook/ a v klubu https://junior.guru/club/, který jsem pro juniory vytvořil přesně za účelem toho, aby měli někoho po ruce a dostalo se jim pomoci. Z toho co pozoruju, toto je ten osvědčený postup, jak ve tvém případě (a případě Zuzka Procházková, která tu psala komentář) postupovat.

Automated Code Review for C#, C++, Java, CSS, JS, Go, Python, Ruby, TypeScript, Scala, CoffeeScript, Groovy, C, PHP, Dockerfile, Shell, YAML, Vue, HTML, Swift, Kotlin, PowerShell, Dart and R source code | CodeFactor
https://www.codefactor.io/

TODO přidat do projektu:

Me osobne prijde, ze nejlepsi zpusob jak "se to naucit" je najit si problem(y) ktery te tizi, a zkusit s tim neco udelat. Zacnes od drobnosti (ano, na zacatku je tezky zjistit, co je drobnost, ale to je soucast procesu uceni se) typu "rucne neco opakovane pisu do excelu, tak si na to udelam program", nebo "hraju onlinovku a zajima me jak optimalne utracet zdroje a posilat vojacky do bitvy" (hmm, existuje vubec jeste fenomen veic jako Duna online a tak? Citim se starej), pak si zkusis napsat treba jednoduchou skakacku, nebo neco co ti pomuze ucenim se treba ciziho jazyka. Zjistis ze existuje neco jako sit a internet, tak si zkusis k ty skakacce treba pripsat druhyho hrace ovladanyho po siti...

pythonanywhere
https://www.facebook.com/groups/ucimepython/permalink/2784405088331098/

Nápady na projekty
https://www.reddit.com/r/learnprogramming/comments/i2c0ud/keep_being_told_to_build_projects_but_dont_know/

Python projects for beginners
https://www.reddit.com/r/opensource/comments/i2bqyx/i_made_3_current_python_projects_for_beginners/

Python Projects with Source Code – Practice Top Projects in Python
https://data-flair.training/blogs/python-projects-with-source-code/

Čus - v dnešním videu vysvětluje jak začít s prgáním, má tam doporučení na nějaký tutoriály, to je celkem standardní, ale na konci se mi líbí jak zmiňuje svůj první programovací projekt, to mi občas chybí, něco hodně konkrétního. https://www.youtube.com/watch?v=khqIPspzh4A

https://www.practicepython.org/exercises/

Jak na projekty - jak zjistit zda jsem si nevymyslel blbost
https://discord.com/channels/769966886598737931/789045589869461536/911723281869053952

web scraping sandbox
http://toscrape.com/

https://www.vaclavaky.cz/
https://github.com/jandolezal/energy-mix
https://jakbude.herokuapp.com/

review
https://discord.com/channels/769966886598737931/1089219133968752650/1096078922724163615

https://dariagrudzien.com/posts/the-one-about-giving-and-receiving-feedback/

Jak sehnat jobíky
https://discord.com/channels/769966886598737931/769966887055392768/857539026194399232


PROC NEDELAT ESHOPY
Rozhodně ne jako byznys model pro začátečníka v oboru. Fungující byznys modely v tomto směru:
- Jsme velmi náročný eshop a máme vlastní inhouse tým lidí, kteří ho dělají (Alza, Mall, CZC…).
- Jsme velká firma, která dělá pouze systém pro eshopy a to prodáváme ostatním (Shopify, v česku ShopSys), ostatní u nás provoz eshopu de facto outsourcují.
- Jsme velká agentura s týmy lidí a jsme schopni vytvořit nebo dlouhodobě tvořit náročný eshop úplně na míru jako subdodavatel. (Vlastně nevím, jestli toto v roce 2021 opravdu ještě existuje?)
- Jsme malá agentura nebo profesionál na volné noze. Umím(e) dobře WordPress, WooCommerce, Shopify, apod., všechno zvládám(e) naklikat, nastavit, přizpůsobit, doplnit custom šablony, nainstalovat pluginy, propojit, atd.
Třeba https://www.digismoothie.com/ je česká firma o pár lidech, dělají eshopy na míru, ale dělají je tak, že použijou Shopify a postaví to na tom 🙂 Protože kdyby měli dělat všechno, tak je to za a) zbytečné, b) by se zbláznili z toho, jak by se nadřeli.
Čím menší jsi, tím spíš se živíš rozšiřováním polotovaru v podobě WordPressu apod., jinak je to naprosto nerentabilní. Neříkám, že jako freelancer neseženeš zakázku na zhotovení eshopu, ale takové zakázky považuju za spojení pomýleného zadavatele a pomýleného zhotovitele, protože jeden nebo druhý by měli tušit, že platit zhotovení eshopu od úplných základů je blbost a reálně to má smysl opravdu až pro level na úrovni Alza, Mall, CZC, atd.
https://www.facebook.com/groups/144621756262987/permalink/847188889339600/?comment_id=847716445953511&reply_comment_id=848019465923209


včera a předevčírem mi bublinou prolétlo tohle vlákno https://twitter.com/varjmes/status/1363607492765376513, kde se lidé vyjadřují k tomu, jestli dělají side projects nebo ne. spousta lidí programuje v práci, ve volném čase už ne, to myšlení o programátorovi, co programuje od rána do noci se už posunulo. časté jsou sebevzdělávací side projects - vyzkoušet si technologie apod. nebo "cesta je cíl" - hraní si s projektem, ale nikdy nedokončit.

tipy na projekty
https://www.theguardian.com/news/datablog/2012/apr/25/baby-names-data
https://www.theguardian.com/news/datablog/2012/feb/14/highstreet-clothes-size-chart

Charakter juniorniho projektu
https://discord.com/channels/769966886598737931/788826407412170752/861505874539446282

--- https://discord.com/channels/769966886598737931/789087476072710174/862669093898813440
Jako nástroj doporučim naprosto boží TablePlus. Velmi lightweight, velmi rychlý, relativně levný https://tableplus.com/
---


--- https://discord.com/channels/769966886598737931/789087476072710174/864057143056662528
Zrovna ve čtvrtek jsem se na to víc koukal a úvodní video z této stránky má asi 25 minut a dá slušnou představu 😀
https://docs.docker.com/get-started/
---


--- https://discord.com/channels/769966886598737931/789087476072710174/864484645721604097
V minulosti měli limit 18 hod./den. Teď mají 550 hod./měsíc, případně 1000 hod./měsíc, když ověříš svojí identitu platební kartou. Průměrný měsíc má 730 hod. (konstanta, kterou je dobré si pamatovat, když procházíš ceníky cloudových služeb), takže by to mělo být v pohodě, i když tam pošleš Pingdoma/UptimeRobota.

Zdroj: https://devcenter.heroku.com/articles/free-dyno-hours#free-dyno-hour-pool
---


--- https://discord.com/channels/769966886598737931/769966887055392768/859041142553051138
Z mých poznámek, kde se dají sehnat projekty na rozjezd:

- https://junior.guru/practice/#projects
- dobrovolničení pro https://cesko.digital/
- okopírovat existující věc (viz co píše <@!419662350874837003> nebo yablko tu https://www.linkedin.com/feed/update/urn:li:activity:6796762431776403456/, nebo úplně pecka je toto https://github.com/danistefanovic/build-your-own-x )
- zpracování dat o jménech https://www.theguardian.com/news/datablog/2012/apr/25/baby-names-data, o velikostech oblečení https://www.theguardian.com/news/datablog/2012/feb/14/highstreet-clothes-size-chart
- nějaká další inspirace tady https://www.codementor.io/projects
- https://data-flair.training/blogs/python-projects-with-source-code/
- https://automatetheboringstuff.com/
- tady je spousta dalších nápadů  https://www.reddit.com/r/learnprogramming/comments/i2c0ud/keep_being_told_to_build_projects_but_dont_know/

Nejlepší samozřejmě je, když k tomu máš nějaký osobní vztah, tzn. něco, co ti usnadní život nebo tě bude bavit, ať už je to program, který analyzuje výdaje na účtu, hypoteční kalkulačka na míru, procvičování počítání pro děti, osobní web o nějakém koníčku... Trochu už se to řešilo i tady https://discord.com/channels/769966886598737931/769966887055392768/817042156581421086
---


--- https://discord.com/channels/769966886598737931/788832177135026197/887690090162298930
Al Sweigart byl teď hostem podcastu https://realpython.com/podcasts/rpp/77/  právě kvůli té nové knížce. Docela inspirativní na poslech a obsah knihy je volně i online zde: https://inventwithpython.com/bigbookpython/
---


--- https://discord.com/channels/769966886598737931/789107031939481641/990100877064953856
Chceš ale vlastně vědět, jestli už je máš znalosti na to to zkusit, že?

Takovou informaci ti koukání na ta zadání bohužel nemusí dát, protože nevíš jak na to, co z toho zvládneš budou reagovat v té firmě. Někde mají hodně velká zadání, která „nejdou“ dodělat, chtějí třeba vidět, kam se dostaneš za dva dny a jak to bude vypadat apod.

Neříkám, že se z toho něco nedozvíš, ale dává mi větší smysl udělat si samostatný projekt (tedy ne takový, kterým tě provází nějaký tutorial) a pak to jít zkoušet už na ty pohovory.

Nevíš na co narazíš. Ten proces není nějak standardizovaný jako maturity, firmy jsou různý, dělaj různý věci a lidi v nich jsou taky různí, takže co stačí někde nemusí stačit jinde atd.

Samozřejmě jde i o to, jestli chceš/potřebuješ změnu co nejrychleji nebo je ti jedno, že budeš doma sedět třeba půl roku nebo rok „zbytečně“. Ono i kdybys řekl, že se „to chceš pořádně naučit“ tak si myslím, že po nějakých základech už se stejně rychleji budeš učit ve firmě už jen protože tomu budeš moci věnovat o dost víc času.
---


--- https://discord.com/channels/769966886598737931/769966887055392768/974343605437206548
Mít každý, i malý projekt, v gitu není špatný nápad, zvykat si s tím pracovat je důležité.

Jestli to pak chceš poslat i na GitHub je na tobě. Je to tvůj GitHub a je ok tam mít i nějaké rozpracované nebo banální věci veřejně.

Ale! Pokud hledáš první práci, mysli ale na to, že ten GitHub tě reprezentuje a pokud už se na něj bude někdo dívat, tak nebude mít moc času ani motivace to procházet všechno. Proto si myslím, že je lepší tam mít 2-5 tvých nejlepších projektů a ostatní skrýt, protože pokud se tam někdo dostane, může si udělat mylný dojem o tom, jak komplexní věci už zvládáš.
Jasně, odkážeš na ně z CV přímo, ale nikdy nevíš, kdo a jak se kam dostane…
---


--- https://discord.com/channels/769966886598737931/769966887055392768/974689373226422292
Čtu tvůj případ až teď a chtěl jsem poradit, ale nemám co 😎 Už tady všechno padlo:

1. Pokud už máš v něčem základy, šup a tvořit, vykašli se na další kurzy a učení teorie. Nejvíc se teď naučíš tím, že vytvoříš něco reálného, ať už to bude super mario nebo appka počasí se sluníčky a mráčky. Můžeš projet <#788826190692483082>, nebo můžeme zkusit něco vymyslet speciálně pro tebe. Je jedno co to bude, jako praxe a jako ukázka na pohovoru se počítá cokoliv, klidně webovka pro tvoje morče, pexeso s dinosaury, nebo kalkulačka pojištění. Začít s něčím malým a pak po kouskách vylepšovat, sdílet to tady, klidně rozpracované, nechávat si radit (to je odpověď <@971787978689089676> jak nevyhořet na vlastním projektu <:thisisfine:900831851361501214> ).

2. Dva pohovory jsou málo a motivoval bych tě, ať zkoušíš dál, ale pokud nemáš projekt, tak to dělat nebudu. Vytvoř si projekt, vylepšuj ho postupně, ukazuj ho pak jako praxi, kterou máš. Nech si vyladit CV podle https://junior.guru/handbook/cv/ v <#839059491432431616>. A potom až selže desátý pohovor, pojďme se zamyslet nad tím, kde je problém.

Dík <@652142810291765248>, <@971787978689089676>, <@814084764838658111>, <@866239781313708045> a dalším, že jste už <@567592397647773706> tak pěkně poradili <:meowthumbsup:842730599906279494>
---


--- https://discord.com/channels/769966886598737931/788832177135026197/969844861714984980
Narazila jsem na toto, super jako inspirace na projekty: https://copyassignment.com/
---


--- https://discord.com/channels/769966886598737931/811910392786845737/966807181519372338
<:react:842332165822742539> React-like framework v <:python:842331892091322389> Pythonu pro terminál 🙂 Třeba se to bude někomu hodit na projekt: https://github.com/Textualize/textual
---


--- https://discord.com/channels/769966886598737931/788832177135026197/965331497106165800
**Hromada zdrojů pro ruzné UI, stock media, Icons, Favicons, tools a miliarda dalšího!**
_Doporučuji si to připíchnout někde do záložek :-)_

_Velmi často aktualizované a přidávané další užitečné zdroje._

- https://github.com/bradtraversy/design-resources-for-developers#favicons
---


--- https://discord.com/channels/769966886598737931/769966887055392768/965219975793098842
Tip na projekt: když nevíte, co nového vytvořit, zkuste místo toho něco zkopírovat 🙂 https://dev.to/eknoor4197/i-built-a-devto-clone-from-scratch-including-the-api-56k9
To mi připomíná, že někdo takhle před lety přinesl na pohovor do Seznamu vlastnoručně vytvořenou kopii Seznam homepage. Prý byl úspěšný 🙂 Dává to smysl i z toho pohledu, že pak mate hromadu společných témat k diskuzi.
---


--- https://discord.com/channels/769966886598737931/769966887055392768/907183575244345355
https://www.reddit.com/r/learnprogramming/comments/2a9ygh/1000_beginner_programming_projects_xpost/
---


--- https://discord.com/channels/769966886598737931/811910782664704040/1085161148330029156
Třeba má někdo detailnější poznámky, ale alespoň body ze včerejšího povídání tady v klubovně.
Nebudu to ale vysvětlovat ani rozepisovat.

**Časté chyby začátečníků, když píšou HTML a CSS**
– nekódují podle návrhu, přestože to je většina práce pro většinu těch, co CSS tvoří
– kódují podle návrhu v PNG/JPG apod. místo Figmy (případně XD nebo Sketche)
– berou návrh příliš doslova (vlevo 39px, vpravo 40px…)
– berou návrh od oka: nedávají hodnoty z Figmy
– kopírují „CSS“ z Figmy, přestože 98 % těch hodnot nemá správné jednotky, případně nejsou dostatečné (font-family)
– nastavují `width` častěji než je nutno a ještě pevnými jednotkami (nevyužívají % apod.)
– nastavují `height`, které není potřeba nastavovat skoro nikdy – výška elementů vzniká z velikosti obsahu (často velikosti písma, line-height atd.) jeho paddingů, marginů, borderů atd. ne tak, že nastaví `height`
– zbytečně zaokrouhlují, i 5 desetinných míst je v pořádku
– používají padding tam, kde by stačil margin nebo dokonce gap
– nevyužívají dědičnost vlastností pro nastavení vlastností textu v celé stránce/webu
– jejich css selektory kopírují strukturu v HTML např. `body header p { … }` apod.
– používají v selektorech ID (stačí elementy, třídy + pseudoelementy, pseudotřídy atd.)
– využívají proměnné (custom properties v CSS nebo proměnné v Sassu) tam, kde nemají moc smysl
– používají _CSS reset_, který „smaže“ přiliš mnoho výchozích vlastností a musí je pak znovu nastavovat, spousta práce navíc
– mají „špatně“ nevalidní kód, nevyužívají validátor („dobře“ nevalidní kód je takový, který nic nerozbije, validita sama o sobě velkou hodnotu nemá)
– nekomentují si kód a za pár dní neví proč tam je to, co tam je

A dvě věci, které jsem myslím nezmínil.
– v Sassu příliš vnořují, špatně se to čte
– neporovnávají návrh s výsledkem v prohlížeči
– netestují ve všech možných šířkách (a případně i výškách).
---


--- https://discord.com/channels/769966886598737931/811910782664704040/1077904819328651344
V <#1075155024965025792> <@1016967149371277323> otevřela téma webu jako portfolia frontendisty.
Nemyslím si, že je nutné ho mít, ale mají ho všichni klienti <:coreskill:929824061071192084> CoreSkillu, kteří s námi procházejí cestou z „umím málo“ do „mám první práci“.

Proč? Protože je to výborné zadání na jednoduchý statický web, kterým začínáme a je méně motivující dělat nějaký cvičný, který se pak zahodí, než tohle, co má nějakej smysl a navíc obsah je jasnej. Taky je časem větší motivace ho upravovat a vylepšovat.
---


--- https://discord.com/channels/769966886598737931/1069298711202644051/1072093745635405924
Já vím, jak jsi to myslel, ale trochu se v tom pošťourám 🙂
> použitelná pro prezentaci mých dovedností, když odkaz posílám při odpovídání na nabízené pracovní pozice
Něco jsi vytvořil a je to odrazem tvých znalostí. Použitelné je tedy cokoliv, co zrovna vytvoříš, jelikož to dává firmě informaci o tom, co zhruba tě budou potřebovat doučit. (Slovo „zrovna” je důležité, protože neaktualizovaná věc stará půl roku, rok, by už asi tvé současné znalosti neodrážela.) Neexistuje žádná laťka projektu, za kterou když se dostaneš, je to použitelné. Můžeme vychytat nějaké chybky, které dělá každý začátečník. Ty si je opravíš a tím vylepšíš své znalosti. Takže se nestane opět nic jiného, než že projekt zrcadlí tvé znalosti. Prostě tvoř, vylepšuj a sem tam to zkus poslat na nějaké firmy s CVčkem. Pak ta otázka nestojí, jestli je to dost dobré, ale jestli si ta konkrétní firma vyhodnotí, že na ty konkrétní úkoly, na které tě potřebuje, tě se zvými zdroji zvládne zaučit z té úrovně, kterou si domyslí podle tvého projektu.
---


--- https://discord.com/channels/769966886598737931/1067513448168181850/1067758031472967750
hele mám 6 projektů
---


--- https://discord.com/channels/769966886598737931/1054825337160212571/1057998994980221040
<@668226181769986078> Myslím si, že i jinak proaktivní jedinci můžou mít s projekty problém, ať už se bavíme o jejich vymýšlení nebo realizaci. Společný projekt podle mě člověka více "nakopne", vyzkouší si (byť třeba v hodně omezené míře) spolupracovat s někým jiným a může se u toho naučit věci, se kterými se u samostatného projektu setkat nemusí 🙂 Může se tak třeba podílet i na něčem větším, co by jinak sám nezvládl. Někdo by to taky mohl vidět jako hybrida vlastního projektu a přispívání do něčeho open-source 🤷‍♂️

Moje představa zjednodušeně v bodech ⬇️ ⬇️ ⬇️ Hlavní jsou první dva body, další dva už jsou jen takové doplňky.
---


--- https://discord.com/channels/769966886598737931/1049695821962170498/1049697487209910272
Zkusím ti to dilema vyřešit: pokud se hlásíš na frontendové pozice, tak to musíš mít 100%, pokud ne, tak nepotřebuješ ani web.
---


--- https://discord.com/channels/769966886598737931/983615979881906197/983620893458702356
Pokud bys neměl projekt, tak na https://www.frontendmentor.io/ jsou zadání včetně návrhů.

Tenhle je zadarmo https://www.frontendmentor.io/challenges/space-tourism-multipage-website-gRWj1URZ3 (spíš webovka, ale můžeš ji udělat v Reactu, že jo…)

Jsou tam i víc JS věci typu pexeso https://www.frontendmentor.io/challenges/memory-game-vse4WFPvM a další
https://www.frontendmentor.io/challenges?difficulties=5,4&languages=HTML|CSS|JS

**Pokud bys dělal něco jinýho než *Space tourism*, tak si zaplať těch 12 dolarů na 1 měsíc a stáhni si zadání včetně souboru Figma, což je grafický program ve kterým dělá návrhy webů většina designérů. Je zadarmo (pro tvoje účely) a měl bys umět z něj vytáhnout jak co má přesně vypadat.**
---


--- https://discord.com/channels/769966886598737931/1113873887445397564/1113931127531520050
Junior guru je skvělá příručka. Nauč se základy , udělej alespoň jeden velkej projekt, vymazli github -cv. Následoval jsem tyhle kroky a fungovalo to. Ale nemůžeš vynechat ten projekt. Musíš si prostě tim ušpinit ruce a zaměstnat hlavu. Když si vymyslíš svůj, bude tě to více bavit. Ale musíš vytvářet. A googlit ,jak na ty dílči kroky, ne procházet něčí osnovu. Protože to tě nenutí tolik přemýšlet. člověk  nesmí skončit u piškvorek z návodu, musí přidat něco svého co ho donutí se posunout. A bude to nepříjemné, když se zasekneě. Stalo se mi to hodněkrát. Celý den jsem strávil na tom , jak udělat jednu věc, kterou senior napíše za  20 minut.  Bylo to peklo, říkal jsem si , tohle už je můj limit.  Ale pak jsem to vždy nějak napsal a fungovalo to. Po třech měsích v práci se stydím, za svůj projekt, se kterým jsem se o tu práci ucházel. Ale podle mě bylo to co zaměstnavatele přimělo mě vyzkoušet. To , že se pokusím udělat to co jsem si dal za úkol i když to je náročné. Protože ten projekt je  pro začátečníka podle mě náročnější než kurz.  Ale zábavnější. A určitě tě vědomí toho, že si to dokázal vyrobit, naplní víc, než certifikát.
Nechci hodnotit výše zmíněné kurzy,  určitě mohou pomoci získat znalosti. Ale upřímně si polož otázku, jestli ty nepotřebuješ jen aplikovat a procvičit to, co už si minimálně jednou slyšel. Fandím ti. Máš výdrž a když nepolevíš, tak se ti ten cíl splní. Sleduji tě už dlouho a opravdu držím palce. Kdyby si měl pocit, že se chceš na něco z mé cesty zeptat, klidně napiš. Ale opravdu, zkus jít za tu hranu, toho, co se ti třeba nechce..tam tě totiž čeká to ,co chceš 🙂
---


--- https://discord.com/channels/769966886598737931/788826190692483082/1119196194686648410
Pro ilustraci, tady je screenshot z plánovací tabulky, jak probíhal vývoj tohoto projektu.
---


---
https://neal.fun/space-elevator/ a dalsi na https://neal.fun/ jako inspirace
---


#} -->
