{% from 'macros.html' import img, lead, club_teaser, note, video_card, link_card, figure with context %}

# {{ event.get_full_title() }}

{% set is_past_event = event.start_at < now.replace(tzinfo=none) %}

<script type="application/ld+json">{{ event.to_json_ld() }}</script>

{% call lead() %}
Klub junior.guru pořádá vzdělávací akce{% if not event.venue %}, online na svém Discordu{% endif %}.
{%- if is_past_event %}
  Toto je jeda z nich. Už proběhla, ale najdeš tady o ní všechny informace
  {%- if event.has_recording %}, včetně odkazu na záznam.{% else %}.{% endif %}
{% else %}
  Toto je upoutávka na jednu z nich, která teprve proběhne. Přečti si, jak se k nám můžeš {% if event.venue %}přidat{% else %}připojit{% endif %}!
{% endif %}
{{- ' ' -}}Pojetí akcí je vždy vyloženě pro začátečníky. Žádná záplava odborných „termitů“, které ti nikdo nevysvětlil!
{% endcall %}

<div class="c2a">
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
    {% if event.venue %}
      <a class="c2a-button pulse" href="#jak-se-pridat">{{ 'person-plus-fill'|icon }} Přidej se</a>
    {% else %}
      <a class="c2a-button pulse" href="#jak-se-pripojit">{{ 'person-plus-fill'|icon }} Připoj se</a>
    {% endif %}
  </p>
  {% endif %}
</div>

<div class="figure-container">
  {{ figure('static/' + event.plain_poster_path, 1280, 720, event.get_full_title(), class="standout-top") }}
  <a class="figure-button" href="{{ ("static/" + event.poster_path)|url }}" target="_blank" rel="noopener" download>{{ 'download'|icon }} Stáhni plakát</a>
</div>

## O čem to {% if is_past_event %} bylo{% else %}bude{% endif %}

{{ event.description|md }}

<div class="standout details">
  <div class="details-info avatar">
    <div class="details-image">
      {{ img("static/" + event.avatar_path, event.get_full_title(), 400, 400, class='details-thumbnail', lazy=False) }}
    </div>
    <div class="details-body">
      <h5 class="details-heading">{{ event.bio_name }}</h5>
      {% if event.bio_title %}
        <div class="details-text compact">{{ event.bio_title }}</div>
      {% endif %}
      <div class="details-text">
        {{ event.bio|md }}
        <ul class="icon-links">
          {% for url in event.bio_links %}
            <li>{{ url|bio_link }}</li>
          {% endfor %}
        </ul>
      </div>
    </div>
  </div>
</div>

{% if is_past_event %}

## Záznam

{% if event.public_recording_url %}

Záznamy klubových akcí **bývají dostupné jen pro členy**, ale tento jsme **zveřejnili**, ať pomáhá všem.
Budeme rádi, když video olajkuješ, nebo dokonce okomentuješ!

{{ video_card(
  event.get_full_title(),
  event.public_recording_duration_s|hours,
  event.public_recording_url,
  badge_icon='unlock-fill',
  badge_text='Veřejný záznam',
  thumbnail_url="static/" + event.plain_poster_path,
) }}

{% elif event.club_recording_url %}

Záznam této klubové akce **je dostupný jen pro členy**. Ti mohou záznamy sdílet se svými kamarády, takže pokud nějaké členy znáš, popros je o odkaz na video.

Nebo se můžeš **zdarma registrovat do klubu**. Nemusíš nic platit, ani nic hlídat. Každý nový člen má totiž **14 dní na zkoušku**. Když do dvou týdnů nezadáš kartu, automaticky ti vyprší přístup.

{{ video_card(
  event.get_full_title(),
  event.private_recording_duration_s|hours,
  event.club_recording_url,
  badge_icon='discord',
  badge_text='Pouze pro členy',
  thumbnail_url="static/" + event.plain_poster_path,
) }}

{% endif %}

Členové junior.guru klubu mohou akce sledovat živě a **pokládat hostům dotazy**. Taky mají k dispozici **záznamy všech proběhlých akcí**.

{% if event.public_recording_url and event.club_recording_url and event.public_recording_duration_s != event.private_recording_duration_s %}{% call note() %}
  {{ 'lightbulb'|icon }} Tato akce má **dva záznamy**. Kromě veřejného sestřihu, který má {{ event.public_recording_duration_s|hours }}, existuje ještě i verze pro členy s délkou {{ event.private_recording_duration_s|hours }}. Pokud máš přístup do klubu, můžeš si <a href="{{ event.club_recording_url }}" target="_blank" rel="noopener">pustit i členskou verzi</a>.
{% endcall %}{% endif %}

{{ club_teaser("Mrkni do klubu") }}

{% else %}

{% if event.venue %}
## Jak se přidat
{% else %}
## Jak se připojit
{% endif %}

{% if event.venue %}
{% if event.registration_url %}

Místo konání: **{{ event.venue }}**. Na tuto akci je potřeba se registrovat, takže než přijdeš, přihlas se přes tohle tlačtko:

<div class="c2a compact">
  <a class="c2a-button" href="{{ event.registration_url }}" target="_blank" rel="noopener">
    {{ 'person-plus-fill'|icon }}
    Registruj se
  </a>
</div>

{% else %}

Místo konání: **{{ event.venue }}**. Na tuto akci není potřeba se registrovat, takže prostě jenom přijď!

{% endif %}
{% elif event.public_recording_url %}

Klubové akce běžně bývají jen pro členy, ale tato je **veřejná**, ať pomáhá všem.
Jdi **{{ '{:%-d.%-m.%Y v %-H:%M}'.format(event.start_at_prg) }}** na <a href="{{ event.public_recording_url }}" target="_blank" rel="noopener">adresu streamu</a> a čekej, až to začne.

<div class="c2a compact">
  <a class="c2a-button brand-button youtube" href="{{ event.public_recording_url }}" target="_blank" rel="noopener">
    {{ 'youtube'|icon }}
    Připoj se
  </a>
  <p class="c2a-text">
    <small>Odebírej na YouTube <a href="https://www.youtube.com/@juniordotguru/" target="_blank" rel="noopener">@juniordotguru</a></small>
  </p>
</div>

{% else %}

Na tuto akci se mohou živě připojit a pokládat hostům dotazy **jen členové junior.guru klubu**. Můžeš se do něj **registrovat zdarma**. Nemusíš nic platit, ani nic hlídat. Každý nový člen má totiž **14 dní na zkoušku**. Když do dvou týdnů nezadáš kartu, automaticky ti vyprší přístup. {% if not event.is_within_trial() %}(Ale pozor, tahle akce je hodně v budoucnu, takže pokud si členství koupíš už dnes, nevyjdou ti dny zdarma.){% endif %}

Pokud už máš do klubového Discordu přístup, jdi **{{ '{:%-d.%-m.%Y v %-H:%M}'.format(event.start_at_prg) }}** do kanálu <a href="https://discord.com/channels/769966886598737931/1075814161138860135" target="_blank" rel="noopener">#přednášky</a> a čekej, až to začne.

{{ club_teaser("Připoj se") }}

{% endif %}

{% endif %}

## Mohlo by tě zajímat

<div class="link-cards wide">
{% set events_planned_sample = events_planned|rejectattr("id", "equalto", event.id)|sample(1) %}
{% set events_archive_sample = events_archive|rejectattr("id", "equalto", event.id)|sample(2) %}
{% set events_sample = [
  events_planned_sample.0 or events_archive_sample.0,
  events_archive_sample.1,
] %}

{% for event in events_sample %}
{{ link_card(
  event.title,
  pages|docs_url(event.page_url)|url,
  caption=event.bio_name,
  thumbnail_url="static/" + event.plain_poster_path,
) }}
{% endfor %}
</div>

<div class="pagination">
  <div class="pagination-control">
    <a href="{{ (page|parent_page).url|url }}" class="pagination-button">
      {{ 'arrow-left'|icon }}
      Všechny akce
    </a>
  </div>
</div>
