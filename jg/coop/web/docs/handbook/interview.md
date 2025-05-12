---
title: Pohovor v IT
emoji: 🤝
stages: [preparing, applying, deciding]
description: Jaké otázky ti nejspíš položí u pohovoru na pozici programátor? Jak bude celý pohovor vlastně probíhat? Jak by měla vypadat tvoje příprava?
template: main_handbook.html
---

{% from 'macros.html' import blockquote, blockquote_avatar, link_card, note with context %}

# Pohovor

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }} Kapitola se teprve připravuje.
{% endcall %}

[TOC]

## Otázky na tebe

Na pohovoru ti budou pokládat otázky a také se očekává, že [nějaké otázky budeš mít ty](#tvoje-otazky). Začněme těmi, které můžeš dostat:

*   **Behaviorální otázky.** „Kdo tě nejvíce ovlivnil ve tvé kariéře?“ [Další příklady](https://www.pathrise.com/guides/25-behavioral-interview-questions/).
*   **Technické otázky.** „Představ si, že nic nevím o [Reactu](https://react.dev/). Vysvětli mi, co to je.“ Nebo: „Co je [float](https://developer.mozilla.org/en-US/docs/Web/CSS/float) v CSS?“
*   **[Úlohy u tabule](#ulohy-na-algoritmizaci)**, programování na místě, hádanky. Viz např. [HackerRank](https://www.hackerrank.com/).
*   **Úkoly na doma.** Úkol zpracováváš mimo pohovor a máš na něj kolik času potřebuješ.
*   **Párové programování.** Spolu s někým z firmy řešíte zadaný problém.

Na otázky se můžeš **připravit**. Podle toho, na jakou pozici se hlásíš, můžeš na internetu najít seznamy typických otázek. Hledej třeba „[interview questions python](https://www.google.cz/search?q=interview%20questions%20python)“. Nebo „[behavioral interview questions](https://www.google.cz/search?q=behavioral%20interview%20questions)“.

Ber si všude s sebou notes na poznámky a **zapisuj si všechno, co nevíš. Doma se na to po každém pohovoru podívej.** Nemusíš se hned učit všechno, co kde kdo zmínil, ale zjisti si aspoň, co ty věci jsou, na co se používají, pro jaké profese je nutnost s nimi umět. **Uč se z pohovorů.**

<small>Rady v této podkapitole volně vychází ze [série tipů, které tweetovala Ali Spittel](https://twitter.com/ASpittel/status/1214979863683174400) a z osobních doporučení od Olgy Fomichevy. Velké díky!</small>

## Když nevíš

Během pohovoru **ukaž, jak přemýšlíš**. Vysvětli, jakým způsobem se propracováváš k odpovědi, kresli diagramy, piš kód, vysvětluj díry ve svém přístupu. Ptej se, pokud ti něco není jasné. Situace, kdy mlčíš a přemýšlíš, není příjemná ani tobě, ani ostatním přítomným. Vždy je lepší „přemýšlet nahlas“, ale také prostě říct „nevím“, ideálně spolu s „můžete mi to trochu popsat, ať se mám od čeho odrazit?“.

Pokud neznáš Django, **odpověz upřímně!** Nelži a nesnaž se nic zamaskovat, pro tazatele bude snadné tě prokouknout. Člověka, který mlží, mít nikdo v týmu nechce. Raději řekni „Nevím, ale chci se to naučit“. Nebo: „Mám jeden projekt ve Flasku, což je taky webový framework v Pythonu, tak snad by nebylo těžké do toho proniknout“. Pokud nevíš vůbec, klidně se na správné řešení na místě zeptej. **Ukaž, že se nebojíš ptát když nevíš, a že máš chuť se posouvat.**

{% call blockquote(
  'Říkej pravdu a dostaneš se tam, kam chceš.'
) %}
  Olga Fomicheva, organizátorka a absolventka začátečnického kurzu [PyLadies](https://pyladies.cz)
{% endcall %}

## Úlohy na algoritmizaci

Na pohovorech se můžeš až příliš často setkat s úlohami u tabule, _challenges_, _puzzles_, otázkami na algoritmizaci, na [složitost](https://cs.wikipedia.org/wiki/Asymptotick%C3%A1_slo%C5%BEitost), na řazení, procházení stromů a podobné nesmysly. **Přitom v drtivé většině případů nikdo nic takového ve své práci běžně nepotřebuje.** Většina programátorů stejně jako ty použije na řazení vestavěnou funkci [sort()](https://docs.python.org/3/howto/sorting.html) — a je to. I ti, kteří se vše podrobně dřív učili na VŠ a skládali z toho zkoušky, většinu z toho dávno zapomněli — protože to nepoužívají. Nanejvýš s tím machrují na společném obědě.

**Bohužel pro tebe je ale testování takovýchto znalostí na pohovorech stále velmi populární.** Stejně jako někdo vyučuje dějepis tak, že nutí děti nazpaměť si pamatovat každé datum, v IT zase lidé nesmyslně lpí na tom, aby každý znal princip [Quicksortu](https://en.wikipedia.org/wiki/Quicksort). Přijmi to jako smutný fakt a připrav se. Ono se ti to samozřejmě neztratí, **nejsou to zbytečnosti**. Je dobré znát kontext, vědět jak věci fungují, umět psát efektivnější programy. Jen by bylo lepší to mít možnost objevovat postupně, až když to budeš potřebovat, a ne se to muset učit nazpaměť kvůli pohovorům.

Holt, nedá se nic dělat. Zhluboka se nadechni a hurá do toho:

1.  **Projdi si základy** algoritmizace a práce s datovými strukturami. Začni třeba s [BaseCS](practice.md#zaklady). Algoritmy se nejlépe vysvětlují na videu, takže je [hledej na YouTube](https://www.youtube.com/results?search_query=quicksort).
2.  **Řeš úlohy** na [webech jako Codewars nebo HackerRank](practice.md). Procvičíš si algoritmizaci a datové struktury na reálných problémech. Projdi si [příručky](candidate.md#souvisejici-prirucky) zabývající se řešením úloh z pohovorů.
3.  **Dělej si poznámky**. Díky nim se budeš moci k nabytým vědomostem snadno vracet a budeš je mít v podobě, která ti nejvíc vyhovuje. Psaní navíc upevňuje paměť. Mrkni třeba na [poznámky Ali Spittel](https://github.com/aspittel/coding-cheat-sheets), které si původně psala rukou na papír.

{% call blockquote_avatar(
  'Dělala jsem jednu úlohu každé ráno po probuzení, abych si rozehřála mozek.',
  'ali-spittel.jpg',
  'Ali Spittel'
) %}
  Ali Spittel, [We Learn Code](https://welearncode.com/) & [Ladybug Podcast](https://www.ladybug.dev/)
{% endcall %}

<small>Rady v této podkapitole volně vychází ze [série tipů, které tweetovala Ali Spittel](https://twitter.com/ASpittel/status/1214979863683174400). Velké díky!</small>

## Povědomí o firmě

Kandidát, který se někam hlásí a ani neví, o co se firma na trhu snaží, nepůsobí moc profesionálně. Je důležité mít **základní povědomí o firmě a tom, co dělá**. To získáš díky [průzkumu před pohovorem](candidate.md#informace-o-firme). Dále můžeš dostat zvědavé dotazy typu „Jak jste nás našla?“, ale na ty většinou není těžké odpovědět po pravdě.

Co je horší, jsou **otázky jako „Proč zrovna my?“**, které, pokud se zrovna nehlásíš do práce svých snů, nelze snadno vyhrát. Obcházíš nejspíš desítky pohovorů a není možné toužit pracovat pro každou z firem, které navštívíš. Lidem na pohovoru ovšem nemusí stačit pragmatická odpověď, že „člověk potřebuje něco jíst a z inzerátu se zdálo, že by mohli za dobře odvedenou práci posílat na účet peníze“. Když už se tak hloupě ptají, nezbývá než v tomto případě skutečnost trochu přibarvit a firmě zalichotit, ať si nepřipadá, že je jen jednou z položek na tvém seznamu — i kdyby opravdu byla.

## Tvoje otázky

Připrav si dotazy, které budeš mít ty ohledně firmy a nabízené pozice. Zcela zásadní jsou pro tebe odpovědi na následující dvě otázky:

*   Budu mít ve firmě **přidělené lidi, kteří se mi budou věnovat** a za kterými budu moci chodit pro rady **bez pocitu, že je zdržuji od důležité práce**?
*   Můžete mi dát **konkrétní příklady** toho, na čem budu pracovat?

Nastupuješ jako začátečník a budeš potřebovat, aby ti někdo stále pomáhal. Pokud s tím firma nepočítá, nebude na tebe mít nikdo čas a tvůj pracovní den se brzy promění v peklo. Neschopnost firmy dát ti příklad tvé práce, nebo ti ji srozumitelně vysvětlit, také o něčem vypovídá. Zároveň je to tvoje kontrola, zda právě toto chceš opravdu dělat. Kromě těchto hlavních existuje i spousta dalších otázek, na které se můžeš zeptat:

<div class="link-cards">
  {{ link_card(
    'Reverse interview',
    'https://github.com/viraptor/reverse-interview#readme',
    'Inspiruj se dlouhým seznamem otázek, které můžeš položit.'
  ) }}

  {{ link_card(
    'How to do job interview right',
    'https://trello.com/b/igarGHRw/',
    'Prostuduj nástěnku plnou tipů jak se připravit a na co se ptát.'
  ) }}
</div>

Celkově je dobré se soustředit nejen na firmu, ale i **na sebe**. Jsi juniorní, ale na pohovoru dostáváš rozpačité odpovědi na to, jestli se ti někdo bude věnovat? Vidíš už na pohovoru přebujelá ega, machrování, manipulativní otázky? Nejednají s tebou s respektem? Zaznamenáváš sexistické narážky? Působí firma neorganizovaně? Musíš projít přes desetikolový pohovor se spoustou úloh před tabulí? Až nastoupíš, nebude to lepší! Všechno toto jsou tzv. _red flags_, signály, že **firma, do které se snažíš dostat, [není tak úplně v pořádku](candidate.md#firemni-kultura)** a nejspíš nestojí za to s ní ztrácet čas. Pohovor funguje na obě strany — testuješ si i ty firmu, nejen ona tebe.

{% call blockquote_avatar(
  'Mysli i na sebe. Pokud při pohovoru musíš přeskočit milion překážek, možná je to signál, že tak bude vypadat i ta práce.',
  'ali-spittel.jpg',
  'Ali Spittel'
) %}
  Ali Spittel, [We Learn Code](https://welearncode.com/) & [Ladybug Podcast](https://www.ladybug.dev/)
{% endcall %}

## Vyjednávání

Vyjednávat jde o všem. O nabídkách, [stážích](candidate.md#staze), počtu pracovních hodin, typu úvazku, možnosti pracovat z domů, povinnostech v práci, benefitech, [mzdě](candidate.md#kolik-si-vydelam). **Nic není dáno pevně a hodně firem je ochotno se domluvit alespoň na kompromisu**, pokud o tebe budou mít vážný zájem. Zaměstnavatel by ti měl chtít jít svou nabídkou naproti, protože **čím víc ti budou pracovní podmínky vyhovovat, tím déle zůstaneš** a investice firmy do tvého rozvoje nepřijde za rok vniveč. Vyjednávací pozici ti mohou vylepšit [tvoje úspěchy a reference](candidate.md#zapisuj-si-uspechy), zajímavé předchozí zkušenosti, jakékoliv [aktivity navíc](candidate.md#projev-aktivitu-navic) nebo lepší nabídka v jiné firmě:

*   Poděkuj za nabídku s tím, že se ti líbí
*   Řekni, které věci by se ti hodilo dohodnout jinak
*   Zmiň [úspěchy a zkušenosti](candidate.md#zapisuj-si-uspechy), které podporují tvoje požadavky, nebo konkurenční nabídku
*   Navaž na to tím, jak se těšíš, s čím vším budeš moci firmě pomoci v budoucnu

Drž se [seznamu svých priorit](candidate.md#tvoje-pozadavky) a **nenech se natlačit do něčeho, co nechceš**. Nespokoj se s nižší mzdou, než za jakou by ti bylo příjemné pracovat. **I když začínáš, zasloužíš si adekvátní ohodnocení.** Pokud se firmě líbíš, bude ochotná vyjednávat o mzdě. Jestliže budeš mít příliš nízká očekávání z hlediska mzdy, může to na zaměstnavatele působit zoufale nebo jako znamení velmi nízkého sebevědomí.

## Práce „na IČO“

Při vyjednávání s firmou může padnout návrh, že budeš pracovat „na IČO“. Některé firmy to po tobě mohou i přímo vyžadovat jako jediný způsob, jakým jsou ochotné tě „zaměstnat“. Myslí se tím, že se místo zaměstnaneckého poměru staneš [OSVČ](https://cs.wikipedia.org/wiki/Osoba_samostatn%C4%9B_v%C3%BDd%C4%9Ble%C4%8Dn%C4%9B_%C4%8Dinn%C3%A1) a budeš pro firmu pracovat jako [kontraktor](candidate.md#prace-na-volne-noze).

Přestože jde o balancování na hraně zákona o [švarc systému](https://cs.wikipedia.org/wiki/%C5%A0varc_syst%C3%A9m), v českém IT takto pracuje hodně lidí. [Analýza evropského technologického trhu z roku 2019](https://2019.stateofeuropeantech.com/chapter/people/article/strong-talent-base/#chart-372-1627) obsahuje graf, kde ČR, Ukrajina a Polsko jednoznačně vedou v počtu IT odborníků na volné noze. Asi ale tušíme, že důvodem je spíše šedá ekonomika než úžasné podmínky pro [nezávislé profesionály](candidate.md#prace-na-volne-noze). Proč je práce „na IČO“ v IT tak oblíbená?

*   Ty i firma odvádíte **méně peněz státu**. Firma neplatí pojištění a tvou „mzdu“ si dá do nákladů. Ty máš při programování náklady minimální, takže snižuješ své odvody využitím [výdajových paušálů](https://www.jakpodnikat.cz/pausal-danovy-vydajovy-auto.php).
*   Mnohým se líbí větší **osobní svoboda**, tedy rozmazání hranice mezi klasickým zaměstnáním a podnikáním. Vyvázání ze zákoníku práce vidí v dobře nastavené spolupráci jako výhodu.

Být živnostníkem má však tyto nevýhody:

*   Administrativa je na tobě. Pro každou vydělanou částku musíš vydat a poslat fakturu. Pokud se nepřihlásíš k paušální dani, tak každý rok podáváš [daňové přiznání](https://cs.wikipedia.org/wiki/Da%C5%88ov%C3%A9_p%C5%99izn%C3%A1n%C3%AD), přehled pro ČSSZ a přehled pro zdravotní pojišťovnu.
*   Pokud si při podnikání vytvoříš dluhy, máš povinnost k uhrazení využít i veškerý svůj čistě soukromý majetek (ručíš vším, na rozdíl od s. r. o., tedy [společnosti s ručením omezeným](https://cs.wikipedia.org/wiki/Spole%C4%8Dnost_s_ru%C4%8Den%C3%ADm_omezen%C3%BDm)).
*   I pokud by ti každý měsíc na účet chodilo více peněz než průměrnému zaměstnanci, u banky máš jako OSVČ [výrazně horší pozici pro získání hypotéky](https://www.chytryhonza.cz/hypoteka-pro-osvc-jak-u-banky-s-zadosti-uspet).
*   Za léta práce na živnostenský list budeš mít od státu nižší důchod.
*   Balancuješ na hraně [švarc systému](https://cs.wikipedia.org/wiki/%C5%A0varc_syst%C3%A9m). Když si to spolu s firmou nepohlídáte, je vaše činnost nelegální a postih hrozí jak tobě (až 100 000 Kč), tak firmě ([masivní pokuty, doplacení odvodů](https://magazin.almacareer.com/cz/svarcsystem-je-v-roce-2024-jeste-vetsim-strasakem-nez-driv-na-co-si-dat-pozor)). Znamená to také, že oficiálně nemáš nadřízeného, pracuješ na vlastním počítači, voláš z vlastního telefonu.
*   Nemáš ochranu, kterou zaměstnancům dává zákoník práce. Ta jistě není dokonalá, ale jako OSVČ nemáš žádnou. Nejde o stravenky, ale o nárok na odstupné, výpovědní lhůtu, placenou dovolenou nebo nemocenskou. Když nepracuješ, např. z důvodu dlouhé nemoci, tak nemáš příjem. Zároveň každý měsíc stále platíš zálohy na pojištění (minimálně kolem 5 000 Kč měsíčně).
*   I ti nejlepší mohou být mezi prvními, které firmy „propustí“, když je problém. Ať už jde o krach [startupu](candidate.md#prace-pro-startup) nebo začátek pandemie, když jde do tuhého, firmy neváhají rozloučit se velmi rychle i s celými týmy kontraktorů.

Pracovat „na IČO“ **není nutně nic špatného, ale mělo by to být tvé vlastní rozhodnutí, při kterém zvážíš všechna pro a proti**. Mnozí pracují dlouhé roky jako kontraktoři, aniž by si některé z uvedných nevýhod uvědomovali, čímž si zadělávají na budoucí nepříjemné překvapení. **Proti většině nevýhod se můžeš nějak chránit**, ale musíš o nich vědět a nezanedbat prevenci:

*   Základní administrativu za tebe udělají aplikace, jako např. [Fakturoid](https://www.fakturoid.cz/pro-zivnostniky), který umí nejen posílat faktury, ale i generovat daňová přiznání a přehledy.
*   Pokud do povinnosti platit DPH spadneš vysokým obratem, nejspíš si můžeš dovolit platit si někoho na účetnictví.
*   Proti různým rizikům, která na tebe jako OSVČ číhají, se můžeš nechat relativně levně připojistit u komerčních pojišťoven. Dobře si promysli pravděpodobnost, že něco nastane, a nastuduj vyjímky, které pojištění nepokrývá. Ochranu, jakou mají od státu zaměstnanci, to sice plně nenahradí, ale lepší než nic.
*   Šetři! Měj záložní peníze na horší časy, na dovolenou, pro případ nemoci či jiných nečekaných výpadků příjmů, odkládej si na důchod.
*   Vyhnout se „znakům závislé práce“ [není obtížné](https://www.podnikatel.cz/clanky/7-znaku-ktere-prokazuji-svarcsystem/). Když si to pohlídáš, žádné pokuty za švarc systém ti nehrozí.
*   Některé chybějící „jistoty“ lze řešit dobře napsanou smlouvou mezi tebou a firmou, která zaručuje podmínky rozumné pro obě strany. Některé si s firmou můžete na dobré slovo slíbit, ale ve smlouvě být nemohou (např. placená dovolená, byl by to znak závislé práce). Především si musíš vše dobře spočítat, všechna rizika vyčíslit a přičíst ke své „čisté“ hodinové sazbě. A to včetně peněz, které vydáš na připojištění, nemocenskou, nebo důchod.

Rozhodně se nikdy nenech do práce „na IČO“ dotlačit firmou. Zákon o [švarc systému](https://cs.wikipedia.org/wiki/%C5%A0varc_syst%C3%A9m) totiž neexistuje ani tak proto, aby zabránil menším odvodům státu, ale hlavně aby zabránil tomu, [že na tobě někdo bude šetřit, i když ty nechceš](https://cs.wikipedia.org/wiki/Prekarizace).

Čím vyšší máš hodnotu na trhu, tím spíš budeš z práce „na IČO“ benefitovat. **Jako junior máš ale hodnotu malou, takže taháš za kratší provaz.** Práci třeba sháníš už delší dobu a zjišťuješ, že si bohužel nemůžeš příliš vybírat. U jedné firmy projdeš pohovorem, ale zaměstnavatel tě nutí pracovat „na IČO“. Argumentuje tím, že zřízení živnosti přece není problém a že si vyděláš víc peněz. Nechceš přijít o jedinečnou příležitost, takže nakonec souhlasíš. Nedobrovolně na sebe jako OSVČ bereš veškerá rizika a je velká pravděpodobnost, že si špatně spočítáš, co vše musíš zahrnout do své sazby. Na rozdíl od dlouholetého profíka nemáš na firmu žádnou páku, nemáš naspořeno a neseženeš si do měsíce jinou práci, pokud tě na hodinu vyhodí. Jsi obětí švarc systému.

{% call blockquote(
  'Chtějí, abych byl na IČO. Prý mají účetní, která mi to založí a všechno vyřeší, ale včera o tom šéf už nic nevěděl. Aby nedošlo k podezření ze švarc systému, nemáme placenou dovolenou ani jiné benefity, k práci musím mít vlastní notebook.'
) %}
  Honza S., návštěvník junior.guru, o reálné situaci, do které se dostal
{% endcall %}

Jak už bylo zmíněno výše, **vždy si dobře zvaž, zda se ti nabídka opravdu vyplatí**. Pokud se s firmou nedomluvíš na dostatečně vysoké sazbě, která by vše pokryla, nebo pokud „na IČO“ vůbec jít nechceš, je pro tebe lepší odmítnout a hledat dál. I pokud se ti z dvaceti firem ozvala jedna, nesmíš podlehnout pocitu, že to musíš vzít. Stejně jako u [mizerné firemní kultury](candidate.md#firemni-kultura), nestojí to za to.

## Jak zvládnout odmítnutí

Je velmi pravděpodobné, že tě odmítnou na pohovoru, a to **proto, že se to děje úplně každému**. [Ano, i seniorním programátorům](https://web.archive.org/web/20241212065053/https://sw-samuraj.cz/2017/09/smutna-zprava-o-stavu-it-trhu/). U začátečníků navíc chvíli trvá, než se naladí na aktuální poptávku trhu a na to, jak přesně fungují přijímací pohovory v IT. Raději **počítej s tím, že ze začátku to půjde ztuha** a tvé první hledání práce [bude zahrnovat i desítky pohovorů a může trvat měsíce](candidate.md#jaka-mit-ocekavani).

{% call blockquote_avatar(
  'Pokud tě odmítnou, neznamená to, že nejsi dost dobrá. Nevzdávej to. Máš talent a určitě najdeš práci, která zrovna ten tvůj talent ocení. Každého někdy odmítli na pohovoru.',
  'emma-bostian.jpg',
  'Emma Bostian'
) %}
  Emma Bostian, inženýrka ve Spotify, podcasterka v [Ladybug Podcast](https://www.ladybug.dev/)
{% endcall %}

**Neber odmítnutí jako něco negativního.** Znamená to prostě, že si s firmou nesedíte a bylo by z toho stejně akorát mrzení. Nerozhoduje se jen firma o tobě, ale i ty o ní. **Je to rozhovor, ve kterém se dvě rovnocenné strany snaží přijít na to, zda to spolu zkusí.** Není to test, který musíš dát, a který vyhodnotí, zda „na to máš“. Naopak, často se akorát nepotkáš s představou lidí ve firmě a není to vůbec o tvých schopnostech.

Je to jako Tinder — odmítnutí znamená, že si navzájem šetříte čas. Ber to optimisticky! Není to selhání, ale jen nějaký stav mezi tebou a konkrétní firmou. Nevypovídá nic o tom, jak to bude jinde. **Z každého pohovoru se navíc můžeš něco přiučit, po každém se budeš lépe orientovat na trhu.**

{% call blockquote(
  'NE neznamená špatně, ale že existuje jiná cesta, třeba i lepší. Když se nedaří, obrátím to ve svůj prospěch. Nedostala jsem se do PyLadies? Založila jsem další pražský PyLadies kurz.'
) %}
  Olga Fomicheva, organizátorka a absolventka začátečnického kurzu [PyLadies](https://pyladies.cz)
{% endcall %}

Řekni si o **zpětnou vazbu po pohovoru**. Může to být dobrý zdroj poznatků (nebo ujištění, že ta firma není nic pro tebe). Někdy ti bohužel žádnou zpětnou vazbu nedají, ale to nemusí být vyloženě chyba těch, kteří s tebou vedli pohovor. **Mnoho velkých mezinárodních firem má doporučení od právníků, že zpětnou vazbu nemá vůbec poskytovat.** Existuje pro ně totiž riziko, že by ji kandidát mohl zneužít k žalobě kvůli diskriminaci. Pošlou ti nějakou obecnou větu, např. „hledáme někoho zkušenějšího“. Nepropadej depresi, že zbytečně investuješ hodiny do učení a práci nenajdeš. Za touto větou se ve skutečnosti může skrývat naprosto cokoliv. Můžeš je vzít za slovo a zkusit se [zeptat na stáž](candidate.md#staze).

Počítej i s tím, že **mnoho firem ti na tvůj zájem o práci vůbec neodpoví**. Ať už mají příliš mnoho kandidátů a odpovídat každému by bylo náročné, nebo jsou prostě nedbalí ve svém přijímacím procesu, výsledek je stejný — můžeš čekat týdny a nic z toho nebude. **Odpovídej na několik nabídek zároveň!** Může se ti stát, že budeš mít na výběr, a díky tomu i méně stresu a lepší [vyjednávací pozici](#vyjednavani).



<!-- {#

Monika Ptáčníková
https://overcast.fm/+oxWgC3EHI

The Pragmatic Engineer Test: 12 Questions on Engineering Culture
https://blog.pragmaticengineer.com/pragmatic-engineer-test/

švarc systém - tohle asi ještě oddělit do celé kapitoly zvlášť? na volné noze / ičo?
https://finmag.penize.cz/penize/428665-proklinany-svarcsystem-ocima-expertu-ma-smysl-s-nim-bojovat

konkurencni dolozka
https://discord.com/channels/769966886598737931/788826407412170752/873095213382524988

propad platu
https://discord.com/channels/769966886598737931/788826407412170752/872461572864356412

Ok, you're interviewing somewhere. Rad. There are some things you should write down before your first interview. Don't THINK these things, WRITE them down. It'll help. Those things are below.
https://twitter.com/rands/status/1442577313795768320

Z druhé strany – i tohle se děje 🙂 Ještě můj tip pro kandidáty – na on-line pohovoru čekejte, že vás budou chtít vidět. Je trochu zvláštní, když se kandidát schovává, nebo když zájemce o remote práci má zřejmé potíže nastavit audio/video setup.
dějou se podvody https://trello.com/c/zbsJ4Hs0/6644-z-druh%C3%A9-strany-i-tohle-se-d%C4%9Bje-%F0%9F%99%82-je%C5%A1t%C4%9B-m%C5%AFj-tip-pro-kandid%C3%A1ty-na-on-line-pohovoru-%C4%8Dekejte-%C5%BEe-v%C3%A1s-budou-cht%C3%ADt-vid%C4%9Bt-je-trochu-zvl%C3%A1

- sdilej zazitky, protoze to pomuze tobe i ostatnim
- zdravi mysli
- reality check
- eticke neeticke chovani
- projekty/ukoly na doma
- standardni prubeh pohovoru, jake ma casti, co se kdy deje
- psotka podcast, kamenistak
- codility
- ruzne hadanky a leetcode, co si o tom myslet, zda to potrebovat, jak se na to pripravit, kontext s USA, whiteboard interviews
- obecne o uzitecnosti algoritmu
- proc firmy neodpovidaji (meme king charles)
- pravidlo 10 pohovoru minimum a pak udelat reality check
- zkouset spis driv nez pozdeji, neni uplne co ztratit, impostor syndrom
- rande, neni to jednostranne, i clovek si vybira firmu, nebrat hned prvni prilezitost, duverovat vlastnimu gut feelingu
- svarc system
- https://metro.co.uk/2019/06/01/boss-shares-coffee-cup-test-uses-every-interview-9771626/


https://github.com/jwasham/coding-interview-university

https://www.hanakonecna.cz/jak-jsem-totalne-zvorala-pohovor/


Jinak k tomu DPH drobnost, limit není těch 80k obratu ale aktuálně 1mil ročně, bude prý až 2mil ročně. PLus to je jen povinost při výdělku u nás nebo v EU. Pokud obrat pochází mimo EU (usa), tak se povinnost DPH nevztahuje.


Dohromady jsem se ozval (nebo se mi ozvali recruiteři) na 17 pozic a z toho bylo 7 pohovorů a z toho byly 2 nabídky práce, takže jsem si ještě mohl vybrat. Bohužel negativní odpověď je většinou mlčení, takže když se vám neozvou ve smluveném čase, můžete si firmu vyškrtnout.

Bezpečná částka je z mé zkušenosti někde mezi 30 a 40k. To klidně zkoušejte.

nesmysly na pohovorech https://darkcoding.net/software/a-day-in-the-life-of-a-professional-software-engineer/

posli ukazku kodu na ktery jste pysni

Tituly a role ve firmách
Tituly podle množství zkušeností
https://github.com/juniorguru/junior.guru/issues/427

kdo je senior medior junior
https://discord.com/channels/769966886598737931/769966887055392768/821353834646601829

Tomáš Arcanis Jílek Obecně řečeno: junior - řekneš mu co, řekneš mu jak mid - řekneš mu co a ví jak senior - ví co i jak

61% of “entry-level” jobs require three or more years of experience. HR departments worldwide must stop such nonsense.
https://twitter.com/simongerman600/status/979327554623557632

Je jedno, s jakými jazyky máš zkušenost a máš se hlásit snad na všechno

U startupů jsem se osobně ptal na kolik měsíců mají peníze na výplaty.

Neni to uplne spatne. Nevidel jsem dve veci "Jak odmitnou nabidku" a dost podstatnou vec "kde hledat praci".

Říkat si o stejné peníze je začátečnická chyba, u každé změny práce je třeba si říct minimálně o 10% navíc nebo se naučit vyjednávat a pochopit svojí hodnotu. Nepřijímat práci kde, slibují zvýšení mzdy po zkušebce, protože s tím často jde tlak na přechod na IČ. Nebrat stáže pokud člověk nemá velmi jasnou představu o své karierní cestě.

https://twitter.com/masylum/status/1375740715758682113

Uvést se na pohovoru
Porovnejte sami. Na pohovoru můžete říct: „Jsem maminka a jen to zkouším.“ Ale také můžete říct: „Jsem absolventka Digitální akademie, teď jsem tři měsíce intenzivně studovala a říkala jsem si, že tohle je skvělá příležitost pro mě. Mám dvě děti, které už odrostly, a teď se chci rozvíjet víc pracovně.“
https://www.czechcrunch.cz/2020/10/nejsme-personalka-pokud-firmy-chteji-vice-zen-musi-je-s-nami-vzdelavat-rika-spoluzakladatelka-czechitas-monika-ptacnikova/

Recruiteri mi nerozumí
https://discord.com/channels/769966886598737931/789107031939481641/885272982438699018

Codility - Codility je platforma na pohovory. Dostaneš nějaký úkol a když ho odevzdáš, je vidět výsledek. Autotesty testují jak funkčnost tak výkonnost. Máš omezený čas na každý úkol a je vidět historie, jestli jsi třeba zkopírovala kus kódu nebo ručně ho napsala. Osobní zkušenosti při pohovorech s tím nemám, zkoušela jsem nějaká cvičení. Úlohy jsou většinou zaměřené na algoritmy a výběr správné datové struktury (výkonnost nad velkým datasetem).

Freelancing: Zmínil bych také paušální daň od příštího roku, kdy odpadá povinnost daňového přiznání. Jinak pěkně napsaný článek :)

zvídavost nejdulezitejsi vec u kandidata, bavi ho to, hrabe se v tom

“Leetcoding”

nechat si poradit od lidí, co dělají něco seniornějšího, než chci dělat, pomůže to odfiltrovat firmy kam nejít.

Some of my favorite resources for prepping for a tech interview:💻 @kyleshevlin 's course on @eggheadio https://t.co/Rx7JJOL6yI💻 @hackerrank 💻 @EducativeInc 💻 @Coderbyte 💻 @exercism_io 💻 @LeetCode— Emma Bostian 🐞 (@EmmaBostian) February 11, 2020
https://twitter.com/EmmaBostian/status/1227233753682104322

Nejvíc lidi juniory zajímají, kdy už má smysl začít hledat si práci, co musí umět 😀
potom nejvíc lidi zajímá na co se budou ptát na pohovoru, respektive ty úkoly praktické, z toho je strach 😀
jo jako ono by stačilo třeba 3 konkrétní příklady jak probíhá pohovor

Víš co mě ještě napadlo, co kdybys dával na svůj web příklady zadání, s kterými se junior může u pohovorů setkat nebo u výběrových řízení ? Že by si tak udělal představu jestli už jsou jeho znalosti dostatečné k tom usi hledat práci. Mě osobně nejvíce demotivuje to, že se úplně šprtám snžím se posouvat mám z toho třeba i dobrý pocit a pak při výběrku dostanu úkol, který nejsem v časovém horizontu schopen splnit protože se nestíhám doučit některé frameworky, které vyžadují  pro použití v kódu. Takhle bych si našel mustr co je třeba se doučit a na jaké úrovni. Možná už to budeš dávat do své knihy. Ale prosím tě to je jen nápad klidně to tam nedávej, nevnucuji ti to. Kdyby tě to zaujalo mám jedno zadání na webscraping.

inzeráty, měnící se požadavky, firma sama neví, co chce
https://trello.com/c/AdKjIdkZ/1380-%C3%BAprava

https://dev.to/macmacky/70-javascript-interview-questions-5gfi?utm_campaign=Juniors%20in%20Tech&utm_…

otazky na pohovoru
https://discord.com/channels/769966886598737931/789107031939481641/908679666649399356

dokázat samostatnost
https://trello.com/c/W66BomqZ/4144-dokazat-samostatnost

Zkusit si s někým pohovor nanečisto.

neber hned prvni nabidku, nerozhoduj se ve stresu, zjisti co je na trhu (Olga)

REDDIT + QUORA: I have applied for over 50 positions, most of which I should be completely or partially qualified for, and I have not received 1 response
https://www.reddit.com/r/jobs/comments/7y8k6p/im_an_exrecruiter_for_some_of_the_top_companies/
https://www.quora.com/I-have-applied-for-over-50-positions-most-of-which-I-should-be-completely-or-partially-qualified-for-and-I-have-not-received-1-response-I-need-to-understand-why-Who-can-I-call-to-find-out-if-there-is-a-problem-with

The Best Medium-Hard Data Analyst SQL Interview Questions
https://quip.com/2gwZArKuWk7W

7 tipů, jak zvládnout online pohovor
https://blog.smitio.com/clanek-7-tipu-na-online-pohovor

https://www.glassdoor.com/Salaries/index.htm

https://www.coursera.org/learn/time-value-of-money

https://www.moneyunder30.com/best-salary-information-websites

https://www.coursera.org/learn/negotiation

https://glebbahmutov.com/blog/help-me-say-yes/

Něco o platech a jak vypadají inzeráty, které obsahují platové rozmezí
https://www.facebook.com/groups/junior.guru/permalink/501500764106869/?comment_id=501739954082950&reply_comment_id=503292073927738

Terka's Candidate Handbook
https://teamaround.notion.site/48e616b977b34dde8db103d0974aef23

Hledáme někoho seniornějšího, hledáme absolventy IT
https://discord.com/channels/769966886598737931/788826407412170752/849588484749656064

https://hbr.org/2014/06/why-women-dont-negotiate-their-job-offers

Mzdy podle smitia 2.0 Část 2: HPP vs. OSVČ
https://blog.smitio.com/clanek-mzdy-podle-smitia-2-0-hpp-vs-osvc

diskuze o zkoušení pohovorů
https://discord.com/channels/769966886598737931/788826407412170752/823163748939595827

Trello s tipy na pohovory pro juniory na frontend
https://trello.com/b/WkFLQwP8/pohovor-na-frontend-developera

banka interview otázek
https://www.tryexponent.com/questions

super diskuze o pohovorech hned na n2kolik doplneni prirucky
https://discord.com/channels/769966886598737931/789107031939481641/832172911422472213

téma - testy jazyka na pohovoru
https://trello.com/c/ZtFMpfHB/2850-t%C3%A9ma-testy-jazyka-na-pohovoru

Udělej si tabulku s pohovory
https://trello.com/c/GlUNbcnU/3829-ud%C4%9Blej-si-tabulku-s-pohovory


--- https://discord.com/channels/769966886598737931/789107031939481641/1102928944392577134
Drobky ze Scrimba Discordu 💡
Jedna dívka z 🇬🇧 sdílela své postřehy, zkušenosti a strategie z příjímacích pohovorů. Mě osobně nejvíce zaujala pasáž o tom, že je dobré si zjistit něco jak o firmě samotné, tak i o technologiích, které firmy inzerují. Zabere to pár desítek minut, ale na pohovorujícího to může udělat dojem. 🙂
---


--- https://discord.com/channels/769966886598737931/864434067968360459/864435350793355284
Já taky vykopnu, mého velmi oblíbeného kouče. Když jsem se připravovala na pohovory, shlídla jsem od něj všechno, co jsem na youtube našla a dost mi to dodalo odvahy. Doporučuju! https://www.youtube.com/watch?v=Nu8j-I8DP-g&list=PLHWSimfGgi3uxRy_SHg344tG8p6Ya1lgL&ab_channel=PavelMoric
---


--- https://discord.com/channels/769966886598737931/769966887055392768/860439257353420820
Já si tady odložím mého velmi oblíbeného kouče, https://www.youtube.com/watch?v=Nu8j-I8DP-g&list=PLotrBczWsvlgxQRf7zJcJwIFC4tuhHxZe&index=5&ab_channel=PavelMoric od 10.minuty. Když jsem se připravovala na pohovory, sjela jsem od něj všechny videa a dost mě to povzbudilo. A chtělo to víc, než jen "neboj se".
---


--- https://discord.com/channels/769966886598737931/788833053425926195/860200758481780757
A ještě někdo jinej psal takovou zkratku:

**Junior**: řekneš mu co, řekneš mu jak
**Medior**: řekneš mu co a ví jak
**Senior**: ví sám co i jak
---


--- https://discord.com/channels/769966886598737931/789107031939481641/1035104757188137014
Obecná poučka je to, co najdeš tady: https://junior.guru/handbook/cv/
1) Napiš seznam toho, co umíš. Bez specifikace „jak moc“.
2) U projektů v CV můžeš v popisu zmínit hlavní použité technologie.
To, co tu řešíme je ale to, že na jaké seš úrovni, se pozná podle těch projektů.
To platí pro začátečníka bez komerční praxe.

To co píše <@539022501876072448> se týká lidí, co už něco mají za sebou a dá se čekat, že pokud třeba 3 roky pracovali ve firmě a dělali tam weby na Djangu, tak umí ledascos, co je k tomu potřeba, na nějaké úrovni. Samozřejmě je dobré si to ověřit na pohovoru potom.
---


--- https://discord.com/channels/769966886598737931/864434067968360459/1024068178554400879
Těmi věcmi, které ovlivnit nejdou jsem myslel (a výčet to asi není úplný)
— hlásil ses na nějakou pozici, ale ta už mezitím zanikla / změnila se a ty se na ni nehodíš
— nesoulad mezi jejich představou a tím, co můžeš nabídnout jako junior (prostě jsi juniornější než čekali) to se nutně hned nepozná předem a i když by někdo řekl, že se na to jde připravit, tak jakoby ano, ale vlastně ne, je tu úroveň _switcher_ a ve firmách, kam se třeba nikdy žádný nehlásil netuší, že existují lidi, co umí tak málo i když na první pohled třeba nevypadají tak nezkušeně.
— nejsi jim sympatický
— máš špatný den, kdy se něco stane a prostě nejsi v náladě / mentální kondici a neukážeš, co umíš
— mají nějaké předsudky
— hledají juniora, protože senioři nejsou a on se během toho řízení přeci jen nějaký přihlásí a dostane holt přednost (skutečný příběh)
— pohovor dělají špatně ti na druhé straně, chtějí po tobě nesmysly, které jim o tobě ve skutečnosti moc neřeknou apod.
---


--- https://discord.com/channels/769966886598737931/864434067968360459/1023737337957589032
4) technicky leader/ vedoucí tymu/ .... který bude na vašem pohovoru -> většinou při dalším pohovornim kole po HR, je pohovor s technicky leaderem který se jednak snaží i zjistit něco o vás (jak se chováte,, jaký jste.. jaké maté rysy).. snaží se zjistit zda budete pasovat do jeho tymu po stránce osobnosti, s tím mu pomáhá otázky od HR. a poté ho bude zajímat váš technicky skill, což odhalí jak třeba nějaký test na papíru tak úkol na vypracovaní.

Muže se stát i to že ty znalosti máte, ale nemáte dostatečné vyjadřovací znalosti (nebo jen velká míra stressu) na to tyto znalosti proti straně přednést a dokázat že je opravdu máte (na to je ale většinou právě ten test, aby tohle odhalilo)
některé firmy ale tyto technicky pohovory mají až po úkolu, a tímto pohovorem se snaží z validovat skill který vychází od úkolu či testu. (takže zde nějaký vyjadřovací block muže velmi ublížit u pohovoru)

no a některé firmy to zase mají naopak.. tedy technicky pohovor a až pak úkol.. zde mi přijde daleko větší šance v přijímacím řízení, protože když například technicky neohromíte na pohovoru, tak stále máte šanci dokázat že na to máte skrz úkol

5) souhra vlastnosti osobnosti a technického skillu: aspoň u mě ta výherní kombinace byla to že na pohovoru jsem zaujal člověka který mě chtěl do tymu, a to hlavně po stránce motivace, a pohledu na svět.. (tohle mi řekl když jsem se ho zpětně zeptal ). po stránce technické si nebyl jisty, protože jsem fyzicky na životopisu nic neměl, krom osobních projektu. takže to rozhodl až úkol na vypracovaní který byl úspěšný. Pak už jen doufal že se neutopím v moři korporátu
---


--- https://discord.com/channels/769966886598737931/864434067968360459/1023737296211693650
> Pohovor se úspěšně povede, když je člověk připraven.
souhlas, taky mě to trošku pobouřilo, když jsem to četl (v duchu jsem si říkal.. no určitě 😄 )

neříkám že připravenost ti nedá plusové body, ale je to jen nějaká malá ovlivnitelná část na pohovoru.

asi bych to shrnul na následující aspekty

1) jak má firma nastavené přijímací řízení -> je velký rozdíl pokud má firma 4 kola které se táhnou celkem měsíc, nebo pokud má jen dvě kola které jsou do jednoho týdne hotové

2) HR / komunikace -> takový první dojem dělá to jak firma komunikuje s novými uchazeči. prvotní odpověď na váš email (či vůbec neodepíšou), nebo naopak zavolají na druhy den a domluví si schůzku.  zažil jsem například HR která mi napsala email že mí v pátek zavolá ohledně výsledku přijímacího řízení, a nakonec po celodenním čekáním v pátek, jsem dostal odpověď a to přes email v 8 večer. Což nedělá zrovna moc dobry dojem o firmě, pak je tu druha strana mince, člověk během těch všech přijímacích řízení nesmí na ně myslet, nesmí byt upření jen na to zda to vyjde nebo ne. pak se o tom zbytečně uvažuje, a psychicky akorát stresuje, kdy konečně dostane odpověď. Každopádně tento aspekt HR jsem zmínil i hlavně proto že HR většinou s vámi má osobně pohovor, a je možné že přes HR do dalšího kola nedáte.
---


--- https://discord.com/channels/769966886598737931/788826190692483082/1011743744812392468
Aktualizoval jsem konečně tabulku, která se pokouší o srovnání peněz OSVČ a peněz zaměstnance s pracovní smlovou pro tento rok.
Najdete ji na adrese https://bit.ly/osvc-v-zamestnanec-2022 a jestli tam najdete nějakou chybu, dejte prosím vědět.
Je to v ní napsané, ale připomenu, že je potřeba si pro vlastní použití udělat kopii.

Vysvětlení co tam je a proč najdete v přednášce.
https://www.youtube.com/watch?v=iJGjTFDYw9A

Díky <@614870427931770900> a <@933738477449785384> za pošťouchnutí
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1002496242456219719
Nepíšou inzeráty s názvem *Junior Developer* ale ani *Senior Developer*, prostě popisujou co a v čem tam budeš dělat, co od tebe čekají. Když se na to začátečník nebo junior cítí, ať se klidně ozve. Pokud chtějí spíš někoho seniornějšího, je to v těch popisech popsané těmi požadavky, ne slovem _senior/junior_.

Když napsali junior, měli problém, že těch začátečníků se hlásilo opravdu hodně a opravdu hodně z nich nebylo na úrovni o kterou by stáli, takže i tímto tomu předcházejí.
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1002114785887916123
Sice opět píšu, co se už psalo, co píše <@668226181769986078> v příručce a psali tu i jiní, ale zkusím to jinak, třeba si začneme rozumět.

1) Označení „junior“, „medior“ nebo „senior“ jsou **obecně** jen velmi hrubá označení
představ si recept na koláč, kde je napsáno místo „200 g“ mouky jen: „trochu“, „středně“ a „hodně“. Slouží k tomu, abys věděla, že něco je víc než něco jiného, ale to je tak vše. Někdo dokonce tvrdí, že to nedává vůbec smysl používat.

2) To označení je obvykle přesněji definované v rámci jedné firmy a slouží to jako ne úplně přesná zkratka aby se nemuselo vypisovat detailně, co ten člověk dělá a jaký má přínos firmě. Takže už tam může být definované, že je to „hrnek mouky“ nebo „hrst mouky“, pořád to nemusí být úplně exaktní a splní to různá množství mouky, ale už je to přesnější.
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1001961604889452598
Hele, co me se tyka, je to "deleni" uplne k prdu a zbytecny, ale kdybych nutne musel rict co pro me znamena rozdil mezi Juniorem/Mediorem/Seniorem/Whateverbullshiterem tak jak s nima interaguju ja, tak je to
 - samostatnost - jak moc detailne musim rozepisovat zadani - srovnej "Naprogramuj backend pro blog" s "Zadani z Appliftingu"
 - empatie k ostatnim - treba jak moc resis, ze to po tobe bude nekdo cist. Vyberes si "genialni one-liner co ma o 2 % lepsi performance" (na neco co se spousti jednou za den), nebo "delsi/vic noob-looking kod, kterej je potencialne pomalejsi, ale za pet let porad presne vis co a proc dela"?
 - znalost domeny - jak moc "delas na svym" vs "jak moc reflektujes zbytek projektu/platformy/..."
 - komunikace - je bozi byt superhero, co se na mesic zavre do komory a na konci z nej vypadne DOOM engine, ale kdyz ten mesic zbytek kolegu nevi co, proc, jak dlouho... delas a treba kvuli tomu stoji... Muzes byt genius, ale to je tak vsecko.
---


--- https://discord.com/channels/769966886598737931/789107031939481641/1001119588462899200
Kdyz jsme u toho everestu - vyprava na Everest stoji minimalne milion a to moc nepocitam cestu, jen material, povoleni, pripravu. Takze na Everest nelezou lidi, kterym je jedno, kam jdou - jsou mnohem obtiznejsi/snazsi/zajimavejsi hory, jedine cim je Everest unikatni je prave ta prestiz toho, ze je nejvetsi/nejznamejsi. Kdyz nekomu reknes, ze si vylezl na druhou nejvetsi horu na svete, nezni to tak dobre, i kdyz kazdy horolezec si z toho sedne na prdel protoze K2 je mnohem narocnejsi vystup.

Myslim, ze to dobre pasuje i na ten FAANG - neznam zadneho skutecne seniorniho vyvojare, ktery by chtel pracovat ve FAANG, vcetne tech, kteri si tim (at uz dobrovolne nebo ne) prosli. Je to takova predstava lidi o tom, co je vrchol IT prace, nez ze by to byl skutecny vrchol.
---


--- https://discord.com/channels/769966886598737931/789107031939481641/999948607002259537
> nebudu dostávat zpětnou vazbu, že byli vybráni blbě
Jasně, pak je to klasickej https://en.wikipedia.org/wiki/Survivorship_bias, ale může to nevadit, když je dost kandidátů.
Sice jsme odmítli i lidi, co by tu mohli pracovat, ale nevadí, máme dost jiných. Akorát to v IT spíš není.

> chci dávat šanci lidem, kteří by ji třeba jinde nedostali
to není nutně charita, ale klidně chytrá strategie, jak si rozšířit množství lidi, mezi kterými hledám (nemluvě o výhodách diverznějších týmů)
Toto nedělá ten obchod aby chudáci introverti mohli nakupovat, ale aby vydělal.
---


--- https://discord.com/channels/769966886598737931/789107031939481641/999920569971642508
Tvoje úvaha předpokládá, že pohovor je vždycky/většinou **správně udělaný**.
Což znamená, že to, co se tam děje, je záměrné ze strany toho, kdo pohovor vede a splňuje to asi takové ty obecné cíle, který by pohovor měl mít:
– vede to k tomu, že o daném člověku zjistí co chtějí zjistit
– že to co chtějí zjistit je to, co je potřeba pro pozici, kterou obsazují (ať už jde o osobní vlastnosti nebo odborné schopnosti nebo cokoli dalšího)
– a že na tom pohovoru chtějí předat co nejlépe informace o té pozici tak, aby se kandidát mohl správně rozhodnout, jestli je tam tam pro něj a nebude z reality rozčarovanej

To by bylo krásný, ale zažil jsem dost pohovorů (na obou stranách barikády), abych neměl iluzi o tom, že to tak **vždy** je.

Vyvozovat z průběhu pohovoru, co hledají může tedy být dost nepřesné. Po projití pohovorem, kde polovina úspěchu bude záviset na tvé schopnosti pohotově reagovat mluvením, tě klidně posadí do openspace s dalšími 30 vývojáři a začneš bušit issues z issue trackeru a mluvit zrovna moc nebudeš…

Spousta lidí dělá spoustu věcí nějak ne protože by se zamysleli, co je problém a jaký je nejlepší způsob řešení jeho řešení, ale prostě tak, že kopíruje co dělají jiní (nebo oni sami v minulosti). Že to může být překonané nebo v daném kontextu nevhodné už neřeší.

Taky se může stát, že firma je fajn, lidi ve vývoji jsou fajn, ale zrovna je nějaká personální krize v HR a pohovory jsou horší, než když nabírali ty fajn lidi… (zažil jsem), takže špatné pohovory nutně neindikují špatnou firmu pro práci celkově nebo ne krátkodobě.

Pokud dotáhu argument <@614870427931770900> do extrému, abych ilustroval ten problém, tak pokud by cool firmy chtěly, abys zahrála slušně na saxofon Giant Steps, než tě přijmou jako vývojáře, tak to nemáš co kritizovat a začneš cvičit. Je to přeci skvělej důkaz toho, že máš výdrž a že tam opravdu chceš.

Pokud mi některé techniky nebo postupy na pohovorech nedávají smysl v naprosté většině kontextů, tak takové pohovory budu označovat za špatné a vidím v tom smysl, protože mi z vyplyne užitečná informace i pro toho, kdo ten pohovor dělal: že ještě víc než jindy jeho úspěch nezávisí na tom, co užitečného pro danou práci umí.
(plus to, co jsem tu už psal, že část lidí tady ty pohovory dělá, takže je ta debata užitečná, protože s tím tedy něco dělat můžou)
---


--- https://discord.com/channels/769966886598737931/789107031939481641/999788038861365248
Z toho plyne, že spíše souhlasím s tezí, že nemá smysl hodnotit pohovory jako dobré vs. špatné - protože do firmy, co špatně pohovoruje, ať už je to "špatně" z jakéhokoli důvodu, člověk stejně nechce 🙂  Nebo má chtít?
Mockrát jste tu psali, že pohovor je rande, kde obě strany zjišťují, jestli se chtějí. Kdyby mě pohovoroval budoucí šéf a bylo to pro mě nepříjemný, proč bych do té firmy měla chtít a vídat toho nepříjemného člověka každý den?

Ad live coding:  nezavrhovala bych to šmahem. Prostě jsou pracovní pozice, kde je potřeba nějaká míra komunikativnosti, a totální introvert, kterému je nejlíp na homeoffice, kdy s nikým 3 dny nepromluví, se na to nemusí hodit; ani on by v tom nebyl šťastnej.

Z vlastní zkušenosti: pohovor na práci, kde teď jsem, zahrnoval live coding. Pohovorující byl maximálně příjemný a povzbuzující, ale i já byla maximálně otevřená v tom smyslu, že jsem se snažila komentovat, co dělám, jak to myslím apod.. A ta výsledná pozice opravdu je hodně o spolupráci a komunikaci s dalšími lidmi v týmu, pro introverta by to fakt nebylo. Takže tady měl tenhle typ "testu extroverze" plné opodstatnění a určitě bych v tomhle případě neříkala, že když to kandidát nedá, tak firma přijde o potenciálně kvalitního člověka. Nepřijde, protože by se na takovou pozici nehodil.

Takže znovu:
Když vám nesedne pohovor, není to o tom, že jste špatní. Je to o tom, že nejste kompatibilní s touhle konkrétní firmou /pozicí. Firem je ale milión a pozic taky. Vždycky se dá najít něco, co klapne.
---


--- https://discord.com/channels/769966886598737931/789107031939481641/999298195182059620
Rozhodne pseudokod. Nebo, pokud to jde, jen funkci kterou "dopisu pozdeji." Tohle delam i v beznem zivote a prijde mi to dobry pristup: "tady potrebuju vyresit XYZ, zavolam tedy `vyres_xyz(data)` a tu dopisu pozdeji, ted potrebuju vymyslet zbytek tohodle kodu"
---


--- https://discord.com/channels/769966886598737931/789107031939481641/999289463081553930
Tipy jak projit (i nesmyslnym) pohovorem, ktere funguji u me:

* mluvit - verbalizovat jak o tom premyslim a co delam/snazim se delat
* otevrene priznat co vim a hlavne co nevim
* ptat se - nejen na zadani a otazky, ale i klidne na technicke veci. Pokud mam google/stack overflow, budu se ptat tam, ale jinak bych se klidne ptal i lidi co vedou ten pohovor
* idealne vztahnout dany problem/otazky na nejakou zkusenost z me historie (na projektu "XYZ" jsme resili neco podobneho a ...)
* kdyz vubec necim, popisu jak bych se to dozvedel, jake kroky bych podnikl abych problem vyresil/zjistil co se da

Celkove proste komunikovat, cim vic, tim lip - je hrozny rozdil kdyz na tabuli/papi/chat napisu  "`podil = celek / cast * 100`" bez pruvodniho komentare a kdyz k tomu reknu "spocitam si kolik procent cini `cast` z `celek`"
---


--- https://discord.com/channels/769966886598737931/789107031939481641/999243598371491910
Ok, za me muze fungovat:
• chci videt jak ten clovek realne koduje, dam mu zadani, nejakej cas at si to castecne sam zpracuje, zorientuje se a pak mi to muze okomentovat, a projdem to a u nejakyho neudelanyho zbytku nebo nejake dalsi ficury, co mu nove k tomuhle zadani pridam, to popisuje, ja koukam jak se s tim umi vyporadat, jak komunikuje.. on mel klid, ja vidim jak funguje
• povidam si s tim clovekem opravdu jako s partakem, "nezkousim ho", tohle se strasne spatne urcuje a bude to i zalezet na tom co a jak ten zajemce vnima, ale ja mam treba ze skoly ted dva zazitky kdy jeden vyucujici se mnou proste ten kod probiral, neformalne, v klidu, nezkousel me, pohoda. Druhej chtel proste slyset neco a ani se nejak nesnazil se k tomu dostat, pritom bych ty principy zvladala, ale to ho nezajinalo. Chtel slyset/videt neco a hotovo. Otazka za zlatyho bludistaka, kterou zkousku mam? :) . Nerikam ze to tady nekdo delare nebo ze dokonce se zlym umyslem, to nemyslim, jen i ta "atmosfera dela hodne"
• asi bych radsi zacala nejakym povidanim a "hledanim" neceho spolecnyho, zajimavejch temat, treba i osobnich, souvisi to s tou atmosferou, zmeni se a ovlivni to me i jeho a i kdyz to nevyjde, tak ten clovek(spis oba) pravdepodobneji odejde s tim ze "jo to je dobrej typek, hezkej pohovor, i kdyz to nevyslo"
• klidne bych pred nejakym tim ukolem rekla, ze je mozna trosku narocnejsi, ale ze to nevadi, ze neni nutny zvladnout vsechno, ze je to tak i udelany a neocekavam, ze to clovek zvladne vsechno, takze v klidu. Samozrejme za predpokladu ze to tak je :D netusim jestli to tak nekdo dela ze zada velkej ukol, ale cloveka to pak desi, kdyz vidi tu hromadu veci. Mnohem klidnejsi budu, kdyz vim, ze to je v pohode neudelat vsechno.  Nic na tom nemeni, ze mi to uz na junior.guru rikali tisickrat, ze nemusim umet vsehcno :)
---


--- https://discord.com/channels/769966886598737931/789107031939481641/999239037187534898
Na "jak zvýšit psychickou odolnost" jsou psaný celý knížky 😄 ale já osobně jsem spíš zastánce toho, že tě zocelují náročné životní situace, které jsi překonal. Je rozdíl mezi eustresem a distresem, eustres je mírný a nabudí tě k lepšímu výkonu, distres už je za hranou a tvůj výkon zhorší. Můj tip na snížení stresu je určitě nácvik. Kognitivně behaviorální terapie vystavování se podnětům, které způsobují úzkost hodně propaguje, a funguje to. Takže poprosit někoho blízkého, ať se mnou simuluje pohovorovou situaci může snížit stres při samotném pohovoru.
---


--- https://discord.com/channels/769966886598737931/789107031939481641/999231195726479360
Několikrát týdně programuju (nahlas) před skupinou lidí s vysvětlováním co a jak a k tomu pár poznámek:
- vždycky si ten kod připravuju (a vlastně ho před nima jen přepisuju, sláva více obrazovek), protože jinak začnu být po chvíli nervózní, zaseknu se a vypadám jak kdybych neuměl do pěti počítat (stalo se mi - skončilo, sedl jsem is k tomu znova a najednou vše šlo).
- na každý pohovor co jsem měl, jsem si kod tak připravil předem s tím že "budete chtít vědět, jak programuju, je mi jasný, není ale lepší vidět něco, na čem už delší dobu pracuju? Něco tu pro vás máím..." a díky bohu jsem nikdy algo na pohovoru dělat nemusel. Obvykle schválně vybírám kod, který není perfektní (řeknu to i předem) s tím, že rovnou ukazuju, jak mám v plánu jej vylepšít. **Zatím to fungovali vždy, tak třeba to někomu pomůže.**
- v kanclu **nenávidím** a když to dávám tučně, je fakt **nenávidím** záda do prostoru. Nejsem schopný **skoro nic ** napsat.

Na druhou stranu, když se seznámím s kolektivem, zapadnu, nemám problém s codereviews, párovým programováním, vůbec ničím takovým. To je úplně jiná disciplína.
---


--- https://discord.com/channels/769966886598737931/789107031939481641/990100877064953856
Chceš ale vlastně vědět, jestli už je máš znalosti na to to zkusit, že?

Takovou informaci ti koukání na ta zadání bohužel nemusí dát, protože nevíš jak na to, co z toho zvládneš budou reagovat v té firmě. Někde mají hodně velká zadání, která „nejdou“ dodělat, chtějí třeba vidět, kam se dostaneš za dva dny a jak to bude vypadat apod.

Neříkám, že se z toho něco nedozvíš, ale dává mi větší smysl udělat si samostatný projekt (tedy ne takový, kterým tě provází nějaký tutorial) a pak to jít zkoušet už na ty pohovory.

Nevíš na co narazíš. Ten proces není nějak standardizovaný jako maturity, firmy jsou různý, dělaj různý věci a lidi v nich jsou taky různí, takže co stačí někde nemusí stačit jinde atd.

Samozřejmě jde i o to, jestli chceš/potřebuješ změnu co nejrychleji nebo je ti jedno, že budeš doma sedět třeba půl roku nebo rok „zbytečně“. Ono i kdybys řekl, že se „to chceš pořádně naučit“ tak si myslím, že po nějakých základech už se stejně rychleji budeš učit ve firmě už jen protože tomu budeš moci věnovat o dost víc času.
---


--- https://discord.com/channels/769966886598737931/789107031939481641/981249271489757194
Junior (switcher) hlavně vezme často první nabídku a ignoruje varovný znamení, který by ve svým oboru pro něj byly stopka.
---


--- https://discord.com/channels/769966886598737931/769966887055392768/975832870344069161
Pozor, tohle je rande, kde partner chybí oběma.
Lidi zoufale nejsou. To, že začátečníci se jim hlásí sami, kdežto seniory musej lovit a prosit neznamená, že maj dost lidí.
Zkus si začít uvědomovat, že dojem musí udělat i na tebe. Dojem v tom, jak se budou věnovat tvému rozvoji a že ti lidsky sednou. Bez toho to nebude fungovat a nemá to smysl ani pro tebe.
---


--- https://discord.com/channels/769966886598737931/769966887055392768/975880401212030976
Přemýšlím, že by možná pomohlo zbavit se mindsetu 'udělat dobrý dojem' a mít nějaká očekávání, ale brát to spíš jako zábavu a pokec - jdu potkat nové lidi a možná to povede někam dál a možná ne. To samozřejmě může platit, pokud nemáš časová a finanční omezení.
---


--- https://discord.com/channels/769966886598737931/769966887055392768/975879339033903154
Být sebevědomý a asertivní neznamená střelit se do nohy. Když ti protistrana položí nepříjemnou otázku, polož jí ji taky.

Např. proč chceš odejít ze stávající práce? Zeptej se jich, proč lidi u nich odchází.  Na otázky ohledně technologií se můžeš zeptat, v jakém stavu mají dokumentaci, jaké mají pokrytí testů, jaký mají poměr manuálních versus autotestů atd.

Když je jedna strana needy, je to hodně cítit, ať už na rande nebo na pohovoru. Jen bacha na lidi, kteří to rádi zneužívají.
---


--- https://discord.com/channels/769966886598737931/788826407412170752/972950345863028737
Strach a vzrušení před prvním zveřejněním životopisu…, před prvním pohovorem…, před nástupem do práce… Už vím, že mě chtějí, mám domluvenou pozici i mzdu, a přece se to první pracovní ráno cítím jako kdybych šla k maturitě. Sevřená nervozitou, plná očekávání. Co se bude dít první den? A co ty dny další?
Obecně je nástupní den hlavně o setkání a poznání prostředí, vyřízení administrace, předání notebooku a mobilu, přidělení práv a přístupů, absolvování prvních „školení“ o firmě, práci, režimu, atd. Informace jsem hltala možná až moc vehementně, nevím proč jsem si myslela, že musím nasadit vražedné tempo a všechno si hned zapamatovat… Měla jsem toho tak plnou hlavu, že jsem v noci neusnula.
Druhý den jsem nastoupila na projekt do jiné společnosti. Takže stejné kolečko co předchozí den: další nové prostředí, setkání, administrace, notebook, školení… někdy jste na tom tak dobře, že přijdete, první den dostanete notebook a smlouvu, druhý den vám zařídí přístupy a vysvětlí práci, a třetí den už přispíváte jako plnohodnotný člen týmu. Mně se ty dny změnily v týdny (slabina korporátů), takže třeba první měsíc jsem dost intenzivně bojovala se strachem z vyhazovu a s pocitem, že jsem tam k ničemu, protože „nic neprogramuji a jen čtu dokumentaci“ k projektu. Ale v týmu se vědělo, že jsem úplný nováček a zaškoluji se na nových technologiích, takže všichni byli klidní, nápomocní a já se postupně uklidňovala taky… Hlavně díky rozhovorům v kuchyňkách a na obědech (které vřele doporučuji), protože jsem se dozvěděla, že i mým kolegům trval proces rozkoukávání dlouho, že je to normální, pochopitelné, že není kam spěchat, mám být v klidu a pokud budou mít pocit, že bych „měla zrychlit“, určitě to jasně řeknou – opadly tak moje obavy, že bych ze dne na den dostala smsku, ať už do práce nechodím. Postupně jsem začala psát kód a těšilo mě, že byl schvalován bez připomínek a s pochvalou, že mi to jde. Takže nevzdávejte to!
---


--- https://discord.com/channels/769966886598737931/788826407412170752/969602675261976666
Toto - https://docs.google.com/spreadsheets/d/1YQkyVqyKeNUyMp7DrY_ayJsUvIZIb_0RMwnCStGA0UE/edit ?

Dnes jsem se na to díval 🙂
---


--- https://discord.com/channels/769966886598737931/789107031939481641/963948141487472650
To je jednoduchý, napíšu ti svůj názor, který jsem si udělal na základě rozhovorů na pohovorech :-).

Junior už něco umí, má třeba rok reálných zkušeností, má za sebou nějaký vlastní projekt (ne tutorial z YT), zná základní principy a umí je použít v praxi, i když stále potřebuje odborný dohled seniornějšího kolegy. Dokáže už firmě přinést nějaký (i když zdaleka ne zásadní) zisk, má přidanou hodnotu, může si už říct zhruba o 40-50.000Kč (=cca 250-300Kč/hod).

Starter má za sebou kurzy, je to samouk. nemá reálné zkušenosti z IT firmy, potřebuje v podstatě full-time vedení - intenzivní mentoring, není vůbec samostatný, nezná procesy ve firmě, prvních pár měsíců až třeba půlroku na něm firma reálně těžce prodělává, nepřináší žádnou přidanou hodnotu, starter stojí mnoho času = peněz a je pro firmu velký otazník, proto mu je spíše nabízená i třeba placená "stáž/akademie" na 1-3 měsíce, na reálnou pozici ještě nastoupit nemůže, nemá na to skill. Finančně je to bída, pohybuje se kolem 150-180Kč/hod, více ani náhodou.
---


--- https://discord.com/channels/769966886598737931/789107031939481641/960760268974075904
https://rainofterra.com/interview-theater-f2d749353422
---


--- https://discord.com/channels/769966886598737931/788826407412170752/960828106032164895
Já myslím, že používat tato označení v inzerátech a vnitrofiremně jsou dvě různé věci s hodně odlišnými důsledky. Junior / mid / senior beru jako orientační a vágní škatulky, podle kterých můžeš zhruba signalizovat, koho hledáš, nebo kdo si myslíš, že jsi, na pracovním trhu. Svět je pestrý, ale beru to tak, že tříbarevný semafor prostě pomáhá v hrubé orientaci a je to aspoň nějaký společný jazyk, i když v důsledku stejně musíš toho člověka vzít na pohovor a zjistit, kým doopravdy je. Nebo musíš na pohovor jít a zjistit, koho doopravdy hledají (jsem v oboru 2 roky, napsali junior, ale nejsem na ně dost zkušený, hmm, asi mají tu laťku ustřelenou, tak co už, jejich problém 🤷‍♂️).
---


--- https://discord.com/channels/769966886598737931/788826407412170752/960643262031482930
Teď jsem slyšel tohle o rozdělení junior / mid / senior a přišlo mi to dobrý 🙂 Několikrát se to tu řešilo, tak koho to zajímá, přijde mi tento díl jako dobry odrazový mustek k orientaci https://overcast.fm/+U67H-Wc10
---


--- https://discord.com/channels/769966886598737931/789107031939481641/946297939922387024
_Career switcher_ je za mě člověk, který se rekvalifikuje z jiného oboru. Typicky v pozdějším věku, má už něco za sebou v životě i práci a ve vetsine případu to nedělá skrze studium VS, ale samostudium nebo kurzy. Nedaval bych _career switcher_ a _junior_ na stejnou osu, to první proste popisuje cestu, jakou se ten člověk dostal do oboru a nějaké stereotypy, které se k tomu vážou. Podobně muže byt _absolvent_, čímž se typicky mysli někdo, kdo má relevantni VŠ. Ve vetsine případu se tím mysli někdo, kdo ji vystudoval zrovna teď a nemá zatím moc další praxe. Opět to popisuje především tu cestu a nějaká očekávání, stereotypy vážící se ke studentům, atd.

Pak je _entry level_, to je označení pozic pro úplné začátečníky bez praxe. Pak _junior_. Kde jsou hranice těchto pojmů je vždy na každé firmě, jsou to jen orientační pojmy z HR a jsou vágní, nemají definici. Já vědomě a záměrně říkám _junior_ lidem bez praxe a tlačím firmy spis k tomu, aby měly nároku méně než více. Ten začátek je nejlépe pojmenovatelny a nesnáze se na tom všichni shodneme, zároveň je to podle mě adekvatni očekávání v dnešní době, kdy na trhu není snadné najít lidi i s minimální praxí 🤷‍♂️
---


--- https://discord.com/channels/769966886598737931/788826407412170752/941264446725173259
Rekl bych, ze lide s praxi jsou vic v pohode, maji vice nabidek, a uz vedi, do ceho jit nechteji. Oproti tomu junior je nervozni, ze ho nikdo nechce, tak vezme prvni nabidku co prijde - a bez pracovni zkusenosti jeste nemuze vedet, na co si ma dat pri vyberu prace v novem oboru pozor.
---


--- https://discord.com/channels/769966886598737931/788826407412170752/941265372617773056
Napada mne jedna prakticka rada - pri pohovoru trvat na tom, ze chci mluvit se svym budoucim mentorem?
---


--- https://discord.com/channels/769966886598737931/788826407412170752/941265433300983828
Chtít po nich aby tě tam před přijetím provedli a ukázali na čem budeš dělat asi taky není reálný požadavek pro juniora co? 😄
---


--- https://discord.com/channels/769966886598737931/788826407412170752/916443586302738432
tak pak bych čekal pěkné podrobné zadání, kolega mi to nedáno vysvětloval na příkladu: "potřebuješ stůl"
Zadání pro seniora: "Potřebuji stůl" a on se o to postará a máš stůl
Zadání pro mediora: "Potřebuji ten a ten stůl z IKEA"
Zadání pro juniora: "Potřebuji ten a ten stůl z IKEA Zličín, Částku xy si vezmi na recepci. Do IKEA pojedeš tramvají 1, na zastávce ABC přestoupíš na metro směr Zličín, tam vystoupíš, z nástupiště 3 pojedeš busem....."
---


--- https://discord.com/channels/769966886598737931/788832177135026197/910436103838912532
Kdyby chtěl někdo něco programovat 😉
<:python:842331892091322389> <:javascript:842329110293381142> <:java:847749733664555018>
Vypadá, že to je zadarmo.
https://www.codecademy.com/code-challenges
> With technical interviews, practice makes perfect. Now, you can practice real code challenges from actual interviews to see how your skills stack up. If you get stuck, we’ll point you to what you still need to learn.
Nevím, jestli se v českém prostředí tohle objevuje u pohovorů, ale jako cvičení to pro někoho může být zajímavý.
---


--- https://discord.com/channels/769966886598737931/1099057355620106342/1099665136341487666
A zhruba polovina poslala zamítnutí na základě CV.
Asi 15–20 vůbec neodepsalo. (10–20 %)
---


--- https://discord.com/channels/769966886598737931/1075541542669922424/1099426281302528103
Chápu, že to není cesta pro každého, ale pohovory se pro mě radikálně změnily tím, že jsem si zažil druhou stranu barikády a pochopil tak víc její motivace a postupy. Najednou z toho nebyl neznámej bubák a stres.
Snažím se to tady opakovaně předat, ale nevím jestli se to daří.

Časté je vnímání jako zkoušky někde na VŠ, kterou je potřeba nějak prolézt, kde bude někdo prověřovat, zda máš nějaké znalosti, které se jde případně nahučet pár dní předtím a zase zapomenout. To ale vůbec nedává smysl.

Lepší přirovnání mi přijde první rande, je možné, že o ten vztah jeden z nich stojí víc, ale je to prostě začátek vztahu, často na dobu neurčitou a obě strany po prvním oťukání přes inzerát na jedné straně a screening / CV / projekty na GitHubu na straně druhé zjišťujou, jestli by delší vztah mohl fungovat. Někdy je na to potřeba víc schůzek (kol).

Ti, kteří hledají lidi, je chtějí co nejrychleji a nejsnadněji najít, ale nechtějí se trefit vedle.
Nemají potřebu nikoho potápět, ponižovat nebo zbytečně tahat přes více kol.
Já se před každým pohovorem „modlil“, aby konečně po těch týdnech a měsících přišel někdo, koho můžem bez výhrad vzít…

Samozřejmě píšu o ideálu.
Jako u všeho platí, že 90 % všeho jsou sračky, takže spousta lidí to dělá blbě nebo musí jet podle nějakých pitomých procesů atd. Ale i to je něco, co zjišťuješ ty, jako kandidát o firmě. Jak to tam chodí a jestli chceš s takovými lidmi pak řešit něco dalšího.
---


--- https://discord.com/channels/769966886598737931/789087476072710174/1090957362438869092
🆓 <:shutupandtakemymoney:842465302783590441> **Kalkulačka pro přepočet mezi OSVČ a zaměstnancem** aktualizovaná pro letošní rok.
Má to svoje limity, které tam snad vysvětluju, ale umí to letošní dvě sazby paušální daně apod.

Pokud jste neviděli, je dobré pro pochopení vidět https://www.youtube.com/watch?v=iJGjTFDYw9A

Link na tabulku https://bit.ly/osvc-v-zamestnanec-2023

_🙏 Díky <@380388619061559299> a <@614870427931770900> za feedback, který mě donutil nad tím po letech přemýšlet a opravit ~~nepřesnost~~ chybu <a:thisisfinefire:976193331975557260> (i proto už ty starší tabulky nenajdete <a:awkward:985064290044223488> )_
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1088537642758574150
Tak mě dneska napadlo: Když je práce na částečný úvazek, pro přehlednost se bavme o polovičním, jak dojdete k výpočtu své ceny? Čistě polovinu toho, co byste si řekli za plný?
---


--- https://discord.com/channels/769966886598737931/1031588279532933223/1080435541738258434
2023 update, rekl bych ze  junior, ktery umi kodit, si muze momentalne rict neco mezi 40 a 50k hrubeho, smaozrejme zalezi na lokalite a firme 🙂
---


--- https://discord.com/channels/769966886598737931/1087647522157232139/1087667419880894545
Tohle už možná píšu zbytečně (nepředpokládám, že bys vždycky čekala na odpověď, a až pak psala do jiné firmy), ale podle mě lepší zmínit než nezmínit 🙂 Dokud není práce tak kontaktovat a kontaktovat (další firmy) bez ohledu na to jestli někdo odpovídá, nebo ne. Samozřejmě, bavíme se jen o relevantní pracovních nabídkách. Když nevidím relevantní pracovní nabídky tak hledám, hledám, a pak kontaktuju 😀 Ideální je mít nějaký cíl, např. odpovím na X pracovních nabídek týdně dokud nebudu mít domluvenou práci. To "čekání" na odpovědi se pak stane naprosto irelevantní, jen třeba si poznamenat, kam už jsem psal/a a jestli někdo z firmy odpověděl atd.
---


--- https://discord.com/channels/769966886598737931/1087647522157232139/1087652565954592828
To může být různé. Pro sebe jsem si určil limit dva týdny a jeden až dva týdny mi přijde jako "normální" doba. Když mi do dvou týdnů nikdo neodpověděl, tak jsem kontaktoval přímo jejich HR/osobu uvedenou u pracovního inzerátu. Když ani to nepomohlo, tak jsem si u firmy udělal značku, že nereagují, a že už tu firmu nebudu řešit. Mimochodem, s takovým cejchem u mě skončily jenom dvě firmy z necelých třiceti. Vedl jsem si přehled všech firem, kam jsem napsal, a případně i jak probíhal následný proces - jen pro vysvětlení 🙂
---


--- https://discord.com/channels/769966886598737931/1083418245266165880/1084778814246244393
Pokud jako OSVČ ajťák uzavíráš smlouvu s odběratelem, limitace náhrady újmy je obecně na dohodě smluvních stran.

Zákon v tomhle dává jen následující mantinely, kdy nelze omezit újmu:
- způsobenou úmyslně nebo z hrubé nedbalosti;
- na přirozených právech člověka (ochrana osobnosti, důstojnosti, života, zdraví...);
- způsobenou smluvní straně (tzn. typicky pokud by odběratel byl v pozici spotřebitele, což v praxi asi tolik nebývá).

V ostatních případech jde skutečně jen o to, na čem se smluvní strany dohodnou. Obvykle se nastavuje nějaká horní hranice, ať už fixní částkou, nebo třeba procentem z ceny.

např. *„Dodavatel odpovídá za škodu, která vznikne objednateli v souvislosti s plněním podle této smlouvy maximálně do výše XXXXX Kč.“*

Lze to pak různě modifikovat, např. stanovit různé limity pro různé situace, když třeba předem upozorníš, že škoda může vzniknout atd.

Co se týče ručení celým majetkem, teoreticky se ještě jako alternativa nabízí založení s.r.o., ale jasně, že prakticky to není úplně ideální řešení. 🙂
---


--- https://discord.com/channels/769966886598737931/1071014984819167283/1071112669672788018
Nepytas sa uplne na to, ale prihodim ako to funguje u nas. Najprv ma s uchadzacom call HR a potom automaticky dostane task alebo sa medzi HR call a task dostane kratky uvodny meeting s mojim manazerom a nasledne potom sa cloveku posle task na vypracovanie. Na tom meetingu vobec neviem co riesia, ci sa pozeraju na nejake ukazky prace, ja som bola pritomna iba na tych dalsich viac technickych kolach.

Ten nas task ma vacsinou 3 casti - prva je manualna a cielom je vytvorit testovacie scenaria na nejaku feature na nasej stranke. Byvaju tam rozne obmeny ako maju tie scenaria vyzerat, aku maju mat formu atd. Druha je hladanie bugov na stagingu, ktory vytvorili developeri - naposledy som pripravila list s cca 20 bugmi (vizualne, funkcionalne, niektore boli iba pre mobile) a developer upravil kod, aby tam tie bugy boli. Casto tie bugy ludia ani nenajdu, ale naopak najdu realne bugy, ktore mame na stranke. To je vzdy plus. Tretia cast je automatizacia, kde casto byva ulohou zautomatizovat scenaria z prvej ulohy, ale niekedy je to separatne. V podstate tento task musi urobit kazdy a nepozerame sa na to, ci ma nieco ine na ukazku. Ale na druhu stranu, iba raz sa stalo, ze ten clovek nieco mal - bol to clovek, ktory vedel aj programovat a mal nejaku svoju stranku, na ktoru napisal testy.

Aby som ti teda odpovedala, myslim ze ide mat nieco ako tester na ukazku. Ovplyvnena tym nasim taskom - asi by som zacala tym, ze by som si vybrala nejaku stranku, ktora je vseobecne znama, aby to bolo jednoduchsie pre vsetkych, vybrala by som si tam nejaku feature a k tomu by som napisala nejake testovacie scenaria, ako by som tu feature otestovala manualne. A potom by som k tomu napisala nejake testy, asi podla tych scenarii.
---


--- https://discord.com/channels/769966886598737931/1066992347725971516/1067089251595984947
Nabídky s požadavkem na 1-2 roky praxe bych nepřeskakoval, ale zkusil začít motivační dopis takhle:

> Vím, že požadujete 1-2 roky praxe a já narovinu píšu, že je nemám. Vytvořila jsem ale sama dva větší projekty (odkazy v přiloženém CV), které si můžete prohlédnout a sami usoudit, kolik práce by pro vás bylo doučit mě věci, které potřebujete.
---


--- https://discord.com/channels/769966886598737931/1054800634345422868/1054805319026491392
**G)** Ještě bych dodal **srovnání priorit**. Ideálně mít připravenou optimální a minimální mzdu, za kterou jsem ochoten pracovat, jak moc jsem flexibilní, jestli zvládnu pracovat převážně z HO apod. U dojíždění je například nejlepší si vážně zkusit jet do kanclu v době, kdy bych tam jezdil, a způsobem, jakým bych se tam dopravoval. Pro někoho může hrát velkou roli styl spolupráce, složení týmu a tak. Já se třeba v jednom procesu zaměřoval furt na technickou stránku věci, ale unikaly mi pak některý detaily.
---


--- https://discord.com/channels/769966886598737931/1049592405378224148/1049592407274029076
👗 Napadlo mě toto téma, protože vlastně nikdy moc nevím, jestli se mám na offline pohovory nějak strojit (na online snad stačí, že nejsem nahoře v pyžamu a jsem nějak učesaná), abych udělala dobrý dojem. Sama to mám tak, že šaty skoro nenosím a spíš tíhnu k tričku, kalhotám a teniskám. Formálněji se obléct mi přijde nepohodlné, zvlášť když musím být v tom oblečení celý den. Je potřeba tohle nějak u IT pohovorů řešit? Zatím neřeším nic. Ale v některých korporátech mají dress code a s tím nejsem obeznámená absolutně vůbec.
---


--- https://discord.com/channels/769966886598737931/1006604070972305580/1006622957013053570
Fakt to nevidím jako selhání na tvý straně, přijde mi to naopak jako úspěch, že si tím neztratila víc času.
U juniorů jsou ukončení ve zkušebce o hodně běžnější protože je to častěji průzkum bojem.
---


--- https://discord.com/channels/769966886598737931/967847510234234972/967899831420981329
*"Nejsem čokoláda, nemůžu se zavděčit každému."* (citát)
---


https://www.reddit.com/r/ChatGPT/comments/143ubjs/as_a_recruiter_i_feel_like_i_can_tell_when/


--- https://discord.com/channels/769966886598737931/788826407412170752/1119307390576230492
Petra Nulíčková měla hromadu skvělých tipů na meetupu ReactGirls před měsícem a tady je to na záznamu
https://www.youtube.com/watch?v=uNL3yEzNsbQ
---


--- https://discord.com/channels/769966886598737931/991010207280807986/1119153375347478548
Přemýšlím tu o té zprávě od chvíle, co tu visí, až doteď 🙂 Nejsme úplně společnost, co bere běžně juniory. Ale tu a tam se k nám dostanou a přemýšlel jsem, proč jsme kdy koho pustili (a to přemýšlení mi zabralo tolik času 😀 ).

Jednoznačně bych řekl, že tak z 90 % jsou důvodem měkké schopnosti (soft skills). Nebo vlastně spíše neschopnosti. Nespolehlivost. Neochota nést zodpovědnost za svou práci (nikomu netrháme hlavu, chyby děláme všichni). Obtížná komunikace, vyhnívání mailů a úkolů. Nezeptám se, když mám problém, nekonzultuju návrh s jinými. Konzultuju s jinými, dostanu radu a stejně si to udělám po svém. Nepřijdu do práce a nikdo neví proč. Nepřijdu do práce první den a nikdy se už neozvu (tak u toho vlastně nevím, zda jsme ho pustili a nebo zda nepustil spíše on nás). Někdy možná i nějaké osobní naladění s lidmi v týmu, prostě jsme si lidsky nesedli.

Těch 10 % jsou pak ty znalosti a posouvání se v nich. Každý nemusí být rock star a pokud je na něj spoleh a lehké úkoly zvládá dobře a precizně, může z něj být dobrý "analytik lehčích úkolů" a může to tak být na dlouho, i věčně. Já sám pracuji ve velmi těžké a komplikované doméně. Ty znalosti se ale nestaly za víkend. Mám pochopení pro lidi, kteří se je chtějí naučit a vím, že to bude na dlouho, i roky (ocením pokoru). Mám pochopení i pro ty, co se zastaví v polovině a řeknou, že takto jim to stačí. Pokud pomáhám někomu v učení, stojí mě to nemalou energii navíc. Musím vidět, že to k něčemu je, že to nebylo zbytečné.

Nutno říct, že pro absenci elementárních pracovních soft skills jsme pustili i mnoho nejuniorů.
---


---
To se obávám, že takhle prostě funguje, a to i pro seniory. Akorát ti mají většinou celkem dost, tak to tolik možná neřeší, dlouho pracují na jednom místě za stejné peníze a pak se chytnou za čelo, když si povídají u piva s nějakými kámoši a vyjde najevo, že dělají za mzdu hodně pod aktuálním průměrem. Moderní firmy mají salary ranges apod., snaží se to trochu řešit, ale většina podle mě řeší růst mezd individuálně a holt kdo se necuká, ten zůstane na penězích, které mu „stačí“.

A když to chce člověk cíleně řešit a teda tlačí na to, aby se spolu s posouváním znalostí a zkušeností posouval i mzdově, tak na to firma většinou není připravená, přesně jak píšeš. Zvlášť juniory často naberou i proto, že jsou levní, a vlastně paradoxně nevědí co s nimi, když jim vyrostou a měli by je začít ohodnocovat standardně. Je to boj. A mnohdy je prostě jednodušší odejít jinam, kde ti to dají rovnou. A firmy si za to můžou samy.

Jediná cesta ven je dostat se na peníze, kdy už je ti jedno, jestli máš o 10.000 Kč víc nebo míň, a můžeš se zamýšlet víc nad tím, jestli tě to ve firmě baví, jaký tam je tým, apod. Pak třeba někde zůstaneš dlouho a na menších penězích, ale je ti to doopravdy jedno, protože peněz máš dost a víš, že si tam vážíš jiných výhod.
---


--- https://discord.com/channels/769966886598737931/789107031939481641/1134507945871286293
Vyšla „příručka“ o tom, jak vyjednávat o mzdě nebo platu na pohovoru. Je tam toho strašně moc a pro programátory nebo testery nemusí být všechno relevantní, ale i tak to bude dobrý zdroj pro někoho, kdo by se chtěl do tématu ponořit 🙂 💰 https://www.careerdesigner.cz/penize
---


--- https://discord.com/channels/769966886598737931/789107031939481641/1128788664244244601
Zažívám teď hodně turbulentní pracovní vývoj a nemám to ještě zpracované, ale je tu jedna lekce, kterou už mohu sdílet (a chci to udělat, dokud je to drsně čerstvé):
**když slyšíte u pohovoru charakteristiku (jaká je to firma; na čem se pracuje; co se využívá za technologie), doptejte se na konkrétní činy (pátrejte po důkazech)**

Slyšela jsem to víckrát v podcastech, ale na pohovoru jsem se tak zaměřovala na svůj výkon, že jsem povolila, pokud šlo o kritický přístup k informacím z druhé strany. Ani ve snu mě přitom nenapadlo, jak moc se mohou lišit říkaná slova, resp. představa, kterou ve mně vyvolávají, od reality. Zejména jsem podcenila skutečnost, že druhá strana bude lidsky inklinovat k popisu kýženého stavu (místo reality)... A že nemusím být ve všem ten nejjuniornější člověk v místnosti (přestože vím tak tři a půl věci).

Takhle to zní triviálně, ale je to věda. Základní pravidlo, které si odnáším: **Minulý čas (udělali jsme, zkusili jsme, použili jsme) je přítel**. Je to trochu neintuitivní, protože jinak je pohovor spíš plný samých *budů*, *budeteů* a *bylbychů*.

Já se třeba měla zeptat takhle:
* Co byl v dané oblasti poslední projekt týmu, do kterého bych se přidala? Měli jste v týmu už stážisty/juniory, na čem pracovali?
* Byla zmíněna technologie XYZ - jaké s ní doposud máte vy sami zkušenosti, potýkáte se s nějakými problémy a budu mít k ruce někoho seniorního, pokud budu mít problém např. s (ideálně konkrétní věc)?
* Můžete mi říct více o tom, jak jste vymezili úkol a primární cíl projektu / technologie / rozpočet na výpočetní výkon / reportování výsledků / jaké máte připravené datasety a data / co bude baseline při evaluaci výsledků /...?

Třeba bych dříve poznala, že to nikdo předtím nedělal, není tam na to nikdo seniorní ani mediorní, jsou zcela nereálné představy zhruba o všem, chybí infrastruktura i smysluplný mindset. Bylo mi to jasné hned první den (i zde jen vyvozením z toho, co bylo o projektu řečeno) = šlo to odhalit už při pohovoru...
---


--- https://discord.com/channels/769966886598737931/789107031939481641/1128259545270075465
Slyšel jsem teď u vaření oběda tohle s <@839123616665698354> a <@973649232554782820> a bylo to pěkný! Ani s vysokou školou v kapse nemusí být přímočaré najít si první programátorskou práci. Alica mluví o tom, co jí pomohlo vydržet a jak se k hledání práce postavit. https://www.programhrovani.cz/1843229/12680902-dev-stories-7-alica-kacengova-panaxeo-a-jeji-restarty-v-it
---


--- https://discord.com/channels/769966886598737931/789107031939481641/1125433335699742842
Dojmy z dnešního pohovoru (FE - React):
1) Senior programátor fajn a příjemný. (dost to pomůže proti úvodnímu stresu)
2) I když některé koncepty "tak nějak znám" (immutability) tak na přímou otázku nejsem schopen rychle a přímo odpovědět. I u jednodušších otázek jsem asi zněl dost nejistě. Zvlášť pro lidi co se učí na vlastní pěst jako já, je asi fajn v rámci přípravy "vysvětlovat koncepty gumové kachničce".
3) Otázky typu: srovnání let var const; co jsou hooks; proč použít react...
4) Jo a ještě otázky na git (základy: checkout, merge vs rebase).

Možná mě ještě napadá: U otevřených otázek se doptávejte. Výhody Reaktu je otázka, která může znamenat ledacos. Výhody oproti čemu? Plain JS, nebo oproti Angular a Vue js? Můžete se pak nepotkat s očekávanou odpovědí...
---


--- https://discord.com/channels/769966886598737931/789107031939481641/1124759853559185471
jasné chápu, samozřejmě každou situaci je potřeba řešit na míru. Mě se akorát vyplatilo si tu svojí "na míru" vytvořit. Třeba jsem se před časem s někým bavil že neví co by do takového inzerátu napsal. Ale po pár minutách rozhovoru jsem zjistil, že má kvalitní angličtinu, že má za sebou nějaké zkušenosti které se dají napsat rozhodně jako plus z pohledu zaměstnavatel/zaměstnanec a že by se to nějak vymyslet dalo.

Mě nepřijdou sociální sítě na slepo, pokud člověk vyloženě píše do vhodných skupin a míst. Já psal asi do pěti facebookových českých a slovenských programátorských skupin. Určitě je dobré zmínit i technické skilly. Mě se vyplatilo nic si nevymýšlet, ale zároveň podávat informace pozitivním způsobem - tohle umím (ne tamto všechno ještě neumím :)).

U mě teda bylo nejdůležitější že jsem měl celkem jasnou představu co hledám a věděl jsem že přes to nejede vlak. Tím se zůžil můj fokus a spoustu jsem toho filroval (nejen na sociálních sítích) ale zase tam kde to vypadalo nadějně jsem se fakt snažil :)).

Nedokážu říct jestli ti to takhle dokáže pomoct. Můžu ti třeba poslat ten svůj inzerát do zprávy (nechce se mi ho teďka vyřezávat a dávat ho sem znova). Ale držím palce! :))
---


https://twitter.com/EmilyKager/status/1315837993513492480


--- https://discord.com/channels/769966886598737931/788826407412170752/1164528096851017841
Od října do konce roku se nábor často zpomaluje, nebo úplně zastavuje, podle toho, jak je na tom firma s budgetem na daný rok. Pracoval jsem v IT náboru + teď jsem podobné věci řešil ve firmě. To tomu taky nepomáhá... Já si třeba minulý rok domluvil práci právě v této době, ale taky se začátkem až v únoru.
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1162265111055048775
vytahuju ven citát od <@852528987208024074> z <#1160119402369384498>
> ideálne je sa už rovno na pohovore spýtať v akom stave u nich momentálne je ak je ponuka písaná ako hybrid

Myslím, že tohle platí obecně.

Chcete hlavně programovat v Reactu, ale „zatím budete hlavně psát CSS a víc Reactu časem“? Zeptejte se kolik toho v Reactu aktuálně dělají nebo za poslední půl roku dělali, možná zjistíte, že je to „spíš jako v plánu“ a tedy vůbec není jisté, jestli to půjde. Jasně, třeba tu práci vezmete jako první zkušenost tak jako tak, ale nebudete za pár měsíců frustrovaní z toho, že jste se ještě k Reactu nedostali.
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1147104452650741791
Když bych si jako junior hledala novou práci, na co si dát pozor? Jak naznačoval <@652142810291765248>  v jednom komentáři "Jasně, určitě neber cokoli. Proklepáváš si firmu i ty. Junioři, zvlášť u první práce, na to často zapomínaj a pak je z toho mrzení." Máte nějaké negativní osobní zkušenosti?
---


--- https://discord.com/channels/769966886598737931/1085592788676120636/1143825015171723304
Body pro sebe: pohovorování je extrémně náhodné. Pohovory, ze kterých mám dobrý pocit jsou často negativní a naopak. Nikdy nevím, co bude "ta správná" informace, co je zaujme.

Umím skvěle předstírat, že nejsem nervózní a když proti mne sedí lidi s ještě mizernějším sociálním skillem, vypadá to pro mne dobře.

Naďšení a chuť se učit vypadají opravdu jako klíčové věci pro juniora.

Přesvědčovací bod může být něco, co oni využijí, ale nikdo u nich nedělá/nechce dělat a já si to přináším z předchozích zkušeností.
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1172808574221701180
Nicméně junior.guru vydal několik příruček, jak na první práce. A tento e-book je sice z jiného zdroje, ale speciálně o financích a je skvěle zpracovaný 💸

https://www.careerdesigner.cz/penize
---


--- https://discord.com/channels/769966886598737931/1194368531433783407/1194921225189859368
Ahoj, tak za mne rikam NE NE NE NE a jeste milionkrat NE!!!!

Pripad Tatanka ma tu spojitost, ze mel take kamarada a (spolu)majitele firmy a ze to samo o sobe NEZNAMENA, ze to vzdy musi dobre dopadnout.
Nechci rozebirat davno uzavrene a zhojene historie, takze jenom vecne a konstruktivne:

I kdyz je kamarad, do tve hlavy nevidi, a tvoje ucebni/pracovni schopnosti znat nemusi.
To, co ti nabizi je "postav mi zadarmo stodolu, a kdyz se to dobre naucis (o cemz rozhodnu ja a ty mas malou sanci to ovlivnit), zaplatim ti, abys mi postavil i barak".
Kazdy kope za sebe, coz je uplne prirozena lidska vlastnost.
---

https://karierko.cz/clanek/petra-co-cekat-na-pohovoru/
https://www.platy.cz/


--- https://discord.com/channels/769966886598737931/788826407412170752/1208794856709824552
https://www.lukaspitra.cz/10-zkusenosti-z-naboru-200-lidi/
---


--- https://discord.com/channels/769966886598737931/789107031939481641/1210341399250341888
Tohle je sice pro zkušené programátory, ale myslím, že tam jsou zajímavé rady i pro leckterého juniora. https://newsletter.pragmaticengineer.com/p/finding-the-next-company
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1223220648957186070
Firmy nemají sdílenou představu ani o tom kdo je vůbec junior, takže asi tolik k jakýmkoliv složitějším konstruktům 😅
---


--- https://discord.com/channels/769966886598737931/1222105029851484250/1222127360116264982
> má to rizika, ale s tím počítám
Já bych napsal, že si (už) můžeš dovolit s tím počítat. Něco sis třeba naspořila, tvoje cena na trhu vzrostla, protože toho umíš víc, a když tě někdo vyhodí ze dne na den, tak chvíli vydržíš a práci asi najdeš. Což je fér a přesně takhle většina IT v Česku funguje. Ale pro mnoho juniorů bude chvíli trvat, než se do téhle pozice dostanou, protože jsou po rekvalifikaci v situaci, že by je taková událost akorát dorazila.
---


--- https://discord.com/channels/769966886598737931/1231221825665499156/1231459291165102194
V tom shrnutí od <@668226181769986078> jsou spíš obecné nevýhody té právní formy.
---


Peníze:
https://blog.pragmaticengineer.com/software-engineering-salaries-in-the-netherlands-and-europe/
https://trello.com/1/cards/634d7ed102a75102f33dca4e/attachments/634d7ed202a75102f33dcc6f/download/H1_2022-Salary-guide-CZ.pdf


--- https://discord.com/channels/769966886598737931/1288193728087064740/1303817228973772944
Motivační/průvodní dopis:

Dobrý den,
reaguji na pozici… Bohužel aplikace z předchozích zaměstnání nejsou veřejně dostupné a jejich kód není open-source ani source-available. Nemám ani právo sdílet kód jinak, ale rád s vámi na pohovoru proberu technické problémy a možná řešení, na která jsem u projektů tohoto typu narazil. V CV najdete obecné popisy toho, co jsem dělal a jaké k tomu používal technologie. Pokud je kód, který u vás píšete, k dispozici veřejně na GitHubu, ocením odkaz, rád se podívám, jaké nástroje a postupy používáte. Bohužel hledání NázevFirmy mi nic nenašlo.
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1301606738331435088
o úkolech v přijímacích řízeních

> Nenechte se odradit, pokud budete muset vypracovat úkol. U každé firmy a pozice je to jiné, ale pokud vám na konkrétní firmě opravdu záleží, úkol vypracujte i když chápu, že je to žrout času. Důležité je mít transparentní informace o tom, jak bude úkol hodnocen a jakou roli hraje ve výběrovém řízení. Úkoly jsou běžné zejména pro juniorní pozice, ale mohou se vyskytnout i u seniorních pozic.
>
> Pokud narazíte na zadání, které zahrnuje technologii, kterou zcela neovládáte, komunikujte to. Napište, že se ji budete snažit doučit nebo že potřebujete více času. U našich klientů se například stalo, že zadavatel ocenil komunikaci kandidáta a přizpůsobil úkol jeho znalostem.
>
> Komunikace je klíčová. Dejte vědět, že úkol přijímáte, nebo že budete potřebovat více času kvůli pracovním, studijním nebo rodinným závazkům. Většina firem to pochopí, a pokud je výběrové řízení urgentní, dají vám vědět, ať úkol neřešíte a neztrácíte čas.
>
> Závěrem bych řekla: chovejte se k firmám tak, jak chcete, aby se chovaly k vám. Možná narazíte, ale začněte u sebe. Když očekáváte zpětnou vazbu a transparentnost, jděte příkladem. Pokud firma vaše úsilí neocení, zkuste to jinde. Věřím, že existuje firma, kde budete spokojení. Vysílejte energii, kterou chcete zpět. Podle mě je to hlavní klíč k úspěchu.
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1301863841486999652
Když se vrátím k původnímu problému, kterým to <@1012083835892138074> otevřela:

Zaměstnanecký poměr nabízí menší rizika, aniž o tom musel zaměstnanec moc přemýšlet.
Potenciálních háčků je mnohem méně a funguje to víceméně tak, jak lidi očekávají.

U OSVČ (ve smyslu švarc) je potřeba si **všechno** ohlídat a spočítat a to i s ohledem na realitu.
Tím myslím to, jakou sílu ve vyjednávání máš v různých situacích, které můžou nastat.

Když si budeš vědoma rozdílů a nastavíš si podle toho jak svoje očekávání, tak podmínky spolupráce, tak do toho klidně jdi.
---


--- https://discord.com/channels/769966886598737931/789107031939481641/1294323134924718102
Ano, to je samozřejmě možné, že se tak dozví věk, ale stačí se podívat na LI (nevím jestli v CV máš, kdy jsi studovala VŠ) a i kdyby ti nějak bylo 18, když jsi začla, tak z toho zjistím, že ses narodila v roce 1989 nejpozději, takže nějakou představu (bez ohledu na vzhled) si udělají stejně. A rok, dva, tři navíc už asi není rozdíl z tohoto pohledu. 🤷‍♂️
---


--- https://discord.com/channels/769966886598737931/789107031939481641/1301975275982291028
Nejen junioři zažívají pohovory, který jim nedávaj smysl: https://www.linkedin.com/posts/tom%C3%A1%C5%A1-nov%C3%A1k-51a066258_techhiring-programming-dotnet-activity-7257821574500700162-cjfM/ v diskuzi jsou taky slušný perly.
---


--- https://discord.com/channels/769966886598737931/789107031939481641/1290347772532228217
Tak mě ještě napadlo zeptat se dopředu jaký pohovor tě čeká a na příklad otázek. Třeba v současné firmě dávají code review na pohovor a řekli mi to hned v prvním kole, tak jsem si lokálně nainstalovala asi 10 statických nástrojů na statickou analýzu kódu, o kterých jsem ani nevěděla, že existují, protože jsem věděla, že mi to pak pomůže. Zároveň jsem si udělala code review checklist ze zdrojů na internetu a když mi poslali úkol, tak jsem měla nachystané nástroje a šla jsem podle checklistu.
---


--- https://discord.com/channels/769966886598737931/789087476072710174/1294259606297776168
<@&1134476995229663374>
Po čase připomínám, že jsem dal k zdarma dispozici malý nástroj, který vám může pomoci: [Tabulka pro plánování, sledování času a hledání práce](https://discord.com/channels/769966886598737931/1047219933647487146)

Trackovat si kam a na jaké inzeráty jste poslali reakci není vůbec od věci. Většinou to totiž nevyjde na pár pokusů a v hlavě to neudržíte.
---


--- https://discord.com/channels/769966886598737931/789107031939481641/1288179526521589760
Přemýšlím, jestli přeci jen nechceš to IČO zvážit — [po důkladném spočítání si](https://www.youtube.com/watch?v=iJGjTFDYw9A) samozřejmě — pokud to pro některý firmy je blok.

S paušální daní to ani není moc administrativy: založit živnost a přihlásit se k paušální dani a pak jen platit měsíčně fixní částku. Není potřeba nic dalšího vykazovat a odevzdávat.

Proti o něco složitější (nutnost odevzdat daňové přiznání a poslat 2 „přehledy“ k pojištěním) možnosti se to vyplatí od cca 680 tisíc ročně.
---


--- https://discord.com/channels/769966886598737931/1283445215323099197/1283469132104335380
odkážu svoje video https://youtu.be/iJGjTFDYw9A
sice bych tam pár věcí odebral a pár přidal, ale to hlavní platí.
---


--- https://discord.com/channels/769966886598737931/789107031939481641/1277882869469024266
Neměl jsem zatím čas to přečíst, ale napsal to člověk, o kterém si myslím hodně dobrého, má hodně zkušeností, a který umí psát, takže to asi bude dobré.
> This article contains twelve fairly simple rules or principles that job candidates can put into practice, to improve the quality of their applications and their performance in interviews.
https://vurt.org/articles/twelve-rules/
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1254803183570518117
Má smysl posílat CV do firmy, kam jsem ho již posílala a firma se vůbec neozvala? Je nějaká doba, kterou by se mělo počkat? 🤔 Mám případně nějak zmiňovat, že jsem již jednou na nějakou jejich otevřenou nabídku reagovala? 🙂
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1251180512828063774
📹  Jo a videovizitky jí prej dorazily v jednotkách a většinu těch lidí umístila, nevím kde je tam příčina a následek, ale ušetřili si prý minimálně screener, protože tam o sobě všecko podstatné pověděli. A můžete si to v klidu připravit… To mě docela zaujalo jako cesta jak vystoupit z davu a ještě to některým nervóznějším může usnadnit první kontakt.
---


--- https://discord.com/channels/769966886598737931/789107031939481641/1245067053593919529
Tohle bych rád vypíchl z aktuální přednášky: https://discord.com/channels/769966886598737931/1075814161138860135/1245066837117632513
---


https://vesecky-adam.medium.com/100-interviews-in-1-year-what-have-i-found-part-ii-the-interviews-492eebbecf48


https://www.facebook.com/groups/testericz


--- https://discord.com/channels/769966886598737931/1291678484502020128/1307774460509556787
To ale přece neznamená že je to tvoje chyba. Ohledně těch peněz to trochu chápu. Já si o zvýšení vždycky řekla, když nepřišlo samo.
A i senioři dělají chybi. Prostě o tom programování je.

Znáš takový ten příběh o ceně vody?
V supermarketu stojí 10
Na nádraží 25
Ve vlaku 50
V letadle 100

Znamená to, že občas jsme prostě na místě, kde si nás dostatečně neváží a necení.
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1310318803040604170
Pokud někdo využijete moji tabulku na srovnání peněz za pracovní smlouvu a za práci na živnostenský list, tak jsem udělal verzi pro rok 2025  https://bit.ly/osvc-v-zamestnanec-2025
Je k tomu i [starší povídání](https://www.youtube.com/watch?v=iJGjTFDYw9A), který bych nejradši předělal, ale lepší než nic.
---


https://www.jakybylpohovor.cz/


Studie Jozifová:
recruiteri jsou otevreni career switcherum, ale hiring manazer casto hleda mediora za juniorskej plat a nejsou tak otevreni, odchazi franta, chce za nej frantu

Studie Jozifová:
recruiteri na switcherech nejvic ocenujou rustovej mindset, ze vidi charakterovy vlastnosti ktery jsou chteny, ale narazi na penize nebo na to ze jsou tak juniorni, ze tam nebude nekdo kdo se jim bude venovat


--- https://discord.com/channels/769966886598737931/769966887055392768/1341090446427816046
https://bit.ly/osvc-v-zamestnanec-2025 máte možnost 🙂
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1341084067000750161
našel jsem pěknou kalkulačku osvč hpp 🙂 jestli to někdo dokážete ověřit jestli je to správně tak feedback super, jinak to vypadá jednoduše a funkčně :)) https://countly.cz/hpp-vs-osvc-kalkulacka?pausalniDan=false&manualPausalniDanIndex=-1
---


--- https://discord.com/channels/769966886598737931/789107031939481641/1329486370208485467

---


--- https://discord.com/channels/769966886598737931/789107031939481641/1326904186029346938
Hele, něco jako Atmoskop, ale na pohovory: https://www.jakybylpohovor.cz/
---


--- https://discord.com/channels/769966886598737931/789107031939481641/1349716580270997525
Ahoj. Včera jsem se potkal s IT HR Monety banky, řekl jsem jí, že mám kurz testera a už se na mě dívala skrz prsty (co to zase bude za rychlokvašku) okamžitě byl můj kredit o 50% nižší.
Nakonec se mi jí podařilo trošku přesvědčit, že zas tak marný nejsem, že nějaký slušný základ mám a odnesl jsem si alespoň to na čem víc zapracovat. Ale ten začátek byl hrůzostrašný.
V rámci aktuální situace/přetlaků juniorů by bylo možná lepší takové rozhovory začínat spíš tím co umím, jaké mám zkušenosti, říct jim Váš příběh o tom co Vás tam přivedlo a ke kurzům se dostat později.
---


#} -->
