{% from 'macros.html' import lead, img, partner_link, podcast_player with context %}

<nav aria-label="breadcrumb">
  <ol class="breadcrumb">
    <li class="breadcrumb-item">
      <a href="{{ (page|parent_page).url|url }}">
        {{ (page|parent_page).title }}
      </a>
    </li>
    <li class="breadcrumb-item active" aria-current="page">
      Epizoda {{ podcast_episode.number }}
    </li>
  </ol>
</nav>

# {{ podcast_episode.title_numbered }}

{#
{% call lead() %}
  ...
{% endcall %}
#}

<div>
{% if podcast_episode.partner %}
<p>
  <span class="badge text-bg-primary">Spolupráce</span>
  <small>
  Akce vznikla v rámci
  {% set active_partnership = podcast_episode.partner.active_partnership() %}
  {% if active_partnership %}
    <a href="{{ pages|docs_url(active_partnership.page_url)|url }}">placeného partnerství</a>
  {% else %}
    placeného partnerství
  {% endif %}
  s firmou {{ partner_link(podcast_episode.partner.name, podcast_episode.partner.url, 'podcast') }}
  </small>
</p>
{% endif %}
{{ img('static/' + podcast_episode.avatar_path, podcast_episode.title, 100, 100, class='podcast-episode-image') }}
<p>
<strong>{{ '{:%-d.%-m.%Y}'.format(podcast_episode.publish_on) }}</strong>
— {{ podcast_episode.description }}
</p>
{{ podcast_player(podcast_episode, class='podcast-episode-player') }}
</div>

<div class="pagination">
  <div class="pagination-control">
    <a href="{{ (page|parent_page).url|url }}" class="pagination-button">
      {{ 'arrow-left'|icon }}
      Všechny epizody
    </a>
  </div>
</div>
