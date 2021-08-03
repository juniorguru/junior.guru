---
title: Klub pro začátečníky v programování
thumbnail_title: Klub pro začátečníky v programování
main_class: main-sections
description: Přidej se na junior.guru Discord! Jsme tvoje online programovací parta, skupina, fórum. Začátečníci, kteří to myslí vážně. Profesionálové s chutí pomáhat. Svoje programování nebo hledání práce posuneš o 1 % každý den.
---

{% from 'shared.html' import img %}
{% from 'markdown.html' import markdown, blockquote_avatar, blockquote_toxic, logo, lead %}


<header class="masthead"><div class="masthead-container">
<div class="masthead-content">
<h1>Tvoje programovací parta</h1>

{% call lead() %}
Začátečníci, kteří to myslí vážně. Profesionálové s chutí pomáhat. V klubu svoje programování nebo hledání práce posuneš o **1 % každý den**.
{% endcall %}

<div class="masthead-numbers">
{% call markdown() %}
- **{{ messages_count|thousands }}** příspěvků
- **{{ members_total_count }}** členů
- **{{ companies|length }}** firem
- **{{ events|length }}** akcí
{% endcall %}
</div>

<a class="masthead-button primary" href="#cenik">Přidej se</a>
<span class="masthead-members">
  {% for member in members|sample(8) %}
    {{ img('static/' + member.avatar_path, 'Profilovka člena klubu', 50, 50, lazy=False) }}
  {% endfor %}
</span>

</div>
{{ img('static/images/illustration-club.svg', 'Ilustrace', 400, 400, class='masthead-illustration') }}
</div></header>


<section>
<ul class="logos">
  <li class="logos-item logos-caption">
    <a href="https://docs.google.com/document/d/1keFyO5aavfaNfJkKlyYha4B-UbdnMja6AhprS_76E7c/edit?usp=sharing" target="_blank" rel="noopener">Firemní partneři</a>:
  </li>
  {% for company in companies %}
    {{ logo(company.name, company.filename, company.link) }}
  {% endfor %}
</ul>
<ul class="logos grayscale standout">
  <li class="logos-item logos-caption">
    <a href="#komunity">Komunitní partneři</a>:
  </li>
  {{ logo('Česko.Digital', 'ceskodigital.svg', 'https://cesko.digital/') }}
  {{ logo('DigiKoalice', 'digikoalice.svg', 'https://digikoalice.cz/') }}
  {{ logo('Frontendisti', 'frontendisti.svg', 'https://frontendisti.cz/') }}
  {{ logo('PyLadies', 'pyladies.svg', 'https://pyladies.cz/') }}
  {{ logo('Pyvec', 'pyvec.svg', 'https://pyvec.org/') }}
  {{ logo('CyberMagnolia', 'cybermagnolia.svg', 'https://cybermagnolia.com/') }}
  {{ logo('ReactGirls', 'reactgirls.svg', 'https://reactgirls.com/') }}
  {{ logo('yablko', 'yablko.svg', 'http://robweb.sk/') }}
</ul>
</section>


<section>
<h2>Získej parťáky, mentory, kamarády</h2>
{% call lead() %}
Jsme **online komunita** na [Discordu](https://discord.com/). Občas pořádáme [přednášky](/events/), ale nejsme škola, neděláme kurzy. Sdílíme si tipy a postřehy. Podporujeme se a radíme, když někomu něco nejde. Někteří díky klubu seženou práci. Dáváme si zpětnou vazbu. Společně se radujeme z úspěchů. Můžeš se aktivně zapojit, nebo vše jen potichu sledovat.

Potkáš u nás stejné začátečníky, jako jsi ty. Každý s jiným životním příběhem, ale s velmi podobnými dotazy a problémy. O klub se stará **Honza Javorek, autor junior.guru**, okolo se však „poflakuje“ i řada dalších **profíků s chutí pomáhat**.
{% endcall %}
<div class="standout"><div class="icons">
  <ul class="icons-list">
    <li class="icons-item">
      {{ 'play-btn'|icon }}
      Online klubové akce
    </li>
    <li class="icons-item">
      {{ 'clock-history'|icon }}
      Archiv záznamů akcí
    </li>
    <li class="icons-item">
      {{ 'list-check'|icon }}
      Pracovní nabídky
    </li>
    <li class="icons-item">
      {{ 'compass'|icon }}
      Kariérní konzultace
    </li>
    <li class="icons-item">
      {{ 'person-check'|icon }}
      Zpětná vazba na&nbsp;CV
    </li>
    <li class="icons-item">
      {{ 'code-slash'|icon }}
      Zpětná vazba na&nbsp;kód
    </li>
    <li class="icons-item">
      {{ 'chat-dots'|icon }}
      Recenze a&nbsp;zkušenosti
    </li>
    <li class="icons-item">
      {{ 'heart'|icon }}
      Podpora a&nbsp;pochopení
    </li>
    <li class="icons-item">
      {{ 'person-plus'|icon }}
      Komunita, síť&nbsp;kontaktů
    </li>
    <li class="icons-item">
      {{ 'lightbulb'|icon }}
      Mentoring od&nbsp;profíků
    </li>
    <li class="icons-item">
      {{ 'patch-plus'|icon }}
      Slevy a&nbsp;soutěže
    </li>
    <li class="icons-item">
      {{ 'hand-thumbs-up'|icon }}
      Podporuješ junior.guru
    </li>
  </ul>
</div></div>

{#
  TODO poslední 2-3 akce v klubu
#}

<div class="blockquotes-2">
{{ blockquote_avatar('Jemně popostrkující a nějakou činnost vyvolávající a podněcující síla, kterou jsem potřebovala. Nacpat se sem byl moc dobrej napád.', 'radka.png', 'Radka', 'Radka') }}

{{ blockquote_avatar('Jako kluka z vesnice mě na programování vždy štvalo, že jsem na to byl hrozně moc sám. Jsem opravdu vděčný za tuto komunitu.', 'lukas.png', 'Lukáš', 'Lukáš') }}
</div>
</section>


<div class="section-background gray-white"><section>
<h2>Neztrácej čas s hulváty a sexisty</h2>
{% call lead() %}
Nemáme potřebu někoho stírat. **Hloupé otázky neexistují** a uslintané vtipy nikoho nezajímají. Mezi členy jsou ženy, muži, staří, mladí. **Respektujeme se**, pomáháme si, jsme k sobě laskaví a profesionální. Případné úlety se řídí [pravidly chování](coc.md).
{% endcall %}
<div class="blockquotes-2 standout">
{{ blockquote_avatar('Ty diskuze jsou úžasné. Když to lidi zaplatí, tak je to úplně jiné. Extrémně kultivované, srozumitelné, každý příspěvek dává smysl.', 'jakub.png', 'Jakub', 'Jakub') }}

{{ blockquote_avatar('Je problém najít komunitu, která je o vzájemný pomoci a výměně informací, ne o honění ega. Tady je to krásná výjimka. Jsem ráda, že toho můžu být součástí.', 'hanka.png', 'Hanka', 'Hanka') }}
</div>
<div class="blockquotes-2 standout">
{{
  blockquote_toxic(
    'Loni jsem provedl upgrade PŘÍTELKYNĚ 1.0 na verzi MANŽELKA 1.0…',
    'Tomáš Marek',
    'FB skupina Programátoři začátečníci',
    'https://www.facebook.com/groups/144621756262987/posts/832213487503807/'
  )
}}
{{
  blockquote_toxic(
    'Možná by jsi měl držet hubu p*** když se tě nikdo na nic neptá č*****',
    'Darken Joe Svoboda',
    'FB skupina Programátoři',
    'https://www.facebook.com/groups/193575630828729/posts/1740414872811456'
  )
}}
</div>
</section></div>


<section>
<h2>Neztrácej čas záplavou názorů</h2>
{% call lead() %}
Odborníci, kteří vstoupili do klubu, to udělali ze zájmu o juniory a **s chutí pomáhat**. Vycházíme z [konkrétní cesty jak postupovat](/learn/), která se **osvědčila mnohým začátečníkům**. Zároveň se snažíme radit objektivně a brát ohled na tvou situaci. Poskytneme ti různé pohledy, ale zároveň **jasný směr**. Místo abychom tě utopili v možnostech, pomůžeme ti rozhodnout se.
{% endcall %}

<div class="standout"><div class="comparison">
{% call markdown() %}
{% set check = 'check-circle-fill'|icon('text-success') %}
{% set cross = 'x-square-fill'|icon('text-danger') %}

| Veřejné skupiny                      | Klub junior.guru                                | Osobní mentor                  |
|--------------------------------------|-------------------------------------------------|--------------------------------|
| {{ cross }} kvantita                 | {{ check }} dostatečná kvalita                  | {{ check }} exkluzivní kvalita |
| {{ check }} zdarma                   | {{ check }} dostupné                            | {{ cross }} drahé              |
| {{ cross }} ko&shy;lemjdoucí         | {{ check }} komunita                            | {{ check }} osobní vztah       |
| {{ cross }} radí kdokoliv            | {{ check }} radí anga&shy;žo&shy;vaní odborníci | {{ check }} radí odborník      |
| {{ cross }} správce dobro&shy;volník | {{ check }} správce na plný úvazek              | {{ check }} na plný úvazek     |
| {{ check }} všudy&shy;přítomné       | {{ check }} dostupné                            | {{ cross }} obtížně dostupné   |
{% endcall %}
</div></div>

{% call lead() %}
Rady „kolemjdoucích“ ve veřejných skupinách jsou náchylné k fanouškovství, opakují [nejrůznější mýty](/motivation/#myths), doporučují staré postupy. Vycházejí z toho, že když něco vyhovovalo jednomu, zákonitě musí i druhému. Na jednoduchou otázku běžně dostaneš **desítky rozcházejících se odpovědí**, mnohdy zcela nevhodných.
{% endcall %}
</section>


<div id="cenik" class="section-background yellow"><section>

<h2>Za vyzkoušení nic nedáš</h2>
{% call lead() %}
Nemusíš hned zadávat kartu. Vyber si roční nebo měsíční předplatné a nakoukni, jak to u nás vypadá. **Prvních 14 dní je zdarma.** Pokud ti klub nesedne, prostě akorát nedoplníš platební údaje a systém tě po dvou týdnech vyhodí.

Pokud se vzděláváš u {% for company in companies_students -%}
  {%- if not loop.first %}, {% endif %}{% if loop.last %}nebo {% endif -%}
  {{ company.name }}
{%- endfor %}, tvůj **studijní program může zahrnovat bezplatné členství v klubu**. Zeptej se jich, jestli je to tvůj případ!
{% endcall %}

<div class="pricing standout">
  <div class="pricing-block pulse-hover">
    <h3 class="pricing-heading">Ušetřím</h3>
    <ul class="pricing-benefits">
      <li class="pricing-benefits-item">Prvních 14 dní zdarma</li>
      <li class="pricing-benefits-item">Jeden měsíc ušetříš</li>
    </ul>
    <a class="pricing-button" href="https://juniorguru.memberful.com/checkout?plan=59574">1199 Kč ročně</a>
  </div>
  <div class="pricing-block pulse-hover">
    <h3 class="pricing-heading">Nevážu se</h3>
    <ul class="pricing-benefits">
      <li class="pricing-benefits-item">Prvních 14 dní zdarma</li>
      <li class="pricing-benefits-item">Můžeš to kdykoliv zrušit</li>
    </ul>
    <a class="pricing-button" href="https://juniorguru.memberful.com/checkout?plan=59515">109 Kč měsíčně</a>
  </div>
  <div class="pricing-block pulse-hover">
    <h3 class="pricing-heading">Stipendium</h3>
    <ul class="pricing-benefits">
      <li class="pricing-benefits-item">Podpora pro znevýhodněné</li>
      <li class="pricing-benefits-item">Vyplň formulář a uvidíš</li>
    </ul>
    <strong class="pricing-button disabled">Připravuje se</strong>
  </div>
</div>
</section></div>


<section>
{% call markdown() %}

## Otázky a odpovědi {: #faq }

{% call lead() %}
Projdi si prosím odpovědi na nejčastější otázky, měly by ti vše kolem klubu objasnit. Pokud i tak budeš mít nějaké dotazy, neváhej a piš na {{ 'ahoj@junior.guru'|email_link }}.
{% endcall %}

### {{ 'person-plus'|icon('text-primary me-1') }} Členství

#### Jak přesně funguje členství?

Dokud máš aktivní předplatné, tak jsi členem klubu a máš přístup do klubovny. Ta má podobu uzavřeného komunitního chatu na službě [Discord](https://discord.com/). K členství se mohou vázat i další výhody, které jsou nad rámec Discordu, například přístup k záznamům přednášek, možnost vyhrát lístek na konferenci, sleva u partnerů klubu, apod., ale bez čtení Discordu se o nich nemáš jak dovědět, veškerá komunikace probíhá tam.

#### Můžu být v klubu anonymní?

Je pochopitelné, pokud máš obavu řešit své problémy před zraky potenciálních zaměstnavatelů. V klubu se díky přátelskému a chápavému prostředí bavíme dost otevřeně, ale pokud se na to necítíš, bez problémů můžeš klub využívat i anonymně. Pro registraci na junior.guru sice musíš zadat jméno, ale to se objeví jen na účetním dokladu. Na Discordu můžeš být klidně „beruška42“ a každý o tobě bude vědět pouze to, co o sobě prozradíš.

### {{ 'person-check'|icon('text-primary me-1') }} Pro koho je klub

#### Je klub pouze pro začátečníky?

Jsou mezi námi nejen junioři na všech úrovních znalostí, ale i mnozí senioři, profesionální mentoři, náboráři, psychologové a další. V pestrosti je síla!

#### Co mám z členství v klubu jako senior(ka)?  {: #seniori }

Zatímco čekáš na poště, můžeš někoho posunout o kousek blíž vysněné kariéře v IT. Stačí ti „poflakovat“ se na Discordu, pokud máš zrovna čas. Když vidíš příležitost někomu pomoci, zkusíš pomoci. Někdy to může být debugovací seance na hodinu, někdy dva krátké příspěvky, někdy jedno emoji s palcem nahoru. Nemusíš mít učitelské nadání, stačí [když ti ego nebrání v laskavosti a respektu k druhým](coc.md). Navíc finančně přispíváš na provoz a rozšiřování [otevřených](https://github.com/honzajavorek/junior.guru/) materiálů pro začátečníky, ve kterých nejde o senzační titulky, ale o upřímné a dobře míněné rady.

#### Co mám z členství v klubu jako profesionál(ka) na volné noze?

Kromě [konání dobra](#seniori) můžeš klub naplno využít k propagaci svých aktivit. Ve vyhrazených kanálech klidně zvi členy na svá komerční školení, propaguj svou nabídku mentoringu, upozorňuj na svá videa nebo knihy. Můžeš členům nabídnout slevu, ale nemusíš. Buduj si osobní značku, ať začátečníci ví, kdo je tady ten expert na bezpečnost, nebo na frontend. Ostatně, oni těmi začátečníky nebudou věčně a kromě nich to v klubu uvidí i spousta zajímavých seniorů.

#### Co mám z členství v klubu jako recruiter(ka)?

Zatímco čekáš na kafe, můžeš někoho posunout o kousek blíž vysněné kariéře v IT. Stačí ti „poflakovat“ se na Discordu, pokud máš zrovna čas. Když vidíš příležitost někomu pomoci, zkusíš pomoci. Někdy to mohou být dva krátké příspěvky, někdy jedno emoji s palcem nahoru. Klub není zdaleka jen o programování, ale i o kariérním rozhodování, pohovorech, životopisech. Můžeš si číst, jak proces náboru vnímají junioři, poskytovat zpětnou vazbu z druhé strany, radit s CVčkem, vyhlížet nadějné talenty, sdílet nabídky práce. Navíc podporuješ rozšiřování [příručky](/candidate-handbook/), díky které se můžou kandidáti lépe připravit už před tím, než se ti ozvou na inzerát.

#### Co mám z členství v klubu jako komunitní manažer(ka)?

Získáš publikum nejen mezi nastupující generací programátorek a programátorů, ale i mezi seniory, kteří mají chuť jim pomáhat. Klub můžeš naplno využít k propagaci svých aktivit. Ve vyhrazených kanálech klidně upozorňuj na srazy, konference, hackathony. Ať už jde o vstupenky nebo produkty, můžeš nabízet slevy, organizovat soutěže. Dokonce můžeš vymyslet i nějakou speciální nebo pravidelnou online akci, která se bude odehrávat přímo v klubu. Fantazii se meze nekladou!

### {{ 'compass'|icon('text-primary me-1') }} Co je a není klub

#### Jak se klub liší od škol, akademií a kurzů?

Klub není škola, je to komunita. Samotné členství v klubu tě programovat nenaučí. Je ovšem skvělým doplňkem pro všechny, kdo se programovat snaží, ať už ve škole, na kurzech, nebo zcela po vlastní ose. Klub ti pomůže objasnit kontext, vyřešit zapeklitý problém, najít doplňující materiály, zorientovat se v kariérních možnostech, získat první kontakty v oboru, najít si první práci. [Klub nenabízí ani nedoporučuje žádný konkrétní vzdělávací program](#vzdelavaci-agentury), naopak je místem, kde lze o nabídce vzdělávacích agentur diskutovat na neutrální půdě, sdílet si zkušenosti, porovnávat.

#### Jak se klub liší od individuálního mentoringu?

Online skupina nikdy nebude mít úroveň srovnatelnou s profesionálním individuálním mentoringem. Mnozí ale žádného mentora po ruce nemají, placený mentoring si nemohou dovolit, nebo jej ani neseženou, protože nabídka je omezená. Klub je méně profesionální, ale dostupnou volbou.

#### Jak se klub liší od kariérního poradenství?

Online skupina nikdy nebude mít úroveň srovnatelnou s profesionálním individuálním kariérním poradenstvím. To je ale poměrně exkluzivní službou se sazbami kolem 1.500 Kč/h a víc. Klub je méně profesionální, ale dostupnou volbou. Zaměřujeme se na odhalení a nápravu nejčastějších chyb, které lidi při hledání práce dělají, ať už jde o strategii, nebo obsah životopisu. Na rozdíl od kariérních poradců se kolektivně specializujeme na téma první práce v IT. Snažíme se rady konzultovat s recruitery, kteří v klubu také jsou.

#### Jak se klub liší od skupin na Facebooku?

V klubu se koncentrují lidé, kteří „to myslí vážně“, ať už jde o pomoc druhým, nebo vlastní rozvoj. Je to komornější, kultivované místo s [pravidly chování](coc.md), kde nehrozí, že se někdo bude vysmívat tvému dotazu. Na rozdíl od dobrovolníků spravujících facebookové skupiny, klub má správce na plný úvazek, autora junior.guru [Honzu Javorka](#honza). Ten moderuje, odpovídá, zve přednášející, vítá nové členy, otevírá nová témata a vylepšuje možnosti klubu.

### {{ 'chat-right'|icon('text-primary me-1') }} Discord

#### Proč zrovna Discord?

[Discord](https://discord.com/) sice vznikl pro hráče počítačových her, ale dnes se profiluje jako obecná komunikační platforma vhodná pro komunity. Podobně jako IRC nebo Slack se jedná o skupinový chat. Byť je jasné, že IRC [bude mít vždy své fanoušky](https://xkcd.com/1782/), Discord nabízí o několik dekád modernější prožitek. Slack se zase hodí spíš pro firemní nebo organizační týmy, než pro komunity. Velkou výhodou Discordu jsou hlasové kanály, kde si členové mohou na jeden klik volat, ať už pouze hlasově, nebo i s videem a sdílením obrazovky.

#### Mám platné členství, ale nedaří se mi dostat na Discord

Po registraci na junior.guru by ti měl přijít e-mail s odkazem na propojení. Pokud nic nepřišlo, [klikni sem](https://juniorguru.memberful.com/account/discord/authorize), to je stejný odkaz. Jestliže ještě nemáš účet na Discordu, budeš si jej muset vytvořit. Aby vše správně fungovalo, musí mít tvůj Discord účet ověřenou e-mailovou adresu. V případě problémů napiš na {{ 'ahoj@junior.guru'|email_link }}, společně to vyřešíme.

#### Mám účet na Discordu, jak jej propojím s klubem?

Jestli už Discord používáš a máš tam účet, stačí jej propojit s junior.guru. Aby vše správně fungovalo, musí mít tvůj Discord účet ověřenou e-mailovou adresu. Po registraci na junior.guru by ti měl přijít e-mail s odkazem na propojení. Pokud nic nepřišlo, [klikni sem](https://juniorguru.memberful.com/account/discord/authorize), to je stejný odkaz. V případě problémů napiš na {{ 'ahoj@junior.guru'|email_link }}, společně to vyřešíme.

### {{ 'credit-card'|icon('text-primary me-1') }} Placení

#### Proč je klub placený?

Klub neprovozuje firma, ale jednotlivec, [Honza Javorek](#honza). Jedna osoba, rodina, nájem, jídlo, a tak dále. Chci na plný úvazek pracovat pro juniory, být jejich ambasadorem, průvodcem po nelehké cestě. Stejně jako třeba doktor, nejraději bych pomohl všem, ale musím z něčeho žít. Kdybych nabízel profesionální placené konzultace, mohl by si je dovolit jen málokdo. Díky klubu si ale může kousek toho, co dělám, předplatit skoro každý. Kromě toho, čím větší podíl mají individuální členství na mých příjmech, tím nezávislejší můžu být v informacích, které poskytuji. Klient je ten, kdo posílá peníze. Když to nejsou zaměstnavatelé juniorů nebo vzdělávací agentury, ale samotní junioři, mám rozvázané ruce v tom, co si můžu dovolit. Klidně se na moje příjmy mrkni, [čísla jsou veřejná](#honza).

#### Existuje způsob, jak být v klubu zdarma?

První osadníci, kteří pomáhali klub rozjíždět v době jeho počátků, jsou v klubu zdarma, navždy. Přednášející na [klubových akcích](/events/) dostávají jako poděkování roční členství zdarma. Pro znevýhodněné skupiny lidí připravujeme speciální stipendium, ale zatím není v provozu. Pokud si tvoje firma platí v klubu členství, měla by mít k dispozici minimálně šest ročních vstupů pro své lidi. Pokud tady vidíš logo své firmy, poptej se, zda ještě nemají nevyužité vstupy.

#### Kdy musím zadat platební kartu?

Při registraci kartu zadávat nemusíš, prvních 14 dní je zdarma. Před koncem zkušebního období by ti mělo přijít e-mailem upozornění, že nemáš zadanou kartu. Pokud ji do konce zkušebního období nevyplníš, systém tě z klubu automaticky vyhodí. Skončí ti pouze přístup do klubu, účet na junior.guru ti zůstane. V [nastavení](https://juniorguru.memberful.com/account) můžeš kdykoliv později kartu vyplnit a členství obnovit. Discord účet ti samozřejmě zůstane taky.

#### Jsou údaje o mé platební kartě v bezpečí?

Jasně! K údajům o tvé kartě nemá nikdo z junior.guru přístup, jsou bezpečně uchovány platební bránou [Stripe](https://stripe.com/). Je to světoznámá služba, která má hromadu zabezpečení a certifikátů.

#### Proč mě systém vyhodil z klubu?

S největší pravděpodobností tě vyhodil proto, že nemáš vyplněny údaje o kartě, nebo proto, že tvé kartě vypršela platnost. Platební údaje lze změnit v [nastavení](https://juniorguru.memberful.com/account). Než tě systém vyhodí, měl by ti poslat e-mailové upozornění, že s kartou něco není v pořádku. Jenže to se, jak už to tak bývá, může někam zatoulat. Neboj, nepřijdeš o žádná nasbíraná ocenění a role. Discord bot pozná, že jsi zpět, a při nejbližší příležitosti ti vše zase přiřadí.

#### Kde mohu změnit údaje o platební kartě?

Údaje o kartě lze změnit v [nastavení](https://juniorguru.memberful.com/account).

#### Co když se mi z karty strhne částka, která se mi nelíbí?

Sice se to nikdy nestane, ale kdyby se to náhodou stalo, podívej se nejdříve do [nastavení](https://juniorguru.memberful.com/account), kde by měl být aktuální stav tvého předplatného. Jestliže vidíš nějaký nesoulad, neváhej napsat na {{ 'ahoj@junior.guru'|email_link }}, společně to objasníme. [Honza Javorek](#honza), provozovatel klubu, má možnost v případě jakéhokoliv problému strhnutou částku ručně vrátit zpět. Další detaily najdeš v [obchodních podmínkách](tos.md).

#### Jak zjistím stav svého předplatného?

Zjistíš to v [nastavení](https://juniorguru.memberful.com/account).

#### Jak změním předplatné, např. z měsíčního na roční?

Jde to změnit v [nastavení](https://juniorguru.memberful.com/account).

#### Jak zruším předplatné?

Předplatné můžeš zrušit v [nastavení](https://juniorguru.memberful.com/account). Pokud chceš zrušit roční předplatné, počítej s tím, že se ti nevrátí peníze za zbytek nevyužitého období. Další detaily najdeš v [obchodních podmínkách](tos.md). V případě jakéhokoliv problému neváhej napsat na {{ 'ahoj@junior.guru'|email_link }}.

### {{ 'heart'|icon('text-primary me-1') }} Dobrovolné příspěvky

#### Co když Honzu podporuji na GitHub Sponsors nebo na Patreonu?

Dlouhodobý plán je takový, že by členství v klubu zcela nahradilo původní [dobrovolné příspěvky](/donate/). Můžeš tedy příspěvky zrušit a místo nich si pořídit členství v klubu. Jestliže z nějakého důvodu příspěvky rušit nechceš, napiš prosím na {{ 'ahoj@junior.guru'|email_link }} a domluvíme se, jak to provedeme. Přístup do klubu rozhodně dostaneš.

#### Mám Honzu podporovat dobrovolnými příspěvky, nebo platit členství v klubu?

Dlouhodobý plán je takový, že by členství v klubu zcela nahradilo původní [dobrovolné příspěvky](/donate/). Můžeš tedy příspěvky zrušit a místo nich si pořídit členství v klubu. Někteří přispěvatelé ale tuto variantu dobrovolně odmítli s tím, že chtějí posílat měsíčně víc peněz, než je cena členství, a to mohou zatím pouze na GitHub Sponsors nebo na Patreonu. Pokud to máš podobně, napiš prosím na {{ 'ahoj@junior.guru'|email_link }} a domluvíme se, jak to provedeme. Přístup do klubu rozhodně dostaneš.

#### Jak mohu podporovat junior.guru, pokud mě klub nezajímá?

Zaregistruj se jako člen klubu a plať členství. Nemusíš si vytvářet účet na Discordu, ani tam chodit. V souvislosti s klubem by ti neměly chodit žádné zprávy, pouze systémová upozornění do e-mailu např. v případě, že ti končí platnost karty.

### {{ 'building'|icon('text-primary me-1') }} Spolupráce s firmami a komunitami

#### Co vyplývá z toho, že je členem klubu nějaká firma?

Každá firma, která s klubem spolupracuje, má logo nahoře na této stránce a minimálně šest vstupů pro své lidi. Dále záleží na tom, o jakou kombinaci z [ceníku](https://docs.google.com/document/d/1keFyO5aavfaNfJkKlyYha4B-UbdnMja6AhprS_76E7c/edit?usp=sharing) měli zájem a na jaké konkrétní formě spolupráce se dohodli s provozovatelem junior.guru, [Honzou Javorkem](#honza). Bývá to různé. Některé firmy zajímá nábor juniorů, tak nakupují inzeráty, další berou podporu klubu jako [CSR](https://cs.wikipedia.org/wiki/Spole%C4%8Densk%C3%A1_odpov%C4%9Bdnost_firem), jiné chtějí zviditelnit svou značku.

#### Co firma získává členstvím v klubu?

Firmy, které s klubem spolupracují, do něj mají především přístup. Mohou vyhlížet talentované juniory, promovat ve vyhrazených kanálech své aktivity, poskytovat slevy na své produkty. Mohou se zapojit do diskuzí a radit nebo poskytovat pohled z druhé strany. Mohou spolu s klubem vymýšlet různé způsoby vzájemné podpory, ať už jde o vzájemnou propagaci, slevy, nebo tvorbu společných článků, podcastů, videí. Je na vás, jak to uchopíte a co z toho „vyždímete“. Už jen tím, že svými financemi podpoříte existenci junior.guru a budete zde mít logo, si budujete dobré jméno jak mezi lidmi z nastupující generace vývojářů, tak mezi zainteresovanými profíky. Partnerství pro firmy je od 10.599 Kč/rok. Mrkněte na [ceník](https://docs.google.com/document/d/1keFyO5aavfaNfJkKlyYha4B-UbdnMja6AhprS_76E7c/edit?usp=sharing) a pokud máte zájem, pište na {{ 'ahoj@junior.guru'|email_link }}.

#### Co vyplývá z toho, že je členem klubu nějaká vzdělávací agentura?  {: #vzdelavaci-agentury :}

Klub a celé junior.guru nenabízí ani nedoporučuje žádný konkrétní vzdělávací program, je to nezávislý rozcestník. Pokud je někde odkaz na konkrétní stránku, je to proto, že je autor junior.guru, [Honza Javorek](#honza), upřímně přesvědčen o jejím jedinečném přínosu v daném kontextu. Mimo loga partnerů si na junior.guru nelze koupit žádné odkazy. Klub je místem, kde lze o nabídce firem diskutovat na neutrální půdě, sdílet si zkušenosti, porovnávat. Některé vzdělávací agentury jsou členy klubu, ale Honza si dává pozor na to, aby žádný konkrétní kurz nedoporučoval a aby aktivity v rámci partnerství nezasahovaly do nestrannosti junior.guru.

#### Co vyplývá z toho, že s klubem spolupracuje nějaká komunita?  {: #komunity }

Organizátoři komunit, které s klubem spolupracují, do něj mají přístup a mohou v něm promovat svoje aktivity. Mohou spolu s klubem vymýšlet různé způsoby vzájemné podpory, ať už jde o vzájemnou propagaci, slevy, nebo tvorbu společných článků, podcastů, videí. Je na vás, jak to uchopíte a co z toho „vyždímete“. Spolupráce by ale neměla být samoúčelná, měla by vždy vyústit něco, co bude především nějakým způsobem sloužit samotným juniorům. Partnerství pro komunity je domlouváno nepeněžní formou. Logo komunity se zde objevuje zpravidla ve chvíli, kdy jde o dlouhodobější, ne pouze jednorázovou spolupráci. Máte-li o partnerství zájem, napište na {{ 'ahoj@junior.guru'|email_link }}.

### {{ 'patch-question'|icon('text-primary me-1') }} Ostatní

#### Proč klub vznikl?

Na junior.guru byly původně pouze [rady](/motivation/) a [pracovní nabídky](/jobs/). Začátečníci však potřebují víc než jen příručku. Nejvíc je posune, když v tom všem nejsou sami a může jim někdo pomoci se zapeklitou situací, dát zpětnou vazbu, dodat motivaci. Proto klub v lednu 2020 vznikl. Kromě toho je to samozřejmě také způsob, jak celé junior.guru financovat. [Honza Javorek](#honza), autor junior.guru, svou motivaci a veškeré okolnosti vzniku klubu otevřeně popsal v [rozsáhlém článku na svém blogu](https://honzajavorek.cz/blog/spoustim-klub/).

#### Budou nové rady na junior.guru už pouze pro členy klubu?

Všechen obsah junior.guru zůstává zdarma na webu a rozhodně je v plánu jeho rozšiřování a vylepšování. Klub je způsob, jak tuto dobročinnost financovat a posunout ji na interaktivnější úroveň. [Honza Javorek](#honza), autor všech textů na junior.guru, v klubu diskutuje o nových kapitolách do příručky, sbírá tam tipy na témata, získává zpětnou vazbu. Díky klubu má každodenní kontakt s juniory a jejich radostmi i strastmi. Díky těmto synergiím může být veřejná část junior.guru lepší, než kdy mohla být bez klubu.
{% endcall %}
</section>


<section class="text-center">
  <a class="btn btn-primary btn-lg" href="#cenik">Zpět na ceník</a>
</section>
