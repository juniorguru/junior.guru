---
title: Pohovor v IT
description: Jaké otázky ti nejspíš položí u pohovoru na pozici programátor? Jak bude celý pohovor vlastně probíhat? Jak by měla vypadat tvoje příprava?
template: main_handbook.html
---

{% from 'macros.html' import lead, blockquote_avatar, blockquote, link_card, note with context %}

# Pohovor

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }} Tuto stránku Honza právě přepisuje. Brzy tady bude jiný text, lepší, voňavější, nápomocnější.
{% endcall %}

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

Pokud neznáš [Django](https://www.djangoproject.com/), **odpověz upřímně!** Nelži a nesnaž se nic zamaskovat, pro tazatele bude snadné tě prokouknout. Člověka, který mlží, mít nikdo v týmu nechce. Raději řekni „Nevím, ale chci se to naučit“. Nebo: „Mám jeden projekt ve [Flasku](https://flask.palletsprojects.com/), což je taky webový framework v Pythonu, tak snad by nebylo těžké do toho proniknout“. Pokud nevíš vůbec, klidně se na správné řešení na místě zeptej. **Ukaž, že se nebojíš ptát když nevíš, a že máš chuť se posouvat.**

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
2.  **Řeš úlohy** na [webech jako Codewars nebo HackerRank](practice.md#procvicuj). Procvičíš si algoritmizaci a datové struktury na reálných problémech. Projdi si [příručky](candidate.md#souvisejici-prirucky) zabývající se řešením úloh z pohovorů.
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

*   Administrativa je na tobě. Pro každou vydělanou částku musíš vydat a poslat fakturu. Jednou za rok podáváš [daňové přiznání](https://cs.wikipedia.org/wiki/Da%C5%88ov%C3%A9_p%C5%99izn%C3%A1n%C3%AD), přehled pro ČSSZ a přehled pro zdravotní pojišťovnu.
*   Při fakturaci do zahraničí nebo obratu nad 80 000 Kč měsíčně ti hrozí [povinnost platit DPH](https://www.jakpodnikat.cz/platce-dph-registrace-povinna.php). To znamená ze dne na den začít odvádět 21 %, mít velké množství byrokracie navíc (daňová přiznání a kontrolní hlášení podáváš každý měsíc) a bát se vysokých pokut za přešlapy.
*   Pokud si při podnikání vytvoříš dluhy, máš povinnost k uhrazení využít i veškerý svůj čistě soukromý majetek (ručíš vším, na rozdíl od s. r. o., tedy [společnosti s ručením omezeným](https://cs.wikipedia.org/wiki/Spole%C4%8Dnost_s_ru%C4%8Den%C3%ADm_omezen%C3%BDm)).
*   I pokud by ti každý měsíc na účet chodilo více peněz než průměrnému zaměstnanci, u banky máš jako OSVČ [výrazně horší pozici pro získání hypotéky](https://www.chytryhonza.cz/hypoteka-pro-osvc-jak-u-banky-s-zadosti-uspet).
*   Za léta práce na živnostenský list budeš mít od státu nižší důchod.
*   Balancuješ na hraně [švarc systému](https://cs.wikipedia.org/wiki/%C5%A0varc_syst%C3%A9m). Když si to spolu s firmou nepohlídáte, je vaše činnost nelegální a postih hrozí jak tobě (až 100 000 Kč), tak firmě ([masivní pokuty, doplacení odvodů](https://www.podnikatel.cz/specialy/svarcsystem/sankce-a-kontroly/)). Znamená to také, že oficiálně nemáš nadřízeného, pracuješ na vlastním počítači, voláš z vlastního telefonu.
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

Je velmi pravděpodobné, že tě odmítnou na pohovoru, a to **proto, že se to děje úplně každému**. [Ano, i seniorním programátorům](https://sw-samuraj.cz/2017/09/smutna-zprava-o-stavu-it-trhu/). U začátečníků navíc chvíli trvá, než se naladí na aktuální poptávku trhu a na to, jak přesně fungují přijímací pohovory v IT. Raději **počítej s tím, že ze začátku to půjde ztuha** a tvé první hledání práce [bude zahrnovat i desítky pohovorů a může trvat měsíce](candidate.md#jaka-mit-ocekavani).

{% call blockquote_avatar(
  'Pokud tě odmítnou, neznamená to, že nejsi dost dobrá. Nevzdávej to. Máš talent a určitě najdeš práci, která zrovna ten tvůj talent ocení. Každého někdy odmítli na pohovoru.',
  'emma-bostian.jpg',
  'Emma Bostian'
) %}
  Emma Bostian, [Coding Coach](https://mentors.codingcoach.io/) & [Ladybug Podcast](https://www.ladybug.dev/)
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
