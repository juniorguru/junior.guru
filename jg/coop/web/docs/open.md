---
title: Jak se daří provozovat junior.guru
description: Čísla, statistiky, grafy. Jak se Honzovi daří provozovat junior.guru?
---

{% from 'macros.html' import note with context %}

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }} Tuhle stránku zrovna po kouskách přesouvám [sem](about/index.md), takže si raději vezměte ochranné pomůcky, pohybujete se po staveništi.
{% endcall %}

# Čísla a grafy

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
                'data': charts.subscriptions_breakdown.pop('sponsor'),
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
