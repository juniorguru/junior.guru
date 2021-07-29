---
title: Klub pro začátečníky v programování
thumbnail_title: Klub pro začátečníky v programování
main_class: main-sections
description: Přidej se na junior.guru Discord! Jsme tvoje online programovací parta, skupina, fórum. Začátečníci, kteří to myslí vážně. Profesionálové s chutí pomáhat. Svoje programování nebo hledání práce posuneš o 1 % každý den.
---
{% from 'content.html' import markdown, blockquote_avatar, blockquote_toxic, logo, lead %}


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

<a class="masthead-button primary pulse" href="#pricing">Přidej se</a>
<span class="masthead-members">
  {% for member in members|sample(8) %}
    <img width="50" height="50" src="{{ ('static/' + member.avatar_path)|url }}" alt="Profilovka člena {{ member.id }}">
  {% endfor %}
</span>

</div>
<img class="masthead-illustration" src="{{ 'static/images/illustration-club.svg'|url }}">
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
    <a href="#communities">Komunitní partneři</a>:
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
Nemáme potřebu někoho stírat. **Hloupé otázky neexistují** a uslintané vtipy nikoho nezajímají. Mezi členy jsou ženy, muži, staří, mladí. **Respektujeme se**, pomáháme si, jsme k sobě laskaví a profesionální. Případné úlety se řídí [pravidly chování](/coc/).
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
Odborníci, kteří vstoupili do klubu, to udělali ze zájmu o juniory a **s chutí pomáhat**. Vycházíme z [konkrétní cesty jak postupovat](/learn/), která se **osvědčila na mnoha začátečnících**. Zároveň se snažíme radit objektivně a brát ohled na tvou situaci. Poskytneme ti různé pohledy, ale zároveň **jasný směr**. Místo abychom tě utopili v možnostech, pomůžeme ti rozhodnout se.
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


<div id="pricing" class="section-background yellow"><section>

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

## Otázky a odpovědi

### Komunity {: #communities }

TBD

{% endcall %}
</section>
