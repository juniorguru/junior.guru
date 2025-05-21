{% from 'macros.html' import img, lead with context %}

# {{ event.title }}

{#
{% call lead() %}
  ...
{% endcall %}
#}

{#

## Jak to funguje?

Večerní tematické přednášky jsou vždy předem oznámeny na konkrétní datum a čas. Pokud chceš přednášku slyšet, připoj se v ten čas do hlasové místnosti #přednášky. Po skončení přednášky není žádný další oficiální program. Cílem je, aby přednášky byly spíše rychlé a časté, než plánované do celovečerních bloků. Tak nezaberou příliš mnoho času a můžeš se připojit, i když máš nabitý den, nebo prostě jen nechceš trávit celý večer na nějakém srazu.

Nepořizujeme profesionální záznam, ale snažíme se alespoň nahrát obrazovku, aby si přednášku mohli pustit i členové, kteří v čas přednášky nemají čas. Nedáváme žádnou záruku na existenci záznamu ani jeho kvalitu. Pokud existuje, je členům k dispozici skrze tajný odkaz na YouTube. Odkaz na video veřejně prosím nesdílej, ale kamarádům jej klidně pošli – asi stejně jako když pro známé odemykáš placený článek v novinách.
#}

<p>
  <strong>{{ '{:%-d.%-m.%Y}'.format(event.start_at) }}</strong>
  —
  {{ event.start_at|local_time }} až {{ event.end_at|local_time }} online v klubovně</strong>{% if event.club_recording_url %},
  <a href="{{ event.club_recording_url }}">záznam pro členy</a> ({{ event.private_recording_duration_s|hours }}){% endif %}{% if event.public_recording_url %},
  <a href="{{ event.public_recording_url }}">veřejný záznam</a> ({{ event.public_recording_duration_s|hours }}){% endif %}
  {%- if event.poster_path %}, <a href="{{ ("static/" + event.poster_path)|url }}">plakátek</a>{% endif -%}
</p>
{{ event.description|md }}

## {{ event.bio_name }}

<div>
{{ img('static/' + event.avatar_path, event.title, 100, 100, class='news-page-image') }}
{{ event.bio|md }}
</div>

<div class="pagination">
  <div class="pagination-control">
    <a href="{{ (page|parent_page).url|url }}" class="pagination-button">
      {{ 'arrow-left'|icon }}
      Všechny akce
    </a>
  </div>
</div>
