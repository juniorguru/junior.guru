---
title: Jak na životopis pro juniory v IT
emoji: 📝
stages: [preparing]
description: Co dát do životopisu, když nemáš praxi? Když jsi student? Jak můžeš i jako junior bez praxe připravit CV, které tě dostane na pohovor v IT?
template: main_handbook.html
---

{% from 'macros.html' import lead, figure, note, blockquote_avatar, video_card, podcast_card, club_teaser with context %}

# Životopis

{% call lead() %}
  Co dát do životopisu, když jsi junior v IT a nemáš ještě praxi? Tady máš návod na přehledné a úderné CV, ze kterého budou mít recruiteři radost.
{% endcall %}

[TOC]

## Začni s naší přednáškou a šablonou

Návod na dobré CV si můžeš buď přečíst v následujících odstavcích, nebo si jej pustit v podobě **výživné přednášky** od Dana Srba, který má skvělé předpoklady pro to, aby mohl s životopisy radit:

- Dříve nabíral vývojáře, dnes provází juniory změnou kariéry do IT. Viděl už fakt spoustu životopisů a svá doporučení šije na míru přesně pro lidi, jako jsi ty.
- Pracoval v designu a UX, takže ví, jak věci navrhovat tak, aby se druhé straně příjemně používaly.
- Rozumí DTP, tedy sazbě textových dokumentů.

V přednášce ukazuje, jak vytvořit **efektivní životopis pro hledání první práce v IT**. Pokrývá i témata, která tento textový návod příliš nezmiňuje, jako samotnou sazbu textu a vzhled, barvy, apod.

Taky v přednášce představuje svou **[šablonu na CV](https://coreskill.tech/sablona-cv), která je vymazlená přesně pro potřeby juniorů** a následuje veškeré rady, které jsou tady v příručce. Nevymýšlej kolo!

{% set event = events|selectattr("id", "equalto", 45)|first %}
{{ video_card(
  event.get_full_title(),
  '3,5h',
  event.public_recording_url,
  thumbnail_url="static/" + event.plain_poster_path,
  note='Záznamy [klubových přednášek](../events.md) bývají dostupné jen pro členy, ale tato byla v rámci [Týdne pro Digitální Česko](https://budoucnostjedigitalni.gov.cz/) veřejně, aby pomáhala všem.'
) }}

## Chceš přehlednost, ne krásu

Životopis většiny lidí spadá do jednoho ze dvou extrémů. Buď vyplní [nejobyčejnější šablonu z internetu](https://europass.cz/), nebo se snaží zaujmout růžovými puntíky, kudrlinkami a zlatými kolibříky.

Tím prvním jistě nic nepokazíš, ale jde to udělat lépe. To však nutně neznamená originálně. Některá CV jsou **natolik „kreativní“, že brání recruiterům v práci**. Životopis s kudrlinkami sice v paměti uvízne, ale pouze proto, že písmo bylo špatně čitelné a čtvrt hodiny trvalo zjistit, kdo vlastně jsi a co chceš.

{% call figure('static/figures/daniel-nekonecny.jpg', 470, 296, 'Daniel Nekonečný') %}
  Daniel Nekonečný by tvé CV možná pochválil, recruiter si zaťuká na čelo a vyhodí ho
{% endcall %}

**Nepotřebuješ se odlišit za každou cenu.** Firmy v americkém Silicon Valley mají denně stovky kandidátů. U nás tak velká konkurence začátečníků není, na pozice se hlásí jednotky nebo desítky lidí.

Pokud se nehlásíš na pozici v grafice, designu, nebo UX, tak se neočekává ani to, že budeš mít všechno typograficky vyladěné a správně použiješ pomlčky místo spojovníků. Recruitery, programátory a manažery, kteří to budou číst, **neoslníš barvami a fonty**.

Zásadní je, aby o tobě mohli mít **jasnou představu do pár sekund**. Přehledné CV je dostačující a mnohdy bude i odlišující, protože většina lidí takové vyrobit neumí. Kreativitu a originalitu tedy směřuj raději do svých [projektů](#6-projekty) a na CV si spíš pohlídej základní věci.

## Jak nad tím přemýšlet

Životopis je **reklamní letáček**, kterým se snažíš prodat své zkušenosti. Není to vyčerpávající seznam dokumentující poctivě vše, co máš za sebou. Vypíchni to důležité. Nepodstatné vůbec nepiš.

I bez komerční praxe **máš co nabídnout**. Firma může využít tvé nadšení, energii, vlohy, zájmy. Nemáš existující návyky, takže tě mohou učit věci podle svých představ. Nejsi vyhořelý seniorní programátor, který místo chození do kanceláře touží sázet stromky v lese jako pěstební dělník. Stačí se umět dobře prodat!

Pozor, životopis není „sebechvála“, za kterou se máš stydět. V Česku je hluboce zakořeněná **kultura falešné skromnosti**, která brzdí spoustu šikovných lidí. I největší profíci tady mají problém napsat o sobě půl věty. Mnoho lidí trpí [syndromem podvodníka](https://www.heroine.cz/zeny-it/6341-syndrom-podvodnice-vas-pri-praci-v-it-snadno-dozene-jak-proti-nemu-bojovat), úspěchy si nedokážou přiznat.

Pokud chceš v Česku nebo na Slovensku vystoupit z davu, nehledej okrasný font, ale **nauč se zdravě bavit o sobě**. Když dokážeš popsat svůj potenciál, úspěch, přínos, nebo pokud máš dokonce čísla, která můžeš do svého tvrzení dát, je to pecka.

{% call note() %}
  {{ 'lightbulb'|icon }} V [klubu](../club.md) probíráme sebevědomí a sebelásku celkem často. Dáváme si zpětnou vazbu a podporujeme se.
{% endcall %}

## Posílej „papír“

Usnadni život tomu, kdo bude tvé CV zpracovávat, typicky spolu s životopisy dalších deseti kandidátů. Ve většině firem si recruiteři **organizují údaje o kandidátech** v softwaru, kterému se říká ATS (_application tracking system_). Tam potřebují tvé CV nahrát, někdy i strojově analyzovat. Občas si zase životopisy tisknou na papír.

Posílej tedy **dokument, který bude fungovat i na papíře**. JPG obrázek? Není to dokument, nelze ani označit text. Zelené písmo na černém pozadí? Vypadá velmi „hackersky“ a jistě zaujme. Minimálně tím, že když projde tiskárnou, firma bude muset pořídit nový toner.

Ideálně CV **posílej jako PDF** a soubor pojmenuj tak, aby ho člověk na druhé straně po stažení snadno našel: `javorek-cv.pdf` Pokud máš časté příjmení, připoj raději i křestní jméno: `novakova-eva-cv.pdf`

Na **odkazy** ať jde v PDF opravdu klikat a ať jsou podtržené. Jen tak půjde dobře rozpoznat, že jsou to odkazy. A to i na papíře, kde čtenář aspoň uvidí, že tam původně byly a tiskem o ně přišel.

Říká se, že je dobré vejít se na jednu A4. Jako junior se na ni nejspíš vejdeš, ale pokud ne, nelam si s tím hlavu. **Pokud jsou podstatné věci v úvodu, je už celkem jedno, kolik následuje stránek s detaily.** Určitě CV nenatahuj, lepší ať je úderné a na půl strany, než plné zbytečností, jen aby zaplnilo list. Také necpi vše na jednu stránku za cenu nečitelně malého písma.

## Upravuj na míru

Vytvoř si **polotovar svého CV** a vždy, než jej někam pošleš, zkus si u každé jeho části říct, zda by se nedala přeuspořádat, přeformulovat, odebrat, nebo jestli by šlo něco přidat, aby životopis **lépe seděl na poptávanou pozici**.

Například pokud jsi účetní, která se naučila programovat, pro většinu pozic to nebude významné, v CV to zmíníš jen letmo. Když ale narazíš na firmu, která vytváří účetní software, může ti to přidat body a klidně se o tom rozepiš.

## Česky i anglicky

Polotovar CV měj v obou jazycích a následuj jednoduché pravidlo: **Na inzeráty v angličtině posílej anglickou verzi, na české českou.** Nebo slovenskou, rozdíl mezi češtinou a slovenštinou samozřejmě nikdo neřeší. Pokud chceš udržovat jen jednu verzi polotovaru, tak měj anglickou, s tou si nějak poradí každý.

**Netrap se nedokonalostí svých formulací**, v IT si všichni vystačí s hovorovou [Euro English](https://cs.wikipedia.org/wiki/Euro_English) a češtinářů mezi programátory moc není.

Nech si ale CV někým aspoň jednou přečíst, ať **odchytáš největší hrubky**. Ruší při čtení a působí amatérsky. Je v pořádku jít v oblíbeném tričku, protože chceš působit autenticky. Nesmí ale mít díry.

{% call note() %}
  {{ 'lightbulb'|icon }} V [klubu](../club.md) ti rádi na CV mrkneme. Víc očí, méně hrubek!
{% endcall %}

## Obsah životopisu

Části CV seřaď **od nejpodstatnějších po méně důležité, od nejnovějších po nejstarší**. Co přesně je důležité, se liší pro různé obory, profese, zkušenosti a dokonce i jednotlivé pozice. Pro juniory, kteří zatím nemají pracovní zkušenosti v oboru, je velmi důležitý **souhrn a projekty**, v druhé řadě pak vzdělání.

{% call podcast_card(podcast_episodes|selectattr('number', 'equalto', 1)|first) %}
  Poslechni si [podcast junior.guru](../podcast.md), kde spolu Pavlína a Jirka mluví o tom, jak vyrobit skvělé juniorní CV. Probírají také nejčastější chyby, které při své prezentaci junioři dělají.
{% endcall %}

Následující kapitoly jsou v pořadí, v jakém by se měly dané části na životopisu vyskytovat.

### 1. Jméno

Začni **celým svým jménem**. Velkým, dobře čitelným, výrazným písmem.

Pokud lidé mívají problém tvé jméno přečíst na první dobrou správně, můžeš drobným písmem doplnit **fonetickou nápovědu**. Nepoužívej [IPA](https://cs.wikipedia.org/wiki/Mezin%C3%A1rodn%C3%AD_fonetick%C3%A1_abeceda), běžný smrtelník ji nezná.

Autor jazyka Python, Nizozemec Guido van Rossum, má na [svých stránkách](https://gvanrossum.github.io/) celý odstavec o čtení svého jména a dokonce i nahrávku, tobě bude stačit napsat to **foneticky v jazyce životopisu**. Anglicky třeba \[sharka kash-par-kova\]. Česky například \[viglaš\], pokud se jmenuješ Wiglasz.

### 2. Pozice

Jako podtitulek můžeš dát **název pozice, kterou chceš vykonávat**. Například „junior frontend developer“. Díky tomu si tě druhá strana může okamžitě snadno zařadit.

Pokud už někde pracuješ, pozice na tvém CV by měla označovat tvou ambici, tedy **co hledáš**, a ne co děláš teď. Ať už jsi účetní nebo máš 5 let zkušeností s PHP, pokud měníš zaměření a hledáš práci s daty, napíšeš „junior data analyst”.

Pozice **nezahrnuje název firmy**. Ani té, kde zrovna pracuješ, ani té, kam se teprve hlásíš. Hlavička CV je reklama na tvou osobu a ambici. Současná firma v ní nemá co dělat, protože není součástí té ambice. A předjímat už v CV, že tě někam vezmou, je trochu troufalé.

### 3. Kontakty

V kontaktech by určitě měl být **e-mail a telefon**, na který se recruiter dovolá. Což běžně dělají, takže zvedej neznámá čísla. Můžeš přidat i odkazy na své [GitHub](github-profile.md) a [LinkedIn](linkedin.md) profily.

**Adresu bydliště vynech**, je to zbytečný údaj. V rámci výběrového řízení ti firmy žádné dopisy posílat nebudou. Pokud se někam hlásíš, předpokládá se, že se na místo pracoviště zvládneš dopravit, nebo že si vyřešíš stěhování.

Dá se to vyřídit v [průvodním dopise](#motivacni-dopis), ale pokud má firma víc poboček, můžeš ke kontaktům připsat **město** jedné z nich, nebo nějakou spádovou oblast, aby bylo jasné, kam přesně se hlásíš. Kde zrovna bydlíš je nepodstatné. Vzdálené město na CV vzbudí každopádně zvědavost. Budou se ptát, jestli hodláš dojíždět, pracovat na dálku, nebo se stěhovat.

Pokud nejsi původem z Česka, může se hodit připsat **zemi nebo občanství**, aby firma mohla počítat s vyřizováním pracovního víza, případně aby si mohli včas sehnat šarišsko-český slovník.

### 4. Souhrn

Nejdůležitější část životopisu! Pár úvodních vět, které částečně nahrazují [motivační dopis](#motivacni-dopis). Snažíš se zhuštěně popsat:

1. Kým jsi teď, jaký je aktuální stav?
2. Kým chceš být v budoucnu, jaká je tvá ambice?

Je to [perex](https://cs.wikipedia.org/wiki/Perex) zbytku dokumentu. **Po jeho přečtení musí mít druhá strana jasno, zda chce číst dál.**

- „QA inženýrka, která se chce stát Python programátorkou. Po kurzu od PyLadies a několika vlastních projektech hledám první pracovní příležitost.“
- „I am a recent graduate of the React Girls course, currently contributing to open source projects in Česko.Digital. I am looking for an entry level React job with an opportunity to learn the basics of UX.“
- „Programovat zkouším od základní školy, poslední rok se učím hlavně C#. Po práci ve strojírenství hledám svou první příležitost jako .NET junior programátor, ideálně na dálku.“

Kdo si CV otevře a toto přečte, okamžitě si tě **dokáže zařadit** a zbytek životopisu čte už v **kontextu, který souhrnem nastavuješ**:

- „Aha, začátečnice v PHP.“
- „Aha, bývalý zubař, teď frontendista.“
- „Aha, testerka a datová analytička, která jde na vývojářku.“

Recruiter také dokáže hned vyhodnotit, **jestli se tvoje cíle shodují s jejich očekáváními**. Může to ušetřit hodně času na obou stranách.

{% call blockquote_avatar(
  'Pro recruitery je hlavní se hned zorientovat. Klíčový je souhrn — co umíš za technologie? Jaké tě baví? Kam směřuješ? Potom seznam pozic a na čem jsi pracoval.',
  'pavel-brozek.jpg',
  'Pavel Brožek'
) %}
  Pavel Brožek, recruiter v [dreamBIG](https://www.dreambig.cz/)
{% endcall %}

{% call blockquote_avatar(
  'Můžete si to představit jako zkrácenou verzi průvodního dopisu. Stačí tři, čtyři věty. Kdo jste? Jaká je vaše motivace?',
  'jiri-psotka.jpg',
  'Jiří Psotka'
) %}
  Jiří Psotka, recruiter v [Red Hatu](https://www.redhat.com/en/jobs) v [prvním dílu podcastu junior.guru](../podcast/1.jinja)
{% endcall %}

Nikdo neříká, že je jednoduché souhrn napsat, ale když se ti to povede, **je to tvůj trumf**. Je úplně normální, že to má hlavu a patu až na desátý pokus. Většinou **to mnohem rychleji vymyslí tvůj kamarád**, protože tvou kariéru vnímá z nadhledu.

Vizuálně ať je to **velkorysé** jako vstup do významné budovy. Kresbu monumentálního sloupořadí si odpusť, ale ať je souhrn první, hned za hlavičkou dokumentu. Dej mu celou šířku stránky a dopřej mu klidně větší písmo.

{% call note() %}
  {{ 'lightbulb'|icon }} V [klubu](../club.md) ti rádi dáme na souhrn zpětnou vazbu. Je tam jak Honza, autor tohoto návodu, tak i spousta lidí, kteří mají zkušenosti z obou stran pohovorů.
{% endcall %}

### 5. Dovednosti

Sepiš **technologie, případně metodiky nebo nástroje, které ovládáš**. Technologie jsou HTML nebo Python, metodika je třeba SCRUM, tedy „způsob jak něco dělat“. Nástroj může být Git nebo Jira.

Programátoři si každý den rozšiřují obzory a koukají na nové věci. Ve skutečnosti ale i největší profíci **znají dobře pouze několik technologií**. U dalších jen povrchně tuší o co jde, aby si o nich mohli povídat na obědě.

Do CV patří pouze **věci, se kterými zvládneš dokončit základní praktické úkoly**. YouTube videa o HTML nestačí. Máš vytvořené dva tři HTML soubory? V pořádku. Pokud nemáš praktickou zkušenost, neumíš s věcí pracovat a je nefér ji někomu nabízet jako dovednost. Nic si nepřibarvuj, vždy se na to přijde a budeš působit nevěrohodně.

{% call blockquote_avatar(
  'Někdo se chlubí: Scala, Groovy, Kotlin. Nadchne mě to, ovšem hned dostanu studenou sprchu, protože neví, jaký je mezi nimi rozdíl.',
  'lubos-racansky.jpg',
  'Luboš Račanský'
) %}
  Luboš Račanský, profesionální programátor, autor článku [O náboru juniorů](https://blog.zvestov.cz/software%20development/2018/01/26/o-naboru-junioru.html)
{% endcall %}

Neznamená to samozřejmě, že se nemůžeš hlásit na inzerát, kde **chtějí technologii, kterou neumíš**. Nepiš si ji ale do dovedností. Pokud tě něco láká, ale ještě to neznáš, vyjádři tuto svou ambici v [souhrnu](#4-souhrn).

A opravdu **stačí praktická zkušenost**, nemusíš být expert. Firma si stejně bude číst kód tvých projektů, případně si tě prozkouší. Ať si sami vyhodnotí, zda je tvá znalost dostatečná pro jejich aktuální potřeby.

I když je to oblíbené, **nedělej ze svých znalostí graf s procenty**. Co znamená 100 %? Měl by autor Pythonu plné skóre, když po 30 letech zkušeností říká, že mnohá zákoutí jazyka nezná a stále v něm něco objevuje? Sebehodnocení na neukotvené škále je akorát podhoubím pro [Dunningův–Krugerův efekt](https://cs.wikipedia.org/wiki/Dunning%C5%AFv%E2%80%93Kruger%C5%AFv_efekt).

Neuváděj příliš mnoho dovedností, nedá se v tom orientovat. **Významné technologie** od podružných poznáš tak, že mají svou stránku na (anglické) Wikipedii. Například [Django](https://en.wikipedia.org/wiki/Django_(web_framework)) ji má, [arrow](https://pypi.org/project/arrow/) ne. A vyber jen ty, kterým se chceš do budoucna nejvíc věnovat, nebo jsou podstatné pro konkrétní pozici.

Pokud nechceš trolit, věci jako „práce s počítačem“ nebo „práce s internetem“ si v IT fakt odpusť. Také kancelářské programy se berou na většině pozicích jako samozřejmost.

Takže co je výsledkem? Takové jakoby hashtagy. **Pár klíčových slov za sebou, v jednom řádku, výrazně v úvodu.** Spolu s pozicí a souhrnem to druhé straně pomůže okamžitě si tě zařadit. Opravdu to stačí. Nemůžeš si pomoci a chceš se rozepisovat? Posuň aspoň dovednosti někam níž, ať exkluzivní prostor v úvodu CV nezaplňují odstavce textu.

### 6. Projekty

Ukaž, že zvládáš **prakticky použít vědomosti z kurzů**. Že umíš vyrobit něco vlastního, nebo že se na něčem podílíš. [Portfolio projektů](projects.md) je pro juniory nejdůležitější věc po [souhrnu](#4-souhrn), tak ať jsou na CV hezky vysoko a viditelně.

Absolvent školy s IT zaměřením ukazuje projekty jako svou **první praxi**. Samouk jimi navíc **kompenzuje formální vzdělání**. Jako by říkal: „Sice nemám školy, ale pokud dokážu vytvořit toto, tak je to asi jedno, ne?“

Zajímavý projekt ti také může pomoci **přeskočit ověřování technických znalostí** během přijímacího procesu, jako jsou domácí úlohy nebo testy.

Máš nějaký **větší vlastní výtvor**? Bakalářku nebo diplomku? Vypomáháš na něčem společensky prospěšném v rámci [Česko.Digital](https://blog.cesko.digital/2021/06/zkuste-open-source)? Pochlub se!

{% call blockquote_avatar(
  'Na pohovoru mě nezajímá, co kdo vystudoval, ale jak přemýšlí a jaké má vlastní projekty. Nemusí být nijak světoborné, je to však praxe, kterou ani čerstvý inženýr často nemá.',
  'josef-skladanka.jpg',
  'Josef Skládanka'
) %}
  Josef Skládanka, profesionální programátor
{% endcall %}

{% call blockquote_avatar(
  'Kandidáti na juniorní role si často myslí, že musí mít nějaké obrovské, komplexní projekty, aby mělo význam se tím chlubit. Pro mě je důležité vidět, že do něčeho investuješ čas, energii, někdy i peníze, a že to dotahuješ. Skoro dokončený projekt taky stačí.',
  'jiri-psotka.jpg',
  'Jiří Psotka'
) %}
  Jiří Psotka, recruiter v [Red Hatu](https://www.redhat.com/en/jobs) v [prvním dílu podcastu junior.guru](../podcast/1.jinja)
{% endcall %}

U každé takové věci by neměl chybět **název, krátký popis a odkazy**. Nejen odkaz na kód, ale i na ukázku. Pokud jde o dobrovolnictví nebo jinou spolupráci, popiš kontext a svůj přínos.

Kód projektu můžeš poskytnout **ke stažení jako zip** na nějakém veřejném odkazu. Dropbox bude působit lépe než Ulož.to. Nejmazanější volbou je ale [používat GitHub](github-profile.md), ideálně už během samotného programování. Prokážeš tím, že umíš aspoň trochu pracovat s Gitem a druhá strana si může vše projít přímo v prohlížeči.

Nikdo si nebude nic instalovat, takže **ukázka je zásadní**. Recruiteři kód vůbec nečtou a i programátoři z týmu, kam chceš nastoupit, si jej otevřou až v průběhu technického kola pohovoru. Buď ať to jde proklikat v prohlížeči, nebo někam dej aspoň snímky obrazovky. Když vyrobíš něco interaktivního, třeba hru, můžeš natočit záznam obrazovky, jak ji hraješ, a do CV dát odkaz na YouTube.

Určitě do CV **vypíchni konkrétní projekty**, které chceš ukázat a u každého měj zvlášť odkazy na jejich repozitáře. Nespoléhej se na jeden odkaz na GitHub profil, do hloubky si jej bude procházet málokdo. Pokud si někdo při rozřazování kandidátů otevře repozitář na GitHubu, **proletí očima hlavně [README](git.md#readme)**. Ujisti se, že všechny tvé významné projekty ho mají.

{% call note() %}
  {{ 'lightbulb'|icon }} Pochlub se svými výrobky v [klubu](../club.md)! Rádi na ně mrkneme, pomůžeme ti vyladit si GitHub a vylepšit README tvých projektů.
{% endcall %}

### 7. Vzdělání

Z formálního vzdělání uveď **pouze nejvyšší dosažené**. Rozmezí let, název školy, obor. U nedokončeného vzdělání se hodí to nějak poznačit. Pokud byl na konci projekt, třeba diplomka, dej tam zmínku a téma práce. Jestliže máš více studovaných VŠ, dej tam všechny. U škol vůbec neřeš, zda mají něco společného s IT, vždy to říká něco o **základu, na kterém stavíš**.

Pokud máš kurzy, do vzdělání si je určitě napiš. Pouze však ty, které **souvisí s oborem, délku mají v řádu měsíců a organizuje je nějaká instituce**. Je jedno, jestli byly online nebo prezenčně. YouTube videa nebo mini kurzy z Udemy spíš ne, Coursera nebo PyLadies spíš ano.

Kurzů je hodně a druhá strana skoro nikdy nebude ten tvůj znát nějak blíž. Nemá smysl soutěžit v tom, zda je jeden prestižnější než druhý, jen aby to vypadalo dobře na CV. Na první pohled zaujmou maximálně jména s dobrým marketingem, např. Czechitas. Práci si ale najdou i samouci bez kurzů, protože **na kurzy se nehraje**. Hraje se na praxi, tedy na [projekty](#6-projekty).

Jestliže máš nějaké **certifikace**, nezapomeň je zmínit. Certifikacemi se myslí např. ISTQB u testerů, tedy široce uznávaná věc s vlastní stránkou na Wikipedii. Omalovánku, kterou ti dali za absolvování kurzu, si založ k diplomům z plavání z páté třídy. Mrkni na kapitolu [Certifikáty a certifikace](./certification.md).

Pokud ti z toho vyšlo více záznamů o vzdělání než jeden, seřaď je chronologicky od nejnovějšího po nejstarší.

### 8. Pracovní zkušenosti

Jestli nemáš žádnou praxi v oboru, pracovní zkušenosti odsuň takhle dozadu. Jejich roli přebírá sekce s [projekty](#6-projekty). Pokud však za sebou máš **stáž, brigádu, nebo dobrovolnictví** v IT, dej to samozřejmě na odiv v úvodu životopisu.

Práci mimo obor silně zestručni. Vždy jen **roky od do, název firmy, pozice**. Od nejnovějších po nejstarší. Nemusíš ani uvádět všechny. Vyber pouze významné milníky nebo zkušenosti, které se aspoň trochu váží k pozici, na kterou se hlásíš.

Do jednoho záznamu dej klidně i **celé úseky kariéry**. „Od do jsem dělal v bankovnictví, vypracoval jsem se na pozici investičního specialisty…“ Další detaily těchto minulých zaměstnání jsou pro tvou budoucnost vedlejší.

Připiš **větu o tom, co bylo náplní tvojí práce**. Kuchařinu asi vysvětlovat nemusíš, ale třeba už manažerka je dost široký pojem. Co přesně dělají dělníci na úseku pálených lupků zase neví nikdo mimo úsek.

Když přihodíš, **co se ti tam povedlo a co díky tomu umíš**, jen dobře. Může to být vedení lidí, týmová práce, komunikativnost, sebevzdělávání, koordinace, pečlivost. To vše se dá využít i v IT a je škoda to nezmínit. Samozřejmě krátce.

Můžeš napsat obecně o své chuti ke vzdělávání, ale konkrétní **certifikáty z oborů mimo IT** nikomu nic říkat nebudou. Bohužel, třicet osvědčení ze zubařské praxe při programování nevyužiješ. Zarámuj si je, ale na CV budou zbytečně. I když, popravdě málokdo viděl tolik _[technical debt](https://en.wikipedia.org/wiki/Technical_debt)_ a _[legacy](https://en.wikipedia.org/wiki/Legacy_code)_ jako zubaři.

Firma může usoudit, že právě díky znalosti jiného oboru **můžeš přispět něčím, co ještě nemají**, ať už je to vědecký pohled, lidský přístup, nebo pečlivost účetní. Stalo se i to, že při pohovoru ocenili manažerské dovednosti prokázané při hraní online her (viz [Wired](https://www.wired.com/2006/04/learn/), [CNN](https://web.archive.org/web/20241118204152/https://money.cnn.com/2014/06/19/technology/world-of-warcraft-resume/index.html)). Přemýšlej, jak se díky tomu můžeš lépe prodat, ale aplikuj to spíš v [souhrnu](#4-souhrn) nebo [sekci se _soft skills_](#9-soft-skills). Seznam pracovních zkušeností zachovej stručný.

### 9. Soft skills

„Pečlivá, spolehlivá, motivovaná, komunikativní.“ „Týmový hráč, odolný vůči stresu, s velkou chutí učit se.“ **Nadýchané obláčky slov**, které ve skutečnosti nic neznamenají a do životopisu si je může napsat kdokoliv. Na Wikipedii píšou „měkké“ nebo „jemné“ dovednosti, ale v praxi tomu nikdo neříká jinak než _soft skills_.

I kdyby podvědomě, většina lidí ta slova pouze přeletí. Čtou jen „bla bla bla“ a **ve skutečnosti myslí na řízek v kantýně**. Zkus každou vlastnost podložit něčím konkrétním, co si čtenář představí místo řízku:

- „Jsem pečlivý. Od roku 1997 sbírám známky a pletu svetry.“
- „Jsem týmová hráčka. Dlouhé roky jsem hrála volejbal.“
- „Zvládám organizaci času. S rodinou a zvířaty to jinak ani nejde.“
- „Mám disciplínu. Na fotbalový trénink chodím třikrát týdně.”
- „Ráda se vzdělávám. Poslouchám podcasty, přednášky, čtu odborné knihy.“

Pokud se ti nepovede vlastnost ilustrovat, raději ji neuváděj. Ostatně, **tato sekce není povinná**, nic je také lepší než šňůra bezvýznamných slov. Když se ti ale _soft skills_ povede udělat dobře, vynikneš a zase o kousek vykompenzuješ chybějící praxi.

### 10. Jazyky

Někde na konci CV měj seznam všech jazyků, které ovládáš. Většinu firem bude zajímat **hlavně angličtina**. Jestli hledáš práci v Evropě, popiš znalost každého jazyka pomocí [SERR](https://cs.wikipedia.org/wiki/Spole%C4%8Dn%C3%BD_evropsk%C3%BD_referen%C4%8Dn%C3%AD_r%C3%A1mec) (anglicky _CEFR_). Úroveň angličtiny si můžeš otestovat třeba přes [EF SET](https://www.efset.org/).

[Europass](https://europass.cz/) používá **sebehodnotící škálu** založenou na SERR v pěti okruzích: Poslech, čtení, mluvená komunikace, samostatný ústní projev a psaní. Ke každému okruhu a každé úrovni jsou tam navíc jedno až dvouvětné popisky pro orientaci.

Na druhou stranu, v IT to nikdo zas tak moc neřeší. Stejně všichni nakonec mluví nějakou variantou [Euro English](https://cs.wikipedia.org/wiki/Euro_English). **Gramatika jde stranou, hlavně když se domluvíš.** Většinou si jazyk ověří během pohovoru a pokud dokážeš vést konverzaci, bývá to _good enough_. Určitě nemusíš mít oficiální certifikace.

## Zbytečnosti

Obecně platí, že nic, co na CV nemusí nutně být, by tam být nemělo. Neplýtvej místem a nerozptyluj čtenáře od toho důležitého.

Odpusť si například **nadpis** „Životopis“ nebo „Curriculum Vitae“. Ze samotného obsahu dokumentu je zcela zřejmé, o co jde.

**Fotku** si na CV dát můžeš, ale nemusíš. Záleží na tvém pocitu. Když tam nebude, máš větší šanci, že tě na pohovor pozvali díky vědomostem a ne sympatickému úsměvu, což jsou plusové body pro ně i pro tebe. Fotka může recruiterům pomáhat přiřadit si tě k CV při osobním setkání.

**Datum narození**, **rodinný stav** nebo přesná **adresa bydliště** nemusí nikoho zajímat. Pokud už z nějakého důvodu chceš adresu uvést, stačí nejbližší město, kde se zdržuješ. Určitě si nepiš na CV adresu trvalého bydliště u rodičů, které je na druhém konci republiky a jezdíš tam akorát na Vánoce.

Lidé se liší v tom, zda je zajímají tvé **koníčky**. Někdo je ani nečte, jiný je použije jako otvírák konverzace, další v tom hledá lidskost, osobnost. Problém je, že když děláš hokej, jde v tom vidět týmového hráče i zpoceného primitiva. Vezmi jejich rámování do vlastních rukou a udělej z koníčků raději ty _[soft skills](#9-soft-skills)_.

Programátoři běžně **nedostávají služební auta a nikam neřídí**, takže není nutné psát, jestli máš řidičák a jaký. Dá se to ale sfouknout dvěma slovy, tak pokud na ně máš místo, proč ne.

Ačkoliv se v některých vzorech nacházejí, **vlastnoruční podpis** a **datum vytvoření dokumentu** jsou druhé straně k ničemu a působí archaicky. Když firma obdrží CV, automaticky předpokládá, že je aktuální.

## Motivační dopis

Většinou se na pozici hlásíš e-mailem. Ten má předmět, tělo a do přílohy dáváš PDF s životopisem. Tomuto e-mailu se říká průvodní nebo motivační dopis, anglicky _cover letter_.

U **předmětu** je dobré se zamyslet nad tím, že firma dostává takových e-mailů hodně. Je tedy praktické, když tam bude tvoje jméno a přesný název vypsané pozice, na kterou se hlásíš. Když si recruiter otevře schránku, bude se hned orientovat. Tvůj e-mail také snadněji vyhledá.

Motivační dopis určitě **nedávej do zvláštního dokumentu** a nepřikládej jako přílohu. Piš rovnou do těla e-mailu a **piš to krátké**. Žádný „hluboký lidský příběh“ na deset odstavců. Nepřepisuj životopis do prózy. I tam, kde to čtou, s tím chtějí trávit maximálně několik sekund.

### Souhrn místo dopisu

Důležitost motivačního dopisu se v různých firmách liší. **Někde ho skoro nečtou, jinde má váhu větší.** Nikdy však nejde o zásadní věc. Pokud máš dobře udělaný [souhrn](#4-souhrn), můžeš motivační dopis vypustit. Napiš na jakou pozici se hlásíš, přilož CV, hotovo. Na druhou stranu, pokud by dopis četli, je to **prostor sdělit něco navíc**.

### Co psát

Nemá moc smysl vyrábět si polotovar. Jednotlivé **zprávy si mohou být podobné, ale každá by měla být ze 100 % na míru dané nabídce** a situaci.

Motivačním dopisem usiluješ o „cenu sympatie“, případně **dodáváš kontext**. Píšeš do své vysněné firmy? Znáš od nich konkrétní lidi, například ze srazů nebo konferencí? Dej klidně průchod emocím, pokud jsou upřímné. Popiš např. své nadšení pro obor, nebo ambici učit se něco konkrétního. Můžeš také předem objasnit něco, co by při čtení životopisu mohlo vyvolávat otázky.

Buď spontánní. **Nalaď se na komunikační vlnu z pracovního inzerátu.** Jsou upjatí a seriózní? Formuluj to taky tak. Pohodoví? Piš to jak zprávu kamarádce. Korporátní text plný obecné vaty a nicneříkajících superlativů? Uvař bramboračku z podobných formulací.

## Zpětná vazba

Než začneš CV posílat do firem, nech si na něj dát zpětnou vazbu. Pokud nemáš po ruce někoho z IT nebo HR, nevadí. Skoro kdokoliv ti **zkontroluje překlepy, angličtinu, smysluplnost vět, nebo jestli se dá klikat na odkazy**. Zpětnou vazbu na svůj životopis můžeš dostat i na místním Discordu.

{{ club_teaser("Pošli CV do klubu") }}

## Něco extra

Stačí životopis? Nemáš vlastně místo CV vytvořit video nebo hru? Možností, jak se firmám odprezetovat, je spousta.

### Založ si LinkedIn

[LinkedIn](linkedin.md) je profesní sociální síť, kde recruiteři hledají kandidáty, kandidáti firmy, firmy byznys, a tak dále. **Založ si tam profil** a využij to na maximum.

Ačkoliv LinkedIn **umožňuje stáhnout profil jako PDF**, nepoužívej to jako svoje CV. Výsledný dokument je tragicky nepřehledný.

### Osobní web

Pokud se učíš vytvářet webovky, **vyrob si osobní stránky**. Bude se to počítat jako projekt a zároveň je to možnost, jak se představit barevněji, než PDF dokumentem. Můžeš do toho vložit tolik kreativity, kolik jen chceš. Víc je o tom v kapitole [osobní web a blog](candidate.md#osobni-web-a-blog).

{% call figure('static/figures/robert-belan.png', 1024, 583, 'Robert Belan') %}
  Robert Belan si vyrobil osobní webovky jako konfigurátor postavy v RPG hře
{% endcall %}

### Buď člověk

[Yablko](https://robweb.sk) radí, ať dáš **průchod svojí osobnosti**. Píše o tom ve svém starším článku [Ukaž, že jsi člověk](https://medium.com/@yablko/uk%C3%A1%C5%BE-%C5%BEe-si-%C4%8Dlovek-3d134c421940) a zmiňuje to i tady ve videu:

{{ video_card(
  'Jak získat job v IT?',
  '7min',
  'https://www.youtube.com/watch?v=IyaxCqoqeHo',
  'Posíláš životopisy, ale nedaří se ti vyvolat zájem? Neposílej životopis, ušij něco na míru.',
) }}

Máš se naučit [dobře prodat co umíš](#jak-nad-tim-premyslet) a dávat do všeho svou osobnost. Pokud máš vysněnou firmu, kde fakt chceš pracovat, máš je oslnit něčím ušitým na míru.

{% call blockquote_avatar(
  'Osobne nerozumiem, prečo by dizajnér neposlal pekné CV. Prečo strihač nepošle video a pisálek ho nenapíše formou poviedky.',
  'yablko.jpg',
  'yablko'
) %}
  yablko, v článku [Ukáž, že si človek](https://www.youtube.com/watch?v=Tna7J05UoYU&list=PLhB6F20C-jTPITEXEHus6fVZDfNxzRbv_)
{% endcall %}

Tato strategie je fajn, ale **můžeš být v situaci, kdy se to nehodí**. Nemusíš mít zrovna mentální sílu vystoupit z davu, ne každý má vysněnou firmu, ne vždy si můžeš dovolit programovat něco na míru. A korporát možná ocení PDF víc než hru, kterou si můžou zahrát.

**Životopis podle junior.guru je kompromis**. Posíláš sice papír, ale uděláš ho tak, aby nebyl nudný. Dáváš do popředí svoje výrobky a silné stránky. Necháváš vyniknout, kdo jsi.



<!-- {#

Only 16% of companies looked for further information (my webpage, YouTube channel, GitHub account). Therefore, it’s important to highlight your accomplishments explicitly. https://vesecky-adam.medium.com/100-interviews-in-1-year-what-have-i-found-part-ii-the-interviews-492eebbecf48

Bez projektů jde dnes tvoje CVčko přímo do koše. 200 lidí na jeden inzerát. jak vynikneš?

S tím souhlasím, mně jednou HR manager řekl, že poslal můj životopis dál jen kvůli tomu, že měl pěkný design a měl dobrý pocit z toho. :)  Tehdy jsem našla designerku na platformě UpWork, které jsem poslala všechny informace a ona mi ho napsala a udělala design, teď bych to už dělala sama. Doporučuju https://flowcv.io/ , je to docela jednoduché na naklikávání a vypadá dobře.

jestli chceš sám zkusit, doporučuji flowcv.io, já v tom vyťukala několik životopisů několika různých lidem a všem se líbilo 🙂

jak na cv v angličtině
https://www.youtube.com/watch?v=Jhn5-N7ABP8

- šablona od Dana (Šablona CV thread na Discordu)
- citace z kayly clanku o syndromu
- konkretni priklady na realnych CV
- citace monika ptacnikova, Málokdy poslouchám podcast pro juniory a celou dobu kývu souhlasně hlavou. S Monikou ptacnikovou se mi to stalo, opravdu realisticky náhled na pracovní trh a na možnosti, jaké juniorky a juniori mají 👏 Kolem -5 minuty ptacnikova rika o CV tak něco vzit z tiho - https://overcast.fm/+oxWgC3EHI
- citace nulíčková a link na kariérko
- Další dobré tipy jsou i v [Tech Interview Handbook](https://yangshun.github.io/tech-interview-handbook/resume) nebo na [prace.rovnou.cz](https://prace.rovnou.cz/jak-zivotopis.html).
- hledání práce tím, že se nabídnu v různých skupinách na FB

https://www.resumemaker.online/

První článek je o životopisech EUROPASS. Ve Vašem článku se zmiňujete, že životopisy od EUROPASSu jsou neoriginální, což by šlo krásně podložit naším článkem Europass CV:Některá pozitiva a řada negativ evropského životopisu.

Dále máme několik užitečných návodů i se vzory na životopisy pro jednotlivé pracovní pozice například: Vývojář softwaru, Programátorka, IT manažer či Stáž, případně i obecný návod pro životopis bez jakýchkoli pracovních zkušeností (https://cvapp.cz/blog/jak-napsat-zivotopis-kdyz-vam-chybi%20jakekoli-zkusenosti).

---
Osobní web
Není pro každého a ne každá profese v IT, ani programátorská, nemá nutně skillset na tvorbu vlastního webu. Ale pokud jsem frontenďák, je to low hanging fruit. Třeba https://www.robertbelan.com/ nebo další.

Nebo si udělám web, kde mám možná víc prostoru kreativně vyjádřit kdo jsem a co mám za sebou, i když si ho nevytvořím od píky, ale na nějaké platformě. Taky tam můžu mít třeba blog, kde se dá popisovat např. moje cesta do IT nebo co jsem se naučil nového a může to sloužit jako impostorsyndromový zápisník: https://itnoob.cz/, https://ivet1987.wz.cz/

https://junior.guru/candidate-handbook/#osobni-web-a-blog
---

https://jsonresume.org/
flowcv.io

thread o tom ze mas rict proc zrovna do te firmy
https://discord.com/channels/769966886598737931/932606706809204786/933082534621892638

--- https://discord.com/channels/769966886598737931/839059491432431616/849041512499249222
Ještě k těm jazykům, Europass (https://europass.cz/) v životopisu, v oddílu Jazykové znalosti, používá _sebehodnotící_ škálu založenou na SERR v pěti samostatných okruzích - poslech, čtení, mluvená komunikace, samostatný ústní projev a psaní - ke každému okruhu a každé úrovni jsou tam navíc jedno až dvouvětné popisky pro orientaci. Podle mě se tak snáz vyjádří konkrétní znalosti a zkušenosti v daném cizím jazyku.
---


--- https://discord.com/channels/769966886598737931/789107031939481641/1035104757188137014
Obecná poučka je to, co najdeš tady: https://junior.guru/handbook/cv/
1) Napiš seznam toho, co umíš. Bez specifikace „jak moc“.
2) U projektů v CV můžeš v popisu zmínit hlavní použité technologie.
To, co tu řešíme je ale to, že na jaké seš úrovni, se pozná podle těch projektů.
To platí pro začátečníka bez komerční praxe.

To co píše <@539022501876072448> se týká lidí, co už něco mají za sebou a dá se čekat, že pokud třeba 3 roky pracovali ve firmě a dělali tam weby na Djangu, tak umí ledascos, co je k tomu potřeba, na nějaké úrovni. Samozřejmě je dobré si to ověřit na pohovoru potom.
---


--- https://discord.com/channels/769966886598737931/1099057355620106342/1099665136341487666
A zhruba polovina poslala zamítnutí na základě CV.
Asi 15–20 vůbec neodepsalo. (10–20 %)
---


--- https://discord.com/channels/769966886598737931/839059491432431616/1072271057265901718
<@447531834713047042> Ať tím nekrademe vlákno Lucii… myslím, že historicky největší rozdíl v CV před a po byl <@378163381573648387> a nejen vizuálně a přehledností, ale hlavně obsahem. Takhle to šlo za sebou (bylo jich asi víc, ale tyhle jsou: první, první zásadní změna od Pavla a pak ještě finální verze)
---


--- https://discord.com/channels/769966886598737931/806621830383271937/1061002896558260266
Tool na zhodnocení CV a Linkedinu, který dává i doporučení, co by jak mohlo vypadat. Zkoušel jsem tam nahrát svoje anglické verze Linkedinu a CV a dalo to nějaké zajímavé tipy https://resumeworded.com/
---


--- https://discord.com/channels/769966886598737931/1072259833593606185/1073198884341432340
Rouhodne deti priznat hned na zacatku, pokud s tim ma firma problem, tak to stejne neni firma, kde bys chtela pracovat. Uz to, ze jsi se zvladla ucit a vzdelavat s detmi za zady, tak pravdepodobne dokazes i pracovat s detmi. Porad je v IT ta vyhoda, ze muzes pracovat z domu, pokud by byli deti nemocne, pripadne se postara druhy rodic. Tak doufam, ze to uz neni pro zamestnavatele takova prekazka. Je to soucast nasich zivotu a manzela taky nikomu nezatajuju 😂 Jinak pokud bys mela zajem, muzes se pridat do nasi skupinky <#963857545544470558>
---


--- https://discord.com/channels/769966886598737931/1062006092571361320/1062018181654380605
Na mě to nepůsobí dobře a přesně jak to Martin popsal „vlastně nemám žádnou fotku, tak tam dám něco 5 let starýho“ 🤷‍♂️
Když už fotku, tak něco lehce profesionálnějšího, tedy pro situaci hledám první práci. Dělám nějakej dojem.
Ale to jsem já.
---


--- https://discord.com/channels/769966886598737931/1033829073249644554/1033833523586551848
Do threadu, díky.
Zrovna takoví dva matadoři.

<@614870427931770900>
Flowcv.io - zdarma.

<@414887173154930698>  — Today at 9:53 PM
prosímtě ještě potřebuju aby to šlo udělat Česky :))

<@614870427931770900>  — Today at 9:54 PM
Co to přesně znamená?

<@414887173154930698>  — Today at 9:55 PM
ta šablona má nadpisy v angličtině a já potřebuju aby to bylo české cv

<@614870427931770900>  — Today at 9:56 PM
Dá se to změnit

<@414887173154930698>  — Today at 10:00 PM
ty jo jako je to libovka, jenom nevím kde to změnit :))
---


--- https://discord.com/channels/769966886598737931/991253586312953976/991387575413653635
Mně tam chybí třeba tvoje jméno.

Ten dark mode taky působí zvláštně, předpokládám, že to využije někdo, kdo nemá rád příliš velký jas nebo se mu to blbě čte na světlém a takhle ten problém vlastně vůbec neřešíš, protože tam zůstávají dvě obří bílé pruhy. Za mě bych to teda buď neřešila, nebo to dotáhla.

Zkusila bych být také víc specifická ohledně tvých dosažených "produktů" v práci.
`Work on application for logistics. Drag and drop, infinite scroll, breadcrumb navigation, pagination etc.`
by mohlo byt
`Worked on [...technologie...] applications for logistics. Developed drag & drop feature for [...] using [...] to facilitate user interaction with the system, implemented infinite scroll with lazy loading and pagination for [...]` atp.
Něco na ten styl.  Co jsi dělala, co jsi k tomu používala, čeho jsi tím dosáhla.  Hodně se mi tenhle model osvědčil 🙂
Obzvlášť, pokud ten kód/projekt není nikde veřejně.
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1128348049748545536
třeba mrkni na můj profil (https://www.linkedin.com/in/mia-bajic/) a všimni si prvního odstavce:
> My primary area of focus is backend development, but I am also highly interested in exploring new technologies in the realm of infrastructure, particularly Kubernetes, and data science.
v celém profilu mám python zmíněný x-krát, takže mi ty nabídky na Python, backend a i Kubernetes chodí i když o ně nemám zájem.

disclaimer: nejsem HR, tak třeba někdo líp poradí
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1183365205078589501
Má smysl předělávat CV do ČJ, když ho mám defaultně v AJ, ale firma má v inzerátu "zašli životopis v ČJ", i když požaduje angličtinu?

Upravuju si každé CV podle požadavků konkrétní firmy, kam ho posílám. Je to vždy docela pracné vymyslet co vypustit a co naopak dopsat. Má smysl ztrácet čas tímhle, když bych se hlásila na pozici, která by pro mě byla jen doplňková a měla mi zajistit třeba i minimální příjem v době dalšího studia programování?
---


--- https://discord.com/channels/769966886598737931/1170645820748599328/1171924140136083496
CV je ustálený útvar s určitou funkcí, rolí a historií a pravidly, podobně jako slohové útvary  nebo jakékoli komunikáty (úvaha, složenka, objednání si v restauraci). Není mi moc jasné, odkud se vzal pojem autentičnosti jako související a určující, pokud se pod autenticitu zařazují překlepy, neaktuální fotka nebo fotka nekvalitní. Jako u každého formátu jsou i u CV místa, kde lze být (a je záhodno být) kreativní a osobitý, a místa, kde takové chování vyústí pouze v nižší kvalitu výsledku. **Právě proto, že drtivá většina lidí přistupuje k CV jiným způsobem, což určuje pravidla hry**: překlepy v náhodné zprávě v chatu neznamenají nic, překlepy v CV jsou příznakové; jsou mínus a mohou být čteny jako lenost, zbrklost, nezájem, nepéče...

Nadto je CV vysoce neimprovizovaný útvar; druhá strana ho oprávněně čte jako připravovaný (a už jen tím mimochodem stylizovaný) a servírovaný pro ni. Počítat s nějakou korekcí a shovívavostí u druhé strany je z mého hlediska nerozumné a naivní. Minimálně přicházíš o část čtenářů a zájmu, a tedy i o část možností/nabídek. Ale to zřejmě víš a jsi tomu naopak rád.

V takovém případě používáš svou možnost chovat se příznakově (a psát CV špatně) správně a vhodně, akorát jsme pak trochu zbytečně vypisovali feedback ve snaze CV narovnat k obrazu obecně přijímanému. Ať je to jakkoli, přeju Ti, ať CV splní Tvá očekávání.
---


Lenka: Nedávat si do CV atd slovo junior ani na LinkedIn, proste napsat umím to a to a podložit to tím a tím a nechat na druhé straně, at si zhodnoti senioritu


--- https://discord.com/channels/769966886598737931/788826407412170752/1220317640174731334
Tak mě napadá, že v CV by se rovnou dal možná naznačit ten „deal“, že za možnost se věnovat rodině (pružná pracovní doba) získají loajálnějšího člověka do týmu, protože ví, že to není běžné nebo tak něco. Ideál by samozřejmě byl, kdybychom to nemuseli řešit, protože je to normální, ale jsme tam kde jsme.
---


https://www.linkedin.com/posts/petranulickova_sharingiscaring-zivotopis-activity-7193200652393607170-Sh6Y?utm_source=share&utm_medium=member_desktop


--- https://discord.com/channels/769966886598737931/788826407412170752/1241953460014809170
CV! Až zas budete designovat jako nedesignéři… tak si přečtěte https://www.linkedin.com/posts/petranulickova_sharingiscaring-zivotopis-activity-7193200652393607170-Sh6Y méně je více… ano, až mi nebude blbě z chemoterapie, udělám vám přednášku a věnuju šablonu. Kdo chce šablonu otestovat dřív napište DM.
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1241959718100930570
Bohužel blog, na který odkazuje je nečitelný taky <:lolpain:859017227515854879>, ale už jsem jí psal https://www.petranulickova.cz/l/chyby-v-zivotopisech/
---


--- https://discord.com/channels/769966886598737931/1230251641358258317/1237281354090287117
Odcituju sám sebe

> Nejsi zkušený designér a kombinovat více různých prvků, tvarů, barev, velikostí pro tebe nebude snadné.
>
> Drž se tedy spíš při zemi a nekomplikuj si to.
>
> Kvalita obsahu je v tvém CV mnohem podstatnější než unikátní vzhled.
>
> Když se zamyslíš nad tím, jak vypadají ty obchodně nejúspěšnější e-shopy, tak jsou velmi nudné a podobné jako vejce vejci. Lidi tam jdou nakoupit a ne obdivovat krásu nebo řešit rébus, jak se zrovna tam nakupuje.
>
> Stejně tak recruiteři tvoje CV berou jako zdroj informací o tobě a kandidáty nezvou podle originality CV, ale jestli o nich najdou informace, které zapadají do profilu pozice, kterou obsazují. A na to zjištění informací nemají moc času, proto: čím přehlednější, tím lepší.
---


--- https://discord.com/channels/769966886598737931/1230251641358258317/1237297419847471134
A aby to neznělo jako od puristického funkcionalisty, tak emoční reakce na estetický vjem samozřejmě existuje a má svoji neodpáratelnou roli ve vnímání a přeneseně i vás.

Problém tkví v tom, že něco designovat s tím záměrem a aby to navíc zasáhlo široké publikum je velmi těžké a dřou na tom lidi, co na to mají školy, léta praxe atd.

Proto si myslím, že začít funkcionalisticky není od věci. Čisté a přehledné je lepší než zpatlané. A z toho, co tady často vidím, takové jednoduché CV spíš vynikne v davu nepřehledných z šablon z Canvy. <:lolpain:859017227515854879>

Pro větší zajímavost často stačí trochu zajímavější font…
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1301602352893001768
Vytáhnu z toho (jde o upravený přepis titulků, nejsou to tedy přesné citáty)

> „CV dává smysl, protože když se podíváme na HR nebo na člověka obecně, tak je to líná osoba. Potřebuje vidět hned na první pohled technologie, které jsou relevantní pro danou pozici. Opravdu si projděte všechny zmíněné nástroje v CV tak, aby při prvním otevření CV na ně okamžitě vyskočily. Aby si mohli říct: ‘Jo, tady je C#, Microsoft SQL, SQL jazyk… Super, můžeme ho nebo ji pozvat na online pohovor.’
>
> Asi na to rovnou navážu tím, jestli vůbec musím mít CV, když žádám o roli v IT. V ideálním světě by třeba stačil odkaz na nějaký git, kde mám ukázky kódu a svoje projekty. Nechci tím nijak shazovat HRisty nebo jejich práci, ale mějte tu trpělivost a CV si opravdu připravte. Neplatí to jen pro juniorní pozice. Jak říká Denisa, první síto často nedělají lidé, kteří tomu do hloubky rozumí, takže půjdou hlavně po klíčových slovech. Chápu frustraci, že to možná nemá takovou hodnotu, ale i když je to jen kus papíru, pro nás, když ten filtr děláme – ať už osobně nebo pomocí AI nástrojů – opravdu stojí za to CV přizpůsobit.
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1301604177105125427
k motivačním dopisům

> Pokud v inzerátu není vyžadován motivační dopis, klidně bych ho vynechala. Když dělám nábor, zaměřuji se na to, co je v CV – jaké má kandidát projekty, zkušenosti, jakým směrem se chce dál vyvíjet. První krok je stejně telefonát, kde se ptám přímo na motivaci. Nechci číst text vygenerovaný AI, ale ráda si s kandidátem popovídám o tom, co ho opravdu baví, co potřebuje k efektivní práci a co ho v minulých firmách třeba zklamalo. To mi pomůže zjistit, jestli u nás nebude řešit stejné problémy.
>
> Ne všechny firmy ale nábor dělají takhle. Některé HR  mají tendenci vytvářet si domněnky z CV, a ne vždy zavolají, aby se zeptaly na detaily a kandidáta rovnou eliminují z výběrka. Třeba vidí v CV adresu a usoudí, že kandidát by u nich, pracovat nechtěl, protože je to daleko.
>
> Souhlasím, že motivační dopisy napsané AI jsou zbytečné. Stačí však tři nebo čtyři věty – stručně a vlastními slovy. Něco ve stylu: ‘Viděl jsem, že se technologicky shodujeme, zaujal mě váš manažer na meetupu…’ Prostě osobní zpráva připojená k CV, která naznačí zájem. To není motivační dopis v pravém slova smyslu, dříve se psaly dlouhé a přikládaly k CV. Ale těch pár vět dává to CV lidský rozměr a ukazuje, že kandidát má skutečný zájem a umožňuje to doplnit i informace o tom, že bude stěhovat z Prahy do Brna apod.
> Nemusíte ale psát formální motivační dopis.
---


--- https://discord.com/channels/769966886598737931/789107031939481641/1294323134924718102
Ano, to je samozřejmě možné, že se tak dozví věk, ale stačí se podívat na LI (nevím jestli v CV máš, kdy jsi studovala VŠ) a i kdyby ti nějak bylo 18, když jsi začla, tak z toho zjistím, že ses narodila v roce 1989 nejpozději, takže nějakou představu (bez ohledu na vzhled) si udělají stejně. A rok, dva, tři navíc už asi není rozdíl z tohoto pohledu. 🤷‍♂️
---


--- https://discord.com/channels/769966886598737931/788832177135026197/1268445846555594772
Kdyžtak <@668226181769986078> někam přesuň.

Můj kontakt na LI - Petra Kubita Nulíčková - sdílela velmi dobré rady a tipy ohledně CV: https://www.petranulickova.cz/l/chyby-v-zivotopisech/

Petra v životě viděla cca 50 000 životopisů a další desítky možná stovky tisíc LI profilů.
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1251180184158208122
Ve středu na frontedistech povídala Petra Nulíčková spoustu zajímavého (přednášku si dejte, video bude na https://www.youtube.com/c/FrontendistiCz), ale i když ona je asi trochu extrém, tak sem chtěl vypíchnout jednu věc: vidí prý až několik set CV denně.

Jakákoli vaše „kreativita“ bránící rychlé a snadné čitelnosti CV není v takovém kontextu asi moc vhodná, že? A i když jich někdo vidí „jen“ desítky, tak pořád, že?

Já jen abyste si nepředstavovali, že dorazí vaše CV a pět HR lidí ho hodinu soustředěně analyzuje…
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1251180512828063774
📹  Jo a videovizitky jí prej dorazily v jednotkách a většinu těch lidí umístila, nevím kde je tam příčina a následek, ale ušetřili si prý minimálně screener, protože tam o sobě všecko podstatné pověděli. A můžete si to v klidu připravit… To mě docela zaujalo jako cesta jak vystoupit z davu a ještě to některým nervóznějším může usnadnit první kontakt.
---


Studie Jozifová:
karierni zmena musi byt reflektovana v CV a motivaku, dulezita je sebereflexe a do jake firmy se hlasim, pokud je to genericky tak se to dava pryc. pokud to byl manazer a jde na programatora, tak to jde bokem, protoze ten bude chtit moc penez, switcheri maji hypoteky a maji prehnana financni ocekavani vyhajpovany, takze s pokorou reflektovat tu tranzici

Studie Jozifová:
do motivaku napsat ja vim ze pujdu s platem dolu, zvysuje to strasne sance

Studie Jozifová:
mustr na motivak, ve kterem je "neocekavam ze budu mit stejny plat jako v predchozim zamestnani hned od zacatku", hledam prvni sanci atd.

Studie Jozifová:
lidi neznaji a stydi se - neumi se prodat


https://latexresu.me/
https://www.overleaf.com/latex/templates/tagged/cv


--- https://discord.com/channels/769966886598737931/789107031939481641/1346164546003406869
Sám nevím jistě, kam to dát, protože do <#1123527619716055040> dáváme už hotové CVs na recenze, tak to dám sem, protože pohovory jsou součástí procesu, kde CV hrají zásadní roli reklamního letáku.
Narazil jsem včera na YT na docela dobrá videa od recruitera z USA, takže samozřejmě jiný trh, jiné zvyklosti, ale přišlo mi, že většina toho sedí a alespoň uslyšíte „neposílejte ty vizuálně přepatlaný vícesloupcový CV“ ještě od někoho jinýho, než sem já a <@668226181769986078> v příručce.
https://www.youtube.com/watch?v=R3abknwWX7k
https://www.youtube.com/watch?v=o5vzR_03vQw
https://www.youtube.com/watch?v=F3joY9KCoX8
---


neuvadet nazvy kurzu? protoze mohou byt na blacklistu https://lucietvrdikova.cz/nahlednete-za-oponu-it-kurzy-dotace-reklama-a-realita/
„Rejpla bych si právě do toho, že pak musíš v CV maskovat, u koho si dělal kurz. Protože název instituce tam dávat nemusíš“
https://discord.com/channels/769966886598737931/1355246864206926066/1360152352866308216


--- https://discord.com/channels/769966886598737931/1375466381801291918/1383123429494100110
<@1324778740797935628> Presne tak, tiez mi pride najlepsie co najkonkretnejsie vypisat ake s tym mas skusenosti. Jednak trebars ake nastroje pouzivas a jednak co s nimi konkretne robis. 

Otazka potom je, v akom mnozstve to v zivotpise ma byt. Na trhu mas dnes firmy na celej skale od "ludi co nepracuju s AI a nechytaju vsetky nove trendy ani nechceme" az po "ai je blockchain a za rok to zomrie". V tom prvom pripade by som sa nebal pridat aj komentare k projektom ako si to tam vyuzila atd., v tom druhom pripade ich to skor odradi.

V kazdom pripade by to ale malo znamenat viac ako "ChatGPT - pokročilý". Keď sa na welcome dni kde su kazdy mesiac vsetci nastupujuci zamestnanci do banky pytam kto uz pracoval s ChatGPT tak je hore 90-95% ruk. Samotna zmienka ta dnes uz neodlisi. Ak teda chces ist touto cestou a tymto sposobom skusit zaujat tak je dobre byt co najspecifickejsi 🙂
---


--- https://discord.com/channels/769966886598737931/1429692356705386506/1434645133218807981
A fakt se neboj použít <:chatgpt:1119028488784068649> ne si to nechat úplně vymyslet, ale dávám mu zadání, aby mi dal 10 variant různým stylem apod. a vybírám si z nich části, co mi sedí.
---


#} -->
