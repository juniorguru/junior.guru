---
title: Marketing junior.guru
template: main_about.html
---

{% from 'macros.html' import note, lead with context %}

# Marketing

{% call lead() %}
Co dělá junior.guru v rámci marketingu a jak se mu v tom daří? Sociální sítě, newsletter, základní měření výkonnosti jednotlivých kanálů.
{% endcall %}

[TOC]

## Sociální sítě a newsletter

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

## Výkonnost kanálů podle ankety

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

## Výkonnost kanálů podle předchozí stránky

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
