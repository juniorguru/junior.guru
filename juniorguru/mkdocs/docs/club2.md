---
title: Klub tě nastartuje
thumbnail_title: Klub tě nastartuje
main_class: main-sections
description: Přidej se na junior.guru Discord! Jsme tvoje online parta začátečníků, kteří to myslí vážně, a profesionálů s chutí pomáhat. Svoje programování nebo hledání práce posuneš o 1 % každý den.
---
{% from 'content.html' import blockquote_avatar, blockquote_toxic, logo %}

# Klub tě nastartuje

<div class="lead" markdown="1">
Jsme tvoje online programovací parta. Začátečníci, kteří to myslí vážně, a profesionálové s chutí pomáhat. V klubu svoje programování nebo hledání práce posuneš o 1 % každý den.
</div>

<div class="numbers" markdown="1">
- **{{ members_total_count }}** členů
- **{{ companies|length }}** firemních členů
- **{{ events|length }}** klubových akcí
- **{{ club_elapsed_months }}** měsíců provozu
</div>

<a class="btn btn-primary" href="#pricing">Přidej se</a>
<a class="btn btn-outline-primary" href="#companies">Pro firmy</a>

<div class="members">
    <ul class="members-list">
        {% for member in members|sample(50) %}
        <li class="members-item">
            <img width="50" height="50" class="members-image" src="{{ ('static/' + member.avatar_path)|url }}" alt="Profilovka člena {{ member.id }}">
        </li>
        {% endfor %}
    </ul>
</div>

<ul class="logos">
    <li class="logos-item logos-caption">
        <a href="#companies">Firemní partneři</a>:
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

<section markdown="1">

## Co je klub?

<div class="blockquotes-2">
{{ blockquote_avatar('Jemně popostrkující a nějakou činnost vyvolávající a podněcující síla, kterou jsem potřebovala. Nacpat se sem byl moc dobrej napád.', 'radka.png', 'Radka', 'Radka') }}

{{ blockquote_avatar('Jako kluka z vesnice mě na programování vždy štvalo, že jsem na to byl hrozně moc sám. Jsem opravdu vděčný za tuto komunitu.', 'lukas.png', 'Lukáš', 'Lukáš') }}
</div>

Kdyby šlo o hudbu, tak nejsme kytarová škola, ale místo, kam pravidelně chodíš a kde najdeš podporu, nápady, kamarády, tipy na složitější akordy a kde možná potkáš někoho, s kým založíš kapelu. Nejsme kurz, jsme online komunita. Kroužek. Discord. Skaut pro programátory. Ženeme tě vpřed, ale zároveň u nás najdeš rady a podporu, když ti něco nejde.

<div class="icons">
    <ul class="icons-list">
        <li class="icons-item">
            <i class="bi bi-play-btn"></i>
            Online klubové akce
        </li>
        <li class="icons-item">
            <i class="bi bi-clock-history"></i>
            Archiv záznamů akcí
        </li>
        <li class="icons-item">
            <i class="bi bi-list-check"></i>
            Pracovní nabídky
        </li>
        <li class="icons-item">
            <i class="bi bi-compass"></i>
            Kariérní konzultace
        </li>
        <li class="icons-item">
            <i class="bi bi-person-check"></i>
            Zpětná vazba na&nbsp;CV
        </li>
        <li class="icons-item">
            <i class="bi bi-code-slash"></i>
            Zpětná vazba na&nbsp;kód
        </li>
        <li class="icons-item">
            <i class="bi bi-chat-dots"></i>
            Recenze a&nbsp;zkušenosti
        </li>
        <li class="icons-item">
            <i class="bi bi-heart"></i>
            Podpora a&nbsp;pochopení
        </li>
        <li class="icons-item">
            <i class="bi bi-person-plus"></i>
            Komunita, síť&nbsp;kontaktů
        </li>
        <li class="icons-item">
            <i class="bi bi-lightbulb"></i>
            Mentoring od&nbsp;profíků
        </li>
        <li class="icons-item">
            <i class="bi bi-patch-plus"></i>
            Slevy a&nbsp;soutěže
        </li>
        <li class="icons-item">
            <i class="bi bi-hand-thumbs-up"></i>
            Podporuješ junior.guru
        </li>
    </ul>
</div>

{#
    TODO poslední 2-3 akce v klubu
#}

</section>
<div class="section-background gray-white without-border-bottom" markdown="1">
<section markdown="1">

## Proč platit?

<div class="blockquotes-2">
{{ blockquote_avatar('Ty diskuze jsou úžasné. Když to lidi zaplatí, tak je to úplně jiné. Extrémně kultivované, srozumitelné, každý příspěvek dává smysl.', 'jakub.png', 'Jakub', 'Jakub') }}

{{ blockquote_avatar('Je problém najít komunitu, která je o vzájemný pomoci a výměně informací, ne o honění ega. Tady je to krásná výjimka. Jsem ráda, že toho můžu být součástí.', 'hanka.png', 'Hanka', 'Hanka') }}
</div>

<div class="comparison" markdown="1">
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
</div>

### Neztrácej čas záplavou názorů

Rady kolemjdoucích ve veřejných skupinách jsou náchylné k fanouškovství, opakují [nejrůznější mýty](/motivation/#myths), doporučují staré postupy, nebo vycházejí z toho, že co vyhovovalo jednomu, zákonitě platí i pro druhého. Je běžné, že na jednoduchou otázku dostaneš desítky rozcházejících se a mnohdy i zcela nevhodných odpovědí.

V klubu vycházíme z konkrétní cesty, jak postupovat, která se osvědčila na mnoha začátečnících. Zároveň se snažíme radit objektivně a brát ohled na tvou situaci. Poskytneme ti různé pohledy, ale zároveň jasný směr. Místo abychom tě utopili v možnostech, pomůžeme ti rozhodnout se.

### Neztrácej čas s hulváty a sexisty

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

V klubu neexistují hloupé otázky a nemáme potřebu někoho stírat. Mezi členy je mnoho žen a uslintané vtipy u nás nikoho nezajímají. Respektujeme se, pomáháme si, jsme k sobě laskaví a profesionální. Případné excesy se řídí [pravidly chování](/coc/).

</section>
</div>
<div class="section-background yellow-light">
<section id="pricing">
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
</section>
</div>

{#
    TODO

    Klub spolupracuje s Engeto Academy a Software Development Academy. Někteří jejich absolventi mohou dostat tři měsíce členství v klubu zdarma. Pokud u nich studuješ, kontaktuj je a ověř si, zda to náhodou není tvůj případ.
#}

<section markdown="1">

## FAQ

### Firmy {: #companies }

TBD

### Komunity {: #communities }

TBD

</section>
