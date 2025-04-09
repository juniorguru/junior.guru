---
title: "Mýty a předsudky o práci v IT"
emoji: 🐉
stages: [thinking]
description: Všelijakých mýtů a nesmyslů o kariéře v IT koluje spousta. Jak to je ve skutečnosti?
template: main_handbook.html
---

{% from 'macros.html' import lead, blockquote_avatar, stories_list, video_card_engeto with context %}

# Mýty o programování

{% call lead() %}
Nemáš na to mozek. Není to pro starý. Nemáš to vystudované.
Ale taky: Naučíš se to za tři měsíce a utrhnou ti ruce! Sto tisíc mzda!
Všelijakých mýtů o kariéře v IT koluje spousta. Takže jak to je?
{% endcall %}

[TOC]

## Nejčastější mýty

Některé představy o programování a programátorské profesi nemají moc společného s realitou, ačkoliv je lidé stále opakují. Následující odstavce se snaží věci uvést na pravou míru a zabránit různým falešným obavám nebo naopak nereálným očekáváním. Můžeš si to pustit i jako video.

{{ video_card_engeto(
  'Nejčastější mýty o práci v IT',
  '5min',
  'https://www.youtube.com/watch?v=2Km3orTYFrM&list=PLrsbT5TVJXZa2daxo8_3NagDzPqHjBEpI',
  'Musím mít talent na techniku nebo matematiku? Záleží na věku? Potřebuji vysokou školu?',
) }}


## Už je pozdě začít    <span id="age"></span>

Programování není balet ani hokej, začít se dá opravdu v jakémkoliv věku. Někdo se k programování dostal už v pubertě a pokud je tobě přes třicet, můžeš váhat, jestli má vůbec smysl se o něco pokoušet. Realita je však taková, že těm, kteří začali v patnácti, se už zas tak moc programovat nechce, nebo se na něco specializovali. Jinými slovy, budete soutěžit v jiných ligách a místa je dost pro všechny. Nejspíš se už nestihneš stát programátorskou megahvězdou, byť ani to není zcela vyloučeno, ale normální práci v oboru si v pohodě najdeš.

{% call blockquote_avatar(
  'S programováním jsem začala ve 30, při rodičovské. Hrozně mě to baví, nejradši bych u toho strávila 24h denně. Začít se dá v každém věku.',
  'iveta-cesalova.jpg',
  'Iveta Česalová'
) %}
  Iveta Česalová, bývalá účetní, absolventka začátečnického kurzu [PyLadies](https://pyladies.cz/)
{% endcall %}

Že na věku nezáleží dokazují i následující příběhy reálných lidí, kteří dokázali v pozdějším věku změnit kariéru a dnes se programováním živí.

{{ stories_list(stories_by_tags.age|sample(4)) }}

## Nemáš na to matematický mozek, chybí ti talent    <span id="math"></span>

Častým omylem je představa, že potřebuješ talent na techniku, nebo konkrétně přímo na matematiku. Kromě vysoce specializovaných pozic programátoři při své každodenní práci nic složitého nepočítají. Věda, která za programováním stojí, tedy informatika, má jistě s matematikou mnoho společného, ale v praxi si většinou vystačíš se základy středoškolských počtů a logickým myšlením. Počítání se při programování využívá podobně jako třeba při truhlařině. Je lepší, když si místo zkoušení od oka umíš věci správně změřit a navrhnout.

{% call blockquote_avatar(
  'Z matematiky jsem míval čtyřky a nikdy mě nebavila. Dodnes si beru kalkulačku i na odečítání.',
  'honza-javorek.jpg',
  'Honza Javorek'
) %}
  Honza Javorek, profesionální programátor a autor junior.guru
{% endcall %}

Co se týče nějakého talentu, [žádné speciální předpoklady nepotřebuješ](https://www.youtube.com/watch?v=0VCN-dknx7Q&list=PLhB6F20C-jTPITEXEHus6fVZDfNxzRbv_). Programování je spíše řemeslo a více než vrozená genialita ti pomůže píle a trpělivost. Kromě toho, mnohem více než třeba zrovna matematika je potřeba angličtina. Materiály pro úplné začátečníky existují i v češtině, ale potom už se bez schopnosti alespoň číst anglický text obejít nelze. Nedostatečná angličtina je v IT jako bolavý zub. Chvíli vydržíš, ale když to nezačneš včas řešit, budeš pak už jen litovat.

{% call blockquote_avatar(
  'Všetko, čo je pre teba nové, bude zo začiatku frustrujúce, pôjde ti to pomaly. Ale nie preto, že si blbý alebo si sa nenarodila so špeciálnym génom. Je to len otázka času, snahy, námahy, vytrvalosti, trpezlivosti.',
  'yablko.jpg',
  'yablko'
) %}
  yablko, lektor online kurzů, ve svém [videu o tom, jestli potřebuješ na programování talent](https://www.youtube.com/watch?v=0VCN-dknx7Q&list=PLhB6F20C-jTPITEXEHus6fVZDfNxzRbv_)
{% endcall %}

## IT není pro ženy    <span id="ladies"></span>

Někoho to možná překvapí, ale k programování není potřeba penis. Neexistuje žádný důvod, proč by žena nemohla být skvělou programátorkou a kdo si to myslí, je ze středověku. Naopak, bez žen bychom [neměli počítače](https://cs.wikipedia.org/wiki/Ada_Lovelace), [nedostali bychom se na Měsíc](https://cs.wikipedia.org/wiki/Margaret_Hamilton) a [nevyfotili bychom černou díru](https://cs.wikipedia.org/wiki/Katie_Boumanov%C3%A1).

{{ blockquote_avatar(
  'Když jsem přišla k programu Apollo, nebyly tam žádné jiné ženy, které by psaly software.',
  'margaret-hamilton.jpg',
  'Margaret H. Hamilton',
  'Margaret H. Hamilton, programátorka softwaru pro cestu člověka na měsíc'
) }}

Podle ČSÚ je v Česku zatím žen v IT stále méně než v Turecku, ale na zlepšení se intenzivně pracuje. Aktivity jako [PyLadies nebo Czechitas](women.md) se snaží programování mezi ženami popularizovat a přichystat jim bezpečné prostředí, v němž si z nich nikdo nebude dělat legraci za to, že položily hloupou otázku, nebo je šovinisticky posílat zpátky k plotně. I kultura IT firem se postupně mění a stává se k ženám příjemnější, a to dokonce i v českém rybníčku, kde se lidé běžně děsí slov jako feminismus nebo diverzita.

{{ stories_list(stories_by_tags.women|sample(4)) }}

## IT je pouze pro geniální asociály    <span id="genius"></span>

Když se řekne „ajťák“, lidé si představí brýlatého mladíka s ponožkami v sandálech nebo nějakého hackera v kapuci, který sedí ve sklepě, kde pozoruje změť písmenek. Seriály jako britský [IT Crowd](https://www.csfd.cz/film/224203-ajtaci/) nebo americká [Teorie velkého třesku](https://www.csfd.cz/film/234260-teorie-velkeho-tresku/) stále posilují různé stereotypy, ale i kdybychom jim chtěli v něčem dát za pravdu, je dobré si uvědomit, že jejich první díly vznikly před {{ now.year - 2006 }} lety. Ačkoliv si toho někteří lidé stále ještě nevšimli, IT už dávno nevypadá jako na známé [fotce „brutální pařby informatiků“](https://www.forum24.cz/jak-dopadli-chlapci-z-brutalni-parby-informatiku-2/).

A nejde jen o to, že si ti kluci z fotky dnes přijdou na hezké peníze a pracují v prestižních firmách, ani o to, že už je v oboru mnohem více žen. Technologie možná dříve patřily k obskurním zálibám, dnes už však prostupují život každého z nás. Spolu s tím je IT přístupnější a otevřenější pestré škále osobností. Pro účely rozboření zažitých představ asi postačí [módní stylistka April Speight](https://learn.microsoft.com/en-us/shows/one-dev-minute/what-is-vogue-and-code--one-dev-question) nebo [hardwarová kutilka Naomi Wu](https://www.youtube.com/c/SexyCyborg).

Kromě samotného programování poskytuje IT a na něj napojený internetový průmysl i celou řadu dalších pozic, které ani nemusí být nutně technické: internetový marketing, psaní reklamních textů, design aplikací, psaní technické dokumentace, manažerské pozice, správa počítačové sítě a mnohé další.

Tito všichni většinou společně pracují v týmech, takže schopnost komunikace má na mnohých pracovištích větší hodnotu než zázračná genialita. Pokud to umíte s lidmi, máte zajímavé zkušenosti z jiného oboru a mezi své koníčky řadíte i jiné věci než počítače, je to dnes spíše výhoda než handicap.

## Potřebuješ vysokou školu    <span id="university"></span>

Pokud máš možnost studovat informatiku na vysoké škole, jdi do toho! Odradit se nech snad jen [pokud ji už studuješ a trpíš při tom](http://brm.sk/682/vyser-sa-na-vysoku-skolu). Vysoká škola ti dá především rozhled, stáže, slevy, kontakty, souvislosti a vědomosti do hloubky, možnost jet na Erasmus. Pokud chceš programovat samořídící auta nebo pomáhat raketám do vesmíru, bude to s vysokou školou rozhodně snazší.

To ale většina IT pracovníků nedělá. Běžní zaměstnavatelé po tobě budou chtít vytvářet webové stránky nebo mobilní appky. Ty zhotoví samouk s minimální praxí stejně dobře jako absolvent. K práci v IT tedy [univerzitu nutně mít nemusíš](https://www.youtube.com/watch?v=Tna7J05UoYU&list=PLhB6F20C-jTPITEXEHus6fVZDfNxzRbv_). Ještě se občas objeví firma, která z požadavku na VŠ titul nesleví, ale většinou se zaměstnavatelé spokojí s tím, pokud chybějící řádek v životopise vyvážíš dostatečnou praxí na projektech, klidně i v podobě domácích cvičení.

{% call blockquote_avatar(
  'Nie každý z nás bude programovať tie roboty čo behajú po Marse. V minulosti možno programovanie bola veľmi špecializovaná záležitosť, ale dnes má tak široký záber, že každý kto chce, si v tom spektre miestečko nájde.',
  'yablko.jpg',
  'yablko'
) %}
  yablko, lektor online kurzů, ve svém [videu o tom, jestli potřebuješ na programování talent](https://www.youtube.com/watch?v=0VCN-dknx7Q&list=PLhB6F20C-jTPITEXEHus6fVZDfNxzRbv_)
{% endcall %}

{% call blockquote_avatar(
  'Firmy hlavne zaujíma, či vieš robiť. Je im viacmenej jedno, kde si sa to naučil. Ak ukážeš niečo skutočné, čo si sám vyrobil, tak koho zaujíma odkiaľ to vieš? Vieš to!',
  'yablko.jpg',
  'yablko'
) %}
  yablko, ale v [dalším videu](https://www.youtube.com/watch?v=Tna7J05UoYU&list=PLhB6F20C-jTPITEXEHus6fVZDfNxzRbv_), které je o tom, zda potřebuješ na programování školu
{% endcall %}

Nemysli si ale, že když nepotřebuješ titul z VŠ, nebudeš se muset učit. IT je obor, v němž se naopak nikdy učit nepřestaneš. Ani profíci s dvacetiletými zkušenostmi se nemohou přestat vzdělávat v novinkách.

Zajímavou variantou je zkusit VŠ studovat, vybírat si zajímavé obory a předměty, ale ve chvíli, kdy už ti to přestane dávat smysl, bez pocitu viny odejít. Také se můžeš učit programovat po vlastní ose a studovat při tom úplně jiný obor, který tě zajímá. Svou budoucí kariéru můžeš pak založit na tom, že budeš rozumět např. sociologii nebo školství a dokážeš je propojit s moderními technologiemi.

{{ stories_list(stories_by_tags.student|sample(4)) }}

## Firmy se o tebe porvou    <span id="jobs"></span>

Ve firmách existuje velká poptávka po zkušených programátorech, takže se často mohou náboráři přetrhnout, aby je získali do svého týmu. Na základě toho se pak ale šíří mýtus, že si stačí přečíst čtyři kapitoly o nějakém programovacím jazyku a hned dostaneš spoustu nabídek práce. To je velký omyl a přinesl by ti velké zklamání. Junior (tak se v náborářské hantýrce označují začátečnické pozice) si ve skutečnosti musí svou první příležitost pracně shánět.

Firmy většinou neumí juniory efektivně zaučovat a raději měsíce hledají zkušenější lidi, byť beznadějně. Ve skutečnosti ti může rekvalifikace do IT zabrat i dva roky učení a praktických cvičení. Nenech se tím odradit, akorát si nastav ta správná očekávání. Získat práci v IT jako začátečník není jednoduché, ale rozhodně to jde, a to i bez titulu.

## Programování je zlatý důl    <span id="money"></span>

Mzdová ohodnocení IT odborníků se už roky umisťují na špici všech tabulek, takže finanční ohodnocení může být pro mnohé velkou motivací pro rekvalifikaci. Tím spíše dnes, kdy lidé kvůli pandemii přicházejí o práci v jiných oborech, ale IT se drží. Programátoři mají co se týče výdělku rozhodně nadstandardní možnosti, ale musíš si uvědomit, že bude chvíli trvat, než se tím odborníkem staneš.

Junior je pro firmu náklad, a to především v podobě času ostatních zaměstnanců. Nemůžeš očekávat, že ti hned začne chodit na účet 50 tisíc, nebo dokonce víc. Začátečníci v oboru se ovšem shodují, že když už je někam vzali, byli schopni na vysoké mzdy dosáhnout již poměrně záhy, v řádu jednotek odpracovaných let.

## Sedíš si v teple na židli    <span id="office"></span>

Pro ty, jejichž zaměstnání je fyzicky vyčerpávající nebo se odehrává venku, může kancelářská práce, jakou je i programování, působit lákavě. Člověk u něj přece celý den sedí na židli a v teple, že? Skutečnost je ovšem složitější. Na programátory neprší a nejsou vyčerpaní fyzicky, ale po celém dni intenzivního přemýšlení a komunikace s kolegy se dostavuje velká únava psychická.

Nezřídka dorazíš po práci domů, a byť máš dostatek síly tělesné, z tvého mozku je „zelenina“. Zbytek večera už zvládneš nanejvýš zírat na seriály. Rozhýbání svalů funguje naopak jako způsob relaxace. Ne náhodou se spolu se vzestupem kancelářské práce zaplnily cyklostezky ve městech běžci, a to především v hodinách po konci pracovní doby. Kromě toho brzy zjistíš, že sezení u počítače není úplně nejzdravější způsob trávení dní a musíš vědomě kompenzovat újmu, kterou způsobuje, ať už cvičením nebo kvalitní židlí.

## Je to samá pohoda    <span id="downsides"></span>

Jak už naznačuje předchozí odstavec, programátorská profese má i své nevýhody. Světe div se, je to práce jako každá jiná. Tvoje každodenní spokojenost bude nakonec záviset na konkrétní firmě, projektu, štěstí, šéfech, týmu kolegů a klidně i na tom, co někdo jiný, koho vůbec neznáš, špatně naprogramoval před pěti lety a ty s tím teď musíš pracovat. Budeš bojovat s [psychickou zátěží](https://web.archive.org/web/20241113114734/http://borisovo.cz/programming-sucks-cz.html), můžeš [zpochybňovat svůj zápal pro věc](https://www.youtube.com/watch?v=IwqN4c2BOFs) a časem i [vyhořet](https://cs.wikipedia.org/wiki/Syndrom_vyho%C5%99en%C3%AD).

{% call blockquote_avatar(
  'Programování není něco, co bych milovala. Ne, že bych jej nenáviděla, akorát to prostě nemiluju.',
  'sidney-buckner.jpg',
  'Sidney Buckner'
) %}
  Sidney Buckner, programátorka a autorka videa [I Don't Love Being A Software Engineer](https://www.youtube.com/watch?v=IwqN4c2BOFs)
{% endcall %}

IT ale naštěstí umožňuje mnoho způsobů, jak se uplatnit i jinak, než jen sezením u počítače a na schůzích. Můžeš se časem přesunout k učení a mentorování, psaní technických textů, pořádání komunitních akcí, začít přednášet na konferencích, konzultovat, vést lidi… Možností, jak si programování namíchat něčím jiným nebo jak zcela změnit hlavní zaměření své práce, je v rámci IT nepřeberně.


<!-- {#


https://www.linkedin.com/posts/lucietvrdikova_antireklama-activity-7284852497221865472-NLhk?utm_source=share&utm_medium=member_desktop&rcm=ACoAAACB93ABHHj4UI2winetGMZHboHlZIZojJA


--- https://discord.com/channels/769966886598737931/769966887055392768/1213068879467651114
> Now please don’t misunderstand me: when I say it’s “intensely social,” I don’t mean that you have to be an extroverted social butterfly.
>
> You can be the world’s biggest introvert and make great software.
>
> You can be socially clumsy (I am!) and make great software.
>
> You can be autistic and make great software.
>
> You can be chatty and charming, or silly, or dry and serious, or linear, or chaotic, or or or…and make great software.
>
> What you can’t be is misanthropic. When you write software, you are in relationship with other people…
---


https://mastodonczech.cz/@nedbat@hachyderm.io/111789013379418126


--- https://discord.com/channels/769966886598737931/1080041944236953623/1080549618271666257
Titul není v IT příliš podstatný, ale to co ti škola umožní už podstatné být může.
Všimni si, že píšu **umožní**, ne naučí.

Na VŠ platí mnohem více to než na střední (o základce nemluvě), že to není jen místo, kde do tebe nalejou znalosti, pak prověří, jestli jich v tobě dost utkvělo a „musíš“ to dokončit. Samozřejmě někdo to tak vnímá a chová se tak.

Teď už „nemusíš“, ale můžeš **chtít** nebo si uvědomit, že tam **potřebuješ** chodit k dosažení cíle, který **chceš**.

Ta škola kromě toho, že tě vede nějakými předměty a vyžaduje po tobě nějakou aktivitu, tak je hlavně prostředí, které tě může přivést ke všemu možnému, dát ti možnost si to vyzkoušet, ukázat ti možnosti.

Často je důležitější, co se naučíš sám, protože budeš se spolužákama dělat nějakej projekt mimo školu.
A to, že nebudeš tlačenej v praxi hned vše aplikovat tak, aby to něco vydělalo.

Budeš mít čas a podmínky si hrát a **učit se**.
Toho samozřejmě budeš mít víc, pokud tě během studia budou živit rodiče.

Pro někoho může být prostředí VŠ silně demotivační, akademická sféra umí být všelijaká.
Některé předměty můžou být skoro k ničemu, jiné zase těžké a otravné a sám by ses k nim nedokopal, ale dají ti nějaké základy, které využiješ.

Ty si z toho vem co potřebuješ, studium se dá i všelijak rozkládat, dělat u toho práci atd. není to jako střední, kde propadnout nebo nedat maturitu je průšvih. Dá se odejít po roce, dvou i před těma státnicema jak psala <@773601329095376906>. Ber to tak, že tvůj mozek bude časem jen pomalejší, takže jestli chceš bejt dobrej, tak teď je nejlepší šance se pustit do těch těžších věcí z IT.

A přestože je v IT spousta práce i pro lidi, kteří toho zas tolik neumí, tak jsou tam i hodně těžký problémy, který bez tý VŠ (nebo ekvivalentní znalosti) budou dělat jen těžko.

_Kéž bych tohle svému mladšímu já mohl před 25 lety předat…a ještě i to, že je jedno, jak se mi nepravděpodobné zdá, že se někam dostanu, ať to zkusím. Přinejhorším je tu další rok a ten rok můžu strávit prací a přípravou na studium / zkoušky._
---

--- https://discord.com/channels/769966886598737931/769966887055392768/1082587990104215613
Jak je IT úžasný víme všichni.
Namátkou: topíme se v penězích, pracujeme z pláže v Karibiku / vrcholku Everestu / sklepa na samotě u lesa, měníme svět, pořád se máme co nového učit, umíme opravit libovolnou tiskárnu atd.

Co jsou ale podle vás nevýhody tohoto oboru?
---

--- https://discord.com/channels/769966886598737931/789107031939481641/978387259881562213
„opravdový programování“ 🙄
https://en.wikipedia.org/wiki/Real_Programmers_Don%27t_Use_Pascal
---

ageism a kam mizí staří programátoři
https://abrarmasum.medium.com/when-do-programmers-retire-is-35-the-end-72d173760ee2

hraje věk roli?
https://discord.com/channels/769966886598737931/769966887055392768/818610012866740274
https://discord.com/channels/769966886598737931/788823881024405544/806262752975912960
https://discord.com/channels/769966886598737931/769966887055392768/808041228239241256

Přemýšlím, že se vrátím na šachtu, tam jsem měl prázdnou hlavu. Teď chodím z práce domů, vole, a furt nad něčím přemýšlím, furt mám něco v hlavě, vole, něco tě napadne, musím si ku**a zapnout komp, ty p**o. Mně se zdálo o závorkách - složené závorky, dvě složené závorky, ty p**o, jak to tam mám dát?
https://zpravy.aktualne.cz/domaci/tomas-hisem-z-hornika-programatorem/r~927d3882bc9a11ebaedf0cc47ab5f122/

- https://www.youtube.com/watch?v=HluANRwPyNo

- ajtaci asocialove ze sklepa? a videl nekdy nekdo ten sklep? me to prijde socialni dost (KMENY) https://www.youtube.com/watch?v=xg7xv6adtmI

Ještě bych dodal, abych nastavil správně očekávání, že IT určitě umožňuje dělat poměrně dlouhé úseky práce bez ostatních lidí nebo s kontaktem třeba jen na chatu, ale zároveň je to většinou týmová záležitost a je proto nutné komunikovat přinejmenším i s ostatními vývojáři v týmu. Tedy taková ta představa o někom zalezlém celé dny u počítače, kdo mluví jen s počítačem je spíš stereotyp než realita.

ageism https://www.newyorker.com/magazine/2017/11/20/why-ageism-never-gets-old

student versus career switcher
https://discord.com/channels/769966886598737931/788826407412170752/868086772201062420

- Být ajťák ve sklepě je sociální dostatečně! https://www.facebook.com/groups/junior.guru/posts/603771920546419/?comment_id=603893173867627&reply_comment_id=604521060471505&__cft__[0]=AZWvoQ7k4LtsUi2GvJ5V8o1d9-z3kLYiayBP87mrrziVf8swj67evDh4C-oMjVDL56j0Ikb9xvYiOP2Kholscjoq3hS4x5OtaZld3Bj34ovQLF1wxBPsCiC8P8-uM2gNQUaINrc810Kq9adv7EhE7Z4zxWAP1gd1ol5xD7lpDsSLyPvjhZ8Kz2m3AE6HJPcr45U&__tn__=R]-R

- Nástupní mzdy se pohybují od 35 do 40 tisíc korun hrubého. Lze se dostat i na vyšší částky, je to ale vykoupené tím, že firma očekává vyšší samostatnost a rychlejší rozvoj dovedností. My našim studentům doporučujeme, aby do šesti až devíti měsíců od absolvování kurzu upřednostňovali nabídku s nižší mzdou a větším mentoringem ze strany právě seniorního pracovníka. V začátku kariéry je důležitější nabírat zkušenosti než několik tisícikorun navíc ke mzdě.

https://www.linkedin.com/posts/lucietvrdikova_antireklama-activity-7284852497221865472-NLhk/?rcm=ACoAAAP3cMQB6Z0KS11itMTIOss5Q1J0OCTXkaQ

#} -->
