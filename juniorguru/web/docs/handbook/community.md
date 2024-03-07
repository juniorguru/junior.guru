---
title: Komunity
emoji: 🎪
stages: [trying, preparing, applying]
description: Programátorské komunity tě dokážou posunout jako nic jiného. Kde je najít? Co od toho čekat?
template: main_handbook.html
---

{% from 'macros.html' import blockquote_avatar, lead, link_card with context %}


# Jak na programátorské komunity

{% call lead() %}
  Srazy u piva, konference, online přednášky, firemní akce, jednorázové workshopy, tematické večery.
  Programátorské komunity tě dokážou posunout jako nic jiného. Jak do nich vplout a co od toho čekat?
{% endcall %}

Je velmi těžké se učit zcela samostatně, bez kontaktu s dalšími samouky nebo lidmi z nového oboru. Důvodů, proč polevit, může nastat hodně. Proto je dobré pravidelně se setkávat s komunitou začínajících i pokročilých programátorů a nabíjet se tak novou energií a inspirací. Dříve existovaly hlavně dva druhy setkání: místní srazy a celostátní konference. Během covidu-19 bylo mnoho akcí zrušeno, nebo přešlo do online podoby.

{% call blockquote_avatar(
  'Vplávaj do IT komunít. Každá technológia má svoje skupiny, udalosti, konferencie, stretnutia pri pive. Zúčastňuj sa! Niekto tam má často prednášku, ale hlavne ľudia sa tam rozprávajú a stretávajú a majú joby a zákazky, chcú pomôcť, hľadajú parťáka, zamestnanca…',
  'yablko.jpg',
  'yablko'
) %}
  yablko, lektor online kurzů, ve svém [videu o tom, jak si najít praxi](https://www.youtube.com/watch?v=3-wsqhCK-wU&list=PLhB6F20C-jTPITEXEHus6fVZDfNxzRbv_)
{% endcall %}

<div class="link-cards">
  {{ link_card(
    'Klub junior.guru',
    pages|docs_url('club.md')|url,
    'Diskutuj v klubu pro začátečníky, kde najdeš pomoc, motivaci, kamarády, práci.',
    badge_icon='chat-dots',
    badge_text='Online komunita',
  ) }}

  {{ link_card(
    'Pyvo',
    'https://pyvo.cz',
    'Poznej Python programátory ve svém okolí. Pomohou, budou tě motivovat.',
    badge_icon='calendar-week',
    badge_text='Srazy',
  ) }}

  {{ link_card(
    'Meetup',
    'https://www.meetup.com/',
    'Najdi srazy ve svém okolí, poznej různá odvětví IT, potkej lidi.',
    badge_icon='calendar-week',
    badge_text='Srazy',
  ) }}

  {{ link_card(
    'PyCon CZ',
    'https://cz.pycon.org',
    'Přijeď na českou Python konferenci.',
    badge_icon='calendar-check',
    badge_text='Konference',
  ) }}

  {{ link_card(
    'PyCon SK',
    'https://pycon.sk',
    'Přijeď na slovenskou Python konferenci.',
    badge_icon='calendar-check',
    badge_text='Konference',
  ) }}

  {{ link_card(
    'Write The Docs Prague',
    'https://www.writethedocs.org/conf/',
    'Přijeď na konferenci o psaní technické dokumentace.',
    badge_icon='calendar-check',
    badge_text='Konference',
  ) }}
</div>

### Nebudu mimo mísu?    <span id="beginner-friendly"></span>

Výše uvedené akce jsou vhodné i pro začátečníky a účastní se jich významné procento žen. Náplní těchto akcí jsou odborné přednášky pro různé úrovně znalostí a networking — povídání si s lidmi. Vždy se odehrávají v neformálním, pohodovém prostředí.

### Kde na to vzít?    <span id="fin-aid"></span>

Na konference je potřeba si koupit lístek. Výše zmíněné konference mají velmi dostupné lístky se slevami (např. pro studenty), ale i tak je možné, že je mimo tvé finanční možnosti se účastnit. Pro takový případ konference poskytují „Financial Aid“ — finanční pomoc s lístkem, ubytováním nebo cestou.


<!-- {#

pracovní veletrhy

#} -->
