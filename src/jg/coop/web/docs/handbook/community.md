---
title: Jak se zapojit do programátorských komunit
emoji: 🎪
stages: [trying, preparing, applying]
description: Programátorské komunity tě dokážou posunout jako nic jiného. Kde je najít? Co od toho čekat?
template: main_handbook.html
---

{% from 'macros.html' import blockquote_avatar, illustration, lead, link_card with context %}


# Jak na programátorské komunity

{% call lead() %}
  Srazy u piva, konference, online přednášky, firemní akce, jednorázové workshopy, tematické večery.
  Programátorské komunity tě dokážou posunout jako nic jiného. Jak do nich vplout a co od toho čekat?
{% endcall %}

{{ illustration('static/illustrations/community.webp') }}

Je velmi těžké se učit zcela samostatně, bez kontaktu s dalšími samouky nebo lidmi z nového oboru. Důvodů, proč polevit, může nastat hodně. Proto je dobré pravidelně se setkávat s komunitou začínajících i pokročilých programátorů a nabíjet se tak novou energií a inspirací. Dříve existovaly hlavně dva druhy setkání: místní srazy a celostátní konference. Během covidu-19 bylo mnoho akcí zrušeno, nebo přešlo do online podoby.

{% call blockquote_avatar(
  'Vplávaj do IT komunít. Každá technológia má svoje skupiny, udalosti, konferencie, stretnutia pri pive. Zúčastňuj sa! Niekto tam má často prednášku, ale hlavne ľudia sa tam rozprávajú a stretávajú a majú joby a zákazky, chcú pomôcť, hľadajú parťáka, zamestnanca…',
  'yablko.jpg',
  'yablko'
) %}
  yablko, lektor online kurzů, ve svém [videu o tom, jak si najít praxi](https://www.youtube.com/watch?v=3-wsqhCK-wU&list=PLhB6F20C-jTPITEXEHus6fVZDfNxzRbv_)
{% endcall %}

<div class="link-cards">
  {{ link_card(
    'Klub junior.guru',
    pages|docs_url('club.md')|url,
    'Diskutuj v klubu pro začátečníky, kde najdeš pomoc, motivaci, kamarády, práci.',
    badge_icon='chat-dots',
    badge_text='Online komunita',
    class='highlighted',
  ) }}

  {{ link_card(
    'Pyvo',
    'https://pyvo.cz',
    'Poznej Python programátory ve svém okolí. Pomohou, budou tě motivovat.',
    badge_icon='calendar-week',
    badge_text='Srazy',
  ) }}

  {{ link_card(
    'Meetup',
    'https://www.meetup.com/',
    'Najdi srazy ve svém okolí, poznej různá odvětví IT, potkej lidi.',
    badge_icon='calendar-week',
    badge_text='Srazy',
  ) }}

  {{ link_card(
    'PyCon CZ',
    'https://cz.pycon.org',
    'Přijeď na českou Python konferenci.',
    badge_icon='calendar-check',
    badge_text='Konference',
  ) }}

  {{ link_card(
    'PyCon SK',
    'https://pycon.sk',
    'Přijeď na slovenskou Python konferenci.',
    badge_icon='calendar-check',
    badge_text='Konference',
  ) }}
</div>

### Nebudu mimo mísu?    <span id="beginner-friendly"></span>

Výše uvedené akce jsou vhodné i pro začátečníky a účastní se jich významné procento žen. Náplní těchto akcí jsou odborné přednášky pro různé úrovně znalostí a networking — povídání si s lidmi. Vždy se odehrávají v neformálním, pohodovém prostředí.

### Kde na to vzít?    <span id="fin-aid"></span>

Na konference je potřeba si koupit lístek. Výše zmíněné konference mají velmi dostupné lístky se slevami (např. pro studenty), ale i tak je možné, že je mimo tvé finanční možnosti se účastnit. Pro takový případ konference poskytují „Financial Aid“ — finanční pomoc s lístkem, ubytováním nebo cestou.


<!-- {#

pracovní veletrhy

--- https://discord.com/channels/769966886598737931/1214233351242776646/1214244615499022366
- kolik se sluší sníst chlebicku - nechám odpověď odborníkovi <@652142810291765248>
- dress code většinou není, takže jestli chceš za slusnaka tak svetr a rifle a jestli za pohodare tak mikinu a rifle 😀 nějaký čistý hezký
- firmy tam budou mít stánky s letacky a prospekty a tak, budou se ti snažit vysvětlit na čem delaji a kolik stravenek dávají a ze je cool pro ne pracovat
- když reknes ze jsi junior tak zachovají poker face a budou se ti snažit vysvětlit ze se ti určitě možná někdy ozvou, možná kolega Kvído, který tady zrovna neni
- ale třeba prehanim 😉 každopádně bych se na to připravil
- základ je nebát se stánku a strávit na nich maximum času a bavit se s těmi lidmi na nich
- zkus si pripravit strategii: priprav si třeba 3 otázky které jim budeš pokladat, co te zajímá o te firmě a o tom jak pracuji a koho hledají a tak
- zároveň měj něco co jim das - měj vizitku s QR kódem na svůj LinkedIn nebo něco takového, proste at si te zapamatujou, at se ti muzou ozvat a tak
- sám si ty lidi z HR a recruitmentu co je potkas na stáncích pridavej během vašich konverzaci na LinkedInu a zkus jim týden po akci (až budou mít klid) napsat do zpráv a připomenout se, i kdyby jen “chtěl bych jen podekovat za příjemný pokec na vašem stánku minuly týden, bylo to přínosné, at se daří”
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1235275845753372814
Znáte tenhle tip jak se propojovat s lidmi na akcích a jinde v terénu? https://www.linkedin.com/posts/marek-velas_linkedin-moneyphoo-edupunk-ugcPost-7190503461828878337-GLGX
---

https://blog.glyph.im/2024/05/how-to-pycon.html


--- https://discord.com/channels/769966886598737931/1288770115050934304/1290626100879163392
teď bych to asi udělala oběma způsoby, tzn. přidat na LinkedInu + nechat papírový životopis. protože když jen někoho přidáš, tak si tě ten člověk nebude pamatovat. po akcích jsem měla případy, kde mě přidalo najednou 30 lidí a já netušila kdo je kdo, což si myslím, že může být přípat recruiterů. zároveň jenom papír znamená, že na ně nemáš kontakt. takže teď bych nechala papírový životopis, přidala na LI a po několika dnech poslala zprávu s poděkováním a zeptala se, jestli se někdo už podíval na můj životopis. tím, že už mají papír, to můžou začít řešit a nečekat, až jim to pošlu a pokud to nezačali řešit, tak moje zpráva je připomene. samozřejmě oni to řešít nemusí nebo taky můžou neodpovědět, ale každým krokem si člověk zvyšuje šanci a pokud mám čas, tak lepší než nic.
---


--- https://discord.com/channels/769966886598737931/1287360897932857404/1288086857778987008
Je to sice podobné všude, ale konkétně tady:

1. od 18.00 se začnou trousit lidi, je to v kancelářích firmy, která má zároveň prostor s plátnem a projektorem, ve kterém si sedne ~50 lidí a kde je k dispozici i nějaké jídlo a pití (zdarma, platí firma), takže si můžeš něco zakousnout a seznámit se s lidmi, co už tam jsou
2. cca v 18.30 začne první přednáška, takže sedíš a koukáš a posloucháš spolu s ostatními
3. často bývá mezi přednáškama krátká pauza, využiješ na 🚽, vezmeš si ještě něco k jídlu nebo k pití/pokecáš chvíli s ostatními účastníky
4. je druhá přednáška (děláš to samé)
5. po skončení přednášek je ještě nějaká doba, kdy se zůstává ve firmě a dojídá se co zbylo a opět kecáš s účastníky
6. odchází se z kanceláří
7. ti co si ještě chtějí pokecat, jdou společně ještě do nějaké přilehlé hospody

Samozřejmě nic není povinné, můžeš kdykoli odejít podle svých možností a taky přijít, třeba později, když nestíháš. Jsou lidi, kteří po přednáškách odchází ať už proto, že to mají domů daleko nebo nemají zájem si povídat s lidmi. Na jednu stranu každého volba, ale pokud tě zajímá jen obsah přednášek, tak ho najdeš na YouTube…

Obecně doporučuju využít možnosti pokecat i kdyby to znamenalo, že hlavně posloucháš a tedy naplánovat si to tak, že nebude problém dorazit domů třeba i později.

Nepotřebuješ nic speciálního s sebou (laptop třeba), jsou to přednášky a ne workshopy, takže jen posloucháš. Je to hodně neformální, není tam dresscode nebo něco takovýho, všichni si tykají.
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1319581312666964011
Dobrý článek o tom, proč je lepší psát do veřejných kanálů a nesyslit si věci soukromně v DM nebo v uzavřených skupinkách. https://morethancoding.com/2024/12/10/build-libraries-not-vaults-minimizing-private-channels-in-slack-teams/
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1333570919507034174
- Dostaneš se na ně tak, že na ně přijdeš. 🙂
- Na některé je potřeba se předem registrovat a na některé ne.
- Otázka je spíš jak se o nich dozvědět, můžeš třeba hned tady v klubu ve skupinách podle měst:<#1296383796727386132> <#1296508522451832853> <#1296486471670304878> <#1296425496141107221>můžeš hledat taky na https://www.meetup.com/, kde ale určitě nejsou všichni. Taky se o tom můžeš dozvědět ze sociálních médií.
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1333572790984638464
- Typicky je to sraz na nějaké téma (Python, Frontend, AI, …), který organizuje buď někdo nezávislý nebo firmy.
- Konají se nejčastěji buď v kanclech nějaké firmy (často s občerstvením placeným firmou) nebo někde v hospodě.
- Obvykle je to ve všední den večer.
- Pokud jsou pravidelné, což je asi většina, tak frekvence bývá měsíc nebo více.
- Program se většinou skládá z nějakých přednášek a následné „volné zábavy“, kdy není žádný program, ale můžeš s lidma mluvit a to nejen těma, který znáš, ale počítá se s tím, že tam právě i nový lidi poznáš.
---


--- https://discord.com/channels/769966886598737931/1296486471670304878/1347166489643585569
Ten LI v mobilu je perfektní věc. Chodil jsem furt otevřeným displejem, na kterém svítil QR kód a lidi si samí říkali o toto duchovní propojení.
---


--- https://discord.com/channels/769966886598737931/1351222802296082588/1353734627369422898
No a c# má Update Conference (https://www.updateconference.net/cs) a TechEd atd. což podle mě jsou větší akce než ta Java v Čechách možná 🙂
---


--- https://discord.com/channels/769966886598737931/1351222802296082588/1353735180111708280
A jeste jsem zapomněl na https://wug.cz - to je free , ale Brno 🙂
---


--- https://discord.com/channels/769966886598737931/1410161605232033832/1418565767108104243
> nyní jsem začal chodit na offline akce, kde vidím, že jsou tam lidi stejně hloupý jako já a cítím se lépe
To je skvělý, to si uložím 😂
---


--- https://discord.com/channels/769966886598737931/1296508522451832853/1411973029583519815
Frontendisti nebo Pyvo většinou probíhají tak, že přijdeš, je nějaký čas na rozkoukání, objednání něčeho co chceš jíst/pít (pokud to není zrovna v nějaké firmě, to tam pak bývá catering, nebo aspoň pizza), pak začnou přednášky, na srazech bývají tak dvě tři, mezitím pauzy, a pak to skončí a je volná zábava, kdy se lidi zakecají mezi sebou.
---


#} -->
