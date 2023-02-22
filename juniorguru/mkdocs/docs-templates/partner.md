{% from 'macros.html' import lead, figure, partner_link, note with context %}

{% set active_partnership = partner.active_partnership() %}


# Partnerství s firmou {{ partner.name }}

{% call lead() %}
  Firma {{ partner.name }} je partnerem junior.guru od {{ '{:%-d.%-m.%Y}'.format(partner.first_partnership().starts_on) }}.
  Cílem tohoto přehledu je transparentně popsat, co je domluveno, a jak se to daří plnit.
  Díky tomu všichni vědí, jak na tom jsou. Tato stránka je veřejná, ale vyhledávačům není povoleno ji evidovat a zobrazovat.
{% endcall %}

{{ figure(partner.logo_path, partner.name, 500, 250, class="standout-bottom") }}

<div class="table-responsive"><table class="table">
  <tr>
    <th>Název</th>
    <td>{{ partner.name }}</td>
  </tr>
  <tr>
    <th>Odkaz</th>
    <td>{{ partner_link(partner.url, partner.url, 'open') }}</td>
  </tr>
  <tr>
    <th>Tarif</th>
    <td>
      <a href="{{ pages|docs_url('pricing.md')|url }}">{{ active_partnership.plan.name }}</a>
      {% for _ in range(active_partnership.plan.hierarchy_rank + 1) %}
        {{ 'star'|icon }}
      {% endfor %}
    </td>
  </tr>
  <tr>
    <th>Členů v klubu</th>
    <td>
      {{ partner.list_members|length }} z 15
    </td>
  </tr>
  <tr>
    <th>Prodloužení</th>
    <td>
      {% if active_partnership.expires_on %}
        Partnerství skončí za {{ active_partnership.days_until_expires() }} dní
        (do {{ '{:%-d.%-m.%Y}'.format(active_partnership.expires_on) }})
      {% else %}
        Partnerství nemá stanovený konec
      {% endif %}
    </td>
  </tr>
</table></div>

## Výsledky spolupráce

<div class="table-responsive"><table class="table">
  {% for podcast_episode in partner.list_podcast_episodes %}
  <tr>
    <td>Epizoda podcastu {{ 'mic'|icon }}</td>
    <td><a href="{{ podcast_episode.url }}">{{ podcast_episode.title }}</a></td>
  </tr>
  {% endfor %}

  {% for job in partner.list_jobs %}
  <tr>
    <td>Pracovní inzerát {{ 'pin-angle'|icon }}</td>
    <td>
      <a href="{{ job.url }}">{{ job.title }}</a><br>
      <small>
        {{ 'graph-up'|icon }} statistiky za
        <a href="{{ job.submitted_job.analytics_url(30) }}" target="_blank" rel="noopener">měsíc</a>,
        <a href="{{ job.submitted_job.analytics_url(365) }}" target="_blank" rel="noopener">rok</a>
      </small>
    </td>
  </tr>
  {% endfor %}

  {% for event in partner.list_events %}
  <tr>
    <td>Akce v klubu {{ 'calendar-event'|icon }}</td>
    <td><a href="{{ event.url }}">{{ event.title }}</a></td>
  </tr>
  {% endfor %}

  {% for benefit in active_partnership.evaluate_benefits(benefits_evaluators) %}
  {% if benefit.slug == 'welcome_social' and benefit.done %}
  <tr>
    <td>Oznámení na sociálních sítích {{ benefit.icon|icon }}</td>
    <td>
      <a href="{{ benefit.done }}">LinkedIn</a>
    </td>
  </tr>
  {% endif %}
  {% endfor %}

  {% set intro = partner.intro %}
  <tr>
    <td>Oznámení v klubu {{ 'balloon'|icon }}</td>
    <td>
      {% if intro %}
        <a href="{{ intro.url }}">{{ '{:%-d.%-m.%Y}'.format(intro.created_at) }}</a>
      {% else %}
        Objeví se každým dnem!
      {% endif %}
    </td>
  </tr>

  {% for partnership in partner.list_partnerships_history %}
    {% for agreement in partnership.agreements_registry|selectattr('done') %}
    <tr>
      <td>Další ujednání {{ 'box'|icon }}</td>
      <td>
        {{ agreement.text|md|remove_p }}
      </td>
    </tr>
    {% endfor %}
  {% endfor %}
</table></div>

{% call note() -%}
  {{ 'exclamation-circle'|icon }} Jako placená spolupráce se berou jen akce v klubu a epizody podcastu, které iniciovala firma na základě tarifu. Pokud si někoho sami pozveme, tak se to jako placená spolupráce nebere.
{%- endcall %}

## Stav benefitů

<div class="table-responsive"><table class="table">
{% for benefit in active_partnership.evaluate_benefits(benefits_evaluators) %}
<tr>
  {% if benefit.done %}
    <td class="text-success">{{ 'check-circle-fill'|icon }}</td>
  {% else %}
    <td class="text-danger">{{ 'x-circle'|icon }}</td>
  {% endif %}
  <td>
    {{ benefit.text|md|remove_p }}
    {{ benefit.icon|icon }}
  </td>
</tr>
{% endfor %}
</table></div>

{% if active_partnership.agreements_registry %}
### Další ujednání

<div class="table-responsive"><table class="table">
{% for agreement in active_partnership.agreements_registry %}
<tr>
  {% if agreement.done %}
    <td class="text-success">{{ 'check-circle-fill'|icon }}</td>
  {% else %}
    <td class="text-danger">{{ 'x-circle'|icon }}</td>
  {% endif %}
  <td>
    {{ agreement.text|md|remove_p }}
  </td>
</tr>
{% endfor %}
</table></div>
{% endif %}

## Historie

<div class="table-responsive"><table class="table">
  <tr>
    <th>Tarif</th>
    <th>Od</th>
    <th>Do</th>
  </tr>
{% for partnership in partner.list_partnerships_history %}
  <tr>
    <td>
      {% if partnership.plan %}
        {{ partnership.plan.name }}
      {% else %}
        (starý tarif, už neexistuje)
      {% endif %}
    </td>
    <td>{{ '{:%-d.%-m.%Y}'.format(partnership.starts_on) }}</td>
    <td>
      {% if partnership.expires_on %}
        {{ '{:%-d.%-m.%Y}'.format(partnership.expires_on) }}
      {% else %}
        ?
      {% endif %}
    </td>
  </tr>
{% endfor %}
</table></div>

{% if partner.first_partnership().starts_on.year < 2023 %}
  {% call note() -%}
    {{ 'exclamation-circle'|icon }} Partnerství jsou vždy na jeden rok, ale do 1.1.2023 se při prodlužování nedělal nový záznam, pouze se přepsalo datum ukončení.
  {%- endcall %}
{% endif %}

<div class="pagination">
  <div class="pagination-control">
    <a href="{{ pages|docs_url('open.md')|url }}#firemni-partnerstvi" class="pagination-button">
      {{ 'arrow-left'|icon }}
      Všechna firemní partnerství
    </a>
  </div>
</div>
