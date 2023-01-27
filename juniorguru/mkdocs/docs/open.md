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

Seniorní programátor s mými zkušenostmi, který pracuje pro pražskou nebo zahraniční firmu, vydělává 100.000 Kč měsíčně čistého a víc. Dohodli jsme se doma, že když mě JG tolik baví, zkusím to provozovat a i když to vydělá méně, stojí nám to za větší domácí pohodu. Ze svých předchozích angažmá jsem měl úspory, díky nimž jsem mohl v začátcích JG držet při životě, i když zatím moc nevydělávalo.

Na JG pracuji na plný úvazek, mám malé dítě, ženu na rodičovské, nemáme auto, bydlíme v nájmu uprostřed Prahy. Jako podnikatel potřebuji velkou rezervu, abych se nemusel strachovat s každou změnou rodinných nákladů, jestli mohu pokračovat. Také mi nikdo neplatí dovolenou, nemocenskou, nespoří na důchod.

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

Původně jsem se snažil JG živit z inzerce nabídek práce, ale byznys na tomto modelu jsem nedokázal dostatečně rozpohybovat tak, abych věřil, že má smysl v tom dál pokračovat. Mezitím jsem se pokusil zpeněžit [příručku](handbook/index.md) skrze loga firem a prosil jsem návštěvníky webu o dobrovolné příspěvky.

Ke konci roku 2020 jsem se rozhodl změnit byznys model a vytvořit kolem JG placenou komunitu na Discordu. Toto detailně popisuji ve svém [článku na blogu](https://honzajavorek.cz/blog/spoustim-klub/). [Klub](club.md) se veřejnosti otevřel v únoru 2021.

V ideálním případě by mě živilo individuální členství lidí v klubu, protože je to pravidelný, předvídatelný příjem, který mi navíc zajišťuje největší nezávislost.

Individuální členství ale nevystačí, takže si domlouvám [spolupráce s firmami](pricing.md) vždy formou nějakého ročního firemního členství v klubu. Spolupráce s firmami jsou jednorázové větší příjmy, které lze obtížně předvídat a mohou ovlivňovat mou kritičnost k firmám, se kterými spolupracuji.

Inzerci nabídek práce nechci zrušit, ale aktuálně není na vrcholu mých priorit. Pokud, tak spíše v podobě dlouhodobé spolupráce s firmou, než formou jednorázových inzerátů.

Dobrovolné příspěvky stále hrají významnou roli v mých příjmech a velkou měrou právě díky nim JG ve svých počátcích neskončilo. Teď je ale čas postavit se na vlastní nohy! Možnost přispět zřejmě nezruším, ale přestal jsem ji propagovat. Chtěl bych, aby dobrovolné příspěvky jednou plně nahradilo individuální členství v klubu.

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
                'label': 'spolupráce s firmami',
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

## Členství v klubu

[Placený klub](https://junior.guru/club/) jsem [spustil](https://honzajavorek.cz/blog/spoustim-klub/) v únoru 2021. Aktuálně je na Discordu **{{ members_total_count }} členů**, ale platících členů může být i víc. Někteří si platí členství pouze aby mě podpořili, bez toho aby se vůbec na Discord přihlásili.

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

### Počet zpráv na Discordu

V grafu není celá historie, uchovávám data jen za rok zpětně. Některé kanály se nezapočítávají, např. „volná zábava“. Nejde o kompletní _engagement_, protože lidi se mohou v klubu projevovat různě, např. reagováním pomocí emoji.

Pouze orientační metrika. Nechci sledovat a glorifikovat _engagement_, protože lidi mají z klubu úplně v pohodě hodnotu i pokud si jej pouze čtou. K tématu doporučuji [Stop Measuring Community Engagement](https://rosie.land/posts/stop-measuring-community-engagement/).

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="200"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts_club_messages_labels,
        'datasets': [
            {
                'label': 'počet zpráv na Discordu',
                'data': charts_messages,
                'borderColor': '#1755d1',
                'borderWidth': 2,
            },
        ]
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'beginAtZero': true}},
        'plugins': {'annotation': charts_club_messages_annotations},
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
        'scales': {'y': {'min': 0, 'max': 100}},
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
