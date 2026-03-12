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

{% set is_past_event = event.is_past(now=now) %}

<h2 class="note-explainer-heading">Jak to funguje</h2>
<ul class="note-explainer">
  <li class="note-explainer-item">
    {{ 'info-circle-fill'|icon }}
    <span>
      Klub junior.guru pořádá <strong>vzdělávací akce, online na svém Discordu</strong>.
      {% if is_past_event %}
        Tato akce proběhla <strong>{{ '{:%-d.%-m.%Y}'.format(event.start_at_prg) }}</strong> a trvala <strong>{{ event.duration_s|hours }}</strong>.
      {% else %}
        Tato akce začne <strong>{{ '{:%-d.%-m.%Y v %-H:%M}'.format(event.start_at_prg) }}</strong> a trvat by měla zhruba <strong>{{ event.duration_s|hours }}</strong>. Vždy se snažíme pořídit i záznam.
      {% endif %}
    </span>
  </li>
  {% if event.public_recording_url %}
  <li class="note-explainer-item">
    {{ 'play-circle-fill'|icon }}
    <span>
      {% if is_past_event %}
        Záznamy klubových akcí <strong>bývají dostupné jen pro členy</strong>, ale tento jsme <strong>zveřejnili</strong>, ať pomáhá všem.
        <small>Budeme rádi, když video olajkuješ, nebo dokonce okomentuješ!</small>
      {% else %}
        Klubové akce běžně bývají jen pro členy, ale tato je <strong>veřejná</strong>, ať pomáhá všem.
        Jdi <strong>{{ '{:%-d.%-m.%Y v %-H:%M}'.format(event.start_at_prg) }}</strong> na <a href="{{ event.public_recording_url }}" target="_blank" rel="noopener">adresu streamu</a> a čekej, až to začne.
      {% endif %}
    </span>
  </li>
  {% elif is_past_event and not event.has_recording %}
  <li class="note-explainer-item">
    {{ 'camera-video-off-fill'|icon }}
    <span>
      I když jsme se snažili, <strong>nepodařilo se nám nahrát tuto akci</strong> a nemáme záznam. <small>Shit happens. I proto je lepší připojovat se na akce živě a nespoléhat se na záznamy.</small>
    </span>
  </li>
  {% endif %}
  <li class="note-explainer-item">
    {{ 'star-fill'|icon }}
    <span>
      Členové klubu mohou akce sledovat živě a <strong>pokládat hostům vlastní dotazy</strong>. Taky mají k dispozici <strong>všechny záznamy proběhlých akcí</strong>.
    </span>
  </li>
  <li class="note-explainer-item">
    {{ 'piggy-bank-fill'|icon }}
    <span>
      Do klubu se můžeš <strong>registrovat zdarma</strong>. Nemusíš nic platit, ani nic hlídat. Každý nový člen má totiž <strong>14 dní na zkoušku</strong>. Když do dvou týdnů nezadáš kartu, automaticky ti vyprší přístup.
      {% if not event.is_within_trial() %}
      <small>Ale pozor, tahle akce je hodně v budoucnu, takže pokud si členství koupíš už dnes, nevyjdou ti dny zdarma.</small>
      {% endif %}
    </span>
  </li>
  {% if not event.public_recording_url and not (is_past_event and not event.has_recording) %}
  <li class="note-explainer-item">
    {{ 'play-circle-fill'|icon }}
    <span>
      Pokud už máš přístup do klubového Discordu,
      {% if event.club_recording_url %}
        otevři si <a href="{{ event.club_recording_url }}" target="_blank" rel="noopener">odkaz na záznam</a> a <strong>sleduj</strong>!
      {% else %}
        jdi <strong>{{ '{:%-d.%-m.%Y v %-H:%M}'.format(event.start_at_prg) }}</strong> do kanálu <a href="https://discord.com/channels/769966886598737931/1075814161138860135" target="_blank" rel="noopener">#přednášky</a> a čekej, až to začne.
      {% endif %}
    </span>
  </li>
  {% endif %}
  <li class="note-explainer-item">
    {{ 'heart-fill'|icon }}
    <span>
      Pojetí akcí je vždy <strong>vyloženě pro začátečníky</strong>. Žádná záplava odborných „termitů“, které ti nikdo nevysvětlil!
    </span>
  </li>
</ul>
