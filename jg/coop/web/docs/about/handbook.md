---
title: O příručce na junior.guru
template: main_about.html
---

{% from 'macros.html' import lead with context %}

# Vše o příručce

{% call lead() %}
Informace o [příručce pro juniory](../handbook/index.md). Záměr a hodnoty, se kterými je tvořena. K tomu ještě pár zajímavých statistik.
{% endcall %}

[TOC]

## Záměr

Příručka existuje, aby se programování mohl naučit kdokoliv, kdo se ho naučit chce.
Cílem je ukázat, že to jde i bez vysoké školy, protože materiálů a kurzů je k tomu na internetu dost.
A že i jako samouk je možné sehnat si v oboru práci, a tím si splnit sen, nebo zlepšit životní úroveň.

Bez keců o tom, jak firmy berou každého, peníze se budou jen sypat, a programovat se naučíš za měsíc.
Na junior.guru se dovíš, co je doopravdy potřeba.
Díky tomu budeš vědět, co očekávat, ať se na to můžeš adekvátně připravit.

A je jedno, jestli chceš programovat pro zábavu, plánuješ si něco automatizovat, nebo toužíš po kariéře v IT.
Jestli jsi z velkého města s širokými možnostmi, nebo z odlehlé vesnice.
Jestli jsi žena, muž, stará, mladý.
Jestli máš kůži růžovou nebo hnědou.

## Licence

Příručka je vydávána pod licencí [CC BY-SA](https://creativecommons.org/licenses/by-sa/4.0/deed.cs).
To znamená, že veškerý text může kdokoliv použít, klidně komerčně, pokud uvede autora a výsledek vystaví pod stejnou licencí.
Zdrojový text příručky je [na GitHubu](https://github.com/juniorguru/junior.guru/tree/main/jg/coop/web/docs/handbook).

## Monetizace

Žádná část příručky není zpoplatněná.
Žádný sběr dat o uživatelích.
Žádné cookies.
Osvěžující, že?

Honza nemá rád reklamy, takže ani ty na junior.guru nejsou.
Nahoře na příručce jsou nahoře akorát loga několika sponzorů:
{% for sponsor in sponsors_handbook %}
  {{- utm_link(sponsor.name, sponsor.url, 'about', sponsor.utm_campaign) -}}
  {% if not loop.last %}, {% endif -%}
{% endfor %}.

Jak je vidět z transparentních [finančních výsledků](./finances.md), psaní příručky je možné díky předplatnému za [klub](../club.md) a [příspěvkům sponzorů](../love.jinja).
Pokud se ti příručka líbí nebo ti pomohla, přispěj taky!

## Odkazy v příručce

Neprovádí se tady žádný affiliate marketing, výměna odkazů, sponzorované odkazy, nic takového.

Pokud je na internetu něco dobrého a užitečného, nebo je někde dobře zpracované určité téma, příručka na to odkáže.
Tenhle výběr je subjektivní.

Dnes není problém něco najít. Je problém rozlišit, čemu se vyplatí věnovat pozornost.
Proto se příručka snaží snižovat [rozhodovací paralýzu](https://cs.wikipedia.org/wiki/Rozhodovac%C3%AD_paral%C3%BDza), ne tě zaplavit odkazy na padesát „taky zajímavých“ věcí.

## Garanti kapitol  {: #garanti }

Autorem příručky na junior.guru je Honza Javorek.
Protože ale nerozumí všemu a chce, aby čtenáři mohli získat i rady, které by sám zpracovat nedokázal, začal některé kapitoly dělat ve spolupráci s dalšími profíky z oboru.

Ti mohou takzvaně „garantovat“ kapitolu na téma, kterému rozumí.
To znamená, že připravili texty a odkazy v kapitole a zavazují se stránku doplňovat a udržovat ji aktuální.

Jako poděkování dostávají na oné stránce prostor zviditelnit sebe nebo své služby.
Honza garantům nic neplatí, ani oni jemu.
Obsah kapitol edituje, tzn. hlídá kvalitu a texty upravuje tak, aby zapadly do zbytku příručky.

## Počty impresí

Pokud si sponzor [zaplatí nejvyšší tarif](../love.jinja), má logo na příručce.
Hodí se vědět, kolikrát se takové logo lidem zobrazí.

<figure class="figure"><div class="chart-figure"><canvas
    class="chart" width="400" height="230"
    data-chart-type="bar"
    data-chart="{{ {
        'labels': {
            'home': 'úvodní stránka',
            'courses': 'katalog kurzů',
            'handbook': 'příručka',
        }|mapping(charts.logo_impressions_breakdown.keys()),
        'datasets': [
            {
                'label': 'průměrný počet impresí měsíčně',
                'data': charts.logo_impressions_breakdown.values()|list,
                'backgroundColor': '#1755d1',
            },
        ],
    }|tojson|forceescape }}"
    data-chart-options="{{ {
        'interaction': {'mode': 'index'},
        'scales': {'y': {'beginAtZero': true}},
    }|tojson|forceescape }}"></canvas></div></figure>

## Práce na příručce

Všechny soubory spadající pod příručku mají aktuálně **{{ handbook_total_size|thousands }}** znaků.
Počítání znaků v souborech, kde se míchají Markdown a Jinja značky, má spoustu vad, ale aspoň něco.
[Podle Wikipedie](https://cs.wikipedia.org/wiki/Diplomov%C3%A1_pr%C3%A1ce) je 180.000 znaků doporučovaná velikost disertační práce (titul Ph.D.).

Když chce Honza na nějaké stránce něco doplnit, dělá si na jejím konci HTML komentář a do něj si ukládá nepříliš strukturované poznámky.
Ty se taky započítají do celkové velikosti, ale v grafu je jejich velikost zobrazena šedě, aby šlo vidět, jaký je poměr a kde ještě čeká kolik práce.

Příliš velké stránky bych měly být kratší, nebo by se měly rozdělit do více menších.
Ideální stránka příručky by měla pouze modrý sloupeček a ten by nesahal výše než k červené čáře.

<div class="chart-scroll"><div class="chart-container"><canvas
    class="chart" width="400" height="300"
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
