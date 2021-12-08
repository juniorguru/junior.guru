---
title: "Praktický dárek pro začátečníky v programování"
template: main_memberful.html
description: Dej někomu sílu udržet si své předsevzetí díky členství v online programovací skupině, jaká nemá obdoby. Daruj dlouhodobou motivaci programovat!
---

{% from 'macros.html' import img, markdown, blockquote_avatar, blockquote_toxic, lead, logo, event_circle with context %}


<header class="masthead" id="snow"><div class="masthead-container">
<div class="masthead-content">
<h1>Daruj motivaci programovat</h1>

{% call lead() %}
Dej svým blízkým sílu dodržet své předsevzetí. Chtějí se věnovat programování? Díky členství v klubu neskončí v půlce ledna, ale udrží si **dlouhodobou motivaci**.
{% endcall %}

<a class="masthead-button primary" href="#cenik">1199 Kč za rok</a>
</div>
<div class="masthead-illustration">
  {{ img('static/images/illustration-gift.svg', 'Ilustrace', 400, 400, lazy=False) }}
</div>
</div></header>


<section>
<h2>Podpoř učení nebo kariérní změnu</h2>
{% call lead() %}
Rozhodla se přítelkyně, že se stane programátorkou? Snaží se manžel rekvalifikovat a najít si svou první práci v IT? Můžeš je v tom podpořit! Mnoho lidí napadne, že by zkusili programování, ale **dotáhnout to do úspěšného konce** vyžaduje mnoho dlouhodobé motivace.

Začátečníci potřebují víc než jen kurzy a návody. Nejvíc je posune, **když v tom všem nejsou sami**. Když je u jejich snažení někdo udrží, pomůže jim, dodá motivaci. Klub na junior.guru je speciální placená online komunita na [Discordu](https://discord.com/). Sdílíme si tipy a postřehy. Podporujeme se a radíme. Občas pořádáme přednášky. Dáváme si zpětnou vazbu. Dohazujeme si práci. Společně se radujeme z úspěchů.
{% endcall %}
<div class="text-center">
  <a class="btn btn-lg btn-primary" href="{{ pages|docs_url('club.md')|url }}">
    Všechno o klubu
  </a>
</div>
</section>


<div class="section-background blue-light"><section>
<h2>Nejen leden!</h2>
{% call lead() %}
Všichni to známe. První týden v lednu se najednou všichni učí japonsky, běhají, chodí do posilovny. Ale co ten druhý týden? A co únor? S programováním je to stejné. Samouk jej **začne brzy odkládat**, protože se to zrovna nehodí. Vypadne z rytmu a už se k tomu nevrátí.

S partou kamarádů je jednodušší **udržet si zápal pro věc**. Ať už je to skrze sdílení společného utrpení, odpovědnost k druhým, nebo humor :) Dokonce i v době, kdy se zrovna nehodí zavřít se k počítači a programovat. Klub máš totiž stále u sebe, na mobilu. Při čekání ve frontě na poště, během dojíždění vlakem, při kojení.
{% endcall %}
{{ blockquote_avatar(
  'Jemně popostrkující a nějakou činnost vyvolávající a podněcující síla, kterou jsem potřebovala. Nacpat se sem byl moc dobrej napád.',
  'radka.jpg',
  'Radka',
  'Radka'
) }}
</section>
</div>


<div id="cenik" class="section-background yellow"><section>
<h2>Ježíškem ve dvou krocích</h2>
{% call lead() %}
Zadáš e-mail obdarované osoby a vybereš datum, odkdy začne roční členství platit. Pokud chceš, můžeš přidat i vzkaz. Ve správnou chvíli potom přijdou e-mailem přístupy do klubu.

Že e-mail nejde zabalit pod stromeček? Využij originální poukaz, který vlastní rukou nakreslil [Honza Javorek](#honza), provozovatel junior.guru. Vytiskni, dej do hezké obálky, a je to!
{% endcall %}

<div class="pricing standout">
  <div class="pricing-block pulse-hover">
    <h3 class="pricing-heading">Koupíš dárek</h3>
    <ul class="pricing-benefits">
      <li class="pricing-benefits-item">Roční členství v klubu</li>
    </ul>
    <a class="pricing-button" href="https://juniorguru.memberful.com/gift?plan=74419">1199 Kč</a>
  </div>
  <div class="pricing-block pulse-hover">
    <h3 class="pricing-heading">Stáhneš poukaz</h3>
    <ul class="pricing-benefits">
      <li class="pricing-benefits-item">Vytiskneš a nadělíš</li>
    </ul>
    <a class="pricing-button" href="{{ 'static/darkovy-poukaz-jg.pdf'|url }}">PDF</a>
  </div>
</div>

{% call markdown() %}
[Obchodní podmínky](tos.md) jsou napsané lidsky, klidně si je projdi. Je to smlouva, kterou mezi sebou budeme mít. [Zásady ochrany osobních údajů](privacy.md) popisují, jaká data o tobě Honza má a jak s nimi zachází. Pokud ti něco není jasné, projdi si [otázky a odpovědi](faq.md).
{% endcall %}
</section></div>
