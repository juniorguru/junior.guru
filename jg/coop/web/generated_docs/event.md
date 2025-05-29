{% from 'macros.html' import img, lead, club_teaser, note, link_card with context %}

# {{ event.get_full_title() }}

{% set is_past_event = event.start_at < now.replace(tzinfo=none) %}

{% call lead() %}
Klub junior.guru pořádá vzdělávací akce, online na svém Discordu.
{%- if is_past_event %}
  Toto je jeda z nich. Už proběhla, ale najdeš tady o ní všechny informace
  {%- if event.has_recording %}, včetně odkazu na záznam.{% else %}.{% endif %}
{% else %}
  Toto je upoutávka na jednu z nich, která teprve proběhne. Přečti si, jak se k nám můžeš připojit!
{% endif %}
{% endcall %}

{% if is_past_event %}
<p class="c2a airy">
  <span class="c2a-text display">
    Akce proběhla <strong>{{ '{:%-d.%-m.%Y}'.format(event.start_at_prg) }}</strong>
    a trvala <strong>{{ event.duration_s|hours }}</strong>
  </span>
  <a class="c2a-button" href="#zaznam">Pusť si záznam</a>
</p>
{% else %}
<p class="c2a airy">
  <span class="c2a-text display">
    Akce bude <strong>{{ '{:%-d.%-m.%Y v %-H:%M}'.format(event.start_at_prg) }}</strong>,
    trvat má <strong>{{ event.duration_s|hours }}</strong>
  </span>
  <a class="c2a-button pulse" href="#jak-se-pripojit">Připoj se</a>
</p>
{% endif %}

## O čem to {% if is_past_event %} bylo{% else %}bude{% endif %}

{{ event.description|md }}

<div class="standout details">
  <div class="details-info avatar">
    <div class="details-image">
      {{ img("static/" + event.avatar_path, event.get_full_title(), 400, 400, class='details-thumbnail', lazy=False) }}
    </div>
    <div class="details-body">
      <h5 class="details-heading">{{ event.bio_name }}</h5>
      <div class="details-text compact">
        {{ event.bio_title }}
      </div>
      <div class="details-text">
        {{ event.bio|md }}
      </div>
      {#
      <ul class="details-items compact">
        {% for url in event.bio_links %}
          <li class="details-item">{{ url }}</li>
        {% endfor %}
      </ul>
      #}
    </div>
  </div>
</div>

{% if is_past_event %}

## Záznam
<!-- {{ club_teaser("Hledej recenze v klubu") }} -->

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }} Tahle sekce je dočasně mimo provoz. Podívej se sem prosím zítra, už to bude dodělané.
{% endcall %}

{% else %}

## Jak se připojit
<!-- {{ club_teaser("Připoj se na 14 dní zdarma") }} -->

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }} Tahle sekce je dočasně mimo provoz. Podívej se sem prosím zítra, už to bude dodělané.
{% endcall %}

{% endif %}


{#
<p>
  <strong>{{ '{:%-d.%-m.%Y}'.format(event.start_at) }}</strong>
  —
  {{ event.start_at|local_time }} až {{ event.end_at|local_time }} online v klubovně</strong>{% if event.club_recording_url %},
  <a href="{{ event.club_recording_url }}">záznam pro členy</a> ({{ event.private_recording_duration_s|hours }}){% endif %}{% if event.public_recording_url %},
  <a href="{{ event.public_recording_url }}">veřejný záznam</a> ({{ event.public_recording_duration_s|hours }}){% endif %}
  {%- if event.poster_path %}, <a href="{{ ("static/" + event.poster_path)|url }}">plakátek</a>{% endif -%}
</p>

Zveme si profíky na témata kolem programování nebo shánění první práce v oboru.
  Pojetí akcí je vždy vyloženě pro začátečníky.
  Žádná záplava odborných „termitů“, které ti nikdo nevysvětlil!

## Jak to funguje?

Večerní tematické přednášky jsou vždy předem oznámeny na konkrétní datum a čas. Pokud chceš přednášku slyšet, připoj se v ten čas do hlasové místnosti #přednášky. Po skončení přednášky není žádný další oficiální program. Cílem je, aby přednášky byly spíše rychlé a časté, než plánované do celovečerních bloků. Tak nezaberou příliš mnoho času a můžeš se připojit, i když máš nabitý den, nebo prostě jen nechceš trávit celý večer na nějakém srazu.

Nepořizujeme profesionální záznam, ale snažíme se alespoň nahrát obrazovku, aby si přednášku mohli pustit i členové, kteří v čas přednášky nemají čas. Nedáváme žádnou záruku na existenci záznamu ani jeho kvalitu. Pokud existuje, je členům k dispozici skrze tajný odkaz na YouTube. Odkaz na video veřejně prosím nesdílej, ale kamarádům jej klidně pošli – asi stejně jako když pro známé odemykáš placený článek v novinách.
#}

## Mohlo by tě zajímat

<div class="link-cards wide">
{% set events_planned_sample = events_planned|rejectattr("id", "equalto", event.id)|sample(1) %}
{% set events_archive_sample = events_archive|rejectattr("id", "equalto", event.id)|sample(2) %}
{% set events_sample = [
  events_planned_sample.0 or events_archive_sample.0,
  events_archive_sample.1,
] %}

{% for event in events_sample %}
{{ link_card(
  event.title,
  pages|docs_url(event.page_url)|url,
  caption=event.bio_name,
  thumbnail_url="static/" + event.plain_poster_path,
) }}
{% endfor %}
</div>

<div class="pagination">
  <div class="pagination-control">
    <a href="{{ (page|parent_page).url|url }}" class="pagination-button">
      {{ 'arrow-left'|icon }}
      Všechny akce
    </a>
  </div>
</div>
