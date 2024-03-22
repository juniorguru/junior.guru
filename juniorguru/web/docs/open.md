---
title: Jak se daří provozovat junior.guru
description: Čísla, statistiky, grafy. Jak se Honzovi daří provozovat junior.guru?
---

{% from 'macros.html' import note, partner_link, lead with context %}

# Čísla a grafy

{% call lead() %}
Jmenuji se Honza Javorek a provozuji junior.guru. Tuto stránku jsem vytvořil po vzoru [jiných otevřených projektů](https://openstartuplist.com/). Čísla a grafy stejně potřebuji pro svou vlastní potřebu, takže proč je v rámci transparentnosti nemít rovnou na webu, že?
{% endcall %}

[TOC]

## Plány na rok 2023

Plnění mých [plánů na rok 2023](https://honzajavorek.cz/blog/strategie-na-2023/) lze sledovat [na GitHubu](https://github.com/orgs/juniorguru/projects/1/).

## Týdenní poznámky

Od května 2020 píšu na svůj osobní blog týdenní poznámky, ve kterých popisuji, jak makám na junior.guru.
Pomáhá mi to s páteční psychikou a zároveň si u toho uspořádám myšlenky.
Tady je posledních pět článků:

{% for blog_article in blog[:5] %}
-   [{{ blog_article.title }}]({{ blog_article.url }}), {{ '{:%-d.%-m.%Y}'.format(blog_article.published_on) }}
{% endfor %}

## Čistý zisk

Zisk jsou výnosy mínus náklady včetně daní, tedy částka, která už jde z mého podnikání přímo do rodinného rozpočtu. Aktuální čistý zisk junior.guru je **{{ profit_ttm|thousands }} Kč měsíčně**. Spočítáno jako zisk za posledních 12 měsíců (TTM, _trailing twelve months_) vydělený 12.

Občas si čtu o zahraničních podnikavcích, kteří taky otevřeně sdílí svoje výdělky. Mají to však v jiné měně, tak se mi to špatně srovnává. Proto jsem si to přepočítal. Podle pondělních kurzů ČNB mám zhruba **${{ profit_ttm_usd|thousands }}** nebo **{{ profit_ttm_eur|thousands }}€** čistého měsíčně.

{% call note() %}
  {{ 'bar-chart-line'|icon }} Finanční data se každý den stahují přímo z mého podnikatelského účtu u Fio banky.
{% endcall %}

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts.profit_labels,
        'datasets': [
            {
                'label': 'zisk',
                'data': charts.profit,
                'borderColor': '#1755d1',
                'borderWidth': 2,
            },
            {
                'label': 'zisk TTM/12',
                'data': charts.profit_ttm,
                'borderColor': '#1755d1',
                'borderWidth': 1,
            }
        ]
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'plugins': {'annotation': charts.profit_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

### Cíl

Cílem není zbohatnout, ale dlouhodobě pomáhat juniorům, pohodlně živit rodinu a žít při tom šťastný život. Vlevo vidíte měsíční čistý zisk junior.guru a vpravo jak se na to tvářím.

<table class="table table-mood">
    <tr>
        <th>{{ profit_ttm|thousands }} Kč <small>čistého</small></th>
        <td>
            {% if profit_ttm < 20000 %}
                😱
            {% elif profit_ttm < 40000 %}
                😰
            {% elif profit_ttm < 60000 %}
                🤨
            {% elif profit_ttm < 80000 %}
                😀
            {% else %}
                🤩
            {% endif %}
        </td>
    </tr>
</table>

Seniorní programátor s mými zkušenostmi, který pracuje pro pražskou nebo zahraniční firmu, vydělává 100.000 Kč měsíčně čistého a víc. Dohodli jsme se doma, že když mě junior.guru tolik baví, zkusím to provozovat a i když to vydělá méně, stojí nám to za větší domácí pohodu. Ze svých předchozích angažmá jsem měl úspory, díky nimž jsem mohl v začátcích junior.guru držet při životě, i když zatím moc nevydělávalo.

Na junior.guru pracuji na plný úvazek, mám malé dítě, ženu na rodičovské, nemáme auto, bydlíme v nájmu uprostřed Prahy. Jako podnikatel potřebuji velkou rezervu, abych se nemusel strachovat s každou změnou rodinných nákladů, jestli mohu pokračovat. Také mi nikdo neplatí dovolenou, nemocenskou, nespoří na důchod.

<table class="table table-goals">
    {% set progress_40_ptc = ((profit_ttm * 100) / 40000)|round|int %}
    {% set progress_60_ptc = ((profit_ttm * 100) / 60000)|round|int %}
    {% set progress_80_ptc = ((profit_ttm * 100) / 80000)|round|int %}
    <tr>
        <th class="goal{% if progress_40_ptc >= 100 %} goal-reached{% endif %}">40.000 Kč</th>
        <th class="goal{% if progress_60_ptc >= 100 %} goal-reached{% endif %}">60.000 Kč</th>
        <th class="goal{% if progress_80_ptc >= 100 %} goal-reached{% endif %}">80.000 Kč</th>
    </tr>
    <tr>
        <td class="goal{% if progress_40_ptc >= 100 %} goal-reached{% endif %}">🤨</td>
        <td class="goal{% if progress_60_ptc >= 100 %} goal-reached{% endif %}">😀</td>
        <td class="goal{% if progress_80_ptc >= 100 %} goal-reached{% endif %}">🤩</td>
    </tr>
    <tr>
        <td class="goal{% if progress_40_ptc >= 100 %} goal-reached{% endif %}">
            <div class="progress">
                <div class="progress-bar" style="width: {{ progress_40_ptc }}%">{{ progress_40_ptc }} %</div>
            </div>
        </td>
        <td class="goal{% if progress_60_ptc >= 100 %} goal-reached{% endif %}">
            <div class="progress">
                <div class="progress-bar" style="width: {{ progress_60_ptc }}%">{{ progress_60_ptc }} %</div>
            </div>
        </td>
        <td class="goal{% if progress_80_ptc >= 100 %} goal-reached{% endif %}">
            <div class="progress">
                <div class="progress-bar" style="width: {{ progress_80_ptc }}%">{{ progress_80_ptc }} %</div>
            </div>
        </td>
    </tr>
</table>

## Výnosy a náklady

Silné čáry zobrazují vývoj mých výnosů a nákladů v každém konkrétním měsíci. Tenké linky zobrazují totéž, ale vždy za posledních 12 měsíců (TTM, _trailing twelve months_), vyděleno 12. Čistý zisk je rozdíl mezi modrou a červenou čárou.

Moje výnosy ani náklady nemají pravidelný, měsíční charakter. Jeden měsíc vydělám víc, jiný méně, stejné je to s výdaji. Zároveň nemám s nikým delší kontrakt než roční, ať už jsou to jednotlivci nebo firmy. TTM tedy stírá tyto skoky nahoru a dolů, ale protože můj byznys roste rychleji než ročním tempem, tak zase ukazuje možná menší číslo, než je realitou za poslední půlrok, čtvrtrok. Tu ukazují silné čáry.

{% call note() %}
  {{ 'bar-chart-line'|icon }} Finanční data se každý den stahují přímo z mého podnikatelského účtu u Fio banky.
{% endcall %}

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts.revenue_labels,
        'datasets': [
            {
                'label': 'výnosy',
                'data': charts.revenue,
                'borderColor': '#1755d1',
                'borderWidth': 2,
            },
            {
                'label': 'výnosy TTM/12',
                'data': charts.revenue_ttm,
                'borderColor': '#1755d1',
                'borderWidth': 1,
            },
            {
                'label': 'náklady',
                'data': charts.cost,
                'borderColor': '#dc3545',
                'borderWidth': 2,
            },
            {
                'label': 'náklady TTM/12',
                'data': charts.cost_ttm,
                'borderColor': '#dc3545',
                'borderWidth': 1,
            },
        ]
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'plugins': {'annotation': charts.revenue_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

## Výnosy

Původně jsem se snažil junior.guru živit z inzerce nabídek práce, ale byznys na tomto modelu jsem nedokázal dostatečně rozpohybovat tak, abych věřil, že má smysl v tom dál pokračovat. Mezitím jsem se pokusil zpeněžit [příručku](handbook/index.md) skrze loga firem a prosil jsem návštěvníky webu o dobrovolné příspěvky.

Ke konci roku 2020 jsem se rozhodl změnit byznys model a vytvořit kolem junior.guru placenou komunitu na Discordu. Toto detailně popisuji ve svém [článku na blogu](https://honzajavorek.cz/blog/spoustim-klub/). [Klub](club.md) se veřejnosti otevřel v únoru 2021.

V ideálním případě by mě živilo individuální členství lidí v klubu, protože je to pravidelný, předvídatelný příjem, který mi navíc zajišťuje největší nezávislost. Individuální členství ale nevystačí, takže si domlouvám i [partnerství s firmami](#firemni-partnerstvi). Jsou z toho větší jednorázové příjmy, které lze obtížně předvídat a mohou ovlivňovat mou kritičnost k firmám, se kterými spolupracuji.
Proto všechna partnerství [transparentně popisuji](#firemni-partnerstvi).

V počátcích mohlo junior.guru existovat z velké části jen díky dobrovolným příspěvkům. Když jsem našel funkční byznys model, možnost přispět jsem přestal propagovat a snažím se postavit na vlastní nohy.

{% call note() %}
  {{ 'bar-chart-line'|icon }} Finanční data se každý den stahují přímo z mého podnikatelského účtu u Fio banky.
{% endcall %}

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="bar"
    data-chart="{{ {
        'labels': charts.revenue_breakdown_labels,
        'datasets': [
            {
                'label': 'dobrovolné příspěvky',
                'data': charts.revenue_breakdown.pop('donations'),
                'backgroundColor': '#02cabb',
            },
            {
                'label': 'individuální členství',
                'data': charts.revenue_breakdown.pop('memberships'),
                'backgroundColor': '#1755d1',
            },
            {
                'label': 'partnerství s firmami',
                'data': charts.revenue_breakdown.pop('partnerships'),
                'backgroundColor': '#638cdd',
            },
            {
                'label': 'inzerce nabídek práce',
                'data': charts.revenue_breakdown.pop('jobs'),
                'backgroundColor': '#421bd4',
            },
        ],
    }|tojson|forceescape }}"
    {{ charts.revenue_breakdown.keys()|list|assert_empty }}
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'x': {'stacked': True}, 'y': {'stacked': True}},
        'plugins': {'annotation': charts.revenue_breakdown_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

### Proč tu není MRR

MRR znamená _monthly recurring revenue_ a je základní metrikou většiny online byznysů, které jsou vedeny jako pravidelně placená služba. Je to součet výnosů, které mi pravidelně měsíčně chodí na účet skrze předplatné, tedy pravidelný příjem, na který se dá spolehnout. I když je junior.guru služba s členstvím na měsíční bázi a MRR by spočítat šlo, nakonec jsem se rozhodl jej zatím neřešit a dívám se spíš na ono TTM vydělené 12.

Jedním důvodem je složitost výpočtu. Data beru z bankovního účtu, kam mi ale nechodí částky za jednotlivé lidi. Platební brána mi vždy posílá úhrnné částky za několik týdnů zpětně. Musel bych sbírat data z více zdrojů. Navíc prodávám i roční členství, které bych musel rozpočítávat.

Druhým důvodem je malá vypovídající hodnota. Velkou část výnosů tvoří kontrakty s firmami, jež jsou nárazovým, ale ve svém množství poměrně stabilním příjmem. Pravidelné příjmy mám zase i z dobrovolných příspěvků, jež bych do MRR započítával jen velice složitě. Aby bylo číslo přesné, musel bych mít data o tom, jak přesně kdo přispívá přes Patreon nebo GitHub Sponsors, což se mi nevyplatí řešit.

## Náklady

Zahrnuji pouze náklady na byznys, ale zase i s daněmi a odvody na zdravotní a sociální pojištění. V roce 2020 je v nich díra, protože kvůli covidu-19 nebyla povinnost je platit. Občas jdou do mínusu (stává se z nich příjem), protože mi úřady něco vrátily.

Neplatím si žádnou reklamu. Výdaje na marketing jsou předplatné nástrojů, tisk samolepek, [konzultace](http://janadolejsova.cz/), apod.

{% call note() %}
  {{ 'bar-chart-line'|icon }} Finanční data se každý den stahují přímo z mého podnikatelského účtu u Fio banky.
{% endcall %}

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="bar"
    data-chart="{{ {
        'labels': charts.cost_breakdown_labels,
        'datasets': [
            {
                'label': 'daně a pojištění',
                'data': charts.cost_breakdown.pop('tax'),
                'backgroundColor': '#ddd',
            },
            {
                'label': 'memberful.com',
                'data': charts.cost_breakdown.pop('memberful'),
                'backgroundColor': '#df4b25',
            },
            {
                'label': 'kancelář',
                'data': charts.cost_breakdown.pop('office'),
                'backgroundColor': '#c8102e',
            },
            {
                'label': 'různé',
                'data': charts.cost_breakdown.pop('miscellaneous'),
                'backgroundColor': '#aaa',
            },
            {
                'label': 'produkce videa, podcastu, články',
                'data': charts.cost_breakdown.pop('production'),
                'backgroundColor': '#0c1633',
            },
            {
                'label': 'právnička',
                'data': charts.cost_breakdown.pop('lawyer'),
                'backgroundColor': '#801515',
            },
            {
                'label': 'účetnictví, fakturoid.cz',
                'data': charts.cost_breakdown.pop('accounting'),
                'backgroundColor': '#108a00',
            },
            {
                'label': 'marketing',
                'data': charts.cost_breakdown.pop('marketing'),
                'backgroundColor': '#daa520',
            },
            {
                'label': 'discord.com',
                'data': charts.cost_breakdown.pop('discord'),
                'backgroundColor': '#5865f2',
            },
        ],
    }|tojson|forceescape }}"
    {{ charts.cost_breakdown.keys()|list|assert_empty }}
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'x': {'stacked': True}, 'y': {'stacked': True}},
        'plugins': {'annotation': charts.cost_breakdown_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

## Firemní partnerství

Firmy mohou uzavírat s junior.guru [partnerství](faq.md#firmy) na základě tarifu zakoupeného podle [ceníku](pricing.md).
Partnerství domlouvám osobně a je vždy na rok, potom s firmou jednáme o prodloužení. Tady je detailní přehled všech závazků, které má junior.guru vůči jednotlivým firmám.

<div class="table-responsive standout"><table class="table">
  <tr>
    <th>Detaily</th>
    <th>Tarif</th>
    <th>Zbývá</th>
  </tr>
  {% for partnership in partnerships %}
    {% set partner = partnership.partner %}
    {% set plan = partnership.plan %}
    <tr>
      <td>
        <a href="{{ pages|docs_url(partnership.page_url)|url }}">Partnerství s {{ partner.name }}</a>
      </td>
      <td>
        {%- for _ in range(plan.hierarchy_rank + 1) -%}
          &nbsp;{{- 'star'|icon -}}
        {%- endfor -%}
      </td>
      {% if partnership.expires_on %}
        <td{% if partnership.days_until_expires() < 30 %}
          class="expires-very-soon"
        {% elif partnership.days_until_expires() < 60 %}
          class="expires-soon"
        {%- endif %}>
          {{ partnership.days_until_expires() }} dní
        </td>
      {% else %}
        <td>∞</td>
      {% endif %}
    </tr>
  {% endfor %}
</table></div>

Ukončená partnerství: {% for partner in partners_expired %}{{ partner_link(partner.name, partner.url, 'open') }}{% if not loop.last %}, {% endif %}{% endfor %}.

## Aktivita v klubu

### Počet znaků napsaných na Discordu

V grafu není celá historie, uchovávám data jen za rok zpětně. Některé kanály se nezapočítávají, např. „volná zábava“. Nejde o kompletní _engagement_, protože lidi se mohou v klubu projevovat různě, např. reagováním pomocí emoji.

Pouze orientační metrika. Nechci sledovat a glorifikovat _engagement_, protože lidi mají z klubu úplně v pohodě hodnotu i pokud si jej pouze čtou. K tématu doporučuji [Stop Measuring Community Engagement](https://rosie.land/posts/stop-measuring-community-engagement/).

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts.club_content_labels,
        'datasets': [
            {
                'label': 'počet znaků napsaných na Discordu',
                'data': charts.club_content,
                'borderColor': '#1755d1',
                'borderWidth': 2,
            },
        ]
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'beginAtZero': true}},
        'plugins': {'annotation': charts.club_content_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

### Počet online akcí v klubu

Chtěl bych mít v klubu v průměru aspoň dvě oficiální online akce měsíčně.
Přes léto je většinou pauza.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts.events_labels,
        'datasets': [
            {
                'label': 'počet oficiálních akcí',
                'data': charts.events,
                'borderColor': '#1755d1',
                'borderWidth': 2,
            },
            {
                'label': 'počet oficiálních akcí TTM/12',
                'data': charts.events_ttm,
                'borderColor': '#1755d1',
                'borderWidth': 1,
            },
        ]
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'beginAtZero': true}},
        'plugins': {'annotation': charts.events_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

## Členství v klubu

Když nepočítám roboty, je teď na Discordu **{{ members_total_count }} členů**.
Historická data v grafech jsou z Memberful, služby, která se mi stará o registrace a placení.
Čísla se mohou lišit, protože když někdo ukončí členství a smaže svůj účet, ze statistik zmizí.
Také ne každý, kdo se zaregistroval, je i na Discordu.
Někdo se tam teprve chystá a někdo to ani neplánuje, jelikož mě chce podpořit pouze finančně.
Grafy jsou tedy orientační.

Tenká modrá čára představuje počet členů, kteří si členství platí ze svého. Tenká zelená čára ukazuje ty z nich, kteří preferují roční platbu před měsíční.

{% call note() %}
  {{ 'trash'|icon }} Po zdražení členství jsem si uklízel v administraci a smazal jsem staré tarify. Tím se mi povedlo omylem nenávratně smazat historická data, takže něco v grafu začíná až v březnu 2023.
{% endcall %}

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts.members_labels,
        'datasets': [
            {
                'label': 'všechna členství',
                'data': charts.members,
                'borderColor': '#1755d1',
                'borderWidth': 2,
            },
            {
                'label': 'všechna individuální členství',
                'data': charts.members_individuals,
                'borderColor': '#1755d1',
                'borderWidth': 1,
            },
            {
                'label': 'roční individuální členství',
                'data': charts.members_individuals_yearly,
                'borderColor': '#02cabb',
                'borderWidth': 1,
            },
        ],
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'beginAtZero': true}},
        'plugins': {'annotation': charts.members_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

### Typy členství

Každý příchozí člen má v klubu dva týdny zdarma, bez ohledu na to, jakým způsobem za členství následně platí. Některým lidem dávám vstup do klubu zcela zdarma, ať už na základě vlastního uvážení, jako poděkování např. za přednášku v klubu, jako stipendium, nebo ze strategických důvodů. Jde o různé spolupráce s komunitami, podcasty, nebo třeba zvaní mentorů na specifické technologie, jejichž zastoupení na straně seniorů je v klubu slabé, ale od juniorů je po tématu poptávka.

Část lidí má členství zdarma na základě toho, že mě v podpořili dobrovolnými příspěvky. V důsledku to tedy zdarma není, jen mi peníze poslali jinudy. Mnohdy poslali víc, než by je stálo standardní členství v klubu.

S mentory z [CoreSkill](https://coreskill.tech/) máme symbiózu. Nic si navzájem neplatíme. Oni využívají platformu klubu pro svůj mentoring a své studenty. Všichni mají automaticky vstup zdarma. Klub má díky tomu experty na frontend a moderátora Dana Srba.

{% call note() %}
  {{ 'trash'|icon }} Po zdražení členství jsem si uklízel v administraci a smazal jsem staré tarify. Tím se mi povedlo omylem nenávratně smazat historická data, takže graf začíná až v březnu 2023.
{% endcall %}

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="bar"
    data-chart="{{ {
        'labels': charts.subscriptions_breakdown_labels,
        'datasets': [
            {
                'label': 'neplatí členství',
                'data': charts.subscriptions_breakdown.pop('free'),
                'backgroundColor': '#ddd',
            },
            {
                'label': 'dva týdny zdarma',
                'data': charts.subscriptions_breakdown.pop('trial'),
                'backgroundColor': '#a9a9a9',
            },
            {
                'label': 'mají stipendium',
                'data': charts.subscriptions_breakdown.pop('finaid'),
                'backgroundColor': '#02cabb',
            },
            {
                'label': 'členství si platí sami',
                'data': charts.subscriptions_breakdown.pop('individual'),
                'backgroundColor': '#1755d1',
            },
            {
                'label': 'členství platí firma',
                'data': charts.subscriptions_breakdown.pop('partner'),
                'backgroundColor': '#638cdd',
            },
        ],
    }|tojson|forceescape }}"
    {{ charts.subscriptions_breakdown.keys()|list|assert_empty }}
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'x': {'stacked': True}, 'y': {'stacked': True}},
        'plugins': {'annotation': charts.subscriptions_breakdown_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

### Příchody a odchody

Graf s **příchody** obsahuje všechny typy členství. Ať už nový člen přišel přes firmu, stipendium, nebo individuálně, tak se započte. Tenká modrá čára představuje počet členů, kteří v daném měsíci poprvé v historii svého členství přešli na individuální placení. Jsou to především noví členové, kteří se po dvou týdnech na zkoušku rozhodli, že si klub začnou platit. Mohou to ale být i firemní členové, kterým skončilo členství zaplacené někým jiným a rozhodli se pokračovat za svoje.

Graf s **odchody** zahrnuje i ty, kteří klub na dva týdny zdarma vyzkoušeli a poté za něj nezačali platit. Tam se očekává celkem velký odpad. Tenká čára sleduje pouze ty, kdo zrušili už existující individuálně placené členství. Naznačuje tedy odchody členů, kteří se za klub rozhodli platit, ale následně změnili názor. Očekává se, že juniorům, kteří si nakonec práci v IT našli, pokryjí většinu hodnoty klubu kolegové ve firmě, kde pracují. Také se v prvních měsících intenzivně zaučují a na klub tak často už nemají čas, i když je to tam baví.

{% call note() %}
  {{ 'trash'|icon }} Po zdražení členství jsem si uklízel v administraci a smazal jsem staré tarify. Tím se mi povedlo omylem nenávratně smazat historická data, takže něco v grafu začíná až v březnu 2023.
{% endcall %}

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts.signups_labels,
        'datasets': [
            {
                'label': 'všechny nové registrace',
                'data': charts.signups,
                'borderColor': '#1755d1',
                'borderWidth': 2,
            },
            {
                'label': 'nová individuální členství',
                'data': charts.signups_individuals,
                'borderColor': '#1755d1',
                'borderWidth': 1,
            },
            {
                'label': 'všechny odchody',
                'data': charts.quits,
                'borderColor': '#dc3545',
                'borderWidth': 2,
            },
            {
                'label': 'odchody individuálních členů',
                'data': charts.quits_individuals,
                'borderColor': '#dc3545',
                'borderWidth': 1,
            },
        ]
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'beginAtZero': true}},
        'plugins': {'annotation': charts.signups_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

### Konverze dvou týdnů na zkoušku

Nově registrovaní mají v klubu dva týdny zdarma na zkoušku, tzv. _trial_.
Jejich členství není nijak omezeno, mohou dělat všechno, co ostatní členové.
Po dvou týdnech buď vyplní kartu a začnou platit, nebo je jim členství zrušeno.
Graf ukazuje konverzi _trialů_.

{% call note() %}
  {{ 'trash'|icon }} Po zdražení členství jsem si uklízel v administraci a smazal jsem staré tarify. Tím se mi povedlo omylem nenávratně smazat historická data, takže graf začíná až v březnu 2023.
{% endcall %}

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts.trials_conversion_labels,
        'datasets': [
            {
                'label': '% konverze trialu',
                'data': charts.trials_conversion,
                'borderColor': '#1755d1',
                'borderWidth': 2,
            },
        ]
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'beginAtZero': true}},
        'plugins': {'annotation': charts.trials_conversion_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

### Délka setrvání v klubu

Pokud jde graf nahoru, znamená to, že velká část členů zůstává v klubu dlouho.
Propady nastávají, pokud do klubu přijdou noví lidé, kteří tam ale nevydrží a brzy zase odejdou.

{% call note() %}
  {{ 'trash'|icon }} Po zdražení členství jsem si uklízel v administraci a smazal jsem staré tarify. Tím se mi povedlo omylem nenávratně smazat historická data, takže něco v grafu začíná až v březnu 2023.
{% endcall %}

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts.subscriptions_duration_labels,
        'datasets': [
            {
                'label': 'průměrný počet měsíců všech členství',
                'data': charts.subscriptions_duration,
                'borderColor': '#1755d1',
                'borderWidth': 2,
            },
            {
                'label': 'průměrný počet měsíců individuálních členství',
                'data': charts.subscriptions_duration_individuals,
                'borderColor': '#1755d1',
                'borderWidth': 1,
            },
        ]
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'beginAtZero': true}},
        'plugins': {'annotation': charts.subscriptions_duration_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

## Retence klubu

Procento členů, kteří z klubu odcházejí, neboli _churn_.
Opět platí, že silná čára je celkový _churn_, zatímco tenká se týká jen členů, kteří si klub platili za svoje.

{% call note() %}
  {{ 'trash'|icon }} Po zdražení členství jsem si uklízel v administraci a smazal jsem staré tarify. Tím se mi povedlo omylem nenávratně smazat historická data, takže něco v grafu začíná až v březnu 2023.
{% endcall %}

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts.churn_labels,
        'datasets': [
            {
                'label': '% úbytku členů',
                'data': charts.churn,
                'borderColor': '#dc3545',
                'borderWidth': 2,
            },
            {
                'label': '% úbytku individuálních členů',
                'data': charts.churn_individuals,
                'borderColor': '#dc3545',
                'borderWidth': 1,
            },
        ]
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'beginAtZero': true}},
        'plugins': {'annotation': charts.churn_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

### Důvody odchodu

Když někdo ukončuje členství v klubu, může mi sdělit důvod, proč tak činí.
Data jsou celkem od **{{ charts.cancellations_breakdown_count }}** lidí.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="bar"
    data-chart="{{ {
        'labels': charts.cancellations_breakdown_labels,
        'datasets': [
            {
                'label': '% neudali důvod',
                'data': charts.cancellations_breakdown.pop('unknown'),
                'backgroundColor': '#ddd',
            },
            {
                'label': '% jiný důvod',
                'data': charts.cancellations_breakdown.pop('other'),
                'backgroundColor': '#a9a9a9',
            },
            {
                'label': '% klub už nepotřebuju',
                'data': charts.cancellations_breakdown.pop('necessity'),
                'backgroundColor': '#1755d1',
            },
            {
                'label': '% potřeboval(a) jsem klub na omezenou dobu',
                'data': charts.cancellations_breakdown.pop('temporary_use'),
                'backgroundColor': '#02cabb',
            },
            {
                'label': '% vybral(a) jsem jinou službu, která mi vyhovuje víc',
                'data': charts.cancellations_breakdown.pop('competition'),
                'backgroundColor': '#083284',
            },
            {
                'label': '% klub nesplnil moje očekávání',
                'data': charts.cancellations_breakdown.pop('misunderstood'),
                'backgroundColor': '#00b7eb',
            },
            {
                'label': '% klub je moc drahý',
                'data': charts.cancellations_breakdown.pop('affordability'),
                'backgroundColor': '#dc3545',
            },
        ],
    }|tojson|forceescape }}"
    {{ charts.cancellations_breakdown.keys()|list|assert_empty }}
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'x': {'stacked': True}, 'y': {'stacked': True, 'beginAtZero': true, 'max': 100}},
        'plugins': {'annotation': charts.cancellations_breakdown_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

### Důvody odchodu za celou historii

Celkový poměr důvodů odchodu za celou historii, po kterou sbírám tento typ zpětné vazby.
Data jsou celkem od **{{ charts.total_cancellations_breakdown_count }}** lidí.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="pie"
    data-chart="{{ {
        'labels': {
            'unknown': '% neudali důvod',
            'other': '% jiný důvod',
            'necessity': '% klub už nepotřebuju',
            'temporary_use': '% potřeboval(a) jsem klub na omezenou dobu',
            'competition': '% vybral(a) jsem jinou službu, která mi vyhovuje víc',
            'misunderstood': '% klub nesplnil moje očekávání',
            'affordability': '% klub je moc drahý',
        }|mapping(charts.total_cancellations_breakdown.keys()),
        'datasets': [
            {
                'data': charts.total_cancellations_breakdown.values()|list,
                'backgroundColor': {
                    'unknown': '#ddd',
                    'other': '#a9a9a9',
                    'necessity': '#1755d1',
                    'temporary_use': '#02cabb',
                    'competition': '#083284',
                    'misunderstood': '#00b7eb',
                    'affordability': '#dc3545',
                }|mapping(charts.total_cancellations_breakdown.keys())
            },
        ],
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'scales': None,
        'aspectRatio': 2,
    }|tojson|forceescape }}"
    data-chart-milestones-offset-ptc="0"></canvas></div></div>

## Odkud jsou platící členové

O členech neuchovávám prakticky žádné informace, ze kterých bych mohl zjistit, odkud jsou.
Stripe mi ale umožňuje zjistit, v jaké zemi byla vydána jejich karta.
Díky tomu mohu odhadnout, kolik lidí není z Česka.

Potřebuju to sledovat, abych věděl, jestli jsem nepřesáhl limit pro [One Stop Shop](https://vat-one-stop-shop.ec.europa.eu/one-stop-shop/declare-and-pay-oss_en). Ten je {{ charts.countries.oss_limit_eur|thousands }}€/rok, což je {{ charts.countries.oss_limit_czk|thousands }} Kč/rok, což je {{ charts.countries.oss_limit_czk_monthly|thousands }}/měsíc.

Z individuálních členství jsem minulý měsíc vydělal {{ charts.countries.revenue_memberships|thousands }} Kč celkem.
Když použiju procenta z grafu níže, odhadem by mělo být {{ charts.countries.revenue_memberships_non_cz|thousands }} Kč odjinud než z Česka. {% if charts.countries.oss_limit_czk_monthly > charts.countries.revenue_memberships_non_cz %}**Takže asi dobrý.**{% endif %}

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="bar"
    data-chart="{{ {
        'labels': [
            'Česko',
            'Slovensko',
            'jinde',
        ],
        'datasets': [
            {
                'axis': 'y',
                'label': '% členů',
                'data': [
                    charts.countries.breakdown.pop('CZ'),
                    charts.countries.breakdown.pop('SK'),
                    charts.countries.breakdown.pop('other'),
                ],
                'backgroundColor': '#1755d1',
            },
        ],
    }|tojson|forceescape }}"
    {{ charts.countries.breakdown.keys()|list|assert_empty }}
    data-chart-options="{{ {
        'indexAxis': 'y',
        'interaction': {'mode': 'index'},
        'scales': {'y': {'min': 0, 'suggestedMax': 100}},
    }|tojson|forceescape }}"></canvas></div></div>

## Marketingové kanály klubu

### Výkonnost kanálů podle ankety

Když se někdo registruje do klubu, může mi sdělit, kde na junior.guru narazil.
Graf porovnává kolik lidí jednotlivé marketingové kanály přivedly do klubu, a kolik z toho doposud bylo peněz.
Procenta nejsou podíl ze všech příchozích, ale z **{{ charts.total_marketing_breakdown_count }}** lidí, kteří odpověděli na anketu.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="bar"
    data-chart="{{ {
        'labels': {
            'other': 'ostatní',
            'courses': 'doporučení z kurzu',
            'search': 'vyhledávání',
            'internet': '„internet“',
            'friend': 'doporučení známého',
            'facebook': 'Facebook',
            'podcasts': 'podcasty',
            'linkedin': 'LinkedIn',
            'youtube': 'YouTube',
            'yablko': 'yablko',
            'courses_search': 'vyhledávání recenzí kurzů',
        }|mapping(charts.total_spend_marketing_breakdown.keys()),
        'datasets': [
            {
                'label': '% členů',
                'data': charts.total_marketing_breakdown.values()|list,
                'backgroundColor': '#1755d1',
            },
            {
                'label': '% peněz',
                'data': charts.total_spend_marketing_breakdown.values()|list,
                'backgroundColor': '#638cdd',
            },
        ],
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'beginAtZero': true}},
    }|tojson|forceescape }}"></canvas></div></div>

### Výkonnost kanálů podle předchozí stránky

Když se někdo registruje do klubu, systém si uloží [referrer](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referer), tzn. z jaké webové stránky přišel.
Graf porovnává kolik lidí jednotlivé marketingové kanály přivedly do klubu, a kolik z toho doposud bylo peněz.
Procenta nejsou podíl ze všech příchozích, ale z **{{ charts.total_referrer_breakdown_count }}** lidí, kteří měli _referrer_ odjinud než z junior.guru.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="bar"
    data-chart="{{ {
        'labels': {
            'other': 'ostatní',
            'twitter': 'Twitter',
            'honzajavorek': 'honzajavorek.cz',
            'google': 'Google',
            'facebook': 'Facebook',
            'linkedin': 'LinkedIn',
            'youtube': 'YouTube',
        }|mapping(charts.total_spend_referrer_breakdown.keys()),
        'datasets': [
            {
                'label': '% členů',
                'data': charts.total_referrer_breakdown.values()|list,
                'backgroundColor': '#1755d1',
            },
            {
                'label': '% peněz',
                'data': charts.total_spend_referrer_breakdown.values()|list,
                'backgroundColor': '#638cdd',
            },
        ],
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'beginAtZero': true}},
    }|tojson|forceescape }}"></canvas></div></div>

### Sociální sítě a newsletter

Vývoj počtu sledujících na profilech na relevantních sociálních sítích a počtu odběratelů [newsletteru](news.jinja).

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts.followers_breakdown_labels,
        'datasets': [
            {
                'label': 'osobní GitHub',
                'data': charts.followers_breakdown.pop('github_personal'),
                'borderColor': '#343434',
                'borderWidth': 2,
            },
            {
                'label': 'GitHub',
                'data': charts.followers_breakdown.pop('github'),
                'borderColor': '#343434',
                'borderWidth': 1,
            },
            {
                'label': 'osobní LinkedIn',
                'data': charts.followers_breakdown.pop('linkedin_personal'),
                'borderColor': '#1755d1',
                'borderWidth': 2,
            },
            {
                'label': 'LinkedIn',
                'data': charts.followers_breakdown.pop('linkedin'),
                'borderColor': '#1755d1',
                'borderWidth': 1,
            },
            {
                'label': 'YouTube',
                'data': charts.followers_breakdown.pop('youtube'),
                'borderColor': '#dc3545',
                'borderWidth': 2,
            },
            {
                'label': 'Mastodon',
                'data': charts.followers_breakdown.pop('mastodon'),
                'borderColor': '#563acc',
                'borderWidth': 1,
            },
            {
                'label': 'newsletter',
                'data': charts.followers_breakdown.pop('newsletter'),
                'borderColor': '#02cabb',
                'borderWidth': 2,
            },
        ],
    }|tojson|forceescape }}"
    {{ charts.followers_breakdown.keys()|list|assert_empty }}
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'plugins': {'annotation': charts.followers_breakdown_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

## Návštěvnost webu

Návštěvnost měří [Simple Analytics](https://www.simpleanalytics.com/?referral=honza-javorek) a veškerá čísla jsou [veřejná](https://simpleanalytics.com/junior.guru).
Tady jen pár vybraných grafů, které se tam špatně naklikávají ručně.
Grafy zobrazují trend pouze zpětně za jeden rok, protože mi to tak stačí.

### Celková návštěvnost

Většinou je nejvyšší v lednu a nejnižší v létě.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts.web_usage_total_labels,
        'datasets': [
            {
                'label': 'celková návštěvnost',
                'data': charts.web_usage_total,
                'borderColor': '#1755d1',
                'borderWidth': 2,
            },
        ]
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'beginAtZero': true}},
        'plugins': {'annotation': charts.web_usage_total_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

### Souhrnná návštěvnost podle produktů

Nad jednotlivými částmi junior.guru přemýšlím jako nad produkty.
Graf mi pomáhá zjistit, jak velkou návštěvnost přitahuje každý z nich.
Při čtení grafu je ale dobré si uvědomit, že návštěvnost není vše.
Například klub nebo podcast mají „to hlavní“ jinde než na webu.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts.web_usage_breakdown_labels,
        'datasets': [
            {
                'label': 'úvodní stránka',
                'data': charts.web_usage_breakdown.pop('home'),
                'borderColor': '#1755d1',
                'borderWidth': 2,
            },
            {
                'label': 'prodejní stránka klubu',
                'data': charts.web_usage_breakdown.pop('club'),
                'borderColor': '#dc3545',
                'borderWidth': 1,
            },
            {
                'label': 'příručka',
                'data': charts.web_usage_breakdown.pop('handbook'),
                'borderColor': '#02cabb',
                'borderWidth': 1,
            },
            {
                'label': 'katalog kurzů',
                'data': charts.web_usage_breakdown.pop('courses'),
                'borderColor': '#00b7eb',
                'borderWidth': 1,
            },
            {
                'label': 'pracovní inzeráty',
                'data': charts.web_usage_breakdown.pop('jobs'),
                'borderColor': '#638cdd',
                'borderWidth': 1,
            },
            {
                'label': 'stránka s podcastem',
                'data': charts.web_usage_breakdown.pop('podcast'),
                'borderColor': '#872ec4',
                'borderWidth': 1,
            },
        ],
    }|tojson|forceescape }}"
    {{ charts.web_usage_breakdown.keys()|list|assert_empty }}
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'beginAtZero': true}},
        'plugins': {'annotation': charts.web_usage_breakdown_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

### Registrace do klubu podle předchozí stránky

Když se někdo registruje do klubu, systém si uloží [referrer](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referer), tzn. z jaké webové stránky přišel.
{% if charts.total_internal_referrer_breakdown_count %}
Procenta nejsou podíl ze všech příchozích, ale z **{{ charts.total_internal_referrer_breakdown_count }}** lidí, kteří měli za poslední půlrok _referrer_ z junior.guru.
Tzv. _long tail_ je z grafu uříznutý.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="bar"
    data-chart="{{ {
        'labels': charts.total_internal_referrer_breakdown.keys()|list,
        'datasets': [
            {
                'axis': 'y',
                'label': '% členů',
                'data': charts.total_internal_referrer_breakdown.values()|list,
                'backgroundColor': '#1755d1',
            },
        ],
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'indexAxis': 'y',
        'interaction': {'mode': 'index'},
        'scales': {'y': {'beginAtZero': true}},
    }|tojson|forceescape }}"></canvas></div></div>
{% else %}
  {% call note() -%}
    {{ 'cloud-rain'|icon }} Graf je momentálně rozbitý.
  {%- endcall %}
{% endif %}

### Peníze za členství v klubu podle předchozí stránky

Když se někdo registruje do klubu, systém si uloží [referrer](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referer), tzn. z jaké webové stránky přišel.
Graf ukazuje, kolik takhle jednotlivé stránky skrze klub přinesly peněz.
{% if charts.total_spend_internal_referrer_breakdown_count %}
Procenta nejsou podíl ze všech příchozích, ale z **{{ charts.total_spend_internal_referrer_breakdown_count }}** lidí, kteří měli za poslední půlrok _referrer_ z junior.guru.
Tzv. _long tail_ je z grafu uříznutý.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="bar"
    data-chart="{{ {
        'labels': charts.total_spend_internal_referrer_breakdown.keys()|list,
        'datasets': [
            {
                'axis': 'y',
                'label': '% členů',
                'data': charts.total_spend_internal_referrer_breakdown.values()|list,
                'backgroundColor': '#638cdd',
            },
        ],
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'indexAxis': 'y',
        'interaction': {'mode': 'index'},
        'scales': {'y': {'beginAtZero': true}},
    }|tojson|forceescape }}"></canvas></div></div>
{% else %}
  {% call note() -%}
    {{ 'cloud-rain'|icon }} Graf je momentálně rozbitý.
  {%- endcall %}
{% endif %}

## Příručka

Orientační metriky co se týče stránek v [příručce](handbook/index.md).
Všechny soubory spadající pod příručku mají aktuálně **{{ handbook_total_size|thousands }}** znaků.
Počítání znaků v souborech, kde se míchají Markdown a Jinja značky, má spoustu vad, ale aspoň něco.
[Podle Wikipedie](https://cs.wikipedia.org/wiki/Diplomov%C3%A1_pr%C3%A1ce) je 180.000 znaků doporučovaná velikost disertační práce (titul Ph.D.).

Když chci na nějaké stránce něco doplnit, dělám si na jejím konci HTML komentář a do něj si ukládám nepříliš strukturované poznámky.
Ty se taky započítají do celkové velikosti, ale v grafu je jejich velikost zobrazena šedě, abych tušil, jaký je poměr a kde na mě ještě čeká kolik práce.

Příliš velké stránky bych měl nejspíš zkrátit, nebo rozdělit do více menších.
Ideální stránka příručky by měla pouze modrý sloupeček a ten by nesahal výše než k červené čáře.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="bar"
    data-chart="{{ {
        'labels': charts.handbook_labels,
        'datasets': [
            {
                'label': 'znaků TODO',
                'data': charts.handbook_notes,
                'backgroundColor': '#a9a9a9',
            },
            {
                'label': 'znaků obsahu',
                'data': charts.handbook,
                'backgroundColor': '#1755d1',
            },
        ],
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'x': {'stacked': true}},
        'plugins': {
            'annotation': {
                'common': {'drawTime': 'beforeDatasetsDraw'},
                'annotations': {
                    'threshold': {
                        'value': 20000,
                        'scaleID': 'y',
                        'type': 'line',
                        'borderColor': '#dc3545',
                        'borderWidth': 1,
                    }
                },
            }
        },
    }|tojson|forceescape }}"
    data-chart-milestones-offset-ptc="0"></canvas></div></div>

## Ženy

Podíl žen sleduji z vlastní zvědavosti a není to žádná přesná metrika. Nikdo nikde nevyplňuje, zda je žena nebo muž. Pro účely statistik se to určuje jen odhadem podle křestního jména a tvaru příjmení.

### Podíl žen v klubu

Pro srovnání, podle [analýzy ČSÚ z roku 2020](https://www.czso.cz/csu/czso/cri/lidske-zdroje-v-informacnich-technologiich-2020) je v českém IT pouze 10 % žen. Tento podíl se od jejich [předchozí analýzy v roce 2018](https://www.czso.cz/csu/czso/cri/ict-odbornici-v-ceske-republice-a-jejich-mzdy-2018) nezlepšil, naopak nás definitivně předběhly už všechny ostatní státy v Evropě.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts.members_women_labels,
        'datasets': [
            {
                'label': '% žen v klubu',
                'data': charts.members_women,
                'borderColor': '#dc3545',
                'borderWidth': 2,
            },
        ]
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'min': 0, 'suggestedMax': 50}},
        'plugins': {'annotation': charts.members_women_annotations},
    }|tojson|forceescape }}"
    data-chart-milestones-offset-ptc="0"></canvas></div></div>

### Podíl žen mezi přednášejícími

Chtěl bych, aby v průměru polovina přednášejících na online akcích v klubu byly ženy. Graf zobrazuje procentuální podíl žen na počtu přednášejících za posledních 12 měsíců (TTM, _trailing twelve months_).

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts.events_women_labels,
        'datasets': [
            {
                'label': '% přednášejících žen TTM',
                'data': charts.events_women,
                'borderColor': '#dc3545',
                'borderWidth': 2,
            },
        ]
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'min': 0, 'suggestedMax': 50}},
    }|tojson|forceescape }}"></canvas></div></div>

### Podíl žen mezi hosty podcastu

Sice do toho Pavlíně nekecám, ale za mě by bylo fajn, kdyby v průměru polovina hostů v podcastu byly ženy. Graf zobrazuje procentuální podíl žen na počtu hostů za posledních 12 měsíců (TTM, _trailing twelve months_).

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="230"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts.podcast_women_labels,
        'datasets': [
            {
                'label': '% žen v podcastu TTM',
                'data': charts.podcast_women,
                'borderColor': '#dc3545',
                'borderWidth': 2,
            },
        ]
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'min': 0, 'suggestedMax': 50}},
    }|tojson|forceescape }}"></canvas></div></div>

## Kód

Práci na kódu lze sledovat [na GitHubu](https://github.com/juniorguru/junior.guru/graphs/contributors).
