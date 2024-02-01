---
title: Jak získat praxi v programování
emoji: 🛠️
thumbnail_title: Jak získat praxi v programování
description: "Znáš základy? Tvým úkolem jsou nyní dvě věci: Získat alespoň minimální praxi a dál si rozšiřovat znalosti."
template: main_handbook.html
---

{% from 'macros.html' import blockquote_avatar, lead, link_card, links_note, note with context %}


# Získej praxi v programování

{% call lead() %}
  Znáš [základy](learn.md)? Tvým úkolem jsou nyní dvě věci: Získat alespoň minimální praxi a dál si rozšiřovat znalosti. Teprve potom si můžeš začít [hledat svou první práci v IT](candidate.md).
{% endcall %}


## Procvičuj    <span id="exercises"></span>

<div class="link-cards">
  {{ link_card(
    'Exercism',
    'https://exercism.io/',
    'Řeš malé úlohy, dostaň zpětnou vazbu od mentora, uč se z řešení druhých.'
  ) }}

  {{ link_card(
    'Codewars',
    'https://www.codewars.com/',
    'Řeš malé úlohy přímo v prohlížeči, uč se z řešení druhých.'
  ) }}

  {{ link_card(
    'CheckiO',
    'https://checkio.org/',
    'Procházej online hru pomocí programovacích úloh, uč se od druhých.'
  ) }}

  {{ link_card(
    'Umíme programovat',
    'https://www.umimeprogramovat.cz',
    'Uč se skrze cvičení a opakování, <a href="https://www.umimeto.org/podlozeno-vyzkumem">podložený výzkumy</a>.'
  ) }}

  {{ link_card(
    'HackerRank',
    'https://www.hackerrank.com',
    'Soutěž řešením zapeklitých úloh. Propojeno s nabídkami práce.'
  ) }}

  {{ link_card(
    'Project Euler',
    'https://projecteuler.net/',
    'Řeš matematické úlohy pomocí programování.',
    badge_icon='calculator',
    badge_text='Pro matematiky',
  ) }}
</div>

{{ links_note() }}


## Najdi si projekt    <span id="projects"></span>

Nic tě nenaučí tolik, jako když si zkusíš něco samostatně vyrobit. Říká se tomu [projektové učení](https://cs.wikipedia.org/wiki/Projektov%C3%A9_u%C4%8Den%C3%AD). Nejlepší je vymyslet si něco vlastního a řešení procházet s [mentorem](#najdi-si-mentora). Inspirace na projekt se nejlépe hledá přímo okolo tebe:

*   Jednoduchá hra, např. piškvorky nebo [had](https://naucse.python.cz/2018/snake-brno/),
*   automatizace něčeho, co teď na počítači musíš dělat ručně (mrkni na [tuto knihu](https://automatetheboringstuff.com)),
*   program na procvičování příkladů nebo slovíček pro děti do školy,
*   [osobní webová stránka](candidate.md#osobni-web-a-blog).

Pokud vlastní nápad nepřichází a mentor není po ruce, můžeš zkusit [hackathon](#zkus-hackathon) nebo [open source](#zkus-open-source).

{% call blockquote_avatar(
  'Junioři si často udělají kurz, certifikaci, ale potom už tu znalost neprocvičují. A to je strašná škoda, protože ji do pár měsíců zapomenou. Lepší méně kurzů, ale potom začít praktikovat a něco si vytvořit. Nákupní seznam, jednoduchého bota, malou aplikaci.',
  'jiri-psotka.jpg',
  'Jiří Psotka'
) %}
  Jiří Psotka, recruiter v [Red Hatu](https://red.ht/juniorguru) v [prvním dílu podcastu junior.guru](../podcast/1.jinja)
{% endcall %}


## Osvoj si Git a GitHub    <span id="git-github"></span>

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }} Z této kapitoly je teď samostatná stránka: [Git a GitHub](git.md)
{% endcall %}

## Najdi si mentora    <span id="mentors"></span>

Mentor ti pomůže s věcmi, se kterými si samostatně nevíš rady. Nemusí to být vyloženě mistr v oboru, stačí když bude v programování alespoň o něco zkušenější než ty. A klidně může stačit, když se uvidíte jednu hodinu týdně přes videohovor. Pokud znáš někoho, kdo by mohl být tvým mentorem, ale nemá s tím praktické zkušenosti, projděte spolu [přednášku o mentorování](https://github.com/honzajavorek/become-mentor/blob/master/cs.md#readme) a prostě to zkuste!

<div class="link-cards">
  {{ link_card(
    'Coding Coach',
    'https://mentors.codingcoach.io/',
    'Mentoři z celého světa, kteří nabízí své služby zdarma.'
  ) }}

  {{ link_card(
    'Codementor',
    'https://www.codementor.io/',
    'Profesionální, placení mentoři z celého světa.'
  ) }}

  {{ link_card(
    'Mentoring na robime.it',
    'https://robime.it/mentoring-program-robime-it/',
    'Slovenský mentoringový program.'
  ) }}

  {{ link_card(
    'ReactGirls Mentoring',
    'https://reactgirls.com/mentoring',
    'Mentoringový program pro ženy zajímající se o webový frontend.',
    badge_icon='gender-female',
    badge_text='Pro ženy',
  ) }}

  {{ link_card(
    'Femme Palette',
    'https://www.femmepalette.com/mentoring-for-women-it',
    'Český program placeného mentoringu pro ženy.',
    badge_icon='gender-female',
    badge_text='Pro ženy',
  ) }}

  {{ link_card(
    'PyWorking Sessions',
    'https://pyworking.cz/',
    'Zastav se na pravidelná setkání začátečníků, kde jsou i koučové.'
  ) }}

  {{ link_card(
    'GISMentors',
    'https://gismentors.cz/',
    'Mentoři, kteří učí využívaní programování v geografii.'
  ) }}
</div>


## Zkus „hackathon“    <span id="hackathons"></span>

[Hackathon](https://cs.wikipedia.org/wiki/Hackathon) je akce, kde se sejdou lidi se zájmem o nějaké téma, utvoří smíšené týmy (zkušení i začínající programátoři, designéři) a v daném čase vymyslí a zpracují nějaké řešení. Nejlepší někdy dostanou ceny. Pro lepší představu si přečti [článek od účastnice Michaely](https://medium.com/@misasebestova/m%C5%AFj-prvn%C3%AD-datov%C3%BD-hackathon-6f753a4730cf).

<div class="link-cards">
  {{ link_card(
    'Hackathony v Česku',
    'https://www.facebook.com/groups/hackathony.cz/',
    'Největší koncentrace tipů na hackhathony v Česku.
        <small>Někdy ale může být nejlepší prostě
        <a href="https://www.google.cz/search?q=hackathon%20ostrava">hledat</a>.
        </small>'
  ) }}

  {{ link_card(
    'Hackathony - co a jak',
    'https://docs.google.com/presentation/d/1reYrzFy3E3LS-jNzQecLbkf6Qq7iIEjWvXCyvbw389E/',
    'Všechny základní informace o hackathonech na jednom místě.'
  ) }}
</div>

{% call blockquote_avatar(
  'Moji největší bariérou byl strach. Obava, že nebudu tak dobrá jako ostatní a že tam budu úplně mimo. Nakonec jsem zjistila, že to bylo úplně zbytečné.',
  'michaela-sebestova.jpg',
  'Michaela Šebestová',
) %}
  Michaela Šebestová, absolvetnka kurzu [PyLadies](https://pyladies.cz/) a [účastnice hackhatonu Sreality.cz](https://medium.com/@misasebestova/m%C5%AFj-prvn%C3%AD-datov%C3%BD-hackathon-6f753a4730cf)
{% endcall %}


## Zkus „open source“    <span id="opensource"></span>

[Open-source software](https://cs.wikipedia.org/wiki/Otev%C5%99en%C3%BD_software) (OSS) jsou projekty s kódem, na který se může kdokoliv podívat, a které lze většinou využívat zdarma — například [Linux](https://cs.wikipedia.org/wiki/Linux) nebo [LibreOffice](https://cs.wikipedia.org/wiki/LibreOffice). Pokud si [dáš svůj projekt na GitHub](git.md), kde jeho kód mohou číst další lidé, máš taky takový maličký open source. I tyto webové stránky [jsou open source](https://github.com/juniorguru/junior.guru).

Existují tisíce open source projektů uveřejněných pro dobro všech, některé více či méně užitečné, některé vytvářené ve volném čase lidí, jiné zaštiťované organizacemi. Je to obrovský fenomén a když se do něj člověk zapojí, může získat mnoho zkušeností, cenných kontaktů i nových přátel.

### Nemusíš jen programovat    <span id="not-only-coding"></span>

Open source není jen o programování. Pokud se zatím necítíš na psaní kódu, [je i hodně jiných způsobů, jak můžeš přiložit ruku k dílu](https://opensource.guide/how-to-contribute/#what-it-means-to-contribute). Např. psaním dokumentace, psaním článků, navrhováním grafiky nebo „procházením GitHub Issues“ (anglicky _triaging_, hezky popsáno v článku [How to fix a bug in open source software](https://opensource.com/life/16/8/how-get-bugs-fixed-open-source-software)).

### Open source jako inspirace    <span id="open-source-inspiration"></span>

Do open source nemusíš hned přispívat. Ze začátku se můžeš hodně naučit i pouhým pozorováním, čtením cizího kódu, hledáním inspirace. Můžeš se např. podívat, [jak jiní lidé naprogramovali piškvorky v Pythonu](https://github.com/search?l=Python&q=tic-tac-toe).

### Jak začít?    <span id="how-to-start"></span>

Začátky s open source nejsou přímočaré. Většinou na něm lidé pracují ve volném čase. Nováčci jsou vítáni, ale jen málo projektů má sílu aktivně nabízet [mentorování](#najdi-si-mentora). Nejsnazší cesta vede přes různé programy a stáže, jako např. [Google Summer of Code](https://summerofcode.withgoogle.com/), ale nejčastěji se lidé k open source dostanou posloupností „vidím rozbitou věc, spravím, pošlu opravu“.

{% call blockquote_avatar(
  'Stáž na veřejném softwarovém projektu přes Outreachy mi změnila život. Učící křivka byla strmá, ale pomoc komunity kolem projektu byla ohromná. Naučila jsem se všechny běžné postupy, jak se co správně dělá, jak se komunikuje.',
  'lenka-segura.jpg',
  'Lenka Segura',
) %}
  Lenka Segura v [rozhovoru pro CyberMagnolia](https://cybermagnolia.com/blog/lenka-segura-interview/), bývalá agrochemička
{% endcall %}

{% call blockquote_avatar(
  'Moje začátky se nesly v duchu: Vidím rozbitou věc, spravím, pošlu opravu. Tím si člověk vybuduje jméno. Stačí jen otevřít GitHub, všechno je rozbitý.',
  'tomas-janousek.jpg',
  'Tomáš Janoušek',
) %}
  Tomáš Janoušek, profesionální programátor, ve [svém tweetu](https://twitter.com/Liskni_si/status/1224359360517877762)
{% endcall %}

<div class="link-cards">
  {{ link_card(
    'Open Source Guides',
    'https://opensource.guide/',
    'Přečti si vše o tom, jak OSS funguje, a jak začít.'
  ) }}

  {{ link_card(
    'Česko.Digital',
    'https://cesko.digital/',
    'Přidej se do sdružení dobrovolníků okolo OSS projektů s pozitivním dopadem na Česko.'
  ) }}

  {{ link_card(
    'GISMentors',
    'https://gismentors.cz/',
    'Účastni se kurzů nebo školení na OSS související s geografií.'
  ) }}

  {{ link_card(
    'Outreachy',
    'https://www.outreachy.org/',
    'Získej stáž na OSS pro znevýhodněné skupiny.',
    badge_icon='door-open',
    badge_text='Pro znevýhodněné',
  ) }}

  {{ link_card(
    'Google Summer of Code',
    'https://summerofcode.withgoogle.com/',
    'Pracuj na OSS při studiu, během letních prázdnin.',
    badge_icon='pen',
    badge_text='Pro studenty',
  ) }}

  {{ link_card(
    'Google Code-in',
    'https://codein.withgoogle.com/',
    'Účastni se úvodu do OSS pro mládež, vyhraj ceny.',
    badge_icon='pen',
    badge_text='Pro studenty',
  ) }}

  {{ link_card(
    'Rails Girls SoC',
    'https://railsgirlssummerofcode.org/',
    'Přihlaš svůj tým a po několik měsíců pracuj na OSS.',
    badge_icon='gender-female',
    badge_text='Pro ženy',
  ) }}

  {{ link_card(
    'CodeTriage',
    'https://www.codetriage.com/',
    'Najdi rozbitou věc, oprav ji, pošli opravu autorům.'
  ) }}

  {{ link_card(
    'Awesome OSS Mentors',
    'https://github.com/lenadroid/awesome-oss-mentors#readme',
    'Kontaktuj někoho z těch, kdo se sami nabízí zaučovat nováčky na OSS projektech.'
  ) }}
</div>

{{ links_note() }}


## Rozšiřuj si znalosti    <span id="skills"></span>

Umět programovat např. v Pythonu je dobrý základ, ale pro plnohodnotnou práci to nestačí. S prvními pokusy se uplatnit zjistíš, že by se ti hodilo aspoň trochu znát Git, HTML, SQL, JavaScript, … Pro každou takovou technologii existují kurzy, workshopy, knihy.

Vždy, když narazíš na nový pojem nebo zkratku, přečti si alespoň co to je a k čemu se to používá. Pokud o tom uslyšíš poněkolikáté, zkus si najít víc a pochopit základy.

### Základy    <span id="basics"></span>

<div class="link-cards">
  {{ link_card(
    'BaseCS',
    'https://medium.com/basecs',
    'Základy informatiky od <a href="https://twitter.com/vaidehijoshi">Vaidehi Joshi</a>.
        Existuje i jako
        <a href="https://dev.to/vaidehijoshi/linked-lists--basecs-video-series--2le8">video</a>
        a
        <a href="https://www.codenewbie.org/basecs">podcast</a>.'
  ) }}

  {{ link_card(
    'MIT: The Missing Semester',
    'https://missing.csail.mit.edu/',
    'Úvod do všeho možného, co se ti bude v začátku hodit. Příkazová řádka, Git, editor…'
  ) }}
</div>


### Kde hledat kurzy a workshopy?    <span id="courses"></span>

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }} Z této kapitoly je teď samostatná stránka: [Kurzy](../courses.md)
{% endcall %}


## Najdi inspiraci, poznej lidi    <span id="events"></span>

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

  {{ link_card(
    'Write The Docs Prague',
    'https://www.writethedocs.org/conf/',
    'Přijeď na konferenci o psaní technické dokumentace.',
    badge_icon='calendar-check',
    badge_text='Konference',
  ) }}
</div>

### Nebudu mimo mísu?    <span id="beginner-friendly"></span>

Výše uvedené akce jsou vhodné i pro začátečníky a účastní se jich významné procento žen. Náplní těchto akcí jsou odborné přednášky pro různé úrovně znalostí a networking — povídání si s lidmi. Vždy se odehrávají v neformálním, pohodovém prostředí.

### Kde na to vzít?    <span id="fin-aid"></span>

Na konference je potřeba si koupit lístek. Výše zmíněné konference mají velmi dostupné lístky se slevami (např. pro studenty), ale i tak je možné, že je mimo tvé finanční možnosti se účastnit. Pro takový případ konference poskytují „Financial Aid“ — finanční pomoc s lístkem, ubytováním nebo cestou.


## Neflákej angličtinu    <span id="english"></span>

**Bez angličtiny se neobejdeš.** Je to klíč ke dveřím do celého světa. Vybíráš ze dvou českých mentorů, ze tří českých online kurzů? S angličtinou vybíráš ze stovek mentorů a desítek kurzů. **Nedostatečná angličtina je v IT jako bolavý zub.** Chvíli s ním vydržíš, ale když to nezačneš řešit včas, budeš hodně litovat. Nauč se ji aspoň pasivně — pokud zvládáš číst anglický text, pochopit v něm zadání a učit se z něj nové věci, pro start to stačí.

<div class="link-cards">
  {{ link_card(
    'Jak se opravdu naučit anglicky',
    'https://www.youtube.com/watch?v=Xt7QIgzyxLk',
    'Praktický návod jak <strong>opravdu</strong> začít od <a href="https://www.youtube.com/user/BBSobotka">Broni</a>.'
  ) }}

  {% call link_card(
    'Jak si zlepšit angličtinu?',
    pages|docs_url('handbook/learn.md')|url + '#jak-si-zlepsit-anglictinu',
  ) -%}
    Nauč se anglicky podle tipů na junior.guru.
  {%- endcall %}
</div>


<!-- {#

algoritmy http://jeffe.cs.illinois.edu/teaching/algorithms/

https://www.manning.com/books/grokking-algorithms

DOM events https://domevents.dev/

assumptions, predpoklady - https://medium.com/@peter.hozak/krkolomn%C3%A9-predpoklady-6f658f552de4

Hafo se řeší jak odinstalovat Linux k Windows

teoreticka informatika - https://bigmachine.io/products/the-imposters-handbook/ a https://en.wikipedia.org/wiki/The_Pragmatic_Programmer

network programming https://beej.us/guide/bgnet/html/

MARKDOWN JAK FUNGUJE, ANALOGIE
Je to jako když jsi autor knihy a píšeš článek na psacím stroji - když chceš někde udělat nadpis, použiješ k tomu # apod. nebo to podtrhnes, když chceš udělat caru, tak uděláš spoustu - za sebou. Pak ten papír das vydavateli a tam to vezme sazeč a udělá z toho pěknou barevnou knihu. Tak Markdown je ten psací stroj a sazec je jakýkoliv program, který bere MD (strojopis) a produkuje HTML (barevnou knihu)
Jako autor mas na barvu obálky a font nadpisu v knize minimální nebo zcela žádný vliv
Ale můžeš dat sazeči vědět, kde je nadpis a kde je seznam

https://12factor.net/

https://www.freecodecamp.org/news/what-is-web-development-how-to-become-a-web-developer-career-path/

Learn learn learn loop
https://twitter.com/OzolinsJanis/status/1420344259367030784

koľko HODÍN DENNE musím PROGRAMOVAŤ? (programátor radí) https://www.youtube.com/watch?app=desktop&v=LG-d_BOZE6k

https://www.facebook.com/groups/pyonieri/posts/5247478988597569/?comment_id=5249157481763053&reply_comment_id=5249165655095569
Teď měj radost, že jsi to nakonec vyřešil 💪 Netrap se tím, že to bylo obtížné. To znamená, že ses u toho hodně naučil. Pokud je to tvůj první pokus aplikovat naučené znalosti na praktickém projektu, není divu, že to šlo obtížně, protože tohle, to přemýšlení kolem toho, rozsekávání problému na podproblémy, debugování, apod., tohle je na celém tom programování to ono, co je největší skok od laika a sledovače tutoriálů k člověku, který dokáže něco reálně naprogramovat.
Mnoho lidí jen točí tutoriály a diví se, že pak nic nedokážou vytvořit. Ty už jsi dál! 🙂
A neboj, už třeba za měsíc se na ten svůj teď těžce vydřený kód budeš dívat a zasměješ se mu.


univerzální technologie, které potřebuješ všude https://twitter.com/vboykis/status/1451985733867216898

https://exercism.org/tracks/python/concepts
https://www.codecademy.com/code-challenges

nandtetris https://www.nand2tetris.org/

https://ivet1987.wz.cz/2020/03/koucovani-na-pyladies-kurzech/

https://regexcrossword.com/
https://refrf.dev/

UX - https://www.designui.cz/hledame-designera
UX http://www.asociaceux.cz/zacinate-s-user-experience

challenge https://www.trywilco.com/

fyzika, animace v javascriptu - https://thecodingtrain.com/, https://natureofcode.com/

matika pro vyvojare https://youtu.be/bOCHTHkBoAs

zaklady bezpecnosti - odkazy na dobre veci jsou na poslednim slajdu kayly prednasky pro klub

data science - My "data science is different now" post has Data Reddit asking questions already answered by my post.
https://twitter.com/vboykis/status/1419302245854818306

https://nemil.com/categories/notes-to-a-young-software-engineer/

- Tereza podcast skvela citace na vliv a výhody komunit
- https://www.pythonistacafe.com/

https://www.mjt.me.uk/posts/falsehoods-programmers-believe-about-addresses/

testování - Pánek má spoustu materiálů k automatizaci: https://www.youtube.com/watch?v=OnpOwlp8Hrg&list=PLZaZq-LUymhx3Lip30OGmsMPdAVoNl45i&index=5

Tak mě napadá, jestli by zdejší mozkový trust nedokázal dát dohromady typická spojení obor + programovací jazyk. Ve smyslu v jakém jazyce se nejčastěji programuje v konkrétních oborech. To by bylo další ze skvelých vodítek pro switchery, když se rozhodují, do jakého jazyka se pustit.
Už jsem tady ten hypreskill.org (od JetBrains) dával víckrát, mám pocit, že to tam celkem mají. Je nutno si kliknout na *open original*, je to dost velkej screenshot…  (rozbalil jsem na ukázku OOP)

Zkus hyperskill.org od JetBrains. Jsou tam algoritmy, matika, obecny veci (kamarad s nedostudovanym matfyzem a dostudovanym Bc. na CVUT FIT rikal, ze mu prijde, ze je tam toho az az co se tyka tech algoritmu a matiky, takze bych se netyral se vsim, ja to bohuzel neposoudim, sem v tomhle pastevec). A myslim, ze by mohl byt nejakej trial mesicni nebo tak neco, abys videl, ze to stoji za to nebo ne.

Zmínit Sifrovacky jako způsob jak si s tím hrát ve volném case

Complete Introduction to the 30 Most Essential Data Structures & Algorithms - DEV
https://dev.to/iuliagroza/complete-introduction-to-the-30-most-essential-data-structures-algorithms-43kd

https://dr-knz.net/programming-levels.html
CEFR https://www.linkedin.com/feed/update/urn:li:activity:6832917085660725248/?commentUrn=urn%3Ali%3Acomment%3A(activity%3A6832917085660725248%2C6832968938511458304)
CEFR Radek Holý
Už se to potřetí snažím přečíst celý, ale nemám na to morál. Nicméně ty kusy, co jsem viděl, vypadaj super. Moc se mi to líbí.
Jen mám pocit, že tam chybí totéž, co řešíme i u nás ve firmě. Soft skills. Jo, je to takový zaklínadlo, ale ukazuje se, že tak nějak podvědomě člověk bere v potaz při povyšování i tuhle stránku. Hlavně co se týče týmové spolupráce a komunikace s klientem/businessem. To v té tabulce zohledněné nevidím.

https://naucse.python.cz/2020/linux-admin/
https://www.edx.org/course/fundamentals-of-red-hat-enterprise-linux

Toto je na procvičení úplně nej: https://ksi.fi.muni.cz/ a nejlepší Python videa má na YouTube Corey Schafer.

https://wizardzines.com/comics/

Prozkoumat tohleto od Radka - https://www.codingame.com/start

https://codingcompetitions.withgoogle.com/codejam
https://adventofcode.com

testování - co to je https://www.youtube.com/watch?v=LQcKWKJ68ps
testování jak na to - https://discord.com/channels/769966886598737931/788826407412170752/884384772669972481

jak na security https://discord.com/channels/769966886598737931/769966887055392768/897087048110997584

8-Bits of Advice for New Programmers (The stuff they don't teach you in school!) https://www.youtube.com/watch?v=vVRCJ52g5m4

Objektove programovani v pythone https://www.youtube.com/playlist?list=PLITREQqtwnOkN5VZv-pD3vm7eBDp7zVcn

Data a social justice https://ehmatthes.github.io/pcc_2e/challenges/coding_for_social_justice/
samizdat

https://wiki.provyvojare.cz/

I am of the opinion that every developer needs to have a solid foundation in computer science/IT
to be successful. If you're a bootcamp or self taught developer, take the time to learn CS concepts like how CPUs,OSes, memory, filesystems, & networks  work, you'll be better for it
https://twitter.com/terrameijar/status/1309999684413521921

PETR A ALGORITMY
- Jak by sis to vlastne teda konkretne predstavoval? Kdyz potkam nekoho, kdo by chtel o algoritmech neco vedet, mam ho poslat za tebou s tim, ze chces vytvorit materialy na toto tema nebo ze je to naucis?
- Můžeš, nebo jen dej vědět že je zájem. Od juniorů nebo i z druhé strany – kdyby si někdo stěžoval že to junioři z JG neumí.

Skills
https://github.com/juniorguru/junior.guru/issues/3

SQL
Především toto: http://sqlzoo.net a případně http://www.w3schools.com/sql/trysql.asp?filename=trysql_select_all
https://mail.google.com/mail/u/0/#inbox/FMfcgxwDrlfqmHRzCLJsKHHFDHbbwrJF

design systems
https://adele.uxpin.com/
http://styleguides.io/

The Most Important Non-Programming Skills for Programmers
https://welearncode.com/most-important-nonprogramming/

proč třídy
https://www.reddit.com/r/learnpython/comments/f0ir0x/i_have_a_demon_i_consider_myself_a_decent_python/?utm_source=share&utm_medium=ios_app&utm_name=iossmf

pridat neco o data analyticich? https://veekaybee.github.io/2019/02/13/data-science-is-different/

linux kernel https://linux-kernel-labs.github.io/refs/heads/master/index.html

Máme selektuju.cz a jakpsatsql.cz ale je to zatím stavěný na snowflake s predpripravenyma datama a dost punkový. Asi by tam šel přidat návod, jak data v trialce naimportovat.
https://github.com/czechitas/da-data-jakpsatsql

CZECH TESTERS GROUP (Prague, Czech Republic)
https://www.meetup.com/ProfessionalTesting/

https://regex101.com/

API - Frontend backend apis https://discord.com/channels/769966886598737931/788826407412170752/916448465817600001

JAK SE NAUČIT JINÝ JAZYK - CELÁ NOVÁ STRÁNKA
přidávám cheat sheet, který porovnává syntaxy pythonu a JS, což člověku dá rychlý náhled jak něco napsat v JS (nebo obráceně). https://github.com/LambdaSchool/CS-Wiki/wiki/Javascript-Python-cheatsheet a https://sayazamurai.github.io/python-vs-javascript/
learn x in x minutes https://twitter.com/nbashaw/status/1187779382628081664

Data science playground https://www.kaggle.com/

Knihy https://learntocodewith.me/posts/programming-books/

JAK SI VYBRAT JAZYK
Ptáš se, jaké auto je nejlepší na to, aby ses naučil řídit. Odpověď je, že nejlepší je jakékoliv, které můžeš zkoušet řídit a nejlépe takové, ve kterém ti to půjde dobře a bude tě to bavit.
Odpověď je, že je jedno, jaký programovací jazyk si vybereš, pokud tě bude bavit a pokud tě napadá, co si v něm pro sebe vytvoříš jako první projekt. Klidně PHP nebo HTML, pokud to má být webovka, klidně C#, pokud hra, je to jedno. Jestliže vůbec nevíš, tak si vyber Python, protože je to dobrá univerzální první volba, dobře se učí a používá se v mnoha oborech, takže si můžeš vybrat později, kdy už tomu budeš lépe rozumět.
Ptáš se, jaké auto je nejlepší na to, aby ses stal profi řidičem. Jenže profi řidičů je spousta druhů a my nevíme, co budeš chtít potom dělat. Řídit autobus (MHD řidič), kamion (mezinárodní dopravce), motorku (kurýr), limuzínu (řidič a bodyguard v jednom 　 )? Každé z toho bude vyžadovat trochu jinou praxi.
Odpověď je, že každý jazyk se hodí na něco trochu jiného. Pokud jsi si jistý, že chceš profesionálně programovat mobilní aplikace, asi nemá smysl ti doporučovat něco jiného, než Kotlin (Android) nebo Swift (iOS). Pokud si ničím tak úplně jistý nejsi, tak si vyber Python, protože je to dobrá univerzální volba, používá se v praxi v mnoha oborech, takže se i pouze s ním (dokonce bez znalosti HTML a dalších) lze uplatnit a najít si svou první práci. Každý další programovací jazyk pro tebe už bude snazší se naučit, takže pokud nevíš, moc to neřeš, v budoucnu se snadno cokoliv doučíš nebo přeučíš, až vědět budeš.
Víc o tom píšu tady: https://junior.guru/learn/

https://www.learnpython.org/
https://github.com/ronreiter/interactive-tutorials

Nauč sa matiku
https://www.elea.sk/
Elea je historicky prvý projekt s matematickými výukovými videami v SR a ČR. Nájdete tu kvalitné a zrozumiteľné materiály úplne zdarma.

My Favorite Free Resources for New Programmers
https://welearncode.com/favorite-free-resources/

The OSSU curriculum is a complete education in computer science using online materials. It's not merely for career training or professional development. It's for those who want a proper, well-rounded grounding in concepts fundamental to all computing disciplines, and for those who have the discipline, will, and (most importantly!) good habits to obtain this education largely on their own, but with support from a worldwide community of fellow learners.
https://github.com/ossu/computer-science

Podobný cíl jako OSSU má i "Teach Yourself Computer Science". Slovy autorů: "You don’t need yet another “200+ Free Online Courses” listicle. You need answers to these questions: Which subjects should you learn, and why? What is the best book or video lecture series for each subject? This guide is our attempt to definitively answer these questions." https://teachyourselfcs.com/

Parádní příspěvek o algoritmech
https://discord.com/channels/769966886598737931/769966887055392768/906583738140467271

Unity
Za uložení na později stojí i Brackeys na YT. Kanál narvanej úplně vším co tě okolo tvorby her v Unity napadne. K prasknutí. Má pak i discord komunitu, početnou a aktivní. https://www.youtube.com/c/Brackeys

Morsels exercise
https://twitter.com/obiskywalker/status/1278665773523898368

Kateřina Shine Churanová Kniha Fluent Python od O'Reilly. Asi nejlíp zpracovaná učebnice Python pro pokročilé.

sítě
https://www.libordos.eu/Prednasky/

If you want to start learning Python programming with a focus on data analysis (for journalism) this is the best starter course I've ever encountered https://t.co/jkmx3tjAM3— Simon Willison (@simonw) March 21, 2020
https://twitter.com/simonw/status/1241403850788982784

This is a series of books diving deep into the core mechanisms of the JavaScript language. This is the second edition of the book series:
https://github.com/getify/You-Dont-Know-JS

deeplearning
https://www.facebook.com/groups/pyonieri/permalink/3292652264080261/
https://deeplizard.com/learn/playlist/PLZbbT5o_s2xq7LwI2y8_QtvuXZedL6tQU
https://www.mff.cuni.cz/en

datovy povolani - Kokes:
ty role se rok od roku mění, ale ta nějak dlouhodobě to vnímám takhle- data analyst - tohle vzniká z těch různých digitálních akademií, databázovejch tréninků atd., zejména deskriptivní analýzy, reporting atd.
- data scientist - taková všehochuť, všichni to chtěj, nikdo neví co to vlastně je, a každej kdo prošel jednou Kaggle competition si to píše do CV
- data engineer - infrastrukturní/orchestrační support pro ty dvě role výše - moc firem je nemá, často jsou (částečně) nahrazovaný nějakou službou/infrastrukturou/kontraktoremco se týče hlášení - tak na analysty se hlásí juniornější lidi, kteří se chtěji dostat do oboru, na scientisty se hlásí skoro všichni a na engineery skoro nikdo
https://gist.github.com/kokes/49ca2f42edf30d6a1f02e3859ad3f9f2

https://www.fullstackpython.com/

Alois Tomasek za me nejlepsi zdroj kterej rad davam je tenhle https://krokodata.vse.cz/ .... k pochopeni SQL je dobry odkaz treba O modelování -> tutorial analyzy -> vztahy

The old age problem of junior sysadmin or programmer pic.twitter.com/OALNV1Xgij— The Best Linux Blog In the Unixverse (@nixcraft) November 26, 2018
https://twitter.com/nixcraft/status/1066903824634384386

MeetUp-ing like a Boss
https://medium.com/le-wagon/meetup-ing-like-a-boss-1a4493d75fa6

Mapa technologií
https://discord.com/channels/769966886598737931/811910782664704040/847778860928860170

OOP bez blbostí
https://www.reddit.com/r/learnpython/comments/lkaffj/looking_for_a_tutorial_on_classes_that_isnt_about/?utm_source=share&utm_medium=ios_app&utm_name=iossmf

DNS, sítě https://twitter.com/simonw/status/1364356791954366464

nejlepsi kurz na OS https://www.udacity.com/course/introduction-to-operating-systems--ud923

Jak vysvětlit OOP https://www.reddit.com/r/learnprogramming/comments/m6yb5z/how_would_you_explain_what_object_oriented/

design patterns overused
https://twitter.com/ericnormand/status/1364595203420479494
https://trello.com/c/eSNJQTCe/2273-design-patterns
K návrhovým vzorům – rozdělil bych je takto 🙂  - takové, na které selským rozumem přijdete (např. zmíněný adapter), ale je fajn mít nějakou terminologii (a bohužel i buzeraci na pohovorech). - pak takové, které řeší nějaký konkrétní problém v konkrétním jazyce (typicky Java, C++), a třeba nedávají smysl v Pythonu - např. singleton - a vzory, které vám pomohou vyřešit nějaký hlubší problém a selským rozumem byste na ně přicházeli dlouho nebo by vás ani nenapadlo je použít - dataloader, data mapper, unit of work, activerecord, idempotence, immutable typy, job queue...

Junior frontend CLI:  hlavně se toho nebát, za mě tohle (+-): ls, pwd, cd, mkdir, touch, ls -a, ls -l, ls -alt (jako ukázka kombinace parametrů), cp, mv, rm, *, ** (globstar), >, |, sort, grep, doplňování, historie příkazů a hledání v historii + základní použití gitu na CLI, curl, bash profile

dataři https://www.kaggle.com/ plus pripnute odkazy na diskuzi
https://discord.com/channels/769966886598737931/769966887055392768/836998750182047804

debata o čistém kódu
https://discord.com/channels/769966886598737931/789107031939481641/838469696663322625

Certifikát PCAP
https://www.facebook.com/groups/pyonieri/posts/4377451915600285/

VYSVĚTLIT KONCEPT SLOŽEK A ADRESÁŘŮ A PROJEKTŮ, META JAKOŽE
Já právě v tom roce 2017, jeden den dělali jednoduchou HTML stránku (index.html) a když sem druhej den řekl: otevřete si tu stránku a budeme pokračovat, tak byl problém.
„Nevím kde to je“. Protože při vytváření vůbec nemyslela na lokaci, prostě se to udělá a je to. A pak to dala do spotlightu… index.html je na MacOS zjevně dostkrát…
https://www.theverge.com/22684730/students-file-folder-directory-structure-education-gen-z


--- https://discord.com/channels/769966886598737931/769966887055392768/1106993630209638500
ahoj, mam dotaz, nevim jestli bych to měl psát do poradny, ale já se v těch kategoriích tak nevyznám :

MATEMATIKA pro Developery?
Takže, jsem spokojeně zaměstnanej rok mám víc peněz a nějak stíhám (takže pohoda) a uvažuju o tom že bych ve volném čase kouknul po nějaké matematice pro programátory. Hlavní důvod že mě na základce matematika dost bavila. Studoval jsem sice gympl, ale tenkrát jsem nějak nestíhal chodit do školy 😄 😄  tak ze středoškolský matematiky už skoro nic nevím a co jsem věděl, jsem zapomněl po testu. Každopádně, nic mě do toho nenutí, hrozně rád bych se tím ve volným čase prokousával a vytvořil si alespoň nějaké základy. Jednou začas si k tomu sednu a prokousávám se Khan academy. Přesto budu moc rád za jakékoliv tipy na "základy" plus pokročilé - např. jaké kurzy jsou fakt dobré a tak podobně. Je to takovej geekovskej "kink" se naučit nějakou matematiku, nevím jak moc mě to chytne a nedělám si iluze o tom jak náročnej je to obor. Ale když už se na to podívám, mohl bych to spojit s nějakou matikou užitečnou pro developery :))
---


--- https://discord.com/channels/769966886598737931/788826407412170752/901412010410008577
Pánek má spoustu materiálů k automatizaci: https://www.youtube.com/watch?v=OnpOwlp8Hrg&list=PLZaZq-LUymhx3Lip30OGmsMPdAVoNl45i&index=5
---


--- https://discord.com/channels/769966886598737931/769966887055392768/897087048110997584
Vystudovaná škola je irelevantní, fakt. Když pominu procesní části kyberbezpečnosti, kde je stejně dobrý vstup pro právníka, ekonoma jako informatika, tak ty technický části kyberbezpečnosti na škole nic moc neudělají. I na specializovaných školách je to pár profilujících předmětů, navíc (bohužel) ne vždycky valné kvality. Jako juniorní základ bych řekl, že pokud má člověk technické znalosti, aby dokázal přečíst a pochopit Security Engineering od Rosse Andersona https://www.cl.cam.ac.uk/~rja14/book.html (druhá edice je tam elektronicky zdarma), tak je na tom líp než průměrný absolvent oboru kyberbezpečnosti na výšce. Ta vysoká škola s tímhle zaměřením ti dá prostor se tomu věnovat, ale nic negarantuje - můžeš vyjít super nabitej, nebo taky prolézt s tím, že to na tobě nezanechá stop ani v nejmenším.
---


--- https://discord.com/channels/769966886598737931/811910782664704040/892875350655262773
Nedávno jsem narazil na knihu Refactoring UI (https://www.refactoringui.com/book). Rozebírá tam velmi hrubě základní teorii barev, volbu písem, jak pracovat s bílým místem atd. Je ale hlavně o tom řemeslu a systematičnosti - ukazuje, jakým způsobem postupovat, aby výsledek vypadal dobře. Celá kniha se nese v duchu "redukce možností" - radí například, jak si poskládat paletu barev a jejich odstínů. Když pak člověk vybírá vhodnou barvu pro tlačítko a má 20 možností, tak se trefí spíš, než když jich má 16 milionů (celé RGB). V knížce je i spousta praktických tipů na práci s kontrastem, obrázky, stíny...
---


--- https://discord.com/channels/769966886598737931/788826190692483082/884015212573904916
Zkusil jsem něco dát dohromady, postupně to asi budu vylepšovat: https://itsrazy.cz/
Chybí vám tam kdyžtak nějaký meetup?
---


--- https://discord.com/channels/769966886598737931/788832177135026197/883236495060783114
Motivován debatou jinde, jestli je lepší CZ nebo US rozložení klávesnice pro vývojáře jsem aktualizoval „tahák“ na klávesnici. Třeba by se i tady mohl někomu hodit.

**EDIT: verze aktualizovaná  podle připomínek**
PNG (1920×1080 px) https://coreskill.tech/downloads/klavesnice-cz-en.png
SVG https://coreskill.tech/downloads/klavesnice-cz-en.svg
PDF (A4 pro tisk) https://coreskill.tech/downloads/klavesnice-cz-en.pdf
---


--- https://discord.com/channels/769966886598737931/788832177135026197/877136649933455360
YouTube algoritmus mi po čase doporučil dobré video. Pro ty, kteří baží po přehledném vysvětlení OOP https://www.youtube.com/watch?v=m_MQYyJpIjg
---


--- https://discord.com/channels/769966886598737931/788832177135026197/870253808037552168
Je to devops focused, ale i tak je to sada dobrejch rad, kde ty hlavní jsou: 1) koncepty se napříč technologiema tolik neliší, takže je hlavní pochopit ty, 2) je dobrý mít rozhled, i když jste "jen" programátor, protože pak můžete dělat lepší architektonický rozhodnutí https://www.youtube.com/watch?v=d8X4Nd5gswU
---


--- https://discord.com/channels/769966886598737931/788832177135026197/867726165561049129
Ahoj, posílám zdroje, které jsem já používala:

* toto je super úvod do DB, sice tam používá SQLite a Python, ale začíná s ukládáním dat do Google sheets a uvidíš, jaký je rozdíl a proč jsou DB užitečné, takový krok za krokem, jak jsme se dostali k DB: https://www.youtube.com/watch?v=Wb0DM9I8RDo
* k procvičování SQL doporučuju Murder Mystery, je to hrozně zajímavé: http://mystery.knightlab.com/
* k modelování jsem používala krokodýlovy databáze: https://krokodata.vse.cz/DM/DMDB
* MUNI má materiály k DM online: https://www.fi.muni.cz/~xdohnal/lectures/PB154/czech/

EDIT: když už mám několik špendlíků, zkusila jsem vygooglit další zajímavé zdroje:
* ELI5 (explain like I were 5) o databázích, první dvě odpovědi: https://www.reddit.com/r/explainlikeimfive/comments/jht6he/eli5_what_are_databases_and_how_do_they_work/
* ELI5 o tom, jak ukládat velké množství dat do DB: https://www.reddit.com/r/explainlikeimfive/comments/78ppdo/eli5_how_does_a_database_handle_1_billion_users/
* SQL tutorial: https://www.w3schools.com/sql/default.asp
* SQL joins visualizer: https://sql-joins.leopard.in.ua/
* Vennůvy diagramy, ze kterých vychází SQL joiny: https://www.mathsisfun.com/sets/venn-diagrams.html
---


--- https://discord.com/channels/769966886598737931/788832177135026197/867285980209348628
Tohle nemusí být špatný čtení (díky <@!739821357503742042> , že to na LI lajkla https://blog.oliverjumpertz.dev/the-10-most-valuable-lessons-i-learned-as-a-developer)
---


--- https://discord.com/channels/769966886598737931/789092262965280778/1035308642427228221
https://www.smashingmagazine.com/2020/09/figma-developers-guide/
Ještě článek 😉
---


--- https://discord.com/channels/769966886598737931/797040163325870092/1015688999676936252
https://mystery.knightlab.com/ Kdo je vrah? :))
---


--- https://discord.com/channels/769966886598737931/916339896963190785/1014539554952314901
Tohle je ultimátní YT kanál na tohle téma: https://www.youtube.com/c/professormesser
Má to rozházený po playlistech na certifikace od firmy CompTIA (A+ je obecné IT, NET+ jsou sítě a Security+ je IT bezpečnost)
Sjel bych to přesně v tomhle pořadí 🙂
Pokud bys radši česky, tak sítě jsou super napsaný třeba tady od Peterky: https://www.earchiv.cz/l226/index.php3
Dobrý a vtipný YT kanál od jednoho síťaře: https://www.youtube.com/c/NetworkChuck
Penetrační testování: https://www.hackthebox.com/
Python začni klidně tady, kde jsem začal i já 🙂 https://pyladies.cz/course.html
---


--- https://discord.com/channels/769966886598737931/788832177135026197/1007554087887314944
skvělý materiál na téma, jak fungují web servery

https://ruslanspivak.com/lsbaws-part1/
---


--- https://discord.com/channels/769966886598737931/789092262965280778/1000826851050131537
Teoreticky bys měla umět javascript, a ten se používá i na backendu. Backendistu/fullstack z tebe nebude dělat znalost dalsiho jazyka (i když to se hodí), ale znalost databází, ORM, testování, API, queues (async/background zpracovávání), devops, logování, debugování… vše klidně v javascriptu/typescriptu. Nebo v tom javascriptu aspoň můžeš začít, ať vidíš, jestli se ti to líbí, bez toho, abys nejdřív marnila čas učením se dalšího jazyka. Nebo se můžeš učit typescript, pokud ho zatím neovládáš.
---


--- https://discord.com/channels/769966886598737931/788832177135026197/985177771284262962
20 hodin týdně 2 roky.
https://twitter.com/kondrej/status/1535586323461033984
https://twitter.com/svpino/status/1535230313315508224
https://github.com/ossu/computer-science
---


--- https://discord.com/channels/769966886598737931/806215364379148348/981836438893101066
Tohle není moc o zadání, ale o tom, "jak se orientovat v kodu". Když se teď bavím s těmi, které mám třeba na starosti a dělají vlastní první větší projekty, sami se ptají: "když se dostanu k reálnému projektu, který je velký, jak v tom pracovat?"
---


--- https://discord.com/channels/769966886598737931/769966887055392768/974691777820905502
Trochu navážu i na diskuzi výše, že je podle mě dobré dělat si _přehled_, tedy zkoumat věci do šířky (čím víc, tím líp), ale povrchně. Vědět, že existují, tušit, co dělají. A potom mít jednu dvě věci, které se opravdu _učím_. Díky přehledu se pak mohu lépe rozhodovat o tom, co se chci učit. Nesmí se to ale přehnat, aby se místo získávání přehledu (= pustím si pár YT videí o té věci nebo přečtu jeden článek) nestalo učení všeho (= dokončím kurz na to téma).
---


--- https://discord.com/channels/769966886598737931/811910392786845737/968592246209388615
zaujímavé python výzvy na učenie https://www.practiceprobs.com/
---


--- https://discord.com/channels/769966886598737931/769966887055392768/968070061183082536
Dávnejšie som si pre klientov/rodinu/kamarátov a začiatočnícke Czechitas kurzy napísala IT slovník základných pojmov, ktoré pred nimi používam, aby mi rozumeli a lepšie sa v IT zorientovali - https://kompilator.medium.com/it-slovn%C3%ADk-7b71b75d6099 . Celé som sa to snažila napísať svojimi slovami a dala som tam aj čo ma navyše sem-tam napadlo.
---


--- https://discord.com/channels/769966886598737931/811910782664704040/966976515856273428
b) Ty dvě věci, kromě toho, že obě souvisí s JavaScriptem, jsou vlastně úplně něco jiného.

**Next.js je framework postavený na Reactu.**
Je to React + nějaká hromada kódu k tomu + dokumentace a usnadní ti to dělání webů na Reactu, protože už je tam dost věcí, který bys jinak musel dělat sám, vyřešenejch.

**Node.js je „JavaScript runtime“**, tedy běhové prostředí, to je něco, co umí spustit JavaScript na počítači. Ať už je to tvůj notebook nebo nějaký server a musíš si to na něj nainstalovat a pak tam můžeš spouštět programy v JS.
To samé se dělá pro Python a některé další jazyky.
---


--- https://discord.com/channels/769966886598737931/811910782664704040/965681036157653022
jo, rozhodně zkus. Na tom se naučíš řešit problém v jakéomkoli programovacím jazyce. Codewars je asi nejlepší, protože jsou tam přehledně seřazená řešení od jiných lidí - podle kvality kódu a taky se dá filtrovat podle jazyka. Takže až si to napíšeš sám, koukneš, jak to udělali "mistři". A nebo koukneš, když fakt nevíš. A začíná to úplně lehkýma úlohama. Hackerrank je o něco těžší mi přijde. Na druhou stranu u Hackerranku byly k některým úlohám dost kvalitní diskuse, ze kterých se člověk taky ledacos dozvěděl.
---


--- https://discord.com/channels/769966886598737931/916339236721004595/957246070864363520
Pěkný článek, jak funguje OAuth2 pro začátečníky 🙂 (mě to hodně pomohlo, když jsem se to snažil před lety pochopit) - http://agileanswer.blogspot.com/2012/08/oauth-20-for-my-ninth-grader.html
---


--- https://discord.com/channels/769966886598737931/769966887055392768/945383885531930785
článek k tomu: https://digichef.cz/otazky
---


--- https://discord.com/channels/769966886598737931/806621830383271937/939241551681425448
Není jen JS Fiddle, existuje i SQL Fiddle 😱 🙂 http://www.sqlfiddle.com/#!3/002f1/2
---


--- https://discord.com/channels/769966886598737931/811910782664704040/937839936424509500
https://github.com/kettanaito/naming-cheatsheet
---


--- https://discord.com/channels/769966886598737931/789087476072710174/934111300798271529
<:vscode:628587870273142795>  https://vscodecandothat.com/
---


--- https://discord.com/channels/769966886598737931/916346318048337960/930759930904993834
Pokud ti jde o úplný základy syntaxe, tak doporučju hostovaný tutoriály jako je https://sqlzoo.net/wiki/SQL_Tutorial, bude jich jistě víc (tipuju, že repl.it něco má). Pokud bys pak chtěl vlastní data, tak doporučuju SQLite s nějakým rozhraním - já mám rád mnohokrát zmiňovaný TablePlus (jen mu dáš cestu k databázi na disku a jedeš)
---


--- https://discord.com/channels/769966886598737931/806621830383271937/930220329031307285
[sítě] objevil jsem Cisco Packet Tracer https://www.netacad.com/courses/packet-tracer - docela pěkná hračka k pochopení sítí. Jde tam snadno poskládat libovolná síť a pak pozorovat, kudy a jak data tečou, krok za krokem...
---


--- https://discord.com/channels/769966886598737931/788832177135026197/919699123081449543
Asi to tu ještě nebylo zmíněno, tak to sem dávám – super tool na prohledávání modulů a funkcí ve standardních knihovnách různých jazyků (a sem tam i dalších knihoven). Podporuje i offline režim.
https://devdocs.io/
---


--- https://discord.com/channels/769966886598737931/788832177135026197/913331018864414751
Mě pomohl až Lumír 🙂 https://youtu.be/1UPTK8OTdeg
---


--- https://discord.com/channels/769966886598737931/788832177135026197/910436103838912532
Kdyby chtěl někdo něco programovat 😉
<:python:842331892091322389> <:javascript:842329110293381142> <:java:847749733664555018>
Vypadá, že to je zadarmo.
https://www.codecademy.com/code-challenges
> With technical interviews, practice makes perfect. Now, you can practice real code challenges from actual interviews to see how your skills stack up. If you get stuck, we’ll point you to what you still need to learn.
Nevím, jestli se v českém prostředí tohle objevuje u pohovorů, ale jako cvičení to pro někoho může být zajímavý.
---


--- https://discord.com/channels/769966886598737931/769966887055392768/906580836185428020
K algoritmům obecně třeba tohle: https://knihy.nic.cz/files/edice/pruvodce_labyrintem_algoritmu.pdf
---


--- https://discord.com/channels/769966886598737931/788832177135026197/1099057039549927534
Průlet matematikou, která se někdy hodí většině programátorům. Nemusíte ji umět, ale chcete vědět, jak se to jmenuje a co to je, abyste si to uměli aspoň vygooglit, až to budete potřebovat 🔢 https://youtu.be/bOCHTHkBoAs
---


--- https://discord.com/channels/769966886598737931/1075541542669922424/1098976769509445653
ad materialy, z hlavy:
* surrounded by idiots - jak se lidi chovají a proč se chovají tak, jak se chovají
* how to win friends and influence people - nejlepší kniha ever o lidech a o tom, jak udělat takový dojem, že tě lidi budou mít rádi
* how to present on ted talk - o prezentačních dovednostech, do hloubky a na profi úrovni, přímo od zakladatele ted talků
* the subtle art of not giving a fuck - právě čtu, ale má to dobré hodnocení
* radical candor - o dávání zpětné vazby, užitečné pro ty, co se jí bojí
* https://www.youtube.com/watch?v=Ks-_Mh1QhMc - nejlepší talk ever o sebevědomí a imposter syndromu
* https://www.youtube.com/watch?v=H14bBuluwB8 - o disciplíně a její vlivu na úspěch
---


--- https://discord.com/channels/769966886598737931/788826928147857439/1085251519496073368
Byste někdo kdo se těch Pyv účastníte mohl sepsat, jak to celé probíhá. Pro nás co jsme na podobné akci nikdy nebyli. Mě osobně se to těžko představuje. Bývá to v hospodě, zároveň je tam přednáška...někdy popis v angličtině někdy v češtině. Už z těchto informací mě napadá několik dotazů...komunikuje se tam v angličtině nebo je jen přednáška v angličtině? Sedí se tam po nějakých skupinkách u stolů nebo v řadách jako na přednášce? Je tam nějaký tlak na nově příchozí aby se představili nebo je naopak všichni přehlíží dokud se sami někam neuvedou?
---


--- https://discord.com/channels/769966886598737931/806621830383271937/1065341778682712105
MDO https://www.trywilco.com/
---


--- https://discord.com/channels/769966886598737931/1002976022486057020/1004009895634403479
Ten dotaz je hodně do široka, ale v začátku bych se, jak píše Honza, soustředil na to, abych uměl problém rozložit na podproblémy a hlavně abych dokázal projít takovým tím kolečkem řešení problému:

1. Dostanu zadání (převodník z římských na arabská čísla)
2. Zjistím si všechno o problému který řeším, udělám základní rešerši (přečtu Wikipedii o římských číslech, zjistím kolik mají maximálně znaků, jak se strukturují, jaké mají speciální případy, atd.)
3. Až poté se zamyslím, jak nejlépe věc řešit. Navrhnu řešení. To znamená zamyslím se, jestli už něco neexistuje co můžu použít, jestli to vůbec musím programovat, kouknu se na balíčky, na standardní knihovnu, googlím jestli to někdo už neřešil přede mnou, pak si řeknu ok, asi to opravdu naprogramuju, tak a tak. Rozložím velký úkol na menší úkoly (načtení vstupu, převod textu s římskými čísly do arabských čísel, vypsání výsledku...).
4. Až v tuto chvíli jdu psát první kód.

Někdy je dobré smíchat trochu 3 a 4, čemuž se říká prototypování. Zkoušíš různé věci a to ti pomáhá lépe vymyslet finální řešení.

Toto je podle mě největší úkol pro začátečníka a na toto by se začátečník měl soustředit, aby si to osvojil a ideálně na praktických úkolech.
---


--- https://discord.com/channels/769966886598737931/993478147355971684/993479121483075684
pre ludi co nemaju OOP skusenosti mozem odporucit pozret si nejaky clanok k SOLID principom, napr. https://www.digitalocean.com/community/conceptual_articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design a zapamatat si zo 2 vety k aspon 3 z 5 bodov, to by malo stacit na 99% interview o OOP pre zaciatocnikov, aby clovek nedostal cerveny bod (povedat, ze nemam skusenosti, ale cital som clanok o SOLID a zapamatal som si z toho xxx)
---


--- https://discord.com/channels/769966886598737931/789087476072710174/1112727311347875922
https://cron-ai.vercel.app/
---


--- https://discord.com/channels/769966886598737931/789087476072710174/1112726378677272628
Máš odkaz? Já znám jen https://crontab.guru/ (teda „jen“ bych dal do závorek, už tohle mi přijde hodně užitečné 😄 )
---


--- https://discord.com/channels/769966886598737931/789087476072710174/1111723379028922418
Regulární výrazy. Napíšete a máte. https://www.autoregex.xyz/
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1115564713242271854
Ještě jsem našel tento seznam backend challenges. https://github.com/CollabCodeTech/backend-challenges
---


--- https://discord.com/channels/769966886598737931/1117785793533071450/1117787037794324570
Ano, syntaxí, které jsou všechny markdown, ale mají nějaké speciální vlastnosti nebo s v některých detailech chovají jinak, je plno. Nicméně to, co je tady na Discordu jsou jen základní věci, takže se asi užijí všude, kde se to jmenuje Markdown.
---


---
Stalubo@ v mailu:
3. "PRŮBĚŽNÉ ZAPOMÍNÁNÍ" - i když se učíte denně, tak než se nachytříte jedno, tak to druhé pomalu začnete zapomínat. Protože to nepoužíváte. A nepoužíváte, protože čas není nafukovací a vy ho věnujete novému tématu. Navíc, to že se to člověk naučil, není nijak odměněno. Naučíte se, udělate test anebo si jenom odškrtnete a zatleskáte, ale za měsíc už si z toho pamatujete sotva polovinu. A to máte za sebou jen HTML, CSS a 40% SQL a čeká vás Python a GIt-Github.
; Člověk by už potřeboval dostávat malé "honorované" úkoly, aby získával jistotu, že to není jen učení do šuplíku. Kde netvoří žádné hodnoty. Něco, co by za ním zůstávalo. Když se necháte zaměstnat na part-time do Alberta k pokladně, tak je to sice "málo duchaplná práce", ale někdo vám za ni zaplatí. Když se učíte IT, tak "duchaplná práce", ale nevíte, jestli vám někdo někdy za ni bude ochoten zaplatit (jestli vydržíte, aby jste dosáhl toho stádia).
---


--- https://discord.com/channels/769966886598737931/1113873887445397564/1113931127531520050
Junior guru je skvělá příručka. Nauč se základy , udělej alespoň jeden velkej projekt, vymazli github -cv. Následoval jsem tyhle kroky a fungovalo to. Ale nemůžeš vynechat ten projekt. Musíš si prostě tim ušpinit ruce a zaměstnat hlavu. Když si vymyslíš svůj, bude tě to více bavit. Ale musíš vytvářet. A googlit ,jak na ty dílči kroky, ne procházet něčí osnovu. Protože to tě nenutí tolik přemýšlet. člověk  nesmí skončit u piškvorek z návodu, musí přidat něco svého co ho donutí se posunout. A bude to nepříjemné, když se zasekneě. Stalo se mi to hodněkrát. Celý den jsem strávil na tom , jak udělat jednu věc, kterou senior napíše za  20 minut.  Bylo to peklo, říkal jsem si , tohle už je můj limit.  Ale pak jsem to vždy nějak napsal a fungovalo to. Po třech měsích v práci se stydím, za svůj projekt, se kterým jsem se o tu práci ucházel. Ale podle mě bylo to co zaměstnavatele přimělo mě vyzkoušet. To , že se pokusím udělat to co jsem si dal za úkol i když to je náročné. Protože ten projekt je  pro začátečníka podle mě náročnější než kurz.  Ale zábavnější. A určitě tě vědomí toho, že si to dokázal vyrobit, naplní víc, než certifikát.
Nechci hodnotit výše zmíněné kurzy,  určitě mohou pomoci získat znalosti. Ale upřímně si polož otázku, jestli ty nepotřebuješ jen aplikovat a procvičit to, co už si minimálně jednou slyšel. Fandím ti. Máš výdrž a když nepolevíš, tak se ti ten cíl splní. Sleduji tě už dlouho a opravdu držím palce. Kdyby si měl pocit, že se chceš na něco z mé cesty zeptat, klidně napiš. Ale opravdu, zkus jít za tu hranu, toho, co se ti třeba nechce..tam tě totiž čeká to ,co chceš 🙂
---


--- https://discord.com/channels/769966886598737931/1084817360352989294/1120426048308379831
Bohužel mám příliš mnoho dobrovolnických aktivit, takže se nemůžu věnovat mentoringu. Nicméně mám jednu univerzální radu, která vás může zásadně posunout. Používejte statickou analýzu kódu https://blog.zvestov.cz/software%20development/2023/06/19/enum-a-staticka-analyza-kodu.html?utm_source=juniorguru
---


--- https://discord.com/channels/769966886598737931/789087476072710174/1137689798589554688
Tohle mi zrovna přistálo na timeline na Twitteru a když si vzpomenu na svoji první práci a cizí repo, může to tu podle mě někomu přijít vhod - jak se seznámit s existující / cizí codebase?
---


--- https://discord.com/channels/769966886598737931/811910782664704040/1136264122506416148
Nová stránka na procvičování kódění a programování! 🤩
Je to dost podobné jako FrontendMentor akorát jsou tam daily challenges jako na CodeWars. Plus může to člověk kódit přímo v prohlížeči (jako Scrimba 💜 ) a nemusí si nic stahovat.
https://icodethis.com/
---


--- https://discord.com/channels/769966886598737931/916346318048337960/1129327666290507827
Na vejsce jsme procvičovali na tomhle : https://sqltutor.fsv.cvut.cz/cgi-bin/sqltutor je to absolutně super přesně na biflovani základních selectu - některý datasety jsou triviální (nobelisti a Přemyslovci, některé jako třeba vodočty a tramvaje už vyžadovali vnořené selecty a složitější  kombinování tabulek 😀, takže se dá vybrat co zrovna chceš procvičit. Nejsou to velká data, ale to je na selecty téměř jedno.

Btw měli jsme na vejsce jednu slečnu, co se zvládla na zapoctak naučit všechny ty úlohy zpaměti... 😅🤦
---


--- https://discord.com/channels/769966886598737931/811910392786845737/1127896694323949619
Zajímavý článek o tom, jak použít GitHub API a najít zajímavé nové projekty v Pythonu za účelem toho, že by do nich mohl člověk třeba i přispět v rámci open source: https://mostlypython.substack.com/p/exploring-recent-python-repositories
---


--- https://discord.com/channels/769966886598737931/789087476072710174/1127897372047986709
„What if you could easily get a visual picture of how any Git command would impact your local repo, without interrupting your dev workflow?“ Nezkoušel jsem, ale vypadá to pěkně. Nástroj, který umí vizualizovat co se stane s vaším git repozitářem, když nad ním pustíte nějaký git příkaz https://initialcommit.com/blog/git-sim
---


--- https://discord.com/channels/769966886598737931/789087476072710174/1143045188885942314
Taky jste v záčátku hledali kde ja jaký znak?
https://klavesnice.czechitas-podklady.cz/

A moje frontendová verze v PDF ke stažení https://discord.com/channels/769966886598737931/789087476072710174/1090957362438869092
(založena na pythonní https://pyvec.github.io/cheatsheets/keyboard/keyboard-cs.pdf)
---


Security challenges:
- https://discord.com/channels/769966886598737931/769966887055392768/898300896868433931
- https://www.thecatch.cz/
- https://ctftime.org/
- https://ecsc.eu/


https://m.youtube.com/watch?v=LG-d_BOZE6k


--- https://discord.com/channels/769966886598737931/788832177135026197/1163098667738218586
Pro začátečníky možná až moc podrobnej článek o Unicode, ale zase pokud vás to zajímá, tak si počtete https://tonsky.me/blog/unicode/
---


--- https://discord.com/channels/769966886598737931/788832177135026197/1159450058194948138
Takové pozorování. I jako testeři budete potřebovat základy obsluhy linuxu. A když to budete umět předem, tak můžete zabodovat 😉 Typicky `ssh`, `cd`, `ls` a pak si přečíst logy třeba přes `less`.  Ne všechno a všude bude klikací v grafaně. https://www.thegeekstuff.com/2010/02/unix-less-command-10-tips-for-effective-navigation/
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1157220299658493963
<@544187409026252800> dal na LI pěkný příspěvek o networkingu (jak na to) https://www.linkedin.com/posts/david-rajnoha-a62453168_pyconcz-velvetinnovation-edufestival-activity-7113409610085974016-phRH?utm_source=share&utm_medium=member_ios
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1153399676817653840
Advice to beginners | Ned Batchelder

https://nedbatchelder.com/blog/202309/advice_to_beginners.html
---


--- https://discord.com/channels/769966886598737931/788832177135026197/1148913024577581148
Menší sbírka videí o konceptech kolem programování, poměrně nezávislá na použitém jazyce. https://www.youtube.com/@CodeAesthetic
---


--- https://discord.com/channels/769966886598737931/1184491871637078077/1184812245281165363
Ahoj, datová věda je pomerne široká oblasť. Z toho čo píšeš mi to znie že sa aktuálne formuješ ako datový analytik. Možno by som do tvojho rozhodovacieho stromu pridal ešte zamyslenie nad tým, do akej oblasti by si chcela ísť pracovať.

V tradičných korporátoch napríklad typu banka, kde pracujem aj ja, je dnes datová analýza postavená hlavne na SQL a PowerBI. Pokiaľ by si sa ale rada venovala aj nqpr. datařine v pythone tak si postráž na pohovore aby v tejto firme vôbec existovala podpora pre tento jazyk. Zároveň sa ti môže stať, že ťahúňom v rozvoji python riešení budeš práve ty - to nemusí vyhovovať ľuďom, ktorý vyžadujú silné seniorné vedenie.

V technickejšie zameraných firmách už dnes často datový analytik znamená aj SQL a python - tu ale často býva väčši presah do ďalších oblastí - modelovanie, machine learning atď. a často menší dôraz na tvorbu reportov a vizualizácií.

Jeden spoločný menovateľ je zjavný - vedieť dobre SQL je obrovské plus, nejde ani tak o fancy príkazy ako o schopnosť zorientovať sa v rôznych dátových zdrojoch, tieto dáta pospájať a získať požadovaný výsledok.

Ak by ti PowerBI nevyhovovalo, pretože máš radšej programátorskejší ako klikací prístup, python obsahuje veľké množstvo knižníc kde sa môžeš realizovať. Ja pracujem s knižcou Plotly Dash a naviazanými vizualizáciami v Plotly - u nás v banke ho používame ako alternatívu k PowerBI. Ak by si si chcela spraviť základný prehľad tak k workshopu na pycone som napísal aj rozsiahly návod pre datařov, ktorý by s dashom radi začali: https://github.com/martin2097/pycon-prague-2023-dash-workshop
---


--- https://discord.com/channels/769966886598737931/788832177135026197/1184824550324719616
Já se tady zjevím vždycky jen jednou za čas (hlavně v prosinci, náhoda?), tak aspoň (nejspíš opět) přidám tip na jeden z nejlepších malinko pokročilejších kurzů, který vám pomůže pochopit, jak vlastně počítač funguje a co se v něm děje. A je to zábava 🙂

https://www.nand2tetris.org/, resp. https://www.coursera.org/learn/build-a-computer
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1182391116629286923
Do nedávna byla při programování klíčová schopnost efektivně googlit. Může to vypadat banálně ale umět efektivně googlit se člověk učil roky. Teď bude při programování klíčová schopnost efektivně využívat AI.
---


--- https://discord.com/channels/769966886598737931/788832177135026197/1180500106303242322
Ahoj, nedoporučili byste někdo nějaké kvalitní výukové materiály pro regulární výrazy?
Když tak vidím letošní Advent of Code, které mě tentokrát dokázalo demotivovat v jakýchkoli dalších snahách, asi bych se s nimi měla konečně začít kamarádit. 🙃
---


--- https://discord.com/channels/769966886598737931/806621830383271937/1179302149537140836
<:python:842331892091322389> Mnozí se už přesvědčili, že AI může být extrémně nápomocné, ale zároveň je to občas boj, aby dělalo to, co chceme. Tady je nejen skvěle popsáno, jak toto konkrétní GPTs tvořili, ale hlavně je to zaměřené na pomoc a vysvětlování Pythonu. <:python:842331892091322389>

https://www.linkedin.com/posts/nancyebain_meet-pypilot-a-customgpt-case-study-activity-7134904613622706176-eZ_W
---


--- https://discord.com/channels/769966886598737931/1170648798532489226/1170850238823661678
Angličtina.


Vidím asi 3 možné výjimky:
1. začátečníci na úplném začátku, pokud jim to pomáhá s pochopením toho, co dělají
2. lidi v týmu mají tak špatnou angličtinu, že jejich pojmenování brání chápání kódu těm, kteří ji mají lepší
3. to co už tu padlo, zvážil bych to tam, kde jde o termíny, které jdou blbě přeložit a stejně nikdo nebude vědět, co to znamená
---


--- https://discord.com/channels/769966886598737931/864434067968360459/1169910594497953812
Jaký je podel vás smysl či podstat komunikace a dobré komunikace obzvlášť?
---


--- https://discord.com/channels/769966886598737931/797040163325870092/1170063959508926565
Tady nějaký seznam, který jsem náhodně vygooglil https://github.com/kdeldycke/awesome-falsehood
---


--- https://discord.com/channels/769966886598737931/916339896963190785/1192738348998082611
Pokud používáte nějakého AI asistenta při psaní kódu, tak je jistá šance, že bude méně bezpečný a zároveň budete věřit, že je bezpečnější než kdybyste AI nepoužívali https://arxiv.org/abs/2211.03622
---


--- https://discord.com/channels/769966886598737931/1191365076188397591/1192218179880095764
U te diskuze ohledne AI bych vicemene souhlasil se vsemi zucastnenymi.
Ano, jeji podstatou je efektivita. Ta ale v kazde fazi znamena neco jineho.
Kdyz se ucim stavarinu, ochotne mi poradi, jak vypada cihla, proc malta lepi a jak tuhne beton. Odstranim zaseky, kdy nevim jak dal a zvysim efektivitu UCENI. Netroufl bych si ji ale jeste pozadat navrhnout cely dum.
Kdyz uz ale vim, jak se chova cihla, malta a beton, pomuze mi poskladat modulove patrove domy. Odstrani hodiny skladani a pocitani cihel a betonovych konstrukci. Zase to bude efektivita, ale uz efektivita PRACE
---


--- https://discord.com/channels/769966886598737931/789087476072710174/1194549501982163057
Jen tak na okraj kdo je STUDENT? Nebo dokonce i učitel, tak má COPILOT z GITHUBU ZADARMO!!! Šiřte to dál.
https://github.blog/2022-09-08-github-copilot-now-available-for-teachers/
---


https://cpu.land/
https://osveta.nukib.cz/local/dashboard/
https://www.fakturoid.cz/almanach/osobni-rozvoj/jak-pouzivat-chatgpt
https://www.marketawillis.com/blog/prakticke-programatorske-aktivity
https://www.youtube.com/watch?v=44sJQChy8g0

--- https://discord.com/channels/769966886598737931/797040163325870092/1198884862405386240
Dobré ráno 🙂 pondělní dávka motivace pro všechna kuřata 🐤 
https://youtu.be/QG3C1uwuloM?si=wDfZpfewKdenSb7i
---


#} -->
