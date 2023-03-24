---
title: Jak se daří provozovat junior.guru
description: Čísla, statistiky, grafy. Jak se Honzovi daří provozovat junior.guru?
---

{% from 'macros.html' import note, partner_link with context %}

# Čísla a grafy

Stránku jsem vytvořil po vzoru [jiných otevřených projektů](https://openstartuplist.com/). Tyto grafy a čísla stejně potřebuji pro svou vlastní potřebu, takže proč je v rámci transparentnosti nemít rovnou na webu, že?

[TOC]

{% call note() %}
  {{ 'bar-chart-line'|icon }} Finanční data se každý den stahují přímo z mého podnikatelského účtu u Fio banky. Používám [svou vlastní Python knihovnu](https://pypi.org/project/fiobank/), kterou jsem kdysi vytvořil.
{% endcall %}

## Čistý zisk

Zisk jsou výnosy mínus náklady včetně daní, tedy částka, která už jde z mého podnikání přímo do rodinného rozpočtu. Aktuální čistý zisk junior.guru je **{{ profit_ttm|thousands }} Kč měsíčně**. Spočítáno jako zisk za posledních 12 měsíců (TTM, _trailing twelve months_) vydělený 12.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="200"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts_business_labels,
        'datasets': [
            {
                'label': 'zisk',
                'data': charts_profit,
                'borderColor': '#1755d1',
                'borderWidth': 2,
            },
            {
                'label': 'zisk TTM/12',
                'data': charts_profit_ttm,
                'borderColor': '#1755d1',
                'borderWidth': 1,
            }
        ]
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'plugins': {'annotation': charts_business_annotations},
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

Následující graf zobrazuje vývoj mých výnosů a nákladů v každém konkrétním měsíci. Tenké linky zobrazují totéž, ale vždy za posledních 12 měsíců (TTM, _trailing twelve months_), vyděleno 12. Výnosy ani náklady totiž nejsou vždy pravidelného, měsíčního charakteru, jeden měsíc vydělám víc, jiný méně, stejné je to s výdaji. Zároveň nemám s nikým delší kontrakt než roční, ať už jsou to jednotlivci nebo firmy. Číslo za rok tedy stírá tyto skoky nahoru a dolů, ale protože můj byznys roste rychleji než ročním tempem, tak zase ukazuje možná menší číslo, než je realitou za poslední půlrok, čtvrtrok.

Čísla z konkrétních mesíců tedy pomáhají odtušit aktuální trendy. Čistý zisk je rozdíl mezi modrou a červenou čárou.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="200"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts_business_labels,
        'datasets': [
            {
                'label': 'výnosy',
                'data': charts_revenue,
                'borderColor': '#1755d1',
                'borderWidth': 2,
            },
            {
                'label': 'výnosy TTM/12',
                'data': charts_revenue_ttm,
                'borderColor': '#1755d1',
                'borderWidth': 1,
            },
            {
                'label': 'náklady',
                'data': charts_cost,
                'borderColor': '#dc3545',
                'borderWidth': 2,
            },
            {
                'label': 'náklady TTM/12',
                'data': charts_cost_ttm,
                'borderColor': '#dc3545',
                'borderWidth': 1,
            },
        ]
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'plugins': {'annotation': charts_business_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

## Výnosy

Původně jsem se snažil junior.guru živit z inzerce nabídek práce, ale byznys na tomto modelu jsem nedokázal dostatečně rozpohybovat tak, abych věřil, že má smysl v tom dál pokračovat. Mezitím jsem se pokusil zpeněžit [příručku](handbook/index.md) skrze loga firem a prosil jsem návštěvníky webu o dobrovolné příspěvky.

Ke konci roku 2020 jsem se rozhodl změnit byznys model a vytvořit kolem junior.guru placenou komunitu na Discordu. Toto detailně popisuji ve svém [článku na blogu](https://honzajavorek.cz/blog/spoustim-klub/). [Klub](club.md) se veřejnosti otevřel v únoru 2021.

V ideálním případě by mě živilo individuální členství lidí v klubu, protože je to pravidelný, předvídatelný příjem, který mi navíc zajišťuje největší nezávislost.

Individuální členství ale nevystačí, takže si domlouvám i [partnerství s firmami](#firemni-partnerstvi). Jsou z toho větší jednorázové příjmy, které lze obtížně předvídat a mohou ovlivňovat mou kritičnost k firmám, se kterými spolupracuji.

Inzerci nabídek práce nechci zrušit, ale aktuálně není na vrcholu mých priorit. Pokud, tak spíše v podobě dlouhodobého partnerství s firmou, než formou jednorázových inzerátů.

Dobrovolné příspěvky stále hrají významnou roli v mých příjmech a velkou měrou právě díky nim junior.guru ve svých počátcích neskončilo. Teď je ale čas postavit se na vlastní nohy! Možnost přispět zřejmě nezruším, ale přestal jsem ji propagovat. Chtěl bych, aby dobrovolné příspěvky jednou plně nahradilo individuální členství v klubu.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="200"
    data-chart-type="bar"
    data-chart="{{ {
        'labels': charts_business_labels,
        'datasets': [
            {
                'label': 'dobrovolné příspěvky',
                'data': charts_revenue_breakdown.pop('donations'),
                'backgroundColor': '#02CABB',
            },
            {
                'label': 'individuální členství',
                'data': charts_revenue_breakdown.pop('memberships'),
                'backgroundColor': '#1755d1',
            },
            {
                'label': 'partnerství s firmami',
                'data': charts_revenue_breakdown.pop('partnerships'),
                'backgroundColor': '#638CDD',
            },
            {
                'label': 'inzerce nabídek práce',
                'data': charts_revenue_breakdown.pop('jobs'),
                'backgroundColor': '#421BD4',
            },
        ],
    }|tojson|forceescape }}"
    {{ charts_revenue_breakdown.keys()|list|assert_empty }}
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'x': {'stacked': True}, 'y': {'stacked': True}},
        'plugins': {'annotation': charts_business_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

### Proč tu není MRR

MRR znamená _monthly recurring revenue_ a je základní metrikou většiny online byznysů, které jsou vedeny jako pravidelně placená služba. Je to součet výnosů, které mi pravidelně měsíčně chodí na účet skrze předplatné, tedy pravidelný příjem, na který se dá spolehnout. I když junior.guru je služba s členstvím na měsíční bázi a MRR by spočítat šlo, nakonec jsem se rozhodl jej zatím neřešit a dívám se spíš na ono TTM vydělené 12.

Jedním důvodem je složitost výpočtu. Data beru z bankovního účtu, kam mi ale nechodí částky za jednotlivé lidi. Stripe mi vždy posílá úhrnné částky za několik týdnů zpětně. Musel bych brát data zvlášť z Memberful. Navíc prodávám i roční členství, které bych musel rozpočítávat.

Druhým důvodem je malá vypovídající hodnota. Velkou část výnosů tvoří kontrakty s firmami, jež jsou nárazovým, ale ve svém množství poměrně stabilním příjmem. Pravidelné příjmy mám zase i z dobrovolných příspěvků, jež bych do MRR započítával jen velice složitě. Aby bylo číslo přesné, musel bych mít data o tom, jak přesně kdo přispívá přes Patreon nebo GitHub Sponsors, což se mi nevyplatí řešit.

## Náklady

Zahrnuji pouze náklady na byznys, ale zase i s daněmi a odvody na zdravotní a sociální pojištění. V roce 2020 je v nich díra, protože kvůli covidu-19 nebyla povinnost je platit. Občas jdou do mínusu (stává se z nich příjem), protože mi úřady něco vrátily.

Neplatím si žádnou reklamu. Výdaje na marketing jsou předplatné nástrojů jako Buffer nebo MailChimp, tisk samolepek, [konzultace](http://janadolejsova.cz/), apod.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="200"
    data-chart-type="bar"
    data-chart="{{ {
        'labels': charts_business_labels,
        'datasets': [
            {
                'label': 'daně a pojištění',
                'data': charts_cost_breakdown.pop('tax'),
                'backgroundColor': '#ddd',
            },
            {
                'label': 'memberful.com',
                'data': charts_cost_breakdown.pop('memberful'),
                'backgroundColor': '#DF4B25',
            },
            {
                'label': 'různé',
                'data': charts_cost_breakdown.pop('miscellaneous'),
                'backgroundColor': '#aaa',
            },
            {
                'label': 'produkce videa',
                'data': charts_cost_breakdown.pop('video'),
                'backgroundColor': '#0c1633',
            },
            {
                'label': 'produkce podcastu',
                'data': charts_cost_breakdown.pop('podcast'),
                'backgroundColor': '#872ec4',
            },
            {
                'label': 'právnička',
                'data': charts_cost_breakdown.pop('lawyer'),
                'backgroundColor': '#801515',
            },
            {
                'label': 'účetnictví, fakturoid.cz',
                'data': charts_cost_breakdown.pop('accounting'),
                'backgroundColor': '#108a00',
            },
            {
                'label': 'marketing',
                'data': charts_cost_breakdown.pop('marketing'),
                'backgroundColor': '#DAA520',
            },
            {
                'label': 'discord.com',
                'data': charts_cost_breakdown.pop('discord'),
                'backgroundColor': '#5865f2',
            },
        ],
    }|tojson|forceescape }}"
    {{ charts_cost_breakdown.keys()|list|assert_empty }}
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'x': {'stacked': True}, 'y': {'stacked': True}},
        'plugins': {'annotation': charts_business_annotations},
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
  {% for partner in partners %}
    {% set partnership = partner.active_partnership() %}
    {% set plan = partnership.plan %}
    <tr>
      <td>
        <a href="{{ pages|docs_url('open/' + partner.slug + '.md')|url }}">Partnerství s {{ partner.name }}</a>
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

## Členství v klubu

[Placený klub](club.md) jsem [spustil](https://honzajavorek.cz/blog/spoustim-klub/) v únoru 2021. Aktuálně je na Discordu **{{ members_total_count }} členů**, ale platících členů může být i víc. Někteří si platí členství pouze aby mě podpořili, bez toho aby se vůbec na Discord přihlásili.

Tenká modrá čára představuje počet členů, kteří si členství platí ze svého. Tenká zelená čára ukazuje ty z nich, kteří preferují roční platbu před měsíční.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="200"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts_club_labels,
        'datasets': [
            {
                'label': 'všechna členství',
                'data': charts_subscriptions,
                'borderColor': '#1755d1',
                'borderWidth': 2,
            },
            {
                'label': 'všechna individuální členství',
                'data': charts_individuals,
                'borderColor': '#1755d1',
                'borderWidth': 1,
            },
            {
                'label': 'roční individuální členství',
                'data': charts_individuals_yearly,
                'borderColor': '#02CABB',
                'borderWidth': 1,
            },
        ],
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'beginAtZero': true}},
        'plugins': {'annotation': charts_club_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

### Typy členství

Každý příchozí člen má v klubu dva týdny zdarma, bez ohledu na to, jakým způsobem za členství následně platí. Některým lidem dávám vstup do klubu zcela zdarma, ať už na základě vlastního uvážení, jako poděkování např. za přednášku v klubu, jako stipendium, nebo ze strategických důvodů. Jde o různé spolupráce s komunitami, podcasty, nebo třeba zvaní mentorů na specifické technologie, jejichž zastoupení na straně seniorů je v klubu slabé, ale od juniorů je po tématu poptávka.

Část lidí má členství zdarma na základě toho, že mě v podpořili dobrovolnými příspěvky. V důsledku to tedy zdarma není, jen mi peníze poslali jinudy. Mnohdy poslali víc, než by je stálo standardní členství v klubu.

S mentory z [CoreSkill](https://coreskill.tech/) máme symbiózu. Nic si navzájem neplatíme. Oni využívají platformu klubu pro svůj mentoring a své studenty. Všichni mají automaticky vstup zdarma. Klub má díky tomu experty na frontend a moderátora Dana Srba.

S některými vzdělávacími agenturami mám dohodu, že do klubu pošlou studenty svých kurzů a proplatí jim členství na první tři měsíce. Agentura z toho má službu pro studenty navíc a já z toho mám to, že pokud se lidem v klubu zalíbí, budou si jej dál platit ze svého.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="200"
    data-chart-type="bar"
    data-chart="{{ {
        'labels': charts_club_labels,
        'datasets': [
            {
                'label': 'tým junior.guru',
                'data': charts_subscriptions_breakdown.pop('team'),
                'backgroundColor': '#00B7EB',
            },
            {
                'label': 'symbióza s CoreSkill',
                'data': charts_subscriptions_breakdown.pop('coreskill'),
                'backgroundColor': '#666',
            },
            {
                'label': 'neplatí členství',
                'data': charts_subscriptions_breakdown.pop('free'),
                'backgroundColor': '#ddd',
            },
            {
                'label': 'dva týdny zdarma',
                'data': charts_subscriptions_breakdown.pop('trial'),
                'backgroundColor': '#a9a9a9',
            },
            {
                'label': 'mají stipendium',
                'data': charts_subscriptions_breakdown.pop('finaid'),
                'backgroundColor': '#02CABB',
            },
            {
                'label': 'členství si platí sami',
                'data': charts_subscriptions_breakdown.pop('individuals'),
                'backgroundColor': '#1755d1',
            },
            {
                'label': 'členství platí firma',
                'data': charts_subscriptions_breakdown.pop('partner'),
                'backgroundColor': '#638CDD',
            },
            {
                'label': 'členství platí vzdělávací agentura',
                'data': charts_subscriptions_breakdown.pop('students'),
                'backgroundColor': '#083284',
            },
        ],
    }|tojson|forceescape }}"
    {{ charts_subscriptions_breakdown.keys()|list|assert_empty }}
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'x': {'stacked': True}, 'y': {'stacked': True}},
        'plugins': {'annotation': charts_club_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

### Příchody

Graf s registracemi obsahuje všechny typy členství. Ať už nový člen přišel přes firmu, stipendium, nebo individuálně, tak se započte. Tenká modrá čára představuje počet členů, kteří v daném měsíci poprvé v historii svého členství přešli na individuální placení. Jsou to především noví členové, kteří se po dvou týdnech na zkoušku rozhodli, že si klub začnou platit. Mohou to ale být i firemní členové nebo studenti ze vzdělávacích agentur, kterým skončilo členství zaplacené někým jiným a rozhodli se pokračovat za svoje.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="200"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts_club_trend_labels,
        'datasets': [
            {
                'label': 'všechny nové registrace',
                'data': charts_signups,
                'borderColor': '#1755d1',
                'borderWidth': 2,
            },
            {
                'label': 'nová individuálně placená členství',
                'data': charts_individuals_signups,
                'borderColor': '#1755d1',
                'borderWidth': 1,
            },
        ]
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'beginAtZero': true}},
        'plugins': {'annotation': charts_club_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

### Odchody

Procento členů, kteří z klubu odcházejí, neboli _churn_. Tlustá čára zahrnuje i ty, kteří klub na dva týdny zdarma vyzkoušeli a poté za něj nezačali platit. Tam se očekává celkem velký odpad, ale i tak graf napovídá, jak se daří držet nově příchozí členy v klubu. Tenká čára sleduje pouze ty, kdo zrušili už existující individuálně placené členství. Naznačuje tedy odchody členů, kteří se za klub rozhodli platit, ale následně změnili názor. Očekává se, že juniorům, kteří si nakonec práci v IT našli, pokryjí většinu hodnoty klubu kolegové ve firmě, kde pracují. Také se v prvních měsících intenzivně zaučují a na klub tak často už nemají čas, i když je to tam baví.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="200"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts_club_trend_labels,
        'datasets': [
            {
                'label': '% úbytku členů',
                'data': charts_churn_ptc,
                'borderColor': '#dc3545',
                'borderWidth': 2,
            },
            {
                'label': '% úbytku individuálně platících členů',
                'data': charts_individuals_churn_ptc,
                'borderColor': '#dc3545',
                'borderWidth': 1,
            },
        ]
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'beginAtZero': true}},
        'plugins': {'annotation': charts_club_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

### Délka setrvání v klubu

Není pro mě úplně zajímavé sledovat jak dlouho v klubu zůstávají ti, kterým členství platí firma, nebo jej mají zadarmo. Graf průměrné délky členství v klubu tedy počítá pouze s těmi, kdo si platí sami.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="200"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts_club_labels,
        'datasets': [
            {
                'label': 'průměrná délka individuálně placeného členství v měsících',
                'data': charts_individuals_duration,
                'borderColor': '#1755d1',
                'borderWidth': 2,
            },
        ]
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'beginAtZero': true}},
        'plugins': {'annotation': charts_club_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

## Aktivita v klubu

### Počet znaků napsaných na Discordu

V grafu není celá historie, uchovávám data jen za rok zpětně. Některé kanály se nezapočítávají, např. „volná zábava“. Nejde o kompletní _engagement_, protože lidi se mohou v klubu projevovat různě, např. reagováním pomocí emoji.

Pouze orientační metrika. Nechci sledovat a glorifikovat _engagement_, protože lidi mají z klubu úplně v pohodě hodnotu i pokud si jej pouze čtou. K tématu doporučuji [Stop Measuring Community Engagement](https://rosie.land/posts/stop-measuring-community-engagement/).

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="200"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts_club_content_labels,
        'datasets': [
            {
                'label': 'počet znaků napsaných na Discordu',
                'data': charts_club_content,
                'borderColor': '#1755d1',
                'borderWidth': 2,
            },
        ]
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'beginAtZero': true}},
        'plugins': {'annotation': charts_club_content_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

### Počet online akcí v klubu

Chtěl bych mít v klubu v průměru aspoň dvě oficiální online akce měsíčně.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="200"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts_club_labels,
        'datasets': [
            {
                'label': 'počet oficiálních akcí',
                'data': charts_events,
                'borderColor': '#1755d1',
                'borderWidth': 2,
            },
            {
                'label': 'počet oficiálních akcí TTM/12',
                'data': charts_events_ttm,
                'borderColor': '#1755d1',
                'borderWidth': 1,
            },
        ]
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'beginAtZero': true}},
        'plugins': {'annotation': charts_club_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

## Ženy

Podíl žen sleduji z vlastní zvědavosti a není to žádná přesná metrika. Nikdo nikde nevyplňuje, zda je žena nebo muž. Pro účely statistik se to určuje jen odhadem podle křestního jména a tvaru příjmení.

### Podíl žen v klubu

Pro srovnání, podle [analýzy ČSÚ z roku 2020](https://www.czso.cz/csu/czso/cri/lidske-zdroje-v-informacnich-technologiich-2020) je v českém IT pouze 10 % žen. Tento podíl se od jejich [předchozí analýzy v roce 2018](https://www.czso.cz/csu/czso/cri/ict-odbornici-v-ceske-republice-a-jejich-mzdy-2018) nezlepšil, naopak nás definitivně předběhly už všechny ostatní státy v Evropě.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="200"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts_club_labels,
        'datasets': [
            {
                'label': '% žen v klubu',
                'data': charts_women_ptc,
                'borderColor': '#dc3545',
                'borderWidth': 2,
            },
        ]
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'min': 0, 'suggestedMax': 50}},
        'plugins': {'annotation': charts_club_annotations},
    }|tojson|forceescape }}"
    data-chart-milestones-offset-ptc="0"></canvas></div></div>

### Podíl žen mezi přednášejícími

Chtěl bych, aby v průměru polovina přednášejících na online akcích v klubu byly ženy. Graf zobrazuje procentuální podíl žen na počtu přednášejících za posledních 12 měsíců (TTM, _trailing twelve months_).

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="200"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts_club_labels,
        'datasets': [
            {
                'label': '% přednášejících žen TTM',
                'data': charts_events_women_ptc_ttm,
                'borderColor': '#dc3545',
                'borderWidth': 2,
            },
        ]
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'min': 0, 'suggestedMax': 50}},
        'plugins': {'annotation': charts_club_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

## Návštěvnost

Čísla návštěvnosti webu jsou na [simpleanalytics.com/junior.guru](https://simpleanalytics.com/junior.guru).

## Kód

Práci na kódu lze sledovat [na GitHubu](https://github.com/honzajavorek/junior.guru/graphs/contributors).

## Plány na rok 2023

Na blogu jsem si sepsal [plány na rok 2023](https://honzajavorek.cz/blog/strategie-na-2023/).
Jak se mi daří je plnit?
Červené kolečko 🔴 znamená, že jsem na to ještě nesáhl, oranžové 🟠 je rozpracováno, zelené 🟢 je hotovo.
Do konce roku **zbývá {{ '{:.1f}'.format(remaining_months_2023) }} měsíců**!

### Priority

<div class="table-responsive"><table class="table">
  <tr><td>🔴</td><td>Konec výmluv! Vytvořím pro junior.guru novou úvodní stránku. Vlastně už skoro cokoliv bude lepší, než to, co je tam teď.</td></tr>
  <tr><td>🔴</td><td>Udělám MVP katalogu vzdělávacích agentur. Bude to evoluce toho, co už mám, ne revoluce. Bude tam naprosté minimum nejnutnějšího.</td></tr>
  <tr><td>🟠</td><td>Umožním lidem odebírat tento blog a novinky na junior.guru skrze newsletter. Pokud k tomu bude potřeba i blog přímo na junior.guru, vyrobím blog.</td></tr>
</table></div>

### Finance

<div class="table-responsive"><table class="table">
  <tr><td>🔴</td><td>Udělám na webu ceník, který přesvědčí ty správné firmy, že chtějí s junior.guru spolupracovat. Měl bych se zamyslet nad tím, že firmy mě najdou spíš přes aktivitu na LinkedIn než vyhledáváním. Asi nemá smysl dělat landing pages na klíčová slova.</td></tr>
  <tr><td>🔴</td><td>Měl bych firmám hlavně osvětlit, např. screencastem, jak to celé funguje, jak to vypadá, co získají. Ušetří mi to sales call a třeba jich přesvědčím víc.</td></tr>
  <tr><td>🔴</td><td>Rozšířím ceník o nabídku pro vzdělávací agentury, která katalog nějak zahrne. Nedávat zbytečně věci zadarmo. Jak ukazuje RyanAir nebo RemoteOK, cenovku může mít cokoliv. Je to moje platforma a i barva nebo logo jsou věci, které tam být nemusí, když agentura nezaplatí. Cílem je zkoušet, získávat zpětnou vazbu, iterovat a najít to, co je pro mě nejjednodušší byznys a dává to všem největší smysl.</td></tr>
  <tr><td>🟠</td><td>Stanu se identifikovanou osobou, abych mohl nakupovat služby z EU. Zdraží mi to účetnictví, ale vnímám to už jako překážku v rozvoji.</td></tr>
  <tr><td>🟠</td><td>Jasně si určím, kolik může být maximálně nejvyšších tarifů (přikláním se ke 4). Implementovat zdražování s ubývajícími místy. Implementovat vyprodání tarifu a ukazatel, kdy se možná zase místo objeví.</td></tr>
  <tr><td>🟢</td><td>Vyladím customer journey. Já i firma musíme mít včas informaci, že se blíží konec.</td></tr>
  <tr><td>🟢</td><td>Vyladím customer journey. Firma musí vědět vše o svém předplatném, v jakém je stavu, kolik čeho zbývá.</tr>
  <tr><td>🟢</td><td>Do konce roku 2022 připravím zdražení pro členy klubu.</td></tr>
</table></div>

### Příručka

<div class="table-responsive"><table class="table">
  <tr><td>🔴</td><td>Doplním do patičky každé stránky na příručce „diskuzi“. Ve skutečnosti nepůjde o diskuzi, ale o upoutávku na klub.</td></tr>
  <tr><td>🔴</td><td>Rozsekám stránky na příručce do jednotlivých kapitol tak, jak si je v budoucnu představuji. Stránky budou neúplné a nejspíš protkané upozorněními, že tam teprve přibude obsah. To se nedá nic dělat. V rámci tohoto úkolu aktualizuji i úvodní stránku příručky. Nic honosného, stačí když tam budou aspoň pod sebou nějaké karty, pro každou fázi juniora.</td></tr>
  <tr><td>🔴</td><td>Dopíšu alespoň tři kapitoly. Nabízí se dokončit Git a GitHub, LinkedIn, nebo řešení problémů.</td></tr>
</table></div>

### Klub

<div class="table-responsive"><table class="table">
  <tr><td>🔴</td><td>Vylepším bota, aby zakládal na Discordu akce pro různé IRL srazy.</td></tr>
  <tr><td>🟠</td><td>Stanovím si jasné ohraničení MVP s tipy pro nové členy v klubu a dopracuji je do této podoby.</td></tr>
  <tr><td>🟢</td><td>Přidám úplně základní podporu pro forum kanály a budu pozorovat, jak to lidi používají.</td></tr>
  <tr><td>🟢</td><td>Najdu dalšího moderátora nebo moderátorku.</td></tr>
</table></div>

### Podcast

<div class="table-responsive"><table class="table">
  <tr><td>🔴</td><td>Přesunu podcast na novou infrastrukturu (CDN77.com). Začneme evidovat počty stažení u jednotlivých epizod.</td></tr>
  <tr><td>🔴</td><td>Vytvořím nové a lepší promo obrázky, které podcast doprovázejí.</td></tr>
  <tr><td>🔴</td><td>Pokud bude energie a místo (blog? newsletter?), mohli bychom k podcastu publikovat i ručně psané texty, nebo automatické přepisy.</td></tr>
  <tr><td>🟢</td><td>Začneme označovat epizody, které jsou finančně podpořené spoluprací s firmami.</td></tr>
  <tr><td>🟢</td><td>Začnu se s Pavlínou dělit o zisk, který mám díky spolupráci s firmami. Může to být i formou placení nástrojů, které k produkování podcastu potřebuje, nebo by jí usnadnily práci. Napadají mě Headliner, Descript, Podstatus, a další. Může to být i tak, že bude moci úkolovat mého pomocníka na audio/video, pokud by pro něj měla vhodné zadání.</tr>
</table></div>

### Pracovní inzeráty

<div class="table-responsive"><table class="table">
  <tr><td>🔴</td><td>Převedu bota na AI.</td></tr>
  <tr><td>🟢</td><td>Vylepším zobrazení inzerátů na Discordu.</td></tr>
  <tr><td>🟢</td><td>Přidám Jobs.cz.</td></tr>
</table></div>

### Marketing

<div class="table-responsive"><table class="table">
  <tr><td>🟠</td><td>Rozjedu pravidelné Q&A pro komunity.</td></tr>
  <tr><td>🟠</td><td>Budu se podílet na anketě mezi juniory. Pokud z toho budou grafy, vložím je na vhodná místa do příručky.</td></tr>
  <tr><td>🟢</td><td>Vymyslím a zrealizuji nejjednodušší možný způsob, jak zjišťovat, odkud do klubu lidi přišli.</tr>
</table></div>

### Různé

<div class="table-responsive"><table class="table">
  <tr><td>🔴</td><td>Opravím posílání e-mailů inzerujícím firmám a další akutní chyby.</td></tr>
  <tr><td>🔴</td><td>Vyřeším kešování generovaných obrázků.</td></tr>
  <tr><td>🔴</td><td>Vyřeším rychlost buildu webovky (Gulp).</td></tr>
  <tr><td>🔴</td><td>Změním způsob, jak si organizuji úkoly. Pročistím Trello. Možná ho i rozdělím na víc nástěnek.</td></tr>
  <tr><td>🔴</td><td>Budu se snažit chránit si víc svůj čas. Nepřišel jsem ale na žádný „vzorec“, který by šlo v tomto případě použít. Napadá mě pouze vytvořit dostatek materiálů, které mohou sloužit jako předpřipravené odpovědi, např. screencast, který vysvětluje klub. To by řešilo minimálně část sales callů.</td></tr>
  <tr><td>🔴</td><td>Určité věci jsou nově pro firmy vyloženě naceněny. Nabídky neplacené spolupráce přicházející od firem, které neznám, budu odmítat. Výjimkou budiž soutěže, které je většinou snadné provést, ať už jde o lístky, knihy, nebo cokoliv jiného. Jinak si budu neplacenou spolupráci dost vybírat. Například pokud vím, že lidé používají software od JetBrains, sám jim napíšu a navrhnu jim spolupráci na jiném půdorysu, než je v ceníku.</td></tr>
  <tr><td>🟠</td><td>Projekty, se kterými plánuji seknout, buď archivuji, nebo jasně označím jako neudržované. U komunitních projektů to jasně oznámím minimálně na Pyvec Slacku a odhlásím se z různých udržovacích povinností kolem repozitářů (např. dependabot).</td></tr>
  <tr><td>🟠</td><td>Budu se věnovat Pyvci jako člen výboru. Pokud se někdo ozve a bude chtít poradit s některým z projektů, o které jsem se staral, pokusím se najít si čas aspoň na videohovor.</td></tr>
  <tr><td>🟠</td><td>Minimálně dvakrát do roka si dám dovolenou, která bude aspoň týden v kuse. Budu o sebe pečovat. Dovolená, sport, a tak.</td></tr>
  <tr><td>🟠</td><td>Najdu si terapeuta.</td></tr>
  <tr><td>🟢</td><td>Rozjedu newsletter, díky kterému budou mít moji fanoušci možnost odebírat můj blog e-mailem.</tr>
  <tr><td>🟢</td><td>Pohraju si s AI.</td></tr>
</table></div>
