{% from 'macros.html' import note, logo with context %}

{% set active_partnership = partner.active_partnership() %}


# {{ partner.name }}

Stránka popisující partnerství junior.guru s firmou {{ partner.name }}.

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }} Tuto stránku Honza právě připravuje. Brzy to tady bude hezčí.
{% endcall %}

## Tarif

{{ active_partnership.plan.name }}

{% for benefit in active_partnership.evaluate_benefits(benefits_evaluators) %}
- {{ benefit.icon|icon }} {{ benefit.text }} {% if benefit.done %}✅{% else %}❌{% endif %}
{% endfor %}


## Logo

{{ logo(partner.name, partner.logo_path, partner.url) }}

<!-- Logo na webu -->

## Do kdy

{% if active_partnership.expires_on %}
  - {{ '{:%-d.%-m.%Y}'.format(active_partnership.expires_on) }}
  - zbývá {{ active_partnership.remaining_days() }} dní
{% else %}
  - ?
  - zbývá věčnost
{% endif %}

## Uvítání v klubu

{% set intro = partner.intro %}
{% if intro %}
- [{{ '{:%-d.%-m.%Y}'.format(intro.created_at) }}]({{ intro.url }})
{% else %}
- Nemá 😱
{% endif %}

## Lidi

{{ partner.list_members|length }}

<!-- Konkretni lidi muzu poslat mailem, na webu byt nemuzou -->

## Inzeráty

{% for job in partner.list_jobs %}
- [{{ job.title }}]({{ job.url }})
{% endfor %}

<!-- Jsou tam informace i k inzerátům včetně toho, co původně chodilo do mailu -->

## Přednášky

<!-- Disclaimer o tom, že zveme lidi i bez toho, že by si to firma zaplatila -->

{% for event in partner.list_events %}
- {{ event.title }}
{% endfor %}

## Podcast

<!-- Disclaimer o tom, že zveme lidi i bez toho, že by si to firma zaplatila -->

{% for episode in partner.list_podcast_episodes %}
- {{ episode.title }}
{% endfor %}

## Historie

{% for partnership in partner.list_partnerships_history %}
- {{ partnership.starts_on }}, {{ partnership.expires_on }}
{% endfor %}

<!-- výpis minulých partnerství, disclaimer že do ledna 2023 jsem jenom prodlužoval a byl to chaos -->
