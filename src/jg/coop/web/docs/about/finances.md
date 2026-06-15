---
title: Finanční výsledky junior.guru
template: main_about.html
---

{% from 'macros.html' import lead with context %}

# Finanční výsledky

{% call lead() %}
Transparentně o zisku, příjmech, výdajích. Čísla a grafy. Data se každý den stahují přímo z Honzova podnikatelského účtu u Fio banky.
{% endcall %}

[TOC]

## Záměr

Cílem není zbohatnout, ale dlouhodobě pomáhat juniorům, pohodlně živit rodinu a žít při tom šťastný život. Vlevo vidíte měsíční čistý zisk junior.guru a vpravo jak se na to Honza tváří.

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

Honza na junior.guru pracuje na plný úvazek, má malé dítě, bydlí v nájmu uprostřed Prahy, nemá ani auto.
Seniorní programátor s [jeho zkušenostmi](https://www.linkedin.com/in/honzajavorek/), který pracuje pro pražskou nebo zahraniční firmu, vydělává 100.000 Kč měsíčně čistého a víc.
Honzu ale práce na junior.guru hodně naplňuje a tak se tomu za podpory své rodiny věnuje i přesto, že to vydělá méně.
Z předchozích angažmá má úspory, díky nimž může projekt držet při životě, i když je zrovna horší období a moc nevydělává.

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

Částky nelze přímočaře srovnávat se mzdou. Jako podnikatel potřebuje velkou rezervu, aby se nemusel strachovat s každou změnou rodinných nákladů, jestli může pokračovat. Také mu nikdo neplatí dovolenou, nemocenskou, nespoří na důchod.

<p class="text-center standout-top">
  <a href="{{ pages|docs_url("love.jinja")|url }}" class="love-btn btn-lg pulse">{{ 'heart-fill'|icon }} Pošli LOVE</a>
</p>

## Čistý zisk

Zisk jsou výnosy mínus náklady včetně daní, tedy částka, která už jde z Honzova podnikání přímo do rodinného rozpočtu. Aktuální čistý zisk junior.guru je **{{ profit_ttm|thousands }} Kč měsíčně**. Spočítáno jako zisk za posledních 12 měsíců (TTM, _trailing twelve months_) vydělený 12.

Občas se někde píše o zahraničních podnikavcích, kteří taky otevřeně sdílí svoje výdělky. Mají to však v jiné měně, tak se to špatně srovnává. Takže podle pondělních kurzů ČNB se to dá přepočítat na zhruba **${{ profit_ttm_usd|thousands }}** nebo **{{ profit_ttm_eur|thousands }}€** čistého měsíčně.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="300"
    data-chart-type="line"
    data-chart-zero-line
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

## Meziroční růst výnosů

Růst výnosů v procentech. Každý měsíc se porovnává se stejným měsícem o rok dříve (MoM, _Month-over-Month_). Mělo by to ukazovat meziroční růst nebo pokles.

Pro každý měsíc se ještě počítá součet za uplynulých 12 měsíců (TTM, _trailing twelve months_), vyděleno 12, a to se pak srovnává se stejnou hodnotou o rok dříve. Mělo by to ukazovat meziroční růst nebo pokles očištěný o sezónní výkyvy.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="300"
    data-chart-type="line"
    data-chart-zero-line
    data-chart="{{ {
        'labels': charts.revenue_growth_labels,
        'datasets': [
            {
                'label': 'MoM růst v %',
                'data': charts.revenue_growth,
                'borderColor': '#1755d1',
                'borderWidth': 2,
            },
            {
                'label': 'MoM TTM růst v %',
                'data': charts.revenue_ttm_growth,
                'borderColor': '#1755d1',
                'borderWidth': 1,
            }
        ]
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'plugins': {'annotation': charts.revenue_growth_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

## Výnosy a náklady

Silné čáry zobrazují vývoj výnosů a nákladů v každém konkrétním měsíci. Tenké linky zobrazují totéž, ale vždy za posledních 12 měsíců (TTM, _trailing twelve months_), vyděleno 12. Čistý zisk je rozdíl mezi modrou a červenou čárou.

Výnosy ani náklady junior.guru nemají pravidelný, měsíční charakter. Jeden měsíc je to víc, jiný méně, stejné je to s výdaji. Zároveň nemá s nikým delší kontrakt než roční, ať už jsou to jednotlivci nebo firmy. TTM tedy stírá tyto skoky nahoru a dolů. Protože se ale byznys hýbe rychleji než ročním tempem, TTM neukazuje dobře trend za poslední půlrok nebo čtvrtrok. Ten ukazují silné čáry.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="300"
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

Původně junior.guru mělo vydělávat z inzerce nabídek práce, ale byznys na tomto modelu Honza nedokázal dostatečně rozpohybovat tak, aby věřil, že má smysl v tom dál pokračovat. Mezitím se pokusil zpeněžit [příručku](../handbook/index.md) skrze loga firem a začal prosit návštěvníky webu o [dobrovolné příspěvky](../love.jinja).

Ke konci roku 2020 se rozhodl změnit byznys model a vytvořit kolem junior.guru [placenou komunitu na Discordu](../club.md). Toto detailně popisuje ve svém [článku na blogu](https://honzajavorek.cz/blog/spoustim-klub/). Klub se veřejnosti otevřel v únoru 2021.

V ideálním případě by stačilo individuální členství lidí v klubu, protože je to pravidelný, předvídatelný příjem, který navíc zajišťuje největší nezávislost projektu. Individuální členství ale nevystačí, takže má junior.guru i [sponzory](sponsors-partners.md). Z těch jsou větší jednorázové příjmy, které lze obtížně předvídat. Sponzorské dohody mohou ovlivňovat Honzovu kritičnost ke konkrétním firmám, a proto jsou všechna sponzorství [transparentně popsána](sponsors-partners.md).

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="300"
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
                'label': 'sponzoři',
                'data': charts.revenue_breakdown.pop('sponsorships'),
                'backgroundColor': '#638cdd',
            },
            {
                'label': 'inzerce práce',
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

## Skladba výnosů za poslední rok

Procentuální poměr zdrojů výnosů za posledních 12 měsíců (TTM, _trailing twelve months_), vyděleno 12.

Tabulka v podstatě říká, kdo je na junior.guru zákazník, komu projekt slouží, pro koho Honza pracuje.
Čím víc procent jde z členství v klubu nebo dobrovolných příspěvků, tím víc si junior.guru platí samotní junioři nebo fanoušci a tím spíš je nezpochybnitelná Honzova motivace dělat vše pro ně.
Čím víc procent jde ze sponzorských příspěvků, tím spíš se bude Honza věnovat závazkům vůči firmám a dbát na jejich pohled na věc.

<div class="table-responsive"><table class="table">
{% for name, value_pct in revenue_ttm_breakdown|money_breakdown_ptc|revenue_categories %}
  <tr>
    <th>{{ value_pct }} %</th>
    <td>{{ name }}</td>
  </tr>
{% endfor %}
</table></div>

## Proč tu není MRR

MRR znamená _monthly recurring revenue_ a je základní metrikou většiny online byznysů, které jsou vedeny jako pravidelně placená služba. Je to součet výnosů, které pravidelně měsíčně chodí na účet skrze předplatné, tedy pravidelný příjem, na který se dá spolehnout. I když je junior.guru služba s členstvím na měsíční bázi a MRR by spočítat šlo, nakonec se Honza rozhodl jej zatím neřešit a dívá se spíš na ono TTM vydělené 12.

Jedním důvodem je složitost výpočtu. Data se berou z bankovního účtu, kam ale nechodí částky za jednotlivé lidi. Platební brána vždy posílá úhrnné částky za několik týdnů zpětně. Musely by se kombinovat data z více zdrojů. Navíc existují i roční členství, které by se musely rozpočítávat.

Druhým důvodem je malá vypovídající hodnota. Velkou část výnosů tvoří kontrakty s firmami, jež jsou nárazovým, ale ve svém množství poměrně stabilním příjmem. Pravidelné příjmy jsou i z dobrovolných příspěvků, jež by se do MRR započítávaly jen velice složitě. Aby bylo číslo přesné, bylo by potřeba stahovat data o tom, jak přesně kdo přispívá přes GitHub Sponsors (a dříve Patreon), což se nevyplatí řešit.

## Náklady

Zahrnuty jsou pouze náklady na byznys, ale zase i s daněmi a odvody na zdravotní a sociální pojištění. V roce 2020 je v nich díra, protože kvůli covidu-19 nebyla povinnost je platit. Občas jdou do mínusu (stává se z nich příjem), protože úřady něco vrátily.

Výdaje na [marketing](./marketing.md) jsou předplatné nástrojů, tisk samolepek, konzultace, apod., ne platby za reklamu.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="300"
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

## Odkud jsou platící členové klubu

Samotné junior.guru o členech [klubu](../club.md) žádné detailní informace nesbírá, ale platební systém Stripe umožňuje zjistit, v jaké zemi byla vydána jejich karta.
Díky tomu lze odhadnout, kolik lidí není z Česka.

Honza to potřebuje sledovat, aby věděl, jestli nepřesáhl limit pro [One Stop Shop](https://vat-one-stop-shop.ec.europa.eu/one-stop-shop/declare-and-pay-oss_en). Ten je {{ charts.countries.oss_limit_eur|thousands }}€/rok, což je {{ charts.countries.oss_limit_czk|thousands }} Kč/rok, což je {{ charts.countries.oss_limit_czk_monthly|thousands }}/měsíc.

Přes karty minulý měsíc přišlo celkem {{ charts.countries.revenue_memberships|thousands }} Kč.
Když se použijí procenta z grafu níže, odhadem by mělo být {{ charts.countries.revenue_memberships_non_cz|thousands }} Kč odjinud než z Česka. {% if charts.countries.oss_limit_czk_monthly > charts.countries.revenue_memberships_non_cz %}**Takže asi dobrý.**{% endif %}

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
