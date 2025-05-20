{% from 'macros.html' import img, lead with context %}

# {{ event.title }}

{#
{% call lead() %}
  ...
{% endcall %}
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
