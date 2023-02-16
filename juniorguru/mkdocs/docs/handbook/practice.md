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

  {{ link_card(
    'Hackathon.com',
    'https://www.hackathon.com/',
    'Celosvětový seznam místních i online hackhatonů.'
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

<div class="link-cards">
  {{ link_card(
    'Aj Ty v IT',
    'https://www.ajtyvit.sk'
  ) }}

  {{ link_card(
    'BeeIT',
    'https://www.beeit.cz/'
  ) }}

  {{ link_card(
    'Codecademy',
    'https://www.codecademy.com'
  ) }}

  {{ link_card(
    'Coding Bootcamp Praha',
    'https://www.codingbootcamp.cz/'
  ) }}

  {{ link_card(
    'CoreSkill',
    'https://coreskill.tech/'
  ) }}

  {{ link_card(
    'Coursera',
    'https://www.coursera.org'
  ) }}

  {{ link_card(
    'Czechitas',
    'https://www.czechitas.cz/cs/kalendar-akci'
  ) }}

  {{ link_card(
    'edX',
    'https://www.edx.org'
  ) }}

  {{ link_card(
    'ENGETO Academy',
    'https://engeto.cz'
  ) }}

  {{ link_card(
    'egghead.io',
    'https://egghead.io'
  ) }}

  {{ link_card(
    'Green Fox Academy',
    'https://www.greenfoxacademy.cz/'
  ) }}

  {{ link_card(
    'Skillmea',
    'https://skillmea.cz/'
  ) }}

  {{ link_card(
    'Pluralsight',
    'https://www.pluralsight.com/'
  ) }}

  {{ link_card(
    'PrimaKurzy',
    'https://www.primakurzy.cz/'
  ) }}

  {{ link_card(
    'PyWorking',
    'https://pyworking.cz'
  ) }}

  {{ link_card(
    'Software Development Academy',
    'https://sdacademy.cz/'
  ) }}

  {{ link_card(
    'Udacity',
    'https://udacity.com'
  ) }}

  {{ link_card(
    'Udemy',
    'https://www.udemy.com'
  ) }}

  {{ link_card(
    'VŠB-TU',
    'http://kurzy.vsb.cz/'
  ) }}
</div>

<small>Tento seznam je v abecedním pořadí. Pokud víš o dalším webu s kurzy, piš na {{ 'honza@junior.guru'|email_link }}.</small>


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
