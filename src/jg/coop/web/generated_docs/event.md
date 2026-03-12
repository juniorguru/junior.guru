{% from 'macros.html' import event_video_card, lead with context %}

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
{{ 'info-circle-fill'|icon }} <span>Klub junior.guru pořádá <strong>vzdělávací akce, online na svém Discordu</strong>.
Tato akce začne <strong>{{ '{:%-d.%-m.%Y v %-H:%M}'.format(event.start_at_prg) }}</strong> a trvat by měla zhruba <strong>{{ event.duration_s|hours }}</strong>. Vždy se snažíme pořídit i záznam.
</span>
<li class="note-explainer-item">
{{ 'star-fill'|icon }} <span>Členové klubu mohou akce sledovat živě a <strong>pokládat hostům vlastní dotazy</strong>. Taky mají k dispozici <strong>všechny záznamy proběhlých akcí</strong>.</span>
</li>
<li class="note-explainer-item">
{{ 'piggy-bank-fill'|icon }} <span>Do klubu se můžeš <strong>registrovat zdarma</strong>. Nemusíš nic platit, ani nic hlídat. Každý nový člen má totiž <strong>14 dní na zkoušku</strong>. Když do dvou týdnů nezadáš kartu, automaticky ti vyprší přístup. {% if not event.is_within_trial() %}<small>Ale pozor, tahle akce je hodně v budoucnu, takže pokud si členství koupíš už dnes, nevyjdou ti dny zdarma.</small>{% endif %}</span>
</li>
<li class="note-explainer-item">
{{ 'heart-fill'|icon }} <span>Pojetí akcí je vždy <strong>vyloženě pro začátečníky</strong>. Žádná záplava odborných „termitů“, které ti nikdo nevysvětlil!</span>
<li class="note-explainer-item">
{{ 'play-circle-fill'|icon }} <span>
Pokud už máš do klubového Discordu přístup, jdi <strong>{{ '{:%-d.%-m.%Y v %-H:%M}'.format(event.start_at_prg) }}</strong> do kanálu <a href="https://discord.com/channels/769966886598737931/1075814161138860135" target="_blank" rel="noopener">#přednášky</a> a čekej, až to začne.</span>
</ul>


{#
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

  </p>
  <p>
    <a class="c2a-button pulse" href="#jak-se-pripojit">{{ 'person-plus-fill'|icon }} Připoj se</a>
  </p>
  {% endif %}
</div> -->
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

<!-- Na tuto akci se mohou živě připojit a pokládat hostům dotazy **jen členové junior.guru klubu**.

Pokud už máš do klubového Discordu přístup, jdi **{{ '{:%-d.%-m.%Y v %-H:%M}'.format(event.start_at_prg) }}** do kanálu <a href="https://discord.com/channels/769966886598737931/1075814161138860135" target="_blank" rel="noopener">#přednášky</a> a čekej, až to začne. -->

<!-- {{ club_teaser("Připoj se") }} -->
#}
