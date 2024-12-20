---
title: Mnohdy ani sama firma nemá jasno v tom, koho chce nabrat, říká vývojářka Nina
date: 2024-03-15
interviewee: Nina Břicháčková
interviewee_avatar_path: avatars-participants/nina-brichackova.jpg
author: Adéla Pavlun
author_avatar_path: avatars-participants/adela-pavlun.jpg
author_url: https://www.linkedin.com/in/adelapavlun/
thumbnail_subheading: Nina Břicháčková
thumbnail_image_path: avatars-participants/nina-brichackova.jpg
thumbnail_button_heading: Čti na
thumbnail_button_link: junior.guru/stories
template: main_stories.html
---

{% from 'macros.html' import img, lead with context %}

# {{ page.meta.title }}

<ul class="article-details">
  <li class="article-details-item">
    <a class="article-details-author" href="{{ page.meta.author_url }}" target="_blank" rel="noopener">
      {{ img('static/' + page.meta.author_avatar_path, page.meta.author + ', profilovka', 50, 50, lazy=False, class='article-details-avatar') }}
      <strong>{{ page.meta.author }}</strong>
    </a>
  </li>
  <li class="article-details-item">{{ '{:%-d.%-m.%Y}'.format(page.meta.date) }}</li>
</ul>

<div class="article-lead">
{{ img('static/' + page.meta.interviewee_avatar_path, page.title + ', foto', 100, 100, lazy=False, class='article-image') }}
{% call lead() %}
Osmatřicetiletá Nina toužila pracovat v IT už od malička. Studovala informatiku, pak si ale kvůli nedostatku sebevědomí sama zavřela dveře. Cestu zpět našla díky kurzu Pythonu, který jí nedovolil prokrastinovat a propojil ji i na komunitu Junior Guru. „Díky klubu jsem se nenechala strhnout k učení nové technologie jen pro účely pohovoru,” vzpomíná Nina, které se nabídky práce jen hrnuly. Nadšení opadlo, když zjistila, že je náboráři rozesílají zřejmě naslepo.
{% endcall %}
</div>

**Jak by ses charakterizovala?**

Jsem požitkář všedního dne, co miluje informační a komunikační technologie a osobní rozvoj. Užívám si, jak mě uklidňuje hudba, jak mě dokáží pohltit knížky, jak mi voní káva nebo chutná víno. Líbí se mi pozorovat barvy a dění okolo sebe, odpočívat při masáži, relaxovat v sauně a čerpat energii při procházce Prahou. Těší mě dozvědět se každý den něco, co mě obohatí a rozšíří mi obzory. I přes různé držkopády žiji spokojený život a plním si sny. Ráda pracuji, stejně tak ráda se občas zastavím a nedělám nic.

**A teď profesně, čím se živíš?**

Živím se psaním kódu, skriptováním. Pracuji pro firmu, která má kariérní řád rozdělený na
konzultantské pozice, odtud název pozice — konzultant. U zákazníka působím jako vývojářka automatických testů. Původně jsem se podobným pozicím vyhýbala, myslela jsem, že na to nemám znalosti a kompetence.

Hledala jsem čistě jen developerskou pozici, ale jak pro něco máte talent a cit, tak si vás to najde. Já se zatím usadila v Pythonu a Robot Frameworku. S úsměvem vzpomínám na pohovory, kdy mi nabízeli programování robotických procesů a já je odmítala, protože jsem si pro takové pozice nepřipadala jako vhodný adept. Dost jsem bojovala s impostor syndromem. A i teď mě občas myšlenky na to, že nejsem ten pravý člověk na svém místě, přepadnou. Dnes už bych se ale tolik nebála, protože komplikované výzvy mě baví.

**Kdy sis začala hrát s myšlenkou, že se začneš učit programovat?**

Bylo to ještě na základní škole, okouzlila mě Sandra Bullock jako systémová analytička
Angela Bennettová ve filmu Síť. Pálilo jí to, psala jeden kód za druhým, věděla naprosto
přesně, co kde hledat, aby vyřešila problém. Plus scéna, jak sedí s notebookem na pláži.
A práce snů byla na světě. Chtěla jsem to taky umět a vytvářet něco, co bude prospěšné.

**Takže si plníš dětský sen. Jak ses naučila programovat?**

V rámci výuky na vysoké škole jsme měli základy programování v Java a PHP, a vytváření
webů pomocí HTML a CSS. Bylo to hodně o teorii, o pochopení principů a souvislostí.
Studovala jsem informatiku a těch odborných předmětů bylo tolik, že jsem nedokázala určit, kterým bych se věnovala i v praxi, bavily mě skoro všechny. Jít cestou pokus-omyl jsem nechtěla. Řekla jsem si, že tomu dám čas, a až najdu to své, tak za tím půjdu.

**Nakonec ti to trvalo několik let. Proč jsi oddalovala nástup do IT?**

Roli hrál nedostatek sebedůvěry, pořád jsem si nepřišla dost dobrá, aby mě někde přijali. Bála jsem se neuspět, takže jsem to raději ani nezkusila. Z tehdejší brigády v administrativě jsem přešla na plný úvazek, kdy sice časové možnosti i náplň práce umožňovaly dostudování školy, ale do IT praxe jsem si pomyslně „zavřela dveře“ sama.

**Kdy sis to uvědomila?**

Došlo mi to až po několikaleté pracovní a profesní pauze. Tehdy jsem si uvědomila, že se chci do IT oboru vrátit. Jenže kromě teorie jsem neměla co nabídnout. Potřebovala jsem se opřít o nějaký hard skill. Naskytla se příležitost osvěžit si znalosti v kurzu na Python. Přihlásila jsem se do něj a vrhla se do toho po hlavě. Dlouhodobý závazek jak finanční, tak časový pro mě byl pomyslný bič, který já potřebuji.  Díky podpoře rodiny a přátel jsem mohla učení věnovat veškerý volný čas. Stačila i hodinka, dvě denně. Pomohlo mi přečíst třeba tři odstavce a hned to vyzkoušet. Když jsem měla pocit, že se toho valí moc, dala jsem si dva dny pauzu, a pak pokračovala v mírnějším tempu.

**Co ti kurz dal?**

Pomohl mi ujasnit si, co chci. Naučila jsem se zorganizovat si práci a čas, abych stíhala a nemohla se na nic vymlouvat. Užitečné bylo nebýt na to sama, vědět, že když bude zle, mám se na koho obrátit. Při samostudiu bych prokrastinovala, měla v učení chaos, skákala od jednoho k druhému, točila se v kruhu, hrabala se v nepodstatných detailech, určitě by mě to při prvním neúspěchu odradilo a časem bych to prostě vzdala.

**Takže se nestávalo, že ses na něčem zasekla?**

To se taky stávalo. A tak dlouho jsem se v tom šťourala, až jsem se „odsekla“. Miluji
_aha_ a _yes_ momenty, když si něco uvědomím nebo se něco podaří. Takže metodou krok za krokem jsem procházela články, tutoriály, YouTube videa, simulátory, dokumentace a fóra… Prostě jsem se do toho ponořila, dokud jsem nepochopila, o co jde a neposunula se.

Při každém větším záseku je ale vhodné si říct, zda má smysl se jím zabývat, nebo ho s klidem přejít. S tím jsem se setkala i v tom kurzu, kdy v prvních týdnech mohli účastníci odejít, pokud zjistili, že to není pro ně. A tuším, že i v [příručce na Junior Guru](../handbook/index.md) jsem četla, že nemáš mít výčitky, pokud se zasekneš a zjistíš, že tě programování vlastně ani tak moc nebaví.

**Co je podle tebe nejefektivnější cestou, jak se něco nového naučit?**

Já jsem emocionální člověk, takže pro mě je to jednoznačně nadchnout se pro to, co chci
umět. Vzplanout, otevřít se tomu a zamilovat si ten proces učení. Vědět, co chci a proč, a
nenechat se zviklat pochybnostmi ostatních.
Ryze prakticky:

1. Stanovit si cíl a kroky, jak ho dosáhnout. Chtěla jsem se naučit programovat, abych se mohla ucházet o pozici, kterou jsem si jako inspiraci vytiskla. Plán jsem měla daný kurzem a postupovala jsem podle něj.
2. Najít k sobě parťáky. Učíte se sice sami za sebe, ale nejste na to sami. Vzájemně se hecujete, podporujete, máte zpětnou vazbu. Můžete probrat záseky a neúspěchy, utřídit si myšlenky, upřesnit cíl, upravit plán, získat kontakty, načerpat zkušenosti. Hlavní je nestydět se, nebát se, jen se tomu otevřít.
3. Obklopit se tím, co se chci naučit ve formě článků, tutoriálů, simulátorů, her, mobilních aplikací, fór a komunit, a podle nálady si každý den nějaký zdroj vybrat.
4. Co se naučím hned vyzkoušet a začít používat.
5. Vyhradit si čas a věnovat se učení pravidelně.
6. Dělat si poznámky a vracet se k nim.
7. Odpočívat, nehroutit se a nevzdávat se.

**Nehroutit se a nevzdávat se — to se hezky nastaví, vycházelo to vždy?**

Byla jsem smířená s tím, že to „může bolet“. A někdy i bolelo. Únava, vyčerpání, stres, rychlé tempo, narůstající kvanta informací. Mojí motivací bylo, že nechci jednoduchou práci. Chtěla jsem klid ve smyslu mít svobodu volby, pracovat kdykoli a odkudkoli. To byla velmi silná motivace, kdy po pár dnech odpočinku jsem zase najela na zavedený režim. Navíc moje výhoda je, že jsem duší bojovník, naučená se nevzdávat.

**Zmínila si, že je důležité nenechat se zviklat pochybnostmi druhých. Jakou jsi měla podporu ty?**

Čelila jsem nedůvěře u člena rodiny i od tehdejšího přítele, již v době volby vysoké školy. Doma jsem slyšela „jsi přece holka“. Expřítel mě porovnával se svým kamarádem a nevěřil mi, že na to mám. Možná to oba mysleli v dobrém. Pro mě to byl nicméně impuls „já vám ukážu“. Taky  sobě jsem chtěla dokázat, že mě podceňují neprávem. A povedlo se. Vystudovala jsem informatiku a živím se programováním. Věřte si a nevzdávejte své sny.

**V jakém momentu ti do života přišlo Junior Guru a co se pro tebe změnilo příchodem do klubu?**

Ke konci kurzu byl jeden blok věnovaný kariéře, kde lektor kromě praktických tipů k pohovoru zmínil i důležitost networkingu a členství jak na sociální síti LinkedIn, tak v různých komunitách. Představil nám i Junior Guru pro začínající programátory, a jak nám může pomoci. Do [klubu](../club.md) jsem přišla o pár měsíců později. Dodělávala jsem v té době projekt, který bych pak mohla představit na pohovoru, a potřebovala jsem nasávat další informace. Komunita mě pohltila natolik, že jsem z plánovaných tří měsíců na zkoušku členkou už přes dva roky.

**Kolik let ti trvalo než ses odhodlala začít hledat práci v IT?**

Sedm let. Zpětně však nelituji, že to trvalo tak dlouho. Vyzkoušela jsem si spoustu jiných činností, věnovala se rodině a koníčkům, pracovala jsem na sobě, nabrala zkušenosti a ve správný čas si všechno dosedlo.

**A pak už to jelo. Tři měsíce trvalo, než jsi získala práci, odpověděla jsi na osmnáct nabídek práce a zúčastnila se necelé desítky pohovorů. Jak na to vzpomínáš?**

Tři měsíce čistého času hledání. Od prvního zaslaného CV do nástupu to však trvalo půl roku. Stačilo založit si profil na LinkedIn a jobs.cz, aby mě oslovilo překvapivě velké množství personalistů. Někdy však jejich nabídky vůbec neodpovídaly mému profilu. Hledala jsem juniora v Pythonu a dostávala nabídky třeba na seniora v Javě. Takže počáteční nadšení „jak se o mě perou“ vystřídal hořký povzdech nad tím, že někteří ani nečtou, koho oslovují. Sledovala jsem nabídky v IT skupinách na Facebooku, na startupjobs.cz, projela jsem i weby velkých hráčů na trhu. Pravidelně jsem kontrolovala i „kuřebota“ na Junior Guru, který je nastaven tak, aby filtroval nabídky opravdu jen pro juniory. A pak, když se mnou nějaká nabídka opravdu zarezonovala, odpověděla jsem na ni a uložila si její obsah pro případ, že by se ozvali.

Z odeslaných osmnácti životopisů jsem dostala dvanáct odpovědí, z toho dvě rovnou zamítavé. Před každým pohovorem jsem se uklidňovala tím, že nervozita je i na druhé straně, takže hlavně klid. Hodně jsem se doptávala a docela mě překvapilo zjištění, že firmy nehledají jen vlastnosti nutně spojené s programováním. Občas přisedl i šéf týmu, který hledal dalšího komunikativního nadšence nabitého pozitivní energií. Potěšil mě lidský přístup, který mi dal naději, že pokud nemohu nabídnout tolik znalostí v programování, můžu uspět i s jinými plusy, včetně motivace a ochoty se učit. Příště bych se už tolik nepodceňovala, mnohdy ani sama firma nemá úplně jasno v tom, koho přesně chce, a rozhoduje se až o konkrétních lidech.

**Z klubového Discordu jsem vyčetla, že jednou ze zásadních otázek při pohovorech bylo, proč chceš do IT. Jak jsi na to odpovídala?**

Ano, na to se ptali všichni. Když pominu, že mě IT baví a cítím, že tam patřím, tak je to
hlavně jistá a perspektivní budoucnost. Mám kreativní, náročnou práci, která je potřebná a
užitečná, s okamžitě viditelnými výsledky. Tím, jak se IT neustále mění, pořád se budu mít co učit. Každý den se něco nového dozvím a mám možnost pracovat s nejmodernějšími technologiemi. K dalším důvodům patří rovnováha pracovního a volného času. Oceňuji flexibilitu úvazku i pracovní doby, možnost práce částečně z domu, nebo úplně remote.

**A s jakou ses setkala realitou poté, co jsi nastoupila, naplnilo to tvá očekávání?**

Jsem vděčná za to, jak hladce všechno šlo. Věděla jsem, co se bude dít, kde budu pracovat, co se ode mě čeká, jak to bude probíhat. Nastoupila jsem do jedné z vysněných firem, přijetí a podporu jsem cítila od počátku. Byla jsem přidělena na projekt, kde jsem rovnou měla navázat na práci ostatních. Měla jsem obavy, aby moje chybějící komerční praxe nebyla překážkou. Stejně jako všichni nově příchozí, i já jsem neznala prostředí, práci ani projekt. Snažila jsem se nepanikařit a postupovat systematicky. Velmi rychle jsem se naučila s většinou technologií, načerpala potřebné informace a začala přispívat.

Produkt, na kterém pracuji, a lidé z týmu, jsou za odměnu. Byli připraveni mi se vším pomoct a lidsky jsme si sedli. Nedělají se rozdíly mezi absolventem vysoké školy a rekvalifikačního kurzu. Za celou dobu jsem potkala spoustu nováčků z řad switcherů a zvlášť ti 45+ jsou důkazem, že nikdy není pozdě začít. Nemusím být denně v kanceláři, nemám striktně určenou pracovní dobu. Užívám si tu svobodu, že mohu začít pracovat podle svých možností a podle toho skončit dříve či později, pracovat večer nebo v noci. Pracuji, jak potřebuji, v tempu, které mi vyhovuje, s možností se kdykoli zastavit a na chvíli vypnout. Samozřejmě s ohledem na termín dodání. K tomu všemu je doučování a dohledávání informací žádanou a podporovanou součástí pracovního procesu. Co víc si přát? Bála jsem se zbytečně.

**Máš nějaký tip pro ty, kteří se snaží rekvalifikovat?**

Pokud nevíte, jestli je IT pro vás, zkuste to. Začněte, určitě není pozdě. Stačí tomu věnovat dvě tři odpoledne, pročíst si články, zhlédnout videa, zúčastnit se workshopu. Pokud vás něco zaujme, chyťte se toho a jděte víc do hloubky. Měli byste mít cíl, čeho chcete dosáhnout, a silnou motivaci, která vás k tomu cíli dovede. Buď si vytvořte plán pro
samostudium, nebo najděte mentora či kurz. Ať tak, nebo tak, nebuďte na to sami. Dřív nebo později oceníte zkušenosti a podporu stejně naladěných lidí. Setkala jsem se se spoustou začátečníků, kteří z různých důvodů nebyli spokojení se svou prací nebo životem a chtěli především finanční změnu ve stylu: „chci do IT kvůli penězům a je mi jedno, jestli jako tester nebo vývojář“. Já radím ujasnit si, kdo jste a co vás baví, věnovat čas zhodnocení různých možností a pak už jen vytrvat. Bude to stát hodně trpělivosti, času a disciplíny, může to bolet a neúspěchy určitě přijdou. Navíc to úsilí získáním práce nekončí, ale naopak začíná, takže pokud vás to nebude bavit už na začátku nebo v průběhu, jste na nejlepší cestě vyhořet.

**To jsou docela užitečné rady. Na Junior Guru máš stále aktivní účet. Plánuješ se více zapojovat do komunity?**

Už jsem aktivní méně, ale udržuji si přehled. Moc mě baví kanály objevů a pastí. Pak taky,
kdo co řeší za problém, a rady a návody od ostatních. Procházím různé pozvánky na
zajímavé přednášky, workshopy a akce. A odpovídám na soukromé zprávy od uživatelů, kteří z různých důvodů nechtějí psát své dotazy veřejně. Vážím si jejich důvěry.


