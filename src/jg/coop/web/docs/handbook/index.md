---
title: Cesta juniora
emoji: 🗺️
description: Obsáhlá příručka pro všechny, kdo se chtějí naučit programovat a najít si práci v oboru.
template: main_handbook.html
---

{% from 'macros.html' import illustration, lead, img, note with context %}

# Cesta juniora

{% call lead() %}
  Uvažuješ o programování?
  Přemýšlíš nad kariérní změnou do IT, ale nevíš jak na to?
  Láká tě zjistit, jak automatizovat část své práce?
  Studuješ informatiku a zajímá tě, co dál?
  V téhle příručce se postupně hromadí veškerá moudrost, která na toto téma existuje.
{% endcall %}

{{ illustration('static/illustrations/index.webp') }}

Na základě reálných zkušeností mnohých začátečníků jsme v [klubu](../club.md) sestavili **osvědčenou cestu juniora**.
Možná existují i jiné cesty, ale tato **úspěšně zafungovala pro spoustu různých lidí**, a proto ji lze obecně doporučit.
Ne všechna témata se zatím povedlo pokrýt kapitolami v příručce, ale na klubovém Discordu se všemi pomáháme a diskutujeme je.

Ujasni si, **co už umíš a co je tvým cílem.** Jednak ti to pomůže uvědomit si, co tě ještě čeká a co nesmíš vynechat, jednak zjistíš, které části příručky pro tebe budou nejpřínosnější.

{% call note() %}
  {{ 'lightbulb'|icon }} Příručka je živá stránka a kdykoliv tady může přibýt něco nového, takže je dobré se sem vracet. O změnách se můžeš dovědět prostřednictvím [klubu](../club.md) nebo [newsletteru](../news.jinja).
{% endcall %}

Celá cesta má zhruba {{ stages|length }} fází a připomíná Člověče, nezlob se.
Namalované je to hezky jedno za druhým, ale realita je zamotanější.
Nemálo lidí se několikrát vrací do domečku.
Počítej s tím, že se někde zasekneš, nebo že se ti zamíchá pořadí.
U každé fáze je v popisku naznačeno, s jakými problémy ti junior.guru může pomoci.

<div class="stage-cards">
{% for stage_group in stages|slice(3) %}
  {% for stage in stage_group %}
  <div class="stage-card">
    <div class="stage-card-row">
      <div class="stage-card-media">
        <div class="stage-card-icon">{{ stage.icon|icon }}</div>
      </div>
      <div class="stage-card-body">
        <h4 class="stage-card-title">{{ stage.title }}</h4>
        <p class="stage-card-description">
          {{ stage.description }}
        </p>
        <p class="stage-card-pages">
          {% for p in stage.list_pages -%}
            <a href="{{ pages|docs_url(p.src_uri)|url }}">{{ p.nav_name }}</a>
          {%- endfor %}
        </p>
        {% if stage.list_todo_pages|length %}
        <p class="stage-card-todo-pages">
          Plánované kapitoly:
          {% for p in stage.list_todo_pages -%}
            {{ p.title }}
            {%- if not loop.last %}, {% endif -%}
          {%- endfor %}
        </p>
        {% endif %}
      </div>
    </div>
  </div>
  {% endfor %}
  <div class="stage-illustration">
    {{ img('static/chick' + loop.index|string + '.svg', 'Kuře', 50, 50, lazy=False) }}
  </div>
{% endfor %}
</div>
