---
title: Jak najít svou první práci v IT
emoji: 👔
stages: [preparing, applying]
description: Jak začít hledat svou první práci v IT? Jak se připravit na pohovor?
template: main_handbook.html
---

{% from 'macros.html' import blockquote_avatar, blockquote_toxic, jobs_inline, link_card, note, video_card, video_card_engeto with context %}


# Hledání první práce v IT

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }} Původně se „Příručka“ říkalo pouze této stránce, takže má velkolepý úvod a závěr, jako by tady další stránky ani nebyly. Cílem je postupně tuto dlouhou „nudli“ rozsekávat do kratších samostatných stránek.
{% endcall %}

[TOC]

## Úvod    <span id="preface"></span>

Ještě než se začteš, jednu věc si musíme ujasnit hned. **Toto není e-book.** Nacházíš se na „živé stránce“, na které stále probíhají úpravy. Kdykoliv tady může přibýt něco nového, takže není od věci se sem občas vrátit. Všechny změny [najdeš na GitHubu](https://github.com/juniorguru/junior.guru/commits/main/jg/coop/web/docs/handbook/), o těch důležitých se můžeš dovědět na sociálních sítích junior.guru nebo prostřednictvím [klubu](../club.md).

A věci mohou přibývat i díky tobě! Pokud máš připomínku, vlastní zkušenost, nebo nápad na novou kapitolu, napiš na {{ 'honza@junior.guru'|email_link }}.

### Předmluva    <span id="foreword"></span>

Znáš [základy](learn.md) a máš [praxi](practice.md)? Nastal čas zkoušet své štěstí na pracovním trhu. Jak si ale začít hledat svou první práci v IT? Jak se připravit na pohovor?

{{ blockquote_toxic(
  'Nauč se programovat, firmy v IT berou z nedostatku lidí každého, kdo má jen zájem. Do začátku si řekni aspoň o sto tisíc.',
  'český programátorský folklór',
) }}

Tyto věty slyšel v ČR asi každý začátečník — a přitom jde o nesmysly. Ano, senioři mají navrch a firmy jim nadbíhají, junioři si ale oproti tomu musí vše vydřít. Nováčci projdou úvodními kurzy a pak zjistí, že sehnat první práci vůbec není tak snadné. Místo dobrých rad se jim dostane mýtů, takže se na vypsané nabídky hlásí nepřipravení a s nerealistickými očekáváními.

**Tahle část příručky chce situaci změnit.** Ukázat juniorům, jak se kvalitně připravit na hledání své první práce, jak se zorientovat, jak projít pohovorem. Jak vystupovat profesionálně i jako začátečník. A čím více lidí si příručku přečte, tím kultivovanější bude český trh s juniorními kandidáty. Odpovědi na inzeráty budou relevantnější, pozitivní příběhy častější a firmy motivovanější dávat juniorům šanci.

### Doprovodná videa    <span id="yablko"></span>

Svérázný slovenský lektor [yablko](https://www.youtube.com/channel/UC01guyOZpf40pUopBvdPwsg), autor kurzů tvorby webu pro začátečníky, natočil sérii videí o hledání práce v IT. Skvěle doplňují tuto příručku, mrkni na ně!

<div class="media-cards">
  {{ video_card(
    'Kde najdeš první praxi',
    '15min',
    'https://www.youtube.com/watch?v=3-wsqhCK-wU&list=PLhB6F20C-jTPITEXEHus6fVZDfNxzRbv_',
    'Jak získat úplně první praktickou zkušenost?'
  ) }}

  {{ video_card(
    'Pohovor na juniora',
    '17min',
    'https://www.youtube.com/watch?v=cEYnF7G7KXI&list=PLhB6F20C-jTPITEXEHus6fVZDfNxzRbv_',
    'Všeobecné praktické rady, které se mohou hodit i mimo IT.'
  ) }}

  {{ video_card(
    'Pohovor na programátora',
    '17min',
    'https://www.youtube.com/watch?v=cN3V5J9Wd8Y&list=PLhB6F20C-jTPITEXEHus6fVZDfNxzRbv_',
    'Jak vypadají pohovory konkrétně pro programátory?'
  ) }}
</div>


## Jak dlouho to trvá    <span id="how-long"></span>

Jak dlouho je potřeba se učit programování, než je člověk připraven si začít hledat první práci? A kolik času takové hledání zabere? Záleží na tom, jak intenzivně se věnuješ učení, jak k němu přistupuješ, jaké máš příležitosti. Někdo tomu může věnovat osm hodin každý den, takže to zvládne za týdny. Někdo se učí po večerech a stráví s tím klidně **dva roky** nebo i více. Přitom ani jedno nevypovídá nic o talentu.

{% call blockquote_avatar(
  'Dva roky jsem se při rodičovské učila programovat, než jsem si začala hledat práci. Jestli tě to baví, uč se uč, čas nepočítej.',
  'iveta-cesalova.jpg',
  'Iveta Česalová'
) %}
  Iveta Česalová, bývalá účetní, absolventka začátečnického kurzu [PyLadies](https://pyladies.cz/)
{% endcall %}

Raději neplánuj s ohledem na čas. **Jeď si tempo, které můžeš skloubit se zbytkem svého života, a soustřeď se na to, ať umíš [základní minimum](#zakladni-minimum).** Potom si začni hledat práci.

{{ video_card_engeto(
  'Jak dlouho trvá, než se naučím programovat a získám práci?',
  '4min',
  'https://www.youtube.com/watch?v=iSXqU9C3zMI&list=PLrsbT5TVJXZa2daxo8_3NagDzPqHjBEpI',
  'Důležitější je položit si otázku – jak dlouho potrvá, než budou moje dovednosti dostatečně zajímavé pro nějakou firmu?',
) }}


## Kdy začít hledat    <span id="ready"></span>

**Kdy je člověk připraven?** Na to existuje jednoduchá odpověď: **Nikdy!** Každý obor v rámci IT má jiné počáteční nároky. Každá firma má na juniory jiné nároky. Možná si říkáš: „Čím více toho umím, tím lépe se mi bude hledat práce!“ Ale tak to nefunguje. Programátoři se totiž nikdy nepřestávají učit. Od určité chvíle prostě musíš začít hledat, i když máš pocit, že toho ještě umíš strašně málo. Ten pocit se neztratí nikdy, [ani dlouho po tom, co už budeš v IT pracovat](https://overreacted.io/things-i-dont-know-as-of-2018/). **Splň [základní minimum](#zakladni-minimum) a pak si hned začni hledat práci.**


{% call blockquote_avatar(
  'Bez ohledu na to, jak moc zkušený člověk je, stejně se nakonec motá mezi pocitem, že je zdatný, neschopný („Impostor syndrom“) nebo příliš sebejistý („Dunning–Kruger efekt“).',
  'dan-abramov.jpg',
  'Dan Abramov'
) %}
  Dan Abramov, vývojář ve Facebooku známý svou prací na projektech Redux a React
{% endcall %}


## Co budou chtít    <span id="requirements"></span>

Nikdo od tebe nečeká, že budeš oslňovat technickými znalostmi. Dej najevo, že tu práci fakt chceš, že jsi **motivovaná osoba**, která má **chuť se učit**, a že do jejich týmu přineseš **nadšení**. Z programátorských veteránů nadšení vyvanulo už před lety a samozřejmostí není ani u [absolventů VŠ](#je-potreba-vs). Tvůj přístup a [měkké dovednosti](https://cs.wikipedia.org/wiki/M%C4%9Bkk%C3%A9_dovednosti) (_soft skills_) jsou důležitější než znalosti konkrétních technologií (_hard skills_).

{% call blockquote_avatar(
  'Po roce tvrdé práce a citlivého vedení jsou na tom junioři lépe než leckteří samozvaní senioři. Především potřebuji vidět jiskru v oku a nadšení pro věc.',
  'lubos-racansky.jpg',
  'Luboš Račanský'
) %}
  Luboš Račanský, profesionální programátor, autor článku [O náboru juniorů](https://blog.zvestov.cz/software%20development/2018/01/26/o-naboru-junioru.html)
{% endcall %}

### Základní minimum    <span id="minimum-requirements"></span>

1.  Znalost jakéhokoliv běžného jazyka alespoň v rozsahu začátečnického kurzu na [Nauč se Python!](learn.md#jak-zacit)
2.  Mít vytvořený nějaký [malý vlastní projekt](projects.md) jako praktickou ukázku své práce.
3.  Mít na projektech naučenou schopnost dostat zadání a rozložit ho na podproblémy (algoritmizace).

#### Velmi užitečné znalosti navíc

*   [Angličtina](english.md), čím víc tím líp!
*   Základy práce s [Gitem](https://naucse.python.cz/course/pyladies/sessions/foss/).
*   Práce s příkazovou řádkou (ideálně tou v [Linuxu](https://cs.wikipedia.org/wiki/Linux), tzn. Bash).

Ano, **toto opravdu většinou stačí!** Neboj se toho, že se učíš Python, ale v nabídkách je Java. Důležité je především **umět programovat** — další jazyk nebo technologie se dá doučit poměrně rychle.

Není potřeba jít víc do šířky a bez jasného cíle se učit tady trochu HTML, tu základy C#, tam úvod do datové analýzy — jen proto, že někde o těchto věcech uslyšíš. Místo toho si **[vyber projekt](projects.md) a na tom pracuj.** Potřebuješ získat praktické schopnosti, které ti jednodenní workshop nebo čtení knih nedají. Dlouhodobá práce na projektu ti sama ukáže, jaké konkrétní dovednosti a technologie se potřebuješ doučit. A po dokončení projektu ti to ukážou požadavky v pracovních inzerátech a [dotazy na pohovorech](interview.md#otazky-na-tebe).

Angličtina je důležitá, ale **i s omezenou, pasivní angličtinou se dá začít**. Pokud zvládáš číst anglický text, pochopit v něm zadání a učit se z něj nové věci, pro start to stačí.

{% call blockquote_avatar(
  'Na pohovoru mě nezajímá, co kdo vystudoval, ale jak přemýšlí a jaké má vlastní projekty. Nemusí být nijak světoborné, je to však praxe, kterou ani čerstvý inženýr často nemá.',
  'josef-skladanka.jpg',
  'Josef Skládanka'
) %}
  Josef Skládanka, profesionální programátor
{% endcall %}

### Co přesně znamená „junior“    <span id="junior"></span>

Chápání slova junior není mezi firmami ustálené. Někde stačí výše popsané základní minimum, jinde na tebe budou nechápavě kulit oči. Někteří jako juniora označují člověka, který toho akorát „umí méně“ a „déle mu to trvá“, ale v oboru už pár let pracuje.

Nenech se tím vykolejit! **Při prvním kontaktu s firmou se ujisti, že jste na stejné vlně** a doopravdy hledají člověka, pro kterého to bude první práce v IT (anglicky _entry job_). Ušetříte si čas a zklamání na obou stranách. Pozor, _entry job_ neznamená, že „neumíš nic“, takže to tak nikomu neříkej. Znamená to pouze, že **hledáš svou první práci v oboru**. Znalostí [máš nejspíš už spoustu](#zapisuj-si-uspechy).

### Je potřeba VŠ?    <span id="university"></span>

[Ne](myths.md). Běžní zaměstnavatelé ocení [praxi](practice.md) víc než titul. **Webovky nebo mobilní appky udělá samouk stejně dobře jako absolvent.** Studenti VŠ jsou tvá největší konkurence, ale na rozdíl od tebe jsou semletí pěti lety v českém školství. Nadšení z nich zpravidla nesrší a nemají moc praxe. Žena po rodičovské, která si rok šla za svým a učila se při všem shonu programovat po večerech, smete svou motivací každé ucho z VŠ jako nic.

Zrovna v inzerátech nabízejících první práci v IT nebo částečný úvazek se však ještě stále lze setkat s **omezením, že jsou jen pro studenty či absolventy**. Je to proto, že lidi na druhé straně inzerátu ([recruitery](#naborari), šéfy) vůbec nenapadlo, že nováčci v oboru se rodí i jinde než na univerzitě. **Zkus se ozvat i tak.** Nic za to nedáš. Buď firmě otevřeš oči, nebo se rozloučíte už při prvním kontaktu.

{% call blockquote_avatar(
  'Vývojáři nepotřebují titul z informatiky! Přestaňme zbytečně bránit lidem pracovat v IT.',
  'emma-bostian.jpg',
  'Emma Bostian'
) %}
  Emma Bostian, inženýrka ve Spotify, podcasterka v [Ladybug Podcast](https://www.ladybug.dev/)
{% endcall %}

### Záleží na věku? Pohlaví?    <span id="age-gender"></span>

[Ne a ne](myths.md). Programování není balet, [začít se dá v jakémkoli věku](https://www.youtube.com/watch?v=dKclZ55d_F0). Byť jsou stále ještě v menšině, ženy se dnes programátorkami stávají běžně. IT už dávno nevypadá jako na [této fotce](https://www.forum24.cz/jak-dopadli-chlapci-z-brutalni-parby-informatiku-2/), i když si toho někteří možná ještě nevšimli. **Pokud je z pracovního inzerátu cítit diskriminace, vůbec se jím nezabývej**. Kromě toho, že je to [protizákonné](https://www.google.cz/search?q=pracovn%C3%AD%20inzer%C3%A1t%20diskriminace), tak firma, která se myšlenkově zasekla ve středověku, nebude zrovna dobrým přístavem pro začátečníky.

{{ video_card(
  'Tomáš Hisem: Z horníka programátorem',
  '16min',
  'https://www.youtube.com/watch?v=dKclZ55d_F0',
  'Když se v 45 letech dozvěděl, že důl Paskov bude uzavřen, musel se rozhodnout, co dál. Dostal nečekanou příležitost rekvalifikovat se na programátora.',
) }}


## Jaká mít očekávání    <span id="expectations"></span>

### Kde jsou firmy, které berou každého?    <span id="hungry-market"></span>

„Nauč se programovat, firmy v IT berou z nedostatku lidí každého, kdo má jen zájem.“ Toto je bohužel **mýtus**. IT rozhodně je přístupný obor a projít změnou kariéry za poměrně krátkou dobu lze, ale **jednoduché to není a hned to také není**. [Firmy sice opravdu nemají dostatek lidí](https://www.freelo.io/cs/blog/pruzkum-mezi-programatory-penize-nejsou-vse), kteří umí programovat, ale často se rozhodnou investovat spoustu času i peněz do hledání zkušených, než aby přijali juniora a tomu se pak museli věnovat. **Počítej s tím, že můžeš projít i desítky pohovorů, než najdeš svou první práci v IT.** Je to běžné. Připrav se na to, že hledání práce ti může zabrat i měsíce. Obrň své sebevědomí i rodinný rozpočet, bude to náročný kolotoč.

### Proč práci nabízí hlavně velké firmy?    <span id="why-big-companies"></span>

Pro firmu je zaměstnání juniora velký výdaj. I když je to zdánlivě výhodné z hlediska mzdy, firma tě musí všechno učit a věnovat se ti, což ji stojí dost peněz. Byť se dají najít nabídky i od středních či malých firem, **obecně jsou do juniorů ochotny investovat spíše [větší firmy](#prace-pro-velkou-firmu), které na to mají jak finance, tak zázemí**.

Dalším prostředím, kam se probojuješ snadněji, je **státní správa**. Firmy se předbíhají v tom, jaké finanční podmínky nebo benefity nabídnou zkušeným lidem, takže pro většinu z nich není atraktivní pro veřejné instituce pracovat (to si raději vezmou velkou mzdu jinde a pak [dobrovolničí](https://cesko.digital/) ve volném čase). Pro tebe ale může být toto prostředí i mzdové ohodnocení dobrým startem.

### Kolik si vydělám?    <span id="salary"></span>

Bavíme se o první práci. Musíš se ještě hodně učit a bude chvíli trvat, než dosáhneš na ty [vysoké mzdy, kterými se všichni ohání](https://csu.gov.cz/ict-odbornici-a-jejich-mzdy). **Podle dvou anket [Smitia](https://smitio.com/) ([první](https://blog.smitio.com/clanek-mzdy-v-it-podle-smitia.html), [druhá](https://blog.smitio.com/clanke-mzdy-absolventu-ocima-firem-a-ajtaku.html)) začínají nováčci průměrně na 30.000 Kč hrubého.** V Praze a Brně to může být i více, v regionech i výrazně méně. Rovněž lze očekávat rozdíly mezi nabídkou větších a menších firem. Platí ale, že šikovní lidé jsou schopni se poměrně rychle dostat se mzdou nahoru — třeba už i za rok praxe.

Jedním z vodítek, jak si určit nástupní mzdu, může být i tvé předešlé zaměstnání. Pokud tvá mzda zásadně nepřesahovala 30.000 Kč, můžeš si ze začátku prostě **říct o totéž, co ti chodilo na účet v minulé práci**. Příjem tvé domácnosti zůstane stejný, ale do budoucna má velkou pravděpodobnost růst.

### Najdu práci externě, na dálku?    <span id="remote-work"></span>

Před rokem 2020 platilo, že práci na dálku si musíš **vysloužit svou samostatností**. Na začátku kariéry se hodně učíš, topíš se a voláš o pomoc, potřebuješ někoho, kdo ti ke konkrétním věcem, které firma dělá, vysvětlí kontext. Mnoho lidí má za to, že je lepší, když se v takové chvíli můžeš otočit na židli a zeptat se přítomných kolegů.

Situace kolem covidu-19 ale nakonec nedala firmám příliš na výběr. Práce z domova přestala být vnímána jako občasný benefit, stala se plnohodnotnou formou spolupráce. Spolu s tím **firmy objevují i způsoby, jak na dálku zaučovat nové lidi**, čímž odpadá jedna z největších překážek, proč je tento způsob práce nevhodný pro juniory. Lze tedy stále častěji najít i nabídky práce pro juniory, které jsou částečně či zcela „remote“.

Práce na dálku se během pandemie stala trendem, nejde však o nic vyloženě nového. Souhrnný článek [Práce z domova](https://honzajavorek.cz/blog/prace-z-domova/) nebo kniha [Remote](https://basecamp.com/books/remote) vyšly skoro před dekádou, ale i tak mohou dodnes sloužit jako aktuální a kvalitní zdroje informací o této problematice. Projdi si alespoň ten článek, ať se dokážeš dobře připravit i na nevýhody, které práce na dálku přináší.

Možná znáš pojem [digitální nomádství](https://honzajavorek.cz/blog/prace-z-domova/#digitalni-nomadi) a láká tě představa, že ťukáš do notebooku někde na pláži. Na fotkách to vypadá dobře, ale [realita je složitější](https://www.svetpatritemcoseneposerou.cz/blog-ikigai-a-japonsky-smysl-zivota.html) — a nejde jen o displej na přímém slunci nebo písek v klávesnici. Hezký úvod a spoustu dalších odkazů najdeš v článku na [Travel Bibli](https://travelbible.cz/digitalni-nomadstvi/).

{% if jobs_remote %}
#### Nabídky práce na dálku
Přímo na junior.guru najdeš [nabídky práce výhradně pro juniory](../jobs.jinja). Některé z nich práci na dálku umožňují!
{{ jobs_inline(jobs_remote, 2, jobs_url='/jobs/remote/') }}
{% endif %}


## Volba strategie    <span id="strategy"></span>

### Proč začínat programováním    <span id="why-start-with-programming"></span>

Programování je nejlepší způsob, jak začít v IT. **Kolem tvorby softwaru se motá spousta dalších profesí, které tě časem mohou zaujmout více, ale teď o nich ještě ani nevíš. Dokud je neuvidíš v praxi, nebudeš si umět jejich práci ani představit, natož se na ni rovnou hlásit.** Programování má oproti tomu jasně zmapovanou cestu, jak se dá začít učit, a lze z něj časem snadno odskočit jinam. I pokud se nakonec najdeš jinde, ten znalostní základ, který si programováním vytvoříš, [se ti nikdy neztratí](motivation.md#proc-se-to-ucit). Z toho důvodu začni programováním a pak dej volný průchod tomu, kam tě život zavane.

{% call blockquote_avatar(
  'Firma rychle poznala, že umím komunikovat s ostatními a posouvat věci dopředu: Víc než kódit jsem začal odstraňovat překážky a ladit procesy. Posun do role „Scrum Mastera“ byl nabíledni.',
  'michal-havelka.jpg',
  'Michal Havelka'
) %}
  Michal Havelka, autor článku [Jak jsem se (ne)stal front-end vývojářem](https://www.zdrojak.cz/clanky/jak-jsem-se-nestal-front-end-vyvojarem/)
{% endcall %}

### Existují pozice vhodnější pro začátečníky?    <span id="entry-friendly-roles"></span>

Může to zabrat čas, úsilí, a chce to sebevědomí, ale i se [základním minimem](#zakladni-minimum) lze rovnou najít práci, kde se programuje. V rámci toho určitě existují pozice, kde se nováček uplatní snadněji, ale pozor na [zdánlivě související technické pozice](#zacinani-na-jine-technicke-pozici), kde se ovšem neprogramuje a **nikam tě neposunou, pokud programovat chceš**.

V rámci programování se mnoha lidem osvědčilo začít v rámci [DevOps](https://cs.wikipedia.org/wiki/DevOps) nebo [SRE](https://en.wikipedia.org/wiki/Site_Reliability_Engineering), na pozicích jako např. _automation engineer_. Denním chlebem těchto profesí je často **programování jednodušších, samostatných skriptů (malých jednorázových programů), na kterých se dají snadno sbírat zkušenosti**.

### Začínání na jiné technické pozici    <span id="entry-tech"></span>

Vyplatí se začít technickou podporou (_tech support_), testováním (_tester_), [QA](https://cs.wikipedia.org/wiki/Quality_assurance) (_quality assurance_), správou serverů (_operations_) nebo třeba [správou sítě](https://cs.wikipedia.org/wiki/Syst%C3%A9mov%C3%BD_administr%C3%A1tor) (_sys admin_)? Reálné příběhy juniorů praví, že tato povolání sice občas mohou zafungovat jako přestupní stanice k vývojářské pozici, ale mnohem častěji je to **zbytečná odbočka** na tvé cestě. Firmy ti sice slíbí, že kromě testování budeš mít čím dál více příležitostí i programovat (např. automatizované testy) a že tě časem na programování plně přeřadí, ale potom — skutek utek. Než to prokoukneš a odhodláš se ke změně, rok nebo dva strávíš na pozici, kterou vlastně nechceš dělat. Zkušenosti s programováním si neprohloubíš (testování vyžaduje jiné dovednosti), takže na pohovorech budeš ve stejné pozici, jako předtím.

Pokud **chceš** dělat technickou podporu nebo testování, protože cítíš, že tě to bude bavit, tak do toho jdi, na tom rozhodně není nic špatného! **Pokud ale chceš programovat, tak si rovnou hledej vývojářskou pozici.** Ano, může to zabrat více času, úsilí, a chce to sebevědomí, ale i se [základním minimem](#zakladni-minimum) lze takovou práci najít.

Pokud na práci spěcháš, nebo si z jakéhokoliv důvodu opravdu chceš nejdříve zkusit jinou technickou pozici, **snaž se, aby zahrnovala programování**. Např. místo ručního testování hledej pozici na programování automatizovaných testů. Místo administrace sítě hledej programování administračních skriptů. Místo ruční správy serverů (_operations_, _ops_) se ujisti, že firma prosazuje opravdové [DevOps](https://cs.wikipedia.org/wiki/DevOps).

{% call blockquote_avatar(
  'Testování není vstupní brána pro vývoj. QA potřebují jiné dovednosti než vývojář.',
  'pylady.png',
  'PyLady'
) %}
  Poznámky ze srazu absolventek začátečnického kurzu [PyLadies](https://pyladies.cz/) v Brně
{% endcall %}

### Jakým směrem se vydat?    <span id="choosing-field"></span>

Když nahlédneš do IT, zjistíš, že kolem programování se motá spousta dalších profesí. **Pokud tě nějaký směr láká nebo rovnou baví, zkus zjistit, co k tomu potřebuješ a nauč se základy.** Cítíš v sobě [manažerské buňky](https://www.martinus.cz/?uItem=606009)? Rýpeš se v [hardwaru](https://www.raspberrypi.org/)? Chceš [programovat hry](https://warhorsestudios.cz/)? Máš [sklony k psaní](https://www.writethedocs.org/)? Baví tě [vizuální věci](https://frontendisti.cz/)? Trápí tě, [když je software pro lidi komplikovaný](https://cs.wikipedia.org/wiki/User_experience_design)? Pro každou z těchto otázek existuje odpověď v podobě specializace. Jdi za tím, co si myslíš, že by tě mohlo bavit. Neměj strach, že se naučíš něco, co následně nevyužiješ. Ve tvé situaci je to extrémně nepravděpodobné. Cokoliv se naučíš, brzy tak či onak uplatníš. Pokud se tedy nezačneš učit [nějaké ezo](https://cs.wikipedia.org/wiki/Ezoterick%C3%BD_programovac%C3%AD_jazyk).

Co když ale vůbec netušíš kudy se vydat? Možná to zkus přes „misi“ než přes činnost. **Vyber si firmu nebo organizaci, která je ti sympatická, a zkus najít průnik mezi tím, co dělají oni, a co můžeš dělat ty.** [Parfémy](https://www.czechcrunch.cz/2020/01/ceske-notino-je-nejvetsi-e-shop-s-parfemy-v-evrope-loni-v-rekordnich-trzbach-atakovalo-10-miliard-korun/)? [Oblečení](https://www.czechcrunch.cz/2020/01/desitky-milionu-korun-pro-lepe-odene-muze-cesky-startup-genster-nabira-penize-pro-boxy-s-oblecenim-na-miru/)? [Topení](https://www.czechcrunch.cz/2020/01/digitalizace-remesel-funguje-topite-cz-dela-topenarinu-online-rychle-roste-a-obsluhuje-uz-tisice-lidi/)?

No a pokud ti nedá směr ani to, vezmi prostě jakoukoliv práci jako junior vývojářka nebo vývojář, kterou seženeš se [základním minimem](#zakladni-minimum), a **nech volný průběh tomu, kam tě to zavane**. Možná ti někdo řekl, že máš hledat svou vášeň a dělat to, co tě baví, ale [ono to ve skutečnosti funguje jinak](https://www.youtube.com/watch?v=LUQjAAwsKR8).

{{ video_card(
  'Cal Newport: ‘Follow your passion’ is wrong',
  '35min',
  'https://www.youtube.com/watch?v=LUQjAAwsKR8',
  'Říká se, že máš hledat svou vášeň a dělat to, co tě baví. Cal Newport vysvětluje, že to je rada na prd. Ve skutečnosti je to celé složitější.',
) }}

### Na čem programátoři ve firmách pracují?    <span id="na-cem-programatori-ve-firmach-pracuji"></span>

Nabídky zaměstnání se hodí rozlišovat podle toho, na čem budeš po nastoupení pracovat. Zajímavě toto téma rozebírá [Lukáš Linhart v přednášce o své kariéře](https://youtu.be/l7zUC0T1E98?t=999). Doplněné shrnutí toho, co zmiňuje:

*   **Produktové firmy** vyvíjí jeden nebo více vlastních softwarových produktů a ty prodávají. Práce na produktu je jako pečovat o zahrádku. Je důležité, jak moc se ti produkt firmy líbí a jak dlouho tě baví pracovat na jedné věci. Vliv zákazníků na tvou každodenní práci je rozmělněný. Mezi nevýhody patří práce s kódem, který vznikl před lety, a stereotyp.<br>
    Příklady: Prusa Research, Liftago, Red Hat, [startupy](#prace-pro-startup)…
*   **IT oddělení** firem, jejichž hlavní byznys je v něčem jiném než v softwaru. Fungují obdobně jako produktový vývoj, akorát že nic neprodávají, ale podporují svou činností zbytek firmy. Někdy se hranice stírá — jsou Twisto víc finančníci, nebo programátoři?<br>
    Příklady: Rohlik.cz, Hypoteční banka, Škoda Auto, e-shopy…
*   **Digitální agentury** zpracovávají zakázky pro jiné firmy. Projekty přicházejí a odcházejí, je větší prostor pro stavění nového na zelené louce a pro zkoušení nejnovějších technologií. Zákazník může mít prostřednictvím „projekťáků“ velký vliv na tvou každodenní práci, je zde riziko vyššího stresu pro všechny zúčastněné. Některé firmy také provozují _[body shopping](https://www.google.cz/search?q=body%20shopping%20programov%C3%A1n%C3%AD)_, tedy že pracuješ „[na IČO](interview.md#prace-na-ico)“ a agentura tě přeprodává jako [žoldnéře](https://cs.wikipedia.org/wiki/%C5%BDoldn%C3%A9%C5%99).<br>
    Příklady: Fragaria, STRV, Symbio, reklamní agentury…
*   **Média nebo oddělení pro práci s daty** zaměstnávají programátory k tomu, aby řešili jednorázové úkoly. Nároky jsou na tebe značně jiné než u běžného vývoje. Není problém psát „nekvalitní“ kód, protože se hned po použití zahodí. Specifika této práce [popisuje Martin Malý](https://www.zdrojak.cz/clanky/co-se-vyvojar-nauci-v-novinach/).<br>
    Příklady: Economia, Český rozhlas aj. média, vědecké instituce…

Při hledání zaměstnání si během [zjišťování informací o nabídkách](#informace-o-firme) vždy každou z nich zařaď do jedné z kategorií výše, ať víš co očekávat. Pokud máš na výběr, ujasni si, v jakém režimu by se ti líbilo pracovat.

### Dobrovolnictví    <span id="volunteering"></span>

Jeden ze způsobů, jak přijít k první praxi, je **pomoci nějakému neziskovému projektu**. Nemusí to být zrovna [Člověk v tísni](https://www.clovekvtisni.cz/). Třeba přímo ve svém okolí najdeš něco, kde je potřeba programování, ale nejsou prostředky na profesionální programátory a příliš to nespěchá.

Nemáš-li nápady, mrkni na [Pyvec](https://pyvec.org/), [Česko.Digital](https://cesko.digital/), [Hlídač státu](https://www.hlidacstatu.cz/), [Um sem um tam](https://umsemumtam.cz/), nebo si **projdi projekty na [Darujme.cz](https://www.darujme.cz/) a napiš tomu, kterému by se ti líbilo pomoci**. Ideální je, pokud je za projektem nějaké „IT oddělení“ (možná spíš skupinka nadšenců), kde tě budou zaučovat za to, že jim pomůžeš.

{% call blockquote_avatar(
  'GameCon naplňoval ideální simulaci firemních podmínek. Neziskový projekt má své výhody – pracujete na něčem, co se reálně použije, projekt můžete řídit, máte k ruce tým kolegů.',
  'michal-havelka.jpg',
  'Michal Havelka'
) %}
  Michal Havelka, autor článku [Jak jsem se (ne)stal front-end vývojářem](https://www.zdrojak.cz/clanky/jak-jsem-se-nestal-front-end-vyvojarem/)
{% endcall %}

{% if jobs_volunteering %}
Přímo na junior.guru jsou [nabídky práce výhradně pro juniory](../jobs.jinja) a občas se mezi nimi objeví i nabídka dobrovolnictví (neziskovky a malé projekty zde mohou inzerovat zdarma). Zrovna dnes tam něco je:
{{ jobs_inline(jobs_volunteering, 2, jobs_url='/jobs/remote/') }}
{% endif %}


### Stáže    <span id="internships"></span><span id="unpaid-internships"></span>

Některé firmy vypisují stáže (anglicky _internship_), ale **není jich mnoho**. Často jsou [jen pro studenty VŠ](#je-potreba-vs), protože firmu nenapadne, že by se na ně mohl hlásit i někdo jiný. Mnohdy se také podaří naplnit stáže přes známosti nebo partnerství se školami, takže není důvod je veřejně inzerovat.

Stáž přitom může být **dobrá příležitost, jak začít bez zkušeností**. Firma tě zaučí do jednoduchých úkolů a po čase se rozhodne, jestli tě chtějí vzít. A často chtějí, když už do tebe investovali nějaký ten čas. I kdyby to nevyšlo, je z toho aspoň praxe, zkušenost, brigáda na léto.

Pokud studuješ, máš k dispozici nástěnky, poradenská centra, pracovní veletrhy, webové stránky studentských spolků, webové stránky aj. prezentace výzkumných pracovních skupin, spolužáky, cvičící, přednášející…

**Ostatním zbývá [asertivita](https://cs.wikipedia.org/wiki/Asertivita).** Odmítli tě v nějaké firmě, protože hledají někoho zkušenějšího? Zeptej se jich na stáž. Líbí se ti nějaká firma? Napiš jim a zeptej se na stáž. Významnou roli hraje také [networking](#networking). Choď na [srazy a konference](community.md), tam se aktivně druž a — ptej se na stáž.

{% call blockquote_avatar(
  'Už jsem viděl stáže dohozené přes bratrance, klienty, plesy, spolujízdu. Najednou jsi konkrétní člověk a pokud vypadáš inteligentně, firma si řekne: „Proč ne?“',
  'petr-messner.jpg',
  'Petr Messner'
) %}
  Petr Messner, profesionální programátor
{% endcall %}

Pozor na **neplacené stáže**. Je na tobě si vyhodnotit, zda se ti stáž bez odměny ve tvé situaci vyplatí a zda si to vůbec můžeš dovolit. Ač je možné se s neplacenými stážemi setkat běžně u nás i v zahraničí, je to [věc na hranici zákona i etiky](https://www.e15.cz/the-student-times/neplacene-staze-aneb-jak-nedocenitelna-je-zkusenost-1348117). Podle českého práva [není neplacená stáž jednoznačně protizákonná](https://www.epravo.cz/top/clanky/neplacena-praxe-ve-firmach-studenti-i-zamestnavatele-na-hrane-zakona-100528.html), ale **existuje šance, že v případě kontroly ze strany inspektorátu může být taková praxe vyhodnocena jako nelegální práce**.

{% if jobs_internship %}
Přímo na junior.guru najdeš [nabídky práce výhradně pro juniory](../jobs.jinja). Zrovna dnes jsou mezi nimi i nějaké stáže:
{{ jobs_inline(jobs_internship, 2, jobs_url='/jobs/remote/') }}
{% endif %}

### Práce pro velkou firmu    <span id="big-companies"></span>

Velké firmy a instituce [jsou v lepší pozici](#proc-praci-nabizi-hlavne-velke-firmy), aby mohly zaměstnávat začátečníky. Práce pro ně má své **výhody**:

*   [Bývají ochotné platit víc](https://danluu.com/startup-tradeoffs/) než menší firmy.
*   V mezinárodních firmách pracuješ s lidmi různých jazyků a kultur. Čeká tě moderní a profesionální _workplace_.
*   V širokých týmech se můžeš specializovat na určitou věc, pracovat na tématu do hloubky.
*   Kariérní růst je zorganizovaný a tvůj postup _mohou_ určovat jasná pravidla, ne pouze rozmar šéfa.
*   Můžeš mít k dispozici dražší služby a nástroje. Můžeš mít větší možnosti cestovat za firemní peníze, např. na [konference](community.md).

Mají více peněz a nebývá pro ně problém je investovat. Ovšem jen pokud mají pocit, že je daná věc dobrý nápad, a občas je bohužel velmi těžké korporaci o takových dobrých nápadech přesvědčit. Preferuje své zajeté koleje. Mezi další **nevýhody** patří:

*   Mnoho věcí předepisuje struktura a procesy, na jejichž podobu máš minimální vliv.
*   Upřednostňovány jsou starší technologie, které má firma roky odzkoušené a všichni s nimi umí. Ke zkoušení nových moc vůle nebývá.
*   Mezinárodní firmy musí splňovat širokou škálu zákonů a regulací. Z toho plynou omezení a komplikace. Jednoduché věci často nelze dělat jednoduše.
*   Můžeš si připadat jako kapka v moři, číslo v kartotéce. Užitek tvé práce může působit vzdáleně.
*   U mezinárodních firem je ze zřejmých důvodů zcela nepostradatelná komunikativní úroveň [angličtiny](english.md).

Zajímavě korporace rozebírá [Lukáš Linhart v přednášce o své kariéře](https://youtu.be/l7zUC0T1E98?t=5671) nebo [Dan Luu v článku Big companies v. startups](https://danluu.com/startup-tradeoffs/). Oproti obecnému přesvědčení **nemusí být velká firma nutně bez zajímavé práce nebo divokých změn**. Vnitřní reorganizace nebo změny korporátní politiky umí přinést stejný stres jako je ten, který ti budou slibovat ve [startupech](#prace-pro-startup).

**V menších firmách** je méně struktury, méně regulace, méně procesů, máš v nich větší vliv na celkové prostředí. Věci se tak dělají snadněji a možná i rozhodují snadněji. Stejně tak má ale tvůj šéf větší moc a tvůj kariérní růst bude probíhat čistě neformálně, na základě pocitů a vyjednávání. Častěji se také setkáš s [kulturou zatuchlého českého rybníčku](#firemni-kultura).

{% call blockquote_avatar(
  'Proces je kolektivní dohoda, jak se něco bude dělat. Rozdíl mezi zlým procesem a pozitivní dohodou je jen v tom, jak moc je můžeš ovlivnit.',
  'lukas-linhart.jpg',
  'Lukáš Linhart'
) %}
  Lukáš Linhart, technický ředitel v [Apiary](https://byznys.ihned.cz/c1-65593630-oracle-kupuje-za-miliardy-korun-cesky-start-up-apiary-zakladatele-ve-firme-zustavaji) a poté v Oracle
{% endcall %}

Nenech se ale **příliš unést zobecněními**, které jsou v této kapitole. Rozdíly mezi konkrétními firmami (např. [Red Hat](https://www.redhat.com/en/jobs) versus [Oracle](https://www.oracle.com/careers/)), nebo i mezi konkrétními interními týmy v rámci téže korporace, mohou být větší, než výše popsané obecné rozdíly mezi korporacemi a malými firmami. Vždy si [zjisti](#informace-o-firme), jaké podmínky jsou v právě v tom týmu, do jakého se chystáš nastoupit.

{% call blockquote_avatar(
  'Rozdíly mezi jednotlivými manažery a týmy v jedné firmě mohou snadno být větší než rozdíly mezi samotnými firmami.',
  'dan-luu.jpg',
  'Dan Luu'
) %}
  Dan Luu, autor článku [Big companies v. startups](https://danluu.com/startup-tradeoffs/)
{% endcall %}

### Práce pro startup    <span id="startups"></span>

Startup je firma, jejímž cílem je najít nějaký nový [produkt](#na-cem-programatori-ve-firmach-pracuji), který by vydělával peníze a je možné jej s relativně malým úsilím rozjet ve velkém („škáluje to“). Startupy začínají nápadem, ale potom hledají a kličkují na trhu, dokud nenarazí na něco, co opravdu vydělává peníze. A především, **úspěšný startup musí růst jako otesánek**. Na rozdíl od běžné firmy je startup dočasným projektem — buďto se chce stát [korporací](#prace-pro-velkou-firmu), nebo jej jednou nějaká koupí. Pokud ti někdo ve startupu nabízí práci, počítej tedy s následujícím:

*   [Nebude mít tolik peněz jako větší firmy](https://danluu.com/startup-tradeoffs/). Bude se to snažit kompenzovat skrze benefity (moderní pracovní prostředí, neomezené dovolené, pružnou pracovní dobu) nebo nabídnutím podílu ve firmě.
*   Všechno se bude v čase stále měnit. V březnu vás bude pět, v září padesát a s koncem roku může firma zaniknout. V závislosti s tím se mění i všechna rozhodnutí a pravidla.
*   Na začátku jde často o malý neformální kolektiv s plochou organizační strukturou. Nikdo si na nic nehraje, všichni jsou na jedné lodi a chtějí změnit svět. Čím méně lidí ve firmě je, tím větší máš vliv, ale i zodpovědnost.
*   Za začátku musí každý dělat tak trochu všechno. Není prostor pro specializaci ani velké puntičkářství. Nebývá čas na zaučování juniorů. Hodí tě do vody a plav.
*   Dej si velký pozor na [kulturu](#firemni-kultura) a rovnováhu mezi prací a životem (anglicky _work–life balance_). Někdy se předpokládá, že startup znamená makat 16h denně. Ve výjimečných případech může být nasazení potřeba, ale dlouhodobě je to naprosto zcestná praktika vedoucí akorát k vyčerpání a [vyhoření](https://cs.wikipedia.org/wiki/Syndrom_vyho%C5%99en%C3%AD).
*   Pracovat ve startupu může být „cool“ nebo tak aspoň vypadat. Lidé startupům a jejich produktům fandí, může to v tobě vyvolávat hrdost, radost z práce. Máš pocit, že jsi součástí něčeho důležitého, že měníš svět.

Startup **jednou skončí, a to především pokud má investory**. Investoři dávají firmě peníze proto, že je chtějí zhodnotit. To lze udělat jen úspěchem firmy a jejím vstupem na burzu, nebo prodejem větší firmě. Pokud startup nemíří ani k jednomu, budou investoři tlačit na to, aby se choval agresivněji, nebo to zabalil. Není pro ně zajímavé živit běžnou firmu, tzn. tu, která si na sebe vydělá, roste pomalu a [má prostor se chovat rozvážně a ohleduplně](https://m.signalvnoise.com/reconsider/). Devět z deseti startupů zkrachuje, a ten desátý musí investorům vydělat na ostatní a ještě něco přidat jako zisk.

S tím souvisí i **kompenzace nižší mzdy v podobě akcií nebo opcí**. Představa, že máš svůj podíl na úspěchu firmy, a že hodnotu akcií můžeš přímo ovlivnit svou prací, zní jako skvělá příležitost i motivace. [Skutečnost je ale značně složitější.](https://danluu.com/startup-options/) Neupínej se příliš na to, že si za svůj podíl jednou pořídíš jachtu v Karibiku. Ber to spíš tak, že máš „lístek v loterii“. **Angažmá ve startupu si užiješ hlavně pokud věříš jeho misi.** Potom ti to bude stát za to i přestože to nakonec nevyjde.

Startupy jsou dnes velký fenomén, a to především v USA. **Americké [Silicon Valley](https://cs.wikipedia.org/wiki/Silicon_Valley) je pro programátory totéž, co [Hollywood](https://cs.wikipedia.org/wiki/Hollywood) pro tvůrce filmů.** Pokud tě téma zajímá víc, můžeš sledovat český magazín [CzechCrunch](https://www.czechcrunch.cz/) nebo jeho americkou předlohu, [TechCrunch](https://techcrunch.com/). I velká část výše zmiňované [přednášky Lukáše Linharta](https://youtu.be/l7zUC0T1E98?t=1987) je o tom, jak prošel startupem od prvního zaměstnance až po akvizici velkou firmou.

{% call blockquote_avatar(
  'Velké firmy mají určitý druh problémů, které se nevyskytují ve startupech, a startupy zase mají své vlastní problémy, které nenajdeš v korporaci. Je na tobě, jaký kompromis ti vyhovuje, a který druh problémů chceš řešit.',
  'dan-luu.jpg',
  'Dan Luu'
) %}
  Dan Luu, autor článku [Big companies v. startups](https://danluu.com/startup-tradeoffs/)
{% endcall %}

### Práce na volné noze    <span id="freelancing"></span>

Podnikání je z pochopitelných důvodů opomíjenou možností, jak začít v IT. Nejefektivnějším způsobem, jak během prvních 1-2 let nabrat zkušenosti, je jít do klasického zaměstnání ve střední nebo větší firmě. **Ne každému ale něco takového zapadne do jeho životní situace.** Pokud budeš u některé z následujících otázek přikyvovat, stojí za zvážení, zda by pro tebe nebyla živnost vhodnější volbou:

*   Hledáš jednorázové přivýdělky? Nedaří se ti najít zaměstnání na částečný úvazek? Např. při studiu na VŠ, péči o dítě nebo při jiném zaměstnání?
*   Bydlíš mimo velká města, kde se stálé zaměstnání v IT hledá obtížně? [Praha](../jobs/praha.jinja) nebo [Brno](../jobs/brno.jinja) nabízí jiné příležitosti než Šluknovsko či Jesenicko.
*   Nějaké podnikání nebo pokusy o něj už máš za sebou a víš co [OSVČ](https://cs.wikipedia.org/wiki/Osoba_samostatn%C4%9B_v%C3%BDd%C4%9Ble%C4%8Dn%C4%9B_%C4%8Dinn%C3%A1) obnáší? Umíš se otáčet, komunikovat, zvládáš samostatnost, samovzdělávání?
*   Netlačí tě finance a nebude vadit, když během prvních měsíců vyděláš např. jen pár tisíc? Máš velký „sociální kapitál“, ze kterého můžeš čerpat zakázky?

{% call blockquote_avatar(
  'Uvědomil jsem si, že nejspíš nikdy nebudu mít klasické zaměstnání. V mém okolí není po mých schopnostech poptávka. Práci seženu jedině na dálku, jako kontraktor.',
  'vuyisile-ndlovu.jpg',
  'Vuyisile Ndlovu'
) %}
  Vuyisile Ndlovu, [programátor na volné noze ze Zimbabwe](https://vuyisile.com/)
{% endcall %}

[Práci na dálku](#najdu-praci-externe-na-dalku) nebo pružnou pracovní dobu dnes firmy nabízejí i jako benefit v rámci běžného zaměstnaneckého poměru. Pokud se ti ovšem takovou práci dlouho nedaří najít a zároveň je to pro tebe jediná možnost, jak začít, může být volná noha způsobem, jak si tyto podmínky zařídit.

Než ovšem vyrazíš na živnostenský úřad, je dobré si nejdříve ujasnit, co se prací na volné noze přesně myslí. Na českém IT trhu se jako [OSVČ](https://cs.wikipedia.org/wiki/Osoba_samostatn%C4%9B_v%C3%BDd%C4%9Ble%C4%8Dn%C4%9B_%C4%8Dinn%C3%A1) typicky pohybuješ někde mezi těmito dvěma způsoby podnikání:

*   **Freelancer**, nebo také [nezávislý profesionál](https://cs.wikipedia.org/wiki/Nez%C3%A1visl%C3%BD_profesion%C3%A1l), umí nějakou věc velmi dobře a nechává se na ni najímat od mnoha různých klientů. Ti mohou být dlouhodobí, ale vztah mezi ním a firmou je spíše dodavatelský. Je v podstatě jednočlennou [agenturou](#na-cem-programatori-ve-firmach-pracuji). Buduje si vlastní značku a reputaci, měl by se snažit být vidět. Může pracovat kdy chce a [odkud chce](#najdu-praci-externe-na-dalku), ale jako každá svoboda, i tato s sebou nese velkou zodpovědnost. Kromě své profese musí umět být i sám sobě šéfem, asistentem, účetním, marketérem a obchoďákem, nebo by měl vydělat dost na to, aby si alespoň na něco z toho někoho najal. A měl by se naučit i dobře oddělovat pracovní život od soukromého, aby při tom všem brzy [nevyhořel](https://cs.wikipedia.org/wiki/Syndrom_vyho%C5%99en%C3%AD).
*   **Kontraktor** má prakticky jen dlouhodobé klienty a jeho vztah s firmou připomíná vztah zaměstnanecký. Říká se, že „dělá na IČO“. Benefity ani záruky klasického zaměstnaneckého poměru nemá, rizika a náklady si musí připočítat do své sazby. Je to [žoldnéř](https://cs.wikipedia.org/wiki/%C5%BDoldn%C3%A9%C5%99), který si musí umět věci spočítat, našetřit si záložní peníze, uzavírat s firmami oboustranně výhodné dohody. Kromě toho se ale způsob práce kontraktora většinou zásadně neliší od toho, jak svůj den tráví zaměstnanec.

O nástrahách práce „na IČO“ je tady [celá další kapitola](interview.md#prace-na-ico). Pokud tě láká „freelancing“, rozhodně si ji přečti, ale navíc si projdi i následující tipy:

*   Než do toho půjdeš naplno, můžeš si „něco jako práci na volné noze“ **nejdříve vyzkoušet**, a to v podobě tzv. [příležitostné činnosti](https://www.jakpodnikat.cz/prilezitostna-cinnost.php).
*   Firmy [outsourcují](https://cs.wikipedia.org/wiki/Outsourcing) spoustu úkolů, ale **nebudou je chtít svěřit amatérovi**. Ujasni si, jaké jsou tvé přednosti a jak hodláš klientům kompenzovat své nedostatky (např. nízkou cenou). Vytvoř si [portfolio](#osobni-web-a-blog), kde to firmám „vysvětlíš“. Začni s jednoduchými, jasně zadanými a ohraničenými úkoly, které zvládneš vypracovat. Nesnaž se dělat všechno (např. weby, nebo i frontend jsou příliš široká zaměření). Vyber si směr, kterým se chceš vydat a na který se budeš specializovat (např. [kódování newsletterů](https://www.google.cz/search?q=k%C3%B3dov%C3%A1n%C3%AD%20newsletter%C5%AF)). Začni malými krůčky, propracovávej se k větším úkolům a s nimi i k sebedůvěře, která ti pomůže odhadnout, do čeho se zvládneš pustit a kolik si za to máš říct.
*   **Poptávky nepřijdou samy.** Je velká pravděpodobnost, že nikdo zatím ani neví, že vůbec existuješ a něco nabízíš. Zkus si na internetu najít vhodné firmy a napsat jim e-mail s nabídkou svých služeb, účastni se [srazů nezávislých profesionálů](https://www.facebook.com/navolnenoze/events/), procházej různá internetová tržiště s poptávkami. V Česku má jistou tradici fórum [Webtrh](https://webtrh.cz/), ale existuje toho spousta (abecedně): [fiverr.com](https://fiverr.com/), [freelance.cz](https://freelance.cz), [freelancer.com](https://freelancer.com), [guru.com](https://guru.com), [navolnenoze.cz](https://navolnenoze.cz), [peopleperhour.com](https://peopleperhour.com), [topcoder.com](https://topcoder.com), [toptal.com](https://toptal.com), [upwork.com](https://upwork.com)… Připrav se na to, že musíš každý měsíc platit zálohy na pojištění (minimálně kolem 5 000 Kč měsíčně), ať už něco vyděláš, nebo ne.
*   **Žádný senior nebude mít v popisu práce se ti věnovat a rozvíjet tě**, pokud budeš vůbec dělat v týmu. Intenzivní samostudium a vypracovávání zakázek budou zřejmě jedinými způsoby, jakými se budeš učit. Pokud na to vyděláš, můžeš si [platit mentora](mentoring.md). Počítej s tím, že ze začátku budeš moci klientovi účtovat jen zlomek hodin, než kolik jich reálně nad úkolem strávíš. Neboj se ale s nabytými zkušenostmi tento poměr vylepšovat. Chybějící tým kompenzuj v [coworkingu](https://navolnenoze.cz/blog/coworkingy/), účastí v profesní komunitě, na [srazech](community.md) nebo [online](help.md).

Další rady ohledně rozjíždění vlastního podnikání jsou nad rámec této příručky. Následující odkazy by ti nicméně měly ukázat cestu k tomu hlavnímu, co se může do startu hodit. Hodně štěstí!

<div class="link-cards">
  {{ link_card(
    'Jak podnikat',
    'https://www.jakpodnikat.cz/',
    'Administrativa malého podnikání, lidsky. OSVČ, ŽL, daně.'
  ) }}

  {{ link_card(
    'Podnikatelský almanach',
    'https://www.fakturoid.cz/almanach/',
    'Sbírka praktických tipů jak podnikat.'
  ) }}

  {{ link_card(
    'Blog Na volné noze',
    'https://navolnenoze.cz/blog/',
    'Články o všem, co se týká podnikání na volné noze.'
  ) }}

  {{ link_card(
    'nakopni.to',
    'https://www.nakopni.to/',
    '50% sleva na profi nástroje pro všechny, jejichž IČO je mladší než 1 rok.'
  ) }}

  {{ link_card(
    'Kniha Na volné noze',
    'https://freelanceway.eu/',
    'Bible profesionálů na volné noze.',
    badge_icon='book',
    badge_text='Kniha',
  ) }}
</div>


## Příprava    <span id="preparation"></span>

Jak bylo už zmíněno, [nečekej příliš dlouho](#kdy-zacit-hledat). Zkoušej to, i když si myslíš, že na to nemáš. Uč se v průběhu na základě toho, co zjistíš na [pohovorech](interview.md). Speciálně pokud jsi žena, buď až „drzá“. **Muži jdou na pohovor i pokud mají pocit, že mají polovinu znalostí. Žena se často neodváží, dokud nevěří, že má 120 % požadovaného**. Tento problém se nazývá _[confidence gap](https://www.theatlantic.com/magazine/archive/2014/05/the-confidence-gap/359815/)_, ale [kořeny má nejspíš hlouběji než jen v malém sebevědomí](https://www.theatlantic.com/family/archive/2018/09/women-workplace-confidence-gap/570772/).

Nepodceňuj se, v inzerátech je ideál, který ti má spíše ukázat kam pozice směřuje. Mnohdy ani sama firma nemá úplně jasno v tom, koho přesně chce, a rozhoduje se až o konkrétních lidech. **Jestliže je v inzerátu něco, co toužíš jednou dělat, zkus to i přesto, že to ještě neumíš.**

### Související příručky    <span id="handbooks"></span>

<div class="link-cards">
  {{ link_card(
    'Tech Interview Handbook',
    'https://www.techinterviewhandbook.org/',
    'Přečti si jak na CV, pohovory, algoritmy.'
  ) }}

  {{ link_card(
    'Shánění práce na internetu',
    'https://prace.rovnou.cz/',
    'Projdi si českou příručku základů hledání práce na internetu.'
  ) }}

  {{ link_card(
    'Cracking the Coding Interview',
    'http://www.crackingthecodinginterview.com/',
    'Slavná kniha plná úloh, které můžeš dostat na pohovoru.'
  ) }}
</div>

### Tvoje požadavky    <span id="priorities"></span>

Pokud hledáš ve velkém městě, kde je nabídek více, připrav si **seznam konkrétních věcí, které jsou pro tebe důležité**. Ten si u každé nabídky odškrtávej. Může to být třeba že chceš:

*   na programátorskou pozici ([ne testování](#zacinani-na-jine-technicke-pozici)),
*   pružnou pracovní dobu,
*   [příjemný kolektiv](#firemni-kultura),
*   stabilitu, nebo naopak [startup](#prace-pro-startup) plný rychlých změn,
*   prostředí, kde nebude problém se učit nebo [zajet na konferenci](community.md),
*   rovnováhu mezi prací a volným časem,
*   malou dojezdovou dobu do kanceláře,
*   [mzdu větší než určitou částku](#kolik-si-vydelam),
*   možnost kariérního postupu…

Cokoliv z toho pro tebe může být zásadní. Je dobré si v tom dopředu udělat pořádek a pak upřednostnit ty nabídky, které to splňují. Nehledej naslepo „něco“. Ze svých požadavků neslevuj, raději obejdi více pohovorů.

Seznam udělej podle sebe. Netrap se tím, co chtějí ostatní — každý je v jiné situaci, každého motivuje něco jiného. Tvoje priority **jsou tvoje a jsou důležité**.

### Informace o firmě    <span id="research"></span>

Než firmě napíšeš, **něco si o ní zjisti**. Vyhledej si firmu na internetu, zkus pochopit její produkt, [kulturu](#firemni-kultura), apod. Lidé na pohovorech často zjišťují, jestli o firmě něco víš, a kromě toho ti to pomůže i s [vlastními dotazy](interview.md#tvoje-otazky). Pokud firma [pořádá nějaké své akce](#firemni-akce), můžeš část svého průzkumu provést i tam.

Zjisti si **zákulisní informace**. Ty nejzajímavější věci z lidí vytáhneš [u piva](#networking), ale i na internetu lze leccos najít. Existují weby jako [Atmoskop](https://www.atmoskop.cz/) nebo [Glassdoor](https://www.glassdoor.com/), kde si můžeš přečíst hodnocení firem napsané bývalými a současnými zaměstnanci. Můžeš narazit na _red flags_, signály, že **firma, do které se snažíš dostat, [není tak úplně v pořádku](#firemni-kultura)**. Nebo ti to může pomoci alespoň připravit si zajímavé [dotazy, které můžeš položit během pohovoru](interview.md#tvoje-otazky).

### Zapisuj si úspěchy    <span id="wins"></span>

Jedna z věcí, které chceš ukázat potenciálnímu nebo stávajícímu zaměstnavateli je, že se umíš učit a zlepšovat. A chceš to ostatně ukázat i sobě, pomůže ti to bojovat s nedostatečným sebevědomím („[Impostor syndrom](https://www.google.cz/search?q=impostor+syndrome&lr=lang_cs)“). Jak na to? **Dělej si poznámky o naučených vědomostech.** Vždy, když se k seznamu vrátíš, pomůže ti to **uvědomit si, jak dlouhou cestu máš za sebou** a kolik nových skvělých věcí umíš od posledně.

Veď si seznam svých [projektů](projects.md) na [osobní stránce](#osobni-web-a-blog), na LinkedIn profilu, nebo na GitHubu. **Možná se budeš za svůj nejstarší kód stydět, ale to je normální. Aspoň jde vidět tvůj posun!** Profesionální programátoři se stále učí nové věci a tak je běžné, že se stydí i za to, co napsali před pár měsíci, natož před lety. Eviduj svoje [přednášky a články](#projev-aktivitu-navic). Pokud o tvé práci někdo napíše něco pochvalného (na sociálních sítích, na LinkedIn, do e-mailu), poznamenej si to a klidně si ulož i [snímek obrazovky](https://cs.wikipedia.org/wiki/Sn%C3%ADmek_obrazovky). Na [osobní stránce](#osobni-web-a-blog) to můžeš využít do seznamu referencí (anglicky _testimonials_).

Nejen že **se takovými věcmi dobře chlubí na pohovoru nebo při pokusu o zvýšení mzdy**, ale i pro tebe to bude hezká připomínka úspěchů, které máš za sebou.

## Kde hledat    <span id="seeking"></span>

### Pracovní portály    <span id="job-boards"></span>

Pracovní portály (anglicky _job board_) jsou „nástěnky“ s nabídkami práce. Je to asi **nejpřímočařejší způsob, jak hledat práci**.

Jednou z nevýhod je, že nabídky na portálech si může přečíst každý a **vystavuješ se tak větší konkurenci na pohovoru**. Na americkém trhu na inzerát odpoví i stovky uchazečů a je velmi obtížné mezi nimi vyniknout. **V Česku tento problém tak žhavý není**, čísla uchazečů jsou zřídkakdy v desítkách. Prakticky každý se časem někde prosadí.

Větší problém je tedy spíš s hledáním nabídek vhodných zrovna pro tebe. Mnohé portály umožňují filtrovat podle místa kanceláře nebo programovacího jazyka, ale s rozřazením nabídek na seniorní a juniorní už je to horší.

{% call blockquote_avatar(
  'Narazil jsem na pracovní nabídku, která vyžadovala více než 4 roky zkušeností s FastAPI. Nemohl bych se přihlásit, protože jsem FastAPI vytvořil jen před 1,5 rokem.',
  'sebastian-ramirez.jpg',
  'Sebastián Ramírez'
) %}
  Sebastián Ramírez, autor FastAPI
{% endcall %}

Začátečníci většinou na konkrétní technoligii nelpí a rádi se zaučí v čemkoliv, takže filtrování podle programovacích jazyků využijí jen omezeně. Filtr na juniorní nabídky by ocenili, ale je málokde. I tam, kde takový filtr je, nefunguje podle očekávání. Buď vyskočí brigády pro studenty, nebo **výsledky zahrnují spoustu nabídek, které ve skutečnosti vůbec juniorní nejsou**.

Např. amatérská analýza dat z LinkedIn [odhalila](https://www.reddit.com/r/dataisbeautiful/comments/hvtn0i/oc_only_26_of_jobs_marked_entrylevel_are_actually/), že jen 26 % tamních nabídek práce označených jako _entry level_ je opravdu pro začátečníky. Jistě, [slovo junior vnímá každý jinak](#co-presne-znamena-junior), ale některé nabídky požadují dokonce víc než 12 let zkušeností! Tato praxe je předmětem [kritiky](https://www.youtube.com/watch?v=Ictmhp2uJu8), [údivů](https://twitter.com/tiangolo/status/1281946592459853830) i [vtipů](https://twitter.com/nixcraft/status/1294220253224828928), ale v dohledné době se asi nezmění.

{% call blockquote_avatar(
  'Pracovné ponuky sú šľahnuté! Ja neviem polovicu vecí, čo chcú od juniora. A ich seniori tiež nie.',
  'yablko.jpg',
  'yablko'
) %}
  yablko, lektor online kurzů, ve svém [videu o nabídkách práce](https://www.youtube.com/watch?v=Ictmhp2uJu8)
{% endcall %}

{% if jobs %}
#### Nabídky práce na junior.guru
Přímo na junior.guru také najdeš [pracovní portál](../jobs.jinja), ale s nabídkami jen a pouze pro juniory. Jiné zde inzerovat ani nelze. Navíc se každý den spouští robot, který se rozhlíží i po nabídkách z dalších zdrojů. Poté je filtruje na základě přísných pravidel a nechá jen ty, o nichž usoudí, že jsou opravdu pro začátečníky:
{{ jobs_inline(jobs, 3, jobs_url='/jobs/remote/') }}
{% endif %}

### Náboráři    <span id="recruiters"></span>

Existují dva druhy náborářů (anglicky _recruiter_):

*   **Pracují přímo pro konkrétní firmu**, zpravidla velkou, a hledají na trhu lidi jen do ní. Můžeš se s nimi setkat na stáncích firem na [konferencích](community.md) či pracovních veletrzích. Také jsou to oni, kdo s tebou řeší přijímací pohovor, když se velké firmě ozveš na nabídku práce. Navenek je reprezentují „kariérní portály“.
    Příklady: [Red Hat](https://www.redhat.com/en/jobs), [ČSOB](https://www.csob.cz/portal/v-obraze/kariera)…
*   **Pracují samostatně pro více firem**, hledají kandidáty a snaží se je umístit. Najímají si je firmy, které nemají náboráře vlastní. Jejich odměna je zpravidla výkonová, tzn. že dostávají provizi až v případě, že se jim podaří umístit kandidáta. Provizi vyplácí firma, a to ve výši několika měsíčních mezd kandidáta.
    Příklady: [dreamBIG](https://www.dreambig.cz/), [Three Queens](https://www.3queens.cz/)…

Výhodou firemních náborářů je, že **znají společnost do hloubky** a jsou schopni ti stoprocentně odpovědět na všechny dotazy. Budou ale v odpovědích hájit hlavně zájmy zaměstnavatele. Samostatně operující recruiteři **jsou zase nestranní**. Mohou ti dát na výběr z více společností, které zastupují, a prezentovat ti jejich pro a proti. Na detailní dotazy jsou ovšem schopni odpovídat jen omezeně.

**Samostatně operující recruiteři ti mohou pomoci sehnat práci, a to z tvého pohledu zadarmo**, protože je zaplatí firma. Problém je v tom, že pro firmu je zaměstnání juniora už tak dost velký výdaj. I když je to levné z hlediska mzdy, firma tě musí všechno učit a věnovat se ti. **Jako junior nejsi zrovna atraktivní „balíček“ na trhu a když se k tomu přidá ještě potřeba vyplatit provizi náborářům, dokonce ti to může snížit šance na přijetí.** Firma, která by tě klidně vzala napřímo, tě může odmítnout, pokud tě dohazuje externí recruiter. Zároveň tvá nízká startovní mzda znamená, že recruiteři si nepřijdou na zajímavou odměnu (na rozdíl od toho, kdyby svůj čas věnovali umisťování zkušenějších programátorů s jejich astronomickými mzdami).

### Profily    <span id="profiles"></span>

Kromě procházení nabídek práce **si můžeš vytvořit profil, na základě kterého tě mohou firmy najít samy**. Přesněji, mohou tě najít [recruiteři](#naborari).

Základem profilu je životopis. [Účet na LinkedIn](https://www.linkedin.com/in/honzajavorek/) nebo [osobní stránky](#osobni-web-a-blog) by tedy šlo za takový „profil kandidáta“ považovat, ale ten většinou bývá **obohacen ještě o další, zpravidla neveřejné informace, které pomáhají náborářům v orientaci**. Mohou to být výsledky testů tvých znalostí, podrobnější informace o tvých mzdových představách nebo popis ideální hledané pozice z pohledu kandidáta. Profil si můžeš vytvořit na každém druhém webu, který se zabývá nabídkou a poptávkou práce. Existují ale i služby specializované jen na profily, např. [Techloop](https://techloop.io/).

Kromě takovýchto strukturovaných profilů **se můžeš nabízet také volně v programátorské komunitě**. Základem je [networking](#networking), ale lze využít i sílu sociálních sítí. Příspěvky o tom, že hledáš práci, můžeš zveřejnit na místech, kde se sdružují programátoři, např. ve [Facebookové skupině o jazyce Python](https://www.facebook.com/groups/pyonieri/). **Upřímně popiš co umíš a co hledáš.** Konkrétně v případě Facebooku si dej ale pozor na to, že soukromé zprávy od lidí, které nemáš v přátelích, ti spadnou do „žádostí o zprávy“. Můžeš tak minout vážně míněné nabídky práce zaslané jako reakce na tvůj příspěvek.

### Oslovování firem    <span id="cold-calling-companies"></span>

Nenech se odradit tím, že firma neinzeruje pracovní nabídky nebo že mezi jejími nabídkami nenajdeš něco pro sebe. **Neboj se firmy napřímo oslovovat a ptát se jich, jestli by v nich nebyla příležitost pro [stáž](#staze) nebo juniorní pozici.** Někdy je lepší si příležitost vytvořit než na ni pasivně čekat.

**Je tvým snem pracovat pro nějakou konkrétní společnost? Napiš jim!** Nejlépe napřímo oslov konkrétní osobu z technického týmu, ne [recruitery](#naborari). I pokud nemáš něco vyloženě vysněného, můžeš si vybrat firmu nebo organizaci, která je ti sympatická, a zkusit najít průnik mezi tím, co dělají oni, a co můžeš dělat ty. [Parfémy](https://www.czechcrunch.cz/2020/01/ceske-notino-je-nejvetsi-e-shop-s-parfemy-v-evrope-loni-v-rekordnich-trzbach-atakovalo-10-miliard-korun/)? [Oblečení](https://www.czechcrunch.cz/2020/01/desitky-milionu-korun-pro-lepe-odene-muze-cesky-startup-genster-nabira-penize-pro-boxy-s-oblecenim-na-miru/)? [Topení](https://www.czechcrunch.cz/2020/01/digitalizace-remesel-funguje-topite-cz-dela-topenarinu-online-rychle-roste-a-obsluhuje-uz-tisice-lidi/)? Mít v týmu lidi zapálené pro to, čím se firma zabývá, je přání mnoha manažerů.

### Firemní akce    <span id="company-events"></span>

Občas firmy pořádají přednášky, dny otevřených dveří, školení, [hackathony](collaboration.md), [srazy](community.md), aj. **akce přímo na své domácí půdě**. Na nich se dá obhlédnout prostředí, neformálně navázat kontakty, poptat se osobně na [stáž](#staze). Některé firmy dokonce přímo konají kurzy pro začátečníky nebo s nějakými spolupracují, a nabízí práci nejšikovnějším absolventům.

Činnost tohoto typu vypovídá minimálně o tom, že **firma není uzavřená do sebe**, že se snaží být aktivní v širší komunitě programátorů, a že u svých lidí podporuje i aktivity nad rámec sezení za počítačem „od devíti do pěti“.

Tyto akce najdeš na stránkách jednotlivých firem, nebo i na [meetup.com](https://meetup.com): [TopMonks Caffè](https://www.meetup.com/TopMonks-Caffe/), [Y-Soft: Technology Hour](https://www.meetup.com/ysoft-th/), [STRV Meetups](https://www.meetup.com/STRV-Meetups/)…

### Networking

Jedním z nejefektivnějších způsobů, jak si v malé ČR sehnat dobrou práci, je **networking, tedy setkávání s lidmi a získávání kontaktů**. Staň se [aktivním členem programátorské komunity](#projev-aktivitu-navic) a zajímavé nabídky práce po čase přijdou samy. Choď na [srazy a konference](community.md), seznamuj se s lidmi, představuj se. Jsou to místa, kde lidé zhusta mění a získávají práci — i proto se na nich vyskytují [recruiteři velkých firem](#naborari). Můžeš zkusit i veletrhy práce, které jsou na toto přímo zaměřené (např. [Job Fair Czechitas](https://jobfair.czechitas.cz/)). **Velké akce lze pojmout systematicky** — vytiskni si 50 vizitek s nápisem „sháním stáž“ a jdi je rozdat mezi lidi. Představuj se, vysvětli co umíš a co hledáš, prodej se. **Malé akce jako srazy ber jako způsob jak najít nové kamarády** v oboru a pracovním příležitostem tam nech spíš volný průběh.

Networking je také způsob, jak od lidí dostat doporučení. Někteří lidé jsou schopní tě ve své firmě doporučit i po pěti minutách rozhovoru, ať už protože mají dobré srdce, protože na ně zapůsobíš, nebo protože chtějí dostat _referral bonus_ (odměna za doporučení nového zaměstnance, kterou některé firmy nabízejí).

Česká komunita programátorů je malá a existuje na malém prostoru — z Plzně do Ostravy je to pár hodin vlakem. **„Všichni se znají“, je snadné se setkávat**. Díky tomu je u nás networking velmi důležitou složkou budování kariéry.


## Firemní kultura    <span id="culture"></span>

Programátor génius, který sám na všechno přijde, ale nevychází dobře s lidmi, je dnes minulostí. Pro takové lidi se vžilo označení _brilliant jerk_ a [internet je plný článků o tom, proč se jich mají firmy vyvarovat](https://www.google.cz/search?q=brilliant%20jerk). Programování je už dlouho **týmová práce v níž je ego na překážku** a kde je schopnost **komunikace s lidmi stejně důležitá jako technické vědomosti**.

Pokud jsou v týmu lidé s toxickým přístupem, silně to ovlivní každý jeden den, který v práci strávíš. **Pozoruj už při pohovoru, jakému chování dává firma volný průchod. Jaká je v ní kultura? Kdo budou tví kolegové?** Všímej si, jestli má firma smíšený kolektiv, nebo je to [monokultura dvacetiletých geeků](https://honzajavorek.cz/blog/mlady-kolektiv/), a přemýšlej, co by ti vyhovovalo víc. Některé firmy mají tzv. _lunch round_, což je **neformální kolo pohovoru, kdy můžeš jít se svými budoucími kolegy na oběd** a zjistit tak, jestli si s nimi sedneš (totéž se samozřejmě snaží zjistit i oni). O kulturách konkrétních firem se lze také dovědět na [Cocuma](https://www.cocuma.cz/) a [Welcome to the Jungle](https://www.welcometothejungle.com/).

Kdo bude tvůj šéf? Hledej manažera, pro kterého jsou důležité tvoje zájmy a cíle, který vytvoří prostředí, kde se ti bude dařit. **Dobrý manažer se snaží o tvůj úspěch.**.

Jedna z nejdůležitějších věcí, které potřebuješ jako junior vědět o svém týmu: **Bude se ti někdo ve firmě soustavně věnovat? Budeš mít komu pokládat dotazy bez toho, aby z tebe dělal blbce?** Zeptej se na to! A ptej se na všechno, co se ti nezdá. Projdi si pečlivě rady, které jsou v [kapitole o tvých otázkách na pohovoru](interview.md#tvoje-otazky).

Pokud cítíš, že ti firemní kultura něčím nesedne, **vždy je lepší zkusit hledat jinde než zůstat**. Kulturu firmy prakticky není možné opravit zevnitř. I pokud už zrovna dostaneš svou první práci v IT, je lepší odejít. Je jasné, že není snadné se vzdát těžce nabyté příležitosti a vrátit se do onoho náročného obcházení pohovorů, ale **žádná práce nestojí za dlouhodobý stres a narušené duševní zdraví**. Neboj, za ukončení práce ve zkušebce tě nikdo hodnotit nebude, od toho zkušebka je!

<div class="link-cards">
  {{ link_card(
    'Cocuma',
    'https://www.cocuma.cz/',
    'Projdi si firmy podle jejich kultury.'
  ) }}

  {{ link_card(
    'Welcome to the Jungle',
    'https://www.welcometothejungle.com/',
    'Projdi si firmy podle jejich kultury.'
  ) }}
</div>


## Projev aktivitu navíc    <span id="proactive"></span>

Existuje mnoho způsobů, jak na sebe můžeš upozornit a tím **vystoupit z davu**. Kandidát, který se aktivně snaží něčím přispět do oboru, dává najevo velký zájem a nadšení. Kromě toho si ve firmě mohou říct, že když tě baví např. [organizovat akce](#organizovani-komunitnich-akci) nebo [psát články](#osobni-web-a-blog), byla by škoda tě mít jen na programování. Nabídnou ti, že tyto činnosti můžeš dělat pro firmu jako součást své pracovní náplně.

Tyto aktivity mohou navíc podněcovat [networking](#networking), tedy setkávání a kontakty — což je nejefektivnější způsob, jak si v malé ČR sehnat dobrou práci.

### Osobní web a blog    <span id="portfolio"></span>

Vlastní osobní webová stránka (_portfolio_) ti dává prostor **vyniknout mezi ostatními kandidáty**. Je to [projekt](projects.md), na kterém si prakticky vyzkoušíš různé technologie a který klidně můžeš ukázat při pohovoru jako důkaz, že něco umíš. Mimo to můžeš na své webovce dát průchod vlastní osobnosti a kreativitě.

Stránka nemusí být komplikovaná, stačí aby to byl **rozcestník**. Dvě věty o sobě, popis zkušeností, odkazy na profily (LinkedIn, GitHub…) a případně na tvé [projekty](projects.md). Pokud tě baví psaní, časem můžeš přidat **blog**. Můžeš psát o své cestě do IT (a tak se [objevit na těchto stránkách](../stories.md)) nebo přidat článek vždy, když se naučíš něco nového — čímž pomůžeš dalším začátečníkům a zároveň tím vystoupíš z davu. Začneš si v oboru budovat své jméno a to ti může pomoci nejen u pohovorů, ale i pokud budeš chtít [přednášet na konferencích](#projev-aktivitu-navic).

{% call blockquote_avatar(
  'Tweetuju nebo píšu články o všem, co se naučím. Mohu se k tomu vždy vrátit a zároveň s učením pomáhám ostatním. Díky psaní článků navíc věcem porozumím do hloubky a umím je vysvětlit.',
  'vladimir-gorej.jpg',
  'Vladimír Gorej'
) %}
  Vladimír Gorej, profesionální programátor, o svém [Twitteru](https://twitter.com/vladimirgorej/) a [blogu](https://vladimirgorej.com/)
{% endcall %}

Příklady osobních stránek s blogem: [Honza Javorek](https://honzajavorek.cz/) (autor této příručky) nebo [Iveta Česalová](https://web.archive.org/web/20240421092834/https://ivet1987.wz.cz/blog/) (absolventka PyLadies). Další inspiraci lze [snadno najít na internetu](https://www.google.cz/search?q=best%20(personal%20or%20portfolio)%20websites).

### Učení    <span id="teaching"></span>

I když se to nezdá, i začátečníci mohou učit! **Nejlepší způsob, jak se něco pořádně naučit, je vysvětlit to někomu jinému.** Učení upevňuje hloubku tvých vlastních znalostí a umožňuje ti setkat se s lidmi z oboru. Můžeš [napsat článek na blog pokaždé, když se naučíš něco nového](#osobni-web-a-blog), můžeš [nabízet mentoring](mentoring.md), můžeš pomáhat na komunitně organizovaných kurzech a workshopech jako jsou ty od [PyLadies](https://pyladies.cz/) nebo [Czechitas](https://www.czechitas.cz/).

Na PyLadies kurzech **můžeš „koučovat“ i bez velkých znalostí programování**, stačí se [přihlásit](https://pyladies.cz/stan_se/). Je to doplňková role bez velké zodpovědnosti, se kterou můžeš kdykoliv přestat. Pro lepší představu si přečti [článek od koučky Ivety](https://web.archive.org/web/20240421083253/https://ivet1987.wz.cz/2020/03/koucovani-na-pyladies-kurzech/). Další podobná role, kterou jde dokonce dělat na dálku z pohodlí domova, je [opravování úkolů](https://pyladies.cz/stan_se/).

{% call blockquote_avatar(
  'Na začátku to byly hrozné pocity. Někdo si mě zavolá k problému, se kterým nedokážu pomoci, budu za trubku. Nakonec to ale byly obyčejné, jednoduché problémy, se kterými jsem poradila.',
  'iveta-cesalova.jpg',
  'Iveta Česalová'
) %}
  Iveta Česalová, autorka [článku o koučování na PyLadies](https://web.archive.org/web/20240421083253/https://ivet1987.wz.cz/2020/03/koucovani-na-pyladies-kurzech/)
{% endcall %}


### Přednášení    <span id="giving-talks"></span>

Podobně jako učení, přednášení na [srazech a konferencích](community.md) vypadá jako něco, co je vyhrazeno profesionálům, ale není to tak. **Zmíněné akce jsou komunitní a obvykle podporují přednášky od začátečníků a pro začátečníky.** Neboj se toho! Přijít na pohovor s tím, že máš za sebou přednášku na srazu nebo dokonce konferenci, je naprostá pecka! Pro inspiraci si projdi nějaké přednášky z minulých let konference [PyCon CZ](https://cz.pycon.org/). Nejsou to nutně pokročilá technická témata:

*   [Keep formatting consistent with Black](https://cz.pycon.org/2019/programme/talks/29/)
*   [Proč a jak učit děti programovat](https://cz.pycon.org/2018/programme/detail/talk/13/)
*   [Python developer wannabe: How to make a change in your life and get satisfaction](https://cz.pycon.org/2018/programme/detail/talk/2/)
*   [Three Ways My Programming Teacher Rocks (and you can too)!](https://cz.pycon.org/2018/programme/detail/talk/33/)
*   [Be(come) a mentor! Help others succeed!](https://cz.pycon.org/2017/speakers/detail/talk/10/)
*   [Your first open source Pull Request](https://cz.pycon.org/2017/speakers/detail/talk/38/)
*   [Humanizing among coders](https://www.youtube.com/watch?v=npyB5Oz-v-I)

Pokud by tě přednášení a konference bavily hodně, můžeš dokonce zkusit hledat _DevRel_ pozici (z anglického _developer relations_), což je něco jako známé disciplíny _public relations_ nebo _marketing_, ale vůči vývojářům.

### Organizování komunitních akcí    <span id="organizing"></span>

Aktivitu lze projevit i **organizováním akcí** ve volném čase — můžeš třeba [založit sraz](https://docs.pyvec.org/guides/meetup.html) nebo sehnat lektory a podle [volně dostupných materiálů](https://naucse.python.cz/) rozjet kurz ve svém městě (např. [začátečnický kurz PyLadies](https://pyladies.cz/ostatni/)). Pokud tyto akce ve svém okolí už máš, můžeš s nimi pomoci (napiš organizátorům). Stejně tak se lze přihlásit jako výpomoc při organizaci konferencí (např. [PyCon CZ](https://cz.pycon.org/)). Firmy občas dokonce přímo hledají lidi, které organizování akcí a práce s komunitou baví — pozice se jmenuje _event manager_ nebo _community manager_.

{% call blockquote_avatar(
  'Sraz jsem založil, abych na něj mohl sám chodit a učit se Python. Na to, abych zarezervoval stůl, jsem nepotřeboval být Python expert. Získal jsem díky tomu kontakty, kamarády, vědomosti, pracovní nabídky.',
  'honza-javorek.jpg',
  'Honza Javorek'
) %}
  Honza Javorek, zakladatel [brněnského Python srazu](https://pyvo.cz/brno-pyvo/)
{% endcall %}

### Přispívání do open source    <span id="oss-contributing"></span>

V neposlední řadě si lze vybudovat jméno [přispíváním do open source](collaboration.md). I pokud se necítíš na samotné programování, [je i hodně jiných způsobů, jak můžeš přiložit ruku k dílu](https://opensource.guide/how-to-contribute/#what-it-means-to-contribute). Je to skvělá příležitost jak nabrat zkušenosti, vyniknout, získat kontakty mezi lidmi z oboru.


## Závěrem    <span id="end"></span>

Snad neexistuje jiný profesionální obor vyučovaný na vysokých školách, který je stejně přístupný jako IT. Všechno ohledně programování si můžeš nastudovat na internetu a vždy můžeš najít i někoho, kdo ti rád poradí. Získat první práci v IT rozhodně není jednoduché, ale jde to, a to i bez titulu. Do chirurgie nebo architektury se takto dostat nelze, i kdyby byl člověk sebevětší nadšenec.

Vložená dřina se navíc s největší pravděpodobností dobře zúročí. IT je a bude zárukou dobré a stabilní kariéry v nejisté době. Ať se bude dít cokoliv, technologie budou stále více prostupovat naše životy. Spolu s tím bude potřeba lidi, kteří jim rozumí. IT neexistuje ve vzduchoprázdnu a ostatní obory potřebuje, ale jednotlivec se uplatní napříč hospodářskými odvětvími. Když přestane fungovat prodej letenek, můžeš jít programovat třeba pro banky.

Lepší peníze nebo pracovní podmínky jsou legitimní a racionální důvody, proč se chtít do IT dostat, nebudou ale fungovat dobře jako tvá jediná motivace. Nejdál to nakonec dotáhneš, pokud tě aspoň trochu baví technologie. Vidina peněz tě nepřenese přes hodiny sezení na židli a psaní závorek do editoru. IT má navíc na rozdíl od jiných oborů extrémní nároky na sebevzdělávání. Nelze se jej jednou naučit tak, že to „stačí“ a pak už jen pracovat. Půl roku se nevzděláváš a hned jsi pozadu. Aby to mohla být tvá práce na spoustu let dopředu, potřebuješ se vyloženě chtít učit. Potřebuješ chtít opakovaně prožívat radost z fungujícího programu, chtít trénovat trpělivost při ladění kódu, chtít zvědavě prozkoumávat nové knihovny, chtít něco tvořit. Jinými slovy, nejvíc ti pomůže vášeň. A vášeň je nakonec i to hlavní, co firmy v juniorech hledají na pohovorech.

{% call blockquote_avatar(
  'Vášeň není to, co se vám líbí, ale něco, pro co jste ochotni trpět, jen abyste to mohli dál dělat.',
  'jenika-mcdavitt.jpg',
  'Jenika McDavitt'
) %}
  Jenika McDavitt, autorka [Psychology for Photographers](https://psychologyforphotographers.com/how-to-live-your-passion-stop-confusing-hobbies-with-passions)
{% endcall %}

Kde se bere vášeň? Do začátku stačí, když ti programování přijde jako něco zajímavého. Když máš alespoň základní touhu to zkoušet a řemeslně se v tom zlepšovat. Stejně jako když se učíš tancovat nebo hrát na kytaru, musíš si na to umět pravidelně vyhradit čas a trénovat. [Vášeň se postupně dostaví sama](https://www.youtube.com/watch?v=LUQjAAwsKR8) a stane se motorem pro veškerou dřinu, která tě čeká. Je to eso, které zvládne přebít titul, talent, i štěstí.

{{ video_card(
  'Cal Newport: ‘Follow your passion’ is wrong',
  '35min',
  'https://www.youtube.com/watch?v=LUQjAAwsKR8',
  'Říká se, že máš hledat svou vášeň a dělat to, co tě baví. Cal Newport vysvětluje, že to je rada na prd. Ve skutečnosti je to celé složitější.',
) }}

**P.S.** Nezapomeň, že jsi na „živé stránce“, na které stále probíhají úpravy. Kdykoliv tady může přibýt něco nového, takže není od věci se sem občas vrátit. Všechny změny [najdeš na GitHubu](https://github.com/juniorguru/junior.guru/commits/main/jg/coop/web/docs/handbook/), o těch důležitých se můžeš dovědět na sociálních sítích junior.guru nebo prostřednictvím [klubu](../club.md).

A věci mohou přibývat i díky tobě! Pokud máš připomínku, vlastní zkušenost, nebo nápad na novou kapitolu, napiš na {{ 'honza@junior.guru'|email_link }}. Jestli se ti díky junior.guru povede sehnat práci, ozvi se! Můžeš [motivovat ostatní svým příběhem](../stories.md), nebo tím prostě jen udělat [Honzovi](#honza) radost.


<!-- {#

https://www.freecodecamp.org/news/what-is-web-development-how-to-become-a-web-developer-career-path/

Suma sumárum je to 10 měsíců od chvíle, kdy jsem se rozhodl změnit kariéru z učitele na programátora. Doufám, že vám tohle trochu pomůže a nabudí vás to. Kdyžtak se na cokoliv ptejte.
jak jsem hledal práci - https://discord.com/channels/769966886598737931/789107031939481641/866373605951537173

https://www.freelance.cz/

https://web.archive.org/web/20230322060142/https://cybermagnolia.com/blog/the-money-talk-meetup/

podle čeho vybrat první job https://youtu.be/dyQTfuL1Q0g

glue kariéra, dobře komunikující lidi na pomezí technical a communitative https://noidea.dog/glue

https://cestakzamestnani.cz/

http://simonwillison.net/2022/Nov/6/what-to-blog-about/

v létě jsou hiring manažeři a HR často na dovolené + s juniorními pozicemi počítají, že nejvíce zájemců bude v září - absolventi si většinou udělají poslední hezké léto na půl úvazek nebo na žádný, a nastupujou až v září. Léto je určitě slabší. Stejně jako prosinec.

velká část firem má fiskální rok a kalendářní rok identický (my zrovna ne, náš fiskál končí teď v říjnu), takže typicky od října/listopadu už je jasné, kolik peněz a na jaké pozice bude a začínají se vypisovat - s ideálem, aby ten nový člověk nastoupil co nejdřív od začátku roku
https://discord.com/channels/769966886598737931/788826407412170752/902872779924316161

blogging was the best thing i ever did
https://open.spotify.com/episode/2VKvivHgq6SwunwIUGfmQZ

For junior position it might be rather difficult to go through recruitment agency. The reason is that recruiters are generally considered expensive and there are a lot of candidates for junior positions on the market, so companies prefer to hire juniors themselves and use recruiters' help with positions that are more difficult to fill.  While it might still be possible to find junior role via recruiters, I'd recommend to start applying directly to companies. Check out LinkedIn, Xing (if you consider Germany), Stack Overflow, but also company pages directly (they might be promoting higher positions outside but also have junior roles on their career sites)

jeste jedna vec takova, ale to nevim jestli jsem zrovna nemel jen kliku, tak mi prijde, ze ve velkejch firmach muzes vic najit mega chytryho cloveka od kteryho se da ucit. to v mensich tezko najdes, pac ho nezaplatej

Types of companies
https://almad.blog/notes/2020/on-four-types-of-dev-companies/

https://technicalinterviews.dev/

Udělám kompromis na kulturu, zamknu se v česky firmě, nebo půjdu ven angličtina větší svět

vuy radí https://twitter.com/terrameijar/status/1311839746537254913

https://www.linkedin.com/feed/update/urn:li:activity:6679279756376064001/?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A6679279756376064001%2C6679322502440722432%29
Prosím přidej i popis různých typů produktů https://www.joelonsoftware.com/2002/05/06/five-worlds/

úpravy v rozdělení firem a tak
https://trello.com/c/c5ZXh2OV/850-upravy

větší menší firmy
https://trello.com/c/FJGVxHqF/933-p%C5%99%C3%ADru%C4%8Dka

kolik si vydělám?
https://trello.com/c/Ivq66HuS/888-p%C5%99%C3%ADru%C4%8Dka

Uaaa, dataři neřeší jen jednorázový úkoly!!!!1
https://twitter.com/PetraVidnerova/status/1301810810763833344
https://twitter.com/kondrej/status/1301792984141365248

Studie ze algoritmy na pohovoru jsou bullshit
https://www.facebook.com/fczbkk/posts/10157621725912741

Here are their top tips:
-    Cold email and use LinkedIn- Candidates who created tailored emails and sent them directly to the CEO, co-founder or hiring manager expressing interest and outlining your qualifications landed positions this way and received an accelerated interview process!
-    Use Slack Groups- Join various slack groups and find #hiring channels where employers will post open positions, then reach out to the poster via email or on Slack
-    Don’t underestimate the behavioural interview- Prepare for the most common behavioural questions such as “tell me about yourself,” “what are you looking for in your next role” and “why do you want to work here” questions. Make sure you make these personal, and do your research on the company to make sure your answers align.

https://twitter.com/jurri_cz/status/1299425286077976581

Arogantni HR
https://www.linkedin.com/pulse/jak-recruite%C5%99i-sm%C3%BD%C5%A1lej%C3%AD-o-aj%C5%A5%C3%A1c%C3%ADch-pavel-%C5%A1imerda/

Entry level jobs. Sad. Only 26% of jobs marked 'entry-level', are actually entry-level. Details here https://reddit.com/r/dataisbeautiful/comments/hvtn0i/oc_only_26_of_jobs_marked_entrylevel_are_actually/

https://twitter.com/nixcraft/status/1286275591512064001

Finding Employment - Python Crash Course, 2nd Edition
https://ehmatthes.github.io/pcc_2e/finding_employment/

DOPLNIT TYP FIREM: OUTSOURCING
Jen bych doplnil ještě jeden typ firem do https://junior.guru/candidate-handbook/#job-types a sice firmy dělající outsourcing. Tyto firmy narozdíl od bodyshoppingu umožňují dělat v rámci týmu dlouhodobě (roky) na konkrétním produktu a mít tak dost času se s ním žít a výrazně jej ovlivnit. Zároveň ale umožňují co pár let změnit projekt a dělat tak na jiném produktu, třeba i z jiného odvětví, v rámci stejného kolektivu. Nejzajímavější jsou podle mě firmy dělající outsourcing pro USA, protože se tak zároveň programátor dostane k zajímavým produktům, např. monitorování výkonnosti a funkčnosti databází firem jako je Netflix nebo Sony, SW infrastruktura pro zabezpečeníAustralian Open a olympiády v Tokyu, vizuální dashboard pro plánování strategií v Amazonu či NASA a podobně. Nevýhodou těchto firem pak jsou omezené možnosti růstu mimo programátorskou profesi, protože díky svému typu práce mívají hodně plochou organizační strukturu. Příklad takové firmy je třeba SDE Software Solutions (www.sde.cz.), kde pracuju, nebo jiné.

networking / konference / hackathon / jak se zapojit: https://code.kiwi.com/pythonweekend/

Mzda zaručena minimální https://discord.com/channels/769966886598737931/821411678167367691/910826527812370432

https://www.goodsailors.cz/ - popis firem, diverzita, hendikepy

Reddit - cscareerquestions - What are the harshest truths of being a software engineer?
https://www.reddit.com/r/cscareerquestions/comments/ihj5ha/what_are_the_harshest_truths_of_being_a_software/

Trying to land a high paying job in tech? Want companies reaching out to you?
https://randallkanna.com/the-standout-developer/

https://dariagrudzien.com/posts/the-one-about-researching-job-market/

Korporaty https://finmag.penize.cz/recenze/416865-za-stastne-dnesky!-vysla-pusobiva-studie-zivota-v-korporatu

My advice to her & to CS students who don't feel ready
https://twitter.com/venikunche/status/1217928485626355718


CO BY MĚL DNES DĚLAT JUNIOR
When I graduated a few years ago in the UK almost all the companies I applied to had a hackerrank/leetcode stage. Definitely worth doing as a junior dev.

Hi there, first of all sorry for the late reply - haven't been that active on Reddit of late.

I think for the current scenario - if you're actually a fresher who may have lost his/her job, then I'd recommend grinding more on GeeksForGeeks, Leetcode and also on contests on codechef, codeforces, kaggle, etc. - achievements on these platforms promote visibility if you post them on sites such as LinkedIn and/or AngelList.

I mentioned about being constantly in touch with CS subjects - primarily since if someone's actually out of job and if they suddenly get a call from a dream company, then it can become difficult for them to start preparing all of a sudden. Also, when you keep preparing yourself for a length of time, you're in some sort of a rhythm and then when the time comes to up the ante, you can do so easily.

Collapse of certain segments like travel - maybe utilize that time to do some exercising, do some sort of distance socializing (connecting with friends over a video call), hop onto websites that are offering free courses - last but not the least, one should keep their LinkedIn profiles updated. I got my 2nd job (around August last year) due to that thing only.


Tipy od holky ze Skotska
https://www.reddit.com/r/cscareerquestionsEU/comments/idhfuw/i_bring_some_hope_39_female_selftaught_just_got/

Leetcode rant
https://www.reddit.com/r/cscareerquestions/comments/jsrmtw/remove_cs_and_replace_with_leetcode_engineering/

Náhodné rady z FB
https://www.facebook.com/nixcraft/posts/4076448305701850

Olga, dodělat
https://slides.com/olgafomicheva/my-journey-as-a-developer#/4

jak uzitecny je realne glassdoor
https://www.reddit.com/r/cscareerquestions/comments/kaiyoa/is_it_just_me_or_is_glassdoor_becoming_less_and/


ZAVER
"...Půl roku se nevzděláváš a hned jsi pozadu." Tady bych asi byl opatrný, že je člověk za 6 měsíců bez vzdělávání pozadu. Reálně z hlediska práce si myslím, že to tak vždycky být nemusí (záleží, co bude dotyčná osoba konkrétně dělat). Problém vidím v tom, že bude stagnovat, tj. 6 měsíců se nikde neposune, nezlepší se v řemesle. Obecně bych možná ten řemeslný přístup trošku více akcentoval. Rozhodně bych více rozepsal "chuť něco tvořit" - tohle je podle mě killer feature programování. Ta možnost z ničeho vytvořit něco. Z prázdného editoru, kde bliká jen kurzor, k programu, který třeba interepretuje jiný program, sekvencuje genom něčeho atd. V tom je ta krása.
A taky to, že do toho kódu můžeš vložit kus sebe - jak řešením problému (algo), tak filozofií řešení (OOP vs. FP. vs. ?), ale i celkovým vzhledem kódu (vytiskni a pověs na zeď 😊).
Možná by se hodilo i zmínit, že je ideální mít mindset maratonce - není to závod na 100m, ale celoživotní cesta za "mistrovstvím."
Jinak celkově je ten závěr dobrý. Ten poslední odstavec je v nové podobě podstatně lepší, než byl 👍🏿


Na volné noze
https://navolnenoze.cz/novinky/it/



JAK KOMPENZOVAT HANDICAP (NESLYŠÍCÍ A TAK)
Ahoj Jakube,

poradil bych ti následující:

1) Stejně jako každý jiný junior, vytvořit si praxi na projektech. Popisuji to zde: https://junior.guru/practice/#projects Ostatně, celá ta stránka se soustředí na to, jak si sehnat praxi: https://junior.guru/practice/ Jsou tam i ty tipy na různá místa, kde se můžeš zapojit. Trochu je pak o tom i zde: https://junior.guru/candidate-handbook/#projects Mrkni i na možnosti stáží a dobrovolnictví: https://junior.guru/candidate-handbook/#internships

2) Kompenzovat své nedostatky. Ve tvém případě to bude to, že jsi neslyšící, ale znám programátora bez ruky, slepého programátora, znám lidi, kteří řeší různé psychické potíže. Někdo má zase omezení, která jsou úplně jiného charakteru, ale taky jej penalizují na pracovním trhu - třeba bydlí někde v Jihlavě a starají se tam o rodiče. Nemohou tedy jednoduše sehnat práci třeba v Brně nebo Praze a přestěhovat se za ní. Všichni musí něco kompenzovat.

Chce to jasnou strategii.

Pokud je tvé omezení, že neslyšíš, můžeš se zkusit zaměřit na firmy, kterým to vadit nebude, nebo se můžeš snažit ukázat, že to není problém. Ideálně možná oboje. V prvním případě bych ti doporučil zaměřit se na velké firmy, které mají zkušenosti se zaměstnáváním různě limitovaných lidí. Např. Red Hat nebo Oracle jsou velké firmy, které mají jako součást své firemní kultury přímo kodex, který říká, že chtějí zaměstnávat všechny lidi, i lidi s nějakým omezením - viz třeba https://blog.python.cz/blind-attendee-about-pycon-cz-2016

Druhá věc je všem firmám ukázat, že to prostě není problém. Vzhledem k tomu, že neslyšíš, asi nikdo nebude zpochybňovat, že bys mohl mít problém s programováním samotným, ale půjde spíš o komunikaci s ostatními. Přímo v CV bych tedy být tebou měl nějakou pasáž, kde popíšeš, jakým způsobem s ostatními běžně komunikuješ (protože pro lidi ve firmě to třeba není problém, ale neumí si to prostě jen představit a je pro ně jednodušší tě vyřadit). Dnes lidi dost pracují na dálku, takže to ti může i nahrát - sice asi nedáš nějaký videocall (nebo dáš? já vůbec nevím, co všechno dnes různé asistivní technologie dokážou), ale můžeš si s lidmi stejně jako ostatní psát apod. Největší průlom potom asi nastane ve chvíli, kdy budeš mít pozitivní zkušenost z reálného týmu. Našel bych si tedy být tebou nějaký tým lidí, ať už to bude neziskovka nebo nějaký nadšenecký hobby projekt, kde ověříte, že práce v týmu funguje, a budeš schopen od lidí, se kterými pracuješ, dostat nějaké doporučení. Toto doporučení si potom zase opět klidně přímo napiš do CV. Vyzdvihni, že máš za sebou tento týmový projekt a pod tím klidně citaci ve smyslu "S Jakubem se mi pracovalo skvěle, vše podstatné jsme zvládli vyřešit po Slacku, s jeho prací jsem spokojen. -- Tomáš, týmový kolega"

Abych to shrnul, pracuj na sobě jako každý jiný junior, vyselektuj si firmy tak, aby ses hlásil do těch, kde jim to bude vadit s nejmenší pravděpodobností, a snaž se v CV kompenzovat vysvětlováním a pozitivními referencemi, které jdou přímo proti jakýmkoliv předsudkům, které by kdo mohl mít.

Ještě mě napadá, že mohou existovat různé organizace, které řeší sluchové omezení, a mohli by vědět o jiných programátorech a dalších profesionálech, kteří prorazili. Já znám jen Radka Pavlíčka https://twitter.com/radlicek, který se angažuje ve webové přístupnosti nejen pro lidi se zrakovým postižením, možná mu zkus napsat. Jde o to, že pokud bys znal další programátory, kteří neslyší, mohl by ses jich vyptat na reálné zkušenosti, tipy jak prorazit, jak to firmám vysvětlit. A možná i na tipy jak efektivně pracovat v programátorském týmu, atd.

Doufám, že něco z mých tipů půjde použít :) Držím palce a měj se!
https://mail.google.com/mail/u/0/#search/nesly%C5%A1%C3%ADc%C3%AD/FMfcgxwJXxtFnJVBQdXrFLxRwmnqHQzg



How to become self taught dev
https://www.reddit.com/r/learnprogramming/comments/inm8z3/how_i_became_a_selftaught_developer/

Neplacené stáže ano/ne?
https://discord.com/channels/769966886598737931/788826407412170752/860449245131309116

part-time rozebrat, odkazy uvnitř
vše před a po https://discord.com/channels/769966886598737931/788826407412170752/935797332501491772


--- https://discord.com/channels/769966886598737931/1106936398893826058/1107086623709081710
Ode dneška je 6 měsíců (nebo 31 týdnů) do Vánoc, respektive týdne před nimi, kdy už ve většině firem nikdo nebude žádné přijímání řešit.

Na současném trhu (ještě před rokem to bylo jiné, snazší) říkám, že na hledání práce s určitou úrovní znalostí je potřeba 8–12 týdnů. Někdo má kliku a stačí mu méně a na druhé straně nedává ani těch 12 týdnů úplnou jistotu.
I během hledání se dál učíš a zvyšuješ si kvalifikaci a tedy i pravděpodobnost, že se to povede.
Samotné hledání ale zabere taky nějaký čas, takže už učení není v takovém tempu.

Řekněme, že by se to povedlo za 11 týdnů, takže ti zbyde 20 týdnů na to, aby ses co nejlépe připravil, než s hledáním vůbec začneš.
To je čas, který může stačit, ale má to několik podmínek:

— Chce to mít v podstatě fulltime čas a trávit tím řekněme 18–22 hodin čistého času týdně.
Ono to reálně ani o moc víc nejde, protože to není rutina, ale dělání a učení se stále nových věcí a to je záhul.
Nejde to tedy dělat spolu s prací.

— Dělat to efektivně: nevěnovat se věcem, které jsou zbytečné a učit se jen to nejnutnější (můžu ti dát detailní seznam, většinou anglicky…)

— Mít se kde zeptat a kde dostat zpětnou vazbu na to, co uděláš (to je třeba i tady klub)

Je taky třeba počítat s tím, že další roky se budeš muset pořád učit, to, co se jde naučit za 6 měsíců je zlomek toho, co budeš muset umět za 3 roky…
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


--- https://discord.com/channels/769966886598737931/788826407412170752/1102522930686079047
Nejednou jsme tady slyšeli od různých lidí varianty vlastně téhož příběhu, je to nějak takhle:

1️⃣ Bavil jsem se v nějaké firmě a říkali, že sice s jazykem X, který se učím, nikoho nepotřebujou, ale kdybych se naučil jazyk/technologii Y, tak s tím lidi hledají.
2️⃣ Přestože jsem už v X ledascos uměl, vrhnul jsem na Y, protože byla přece šance, že mě někde vezmou!!!
3️⃣ Přišel jsem do firmy s tím, že umím už dost z Y a dozvěděl jsem se, že pro mě práci nemají.

Proč to podle mě nemá moc šance vyjít?
– z pohledu té firmy nejde o žádný závazek, prostě to tak plácnou, že by si někdo takový hodil
– leckdy to ani neříká někdo, kdo ve firmě o najímání rozhoduje, ale nějaký tvůj známý, který tam pracuje jako programátor
– nikdo neví, co bude za několik měsíců, které ti bude trvat se to naučit, jestli budou zrovna toužit po juniorovi
– i kdyby to věděli, tak neví předem, kam se za tu dobu dostaneš, jestli to bude stačit
– pokud to bylo na pohovoru, tak třeba už vědí, že lidsky a z dalších hledisek by to s tebou bylo ok a jde jen o tu odbornost, ale leckdy je to neformální pokec, takže to klidně může selhat na mnoha dalších faktorech, stejně jako všechny další juniorní přijímací řízení, kde je běžná větší nejistota a tedy i větší množství odmítnutí, takže sázet vše na jednoho koně je dost riskantní.

Je možné, že to někomu to vyšlo, tak se prosím podělte, zatím jsem ale takovou verzi neslyšel.
---


--- https://discord.com/channels/769966886598737931/788833053425926195/847575361696825416
Ono už je to asi i vedle, ale dávám raději i sem 🙂 Letní stáž v JetBrains: https://www.facebook.com/315284691916211/posts/3773302836114362/
---


--- https://discord.com/channels/769966886598737931/788826407412170752/902872779924316161
Jinak jedna věc, na kterou mě <@!819485466231177256> přivedl - je dobrý vědět, že v průběhu roku máte z definice různý šance na úspěšné přijetí. Drtivá většina firem funguje na bázi ročních rozpočtů - a čím větší firma, tím striktnější ten proces je. Což znamená, že v průběhu roku se ukáže, že je třeba přidat člověka, ale není na něj/ni žádná část rozpočtu přiřazená (protože když se rozpočet plánoval,, tak se to nevědělo - nebo neprosadilo). Což znamená, že se může snadno stát, že taková pozice bude vypsaná při nejbližší možné příležitosti - což je typicky další rok.
No a velká část firem má fiskální rok a kalendářní rok identický (my zrovna ne, náš fiskál končí teď v říjnu), takže typicky od října/listopadu už je jasné, kolik peněz a na jaké pozice bude a začínají se vypisovat - s ideálem, aby ten nový člověk nastoupil co nejdřív od začátku roku.
Není to náhoda, dá se s tím pracovat - a doporučuju to. Pokud naopak máte zájem o konkrétní firmu, zjistit jak to tam mají s fiskálem a rozpočtem vám s tím časováním může pomoct taky. Totéž platí, když se nabírají absolventi - typicky firma, co chce absolventy je chce mít "co nejdřív" poté co absolvují. Ale zároveň ví, že málokdo nastoupí v červenci, protože si chce užít poslední prázdniny. Takže se snaží naplánovat hiring kampaň tak, aby proběhla PO zkouškovým a PO státnicích (protože student, který řeší jestli a jak dokáže vůbec projít nemá v hlavě prostor na pohovory), ale zároveň aby stihli ti lidi nastoupit v září nebo říjnu.
Obecně chci tímhle dlouhým textem říct, že má smysl přemýšlet o faktoru času při hledání práce - a to i z pohledu druhé strany (která se zase snaží vcítit do vás, takže je to nekonečný cyklus).
---


--- https://discord.com/channels/769966886598737931/788826407412170752/887687959669800970
Ano, existují lidé (spíš firmy), kteří ti umí pomoci za peníze, s tím, aby ses (ty) naučila, co je třeba. I v té intenzivní podobě, kterou plánuješ. I u nás je jich několik.
Debata o tom byla tady
https://discord.com/channels/769966886598737931/769966887055392768/860589911634477076 + aktualizace
https://discord.com/channels/769966886598737931/769966887055392768/866680751499902986
---


--- https://discord.com/channels/769966886598737931/789092262965280778/1050378327627669544
Nedávno jsme v <#769966887055392768> řešili návratnost investice (ROI) do switche.
Byla to diskuze k článku https://www.seznamzpravy.cz/clanek/ekonomika-firmy-cesi-se-predelavaji-na-ajtaky-vydelavaji-i-nasobky-toho-co-driv-216944

Psal jsem:
> A vůbec tam nepočítají náklady, které na to jsou. Ať už ušlý příjem nebo na kurzy samotný. Finanční ROI je mizerný, návratnost je někde v dalekém budoucnu.
> Důvody pro switch jsou samozřejmě i nefinanční a ty jsou pro mnoho lidí podstatnější.

No a teď čtu na stránkách GFA tohle
> Chceš začít v IT, ale dávat za školné tolik peněz připadá moc? My tvrdíme opak. Školné se ti totiž za pár měsíců vrátí ve výplatě.
> ‍Pojďme počítat:
> V rámci našeho bootcampu máš 100% garanci umístění a nástupní plat minimálně 40 000 Kč hrubého. Průměrná mzda našich čerstvých absolventů je však 47 200 Kč.
> 47 200 Kč x 4 (měsíce) = 188 800 Kč
> Stačí ti tedy v nové kariéře odpracovat 4 měsíce a školné budeš mít zpátky na svém účtě. Tím ale zdaleka nekončíš, protože platy v IT neustále rostou. Za 2 roky z tebe může být medior a do 5 let už můžeš být seniorní programátor, jehož hrubá mzda se s přehledem vyšplhá i přes 100 tisíc měsíčně.

No tak tedy pojďme, ale nic nevynechejme…
Kalkulačku ROI do Google Sheetu jsem udělal už tehdy, ale teď jsem tam doplnil ty mzdy dle toho co píšou a taky cenu online kurzu s platbou předem.

https://docs.google.com/spreadsheets/d/1uxb1ZotwxRAB40u99LE4B59hC15nHkLO4WNZNrA9V0Q/ (Udělejte si kopii a klidně si doplňte svoje čísla.)

Jasně, že se to někdy zlomí. Dřív, pokud někdo před tím nevydělával moc peněz, ale rozhodně to není tak rychle, že náklady jsou zpět za pár měsíců.
Mám v té logice někde chybu? 🤔
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1048193165875757096
ber inzeráty jako kdyby si firmy psaly seznam vánočních přání - i když dostanou od ježíška něco podobného, jsou rádi
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1047556321274245182
Ja by som to chapala tak, ze intern moze/nemusi byt plateny a ten internship je na pevne danu dobu, ktora ked skonci, tak sa uvidi co dalej, ale nemusi sa udiat nic. A trainee moze/nemusi byt plateny (ale asi skor ano ako nie) a po skonceni zacne normalne pracovat 🤔
---


--- https://discord.com/channels/769966886598737931/797040163325870092/1044323870737432617
Pokud narazíte na inzerát, kde je napsáno _mladý dynamický_ kolektiv nebo firma, dejte link do threadu. Myslel sem, že to vymřelo podobně jako fialová saka z devadesátek.
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1030150072895295552
**Zajímaly by mě vaše zkušenosti s Úřady práce.**
Ti, co se pustí do hledání nebo změny na fulltime a nejsou na rodičovské s nimi asi mají zkušenost.
A taky schvalují proplácení různých rekvalifikací.
Připomenu, že je dobré se tam registrovat už jen proto, že si nemusíte platit zdravotní pojištění.

Sám jsem byl na ÚP registrovaný před asi 7 lety a musím říct, že to byl poměrně depresivní zážitek a byl jsem rád, že reálně nejsem odkázán na jejich „pomoc“.

Jaká byla vaše zkušenost?
Snažili se vám nějak pomoci?
Tlačili vás do nějakého zaměstnání na které máte kvalifikaci?
Chápali, že se sami učíte a práci si pak najdete?
Nebo vás nechali žít?
---


--- https://discord.com/channels/769966886598737931/788833053425926195/1002163691120246834
**FB skupiny aj. místa, kde jde číhat na pracovní nabídky, nebo tam jde dát příspěvek s vlastním představením a vlastními požadavky a čekat, kdo se ozve**

🔵 Pyonieri - Python SR & ČR https://www.facebook.com/groups/pyonieri/
🔵 Frontendisti.cz práce https://www.facebook.com/groups/frontendistiprace/
🔵 IT jobs / Práce v IT https://www.facebook.com/groups/1806114342948040/
🔵 Backendisti práce https://www.facebook.com/groups/backendistiprace/
🔵 Práce v IT - nabídka, poptávka, rady a tipy https://www.facebook.com/groups/pracevit/
🔵 Ajťáci pro IT komunitu https://www.facebook.com/groups/114237176143464/
🔵 Czechitas Příležitosti https://www.facebook.com/groups/292829031070632/
🔵 PRÁCE - PROGRAMÁTOŘI, VÝVOJÁŘI, KODÉŘI - PRÁCE A BRIGÁDY V OBLASTI IT https://www.facebook.com/groups/684672464913744/
🔵 IT jobs in Brno, Praha, Ostrava https://www.facebook.com/groups/1410077719228836/
🔵 Práce pro webové programátory https://www.facebook.com/groups/469950746429675/
🔵 IT Jobs & Internships (Czech Republic) https://www.facebook.com/groups/168885910244057/
🔵 Data Jobs - Data Analysts, Data Engineers & Data Scientists - Prace https://www.facebook.com/groups/1788236724824404
🔵 No Fluff Jobs CZ/SK –⁠ IT Junioři https://www.facebook.com/groups/604043784717336/

⚠️ Předem upozorňuju, že některé z nich jsou vyloženě toxické, ale svůj jednorázový účel přesto mohou splnit. Pokud se představíte, nejspíš vám přijde spousta nesmyslných zpráv (udělej něco zadarmo, za pár stovek, atd.), ale mohou se ozvat i seriózní nabídky, je dobré to poctivě filtrovat. Ty zprávy najdete někde bokem, protože třeba zrovna FB zprávy od cizích lidí schová do nějakého šuplíku a nezobrazí je normálně s notifikací, tak je dobré to ručně kontrolovat. Stejně tak nabídky tam mohou být od kdejakého nadšence, který vám pak nemusí být schopen platit, takže bacha a lustrujte si, komu odpovídáte.

👉 Pokud víte o dalších, zmiňte je ve vlákně. Tento příspěvek tady připnu a budu ho průběžně i editovat, dokud věc celou nepřesunu do nějaké specializované stránky přímo v rámci webu junior.guru.
---


--- https://discord.com/channels/769966886598737931/769966887055392768/999304168261029968
Ja si tu jen naskocim s mym pet-peeve - nemam rad oznaceni *soft skills* vs *hard skills*, obsahuje to nejakou implicitni vahu. Preferuju misto toho rozdeleni *technical skills* a *professional skills*. Imho to lepe vyjadruje, co ty skills (a hlavne jejich absence) znamena - neoznacil bych za seniora nekoho, kdo se chova neprofesionalne, neumi komunikovat, nechape/nechce chapat prdukt v sirsim kontextu a nema empatii s uzivateli.
---


--- https://discord.com/channels/769966886598737931/769966887055392768/983610893973745714
Já mám taky pocit, že nejsme názorově tak vzdálený. Snad všichni tu souhlasíme, že udělat kariérní switch je dřina, pot a nutné oběti. A každá minuta se počítá a posouvá člověka vpřed. Opakovaně tu pomáháme lidem omámeným sladkými marketingovými se zakotvit v realitě a vyvracet mýty (ty jsou i v příručce). Kde se domnívám neshodneme je ta premisa toho, že "co dělám, musím dělat na 110% abych byl skvělej". A tam myslím, že je právě velkej rozdíl v junior x senior, kde pro juniora je nový snad všechno a posouvá se mílovými kroky v pracovní době, což se o seniorovi asi tak snadno tvrdit nedá - ten pak víc skilluje mimo pracovní dobu, aby dělal větší kroky, pokud si to přeje. Takže podle mě má junior skvěle našlápnuto i když nedělá nic mimo pracovní dobu. A druhý háček, jak tu psalo víc lidí, každej nemusí chtít být špička v oboru, anebo ani nemůže (povinnosti, vlastní omezení..), a to je taky v pořádku. Nejzdravější je podle mě být si vlastním měřítkem úspěchu - já teď x já před rokem.
---


--- https://discord.com/channels/769966886598737931/769966887055392768/983340740778266647
Tohle podepisuju. Přečetl jsem celou tu diskuzi. Předně dík, že jste se udrželi a zvládli to ještě relativně nekonfliktně, i přes rozdílný pohled na věc 😉 Pokusím se shrnout, jak to vidím já. Mám dojem, že každý má trochu pravdu a že se to tu míchá do jednoho velkého guláše.

Přesně jak psal <@419662350874837003>, většina lidí nic „navíc“ nedalají a normálně se v oboru uživí a jsou spokojení, po práci jdou na kolo nebo pečují o děti, zajedou na chatu, prostě řeší život. Kvalitně si odpočinou a nic jim nechybí. Absolutní minimum lidí z oboru dělá aktivně open source, píše si blog, čte tuny knih, přednáší, jezdí na mnoho konferencí, nebo přijde na sraz programátorů. Pokud jste někdy zašli na Pyvo, jste z hlediska vlastní proaktivity dál, než 99 % lidí, kteří se v Česku živí programováním. Další sebevzdělávání lidi běžně nechávají na tom, co se přihodí v práci. Nový projekt, nová technologie, novinka z oboru, co poslal kolega do Slacku nebo vysvětlil na obědě, jednou za rok třeba nějaká konference, občas nějaké školení. V normální firmě s normálním kolektivem mi přijde skoro nemožný nenasávat novinky v rámci pěny dní. Samozřejmě jsou i firmy a kolektivy, kde se člověk rozvojem zasekne na dekádu a taky to jde.

I z vlastní zkušenosti bych řekl, že <@839123616665698354> má pravdu v tom, že kdo dělá něco „navíc“, tak se mu prostě vrátí „víc“, a to v mnoha ohledech. Každý přečtený odborný článek nad rámec toho, co se vám přihodí ve firmě, každá konference, každý sraz, na který zajdete. Cokoliv navíc se prostě z mé zkušenosti 4x vrátí. Někdy třeba za rok za dva, ale vrátí. Ani nejde o to, aby člověk byl top programátor, ale prostě si tím otevírá příležitosti, je víc v obraze, dokáže lépe posloužit svému týmu, je lepším seniorem, profesně a kariérně roste. Z definice slova „navíc“ to ale není pro každého. Nechci zašlapávat u lidí ambici - sám jsem příkladem toho, kam to jde dotáhnout, když člověk dělá věci navíc. Nechci to akorát lidem předkládat jako standard. Jak psala <@791020144661889054>, když si to přečtu jako junior, tak budu mít očekávání, že bez věcí navíc budu nula, což prostě není pravda. Zase chci lidem říkat, že ty možnosti existují, protože pokud na ně tu energii a chuť mají, je to skvělý kariérní výtah.

Takže za mě je OK nedělat nic navíc. Zároveň kdo má ty možnosti a ambici, existuje 30 věcí, které navíc dělat lze a komukoliv o nich rád řeknu a poradím jak na ně, protože junior si tím může reálně pomoci a urychlit svůj postup. Ale pouze v případě, kdy má sám pocit, že to dělat chce. Nerad bych dával signál, že bez toho to nejde a že je to nutná podmínka, protože si to ani nemyslím. A nepřijde mi např. etické takový tlak paušálně vyvíjet na svoje lidi ve firmě. Nebo obecně na juniory. A přijde mi OK, pokud někam do firmy nastoupím jako junior a chtějí po mě věci navíc a já to nedávám, jelikož potřebuji ten odpočinek, nebo mám rodinu, tak mi přijde OK tu práci změnit. Protože jsou firmy, kde věci navíc nechtějí a je zbytečné, aby se ten člověk topil v depkách, pokud nemusí.

Prostě kdo bude chtít, toho pošlu do vesmíru a až na měsíc, ukážu mu cestu. Ale kdo z jakéhokoliv důvodu do vesmíru nemůže nebo nechce, tak chci, aby chápal, že většina letadel do vesmíru nelítá a úplně v pohodě dopravuje velice efektivně spoustu lidí po celé planetě na letových výškách a bez stavu beztíže a že to fakt stačí.
---


--- https://discord.com/channels/769966886598737931/788826407412170752/979547837052362772
hledal jsem alespoň part-time myslel jsem že půjdu do lidlu, protože part-time a linked in je jako šikana lidskýho přístupu :D,...

Pak jsem napsal příspěvek na facebook co chci co nabízím (jo taky jsem dostal nový léky, protože jsem se mezitím málem zabil - tak trochu bez nadsázky, ale to je spíš ta psychika... 😄 ))) a sehnal super práci. Na částečný úvazek, Vývojář v Javě (kterou jsem dělal  v green fox academy) a s lidma který konečně taky myslí že zajetý koncepty pruzení nadřízenej podřízenej sou totální bulshit. ..

Takže Konečně pracuju. Jako vývojář. Success story? Možná možná se mi nelíbí na něco takového dávat takovej label... Každopádně jsem fakt rád že to za těch asi deset let vyšlo, a stálo to za to. Kdybych si to tenkrát nevybral, nikdy bych to nedělal a nemyslel si že toho sem schopnej.... GL to you too 😄 :)))
---


--- https://discord.com/channels/769966886598737931/789107031939481641/977161736987754546
Formou bodyshoppingu pracuji já, tak kdybys pak sbíral názory, ráda přispěju.
---


--- https://discord.com/channels/769966886598737931/789107031939481641/973580991274823740
<@668226181769986078>  Nebylo by tohle téma možné přidat do příručky pro juniora? Já jsem třeba vůbec nevěděl, že to takhle funguje a dozvěděl jsem se o tom až nedávno, právě na  tom pohovoru, taktéž jsem o tom nikdy nečetl... Ale možná jsem to jen přehlédl a v příručce už o tom máš napsáno. 🙂
---


--- https://discord.com/channels/769966886598737931/788826407412170752/972951035226247258
Práce, kterou jste doteď dělali jako koníčka po večerech najednou děláte přes den a máte za ni zaplaceno. Učíte se 3x rychleji -> nové informace nasáváte jak podvědomě (protože se to na vás valí ze všech stran a chtě nechtě jste součástí), tak vědomě a cíleně (protože máte silnější potřebu a motivaci se učit, už jen pro to, abyste si tu práci udrželi).
Píšu, nevzdávejte to, ale ve zkušební době není ostuda to vzdát, pokud cítíte, že to není ono. Nemusí vám vyhovovat prostředí (malá kancelář nebo velký open-space), tým (ne s každým si lidsky sednete), práce (představovali jste si něco jiného), časové možnosti (dojíždění moc dlouhé a drahé), nebo naopak remote či home-office není tak super, jak jste si mysleli.
Buď máte to štěstí a víte předem, co hledáte (a moc nedoporučuji se do něčeho nutit s tím, že si možná zvyknete), nebo si to prostě musíte vyzkoušet a pak zvážit případnou změnu. I samotná změna projektu může být pro někoho problémová, na to pozor už při pohovoru, zda si chcete přechod na jiný projekt určovat sami nebo vám nevadí, když vás podle potřeby realokují jinam.
To se teď stalo mně, po 3 měsících zaškolování na jednom projektu (a s ním související tým, prostory, režim, atd.) mě zítra čeká v rámci zákaznické společnosti nový projekt, nové prostory, nový tým, nový režim. Já jsem dost přizpůsobivá a obecně nemívám se změnami problém, přesto je pro mě tento přesun trochu „šok“, že se to v praxi opravdu děje. 😊
Co bych si dnes před nástupem do práce poradila, tak hlavně KLID. Kladla jsem na sebe od začátku vysoké nároky a zbytečně se tím nervovala. Nepřemýšlela jsem nad tím tak, že mám celé 3 měsíce na to, abych poznala novou práci, spíš jsem to brala jako snahu nic nezkazit a za každou cenu se tam udržet. 😊 Do dnešního dne se mi přes LinkedIn ozvalo asi 10 dalších recruiterů, zda nehledám pracovní příležitost (a to nemám zelené kolečko opentowork). Lidí je opravdu nedostatek, a pokud nejste na stávající pozici spokojeni, nebojte se změny. Držím palce!
---


--- https://discord.com/channels/769966886598737931/788826407412170752/971919809212190790
No jak nějaká holka, která je trans a fakt hezká říkala - znám obě varianty byla jsem kluk a teďka jsem holka, a to že máte spoustu nabídek a matchů ať už skvělých nebo míň nebo dokonce otravných na tinderu, bych nevyměnila za to když vám nikdo nepíše a nikoho nezajímáte.

Jinými slovy je rozdíl psát firmám bez praxe a bez vzdělání(a jiné - hledám part-time, x , y, z, ....)  atp., milion životopisů a horkotěžko přemýšlet jak dostat více než nula až jednu reakci - děkujeme vám ale dali jsme přednost jinému kandidátovi - než napsat inzerát který můžete pojmout úplně po svém - protože běžné sociální sítě to snesou ba co často ocení, můžete vyzdvihnout svoje silné stránky které by jste do životopisu nedali - ale sem tak nějak sedí - a dostat reakce od reálných firem a lidí zaměstnávajících programátory (checkujte zprávy a žádosti o zprávy 😛 ) a hlavně! Je to inzerát podle Vás, budou s větší šancí rovnou reagovat na vaše podmínky a "rukopis".

Pokud se vaše hledání pozice vymyká standardu toxického linked-inu, nebo obecně považovaných nejlepších podmínek pro start v IT (vlastní projekt, škola, bootcamp, plný-úvazek, plynulá angličtina, 10 let praxe 😛 atp.) a nejste úplně šablonový uchazeč, nejen že možná (VY!) zaujmete firmu která vám s větší šancí sedne, ale hlavně dostanete možnost napsat úplně cokoliv a vybírat si ať už z dobrých, méně dobrých a úplně mimo nabídek které musíte vyfiltrovat ale zareagovali oni na vás.
A ať to klapne nebo ne, v nejhorším to smažete / dáte novou zprávu za týden / za měsíc - a i když budete muset někomu vysvětlit že mu nenaprogramujete za dva tisíce apku do mobilu kterou potřebuje na doma - za večer (spěchá) a 2000 korun (jestli by to teda nešlo za pět set nemám zrovna cash) a jinému že dobrovolničit od února do konce příštího roku nemůžete( a vlastně vám to ani nepřijde úplně fér, ale sorry nechtěl jsem se vás dotknout), tak dostanete reakce které mají šanci na úspěch.

Napsání klidně může trvat kolem pěti minut (nebo víc :D).
---


--- https://discord.com/channels/769966886598737931/788826407412170752/971690440443191306
Tenhle příspěvěk z jedné veřejné FB skupiny by mohl být pro někoho inspirací, jak proniknout do nového oboru. Naprosto jednoduchá strategie a při tom za pár hodin hned 2 příležitosti <:notbad:842465452911099905>
---


--- https://discord.com/channels/769966886598737931/797040163325870092/971670339052503060
Mi říkal jeden aktivní týpek z TAČR (agentura pod úřadem vlády, která rozděluje státní granty na aplikovaný výzkum), že vidí 3 druhy státních ajťáků:
1) ne moc dobrej: v komerční sféře mě nechtěj (což je co říct, protože díky nedostatku lidí jsem viděl, jak firmy zkously dost děsný lidi)
2) doklepu to v klidu do důchodu, ktere není daleko
3) idealisti, co chtějí, aby stát dobře fungoval (ti většinou dříve nebo později vyhoří)
---


--- https://discord.com/channels/769966886598737931/788826407412170752/952720555872747581
Většinou tady řešíme reaktivní způsob hledání práce. Tedy koukáte na nabídky a reagujete na ně.

Občas ale někde vidím **aktivní způsob**, kdy se switcheři nějakým způsobem sami ozvou, že hledají práci. Typicky někde na FB ve skupině s nabídkami práce někdo napíše: *„Projel sem nějaký kurzy, udělal tady projekt a teď bych chtěl najít první práci, mám šanci s tímto? Nevíte o něčem?“*.

Nevím jak to reálně funguje, ale pro mě až překvapivě často tam jsou odpovědi typu *„SZ“* nebo *„Napiš na hr@nasefirma.cz“*.

Taky je možný, že někdo i přímo oslovuje firmy, které mu nějak přijdou zajímavé, jen to není vidět (tedy uvnitř té firmy to vidí). To se ostatně dělalo i před mnoha lety. Na vlastní oči jsem viděl, jak někdo přišel na recepci firmy s papírovým CV, že by to chtěl předat HR (ano, je to dlouho 👴)

Co si o tom myslíte?
Zkusil jste to někdo?
Zvažujete že byste to zkusili?
---


--- https://discord.com/channels/769966886598737931/788826407412170752/925305675838550036
https://twitter.com/norootcause/status/1475518692041510915?s=21
---


--- https://discord.com/channels/769966886598737931/864434067968360459/910398477794697216
Nevím jakého přesně rázu jsou tvoje problémy, ale napadlo mě, že tahle firma zaměstnává převážně lidi s nějakými problémy, šéf vývoje je na vozíku, pracujou tam i lidi s psychiatrickýma diagnózama https://www.goodsailors.cz/ je sice v Děčíně, ale jak píšou na webu *„Kotvíme v Děčíně, fyzicky ale můžeme být kdekoliv“*
Známý, který má Crohnovu chorobu tam dělá projektovýho manažera a říkal o nich samý dobrý věci.
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1100742108870086716
Včera <@771661208007868446> hrozně pěkně mluvil o herním testování, tak jsem si vzpomněl na jeden web, jehož název mluví asi za vše. Kvalitu a kvantitu všech těch informací může posoudit někdo povolanější, ale říkal jsem si, že by se to mohlo někomu líbit/hodit. Já si tam jen něco málo četl a přišlo mi to zajímavý 🎮 https://www.gameindustrycareerguide.com/how-to-break-into-video-game-industry/
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1099677728803913749
Jojo včera. Za mě dobrý, nemám teda žádnou zkušenost z podobné akce, ale kupodivu jsem u toho vydržela až do konce. Neobešlo se to bez technických potíží, kdy to každého občas vyhodilo a musel se přihlásit znovu, takže si tak povídáte s HR a najednou zmizne, no byla sranda 😄  Chat byl neustále plný zpráv typu nejede mi mikrofon, nejde mi kamera, nic neslyším, nevidím, kam zmizel ten nebo onen. Pozdravila jsem se s <@1028946296771461180> . Nakonec ani kamera nebyla nutná, spoustu lidí jelo bez kamer, jen přes mikrofon a pokud člověk nechtěl, tak nemusel mluvit s nikým. Součástí byl i malý kvíz, kdy v rámci světa bylo 5 otazníků, které jste museli najít a odpovědět na různé otázky či hádanky.

Celkem se mi líbilo představení ČSOB ze kterého jsem měla pocit, že hodně podporují remote pozice i částečné úvazky a mají dobrou firemní kulturu. Co se týče firemní kultury, tak se mi hodně líbí i brněnská firma IRESOFT, momentálně nabízí pozice na C#, Python a React. Podle příspěvků na LI by měli uchazeči dostat zpětnou vazbu vždy, ikdyž si vás nepozvou ani na pohovor, dají vám vědět a řeknou proč, což mi přijde dost super. Více takových firem.

Na základě mého LI se mi ozvala na mail paní z jedné firmy, která nebyla součástí veletrhu, takže jsem s ní v kontaktu a uvidím co z toho bude.

I přes technické problémy hodnotím kladně, mě všechno jelo jak mělo, jen mě to občas vyhodilo a musela jsem se připojit znovu. Nevím jak přínosné je to pro lidi co už vyloženě aktivně hledají práci, já to beru zatím jako takový průzkum trhu.
---


--- https://discord.com/channels/769966886598737931/1083734944121102436/1088109106482651216
Na IT network jsem práve v kurzu "programátor ww aplikací - C# .NET". Mám to přes ÚP a při podávání žádosti mi paní zdělila, že do zdůvodnění žádosti je nejlepší napsat průzkum aktuálního stavu trhu práce, proste data a fakta, ne jen pocity. Ideální je mít příslib práce, ale není to nutné. Nakonec mě ještě iniciativně dostali do programu Outplacement, který novému zaměstnavateli přispívá na mzdy do výše 15k na 9 měsíců. Tak uvidíme, jestli to pomůže se uplatnit.
ITnetwork jsem volil hlavně kvůli akreditaci a ÚP. Líbila se mi i GFA, ale to bylo výrazně dražší.
V podstatě to, co popsali lidi přede mnou, jsou i moje dojmy. Kvalita e-learningu je závislý na tématu a tvůrci obsahu. Já měl největší problém s tím, že jsem lekci prošel, poctivě procvičil zadání a pak v řešených úlohách tápal, jelikož se s těmi informacemi daný úkol nedokázal udělat. Hledal jsem řešení v dikuzích, googlil, ptal se známých a tak postupoval dále. Taky jsem si k tomu vzal ještě kurz na Udemy, protože mi video učení více sedí. Vidím, co se tam děje, lektor to i patřičně popisuje a tak se mi ty informace lépe spojí a mohu pak kódit i sám. Postupem času jsem se zlepšil a zvládal udělat Jednoduché a Středně náročné úlohy sám. Pokročilé jsem rozpracoval do stádia, co jsem věděl a pak hledal pomoc nebo se prostě podíval do řešení, přečetl si kód, snažil se tomu porozumět a pak to reprodukovat po vlastní ose. Někdy to šlo někdy ne. Zde myslím, že má ITnetwork slabinu v tom, že není k dispozici nikdo, kdo by ti dokázal obratem pomoci se hnout z místa a vysvětlit "polopatě", co, proč a jak se děje. Porozumět, co se v kódu děje, mi nejvíce pomohla rada od zkušeného známého, který mě navedl, jak to pozorovat ve VS. To byl pro mě "game changer". Do té doby jsem se trápil a procházel lekcemi sem a tam, jestli nejsem trotl a něco mi neuniklo nebo jsem to nepochopil. Prezeční školení je fajn, chlapi jsou vstřícní a pomohou věci lépe vysvětlit. A to, že jsou tyto dny s odtupem po ukončení E-L, je jen dobře ...
---


--- https://discord.com/channels/769966886598737931/1066992347725971516/1067089251595984947
Nabídky s požadavkem na 1-2 roky praxe bych nepřeskakoval, ale zkusil začít motivační dopis takhle:

> Vím, že požadujete 1-2 roky praxe a já narovinu píšu, že je nemám. Vytvořila jsem ale sama dva větší projekty (odkazy v přiloženém CV), které si můžete prohlédnout a sami usoudit, kolik práce by pro vás bylo doučit mě věci, které potřebujete.
---


--- https://discord.com/channels/769966886598737931/1063112761841831990/1063113351573536938
**__Nevýhody__**

•   ** Agentura si bere provizi**
 výši se nedozvíš - která je počítaná z výše tvé mzdy a dojednává si jí agentura s klientem, takže pro firmu jsi dražší položka, takže záleží na tobě jestli s tím budeš OK
•    Nevztahuje se na tebe zákoník práce
takže při propouštění jde většinou externista jako první pokud jde o budget a není tu ani výpovědní lhůta - ta je pak na domluvě s klientem
•    **Neplacené volno, nemocenská**
Protože nejsi zaměstnanec, tak většinou nemáš nárok na placenou dovolenou, nemocenskou, firemní benefity a odměny, školení atd...  - ale i tady hodně záleží na klientovi, jsou firmy, které nabízí stejné podmínky i externistům jako internímu zaměstnanci nebo aspoň rozšířené, v TM ale ne
•   ** Omezené přístupy a práva**
Protože nejsi zaměstnanec tak HW máš vlastní a občas nemáš práva a přístupy takovém rozsahu jako má interní zaměstnanec - zase záleží na klientovi...
•    **Staráš se sám o daně, daňové přiznání, atd... **
pokud tedy nejsi přímým zaměstnancem agentury a o odvody se ti stará zaměstnavatel...


Hodně záleží na tom, jak to mají dané firmy a agentury nastavené, co máš ve smlouvě s agenturou a co ti bude více vyhovovat. Vždy si pořádně projdi smlouvu/objednávku než ji podepíšeš...
---


--- https://discord.com/channels/769966886598737931/1058066444677550132/1058313285495164978
Ahoj 🙂 podpořím tu Dana, v jeho tvrzení, že po menších úvazcích než full-time zájem moc není. Mě se povedlo sehnat před rokem svoji 2. práci v IT (a ta první trvala jen 3m) na 0.6 (potřebovala jsem prostor na vlastní praxi https://www.nelaprovazi.cz). Ale jednoduchý to nebylo, firmy ještě tak slyší trochen na 0.8, a cokoliv pod 0.5 mi přijde naprosto nereálný jako první job. Na částečnej úvazek bys musel být hodně naskillenej switcher (což jsem myslím byla), mít kliku (taky můj případ) a mít prostor na 0.6 výš, na míň bys musel mít hodně velkou kliku a asi spíš hledat něco formou hůře placené brigády, ideálně přes známý.
---


--- https://discord.com/channels/769966886598737931/1002976022486057020/1003021387142807659
Vzdy je dobre delat neco navic, ale je hrozne tezke rict co presne a konkretne. Za me klicove body jsou:

* Vzdy premyslet co je mym cilem, tedy proc neco delam (jaky problem v realnem svete resim)
* Umet problem rozsekat na kousky ktere jsou snadno uchopitelne a popsatelne, tedy rozlozit slozity problem na jednodussi.
---


--- https://discord.com/channels/769966886598737931/1118986066117009519/1118986066117009519
Asi by se mi hodily praktické tipy, jak na to. Zatím na všech akcích, kde jsem byla, jsme po akci na sebe velmi často všichni jen hloupě zírali, popř. mluvilo jen pár lidí.

Nikdy jsem si na nikoho nevzala kontakt a jako bonus jsem se skoro nikdy neúčastnila žádné "afterparty", které jsou pro mne kvůli bariérovosti extrémně náročné.

Zkouším si občas vychytat někoho na LI, ale všude doporučují i tak udržovat alespoň virtuální kontakt. I na Seduo jsem si vysbírala pár přednášek na téma networking, ale vůbec se nechytám.

Nesmírně mne děsí, že nejčastěji lidé nachází práci právě přes známosti a já tuhle možnost nemám.
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1120721530561773649
K zamyšlení: https://www.idnes.cz/finance/financni-radce/omyly-uvazovani-psychologie-kariera-uspech-jan-urban.A230616_081121_viteze_sov&h=9B92CD62E5D55260B84BF71F5E2391D8
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1119307390576230492
Petra Nulíčková měla hromadu skvělých tipů na meetupu ReactGirls před měsícem a tady je to na záznamu
https://www.youtube.com/watch?v=uNL3yEzNsbQ
---


--- https://discord.com/channels/769966886598737931/789107031939481641/1134507945871286293
Vyšla „příručka“ o tom, jak vyjednávat o mzdě nebo platu na pohovoru. Je tam toho strašně moc a pro programátory nebo testery nemusí být všechno relevantní, ale i tak to bude dobrý zdroj pro někoho, kdo by se chtěl do tématu ponořit 🙂 💰 https://www.careerdesigner.cz/penize
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1129510378649440359
Super podcast od <@839123616665698354> a Šárky Kousalové o IČO vs HPP 👍 https://overcast.fm/+1O3llyR6c
---


Zdravim Honzo. Jsem z Czechitas a napadlo me, zda by pro vase sledujici nebyl relevantni nas Job Fair, veletrh pracovnich prilezitosti v IT? Mame letos dva, jeden v rijnu v Praze a v listopdu v Brne. Jobfair.czechitas.cz


--- https://discord.com/channels/769966886598737931/1165950098681892934/1166254719367401503
Obecne se pry temto inzeratum rika 'fake jobs' , davaji se mimo jine i z techto duvodu:
* firma potrebuje jenom ukazat akcionarum, ze roste: Chteji nabirat, ale 'proste nejde nikoho najit'
* firma zkousi, kolik se hlasi lidi a postupne snizuje nabidku
* chysta se nejaky novy projekt a tak se dela pruzkum trhu, jestli budou lokalne lidi
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1164528096851017841
Od října do konce roku se nábor často zpomaluje, nebo úplně zastavuje, podle toho, jak je na tom firma s budgetem na daný rok. Pracoval jsem v IT náboru + teď jsem podobné věci řešil ve firmě. To tomu taky nepomáhá... Já si třeba minulý rok domluvil práci právě v této době, ale taky se začátkem až v únoru.
---


--- https://discord.com/channels/769966886598737931/788832177135026197/1161225273186992238
Michael Lopp, druhé vydání knihy Being Geek, nové jméno The Software Developer’s Career Handbook. Ještě jsem nečetl, ale bude určitě pecka. Kdo neznáte jeho styl, projděte si alespoň blog https://randsinrepose.com/archives/the-software-developers-career-handbook/
---


--- https://discord.com/channels/769966886598737931/1178734115441356850/1178816328694517850
Jestli potřebují někoho nabrat ale nemají čas dělat nábor, tak mě to upřímně nezajímá. To je jejich problém. Já mám vlastní starosti 😄
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1172808574221701180
Nicméně junior.guru vydal několik příruček, jak na první práce. A tento e-book je sice z jiného zdroje, ale speciálně o financích a je skvěle zpracovaný 💸

https://www.careerdesigner.cz/penize
---


--- https://discord.com/channels/769966886598737931/1150481852516290641/1169670818926706860
Tak jsem ráda, že jsem napsala o relevantnější zpětnou vazbu a dostal se mi zajímavý vhled. Frontendistů je teda asi opravdu jak máků 😦 Asi se budu muset přece jen učit ten backend (Node.js)
---


--- https://discord.com/channels/769966886598737931/1194368531433783407/1194921225189859368
Ahoj, tak za mne rikam NE NE NE NE a jeste milionkrat NE!!!!

Pripad Tatanka ma tu spojitost, ze mel take kamarada a (spolu)majitele firmy a ze to samo o sobe NEZNAMENA, ze to vzdy musi dobre dopadnout.
Nechci rozebirat davno uzavrene a zhojene historie, takze jenom vecne a konstruktivne:

I kdyz je kamarad, do tve hlavy nevidi, a tvoje ucebni/pracovni schopnosti znat nemusi.
To, co ti nabizi je "postav mi zadarmo stodolu, a kdyz se to dobre naucis (o cemz rozhodnu ja a ty mas malou sanci to ovlivnit), zaplatim ti, abys mi postavil i barak".
Kazdy kope za sebe, coz je uplne prirozena lidska vlastnost.
---


--- https://discord.com/channels/769966886598737931/1189829769320202260/1189841216154636399
Zkusím přirovnání.

Chceš být truhlářem a sám ses ve své skromně vybavené domácí dílničce naučil základy: jaké jsou druhy dřeva, pracovat s pár základními ručními nástroji a umíš udělat skříňku a stůl a možná židli a to jen jedním způsobem a celkem si udělal jeden kus od každého.

- přesvědčíš mistra, že tě to baví, že se to chceš učit a že budeš na sobě makat, takže tě vezme do učení
- máš pořád co dělat, protože mistr má dost zakázek
- mistr ohlídá, abys to nedělal špatně a klienti nedostávali šunty
- když něco uřízneš moc krátký, tak tě sice mistr nepochválí, ale v těch tunách dřeva, které zpracuje každý měsíc, se to ztratí
- okoukáš od mistra jak vůbec dělat komplexní výrobky a používat při tom nářadí, které by sis ani nemohl sám dovolit
- zjistíš, co všechno vlastně ve velké truhlárně dělají, co všechno se na takové úrovni v praxi řeší
- hlavně okoukáš od mistra i jak shání zakázky, jak komunikuje s klienty, jak řeší, když jsou nespokojení, jak stanovuje ceny
- po nějaké době, kdy se už nemáš co naučit, se uděláš pro sebe a klidně to můžeš začít zkoušet dělat jinak, ale budeš mít ten základ
---


https://vesecky-adam.medium.com/100-interviews-in-1-year-what-have-i-found-part-i-the-data-090aebe68ff5
https://www.youtube.com/watch?v=1efZbhcYY4g
https://www.youtube.com/watch?v=qGCRy-Rl2p0
https://www.youtube.com/watch?v=icwvzPez_mc
https://www.youtube.com/watch?v=9dKKn5XNrn0
https://www.youtube.com/watch?v=FJbVpaYIeUg
https://www.youtube.com/watch?v=uNL3yEzNsbQ


--- https://discord.com/channels/769966886598737931/769966887055392768/1202540543767216188
Dobré video, zaznelo tam niekoľko podľa mňa veľmi dobrých tipov, pár vecí by som ale k tomu dodal.

To aby si juniori skúsili hľadať prácu aj mimo tech je dobrý point. Ako človek ktorý pracuje pre banku a viem, že keď hirujeme ku nám do teamu, máme zúfalo málo kompetetných uchádzačov k tomu ale mám niekoľko poznámok.

- pozície v týchto firmách často nenájdete pod názvom, pod ktorým by ste ich čakali - napríklad moja pozícia sa volá credit policy manager ale posledný pol rok vyvýjam interný balíček v pythone a 5 rokov robím datového analytika
- to sa ale spája aj s tým, že súčasťou vašej práce bude oveľa väčšie prepojenie s "bussinessom" a "netechnickými" zadaniami - v banke napríklad s rôznymi bankovými procesmi atď
- veľmi rýchlo sa vám môže stať, že budete technicky najskúsenejší človek v teame - pokiaľ teda neradi experimentujete, robíte chyby, potrebujete veľa spätnej väzby od technicky seniornejšich ľudí, bude vám to chýbať. Pokiaľ sa radi realizujete môže to byť naopak veľmi vhodné prostredie.
- občas tu ale zaznieva správna otázka: Prečo ste sa rozhodli byť SW dev? Pokiaľ je vaša odpoveď napríklad v zmysle, že ste chceli lepšiu prácu, work life balance a technicky sa rozvýjať aby ste mali lepší plat a vašim cieľom nebolo byť 100% sw dev ktorý iba programujete, môžete nájsť firmy kde im na týchto hodnotách záleží a nie je to tech
- veľa toho bude záležať na ľuďoch a nadriadených - z banky môžete mať občas pocit, že je to 10 firiem v jednej, v jednom teame je to sluníčkové, v inom čistá pakáreň

Neprepadal by som ale depresii, myslím si, že už len samotná snaha a záujem ktorý tu väčšina ľudí do toho vkladá vám dáva výhodu, ktorú si s trochou šťastia určite niekto všimne <:meowsheart:1002448596572061746>
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1202352655717114007
Dneska jsem narazila na zajimave video od Kayla https://m.youtube.com/watch?v=a6IIhwZv4ls
---


--- https://discord.com/channels/769966886598737931/788832177135026197/1202770155470454784
V <#769966887055392768> se konverzace nedávno opět stočila k situaci na pracovním trhu a jaké jsou těžké časy pro juniory. Ještě jsem to neviděl, ale rovnou sem hodím. Lane je super a myslím si, že tam bude dost dobrých tipů/informací : https://www.youtube.com/watch?v=6nz8GXjxiHg
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1208794856709824552
https://www.lukaspitra.cz/10-zkusenosti-z-naboru-200-lidi/
---


--- https://discord.com/channels/769966886598737931/789107031939481641/1210341399250341888
Tohle je sice pro zkušené programátory, ale myslím, že tam jsou zajímavé rady i pro leckterého juniora. https://newsletter.pragmaticengineer.com/p/finding-the-next-company
---


Tvrdíková - různé pozice do startu
https://www.linkedin.com/posts/lucietvrdikova_startvit-activity-7183000015961780224-j885?utm_source=share&utm_medium=member_desktop


--- https://discord.com/channels/769966886598737931/769966887055392768/1223220648957186070
Firmy nemají sdílenou představu ani o tom kdo je vůbec junior, takže asi tolik k jakýmkoliv složitějším konstruktům 😅
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1222146790460231710
Když se tady říká part time, tak se neříká se jak moc „part“: 80 % vs. 60 % vs. 20 % je velký rozdíl.
Taky je rozdíl, jestli někdo pracuje každý den, jen kratší dobu nebo jsou celé dny, kdy tam není. Stejně tak může být ok, že je někdo dostupný jen 4 hodiny dopoledne a jinde je zase lepší, když je dostupný 2 hodiny dopoledne a 2 hodiny odpoledne.
Samozřejmě záleží na typu práce a tom, jak je to kde organizované.
---


--- https://discord.com/channels/769966886598737931/1231221825665499156/1231459291165102194
V tom shrnutí od <@668226181769986078> jsou spíš obecné nevýhody té právní formy.
---

deleni firem spis podle cost/profit https://newsletter.pragmaticengineer.com/p/profit-centers-cost-centers


místa, kde se mohou lidi nabízet, nebo kde mohou hledat práci - https://discord.com/channels/769966886598737931/788833053425926195/1002163691120246834


For the most part all entry level jobs are “we understand you are going to be worthless and be a net drain on productivity for your team for at least 6 months” with the expectation that you learn and grow to be contributing and advance to mid level.


--- https://discord.com/channels/769966886598737931/789087476072710174/1294259606297776168
<@&1134476995229663374>
Po čase připomínám, že jsem dal k zdarma dispozici malý nástroj, který vám může pomoci: [Tabulka pro plánování, sledování času a hledání práce](https://discord.com/channels/769966886598737931/1047219933647487146)

Trackovat si kam a na jaké inzeráty jste poslali reakci není vůbec od věci. Většinou to totiž nevyjde na pár pokusů a v hlavě to neudržíte.
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1288888379668168796
Párkrát jsem tu už podobnou debatu viděl, ale zapomněl jsem to zainzerovat do <#1187770159595794472>, tak aspoň napíšu tady.

Za malou chvíli nám začíná diskuzní **Nakopni svou kariéru aneb jak to chodí v korporátu**, kde si budu povídat s Honzou Baráškem a já budu zastávat roli oponenta vůči korporátům, tak se můžete těšit na dynamickou debatu s pohledy z obou stran! 🙂

https://www.youtube.com/watch?v=Lyut1YWYuyw
---


--- https://discord.com/channels/769966886598737931/789107031939481641/1288179526521589760
Přemýšlím, jestli přeci jen nechceš to IČO zvážit — [po důkladném spočítání si](https://www.youtube.com/watch?v=iJGjTFDYw9A) samozřejmě — pokud to pro některý firmy je blok.

S paušální daní to ani není moc administrativy: založit živnost a přihlásit se k paušální dani a pak jen platit měsíčně fixní částku. Není potřeba nic dalšího vykazovat a odevzdávat.

Proti o něco složitější (nutnost odevzdat daňové přiznání a poslat 2 „přehledy“ k pojištěním) možnosti se to vyplatí od cca 680 tisíc ročně.
---


--- https://discord.com/channels/769966886598737931/1285884920648040449/1285927173827461210
4. Hack je, že nehledáš part-time nabídky ani jim dopředu nepíšeš, že to chceš a řekneš si o to až na pohovoru, kdy měli šanci tě poznat. mluvíš třeba už s teamleadem a ne jen s HR. Ano, třeba to bude dealbreaker, ale pořád větší šance…
---


--- https://discord.com/channels/769966886598737931/1283445215323099197/1283469132104335380
odkážu svoje video https://youtu.be/iJGjTFDYw9A
sice bych tam pár věcí odebral a pár přidal, ale to hlavní platí.
---


--- https://discord.com/channels/769966886598737931/916361226588684328/1275769449722413109
Takze si vyber no. Ale osobne si nemyslim, ze to je jednodussi cesta. Junior manualni tester, je dle meho nazoru mene kvalifikovana pozice nez junior programator. Takze zabere mene casu a usili se na to pripravit, ale bude vetsi natrask na vypsane pozice, vyber kandidatu bude trochu random podle “culture fit” a ne podle “hard skills”, a dostanes mene penez. Nic to nevypovida o te praci, ta je dulezita a vede k seniornim pozicim, ktere jsou taky dulezite a je tam uz potom i kvalifikace, kterou se muzes ohanet. Byt dobry QA neni jen tak a je potreba umet a znat hodne veci. Ale ten uplny zacatek ma relativne nizkou vstupni latku. Jenze je to dvojsecna zbran. A jsou to ruzne prace, mezi kterymi se tezko karierne preskakuje. Takze osobne bych se vydal na cestu, ktera plni moje zadani - napriklad pokud chci programovat, tak pracovat na tom abych byl programator, pokud chci testovat a bavi me to, abych byl tester. Neohlizel bych se na zdanlivou jednoduchost, protoze co je jednoduche v kroku 1 je pak nakonec velmi tezke v kroku 2. Neexistujou zkratky.
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1257570562352353320
Nedávno tu byla přednáška od analytika z Alma Career  (Jobs.cz atd.)
Vytahal jsem data z toho videa, protože mi přijde zajímavé číslo počet **reakcí na inzerát**. Chápu ho tak, že říká, jaká je tlačenice na dané pozice. To je unikátní pohled, který zvenku nemáme.

Data jsou tuším za první 4 měsíce tohoto roku a nejde jen o juniorní pozice (sice filtroval i podle „vhodné pro absolventy“, ale pak nebylo vidět data u poloviny pozic).

Tak jak to prezentoval, tak ty nižší čísla znamenají, že tam je fakt problém lidi sehnat (i když vám 8 nebo 10 zájemců může připadat hodně, tak je to průměr! navíc ve výběrkách bývá část zájemců fakt mimo), naopak přes 30 u testerů znamená určitě, že mají už z čeho vybírat.

**Zdaleka si ale nemyslím, že by to měl být hlavní faktor, pokud se rozhodujete pro jazyk.** Vypadá to sice exaktně, ale nic to neříká o tom, s jakou úrovní dané specializace máte šanci najít první práci a jak je těžké se na ni dostat a tipl bych, že u C++ se čeká mnohem hlubší pochopení než třeba u Pythonu.

A taky tam chybí informace o tom, jaké procento lidí se hlásí na kterou pozici „špatně“, tedy bez dostatečné kvalifikace. Opět tipuju, že na testing nebo React bude mnohem víc těch, kteří toho ještě neumí dost, ale zkouší to, než s C++, takže je možné, že reálně tam taková konkurence není.

```markdown
| pozice         | inzerátů | reakcí na inzerát |
|----------------|----------|-------------------|
| C++            | 241      |  8.0              |
| DevOps         | 155      | 10.8              |
| C#             | 342      | 12.4              |
| Node.js        |  74      | 13.9              |
| .NET           | 317      | 14.1              |
| Java           | 279      | 15.3              |
| Android        |   ?      | 17.6              |
| PHP            |  95      | 17.7              |
| Python         | 197      | 19.2              |
| JavaScript     | 265      | 19.6              |
| Data Scientist | 166      | 22.2              |
| React          | 170      | 24.5              |
| Tester         | 337      | 32.1              |
```
---


--- https://discord.com/channels/769966886598737931/789107031939481641/1245067053593919529
Tohle bych rád vypíchl z aktuální přednášky: https://discord.com/channels/769966886598737931/1075814161138860135/1245066837117632513
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1334481244917858356
Slyšel jsem to tak, že 100% není problém reagovat po pár měsících znovu.
1. Ty se můžeš dost posunout, pokud „jen“ hledáš práci a děláš při tom třeba na svém projektu, tak třeba 3 měsíce můžou znamenat ohromný posun.
2. Může se změnit situace ve firmě a i „stejný“ člověk najednou může dávat smysl.
3. Nedá se počítat s tím, že by firmy fungovaly tak, že mají databázi lidí, co se k nim někdy hlásili a jen do ní sáhly a ty lidi oslovily. Některé možná víc a spíš u seniornějších lidí. Je tedy lepší se aktivně ozvat.
---


--- https://discord.com/channels/769966886598737931/789107031939481641/1329486370208485467

---


--- https://discord.com/channels/769966886598737931/769966887055392768/1328977405402157078
Nejsem mobilní vývojář (napsal jsem před dvaceti lety nějakou stáž v Java Mobile edition 👴 ), velmi zhruba tuším, co se v tom světě děje. Tohle shrnutí mi přijde přehledné. https://newsletter.pragmaticengineer.com/p/cross-platform-mobile-development
---


--- https://discord.com/channels/769966886598737931/789107031939481641/1349716580270997525
Ahoj. Včera jsem se potkal s IT HR Monety banky, řekl jsem jí, že mám kurz testera a už se na mě dívala skrz prsty (co to zase bude za rychlokvašku) okamžitě byl můj kredit o 50% nižší.
Nakonec se mi jí podařilo trošku přesvědčit, že zas tak marný nejsem, že nějaký slušný základ mám a odnesl jsem si alespoň to na čem víc zapracovat. Ale ten začátek byl hrůzostrašný.
V rámci aktuální situace/přetlaků juniorů by bylo možná lepší takové rozhovory začínat spíš tím co umím, jaké mám zkušenosti, říct jim Váš příběh o tom co Vás tam přivedlo a ke kurzům se dostat později.
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1380107658127998977
Daniele Procida sepsal „něco jako junior.guru“ pro africké vývojáře ❤️ https://fanaka.readthedocs.io/ Pokud vám přijde těžký sehnat si IT job v Česku, tohle může posloužit jako reality check. A pokud máte nějaké kamarády z Afriky, sdílejte. A pro mně je to inspirace jak by šlo junior.guru vylepšit, co by šlo doplnit.
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1364204177567387779
„Účastníci byli v průměru ochotni vzdát se 15 až 30 procent svého platu, aby se vyhnuli toxickému pracovnímu prostředí. Nejvíce ceněnou vlastností byla práce bez sexuálního obtěžování, podle respondentů měla hodnotu téměř třetiny mzdy.“ A pak kde se bere ten pay gap! A ještě: „…ženy se mohou vyhýbat kariérnímu postupu či vedoucím rolím ne proto, že by neměly ambice, ale proto, že chrání samy sebe.“ https://houdekpetr.blogspot.com/2025/04/neco-za-neco.html
---


--- https://discord.com/channels/769966886598737931/1351222802296082588/1353735180111708280
A jeste jsem zapomněl na https://wug.cz - to je free , ale Brno 🙂
---


--- https://discord.com/channels/769966886598737931/1351222802296082588/1353735208158888039
Odkaz na největší místní konferenci k danému jazyku, to je cenná věc. Co udělá junior? Možná zváží účast, jasně, ale hlavně si otevře https://www.updateconference.net/cs/2025/partners a všechny prokliká a podívá se na otevřené pozice, případně jim zkusí napsat i „na studeno“ 😄 Protože firmy, které sponzorují = firmy, které mají peníze, případně nabírají.
---


--- https://discord.com/channels/769966886598737931/1351222802296082588/1353735510064894053
Seznam přednášejících nemají, tam je to podobný trik (každý pro někoho pracuje), ale třeba tady vidím pod jmény hodně firem https://wug.cz/prednasejici
---


#} -->
