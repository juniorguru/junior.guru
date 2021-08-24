---
title: Klub pro začátečníky v programování
thumbnail_badge: 109 Kč/měs
main_class: main-sections
description: Přidej se na junior.guru Discord! Jsme tvoje online programovací parta, skupina, fórum. Začátečníci, kteří to myslí vážně. Profesionálové s chutí pomáhat. Svoje programování nebo hledání práce posuneš o 1 % každý den.
---

{% from 'shared.html' import img %}
{% from 'docs.html' import markdown, blockquote_avatar, blockquote_toxic, logo, lead, event_circle %}


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
<h2>Získej parťáky, mentory, kamarády</h2>
{% call lead() %}
Začátečníci potřebují víc než [příručku](/learn/). Nejvíc je posune, **když v tom všem nejsou sami**. Když jim někdo může pomoci se zapeklitou situací, dát zpětnou vazbu, dodat motivaci.

Jsme **online komunita** na [Discordu](https://discord.com/). Občas pořádáme přednášky, ale nejsme škola, neděláme kurzy. Sdílíme si tipy a postřehy. Podporujeme se a radíme, když někomu něco nejde. Někteří díky klubu seženou práci. Dáváme si zpětnou vazbu. Společně se radujeme z úspěchů. Můžeš se aktivně zapojit, nebo vše jen potichu sledovat.
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
<div class="blockquotes-2">
{{ blockquote_avatar('Jemně popostrkující a nějakou činnost vyvolávající a podněcující síla, kterou jsem potřebovala. Nacpat se sem byl moc dobrej napád.', 'radka.png', 'Radka', 'Radka') }}

{{ blockquote_avatar('Jako kluka z vesnice mě na programování vždy štvalo, že jsem na to byl hrozně moc sám. Jsem opravdu vděčný za tuto komunitu.', 'lukas.png', 'Lukáš', 'Lukáš') }}
</div>
</section>


<div class="section-background blue-light"><section>
<h2>Užívej si přednášky pro začátečníky</h2>
{% call lead() %}
Jednou za čas máme na Discordu večerní akci. Je to **online a zhruba na hodinku**, takže můžeš zůstat v bačkorách a stihneš potom díl seriálu, uspat děti, nebo oboje. Můžeš pokládat dotazy, nebo si to jen pustit do uší při vaření večeře. **Záznamy minulých akcí** máš na YouTube. A to nejlepší nakonec: Téma i pojetí je vždy **vyloženě pro začátečníky**! Žádná záplava odborných termitů, které ti nikdo nevysvětlil.
{% endcall %}

<ul class="event-circles standout">
{% for event in events|selectattr('recording_url')|selectattr('is_public', 'true')|sample(1) %}
  {{ event_circle(event) }}
{% endfor %}
{% for event in events|selectattr('recording_url')|selectattr('is_public', 'false')|sample(5) %}
  {{ event_circle(event) }}
{% endfor %}
</ul>
<div class="standout text-center">
  <a class="btn btn-lg btn-outline-primary" href="/events/">
    Všechny akce
  </a>
</div>
</section></div>


<section>
<h2>Propoj se s lidmi z oboru</h2>
{% call lead() %}
O klub se stará **Honza Javorek, autor junior.guru**. Okolo se však „poflakuje“ i řada dalších **profíků s chutí pomáhat**. S **firmami**, které klub podporují, podnikáme různé aktivity, například mentoring nebo propojování juniorů s jejich recruitery. Partnerství s **programátorskými komunitami** ti zase rozšíří možnosti zapojit se i jinde, dovědět se o zajímavých akcích, případně na ně získat slevu. S lidmi ze všech těchto organizací se můžeš v klubu potkat a propojit.

Potkáš u nás samozřejmě i **stejné začátečníky, jako jsi ty**. Každý s jiným životním příběhem, ale s velmi podobnými dotazy a problémy.
{% endcall %}
<ul class="logos standout">
  <li class="logos-item logos-caption">
    <a href="https://docs.google.com/document/d/1keFyO5aavfaNfJkKlyYha4B-UbdnMja6AhprS_76E7c/edit?usp=sharing" target="_blank" rel="noopener">Firemní partneři</a>:
  </li>
  {% for company in companies %}
    {{ logo(company.name, company.filename, company.link) }}
  {% endfor %}
</ul>
<ul class="logos grayscale standout">
  <li class="logos-item logos-caption">
    <a href="{{ pages|docs_url('faq.md')|url }}#komunity">Komunitní partneři</a>:
  </li>
  {{ logo('Česko.Digital', 'ceskodigital.svg', 'https://cesko.digital/') }}
  {{ logo('DigiKoalice', 'digikoalice.svg', 'https://digikoalice.cz/') }}
  {{ logo('Frontendisti', 'frontendisti.svg', 'https://frontendisti.cz/') }}
  {{ logo('#HolkyzMarketingu', 'holkyzmarketingu.svg', 'https://holkyzmarketingu.cz/') }}
  {{ logo('PyLadies', 'pyladies.svg', 'https://pyladies.cz/') }}
  {{ logo('Pyvec', 'pyvec.svg', 'https://pyvec.org/') }}
  {{ logo('CyberMagnolia', 'cybermagnolia.svg', 'https://cybermagnolia.com/') }}
  {{ logo('ReactGirls', 'reactgirls.svg', 'https://reactgirls.com/') }}
  {{ logo('yablko', 'yablko.svg', 'http://robweb.sk/') }}
</ul>
</section>


<div class="section-background blue-light"><section>
<h2>Ptej se bez obav</h2>
{% call lead() %}
Respektujeme se, pomáháme si, jsme k sobě laskaví a profesionální. **Hloupé otázky neexistují,** nemáme potřebu někoho stírat. **Uslintané vtipy nikoho nezajímají,** mezi členy jsou ženy, muži, staří, mladí.
{% endcall %}
<div class="blockquotes-2 standout">
{{ blockquote_avatar('Ty diskuze jsou úžasné. Když to lidi zaplatí, tak je to úplně jiné. Extrémně kultivované, srozumitelné, každý příspěvek dává smysl.', 'jakub.png', 'Jakub', 'Jakub') }}

{{ blockquote_avatar('Je problém najít komunitu, která je o vzájemný pomoci a výměně informací, ne o honění ega. Tady je to krásná výjimka. Jsem ráda, že toho můžu být součástí.', 'hanka.png', 'Hanka', 'Hanka') }}
</div>
{% call lead() %}
Šetři čas a energii. Posouvej se vpřed bez zakopávání o nezralé názory, hulváty, sexisty a přebujelá ega. Případné úlety se u nás řídí [pravidly chování](coc.md).
{% endcall %}
<div class="blockquotes-2 standout">
{{
  blockquote_toxic(
    'Asistentky? Nene, my máme asistenty, na tuhle pozici se holka nemůže dostat. Neuměla by otvírat pivo a zahřívat playstation',
    'Vojtěch P.',
    'skupina Programátoři začátečníci na FB',
    'https://www.facebook.com/groups/144621756262987/posts/840617993330023/?comment_id=841544619904027'
  )
}}
{{
  blockquote_toxic(
    'Možná by jsi měl držet hubu p*** když se tě nikdo na nic neptá č*****',
    'Darken Joe S.',
    'skupina Programátoři na FB',
    'https://www.facebook.com/groups/193575630828729/posts/1740414872811456'
  )
}}
</div>
</section></div>


<section>
<h2>Nech si radit od profíků</h2>
{% call lead() %}
Vycházíme z [postupu](/learn/), který je založen na reálných zkušenostech a **osvědčil se mnohým začátečníkům**. Snažíme se však radit objektivně a brát ohled i na tvou konkrétní situaci. Než abychom tě utopili v možnostech, **pomůžeme ti s rozhodováním**. Poskytneme ti sice různé pohledy, ale taky **jasný směr**. Profíci, kteří šli do klubu, to udělali ze zájmu o juniory a **s chutí pomáhat**, nejsou to náhodní kolemjdoucí.
{% endcall %}

<div class="standout"><div class="comparison">
{% call markdown() %}
{% set check = 'check-circle-fill'|icon('text-success') %}
{% set cross = 'x-square-fill'|icon('text-danger') %}

| Veřejné skupiny                      | Klub junior.guru                              | Osobní mentor                  |
|--------------------------------------|-----------------------------------------------|--------------------------------|
| {{ cross }} kvantita                 | {{ check }} dostatečná kvalita                | {{ check }} exkluzivní kvalita |
| {{ check }} zdarma                   | {{ check }} dostupné                          | {{ cross }} drahé              |
| {{ cross }} ko&shy;lemjdoucí         | {{ check }} komunita                          | {{ check }} osobní vztah       |
| {{ cross }} radí kdokoliv            | {{ check }} radí anga&shy;žo&shy;vaní profíci | {{ check }} radí odborník      |
| {{ cross }} správce dobro&shy;volník | {{ check }} správce na plný úvazek            | {{ check }} na plný úvazek     |
| {{ check }} všudy&shy;přítomné       | {{ check }} dostupné                          | {{ cross }} obtížně dostupné   |
{% endcall %}
</div></div>

{% call lead() %}
Rady kolemjdoucích ve veřejných skupinách jsou náchylné k fanouškovství, opakují [nejrůznější mýty](/motivation/#myths), doporučují staré postupy. Vycházejí z toho, že když něco vyhovovalo jednomu, zákonitě musí i druhému. Na jednoduchou otázku běžně dostaneš **desítky rozcházejících se odpovědí**, mnohdy zcela nevhodných.
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

{% call markdown() %}
[Obchodní podmínky](tos.md) jsou napsané lidsky, klidně si je projdi. Je to smlouva, kterou mezi sebou budeme mít. Odkazuje se na [pravidla chování](coc.md), tak na ně taky mrkni, ať znáš mantinely a víš kam pro pomoc. [Zásady ochrany osobních údajů](privacy.md) popisují, jaká data o tobě Honza má a jak s nimi zachází.
{% endcall %}
</section></div>


<section>
<h2>Otázky?</h2>
{% call lead() %}
Vrtá ti hlavou, jak přesně to celé funguje? Máš nějaké problémy s registrací nebo s Discordem? Zajímají tě veškeré detaily ohledně placení? Vypršela ti platnost karty? Prolétni si **otázky a odpovědi**.
{% endcall %}
<div class="standout text-center">
  <a class="btn btn-lg btn-outline-primary" href="{{ pages|docs_url('faq.md')|url }}">
    Chci odpovědi
  </a>
</div>
</section>
