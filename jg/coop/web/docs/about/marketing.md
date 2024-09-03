---
title: Marketing junior.guru
template: main_about.html
---

{% from 'macros.html' import lead with context %}

# Marketing

{% call lead() %}
Co dělá junior.guru v rámci marketingu a jak se mu v tom daří? Týdenní poznámky, sociální sítě, newsletter… K tomu pár grafů se základním měřením výkonnosti jednotlivých kanálů.
{% endcall %}

[TOC]

## Reklama vs. inbound marketing

Od začátku existence si junior.guru nikde nezaplatilo žádnou reklamu. Spoléhá se na vlastní marketingové aktivity a čistě organický dosah.
Je to částečně proto, že Honza v osobním životě reklamu rád nemá a spíš mu vadí.

Za dosavadním úspěchem junior.guru stojí především víra v samonosný obsah užitečný pro společnost, který si pak lidi sdílí dobrovolně.
Tahounem návštěvnosti je tedy [inbound marketing](https://cs.wikipedia.org/wiki/Inbound_marketing).
Obsah ale není tvořen s účelem, aby někoho přilákal, je tvořen primárně proto, aby byl někomu užitečný.

Honza se snaží dávat důraz na základní SEO poučky a vytvářet rychle se načítající webovou stránku, což má Google rád a přivádí potom na web lidi z vyhledávání.

## Otevřenost a Týdenní poznámky

Jednou z [hodnot junior.guru](./mission.md) je otevřenost, díky které existuje celá tato sekce webu, kde jsou transparentně všechny čísla a grafy.
V souladu s otevřeností jsou i pravidelné „týdenní poznámky” na Honzově blogu:

{% for blog_article in blog[:5] %}
-   [{{ blog_article.title }}]({{ blog_article.url }}), {{ '{:%-d.%-m.%Y}'.format(blog_article.published_on) }}
{% endfor %}

Byť primárním záměrem této otevřenosti není marketing, je vedlejším produktem.
Lidé rádi nakukují pod pokličku, projektu potom fandí a šíří o něm povědomí.

Když jeli [trabanti do Afriky](https://www.ceskatelevize.cz/porady/10660318675-trabantem-napric-afrikou/), našlo se ohromné publikum lidí, kteří by tam nikdy nejeli, ale fandili jim a drželi palce, bavilo je sledovat tu cestu a ty obtíže. Taková trochu reality show. Když Honza píše o svém podnikání, lidi si připadají, že jsou součástí toho příběhu, že mají kousek toho úspěchu.

## Sociální sítě

V roce 2022 [Honzu unavily sociální sítě](https://honzajavorek.cz/blog/moje-nova-strategie-na-socialni-site/) a z většiny odešel.
Aktuálně je aktivní hlavně na LinkedInu a uvažuje o tom, že by víc využíval YouTube.
Nejraději používá [Mastodon](https://mastodonczech.cz/@honzajavorek), ale spíš pro soukromé než marketingové účely.

- [LinkedIn](https://www.linkedin.com/in/honzajavorek/)
- [YouTube](https://www.youtube.com/@juniordotguru)
- [Mastodon](https://mastodonczech.cz/@honzajavorek/)

Žádnou ucelenou strategii nemá a plácá příspěvky na sítě tak, jak to cítí.
Nemá rád poskakování podle toho, jak algoritmus píská, takže nedbá obecných doporučení a příspěvky hází nepravidelně, podle nálady, ne podle redakčního plánu.

## Newsletter

Dříve existoval newsletter junior.guru, kde se rozesílaly aktuální nabídky práce, postupně i zajímavé tipy.
Ten byl zrušen pro nedostatek sil se mu věnovat a také jako zbytečná duplicita vedle [klubu](../club.md).

Newsletter na obnovení stále čeká, ale alespoň se na web už vrátil [sběrný formulář pro zadávání e-mailové adresy](../news.jinja).
Restart rozesílání je v plánu, ale zatím bohužel pouze v plánu a nic se neposílá.

## Veřejná vystoupení a publikace

Na Honzově webu je [historie všech jeho vystoupení a publikací](https://honzajavorek.cz/#appearances).
Postupně opouští psaní článků nebo přednášení na srazech a oborových konferencích.
Preferuje vystupování v podcastech, rozhovorech a diskuzních panelech.

Oproti psaní článku, které může zabrat i týden, nebo přednášce, která vyžaduje mnoho příprav a stresu, jsou nároky na rozhovor minimální, a přesto má výsledek dosah.

## Sociální sítě a newsletter

Vývoj počtu sledujících na profilech na relevantních sociálních sítích a počtu odběratelů newsletteru.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="300"
    data-chart-type="line"
    data-chart="{{ {
        'labels': charts.followers_breakdown_labels,
        'datasets': [
            {
                'label': 'newsletter',
                'data': charts.followers_breakdown.pop('newsletter'),
                'borderColor': '#02cabb',
                'borderWidth': 2,
            },
            {
                'label': 'osobní LinkedIn',
                'data': charts.followers_breakdown.pop('linkedin_personal'),
                'borderColor': '#1755d1',
                'borderWidth': 2,
            },
            {
                'label': 'YouTube',
                'data': charts.followers_breakdown.pop('youtube'),
                'borderColor': '#dc3545',
                'borderWidth': 2,
            },
            {
                'label': 'osobní GitHub',
                'data': charts.followers_breakdown.pop('github_personal'),
                'borderColor': '#343434',
                'borderWidth': 2,
            },
            {
                'label': 'LinkedIn',
                'data': charts.followers_breakdown.pop('linkedin'),
                'borderColor': '#1755d1',
                'borderWidth': 1,
            },
            {
                'label': 'Mastodon',
                'data': charts.followers_breakdown.pop('mastodon'),
                'borderColor': '#563acc',
                'borderWidth': 1,
            },
            {
                'label': 'GitHub',
                'data': charts.followers_breakdown.pop('github'),
                'borderColor': '#343434',
                'borderWidth': 1,
            }
        ],
    }|tojson|forceescape }}"
    {{ charts.followers_breakdown.keys()|list|assert_empty }}
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'plugins': {'annotation': charts.followers_breakdown_annotations},
    }|tojson|forceescape }}"></canvas></div></div>

## Výkonnost kanálů podle ankety

Když se někdo registruje do klubu, může v anketě sdělit, kde na junior.guru narazil.
Graf porovnává kolik lidí jednotlivé marketingové kanály přivedly do klubu, a kolik z toho doposud bylo peněz.
Procenta nejsou podíl ze všech příchozích, ale z **{{ charts.total_marketing_breakdown_count }}** lidí, kteří odpověděli na anketu.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="300"
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

## Výkonnost kanálů podle předchozí stránky

Když se někdo registruje do klubu, systém si uloží [referrer](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referer), tzn. z jaké webové stránky přišel.
Graf porovnává kolik lidí jednotlivé marketingové kanály přivedly do klubu, a kolik z toho doposud bylo peněz.
Procenta nejsou podíl ze všech příchozích, ale z **{{ charts.total_referrer_breakdown_count }}** lidí, kteří měli _referrer_ odjinud než z junior.guru.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="300"
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
