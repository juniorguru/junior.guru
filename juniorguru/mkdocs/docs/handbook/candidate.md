---
title: Hledání první práce v IT
thumbnail_title: Jak najít svou první práci v IT
description: Jak začít hledat svou první práci v IT? Jak se připravit na pohovor?
template: main_handbook.html
---

{% from 'macros.html' import blockquote_toxic, blockquote_avatar, blockquote, link_card, jobs_inline, video_card, video_card_engeto, note with context %}


# Hledání první práce v IT

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }} Původně se „Příručka“ říkalo pouze této stránce, takže má velkolepý úvod a závěr, jako by tady další stránky ani nebyly. Cílem je postupně tuto dlouhou „nudli“ rozsekávat do kratších samostatných stránek.
{% endcall %}

## Úvod    <span id="preface"></span>

Ještě než se začteš, jednu věc si musíme ujasnit hned. **Toto není e-book.** Nacházíš se na „živé stránce“, na které stále probíhají úpravy. Kdykoliv tady může přibýt něco nového, takže není od věci se sem občas vrátit. Všechny změny [najdeš na GitHubu](https://github.com/honzajavorek/junior.guru/commits/main/juniorguru/mkdocs/docs/handbook/), o těch důležitých se můžeš dovědět na sociálních sítích junior.guru nebo prostřednictvím [klubu](../club.md).

A věci mohou přibývat i díky tobě! Pokud máš připomínku, vlastní zkušenost, nebo nápad na novou kapitolu, napiš na {{ 'honza@junior.guru'|email_link }}.

### Předmluva    <span id="foreword"></span>

Znáš [základy](learn.md) a máš [praxi](practice.md)? Nastal čas zkoušet své štěstí na pracovním trhu. Jak si ale začít hledat svou první práci v IT? Jak se připravit na pohovor?

{{ blockquote_toxic(
  'Nauč se programovat, firmy v IT berou z nedostatku lidí každého, kdo má jen zájem. Do začátku si řekni aspoň o pade.',
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
2.  Mít vytvořený nějaký [malý vlastní projekt](practice.md#najdi-si-projekt) jako praktickou ukázku své práce.
3.  Mít na projektech naučenou schopnost dostat zadání a rozložit ho na podproblémy (algoritmizace).

#### Velmi užitečné znalosti navíc

*   [Angličtina](learn.md#jak-si-zlepsit-anglictinu), čím víc tím líp!
*   Základy práce s [Gitem](https://naucse.python.cz/course/pyladies/sessions/foss/).
*   Práce s příkazovou řádkou (ideálně tou v [Linuxu](https://cs.wikipedia.org/wiki/Linux), tzn. Bash).

Ano, **toto opravdu většinou stačí!** Neboj se toho, že se učíš Python, ale v nabídkách je Java. Důležité je především **umět programovat** — další jazyk nebo technologie se dá doučit poměrně rychle.

Není potřeba jít víc do šířky a bez jasného cíle se učit tady trochu HTML, tu základy C#, tam úvod do datové analýzy — jen proto, že někde o těchto věcech uslyšíš. Místo toho si **[vyber projekt](practice.md#najdi-si-projekt) a na tom pracuj.** Potřebuješ získat praktické schopnosti, které ti jednodenní workshop nebo čtení knih nedají. Dlouhodobá práce na projektu ti sama ukáže, jaké konkrétní dovednosti a technologie se potřebuješ doučit. A po dokončení projektu ti to ukážou požadavky v pracovních inzerátech a [dotazy na pohovorech](#otazky-na-tebe).

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

[Ne](motivation.md#potrebujes-vysokou-skolu). Běžní zaměstnavatelé ocení [praxi](practice.md) víc než titul. **Webovky nebo mobilní appky udělá samouk stejně dobře jako absolvent.** Studenti VŠ jsou tvá největší konkurence, ale na rozdíl od tebe jsou semletí pěti lety v českém školství. Nadšení z nich zpravidla nesrší a nemají moc praxe. Žena po rodičovské, která si rok šla za svým a učila se při všem shonu programovat po večerech, smete svou motivací každé ucho z VŠ jako nic.

Zrovna v inzerátech nabízejících první práci v IT nebo částečný úvazek se však ještě stále lze setkat s **omezením, že jsou jen pro studenty či absolventy**. Je to proto, že lidi na druhé straně inzerátu ([recruitery](#naborari), šéfy) vůbec nenapadlo, že nováčci v oboru se rodí i jinde než na univerzitě. **Zkus se ozvat i tak.** Nic za to nedáš. Buď firmě otevřeš oči, nebo se rozloučíte už při prvním kontaktu.

{% call blockquote_avatar(
  'Vývojáři nepotřebují titul z informatiky! Přestaňme zbytečně bránit lidem pracovat v IT.',
  'emma-bostian.jpg',
  'Emma Bostian'
) %}
  Emma Bostian, [Coding Coach](https://mentors.codingcoach.io/) & [Ladybug Podcast](https://www.ladybug.dev/)
{% endcall %}

### Záleží na věku? Pohlaví?    <span id="age-gender"></span>

[Ne a ne](motivation.md#myty-o-programovani). Programování není balet, [začít se dá v jakémkoli věku](https://www.youtube.com/watch?v=dKclZ55d_F0). Byť jsou stále ještě v menšině, ženy se dnes programátorkami stávají běžně. IT už dávno nevypadá jako na [této fotce](https://www.forum24.cz/jak-dopadli-chlapci-z-brutalni-parby-informatiku-2/), i když si toho někteří možná ještě nevšimli. **Pokud je z pracovního inzerátu cítit diskriminace, vůbec se jím nezabývej**. Kromě toho, že je to [protizákonné](https://www.google.cz/search?q=pracovn%C3%AD%20inzer%C3%A1t%20diskriminace), tak firma, která se myšlenkově zasekla ve středověku, nebude zrovna dobrým přístavem pro začátečníky.

{{ video_card(
  'Tomáš Hisem: Z horníka programátorem',
  '16min',
  'https://www.youtube.com/watch?v=dKclZ55d_F0',
  'Když se v 45 letech dozvěděl, že důl Paskov bude uzavřen, musel se rozhodnout, co dál. Dostal nečekanou příležitost rekvalifikovat se na programátora.',
) }}


## Jaká mít očekávání    <span id="expectations"></span>

### Kde jsou firmy, které berou každého?    <span id="hungry-market"></span>

„Nauč se programovat, firmy v IT berou z nedostatku lidí každého, kdo má jen zájem.“ Toto je bohužel **mýtus**. IT rozhodně je přístupný obor a projít změnou kariéry za poměrně krátkou dobu lze, ale **jednoduché to není a hned to také není**. [Firmy sice opravdu nemají dostatek lidí](https://blog.freelo.cz/pruzkum-mezi-programatory-penize-nejsou-vse/), kteří umí programovat, ale často se rozhodnou investovat spoustu času i peněz do hledání zkušených, než aby přijali juniora a tomu se pak museli věnovat. **Počítej s tím, že můžeš projít i desítky pohovorů, než najdeš svou první práci v IT.** Je to běžné. Připrav se na to, že hledání práce ti může zabrat i měsíce. Obrň své sebevědomí i rodinný rozpočet, bude to náročný kolotoč.

### Proč práci nabízí hlavně velké firmy?    <span id="why-big-companies"></span>

Pro firmu je zaměstnání juniora velký výdaj. I když je to zdánlivě výhodné z hlediska mzdy, firma tě musí všechno učit a věnovat se ti, což ji stojí dost peněz. Byť se dají najít nabídky i od středních či malých firem, **obecně jsou do juniorů ochotny investovat spíše [větší firmy](#prace-pro-velkou-firmu), které na to mají jak finance, tak zázemí**.

Dalším prostředím, kam se probojuješ snadněji, je **státní správa**. Firmy se předbíhají v tom, jaké finanční podmínky nebo benefity nabídnou zkušeným lidem, takže pro většinu z nich není atraktivní pro veřejné instituce pracovat (to si raději vezmou velkou mzdu jinde a pak [dobrovolničí](https://cesko.digital/) ve volném čase). Pro tebe ale může být toto prostředí i mzdové ohodnocení dobrým startem.

### Kolik si vydělám?    <span id="salary"></span>

Bavíme se o první práci. Musíš se ještě hodně učit a bude chvíli trvat, než dosáhneš na ty [vysoké mzdy, kterými se všichni ohání](https://www.czso.cz/documents/10180/95632581/063009-18.pdf/0f4ba681-c6b3-4226-b81e-6634cac046fb?version=1.2). **Podle dvou anket [Smitia](https://smitio.com/) ([první](https://blog.smitio.com/clanek-mzdy-v-it-podle-smitia), [druhá](https://blog.smitio.com/clanke-mzdy-absolventu-ocima-firem-a-ajtaku)) začínají nováčci průměrně na 30.000 Kč hrubého.** V Praze a Brně to může být i více, v regionech i výrazně méně. Rovněž lze očekávat rozdíly mezi nabídkou větších a menších firem. Platí ale, že šikovní lidé jsou schopni se poměrně rychle dostat se mzdou nahoru — třeba už i za rok praxe.

Jedním z vodítek, jak si určit nástupní mzdu, může být i tvé předešlé zaměstnání. Pokud tvá mzda zásadně nepřesahovala 30.000 Kč, můžeš si ze začátku prostě **říct o totéž, co ti chodilo na účet v minulé práci**. Příjem tvé domácnosti zůstane stejný, ale do budoucna má velkou pravděpodobnost růst.

### Najdu práci externě, na dálku?    <span id="remote-work"></span>

Před rokem 2020 platilo, že práci na dálku si musíš **vysloužit svou samostatností**. Na začátku kariéry se hodně učíš, topíš se a voláš o pomoc, potřebuješ někoho, kdo ti ke konkrétním věcem, které firma dělá, vysvětlí kontext. Mnoho lidí má za to, že je lepší, když se v takové chvíli můžeš otočit na židli a zeptat se přítomných kolegů.

Situace kolem covidu-19 ale nakonec nedává firmám příliš na výběr. Práce z domova přestává být vnímána jako občasný benefit, stává se plnohodnotnou formou spolupráce. Spolu s tím **firmy objevují i způsoby, jak na dálku zaučovat nové lidi**, čímž odpadá jedna z největších překážek, proč je tento způsob práce nevhodný pro juniory. Lze tedy stále častěji najít i nabídky práce pro juniory, které jsou částečně či zcela „remote“.

Práce na dálku se během pandemie stala trendem, nejde však o nic vyloženě nového. Souhrnný článek [Práce z domova](https://honzajavorek.cz/blog/prace-z-domova/) nebo kniha [Remote](https://basecamp.com/books/remote) vyšly skoro před dekádou, ale i tak mohou dodnes sloužit jako aktuální a kvalitní zdroje informací o této problematice. Projdi si alespoň ten článek, ať se dokážeš dobře připravit i na nevýhody, které práce na dálku přináší.

Možná znáš pojem [digitální nomádství](https://honzajavorek.cz/blog/prace-z-domova/#digitalni-nomadi) a láká tě představa, že ťukáš do notebooku někde na pláži. Na fotkách to vypadá dobře, ale [realita je složitější](https://www.svetpatritemcoseneposerou.cz/blog-ikigai-a-japonsky-smysl-zivota.html) — a nejde jen o displej na přímém slunci nebo písek v klávesnici. Hezký úvod a spoustu dalších odkazů najdeš v článku na [Travel Bibli](https://travelbible.cz/digitalni-nomadstvi/).

{% if jobs_remote %}
#### Nabídky práce na dálku
Přímo na junior.guru najdeš [nabídky práce výhradně pro juniory](/jobs/). Některé z nich práci na dálku umožňují!
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

Když nahlédneš do IT, zjistíš, že kolem programování se motá spousta dalších profesí. **Pokud tě nějaký směr láká nebo rovnou baví, zkus zjistit, co k tomu potřebuješ a nauč se základy.** Cítíš v sobě [manažerské buňky](https://www.martinus.cz/?uItem=606009)? Rýpeš se v [hardwaru](https://www.raspberrypi.org/)? Chceš [programovat hry](https://warhorsestudios.cz/)? Máš [sklony k psaní](https://www.writethedocs.org/)? Baví tě [vizuální věci](https://frontendisti.cz/)? Trápí tě, [když je software pro lidi komplikovaný](http://www.asociaceux.cz/zacinate-s-user-experience)? Pro každou z těchto otázek existuje odpověď v podobě specializace. Jdi za tím, co si myslíš, že by tě mohlo bavit. Neměj strach, že se naučíš něco, co následně nevyužiješ. Ve tvé situaci je to extrémně nepravděpodobné. Cokoliv se naučíš, brzy tak či onak uplatníš. Pokud se tedy nezačneš učit [nějaké ezo](https://cs.wikipedia.org/wiki/Ezoterick%C3%BD_programovac%C3%AD_jazyk).

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
*   **Digitální agentury** zpracovávají zakázky pro jiné firmy. Projekty přicházejí a odcházejí, je větší prostor pro stavění nového na zelené louce a pro zkoušení nejnovějších technologií. Zákazník může mít prostřednictvím „projekťáků“ velký vliv na tvou každodenní práci, je zde riziko vyššího stresu pro všechny zúčastněné. Některé firmy také provozují _[body shopping](https://www.google.cz/search?q=body%20shopping%20programov%C3%A1n%C3%AD)_, tedy že pracuješ „[na IČO](#prace-na-ico)“ a agentura tě přeprodává jako [žoldnéře](https://cs.wikipedia.org/wiki/%C5%BDoldn%C3%A9%C5%99).<br>
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
Přímo na junior.guru jsou [nabídky práce výhradně pro juniory](/jobs/) a občas se mezi nimi objeví i nabídka dobrovolnictví (neziskovky a malé projekty zde mohou inzerovat zdarma). Zrovna dnes tam něco je:
{{ jobs_inline(jobs_volunteering, 2, jobs_url='/jobs/remote/') }}
{% endif %}


### Stáže    <span id="internships"></span><span id="unpaid-internships"></span>

Některé firmy vypisují stáže (anglicky _internship_), ale **není jich mnoho**. Často jsou [jen pro studenty VŠ](#je-potreba-vs), protože firmu nenapadne, že by se na ně mohl hlásit i někdo jiný. Mnohdy se také podaří naplnit stáže přes známosti nebo partnerství se školami, takže není důvod je veřejně inzerovat.

Stáž přitom může být **dobrá příležitost, jak začít bez zkušeností**. Firma tě zaučí do jednoduchých úkolů a po čase se rozhodne, jestli tě chtějí vzít. A často chtějí, když už do tebe investovali nějaký ten čas. I kdyby to nevyšlo, je z toho aspoň praxe, zkušenost, brigáda na léto.

Pokud studuješ, máš k dispozici nástěnky, poradenská centra, pracovní veletrhy, webové stránky studentských spolků, webové stránky aj. prezentace výzkumných pracovních skupin, spolužáky, cvičící, přednášející…

**Ostatním zbývá [asertivita](https://cs.wikipedia.org/wiki/Asertivita).** Odmítli tě v nějaké firmě, protože hledají někoho zkušenějšího? Zeptej se jich na stáž. Líbí se ti nějaká firma? Napiš jim a zeptej se na stáž. Významnou roli hraje také [networking](#networking). Choď na [srazy a konference](practice.md#najdi-inspiraci-poznej-lidi), tam se aktivně druž a — ptej se na stáž.

{% call blockquote_avatar(
  'Už jsem viděl stáže dohozené přes bratrance, klienty, plesy, spolujízdu. Najednou jsi konkrétní člověk a pokud vypadáš inteligentně, firma si řekne: „Proč ne?“',
  'petr-messner.jpg',
  'Petr Messner'
) %}
  Petr Messner, profesionální programátor
{% endcall %}

Pozor na **neplacené stáže**. Je na tobě si vyhodnotit, zda se ti stáž bez odměny ve tvé situaci vyplatí a zda si to vůbec můžeš dovolit. Ač je možné se s neplacenými stážemi setkat běžně u nás i v zahraničí, je to [věc na hranici zákona i etiky](https://www.e15.cz/the-student-times/neplacene-staze-aneb-jak-nedocenitelna-je-zkusenost-1348117). Podle českého práva [není neplacená stáž jednoznačně protizákonná](https://www.epravo.cz/top/clanky/neplacena-praxe-ve-firmach-studenti-i-zamestnavatele-na-hrane-zakona-100528.html), ale **existuje šance, že v případě kontroly ze strany inspektorátu může být taková praxe vyhodnocena jako nelegální práce**.

{% if jobs_internship %}
Přímo na junior.guru najdeš [nabídky práce výhradně pro juniory](/jobs/). Zrovna dnes jsou mezi nimi i nějaké stáže:
{{ jobs_inline(jobs_internship, 2, jobs_url='/jobs/remote/') }}
{% endif %}

### Práce pro velkou firmu    <span id="big-companies"></span>

Velké firmy a instituce [jsou v lepší pozici](#proc-praci-nabizi-hlavne-velke-firmy), aby mohly zaměstnávat začátečníky. Práce pro ně má své **výhody**:

*   [Bývají ochotné platit víc](https://danluu.com/startup-tradeoffs/) než menší firmy.
*   V mezinárodních firmách pracuješ s lidmi různých jazyků a kultur. Čeká tě moderní a profesionální _workplace_.
*   V širokých týmech se můžeš specializovat na určitou věc, pracovat na tématu do hloubky.
*   Kariérní růst je zorganizovaný a tvůj postup _mohou_ určovat jasná pravidla, ne pouze rozmar šéfa.
*   Můžeš mít k dispozici dražší služby a nástroje. Můžeš mít větší možnosti cestovat za firemní peníze, např. na [konference](practice.md#najdi-inspiraci-poznej-lidi).

Mají více peněz a nebývá pro ně problém je investovat. Ovšem jen pokud mají pocit, že je daná věc dobrý nápad, a občas je bohužel velmi těžké korporaci o takových dobrých nápadech přesvědčit. Preferuje své zajeté koleje. Mezi další **nevýhody** patří:

*   Mnoho věcí předepisuje struktura a procesy, na jejichž podobu máš minimální vliv.
*   Upřednostňovány jsou starší technologie, které má firma roky odzkoušené a všichni s nimi umí. Ke zkoušení nových moc vůle nebývá.
*   Mezinárodní firmy musí splňovat širokou škálu zákonů a regulací. Z toho plynou omezení a komplikace. Jednoduché věci často nelze dělat jednoduše.
*   Můžeš si připadat jako kapka v moři, číslo v kartotéce. Užitek tvé práce může působit vzdáleně.
*   U mezinárodních firem je ze zřejmých důvodů zcela nepostradatelná komunikativní úroveň [angličtiny](learn.md#jak-si-zlepsit-anglictinu).

Zajímavě korporace rozebírá [Lukáš Linhart v přednášce o své kariéře](https://youtu.be/l7zUC0T1E98?t=5671) nebo [Dan Luu v článku Big companies v. startups](https://danluu.com/startup-tradeoffs/). Oproti obecnému přesvědčení **nemusí být velká firma nutně bez zajímavé práce nebo divokých změn**. Vnitřní reorganizace nebo změny korporátní politiky umí přinést stejný stres jako je ten, který ti budou slibovat ve [startupech](#prace-pro-startup).

**V menších firmách** je méně struktury, méně regulace, méně procesů, máš v nich větší vliv na celkové prostředí. Věci se tak dělají snadněji a možná i rozhodují snadněji. Stejně tak má ale tvůj šéf větší moc a tvůj kariérní růst bude probíhat čistě neformálně, na základě pocitů a vyjednávání. Častěji se také setkáš s [kulturou zatuchlého českého rybníčku](#firemni-kultura).

{% call blockquote_avatar(
  'Proces je kolektivní dohoda, jak se něco bude dělat. Rozdíl mezi zlým procesem a pozitivní dohodou je jen v tom, jak moc je můžeš ovlivnit.',
  'lukas-linhart.jpg',
  'Lukáš Linhart'
) %}
  Lukáš Linhart, technický ředitel v [Apiary](https://byznys.ihned.cz/c1-65593630-oracle-kupuje-za-miliardy-korun-cesky-start-up-apiary-zakladatele-ve-firme-zustavaji) a poté v Oracle
{% endcall %}

Nenech se ale **příliš unést zobecněními**, které jsou v této kapitole. Rozdíly mezi konkrétními firmami (např. [Red Hat](https://www.redhat.com/en/jobs) versus [Oracle](https://www.oracle.com/corporate/careers/)), nebo i mezi konkrétními interními týmy v rámci téže korporace, mohou být větší, než výše popsané obecné rozdíly mezi korporacemi a malými firmami. Vždy si [zjisti](#informace-o-firme), jaké podmínky jsou v právě v tom týmu, do jakého se chystáš nastoupit.

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
*   Bydlíš mimo velká města, kde se stálé zaměstnání v IT hledá obtížně? [Praha](/jobs/region/praha/) nebo [Brno](/jobs/region/brno/) nabízí jiné příležitosti než Šluknovsko či Jesenicko.
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

O nástrahách práce „na IČO“ je tady [celá další kapitola](#prace-na-ico). Pokud tě láká „freelancing“, rozhodně si ji přečti, ale navíc si projdi i následující tipy:

*   Než do toho půjdeš naplno, můžeš si „něco jako práci na volné noze“ **nejdříve vyzkoušet**, a to v podobě tzv. [příležitostné činnosti](https://www.jakpodnikat.cz/prilezitostna-cinnost.php).
*   Firmy [outsourcují](https://cs.wikipedia.org/wiki/Outsourcing) spoustu úkolů, ale **nebudou je chtít svěřit amatérovi**. Ujasni si, jaké jsou tvé přednosti a jak hodláš klientům kompenzovat své nedostatky (např. nízkou cenou). Vytvoř si [portfolio](#osobni-web-a-blog), kde to firmám „vysvětlíš“. Začni s jednoduchými, jasně zadanými a ohraničenými úkoly, které zvládneš vypracovat. Nesnaž se dělat všechno (např. weby, nebo i frontend jsou příliš široká zaměření). Vyber si směr, kterým se chceš vydat a na který se budeš specializovat (např. [kódování newsletterů](https://www.google.cz/search?q=k%C3%B3dov%C3%A1n%C3%AD%20newsletter%C5%AF)). Začni malými krůčky, propracovávej se k větším úkolům a s nimi i k sebedůvěře, která ti pomůže odhadnout, do čeho se zvládneš pustit a kolik si za to máš říct.
*   **Poptávky nepřijdou samy.** Je velká pravděpodobnost, že nikdo zatím ani neví, že vůbec existuješ a něco nabízíš. Zkus si na internetu najít vhodné firmy a napsat jim e-mail s nabídkou svých služeb, účastni se [srazů nezávislých profesionálů](https://www.facebook.com/navolnenoze/events/), procházej různá internetová tržiště s poptávkami. V Česku má jistou tradici fórum [Webtrh](https://webtrh.cz/), ale existuje toho spousta (abecedně): [fiverr.com](https://fiverr.com/), [freelance.cz](https://freelance.cz), [freelancer.com](https://freelancer.com), [guru.com](https://guru.com), [navolnenoze.cz](https://navolnenoze.cz), [peopleperhour.com](https://peopleperhour.com), [topcoder.com](https://topcoder.com), [toptal.com](https://toptal.com), [upwork.com](https://upwork.com)… Připrav se na to, že musíš každý měsíc platit zálohy na pojištění (minimálně kolem 5 000 Kč měsíčně), ať už něco vyděláš, nebo ne.
*   **Žádný senior nebude mít v popisu práce se ti věnovat a rozvíjet tě**, pokud budeš vůbec dělat v týmu. Intenzivní samostudium a vypracovávání zakázek budou zřejmě jedinými způsoby, jakými se budeš učit. Pokud na to vyděláš, můžeš si [platit mentora](practice.md#najdi-si-mentora). Počítej s tím, že ze začátku budeš moci klientovi účtovat jen zlomek hodin, než kolik jich reálně nad úkolem strávíš. Neboj se ale s nabytými zkušenostmi tento poměr vylepšovat. Chybějící tým kompenzuj v [coworkingu](https://navolnenoze.cz/blog/coworkingy/), účastí v profesní komunitě, na [srazech](practice.md#najdi-inspiraci-poznej-lidi) nebo [online](learn.md#kde-najdes-pomoc).

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

Jak bylo už zmíněno, [nečekej příliš dlouho](#kdy-zacit-hledat). Zkoušej to, i když si myslíš, že na to nemáš. Uč se v průběhu na základě toho, co zjistíš na [pohovorech](#pohovor). Speciálně pokud jsi žena, buď až „drzá“. **Muži jdou na pohovor i pokud mají pocit, že mají polovinu znalostí. Žena se často neodváží, dokud nevěří, že má 120 % požadovaného**. Tento problém se nazývá _[confidence gap](https://www.theatlantic.com/magazine/archive/2014/05/the-confidence-gap/359815/)_, ale [kořeny má nejspíš hlouběji než jen v malém sebevědomí](https://www.theatlantic.com/family/archive/2018/09/women-workplace-confidence-gap/570772/).

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
    'Slavná kniha plná <a href="#leetcode">úloh, které můžeš dostat na pohovoru</a>.'
  ) }}
</div>

### Tvoje požadavky    <span id="priorities"></span>

Pokud hledáš ve velkém městě, kde je nabídek více, připrav si **seznam konkrétních věcí, které jsou pro tebe důležité**. Ten si u každé nabídky odškrtávej. Může to být třeba že chceš:

*   na programátorskou pozici ([ne testování](#zacinani-na-jine-technicke-pozici)),
*   pružnou pracovní dobu,
*   [příjemný kolektiv](#firemni-kultura),
*   stabilitu, nebo naopak [startup](#prace-pro-startup) plný rychlých změn,
*   prostředí, kde nebude problém se učit nebo [zajet na konferenci](practice.md#najdi-inspiraci-poznej-lidi),
*   rovnováhu mezi prací a volným časem,
*   malou dojezdovou dobu do kanceláře,
*   [mzdu větší než určitou částku](#kolik-si-vydelam),
*   možnost kariérního postupu…

Cokoliv z toho pro tebe může být zásadní. Je dobré si v tom dopředu udělat pořádek a pak upřednostnit ty nabídky, které to splňují. Nehledej naslepo „něco“. Ze svých požadavků neslevuj, raději obejdi více pohovorů.

Seznam udělej podle sebe. Netrap se tím, co chtějí ostatní — každý je v jiné situaci, každého motivuje něco jiného. Tvoje priority **jsou tvoje a jsou důležité**.

### Životopis    <span id="cv"></span>

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }} Z této kapitoly jsou teď dvě samostatné stránky: [Životopis](cv.md) a [LinkedIn](linkedin.md)
{% endcall %}

### Zkušenosti získané mimo IT    <span id="non-tech-experience"></span>

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }} Z této kapitoly je teď samostatná stránka: [Životopis](cv.md)
{% endcall %}

### Projekty    <span id="projects"></span>

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }} Z této kapitoly jsou teď dvě samostatné stránky: [Životopis](cv.md) a [GitHub](git.md)
{% endcall %}

### Informace o firmě    <span id="research"></span>

Než firmě napíšeš, **něco si o ní zjisti**. Vyhledej si firmu na internetu, zkus pochopit její produkt, [kulturu](#firemni-kultura), apod. Lidé na pohovorech často zjišťují, jestli o firmě něco víš, a kromě toho ti to pomůže i s [vlastními dotazy](#tvoje-otazky). Pokud firma [pořádá nějaké své akce](#firemni-akce), můžeš část svého průzkumu provést i tam.

Zjisti si **zákulisní informace**. Ty nejzajímavější věci z lidí vytáhneš [u piva](#networking), ale i na internetu lze leccos najít. Existují weby jako [Atmoskop](https://www.atmoskop.cz/) nebo [Glassdoor](https://www.glassdoor.com/), kde si můžeš přečíst hodnocení firem napsané bývalými a současnými zaměstnanci. Můžeš narazit na _red flags_, signály, že **firma, do které se snažíš dostat, [není tak úplně v pořádku](#firemni-kultura)**. Nebo ti to může pomoci alespoň připravit si zajímavé [dotazy, které můžeš položit během pohovoru](#tvoje-otazky).

### Zapisuj si úspěchy    <span id="wins"></span>

Jedna z věcí, které chceš ukázat potenciálnímu nebo stávajícímu zaměstnavateli je, že se umíš učit a zlepšovat. A chceš to ostatně ukázat i sobě, pomůže ti to bojovat s nedostatečným sebevědomím („[Impostor syndrom](https://www.google.cz/search?q=impostor+syndrome&lr=lang_cs)“). Jak na to? **Dělej si poznámky o naučených vědomostech.** Vždy, když se k seznamu vrátíš, pomůže ti to **uvědomit si, jak dlouhou cestu máš za sebou** a kolik nových skvělých věcí umíš od posledně.

Veď si seznam svých [projektů](practice.md#najdi-si-projekt) na [osobní stránce](#osobni-web-a-blog), na LinkedIn profilu, nebo na GitHubu. **Možná se budeš za svůj nejstarší kód stydět, ale to je normální. Aspoň jde vidět tvůj posun!** Profesionální programátoři se stále učí nové věci a tak je běžné, že se stydí i za to, co napsali před pár měsíci, natož před lety. Eviduj svoje [přednášky a články](#projev-aktivitu-navic). Pokud o tvé práci někdo napíše něco pochvalného (na sociálních sítích, na LinkedIn, do e-mailu), poznamenej si to a klidně si ulož i [snímek obrazovky](https://cs.wikipedia.org/wiki/Sn%C3%ADmek_obrazovky). Na [osobní stránce](#osobni-web-a-blog) to můžeš využít do seznamu referencí (anglicky _testimonials_).

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
Přímo na junior.guru také najdeš [pracovní portál](/jobs/), ale s nabídkami jen a pouze pro juniory. Jiné zde inzerovat ani nelze. Navíc se každý den spouští robot, který se rozhlíží i po nabídkách z dalších zdrojů. Poté je filtruje na základě přísných pravidel a nechá jen ty, o nichž usoudí, že jsou opravdu pro začátečníky:
{{ jobs_inline(jobs, 3, jobs_url='/jobs/remote/') }}
{% endif %}

### Náboráři    <span id="recruiters"></span>

Existují dva druhy náborářů (anglicky _recruiter_):

*   **Pracují přímo pro konkrétní firmu**, zpravidla velkou, a hledají na trhu lidi jen do ní. Můžeš se s nimi setkat na stáncích firem na [konferencích](practice.md#najdi-inspiraci-poznej-lidi) či pracovních veletrzích. Také jsou to oni, kdo s tebou řeší přijímací pohovor, když se velké firmě ozveš na nabídku práce. Navenek je reprezentují „kariérní portály“.
    Příklady: [Red Hat](https://www.redhat.com/en/jobs), [Oracle](https://www.oracle.com/corporate/careers/)…
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

Občas firmy pořádají přednášky, dny otevřených dveří, školení, [hackathony](practice.md#zkus-hackathon), [srazy](practice.md#najdi-inspiraci-poznej-lidi), aj. **akce přímo na své domácí půdě**. Na nich se dá obhlédnout prostředí, neformálně navázat kontakty, poptat se osobně na [stáž](#staze). Některé firmy dokonce přímo konají kurzy pro začátečníky nebo s nějakými spolupracují, a nabízí práci nejšikovnějším absolventům.

Činnost tohoto typu vypovídá minimálně o tom, že **firma není uzavřená do sebe**, že se snaží být aktivní v širší komunitě programátorů, a že u svých lidí podporuje i aktivity nad rámec sezení za počítačem „od devíti do pěti“.

Tyto akce najdeš na stránkách jednotlivých firem, nebo i na [meetup.com](https://meetup.com): [TopMonks Caffè](https://www.meetup.com/TopMonks-Caffe/), [Y-Soft: Technology Hour](https://www.meetup.com/ysoft-th/), [STRV Meetups](https://www.meetup.com/STRV-Meetups/)…

### Networking

Jedním z nejefektivnějších způsobů, jak si v malé ČR sehnat dobrou práci, je **networking, tedy setkávání s lidmi a získávání kontaktů**. Staň se [aktivním členem programátorské komunity](#projev-aktivitu-navic) a zajímavé nabídky práce po čase přijdou samy. Choď na [srazy a konference](practice.md#najdi-inspiraci-poznej-lidi), seznamuj se s lidmi, představuj se. Jsou to místa, kde lidé zhusta mění a získávají práci — i proto se na nich vyskytují [recruiteři velkých firem](#naborari). Můžeš zkusit i veletrhy práce, které jsou na toto přímo zaměřené (např. [JobsDev](http://www.jobsdev.cz/)). **Velké akce lze pojmout systematicky** — vytiskni si 50 vizitek s nápisem „sháním stáž“ a jdi je rozdat mezi lidi. Představuj se, vysvětli co umíš a co hledáš, prodej se. **Malé akce jako srazy ber jako způsob jak najít nové kamarády** v oboru a pracovním příležitostem tam nech spíš volný průběh.

Networking je také způsob, jak od lidí dostat doporučení. Někteří lidé jsou schopní tě ve své firmě doporučit i po pěti minutách rozhovoru, ať už protože mají dobré srdce, protože na ně zapůsobíš, nebo protože chtějí dostat _referral bonus_ (odměna za doporučení nového zaměstnance, kterou některé firmy nabízejí).

Česká komunita programátorů je malá a existuje na malém prostoru — z Plzně do Ostravy je to pár hodin vlakem. **„Všichni se znají“, je snadné se setkávat**. Díky tomu je u nás networking velmi důležitou složkou budování kariéry.


## Pohovor    <span id="interview"></span>

### Otázky na tebe    <span id="questions"></span>

Na pohovoru ti budou pokládat otázky a také se očekává, že [nějaké otázky budeš mít ty](#tvoje-otazky). Začněme těmi, které můžeš dostat:

*   **Behaviorální otázky.** „Kdo tě nejvíce ovlivnil ve tvé kariéře?“ [Další příklady](https://www.pathrise.com/guides/45-behavioral-interview-questions/).
*   **Technické otázky.** „Představ si, že nic nevím o [Reactu](https://reactjs.org/). Vysvětli mi, co to je.“ Nebo: „Co je [float](https://developer.mozilla.org/en-US/docs/Web/CSS/float) v CSS?“
*   **[Úlohy u tabule](#ulohy-na-algoritmizaci)**, programování na místě, hádanky. Viz např. [HackerRank](https://www.hackerrank.com/).
*   **Úkoly na doma.** Úkol zpracováváš mimo pohovor a máš na něj kolik času potřebuješ.
*   **Párové programování.** Spolu s někým z firmy řešíte zadaný problém.

Na otázky se můžeš **připravit**. Podle toho, na jakou pozici se hlásíš, můžeš na internetu najít seznamy typických otázek. Hledej třeba „[interview questions python](https://www.google.cz/search?q=interview%20questions%20python)“. Nebo „[behavioral interview questions](https://www.google.cz/search?q=behavioral%20interview%20questions)“.

Ber si všude s sebou notes na poznámky a **zapisuj si všechno, co nevíš. Doma se na to po každém pohovoru podívej.** Nemusíš se hned učit všechno, co kde kdo zmínil, ale zjisti si aspoň, co ty věci jsou, na co se používají, pro jaké profese je nutnost s nimi umět. **Uč se z pohovorů.**

<small>Rady v této podkapitole volně vychází ze [série tipů, které tweetovala Ali Spittel](https://twitter.com/ASpittel/status/1214979863683174400) a z osobních doporučení od Olgy Fomichevy. Velké díky!</small>

### Když nevíš    <span id="when-you-dont-know"></span>

Během pohovoru **ukaž, jak přemýšlíš**. Vysvětli, jakým způsobem se propracováváš k odpovědi, kresli diagramy, piš kód, vysvětluj díry ve svém přístupu. Ptej se, pokud ti něco není jasné. Situace, kdy mlčíš a přemýšlíš, není příjemná ani tobě, ani ostatním přítomným. Vždy je lepší „přemýšlet nahlas“, ale také prostě říct „nevím“, ideálně spolu s „můžete mi to trochu popsat, ať se mám od čeho odrazit?“.

Pokud neznáš [Django](https://www.djangoproject.com/), **odpověz upřímně!** Nelži a nesnaž se nic zamaskovat, pro tazatele bude snadné tě prokouknout. Člověka, který mlží, mít nikdo v týmu nechce. Raději řekni „Nevím, ale chci se to naučit“. Nebo: „Mám jeden projekt ve [Flasku](https://flask.palletsprojects.com/), což je taky webový framework v Pythonu, tak snad by nebylo těžké do toho proniknout“. Pokud nevíš vůbec, klidně se na správné řešení na místě zeptej. **Ukaž, že se nebojíš ptát když nevíš, a že máš chuť se posouvat.**

{% call blockquote(
  'Říkej pravdu a dostaneš se tam, kam chceš.'
) %}
  Olga Fomicheva, organizátorka a absolventka začátečnického kurzu [PyLadies](https://pyladies.cz)
{% endcall %}

### Úlohy na algoritmizaci    <span id="leetcode"></span>

Na pohovorech se můžeš až příliš často setkat s úlohami u tabule, _challenges_, _puzzles_, otázkami na algoritmizaci, na [složitost](https://cs.wikipedia.org/wiki/Asymptotick%C3%A1_slo%C5%BEitost), na řazení, procházení stromů a podobné nesmysly. **Přitom v drtivé většině případů nikdo nic takového ve své práci běžně nepotřebuje.** Většina programátorů stejně jako ty použije na řazení vestavěnou funkci [sort()](https://docs.python.org/3/howto/sorting.html) — a je to. I ti, kteří se vše podrobně dřív učili na VŠ a skládali z toho zkoušky, většinu z toho dávno zapomněli — protože to nepoužívají. Nanejvýš s tím machrují na společném obědě.

**Bohužel pro tebe je ale testování takovýchto znalostí na pohovorech stále velmi populární.** Stejně jako někdo vyučuje dějepis tak, že nutí děti nazpaměť si pamatovat každé datum, v IT zase lidé nesmyslně lpí na tom, aby každý znal princip [Quicksortu](https://en.wikipedia.org/wiki/Quicksort). Přijmi to jako smutný fakt a připrav se. Ono se ti to samozřejmě neztratí, **nejsou to zbytečnosti**. Je dobré znát kontext, vědět jak věci fungují, umět psát efektivnější programy. Jen by bylo lepší to mít možnost objevovat postupně, až když to budeš potřebovat, a ne se to muset učit nazpaměť kvůli pohovorům.

Holt, nedá se nic dělat. Zhluboka se nadechni a hurá do toho:

1.  **Projdi si základy** algoritmizace a práce s datovými strukturami. Začni třeba s [BaseCS](practice.md#zaklady). Algoritmy se nejlépe vysvětlují na videu, takže je [hledej na YouTube](https://www.youtube.com/results?search_query=quicksort).
2.  **Řeš úlohy** na [webech jako Codewars nebo HackerRank](practice.md#procvicuj). Procvičíš si algoritmizaci a datové struktury na reálných problémech. Projdi si [příručky](#souvisejici-prirucky) zabývající se řešením úloh z pohovorů.
3.  **Dělej si poznámky**. Díky nim se budeš moci k nabytým vědomostem snadno vracet a budeš je mít v podobě, která ti nejvíc vyhovuje. Psaní navíc upevňuje paměť. Mrkni třeba na [poznámky Ali Spittel](https://github.com/aspittel/coding-cheat-sheets), které si původně psala rukou na papír.

{% call blockquote_avatar(
  'Dělala jsem jednu úlohu každé ráno po probuzení, abych si rozehřála mozek.',
  'ali-spittel.jpg',
  'Ali Spittel'
) %}
  Ali Spittel, [We Learn Code](https://welearncode.com/) & [Ladybug Podcast](https://www.ladybug.dev/)
{% endcall %}

<small>Rady v této podkapitole volně vychází ze [série tipů, které tweetovala Ali Spittel](https://twitter.com/ASpittel/status/1214979863683174400). Velké díky!</small>

### Povědomí o firmě    <span id="company-info"></span>

Kandidát, který se někam hlásí a ani neví, o co se firma na trhu snaží, nepůsobí moc profesionálně. Je důležité mít **základní povědomí o firmě a tom, co dělá**. To získáš díky [průzkumu před pohovorem](#informace-o-firme). Dále můžeš dostat zvědavé dotazy typu „Jak jste nás našla?“, ale na ty většinou není těžké odpovědět po pravdě.

Co je horší, jsou **otázky jako „Proč zrovna my?“**, které, pokud se zrovna nehlásíš do práce svých snů, nelze snadno vyhrát. Obcházíš nejspíš desítky pohovorů a není možné toužit pracovat pro každou z firem, které navštívíš. Lidem na pohovoru ovšem nemusí stačit pragmatická odpověď, že „člověk potřebuje něco jíst a z inzerátu se zdálo, že by mohli za dobře odvedenou práci posílat na účet peníze“. Když už se tak hloupě ptají, nezbývá než v tomto případě skutečnost trochu přibarvit a firmě zalichotit, ať si nepřipadá, že je jen jednou z položek na tvém seznamu — i kdyby opravdu byla.

### Tvoje otázky    <span id="reverse-interview"></span>

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

Celkově je dobré se soustředit nejen na firmu, ale i **na sebe**. Jsi juniorní, ale na pohovoru dostáváš rozpačité odpovědi na to, jestli se ti někdo bude věnovat? Vidíš už na pohovoru přebujelá ega, machrování, manipulativní otázky? Nejednají s tebou s respektem? Zaznamenáváš sexistické narážky? Působí firma neorganizovaně? Musíš projít přes desetikolový pohovor se spoustou úloh před tabulí? Až nastoupíš, nebude to lepší! Všechno toto jsou tzv. _red flags_, signály, že **firma, do které se snažíš dostat, [není tak úplně v pořádku](#firemni-kultura)** a nejspíš nestojí za to s ní ztrácet čas. Pohovor funguje na obě strany — testuješ si i ty firmu, nejen ona tebe.

{% call blockquote_avatar(
  'Mysli i na sebe. Pokud při pohovoru musíš přeskočit milion překážek, možná je to signál, že tak bude vypadat i ta práce.',
  'ali-spittel.jpg',
  'Ali Spittel'
) %}
  Ali Spittel, [We Learn Code](https://welearncode.com/) & [Ladybug Podcast](https://www.ladybug.dev/)
{% endcall %}

### Vyjednávání    <span id="negotiation"></span>

Vyjednávat jde o všem. O nabídkách, [stážích](#staze), počtu pracovních hodin, typu úvazku, možnosti pracovat z domů, povinnostech v práci, benefitech, [mzdě](#kolik-si-vydelam). **Nic není dáno pevně a hodně firem je ochotno se domluvit alespoň na kompromisu**, pokud o tebe budou mít vážný zájem. Zaměstnavatel by ti měl chtít jít svou nabídkou naproti, protože **čím víc ti budou pracovní podmínky vyhovovat, tím déle zůstaneš** a investice firmy do tvého rozvoje nepřijde za rok vniveč. Vyjednávací pozici ti mohou vylepšit [tvoje úspěchy a reference](#zapisuj-si-uspechy), zajímavé předchozí zkušenosti, jakékoliv [aktivity navíc](#projev-aktivitu-navic) nebo lepší nabídka v jiné firmě:

*   Poděkuj za nabídku s tím, že se ti líbí
*   Řekni, které věci by se ti hodilo dohodnout jinak
*   Zmiň [úspěchy a zkušenosti](#zapisuj-si-uspechy), které podporují tvoje požadavky, nebo konkurenční nabídku
*   Navaž na to tím, jak se těšíš, s čím vším budeš moci firmě pomoci v budoucnu

Drž se [seznamu svých priorit](#tvoje-pozadavky) a **nenech se natlačit do něčeho, co nechceš**. Nespokoj se s nižší mzdou, než za jakou by ti bylo příjemné pracovat. **I když začínáš, zasloužíš si adekvátní ohodnocení.** Pokud se firmě líbíš, bude ochotná vyjednávat o mzdě. Jestliže budeš mít příliš nízká očekávání z hlediska mzdy, může to na zaměstnavatele působit zoufale nebo jako znamení velmi nízkého sebevědomí.

### Práce „na IČO“    <span id="contracting"></span>

Při vyjednávání s firmou může padnout návrh, že budeš pracovat „na IČO“. Některé firmy to po tobě mohou i přímo vyžadovat jako jediný způsob, jakým jsou ochotné tě „zaměstnat“. Myslí se tím, že se místo zaměstnaneckého poměru staneš [OSVČ](https://cs.wikipedia.org/wiki/Osoba_samostatn%C4%9B_v%C3%BDd%C4%9Ble%C4%8Dn%C4%9B_%C4%8Dinn%C3%A1) a budeš pro firmu pracovat jako [kontraktor](#prace-na-volne-noze).

Přestože jde o balancování na hraně zákona o [švarc systému](https://cs.wikipedia.org/wiki/%C5%A0varc_syst%C3%A9m), v českém IT takto pracuje hodně lidí. [Analýza evropského technologického trhu z roku 2019](https://2019.stateofeuropeantech.com/chapter/people/article/strong-talent-base/#chart-372-1627) obsahuje graf, kde ČR, Ukrajina a Polsko jednoznačně vedou v počtu IT odborníků na volné noze. Asi ale tušíme, že důvodem je spíše šedá ekonomika než úžasné podmínky pro [nezávislé profesionály](#prace-na-volne-noze). Proč je práce „na IČO“ v IT tak oblíbená?

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
*   I ti nejlepší mohou být mezi prvními, které firmy „propustí“, když je problém. Ať už jde o krach [startupu](#prace-pro-startup) nebo začátek pandemie, když jde do tuhého, firmy neváhají rozloučit se velmi rychle i s celými týmy kontraktorů.

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

Jak už bylo zmíněno výše, **vždy si dobře zvaž, zda se ti nabídka opravdu vyplatí**. Pokud se s firmou nedomluvíš na dostatečně vysoké sazbě, která by vše pokryla, nebo pokud „na IČO“ vůbec jít nechceš, je pro tebe lepší odmítnout a hledat dál. I pokud se ti z dvaceti firem ozvala jedna, nesmíš podlehnout pocitu, že to musíš vzít. Stejně jako u [mizerné firemní kultury](#firemni-kultura), nestojí to za to.

### Jak zvládnout odmítnutí    <span id="handling-rejection"></span>

Je velmi pravděpodobné, že tě odmítnou na pohovoru, a to **proto, že se to děje úplně každému**. [Ano, i seniorním programátorům](https://sw-samuraj.cz/2017/09/smutna-zprava-o-stavu-it-trhu/). U začátečníků navíc chvíli trvá, než se naladí na aktuální poptávku trhu a na to, jak přesně fungují přijímací pohovory v IT. Raději **počítej s tím, že ze začátku to půjde ztuha** a tvé první hledání práce [bude zahrnovat i desítky pohovorů a může trvat měsíce](#jaka-mit-ocekavani).

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

Řekni si o **zpětnou vazbu po pohovoru**. Může to být dobrý zdroj poznatků (nebo ujištění, že ta firma není nic pro tebe). Někdy ti bohužel žádnou zpětnou vazbu nedají, ale to nemusí být vyloženě chyba těch, kteří s tebou vedli pohovor. **Mnoho velkých mezinárodních firem má doporučení od právníků, že zpětnou vazbu nemá vůbec poskytovat.** Existuje pro ně totiž riziko, že by ji kandidát mohl zneužít k žalobě kvůli diskriminaci. Pošlou ti nějakou obecnou větu, např. „hledáme někoho zkušenějšího“. Nepropadej depresi, že zbytečně investuješ hodiny do učení a práci nenajdeš. Za touto větou se ve skutečnosti může skrývat naprosto cokoliv. Můžeš je vzít za slovo a zkusit se [zeptat na stáž](#staze).

Počítej i s tím, že **mnoho firem ti na tvůj zájem o práci vůbec neodpoví**. Ať už mají příliš mnoho kandidátů a odpovídat každému by bylo náročné, nebo jsou prostě nedbalí ve svém přijímacím procesu, výsledek je stejný — můžeš čekat týdny a nic z toho nebude. **Odpovídej na několik nabídek zároveň!** Může se ti stát, že budeš mít na výběr, a díky tomu i méně stresu a lepší [vyjednávací pozici](#vyjednavani).


## Firemní kultura    <span id="culture"></span>

Programátor génius, který sám na všechno přijde, ale nevychází dobře s lidmi, je dnes minulostí. Pro takové lidi se vžilo označení _brilliant jerk_ a [internet je plný článků o tom, proč se jich mají firmy vyvarovat](https://www.google.cz/search?q=brilliant%20jerk). Programování je už dlouho **týmová práce v níž je ego na překážku** a kde je schopnost **komunikace s lidmi stejně důležitá jako technické vědomosti**.

Pokud jsou v týmu lidé s toxickým přístupem, silně to ovlivní každý jeden den, který v práci strávíš. **Pozoruj už při pohovoru, jakému chování dává firma volný průchod. Jaká je v ní kultura? Kdo budou tví kolegové?** Všímej si, jestli má firma smíšený kolektiv, nebo je to [monokultura dvacetiletých geeků](https://honzajavorek.cz/blog/mlady-kolektiv/), a přemýšlej, co by ti vyhovovalo víc. Některé firmy mají tzv. _lunch round_, což je **neformální kolo pohovoru, kdy můžeš jít se svými budoucími kolegy na oběd** a zjistit tak, jestli si s nimi sedneš (totéž se samozřejmě snaží zjistit i oni). O kulturách konkrétních firem se lze také dovědět na [Cocuma](https://www.cocuma.cz/) a [Welcome to the Jungle](https://www.welcometothejungle.com/).

Kdo bude tvůj šéf? Hledej manažera, pro kterého jsou důležité tvoje zájmy a cíle, který vytvoří prostředí, kde se ti bude dařit. **Dobrý manažer se snaží o tvůj úspěch.**.

Jedna z nejdůležitějších věcí, které potřebuješ jako junior vědět o svém týmu: **Bude se ti někdo ve firmě soustavně věnovat? Budeš mít komu pokládat dotazy bez toho, aby z tebe dělal blbce?** Zeptej se na to! A ptej se na všechno, co se ti nezdá. Projdi si pečlivě rady, které jsou v [kapitole o tvých otázkách na pohovoru](#tvoje-otazky).

Pokud cítíš, že ti firemní kultura něčím nesedne, **vždy je lepší zkusit hledat jinde než zůstat**. Kulturu firmy prakticky není možné opravit zevnitř. I pokud už zrovna dostaneš svou první práci v IT, je lepší odejít. Je jasné, že není snadné se vzdát těžce nabyté příležitosti a vrátit se do onoho náročného obcházení pohovorů, ale **žádná práce nestojí za dlouhodobý stres a narušené duševní zdraví**. Neboj, za ukončení práce ve zkušebce tě nikdo hodnotit nebude, od toho zkušebka je!

<div class="link-cards">
  {{ link_card(
    'WinWinJob',
    'https://www.winwinjob.cz/',
    'Vyber si práci podle šéfa.'
  ) }}

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

Vlastní osobní webová stránka (_portfolio_) ti dává prostor **vyniknout mezi ostatními kandidáty**. Je to [projekt](practice.md#najdi-si-projekt), na kterém si prakticky vyzkoušíš různé technologie a který klidně můžeš ukázat při pohovoru jako důkaz, že něco umíš. Mimo to můžeš na své webovce dát průchod vlastní osobnosti a kreativitě.

Stránka nemusí být komplikovaná, stačí aby to byl **rozcestník**. Dvě věty o sobě, popis zkušeností, odkazy na profily (LinkedIn, GitHub…) a případně na tvé [projekty](practice.md#najdi-si-projekt). Pokud tě baví psaní, časem můžeš přidat **blog**. Můžeš psát o své cestě do IT (a tak se [objevit na těchto stránkách](motivation.md#vsechny-motivacni-pribehy)) nebo přidat článek vždy, když se naučíš něco nového — čímž pomůžeš dalším začátečníkům a zároveň tím vystoupíš z davu. Začneš si v oboru budovat své jméno a to ti může pomoci nejen u pohovorů, ale i pokud budeš chtít [přednášet na konferencích](#projev-aktivitu-navic).

{% call blockquote_avatar(
  'Tweetuju nebo píšu články o všem, co se naučím. Mohu se k tomu vždy vrátit a zároveň s učením pomáhám ostatním. Díky psaní článků navíc věcem porozumím do hloubky a umím je vysvětlit.',
  'vladimir-gorej.jpg',
  'Vladimír Gorej'
) %}
  Vladimír Gorej, profesionální programátor, o svém [Twitteru](https://twitter.com/vladimirgorej/) a [blogu](https://vladimirgorej.com/)
{% endcall %}

Příklady osobních stránek s blogem: [Honza Javorek](https://honzajavorek.cz/) (autor této příručky) nebo [Iveta Česalová](https://ivet1987.wz.cz/) (absolventka PyLadies). Další inspiraci lze [snadno najít na internetu](https://www.google.cz/search?q=best%20(personal%20or%20portfolio)%20websites).

### Učení    <span id="teaching"></span>

I když se to nezdá, i začátečníci mohou učit! **Nejlepší způsob, jak se něco pořádně naučit, je vysvětlit to někomu jinému.** Učení upevňuje hloubku tvých vlastních znalostí a umožňuje ti setkat se s lidmi z oboru. Můžeš [napsat článek na blog pokaždé, když se naučíš něco nového](#osobni-web-a-blog), můžeš [nabízet mentoring](practice.md#najdi-si-mentora), můžeš pomáhat na komunitně organizovaných kurzech a workshopech jako jsou ty od [PyLadies](https://pyladies.cz/) nebo [Czechitas](https://www.czechitas.cz/).

Na PyLadies kurzech **můžeš „koučovat“ i bez velkých znalostí programování**, stačí se [přihlásit](https://pyladies.cz/stan_se/). Je to doplňková role bez velké zodpovědnosti, se kterou můžeš kdykoliv přestat. Pro lepší představu si přečti [článek od koučky Ivety](https://ivet1987.wz.cz/2020/03/koucovani-na-pyladies-kurzech/). Další podobná role, kterou jde dokonce dělat na dálku z pohodlí domova, je [opravování úkolů](https://pyladies.cz/stan_se/).

{% call blockquote_avatar(
  'Na začátku to byly hrozné pocity. Někdo si mě zavolá k problému, se kterým nedokážu pomoci, budu za trubku. Nakonec to ale byly obyčejné, jednoduché problémy, se kterými jsem poradila.',
  'iveta-cesalova.jpg',
  'Iveta Česalová'
) %}
  Iveta Česalová, autorka [článku o koučování na PyLadies](https://ivet1987.wz.cz/2020/03/koucovani-na-pyladies-kurzech/)
{% endcall %}


### Přednášení    <span id="giving-talks"></span>

Podobně jako učení, přednášení na [srazech a konferencích](practice.md#najdi-inspiraci-poznej-lidi) vypadá jako něco, co je vyhrazeno profesionálům, ale není to tak. **Zmíněné akce jsou komunitní a obvykle podporují přednášky od začátečníků a pro začátečníky.** Neboj se toho! Přijít na pohovor s tím, že máš za sebou přednášku na srazu nebo dokonce konferenci, je naprostá pecka! Pro inspiraci si projdi nějaké přednášky z minulých let konference [PyCon CZ](https://cz.pycon.org/). Nejsou to nutně pokročilá technická témata:

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

V neposlední řadě si lze vybudovat jméno [přispíváním do open source](practice.md#zkus-open-source). I pokud se necítíš na samotné programování, [je i hodně jiných způsobů, jak můžeš přiložit ruku k dílu](https://opensource.guide/how-to-contribute/#what-it-means-to-contribute). Je to skvělá příležitost jak nabrat zkušenosti, vyniknout, získat kontakty mezi lidmi z oboru.


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

**P.S.** Nezapomeň, že jsi na „živé stránce“, na které stále probíhají úpravy. Kdykoliv tady může přibýt něco nového, takže není od věci se sem občas vrátit. Všechny změny [najdeš na GitHubu](https://github.com/honzajavorek/junior.guru/commits/main/juniorguru/mkdocs/docs/handbook/), o těch důležitých se můžeš dovědět na sociálních sítích junior.guru nebo prostřednictvím [klubu](../club.md).

A věci mohou přibývat i díky tobě! Pokud máš připomínku, vlastní zkušenost, nebo nápad na novou kapitolu, napiš na {{ 'honza@junior.guru'|email_link }}. Jestli se ti díky junior.guru povede sehnat práci, ozvi se! Můžeš [motivovat ostatní svým příběhem](motivation.md#vsechny-motivacni-pribehy), nebo tím prostě jen udělat [Honzovi](#honza) radost.
