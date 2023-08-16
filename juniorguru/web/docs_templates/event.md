{% from 'macros.html' import lead, img, partner_link with context %}

<nav aria-label="breadcrumb">
  <ol class="breadcrumb">
    <li class="breadcrumb-item">
      <a href="{{ parent_page.url|url }}">
        {{ parent_page.title }}
      </a>
    </li>
    <li class="breadcrumb-item active" aria-current="page">
      {{ event.title }}
    </li>
  </ol>
</nav>

# {{ event.title }}

{% call lead() %}
  <!-- TODO Tady je aspoň základní info, které ti pomůže s rozhodováním. -->
{% endcall %}

{% if event.partner %}
<p>
  <span class="badge text-bg-primary">Spolupráce</span>
  <small>
  Akce vznikla v rámci
  {% set active_partnership = event.partner.active_partnership() %}
  {% if active_partnership %}
    <a href="{{ pages|docs_url(active_partnership.page_url)|url }}">placeného partnerství</a>
  {% else %}
    placeného partnerství
  {% endif %}
  s firmou {{ partner_link(event.partner.name, event.partner.url, 'podcast') }}
  </small>
</p>
{% endif %}
<p>
  <strong>{{ '{:%-d.%-m.%Y}'.format(event.start_at) }}</strong>
  —
  {{ event.start_at|local_time }} online v klubovně</strong>{% if event.recording_url %},
  <a href="{{ event.recording_url }}">záznam pro členy</a>{% endif %}{% if event.public_recording_url %},
  <a href="{{ event.public_recording_url }}">veřejný záznam</a>{% endif %}
</p>
{{ event.description|md }}

## {{ event.bio_name }}

<div>
{{ img('static/' + event.avatar_path, event.title, 100, 100, class='podcast-episode-image') }}
{{ event.bio|md }}
</div>

<div class="pagination">
  <div class="pagination-control">
    <a href="{{ parent_page.url|url }}" class="pagination-button">
      {{ 'arrow-left'|icon }}
      Všechny akce
    </a>
  </div>
</div>
