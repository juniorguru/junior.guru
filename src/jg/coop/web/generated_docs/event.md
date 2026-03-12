{% from 'macros.html' import club_teaser, event_video_card, lead, note with context %}

# {{ event.get_full_title() }}

<script type="application/ld+json">{{ event.to_json_ld() }}</script>

<ul class="article-details">
  <li class="article-details-item">{{ '{:%-d.%-m.%Y, %-H:%M}'.format(event.start_at_prg) }}</li>
  <li class="article-details-item">
    <a class="article-details-link" href="{{ ("static/" + event.poster_path)|url }}" target="_blank" rel="noopener" download>Stáhni plakát</a>
  </li>
</ul>

{% call lead() %}{{ event.description|md }}{% endcall %}
{{ event_video_card(event) }}

<h2 class="note-explainer-heading">Jak to funguje</h2>
<ul class="note-explainer">
  <li class="note-explainer-item">
    {{ 'github'|icon }}
    <span>
      Junioři musí <strong>prokázat iniciativu a základní technickou zdatnost</strong>, aby se v seznamu vůbec objevili.
      <small>Sami se musí dokázat přidat přes <a href="https://github.com/juniorguru/eggtray/">github.com/juniorguru/eggtray</a>.</small>
    </span>
  </li>
  <li class="note-explainer-item">
    {{ 'check-circle-fill'|icon }}
    <span>
      Robot každý den vyhodnocuje, které profily <strong>splňují naše standardy</strong>. Ty ostatní se zobrazí poloprůhledně.
      <small>Klidně si <a href="{{ pages|docs_url('handbook/github-profile.md')|url }}">zpětnou vazbu od robota</a> vyzkoušej.</small>
    </span>
  </li>
  <li class="note-explainer-item">
    {{ 'star-fill'|icon }}
    <span>
      Pokud junior vše splňuje a navíc <strong>se rozvíjí v našem klubu</strong>, zobrazí se žlutě.
      <small>Naše <a href="{{ pages|docs_url('club.md')|url }}">online komunita</a> dává juniorům kontakt s realitou, seniorní dohled a ověřuje jejich komunikační schopnosti.</small>
    </span>
  </li>
  <li class="note-explainer-item">
    {{ 'piggy-bank-fill'|icon }}
    <span>
      Když si někoho vybereš, <strong>opravdu nic neplatíš</strong>. Oslovuješ napřímo.
      <small>Pokud chceš projevit vděčnost, podpoř junior.guru <a href="{{ pages|docs_url('love.jinja')|url }}">dobrovolným příspěvkem nebo sponzorstvím</a>.</small>
    </span>
  </li>
</ul>

<!-- ## O akci
{% set is_past_event = event.start_at < now.replace(tzinfo=none) %}

Klub junior.guru pořádá vzdělávací akce, online na svém Discordu.
{%- if is_past_event %}
  Toto je jeda z nich. Už proběhla, ale najdeš tady o ní všechny informace
  {%- if event.has_recording %}, včetně odkazu na záznam.{% else %}.{% endif %}
{% else %}
  Toto je upoutávka na jednu z nich, která teprve proběhne. Přečti si, jak se k nám můžeš připojit!
{% endif %}
{{- ' ' -}}Pojetí akcí je vždy vyloženě pro začátečníky. Žádná záplava odborných „termitů“, které ti nikdo nevysvětlil! -->

<!--
<div class="c2a standout">
  {% if is_past_event %}
  <p class="c2a-text display">
    Akce proběhla <strong>{{ '{:%-d.%-m.%Y}'.format(event.start_at_prg) }}</strong>
    a trvala <strong>{{ event.duration_s|hours }}</strong>
  </p>
  <p>
    <a class="c2a-button" href="#zaznam">{{ 'play-circle-fill'|icon }} Pusť si záznam</a>
  </p>
  {% else %}
  <p class="c2a-text display blue">
    Akce bude <strong>{{ '{:%-d.%-m.%Y v %-H:%M}'.format(event.start_at_prg) }}</strong>,
    trvat má <strong>{{ event.duration_s|hours }}</strong>
  </p>
  <p>
    <a class="c2a-button pulse" href="#jak-se-pripojit">{{ 'person-plus-fill'|icon }} Připoj se</a>
  </p>
  {% endif %}
</div> -->

{#
Archived prototype text blocks (kept intentionally for later iteration):

<!-- ## Záznam -->

<!-- Záznamy klubových akcí **bývají dostupné jen pro členy**, ale tento jsme **zveřejnili**, ať pomáhá všem.
Budeme rádi, když video olajkuješ, nebo dokonce okomentuješ!

Členové junior.guru klubu mohou akce sledovat živě a **pokládat hostům dotazy**. Taky mají k dispozici **všechny záznamy proběhlých akcí**. -->

<!-- {% if event.club_recording_url and event.public_recording_duration_s != event.private_recording_duration_s %}{% call note() %}
  {{ 'lightbulb'|icon }} Tato akce má **dva záznamy**. Kromě veřejného sestřihu, který má {{ event.public_recording_duration_s|hours }}, existuje ještě i verze pro členy s délkou {{ event.private_recording_duration_s|hours }}. Pokud máš přístup do klubu, můžeš si <a href="{{ event.club_recording_url }}" target="_blank" rel="noopener">pustit i členskou verzi</a>.
{% endcall %}{% endif %} -->

<!-- Záznam této klubové akce **je dostupný jen pro členy**. Ti mohou záznamy sdílet se svými kamarády, takže pokud nějaké členy znáš, popros je o odkaz na video.

Nebo se můžeš **zdarma registrovat do klubu**. Nemusíš nic platit, ani nic hlídat. Každý nový člen má totiž **14 dní na zkoušku**. Když do dvou týdnů nezadáš kartu, automaticky ti vyprší přístup. -->

<!-- ## Jak se připojit -->

<!-- Klubové akce běžně bývají jen pro členy, ale tato je **veřejná**, ať pomáhá všem.
Jdi **{{ '{:%-d.%-m.%Y v %-H:%M}'.format(event.start_at_prg) }}** na <a href="{{ event.public_recording_url }}" target="_blank" rel="noopener">adresu streamu</a> a čekej, až to začne. -->

<!-- Na tuto akci se mohou živě připojit a pokládat hostům dotazy **jen členové junior.guru klubu**. Můžeš se do něj **registrovat zdarma**. Nemusíš nic platit, ani nic hlídat. Každý nový člen má totiž **14 dní na zkoušku**.

Když do dvou týdnů nezadáš kartu, automaticky ti vyprší přístup. {% if not event.is_within_trial() %}(Ale pozor, tahle akce je hodně v budoucnu, takže pokud si členství koupíš už dnes, nevyjdou ti dny zdarma.){% endif %}

Pokud už máš do klubového Discordu přístup, jdi **{{ '{:%-d.%-m.%Y v %-H:%M}'.format(event.start_at_prg) }}** do kanálu <a href="https://discord.com/channels/769966886598737931/1075814161138860135" target="_blank" rel="noopener">#přednášky</a> a čekej, až to začne. -->

<!-- {{ club_teaser("Připoj se") }} -->
#}
