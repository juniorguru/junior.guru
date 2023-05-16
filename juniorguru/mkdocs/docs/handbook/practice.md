---
title: Jak získat praxi v programování
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
  Jiří Psotka, recruiter v [Red Hatu](https://red.ht/juniorguru) v [prvním dílu podcastu junior.guru](../podcast.md#episode0001)
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

[Open-source software](https://cs.wikipedia.org/wiki/Otev%C5%99en%C3%BD_software) (OSS) jsou projekty s kódem, na který se může kdokoliv podívat, a které lze většinou využívat zdarma — například [Linux](https://cs.wikipedia.org/wiki/Linux) nebo [LibreOffice](https://cs.wikipedia.org/wiki/LibreOffice). Pokud si [dáš svůj projekt na GitHub](git.md), kde jeho kód mohou číst další lidé, máš taky takový maličký open source. I tyto webové stránky [jsou open source](https://github.com/honzajavorek/junior.guru).

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
    'https://pycon.cz',
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

#} -->
