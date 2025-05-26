{% from 'macros.html' import img, lead, club_teaser with context %}

# {{ event.title }}

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

## Téma

{{ event.description|md }}

<div class="standout details">
  <div class="details-info avatar">
    <div class="details-image">
      {{ img("static/" + event.avatar_path, event.full_title, 400, 400, class='details-thumbnail', lazy=False) }}
    </div>
    <div class="details-body">
      <ul class="details-items">
        <li class="details-item">
          <strong>Kdy:</strong>
          {{ '{:%-d.%-m.%Y, %-H:%M}'.format(event.start_at_prg) }}
        </li>
        <li class="details-item">
          <strong>{% if is_past_event %}Délka{% else %}Očekávaná délka{% endif %}:</strong>
          {{ event.duration_s|hours }}
        </li>
      </ul>
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

{#

{% if is_past_event %}

## Záznam
{{ club_teaser("Hledej recenze v klubu") }}

{% else %}

## Jak se připojit
{{ club_teaser("Připoj se na 14 dní zdarma") }}

{% endif %}

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

<div class="pagination">
  <div class="pagination-control">
    <a href="{{ (page|parent_page).url|url }}" class="pagination-button">
      {{ 'arrow-left'|icon }}
      Všechny akce
    </a>
  </div>
</div>
