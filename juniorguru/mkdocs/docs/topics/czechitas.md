---
title: Zkušenosti s Czechitas
messages_keyword: czechitas
---

<header class="intro">
  <h1 class="intro__title">Recenze na Czechitas</h1>
  <p class="intro__lead">
    Hledáš někoho, kdo má zkušenosti s Czechitas? Má smysl hlásit se na jejich kurzy? Vyplatí se datová akademie?
    <br><br>
    Jsme klub pro úplné začátečníky v programování, kde se přesně takové věci probírají. Dostaneš informace, motivaci, rady. Kromě toho ale i parťáky, podporu, kontakty a pracovní nabídky.
  </p>
</header>

<p class="mentions">
  V klubu je {{ messages_count }} zmínek o Czechitas. Poradíme ti!
</p>

<!--
<ul class="numbers">
  <li data-annotate><strong>{{ messages_count }}</strong> <small>zmínek o PyLadies</small></li>
  <li><strong>{{ members_total_count }}</strong> <small>členů v klubu</small></li>
  <li><strong>{{ jobs_count }}</strong> <small>nabídek práce</small></li>
</ul>
-->

<div class="members">
  <ul class="members__items">
    {% for member in members|sample(20) %}
      <li class="members__item">
        <img width="51" height="51" class="members__image" src="{{ fix_url('../static/' + member.avatar_path) }}" alt="Profilovka člena {{ member.id }}">
      </li>
    {% endfor %}
    <li class="members__item members__item--count">
      a&nbsp;{{ members_total_count - 20 }}&nbsp;dalších
    </li>
  </ul>
</div>

<p class="button-compartment">
  <a href="{{ fix_url('../club/') }}" class="button">
    Přidej se&nbsp;k&nbsp;nám
  </a>
</p>

{#

----------

### Co jsou Czechitas?

TODO

### Datová akademie

TODO

### Pozadí

TODO

----------

<p class="button-compartment button-compartment--row">
  <a class="button button--spaced" href="{{ fix_url('../learn/') }}">Jak začít programovat?</a>
  <!-- <a class="button button--secondary button--spaced" href="{{ fix_url('../jobs/') }}">Sežeň&nbsp;práci</a> -->
</p>

#}
