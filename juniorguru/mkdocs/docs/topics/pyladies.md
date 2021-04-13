---
title: Zkušenosti s PyLadies
messages_keyword: pyladies
---

<header class="intro">
  <h1 class="intro__title">Zjisti vše o kurzech PyLadies</h1>
  <p class="intro__lead">
    Hledáš někoho, kdo má zkušenosti s PyLadies? Jsou jejich materiály kvalitní? Má smysl hlásit se na jejich začátečnický kurz? Jak si poradit s projekty?
    <br><br>
    Jsme klub pro úplné začátečníky v programování, kde se přesně takové věci probírají. Dostaneš informace, motivaci, rady. Kromě toho ale i parťáky, podporu, kontakty a pracovní nabídky.
  </p>
</header>

<p class="mentions">
  V klubu je {{ messages_count }} zmínek o PyLadies. Poradíme ti!
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

### Co jsou PyLadies?

PyLadies (ze slov Python a ladies) jsou mezinárodní komunita, která se snaží přiblížit IT ženám a ženy k IT. K tomu využívá [programovací jazyk Python](/learn/#python), který je perfektní pro výukové účely a zároveň je po něm velká poptávka na trhu práce.

### Začátečnický kurz

Zatímco v jiných zemích PyLadies organizují spíše srazy, [PyLadies v ČR](https://pyladies.cz/) organizují především tříměsíční začátečnický kurz základů programování. Ten dříve probíhal prezenčně hned v několika městech, ale kvůli covidu-19 byl buďto převeden do online podoby, nebo pozastaven. Kurz je založen na volně přístupných a komunitně vylepšovaných materiálech ze stránek [Nauč se Python!](https://naucse.python.cz/), kde si můžeš stejnou látku procházet i jako samouk.

Absolvování kurzu je zdarma, musíš se registrovat přes formulář a projít výběrem, jelikož je pro výuku velmi omezená kapacita. Často se stane, že se přihlásí 150 lidí, přitom kapacita kurzu je např. 20. Organizátorky účastnice vybírají podle jejich sepsané motivace a dosavadních znalostí tak, aby se do kurzu dostaly ty ženy, kterým to nejvíc pomůže a mají důvod a chuť kurzem projít až do konce. Kurz samotný je založen na 2h vyučování jednou týdně večer, ale pro úspěšné dokončení je zcela nezbytné se věnovat i vypracovávání projektů v čase mezi jednotlivými hodinami.

### Pozadí

PyLadies v Česku fungují zhruba od roku 2012 a mají zcela neformální, dobrovolnickou strukturu, která funguje na principech komunity, práce ve volném čase, nadšení a Open Source. S firmami si domlouvají hlavně možnost bezplatně využívat jejich prostory k výuce, případně poskytnutí drobných výhod jako např. občerstvení. Organizátorky v jednotlivých městech operují poměrně nezávisle, ale jsou spolu v kontaktu. Příliš se nezabývají ani marketingem, ani sháněním dotací. Účetně na českém území aktivity PyLadies zaštiťuje neziskovka [Pyvec](https://pyvec.org/).

----------

<p class="button-compartment button-compartment--row">
  <a class="button button--spaced" href="{{ fix_url('../learn/') }}">Jak začít programovat?</a>
  <!-- <a class="button button--secondary button--spaced" href="{{ fix_url('../jobs/') }}">Sežeň&nbsp;práci</a> -->
</p>

#}
