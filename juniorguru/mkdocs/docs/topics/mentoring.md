---
title: Komunitní mentoring na programování
topic_name: mentoring
description: Hledáš někoho, kdo má zkušenosti s programováním a dokáže ti poradit, když se na něčem při učení zasekneš? Někoho, kdo tématu rozumí a umí tě navést na správné postupy?
---
{% from 'topic.html' import intro, mentions, members_roll %}

<header class="intro">
  <h1 class="intro__title">Komunitní mentoring</h1>
  <p class="intro__lead">
    {{ page.meta.description }}
    <br><br>
    Jsme klub pro úplné začátečníky v programování, kde přesně toto najdeš. Navíc dostaneš informace, motivaci, rady, parťáky, podporu, kontakty a pracovní nabídky.
  </p>
</header>

<p class="mentions">
  V klubu máme na&nbsp;mentoring hned několik místností, kde jsme si už napsali {{ topic.topic_channels_messages_count }}&nbsp;zpráv. Poradíme&nbsp;ti!
</p>

{{ members_roll(members, members_total_count, club_elapsed_months) }}
