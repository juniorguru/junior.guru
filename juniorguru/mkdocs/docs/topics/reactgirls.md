---
title: Zkušenosti s ReactGirls
messages_keyword: reactgirls
---

<header class="intro">
  <h1 class="intro__title">Recenze na ReactGirls</h1>
  <p class="intro__lead">
    Hledáš někoho, kdo má zkušenosti s ReactGirls? Má smysl účastnit se jejich akademie? Vyplatí se jimi nabízený mentoring?
    <br><br>
    Jsme klub pro úplné začátečníky v programování, kde se přesně takové věci probírají. Dostaneš informace, motivaci, rady. Kromě toho ale i parťáky, podporu, kontakty a pracovní nabídky.
  </p>
</header>

<p class="mentions">
  V klubu je {{ messages_count }} zmínek o ReactGirls. Poradíme ti!
</p>

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
