---
title: Jak se daří provozovat junior.guru
description: Čísla, statistiky, grafy. Jak se Honzovi daří provozovat junior.guru?
---

{% from 'macros.html' import note with context %}

# Čísla a grafy

Stránku jsem vytvořil po vzoru [jiných otevřených projektů](https://openstartuplist.com/), především [NomadListu](https://nomadlist.com/open). Tyto grafy a čísla stejně potřebuji pro svou vlastní potřebu, takže proč je v rámci transparentnosti nemít rovnou na webu, že?

Finanční data se každý den stahují přímo z mého podnikatelského účtu u Fio banky. Používám [svou vlastní Python knihovnu](https://pypi.org/project/fiobank/), kterou jsem kdysi vytvořil.

## Čistý zisk

Zisk jsou výnosy mínus náklady včetně daní, tedy částka, která už jde z mého podnikání přímo do rodinného rozpočtu. Aktuální čistý zisk junior.guru je **{{ profit_ttm|thousands }} Kč měsíčně**. Spočítáno jako zisk za posledních 12 měsíců (TTM, _trailing twelve months_) vydělený 12.

<canvas
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
        'interaction': {'mode': 'index'}
    }|tojson|forceescape }}"></canvas>

### Cíl

Ze svých předchozích angažmá mám nějaké úspory, díky nimž mohu JG provozovat, i když zatím moc nevydělá. Jako seniorní programátor s mými zkušenostmi bych prací pro pražskou nebo zahraniční firmu mohl vydělávat kolem 100.000 Kč měsíčně čistého. Dohodli jsme se doma, že když mě JG tolik baví, zkusím to provozovat a i když to vydělá méně, stojí nám to za větší domácí pohodu. Na JG dělám na full time, máme jedno malé dítě, nemáme auto, bydlíme v nájmu uprostřed Prahy. Kdybych vydělával 40.000 Kč čistého, tak by nám to myslím vystačilo. Cílem JG není zbohatnout, ale dlouhodobě pomáhat juniorům, pohodlně živit rodinu a žít při tom šťastný život.

<div class="charts-progress">
    {% set progress_max = 40000 %}
    {% set progress_ptc = ((profit_ttm * 100) / progress_max)|round|int %}
    <div class="progress-bar" role="progressbar" style="width: {{ progress_ptc }}%" aria-valuenow="{{ progress_ptc }}" aria-valuemin="0" aria-valuemax="{{ progress_max }}">
    {{ progress_ptc }} % ze {{ progress_max|thousands }} Kč
    </div>
</div>

## Výnosy a náklady

Následující graf zobrazuje vývoj mých výnosů a nákladů v každém konkrétním měsíci. Tenké linky zobrazují totéž, ale vždy za posledních 12 měsíců (TTM, _trailing twelve months_), vyděleno 12. Výnosy ani náklady totiž nejsou vždy pravidelného, měsíčního charakteru, jeden měsíc vydělám víc, jiný méně, stejné je to s výdaji. Zároveň nemám s nikým delší kontrakt než roční, ať už jsou to jednotlivci nebo firmy. Číslo za rok tedy stírá tyto skoky nahoru a dolů, ale protože můj byznys roste rychleji než ročním tempem, tak zase ukazuje možná menší číslo, než je realitou za poslední půlrok, čtvrtrok.

Čísla z konkrétních mesíců tedy pomáhají odtušit aktuální trendy. Čistý zisk je rozdíl mezi modrou a červenou čárou.

<canvas
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
        'interaction': {'mode': 'index'}
    }|tojson|forceescape }}"></canvas>

## Výnosy

Původně jsem se snažil JG živit z inzerce nabídek práce, ale byznys na tomto modelu jsem nedokázal dostatečně rozpohybovat tak, abych věřil, že má smysl v tom dál pokračovat. Mezitím jsem se pokusil zpeněžit [příručku](motivation.md) skrze loga firem a [prosil jsem návštěvníky webu o dobrovolné příspěvky](/donate/).

Ke konci roku 2020 jsem se rozhodl změnit byznys model a vytvořit kolem JG placenou komunitu na Discordu. Toto detailně popisuji ve svém [článku na blogu](https://honzajavorek.cz/blog/spoustim-klub/). [Klub](club.md) se veřejnosti otevřel v únoru 2021.

V ideálním případě by mě živilo individuální členství lidí v klubu, protože je to pravidelný, předvídatelný příjem, který mi navíc zajišťuje největší nezávislost.

Individuální členství ale nevystačí, takže si domlouvám [spolupráce s firmami]({{ pricing_url }}) vždy formou nějakého ročního firemního členství v klubu. Spolupráce s firmami jsou jednorázové větší příjmy, které lze obtížně předvídat a mohou ovlivňovat mou kritičnost k firmám, se kterými spolupracuji.

Inzerci nabídek práce nechci zrušit, ale aktuálně není na vrcholu mých priorit. Pokud, tak spíše v podobě dlouhodobé spolupráce s firmou, než formou jednorázových inzerátů.

Dobrovolné příspěvky stále hrají významnou roli v mých příjmech a velkou měrou právě díky nim JG ve svých počátcích neskončilo. Teď je ale čas postavit se na vlastní nohy! Možnost přispět zřejmě nezruším, ale přestal jsem ji propagovat. Chtěl bych, aby dobrovolné příspěvky jednou plně nahradilo individuální členství v klubu.

<canvas
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
                'label': 'firemní členství',
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
        'scales': {'x': {'stacked': True}, 'y': {'stacked': True}}
    }|tojson|forceescape }}"></canvas>

### Proč tu není MRR

MRR znamená _monthly recurring revenue_ a je základní metrikou většiny online byznysů, které jsou vedeny jako pravidelně placená služba. Je to součet výnosů, které mi pravidelně měsíčně chodí na účet skrze předplatné, tedy pravidelný příjem, na který se dá spolehnout. I když junior.guru je služba s členstvím na měsíční bázi a MRR by spočítat šlo, nakonec jsem se rozhodl jej zatím neřešit a dívám se spíš na ono TTM vydělené 12.

Jedním důvodem je složitost výpočtu. Data beru z bankovního účtu, kam mi ale nechodí částky za jednotlivé lidi. Stripe mi vždy posílá úhrnné částky za několik týdnů zpětně. Musel bych brát data zvlášť z Memberful. Navíc prodávám i roční členství, které bych musel rozpočítávat.

Druhým důvodem je malá vypovídající hodnota. Velkou část výnosů tvoří kontrakty s firmami, jež jsou nárazovým, ale ve svém množství poměrně stabilním příjmem. Pravidelné příjmy mám zase i z dobrovolných příspěvků, jež bych do MRR započítával jen velice složitě. Aby bylo číslo přesné, musel bych mít data o tom, jak přesně kdo přispívá přes Patreon nebo GitHub Sponsors, což se mi nevyplatí řešit.

## Náklady

Zahrnuji pouze náklady na byznys, ale zase i s daněmi a odvody na zdravotní a sociální pojištění. V roce 2020 je v nich díra, protože kvůli covidu-19 nebyla povinnost je platit. Občas jdou do mínusu (stává se z nich příjem), protože mi úřady něco vrátily.

Neplatím si žádnou reklamu. Výdaje na marketing jsou většinou za tisk samolepek apod. Také jsem si jednu dobu platil [Buffer](https://buffer.com/).

<canvas
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
                'label': 'různé',
                'data': charts_cost_breakdown.pop('miscellaneous'),
                'backgroundColor': '#dc3545',
            },
            {
                'label': 'právnička',
                'data': charts_cost_breakdown.pop('lawyer'),
                'backgroundColor': '#801515',
            },
            {
                'label': 'účetní',
                'data': charts_cost_breakdown.pop('accounting'),
                'backgroundColor': '#a9a9a9',
            },
            {
                'label': 'marketing',
                'data': charts_cost_breakdown.pop('marketing'),
                'backgroundColor': '#e8ccd7',
            },
            {
                'label': 'memberful.com',
                'data': charts_cost_breakdown.pop('memberful'),
                'backgroundColor': '#EF704F',
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
        'scales': {'x': {'stacked': True}, 'y': {'stacked': True}}
    }|tojson|forceescape }}"></canvas>

## Členové klubu

[Placený klub](https://junior.guru/club/) jsem [spustil](https://honzajavorek.cz/blog/spoustim-klub/) v únoru 2021. Aktuálně je na Discordu **{{ members_total_count }} uživatelů**.

Každý příchozí člen má v klubu dva týdny zdarma, bez ohledu na to, jakým způsobem za členství následně platí. Některým lidem dávám vstup do klubu zcela zdarma, ať už na základě vlastního uvážení, jako poděkování např. za přednášku v klubu, jako stipendium, nebo ze strategických důvodů. Jde o různé spolupráce s komunitami, podcasty, nebo třeba zvaní mentorů na specifické technologie, jejichž zastoupení na straně seniorů je v klubu slabé, ale od juniorů je po tématu poptávka.

S mentory z [CoreSkill](https://coreskill.tech/) máme symbiózu. Nic si navzájem neplatíme. Oni využívají platformu klubu pro svůj mentoring a své studenty. Všichni mají automaticky vstup zdarma. Klub má díky tomu experty na frontend a moderátora Dana Srba, který může zaskakovat, kdyby bylo potřeba.

Část lidí mi neplatí přes systém pro správu členství, ale dostali členství zdarma na základě toho, že mě [podporovali na GitHub Sponsors nebo Patreonu](/donate/). V důsledku to tedy zdarma není, jen mi peníze posílají jinudy. Mnohdy posílají víc, než by je stálo standardní členství v klubu.

S některými vzdělávacími agenturami mám dohodu, že do klubu pošlou studenty svých kurzů a proplatí jim členství na první tři měsíce. Agentura z toho má službu pro studenty navíc a já z toho mám to, že pokud se lidem v klubu zalíbí, budou si jej dál platit ze svého.

<canvas
    class="chart" width="400" height="200"
    data-chart-type="bar"
    data-chart="{{ {
        'labels': charts_club_labels,
        'datasets': [
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
                'label': 'symbióza s CoreSkill',
                'data': charts_subscriptions_breakdown.pop('coreskill'),
                'backgroundColor': '#638CDD',
            },
            {
                'label': 'přispívají přes GitHub Sponsors, Patreon',
                'data': charts_subscriptions_breakdown.pop('supporters'),
                'backgroundColor': '#02CABB',
            },
            {
                'label': 'členství si platí sami',
                'data': charts_subscriptions_breakdown.pop('individuals'),
                'backgroundColor': '#1755d1',
            },
            {
                'label': 'členství platí firma',
                'data': charts_subscriptions_breakdown.pop('company'),
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
        'scales': {'x': {'stacked': True}, 'y': {'stacked': True}}
    }|tojson|forceescape }}"></canvas>

## Podíl žen v klubu

Podíl žen na počtu členů sleduji z vlastní zvědavosti a není to žádná přesná metrika. Nikdo nikde nevyplňuje, zda je žena nebo muž. Pro účely statistiky se to určuje jen odhadem podle křestního jména a tvaru příjmení.

Pro srovnání, podle [analýzy ČSÚ z roku 2020](https://www.czso.cz/csu/czso/cri/lidske-zdroje-v-informacnich-technologiich-2020) je v českém IT pouze 10 % žen a tento podíl se od jejich poslední analýzy před několika lety nezlepšil, naopak nás definitivně předběhly už všechny ostatní státy v Evropě.

<canvas
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
        'scales': {'y': {'min': 0, 'max': 100}}
    }|tojson|forceescape }}"></canvas>

## Návštěvnost

Čísla návštěvnosti webu jsou na [simpleanalytics.com/junior.guru](https://simpleanalytics.com/junior.guru).

## Kód

Práci na kódu lze sledovat [na GitHubu](https://github.com/honzajavorek/junior.guru/graphs/contributors).
