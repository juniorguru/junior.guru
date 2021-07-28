---
title: Klub tě nastartuje
thumbnail_title: Klub tě nastartuje
main_class: main-sections
description: Přidej se na junior.guru Discord! Jsme tvoje online parta začátečníků, kteří to myslí vážně, a profesionálů s chutí pomáhat. Svoje programování nebo hledání práce posuneš o 1 % každý den.
---
{% from 'content.html' import markdown, blockquote_avatar, blockquote_toxic, logo, lead %}

<header class="masthead"><div class="masthead-container">
<div class="masthead-content">
<h1>Klub tě nastartuje</h1>

{% call lead() %}
Jsme tvoje online programovací parta. Začátečníci, kteří to myslí vážně. Profesionálové s chutí pomáhat. V klubu svoje programování nebo hledání práce <span data-annotate>posuneš o 1 % každý den</span>.
{% endcall %}

<div class="masthead-numbers">
{% call markdown() %}
- **{{ messages_count|metric }}** příspěvků
- **{{ members_total_count }}** členů
- **{{ companies|length }}** firem
- **{{ events|length }}** akcí
{% endcall %}
</div>

<a class="masthead-button primary" href="#pricing">Přidej se</a>
<a class="masthead-button secondary" href="{{ 'hire-juniors/'|url }}">Pro firmy</a>
</div>
<div class="masthead-illustration illustration-club">
  <img class="masthead-illustration-image" src="{{ 'static/images/illustration-club.svg'|url }}">
  <div class="illustration-club-members">
    {% for member in members|sample(7) %}
      <img width="50" height="50" src="{{ ('static/' + member.avatar_path)|url }}">
    {% endfor %}
  </div>
</div>
</div></header>

{#
<div class="members">
  <ul class="members-list">
    {% for member in members|sample(20) %}
    <li class="members-item">
      <img width="50" height="50" class="members-image" src="{{ ('static/' + member.avatar_path)|url }}" alt="Profilovka člena {{ member.id }}">
    </li>
    {% endfor %}
  </ul>
</div>
#}
<ul class="logos">
  <li class="logos-item logos-caption">
    <a href="{{ 'hire-juniors/'|url }}">Firemní partneři</a>:
  </li>
  {% for company in companies %}
    {{ logo(company.name, company.filename, company.link) }}
  {% endfor %}
</ul>
<ul class="logos grayscale">
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

<section>

<h2>Co je klub?</h2>
{% call lead() %}
Kdyby šlo o hudbu, tak nejsme kytarová škola, ale místo, kam pravidelně chodíš a kde najdeš podporu, nápady, kamarády, tipy na složitější akordy a kde možná potkáš někoho, s kým založíš kapelu. Nejsme kurz, jsme online komunita. Kroužek. Discord. Skaut pro programátory. Ženeme tě vpřed, ale zároveň u nás najdeš rady a podporu, když ti něco nejde.
{% endcall %}
<div class="margin-standout"><div class="icons">
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

<h2>Neztrácej čas záplavou názorů</h2>

{% call lead() %}
Rady kolemjdoucích ve veřejných skupinách jsou náchylné k fanouškovství, opakují [nejrůznější mýty](/motivation/#myths), doporučují staré postupy, nebo vycházejí z toho, že co vyhovovalo jednomu, zákonitě platí i pro druhého. Je běžné, že na jednoduchou otázku dostaneš desítky rozcházejících se a mnohdy i zcela nevhodných odpovědí.

V klubu vycházíme z konkrétní cesty jak postupovat, která se osvědčila na mnoha začátečnících. Zároveň se snažíme radit objektivně a brát ohled na tvou situaci. Poskytneme ti různé pohledy, ale zároveň jasný směr. Místo abychom tě utopili v možnostech, pomůžeme ti rozhodnout se.
{% endcall %}

<div class="margin-standout"><div class="comparison">
{% call markdown() %}
{% set check = 'check-circle-fill'|icon('text-success') %}
{% set cross = 'x-square-fill'|icon('text-danger') %}

| Osobní mentor                       | Klub junior.guru                                | Veřejné skupiny                      |
|-------------------------------------|-------------------------------------------------|--------------------------------------|
| {{ check }} exkluzivní kvalita      | {{ check }} dostatečná kvalita                  | {{ cross }} kvantita                 |
| {{ cross }} drahé                   | {{ check }} dostupné                            | {{ check }} zdarma                   |
| {{ check }} osobní vztah            | {{ check }} komunita                            | {{ cross }} anonymita                |
| {{ check }} odborník na plný úvazek | {{ check }} správce na plný úvazek              | {{ cross }} správce dobro&shy;volník |
| {{ check }} radí odborník           | {{ check }} radí anga&shy;žo&shy;vaní odborníci | {{ cross }} radí ko&shy;lemjdoucí    |
| {{ cross }} obtížně dostupné        | {{ check }} dostupné                            | {{ check }} všudy&shy;přítomné       |
{% endcall %}
</div></div>

</section></div>
<section>

<h2>Neztrácej čas s hulváty a sexisty</h2>
{% call lead() %}
V klubu neexistují hloupé otázky a nemáme potřebu někoho stírat. Mezi členy je mnoho žen a uslintané vtipy u nás nikoho nezajímají. Respektujeme se, pomáháme si, jsme k sobě laskaví a profesionální. Případné excesy se řídí [pravidly chování](/coc/).
{% endcall %}
<div class="blockquotes-2">
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

</section>
<div id="pricing" class="section-background yellow-light"><section>

<div class="pricing-container">
  <h2>Vyzkoušej to zdarma!</h2>
  <div class="pricing">
    <div class="pricing-block">
      <h3 class="pricing-heading">Ročně</h3>
      <ul class="pricing-benefits">
        <li class="pricing-benefits-item">Prvních 14 dní zdarma</li>
        <li class="pricing-benefits-item">Jeden měsíc ušetříš</li>
      </ul>
      <a class="pricing-button" href="https://juniorguru.memberful.com/checkout?plan=59574">1199 Kč ročně</a>
    </div>
    <div class="pricing-block">
      <h3 class="pricing-heading">Měsíčně</h3>
      <ul class="pricing-benefits">
        <li class="pricing-benefits-item">Prvních 14 dní zdarma</li>
        <li class="pricing-benefits-item">Můžeš to kdykoliv zrušit</li>
      </ul>
      <a class="pricing-button" href="https://juniorguru.memberful.com/checkout?plan=59515">109 Kč měsíčně</a>
    </div>
    <div class="pricing-block">
      <h3 class="pricing-heading">Stipendium</h3>
      <ul class="pricing-benefits">
        <li class="pricing-benefits-item">Podpora pro znevýhodněné</li>
        <li class="pricing-benefits-item">Vyplň formulář a uvidíš</li>
      </ul>
      <strong class="pricing-button disabled">Připravuje se</strong>
    </div>
  </div>
</div>
{#
    TODO

    Klub spolupracuje s Engeto Academy a Software Development Academy. Někteří jejich absolventi mohou dostat tři měsíce členství v klubu zdarma. Pokud u nich studuješ, kontaktuj je a ověř si, zda to náhodou není tvůj případ.
#}

</section></div>
<section>
{% call markdown() %}

## Otázky a odpovědi

### Komunity {: #communities }

TBD

{% endcall %}
</section>
