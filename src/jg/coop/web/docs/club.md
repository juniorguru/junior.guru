---
title: Klub pro začátečníky v programování
template: main_club.html
description: Přidej se na junior.guru Discord! Jsme tvoje online programovací parta, skupina, fórum. Začátečníci, kteří to myslí vážně. Profesionálové s chutí pomáhat. Svoje programování nebo hledání práce posuneš o 1 % každý den.
---

{% from 'macros.html' import img, markdown, blockquote_avatar, blockquote_toxic, lead, logos_sponsors_by_tier, logos_list, event_circle with context %}


<header class="masthead"><div class="masthead-container">
<div class="masthead-column">
<h1>Tvoje programovací parta</h1>
<div class="masthead-body">

{% call lead() %}
Začátečníci, kteří to myslí vážně. Profesionálové s chutí pomáhat. V klubu svoje programování nebo hledání práce posuneš o **1 % každý den**.
{% endcall %}

<div class="masthead-numbers">
{% set years = today.year - 2021 %}
{% call markdown() %}
- **{{ years }}** {{ years|nplurals("rok", "roky", "let") }}
- **{{ members_total_count }}** členů
- **{{ charts.members_women_today|round|int }} %** žen
- **{{ events|length }}** online akcí
{% endcall %}
</div>

<div class="masthead-row">
<a class="masthead-button" href="#cenik">Přidej se</a>
<div class="masthead-members"><span class="members">
    {% for member in members|sample(8) %}
      {{ img('static/' + member.avatar_path, 'Profilovka člena klubu', 50, 50, lazy=False) }}
    {% endfor %}
</span></div>
</div>

</div></div>
<div class="masthead-column masthead-video-container">
  <lite-youtube class="video" videoid="zHt4z5lp2e0" playlabel="Přehrát představení klubu" params="rel=0&modestbranding=1">
    <a href="https://www.youtube.com/watch?v=zHt4z5lp2e0" target="_blank" rel="noopener noreferrer" class="lyt-playbtn" title="Přehrát představení klubu">
      <span class="lyt-visually-hidden">Přehrát představení klubu</span>
    </a>
  </lite-youtube>
</div>
</div></header>

<section class="section">
<h2>Získej parťáky, mentory, kamarády</h2>
{% call lead() %}
Začátečníci potřebují víc než [příručku](handbook/index.md). Nejvíc je posune, **když v tom všem nejsou sami**. Když jim někdo může pomoci se zapeklitou situací, dát zpětnou vazbu, dodat motivaci.

Jsme **online komunita** na [Discordu](https://discord.com/). Občas pořádáme přednášky, ale nejsme škola, neděláme kurzy. Sdílíme si tipy a postřehy. Podporujeme se a radíme, když někomu něco nejde, ať už jde o seniora nebo juniora. Dáváme si zpětnou vazbu. Dohazujeme si práci. Společně se radujeme z úspěchů. Můžeš se aktivně zapojit, nebo vše jen potichu sledovat.
{% endcall %}

<div class="standout"><div class="topics">
{% call markdown() %}
- {{ 'play-btn'|icon }} Online klubové akce
- {{ 'clock-history'|icon }} Archiv záznamů akcí
- {{ 'list-check'|icon }} Pracovní nabídky
- {{ 'compass'|icon }} Kariérní konzultace
- {{ 'person-check'|icon }} Zpětná vazba na CV
- {{ 'code-slash'|icon }} Zpětná vazba na kód
- {{ 'chat-dots'|icon }} Recenze a zkušenosti
- {{ 'heart'|icon }} Podpora a pochopení
- {{ 'person-plus'|icon }} Komunita, síť kontaktů
- {{ 'lightbulb'|icon }} Mentoring od profíků
- {{ 'patch-plus'|icon }} Slevy a soutěže
- {{ 'hand-thumbs-up'|icon }} Podporuješ junior.guru
{% endcall %}
</div></div>
<div class="blockquotes-2">
{{ blockquote_avatar(
  'Jemně popostrkující a nějakou činnost vyvolávající a podněcující síla, kterou jsem potřebovala. Nacpat se sem byl moc dobrej napád.',
  'radka.jpg',
  'Radka',
  'Radka'
) }}
{{ blockquote_avatar(
  'Jako kluka z vesnice mě na programování vždy štvalo, že jsem na to byl hrozně moc sám. Jsem opravdu vděčný za tuto komunitu.',
  'lukas.jpg',
  'Lukáš',
  'Lukáš'
) }}
</div>
</section>

<section class="section">
<h2>Jaká témata zajímají členy klubu</h2>
{% call lead() %}
Chceš mít jistotu, že v klubu najdeš lidi, které zajímá totéž co tebe? Že najdeš publikum pro svůj dotaz nebo parťáky pro svůj projekt? Podívej se, co o svých zájmech prozradili sami členové.
{% endcall %}
<ul class="interests standout-top">
{% set max_members_count = interests|map(attribute=1)|max %}
{% for role, members_count in interests[:12] %}
  {% set shade_index = 7 - ((members_count / max_members_count) * 6)|round(0, 'floor')|int %}
  <li class="interests-item shade-{{ shade_index }}">
    <span class="interests-icon-container">
      {{ img('static/' + role.icon_path, 'Logo: ' + role.interest_name, 50, 50, lazy=False, class="interests-icon") }}
    </span>
    <strong class="interests-name">{{ role.interest_name|replace(' a ', ' a ') }}</strong>
    <span class="interests-badge">{{ members_count }} členů</span>
  </li>
{% endfor %}
</ul>
</section>

<div class="section-background blue-light"><section class="section">
<h2>Užívej si přednášky pro začátečníky</h2>
{% call lead() %}
Jednou za čas máme na Discordu večerní akci. Je to **online a zhruba na hodinku**, takže můžeš zůstat v bačkorách a stihneš potom díl seriálu, uspat děti, nebo oboje. Můžeš pokládat dotazy, nebo si to jen pustit do uší při vaření večeře. **Záznamy minulých akcí** máš na YouTube. A to nejlepší nakonec: Téma i pojetí je vždy **vyloženě pro začátečníky**! Žádná záplava odborných „termitů“, které ti nikdo nevysvětlil.
{% endcall %}

<ul class="event-circles standout">
{% for event in events_promo|selectattr('public_recording_url')|sample(1) %}
  {{ event_circle(event) }}
{% endfor %}
{% for event in events_promo|rejectattr('public_recording_url')|sample(5) %}
  {{ event_circle(event) }}
{% endfor %}
</ul>
<div class="text-center">
  <a class="btn btn-lg btn-outline-primary" href="{{ pages|docs_url('events.md')|url }}">
    Všechny akce
  </a>
</div>
</section></div>


<section class="section">
<h2>Propoj se s lidmi z oboru</h2>
{% call lead() %}
O klub se stará **Honza Javorek, autor junior.guru**. Okolo se však „poflakuje“ i řada dalších **profíků s chutí pomáhat**. S **firmami**, které klub podporují, podnikáme různé aktivity, například mentoring nebo propojování juniorů s jejich recruitery. Partnerství s **programátorskými komunitami** ti zase rozšíří možnosti zapojit se i jinde, dovědět se o zajímavých akcích, případně na ně získat slevu. S lidmi ze všech těchto organizací se můžeš v klubu potkat a propojit.

Potkáš u nás samozřejmě i **stejné začátečníky, jako jsi ty**. Každý s jiným životním příběhem, ale s velmi podobnými dotazy a problémy.
{% endcall %}
<div class="standout-bottom">{{ logos_sponsors_by_tier(sponsors_by_tier, dark=True) }}</div>
{{ logos_list(partners, class="mb-0", dark=True) }}
</section>


<div class="section-background blue-light"><section class="section">
<h2>Ptej se bez obav</h2>
{% call lead() %}
Respektujeme se, pomáháme si, jsme k sobě laskaví a profesionální. **Hloupé otázky neexistují,** nemáme potřebu někoho stírat. **Uslintané vtipy nikoho nezajímají,** mezi členy jsou ženy, muži, staří, mladí.
{% endcall %}
<div class="blockquotes-2 standout">
{{ blockquote_avatar(
  'Ty diskuze jsou úžasné. Když to lidi zaplatí, tak je to úplně jiné. Extrémně kultivované, srozumitelné, každý příspěvek dává smysl.',
  'jakub-mrozek.jpg',
  'Jakub',
  'Jakub'
) }}
{{ blockquote_avatar(
  'Je problém najít komunitu, která je o vzájemný pomoci a výměně informací, ne o honění ega. Tady je to krásná výjimka. Jsem ráda, že toho můžu být součástí.',
  'hanka.jpg',
  'Hanka',
  'Hanka'
) }}
</div>
{% call lead() %}
Šetři čas a energii. Posouvej se vpřed bez zakopávání o nezralé názory, hulváty, sexisty a přebujelá ega. Případné úlety se u nás řídí [pravidly chování](coc.md).
{% endcall %}
<div class="blockquotes-2 standout-top">
{{ blockquote_toxic(
  'Asistentky? Nene, my máme asistenty, na tuhle pozici se holka nemůže dostat. Neuměla by otvírat pivo a zahřívat playstation',
  'Vojtěch P., skupina Programátoři začátečníci na FB',
  'https://www.facebook.com/groups/144621756262987/posts/840617993330023/?comment_id=841544619904027'
) }}
{{ blockquote_toxic(
  'Možná by jsi měl držet hubu p*** když se tě nikdo na nic neptá č*****',
  'Darken Joe S., skupina Programátoři na FB',
  'https://www.facebook.com/groups/193575630828729/posts/1740414872811456'
) }}
</div>
</section></div>


<section class="section">
<h2>Nech si radit od profíků</h2>
{% call lead() %}
Vycházíme z [postupu](handbook/index.md), který je založen na reálných zkušenostech a **osvědčil se mnohým začátečníkům**. Snažíme se však radit objektivně a brát ohled i na tvou konkrétní situaci. Než abychom tě utopili v možnostech, **pomůžeme ti s rozhodováním**. Poskytneme ti sice různé pohledy, ale taky **jasný směr**. Profíci, kteří šli do klubu, to udělali ze zájmu o juniory a **s chutí pomáhat**, nejsou to náhodní kolemjdoucí.
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
Rady kolemjdoucích ve veřejných skupinách jsou náchylné k fanouškovství, opakují [nejrůznější mýty](handbook/myths.md), doporučují staré postupy. Vycházejí z toho, že když něco vyhovovalo jednomu, zákonitě musí i druhému. Na jednoduchou otázku běžně dostaneš **desítky rozcházejících se odpovědí**, mnohdy zcela nevhodných.
{% endcall %}
</section>


<div id="cenik" class="section-background yellow"><section class="section">

<h2>Přidej se k nám</h2>
{% call lead() %}
Zaregistruj se a nakoukni, jak to u nás vypadá. Kartu nezadáváš. Klidně si všechno nejdřív vyzkoušej. Pokud ti klub nesedne, prostě akorát po dvou týdnech nedoplníš platební údaje a systém tě automaticky odebere.
{% endcall %}

<div class="pricing standout">
  <div class="pricing-block pulse-hover">
    <h3 class="pricing-heading">Zdarma na 14 dní</h3>
    <p class="pricing-subheading">Potom <strong>199 Kč</strong> měsíčně<sup>*</sup></p>
    <ul class="pricing-benefits">
      {# <li class="pricing-benefits-item price"><strong>Zdarma na 14 dní</strong></li> #}
      <li class="pricing-benefits-item">{{ 'check-circle-fill'|icon }} Bez zadávání karty, bez placení</li>
      <li class="pricing-benefits-item">{{ 'check-circle-fill'|icon }} Po 2 týdnech se rozhodneš</li>
      <li class="pricing-benefits-item">{{ 'check-circle-fill'|icon }} I potom to jde kdykoliv zrušit</li>
    </ul>
    <a class="pricing-button" href="https://juniorguru.memberful.com/checkout?plan=89511">Bezplatně vyzkoušet</a>
  </div>
</div>

{% call markdown() %}
[Obchodní podmínky](tos.md) jsou napsané lidsky, klidně si je projdi. Je to smlouva, kterou mezi sebou budeme mít. Odkazuje se na [pravidla chování](coc.md), tak na ně taky mrkni, ať znáš mantinely a víš kam pro pomoc. [Zásady ochrany osobních údajů](privacy.md) popisují, jaká data o tobě Honza má a jak s nimi zachází.
{% endcall %}

<p class="pricing-note">
  <small>
    <sup>*</sup> Žádný háček, ani skrytá podmínka. Tohle je jen poznámka na okraj, že pokud by se ti v klubu líbilo, ale 199 Kč měsíčně je na tebe moc, můžeš <a href="{{ pages|docs_url('finaid.md')|url }}">požádat o roční stipendium</a>.
  </small>
</p>
</section></div>


<section class="section">
<h2>Otázky?</h2>
{% call lead() %}
Vrtá ti hlavou, jak přesně to celé funguje? Máš nějaké problémy s registrací nebo s Discordem? Zajímají tě veškeré detaily ohledně placení? Vypršela ti platnost karty? Prolétni si **otázky a odpovědi**.
{% endcall %}

<div class="standout-top"><div class="topics topics-grid">
{% call markdown() %}
- [{{ 'person-plus'|icon }} Členství v klubu](faq.md#jak-funguje-clenstvi)
- [{{ 'person-check'|icon }} Pro koho je klub](faq.md#je-to-jen-pro-zacatecniky)
- [{{ 'compass'|icon }} Co je a není klub](faq.md#jak-se-klub-lisi-od-skol-akademii-a-kurzu)
- [{{ 'chat-right'|icon }} Discord](faq.md#proc-zrovna-discord)
- [{{ 'credit-card'|icon }} Placení za klub](faq.md#proc-je-klub-placeny)
- [{{ 'three-dots'|icon }} Další](faq.md)
{% endcall %}
</div></div>
</section>
