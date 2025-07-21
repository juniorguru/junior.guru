---
title: Projekty
emoji: 🏗️
stages: [creating]
description: Pokud se učíš programovat, práce na vlastních projektech je nejdůležitější věc na tvé cestě
template: main_handbook.html
---

{% from 'macros.html' import blockquote_avatar, note with context %}

# Projekty jako první praxe

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }} Kapitola se teprve připravuje.
{% endcall %}

Nic tě nenaučí tolik, jako když si zkusíš něco samostatně vyrobit. Říká se tomu [projektové učení](https://cs.wikipedia.org/wiki/Projektov%C3%A9_u%C4%8Den%C3%AD). Nejlepší je vymyslet si něco vlastního a řešení procházet s [mentorem](mentoring.md). Inspirace na projekt se nejlépe hledá přímo okolo tebe:

*   Jednoduchá hra, např. piškvorky nebo [had](https://naucse.python.cz/2018/snake-brno/),
*   automatizace něčeho, co teď na počítači musíš dělat ručně (mrkni na [tuto knihu](https://automatetheboringstuff.com)),
*   program na procvičování příkladů nebo slovíček pro děti do školy,
*   [osobní webová stránka](candidate.md#osobni-web-a-blog).

Pokud vlastní nápad nepřichází a mentor není po ruce, můžeš zkusit [hackathon](collaboration.md) nebo [open source](collaboration.md).

{% call blockquote_avatar(
  'Junioři si často udělají kurz, certifikaci, ale potom už tu znalost neprocvičují. A to je strašná škoda, protože ji do pár měsíců zapomenou. Lepší méně kurzů, ale potom začít praktikovat a něco si vytvořit. Nákupní seznam, jednoduchého bota, malou aplikaci.',
  'jiri-psotka.jpg',
  'Jiří Psotka'
) %}
  Jiří Psotka, recruiter v [Red Hatu](https://www.redhat.com/en/jobs) v [prvním dílu podcastu junior.guru](../podcast/1.jinja)
{% endcall %}

Na inzerát bytu k pronájmu, u kterého nejsou fotky, nikdo odpovídat nebude. Stejně je to i s kandidáty. **Potřebuješ ukázat, že umíš něco vyrobit, dotáhnout do konce, že máš na něčem otestované základní zkušenosti z kurzů a knížek.** K tomu slouží projekty. Pokud nemáš vysokou školu s IT zaměřením, kompenzuješ svými projekty i chybějící vzdělání. Snažíš se jimi říct: „Sice nemám školu, ale koukejte, když dokážu vytvořit toto, tak je to asi jedno, ne?“

Říká se, že kód na GitHubu je u programátorů stejně důležitý, ne-li důležitější, než životopis. Není to tak úplně pravda. U zkušených profesionálů je to ve skutečnosti [velmi špatné měřítko dovedností](https://web.archive.org/web/20240329194129/https://www.benfrederickson.com/github-wont-help-with-hiring/). Náboráři se na GitHub nedívají, maximálně jej přepošlou programátorům ve firmě. Přijímací procesy mají většinou i jiný způsob, jak si ověřit tvé znalosti, např. domácí úkol nebo test. **Zajímavý projekt s veřejným kódem ti ale může pomoci přijímací proces doplnit nebo přeskočit.** Dokazuje totiž, že umíš něco vytvořit, že umíš s Gitem, a tví budoucí kolegové si mohou rovnou omrknout tvůj kód. Člověk s projekty skoro jistě dostane přednost před někým, kdo nemá co ukázat, zvlášť pokud ani jeden nebudou mít formální vzdělání v oboru.

Konkrétně GitHub s tím ale nesouvisí. Stejný efekt má, pokud kód vystavíš na BitBucket nebo pošleš jako přílohu v e-mailu. Když někdo říká, že „máš mít GitHub“, myslí tím hlavně to, že máš mít prokazatelnou praxi na projektech. GitHub je akorát příhodné místo, kam všechny své projekty a pokusy nahrávat. **Nahrávej tam vše a nestyď se za to,** ať už jsou to jen řešení [úloh z Codewars](practice.md) nebo něco většího, třeba [tvůj osobní web](candidate.md#osobni-web-a-blog). Nikdo od tebe neočekává skládání symfonií, potřebují ale mít aspoň trochu realistickou představu, jak zvládáš základní akordy. Budou díky tomu vědět, co tě mají naučit.

Pokud se za nějaký starý kód vyloženě stydíš, můžeš repozitář s ním [archivovat](https://docs.github.com/en/repositories/archiving-a-github-repository/archiving-repositories). Jestliže se chceš nějakými repozitáři pochlubit na svém profilu, můžeš si je tam [přišpendlit](https://github.blog/2016-06-16-pin-repositories-to-your-github-profile/). Výhodou je, že přišpendlit jde i cizí repozitáře, do kterých pouze přispíváš.

{% call blockquote_avatar(
  'Na pohovoru mě nezajímá, co kdo vystudoval, ale jak přemýšlí a jaké má vlastní projekty. Nemusí být nijak světoborné, je to však praxe, kterou ani čerstvý inženýr často nemá.',
  'josef-skladanka.jpg',
  'Josef Skládanka'
) %}
  Josef Skládanka, profesionální programátor
{% endcall %}

Máš-li za sebou nějakou vysokou školu z oboru, ukaž svou bakalářku nebo diplomku. Je to něco, co je výsledkem tvé dlouhodobé, intenzivní práce. Pochlub se s tím!

<!-- {#

Bez projektů jde dnes tvoje CVčko přímo do koše. 200 lidí na jeden inzerát. jak vynikneš?

https://dariagrudzien.com/posts/the-one-about-your-github-account/

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


--- https://discord.com/channels/769966886598737931/811910782664704040/1136353788438007968
Zajímavé věci se ženou do CSS. Líbí se mi, jak si s tím vším borec hraje ❤️ Prostě jen proto, že může. Možná je to inspirace i pro juniory - až budete pracovat, tak budete muset dělat na užitečných věcech. Ale ve svých projektech si můžete hrát 😄 https://slideslive.com/39000629/supercharge-your-skills-with-creative-coding
---


--- https://discord.com/channels/769966886598737931/811910392786845737/1127897051741560883
Přivedlo mě to i na projekt refurb, který umí „modernizovat“ kód: https://github.com/dosisod/refurb Umím si představit, že by to šlo pustit na kódu nováčka v Pythonu a že by to umělo doporučit, jak nějaké věci jde s novějšími verzemi Pythonu udělat jednodušeji nebo chytřeji.
---


--- https://discord.com/channels/769966886598737931/811910392786845737/1127896694323949619
Zajímavý článek o tom, jak použít GitHub API a najít zajímavé nové projekty v Pythonu za účelem toho, že by do nich mohl člověk třeba i přispět v rámci open source: https://mostlypython.substack.com/p/exploring-recent-python-repositories
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1196419372537876502
Často tu někdo řeší/řešil **výběr/vypracování prvního projektu**. Můžu doporučit tento článek: https://blog.boot.dev/education/building-your-first-coding-project/ Jsou tam samozřejmě zmíněně věci týkající se přímo dané vzdělávací platformy a zaměření (backend), ale i tak si myslím, že jde o dobré čtení 🙂
---


https://nedbatchelder.com/text/kindling.html


--- https://discord.com/channels/769966886598737931/1202963994420449380/1203002747532877874
Souhlasim s tim co bylo receno, ostatne se ti bude i lepe povidat o projektu, ktery je ti blizsi a ktery pouzivas. Dulezite take je, v jakem je ten projekt stavu - velky dojem, alespon na me, udela treba README kde je popsane jak projekt spustit, prilozene testy, nejaka standardizace atd proste ty veci ktere jsou casto vnimane jako "navic" a pritom jsou tolik dulezite pro realnou praci v pythonu. Zaroven jsou to ty veci, ktere cloveka bavi kdyz dela na projektu co je mu blizky a bavi ho si to vysperkovavat.

Par bodu na ktere se doporucuju podivat (a bez kterych si nedokazu predstavit realny projekt v jakekoliv firme):

* `README.md` s popisem co a jak to dela, jak to nainstalovat a rozjet
* `pyproject.toml` (nebo `setup.py`, `setup.cfg`, konkretni implementace je vcelku jedno) se zavislostmi (vcetne verzi)
* `pre-commit` s beznymi hooky jako `black` nebo `isort` ci `flake8`
* testy + instrukce jak je pustit v README
* Continuous Integration (CI) bohate staci github actions
* `Dockerfile` ci rovnou `docker-compose.yaml` ktery pusti cloveku demo
* screenshot (pokud je to relevantni) v README

Neni potreba ani jedna z tech veci a asi nikdo neceka, ze takovy projekt bude mit vsechny, ale kazda pomuze. Vzdy radsi uvidim jeden projekt ktery ma alespon par techto veci nez 4x rozpracovany tutorial.
---


--- https://discord.com/channels/769966886598737931/1206299260153237544/1206341306700529715
Souhlas s ostatními a trochu to rozepíšu:
- **více autorů kódu?** čtu: paráda umí nějak spolupracovat na kódu a když budu chtít vidět, co dělala ona, není to moc problém i když pokud to bylo nějak vymezené (třeba A dělal frontend a B dělala backend), tak bych to ještě rovnou zmínil v README
- v extrému si umím i představit, že na větším „cizím“ projektu někdo udělá pár pull requestů, tak odkáže přímo na ně a ne nutně na celý projekt
- **reviews?** čtu: super, někdo se už tomu začátečníkovi věnoval, není to čistej samouk, kterej má většinou hrozný díry
- i když je to projekt toho jednoho člověka nebo není, tak bych se stejně ptal, jak to funguje, co tam bylo těžký atd. jeden člověk dneska může, klidně i sám, spoustu věcí opsat nebo si nechat vygenerovat AI, aniž by jim příliš rozuměl.
---


Don't contribute to open source
https://www.youtube.com/watch?v=5nY_cy8zcO4


--- https://discord.com/channels/769966886598737931/1076121659976720494/1212283617808486411
Kdo obcas koukne na muj github, tak si muze vsimnout, ze tam pribyvaji ruzne casti kodu, nove tridy, metody a tak.
S <@708265650619154521> jsme udelali ohromny pokrok (alespon z me strany) a navic se na tom hodne ucim. Velky plus je to, ze mi Dale pomaha hodne 🙂
Jde to dobrym smerem, momentalne pracujeme na vyberu hry. Je to trochu tvrdsi orisek pro me, ale na druhou stranu uz vim +- co a jak. Chybi mi jeste ta zkusenost, kterou ma Dale.
Dale mi vcera odpoledne poslal zajimavou a velmi motivujici zpravu, cituji: ,,Neboj se experimentovat, neboj se
udelat rozhodnuti, vzdycky to muzes prepsat, zvykej si na to. Udelat "spravne" rozhodnuti na zacatku je temer nemozne.”

Toto me hodne namotivovalo 🙂
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1212371552457330719
A nemá smysl se tím, především v případě domácího projektu, nějak trápit. Mám co mám. Ukážu, co mám. Jasně, za půl roku můžu třeba ukázat víc, ale to je nekonečný závod. Je lepší nechat posoudit druhou stranu, jestli je to pro ně dost, než se upinat na to, ze něco musí mít nějakou laťku, aby to bylo “dokončené” 🤷‍♂️
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1212356957240033331
> My advice to a beginner dev struggling with their side-projects would be to always make sure that you're doing them for yourself, and for the right reasons. Instead of approaching your first project purely as a means to make it big or to impress recruiters, see it firstly as a means to learn and explore what's possible.
https://robbowen.digital/wrote-about/abandoned-side-projects/
---


--- https://discord.com/channels/769966886598737931/1215708215527088218/1217120094392553503
Přijde mi strašně super, že když něco vytvoříš, tak si z toho uděláš video, aby to šlo ukázat. Odkaz na takovou věc se pak dá dát i do CVčka a je to mnohem efektnější, než ukazovat kód. Je jasný, že kód je to důležité, ale holt jsme jenom lidi a když se to dobře odprezentuje, vždycky to zaujme víc. Kéž by tohle umělo víc juniorů.
---


Souhlasím, že dělat nějaké projekty navíc po večerech by nemělo být nutnou podmínkou, ale u juniorů to tak bohužel je, a to především u těch, kteří usilují o career switch a musí tím kompenzovat chybějící formální vzdělání nebo prostě jakoukoliv jinou praxi.


Zadání práce na doma mi dává smysl jen pokud není kód, nad kterým se můžu s kandidátem bavit a když ten kód je, ideálně bez práce dostupný na GitHubu, tak nemá cenu je zadávat.
A na pohovoru se budu (kromě samotné náplně práce) bavit právě o tom kódu… Ne každý si může dovolit mít projekty, ale pořád je to mnohem víc lidí, než si může dovolit studovat VŠ.


Když jsme u toho, tak sice říkáme GitHub a veřejně, ale ve skutečnosti prostě chci vidět kód a pokud je vystavený takhle, tak je to prostě pohodlné, nic víc.


Ber to tak, že na GitHub ti nikdo nekouká, i když je to veřejné, dokud mu k tomu nedáš hodně dobrý důvod. Těch profilů je tam milion a dá velkou práci způsobit, aby se tam někdo na něco koukal, když chceš 🙂


@Honza Javorek jj, o tom vím, díky. Používám ještě popis repositáře, aby na první pohled bylo jasné, že jsem nepsala kód, ale odněkud převzala.

K ostatním projektům doplň informace přímo na GitHubu i do README.md a někam je nasaď, statické jdou přímo na GitHubu.

GitHub mám, ale projektov nemám veľa, sú skôr menšie a momentálne pracujem na jednom rozsiahlom, na ktorom to celé sebaprezentovanie tak nejak staviam. Tiež som si vzala k srdcu rady ohľadom GitHubu a pomaly dokončujem popisy a Readme ku všetkým projektom, takže keď to budem mať hotové, tak to určite zazdieľam do


![👍](https://discord.com/assets/7a934d8b65db3219592b.svg) **dobrý nápad**: Poslat se žádostí o práci odkaz na svůj veřejný projekt na GitHubu
![👎](https://discord.com/assets/cac0458c05c01c5f03c1.svg) **špatný nápad**: Poslat se žádostí o práci odkaz na svůj veřejný projekt na GitHubu, kam jste commitli a pushli také složky jako `__pycache__`, `node_modules` a další a taky přístupy na ssh, k databázi a k emailu, které ta aplikace využívá.
- Tak poprvé se to dá pochopit, když se to stane podruhé, tak už je to docela špatný (a smutný).
- Github se to trochu snaží hlídat, ale samozřejmě to není stoprocentní: [https://docs.github.com/en/code-security/secret-security/about-secret-scanning](https://docs.github.com/en/code-security/secret-security/about-secret-scanning "https://docs.github.com/en/code-security/secret-security/about-secret-scanning")
- Jasně. Ty složky, co jsem jmenoval, se do verzovacího systému nepřidávají, protože to nemá smysl. Je to spíš znak toho, že ti jako samoukovi a začátečníkovi něco uteklo.
- Ostatně to druhý taky, ale přeci jen to je o dost větší chyba, protože jde o bezpečnost.
- Přístupy = heslo + jméno.
- SSH je vlastně přístup na nějaký server [https://searchsecurity.techtarget.com/definition/Secure-Shell](https://searchsecurity.techtarget.com/definition/Secure-Shell "https://searchsecurity.techtarget.com/definition/Secure-Shell")
- Databázi taky nechceš mít veřejně přístupnou a ani nějaký e-mailový účet.
- Jsou místa v konfiguracích nebo prostě v kódu, kde je potřeba ty přístupy mít, to je jasný, ale řeší se to tak, aby nebyly přímo v kódu a tedy v repozitáři i kdyby nebyl veřejný.



- název repozitáře `python-012021.` mě triggeruje hned dvakrát - ta tečka na konci, a to (asi) datum, které se dá vykládat třemi způsoby ![🙂](https://discord.com/assets/6e72cca8dcf91e01fac8.svg)
- `.DS_Store` má asi být v `.gitignore`, ale aspoň je vidět, že máš macOS ![🙂](https://discord.com/assets/6e72cca8dcf91e01fac8.svg) (např. v [https://github.com/MartinaHytychova/martinahytychova.github.io](https://github.com/MartinaHytychova/martinahytychova.github.io "https://github.com/MartinaHytychova/martinahytychova.github.io"))
- tohle asi taky mělo být v gitignore? [https://github.com/MartinaHytychova/CSharp_Calculator/tree/master/obj](https://github.com/MartinaHytychova/CSharp_Calculator/tree/master/obj "https://github.com/MartinaHytychova/CSharp_Calculator/tree/master/obj") a adresář bin nejspíš taky
- hele, apiKey ![🙂](https://discord.com/assets/6e72cca8dcf91e01fac8.svg) [https://github.com/MartinaHytychova/pet-finder/blob/main/src/db.js](https://github.com/MartinaHytychova/pet-finder/blob/main/src/db.js "https://github.com/MartinaHytychova/pet-finder/blob/main/src/db.js")
- jinak ten pet-finder vypadá už aspoň docela netriviálně ![👍](https://discord.com/assets/7a934d8b65db3219592b.svg) ![🙂](https://discord.com/assets/6e72cca8dcf91e01fac8.svg) škoda, že má generické readme. A dokonce i nasazené to je ![👍](https://discord.com/assets/7a934d8b65db3219592b.svg) [https://pet-finder.netlify.app/#/](https://pet-finder.netlify.app/#/ "https://pet-finder.netlify.app/#/")
- Pokud zakladate novy repozitar na GitHubu, muzete rovnou pridat .gitignore pro dany jazyk/ide. Pripadne se da pro vetsinu jazyku stahnout tady - [https://github.com/github/gitignore](https://github.com/github/gitignore "https://github.com/github/gitignore")
- S těmi tokeny apod. doporucuju projít si [https://12factor.net/](https://12factor.net/ "https://12factor.net/"), to je v podstatě standard, jak se dnes delaji webové aplikace z hlediska konfigurace, nasazováni, apod. Mnoho lidi by řeklo ze to je takový nepsany, obecně prijimany standard, ale on není nepsany, je popsaný tady na tom webu ![😀](https://discord.com/assets/503f3c92fca30bb4275f.svg) Především [https://12factor.net/config](https://12factor.net/config "https://12factor.net/config") se konkrétně zabývá tím jak dělat konfiguraci tak, aby se nemusel nějaký token nebo heslo commitnout do gitu, kde to uvidí všichni
- gitignore.io




Bylo by fajn v tom CV k MealPalu dát nějaký testovací login. Ne každému se bude chtít registrovat, aby viděl funkcionalitu uvnitř a venku jí tolik k vidění není a to je velká škoda!

Vše, co jsem nenapsal mi přijde fakt fajn 👍 , máš u všeho na GH popisky, readme (u jednoho ne, ale to je nějakej cvičnej Czechitas projektík, možná bych ho schoval), url atd. Máš i pořádnej velkej projekt a tak dále. Držím palce.


Jinak pokud bys chtěl ještě víc zdůraznit, že https://github.com/spaze/libini-djgpp je jen pro archivní účely, můžeš teď na GH repo přímo označit jako archivované, což dá návštěvníkům na první pohled jasnou message. Je to repo > settings > dole dole dole danger zone > Archive this repository


https://www.drmaciver.com/2015/04/its-ok-for-your-open-source-library-to-be-a-bit-shitty/


Taky mrkni na .gitignore a přidej si tam složku .idea.


Mrkni na https://www.makeareadme.com/ jsou tam dobré tipy na to, jak a co napsat.

Taky využij funkce GitHubu a doplň popisy těch projektů. Radši dobrou češtinou než špatnou angličtinou.

Nicméně v kódu je asi lepší angličtina pro názvy proměnných i když upřímně je to to poslední, co bych při zkoumání toho, jak někdo přemýšlí řešil. To už by mě víc zajímalo, jestli ty názvy opravdu popisují to, co obsahují nebo co funkce dělají…



Těm projektům na Githubu chybí třeba popis, co to vlastně je, jak to funguje, a odkaz na nasazenou verzi, ale asi na tom ještě pracuješ. Bude se to hodit, až/pokud se těmito projekty a svým Github profilem budeš prezentovat při hledání práce.

gitleaks projdou kod a oznami vsechno co vypada jako token atd.



dobrá, upravím to podle toho co jste mi napsal, zdá se to celkem i rozumné, a jsem rád za nějakou zpětnou vazbu od někoho kdo se tomu aktivně věnuje, mohl bych se ještě zeptat jak by měl vypadat ideálně github? většina projektu mam převážně ve azure devops, a jen nějaké vybrané jsem si dal do nového github učtu https://github.com/LukePavelka

jedno zadaní od firmy, které jsem vypracoval, jsem si dal taky na github, kritickou chybu nejspiš vidim v tom že jsem udělal jeden velky commit až pak když jsem to měl skoro hotové



Líbí se mi, že projekty maji README, ze kterého jde pochopit, o co jde. Kód samotný úplně neposoudím, ale jinak mi to přijde v pohodě. Jestli je někde jeden velký commit, s tím nic nenaděláš, pokud by se tě na to ptali u pohovoru, tak řekneš, že si to uvědomuješ a že se holt učíš, tak už víš, že se to má dělat jinak. Ale ani jeden velký commit, pokud je na začátku projektu, není úplně chyba. Typicky „initial commit“ v repozitáři může být dost velký, protože před tím, než byl kód Open Source na GitHubu, mohl vzniknout někde vedle a tímto commitem se vše teprve dostalo do repozitáře.



Vpravo nahoře se dá u jednotlivých projektů kdyžtak dopsat jedna větička o projektu a přidat případně odkaz, pokud projekt třeba jede někde spuštěný a má svou webovku.



Zaujalo mě, že některé projekty mají dva contributors, podle jména si vyvozuji, že máš dva GitHub účty. Je pro to nějaký důvod? Přijde mi škoda dělit svou aktivitu na dva účty, pokud ten jeden nepoužíváš na nějakou podvratnou činnost nebo jej nechceš spojovat s vážnou prací (ale jak vidíš, tím že tam má commity, tak se na něj stejně doklikám). Pokud jeden účet nepoužíváš, repozitáře lze přesunout mezi uživateli. Commity na účty GitHub páruje podle e-mailů, takže stačí starý účet smazat a e-mail, pod kterým jsou commity vytvořeny, si přidat k tomu účtu, který chceš používat (GitHub účet může být spárovaný na více e-mailů).


A k těm si vyplň **dobře** 1) popis, abych rychle zjistil o co jde už z přehledu a url přímo na GitHubu, abych se mohl podívat na běžící web, pokud to jde (k tomu ne moc podstatná věc, [https://pet-finder.netlify.app/#/](https://pet-finder.netlify.app/#/ "https://pet-finder.netlify.app/#/") -> [https://pet-finder.netlify.app/](https://pet-finder.netlify.app/ "https://pet-finder.netlify.app/")) 2) readme soubor, nějaký rady na [https://www.makeareadme.com/](https://www.makeareadme.com/ "https://www.makeareadme.com/") abych jako zkoumač toho, co umíš a) snadno a bez práce zjistil o co jde detailněji a třeba jaký technologie / knihovny atd. si tam použila atd. b) uměl si to v případě zájmu snadno rozjet a otestovat sám c) viděl, že dokumentuješ

U každého projektu minimálně do README napsat co to je (mapa útulků), v čem to je vyrobené (React...), proč jsi to vyrobila (dlouhodobě urdžovaný hobby projekt / jednorázové cvičení na kurzu / nějaká cvičení / ...).

A pokud si jsi vědoma nedostatků na tom projektu, lze je do README napsat a přiznat taky: třeba že víš, že tam nejsou testy nebo že blbne přihlašování, ale už se projektu intenzivně nevěnuješ, tak to tak necháváš. Nebo že se k tomu zas někdy chceš vrátit, až bude čas, a napsat, co se tam chystáš vylepšit (todo / roadmap)


dokumentace: Začal bych minimalistickou verzí, kterou zvládneš třeba za hodinu nebo méně. Prostě si dej časový limit a stihni to. Rozepsat to případně můžeš potom.

Já bych asi nějaký opravdu „odpadní“ nebo interní, dočasný apod. radši dal private, míň práce než psát u každýho, že to je jen cosi, co není nic moc a není to udržovaný, což si stejně spousta lidí nepřečte a nedá se vyloučit, že na to nějak nenarazí.


Za sebe: do repositářů, které pošleš, budu koukat na kód a jak pracuješ s gitem. Do těch ostatní nahlédnu také, ale bude mě zajímat spíš jejich historie, než kód: jestli je to tvůj kód, nebo cizí, jak jsou velké commity a jaké píšeš commit messages. To totiž vypovídá o tom, jaké máš návyky: pokud jsou tam commit messages ve stylu "asdfasdf", kde jsou navíc soubory, které spolu očividně nesouvisí, tak to nejspíš značí, nepostupuješ dostatečně organizovaně a ve stresu přestaneš dodržovat konvence. Ten, kdo dokáže udržovat smysluplnou historii vždy, má určitě plus.
Já na tohle zkusím napsat svůj pohled. Dělám většinou technické hodnocení kandidátů a většinou mám max 15-20 minut, abych se dozvěděl co nejvíc o kandidátovi před ústním pohovorem. Takže pokud mám v ruce konkrétní repo, začnu tím. Pak se samozřejmě podívám i zběžně na ostatní projekty. Za mě je lepší, že vidím nějakou aktivitu, i když to jsou školní projekty. Ale rozhodně chlubit se čistě školními projekty nedoporučuji (jsou zde i výjimky). V kódu se většinou dívám jak ten člověk píše kód = má jednotný styl (teď jsem viděl školní projekt, kdy v části souborů bylo odsazeno tabem místo 4 mezer v pythonu), jestli tam používá české komentáře (na tohle jde zavést řeč) Jelikož se u nás ve firmě komunikuje výhradně v AJ, tak u nás musí být všechen kód komentován v AJ... Doporučuji, zkus si tohle 20 minutové kolečko sama na náhodném uživateli a dá ti to představu, kolik zhruba stihneš projít. U ústního pohovoru se pak na kód trochu obrátím, ale zajímají mě i další věci, které v kódu nenajdu.


„... každého věc a svoboda mít na GitHubu co chce.“ To není tak úplně pravda: znám člověka, co na GitHubu chtěl mít práci někoho jiného, vydávat jí za svojí a vydělávat na ní. To bych určitě neoznačoval za jeho svobodu. ![🙂](https://discord.com/assets/6e72cca8dcf91e01fac8.svg) Vím, extrémní případ, ale i s tím je nutné počítat a jakýkoliv kód s nejasným autorstvím (nebo očividně zkopírovaný odjinud) může vyvolat otázky.

Jasně, psal jsem to ne absolutně, ale v kontextu juniorů, kteří podle mě někdy až moc přemýšlí nad tím, jestli by jejich GitHub neměl být učesaný na míru pohovorům. Můj názor je, že ne, že GitHub je moje osobní skříň, kam si odkládám cokoliv, na čem pracuju. Že ta skříň je zároveň i vitrínka pro kolemjdoucí, to je jen příjemný bonus, protože nemusím posílat kód, který chci někomu ukázat, po zipech v mailu.



Když to tady tak čtu, tak mi čím dál víc dává smysl varianta, ke které zatím směřuju: mít pár veřejných projektů v repre verzi = bez komentářů nebo s minimalistickýma v AJ, a zbytek, nebo klidně totéž, v private výukové verzi = podrobně okomentované, abych si i s delším odstupem byla schopná vzpomenout, proč jsem něco napsala tak a tak. Rozhodně ale takové komentáře nemůžu vystavovat veřejně, s tím mám už i přímou negativní zkušenost. Tolik k té svobodě na githubu ![🙂](https://discord.com/assets/6e72cca8dcf91e01fac8.svg)



--- https://discord.com/channels/769966886598737931/1090649291804135485/1090912862542766121

Pokud ti to pomůže, tak je to asi nejčastější chyba začátečníků. Možná bych to měl mít někde napsané, až budu mít v příručce hezkou stránku o projektech 🤔

---


--- https://discord.com/channels/769966886598737931/1082249171278512151/1083785079702163496

Na GitHubu může být ještě detailnější, ale tam nebude koukat recruiter, ten mrkne CV, řekne si, hele má nějakou appku, něco dělá, to pošlu dál. Na GH zase kouká spíš ten technickej člověk, co to posuzuje, mrkne na README, mrkne na kód.

---


--- https://discord.com/channels/769966886598737931/1082316811703427102/1082316817424466000
Mám nějaké vlastní drobné "projekty" a ráda bych je na GitHub dala jako ukázku práce, hlavně přímo kvůli hledání práce, kvůli komunitnímu hodokvasu a poznámkám ani ne 🙂 A teď.
Mám například aplikaci v shiny (dělám v Rku). Takže na GH nahraju kód a do readme dám odkaz na tu apku na webu, kde je možné ji vyzkoušet? Obdobně, když mám script (je to správně použitá terminologie?), kde jsem zpracovala data (u kterých si ani nejsem jistá, jestli bych je mohla publikovat, nejsou moje) a dělám tam klasifikátor - udělám to tak, že nahraju do GH kód, popíšu v readme, co ten script dělá a pak tam například někam nahraju grafy nebo screenshoty úspěšnosti, které z toho klasifikátoru na konci vypadly? Pochopila jsem to správně?
Jde mi o to, že je mi vlastně nepříjemný, že si uživatel/nahlížející nemůže ten kód pustit, aby viděl, jak to funguje. Ani mi nepřišlo, že by to nějak šlo, ale možná jen špatně koukám a hledám. Taky tam cpát ta zdrojová data mi nepřipadá úplně dobré, z vícero důvodů.

---




--- https://discord.com/channels/769966886598737931/1017008201427845153/1017377812602179594

K tomu readme: syntaxe Markdownu

https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax

Něco k tomu jak je psát

https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes

https://www.makeareadme.com/

---



Jak hodnotíte na GitHubu školní / osobní projekty, které tam kandidáti často nahrají, "jen aby něco bylo na GitHubu"? Z mých zkušeností to jsou častokrát samostatné skripty s pomíchanou češtinou a ne nejlepšími best-practices.

Já to vidím tak, že se juniorům často řekne, aby měli GitHub, ale vlastně se jim tak úplně nevysvětlí, k čemu nebo proč. Přitom se tím myslí spíš to, aby měli pár nějakých větších projektů, kterými prokážou praktické použití znalostí, a na pohovoru už je jedno, jestli jsou na GitHubu nebo v .zipu v příloze. Jenže jak je GitHub známý a používaný pro Open Source, je to vlastně takové nejlepší místo, kam ty projekty dávat, takže se ta rada zkrátí na „mějte GitHub“ a „vše dávejte na GitHub“. Junior pak pokrčí rameny, řekne si OK, asi to je něco jako „mějte LinkedIn“ a něco nebo všechno tam dá, podle toho, jakých rad se mu dostane. Školní projekty nebo cvičení z Codewars, pokud je má. Nebo větší projekty, pokud je má. Nemá ale ponětí, jestli je to dobře, špatně, kolik tam toho má mít, jak moc mají být ty projekty velké, hotové, jak vyzdvihnout ty lepší a jak potlačit ty, kde si člověk jen něco zkoušel (já mám teď třeba 161 repozitářů), atd. V tomto má upřímně mezery ještě i příručka na junior.guru, chtěl bych to vysvětlovat lépe.

To, co tam mají, je pak většinou to, co mají. To, co by rád viděl technický recruiter, je „hezky uklizený a načančaný“ repozitář, ideálně s projektem o rozsahu zhruba bakalářky (teď nemyslím tu textovou část, ale tu programovací).

Asi bych se 1) zeptal, jestli si nesyslí ještě něco v šuplíku, protože spousta lidí se přece jenom svůj kód stydí dávat veřejně, 2) na ty projekty bych se díval hlavně z pohledu „toto je to, co ten člověk umí, jaké best practices má zažité a jaké ne a dává mi představu, co ho budu muset doučit“. České komentáře nebo proměnné by mi nutně asi nevadily, pokud jsou v nějakých cvičeních (některé české knihy např. o Pythonu to tak bohužel dokonce učí). Commitnuté tokeny nebo node_modules jsou už horší, tam vidím, jak daleko se ten člověk dostal k praxi.


https://www.linkedin.com/posts/marketa-willis_jak%C3%BD-je-recept-na-top-osobn%C3%AD-projekt-kter%C3%BD-activity-7179030416480194560-pfqP?utm_source=share&utm_medium=member_desktop

https://docs.google.com/document/d/1gk-sER2SHuW6T9sJZyYg5nMUaKNh0w2_-5HCGiF9zxs/edit?usp=sharing

nikdo už nechce vidět projekt typu todolist

--- https://discord.com/channels/769966886598737931/1237340412545339392/1237349106721226793
Souhlas, hlavně ta druhá část od
> Projekt nemusí být dokončený
je přesná.
---


--- https://discord.com/channels/769966886598737931/1237340412545339392/1237347362008203305
Mám z toho, co píšeš, tak trochu pocit, že bojuješ s tímhle https://en.wikipedia.org/wiki/Feature_creep a pak trochu se strachem, že ten projekt není dostatečně dobrý nebo dokončený pro účely hledání práce. Trochu zpomal, nadechni se, projekt klidně na pár dní pusť k ledu a pusť se do těch záležitostí, které ti najdou tu práci (Github, LinkedIn, CV, soft skills, portfolio). To vše je jednorázová práce v podstatě. S perfekcionismem je třeba občas bojovat a mírnit ho. Je to dobrý sluha, ale zlý pán. Plánům dávej jasné časové rámce a tvoř si nějaké větší milníky, kterých když těmi menšími plány dosáhneš, budeš spokojenější, směřuj to k nějakému MVP (minimal viable product), setkáš se s tím často i v budoucí práci. Projekt nemusí být dokončený a nemusí mít zdaleka všechny funkce, které jsi si vysnil. Je v pořádku přijít na pohovor a mluvit o projektu, na kterém pracuješ kontinuálně a umíš vysvětlit jak v základu funguje a co na něm chystáš do budoucna (ergo co se chystáš naučit nového). Nijak to nesnižuje tvoji kvalitu jako uchazeče. Pokud si říkáš, že si najdeš práci, až to dokončíš, tak si ji taky nemusíš začít hledat nikdy. A to dle mého není tvým hlavním a největším cílem. Tím hlavním cílem je  najít si tu pozici.
---


https://www.linkedin.com/feed/update/urn:li:ugcPost:7224054319896039424?commentUrn=urn%3Ali%3Acomment%3A%28ugcPost%3A7224054319896039424%2C7226646759999971328%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287226646759999971328%2Curn%3Ali%3AugcPost%3A7224054319896039424%29


https://roadmap.sh/backend/projects
https://roadmap.sh/frontend/projects


--- https://discord.com/channels/769966886598737931/1256028325105897583/1256201188039458857
Kdy bych s portfoliem neztrácel čas (stačí splnit jediný bod).
- Nejsem frontendista.
- Mám už jiný projekt na kterém demonstruji stejné skilly jako bych demonstroval na portfoliu.
- Designová stránka frontendu mě spíš nezajímá a nemám k dispozici návrh a neumím si ho najít.
- Jsem schopen popsat projekty a co jsem na nich dělal dostatečně v CV a README.md každého.
---


--- https://discord.com/channels/769966886598737931/916346318048337960/1257588804521300052
Z newsletteru Datažurnál od Samizdat:

> Teresa Ibarra si se svým expřítelem vyměnila 80 tisíc zpráv, které pitvá v datové analýze. Ačkoliv jde o docela banální rozbor intenzity a obsahu, stal se virálním – vyvozujeme z toho, že málokoho napadne takovou věc udělat. Přitom je to skvělý projekt pro začínající a mírně pokročilé datařstvo. Snad všechny chatovací platformy umožňují export zpráv a na těch datech si pak lze osahat ledasco: analýzu časových řad i sentimentu, knihovny pro zpracování přirozeného jazyka, regulární výrazy nebo třeba generování word cloudů jako v roce 2012. Hlavně ale potrénujte práci se souborem .gitignore, ať vedle grafů neskončí někde vyvěšený i JSON s kompletní konverzací.

https://teresaibarra.com/texts/
---


I Recreated Shazam's Algorithm from Scratch because no one is hiring jnr devs
https://www.youtube.com/watch?app=desktop&v=a0CVCcb0RJM


--- https://discord.com/channels/769966886598737931/1367214816518996090/1367214816518996090
Ahoj, 
napadla mě otázka kolem bezpečnosti a ochrany osobních údajů u demo aplikací, které mám veřejně online (např. na Renderu). Mám tam třeba veřejné API, do budoucna i přihlašování/registraci nebo původní plán byl ukládat IP adresu + user agent, a přemýšlím, jestli do README stačí poznámka, že jde o demo projekt a data nejsou nijak chráněná, nebo jestli řešíte i cookies, privacy policy apod. 
Jak to máte u svých veřejných projektů vy? Stačí upozornění, nebo to raději děláte „správně“ i pro demo? Nebo to moc řeším? 🙂
---


#} -->
