---
title: Kde a jak hledat pomoc během programování? Jak se ptát? Jak debugovat?
thumbnail_title: Řešení problémů během programování
description: Při programování tě i drobný zádrhel může zaseknout na týdny a úplně ti zkazit radost z učení. Kde můžeš své problémy konzultovat a jak se ptát tak, aby se ti dostalo odpovědi?
template: main_handbook.html
---

{% from 'macros.html' import lead, link_card, note with context %}


# Kde najdeš pomoc

{% call lead() %}
  Je velmi těžké se učit zcela bez cizí pomoci. I drobný zádrhel tě může zaseknout na týdny a úplně ti zkazit radost z učení. Neboj se ptát online, radit se s lidmi na [akcích](practice.md#najdi-inspiraci-poznej-lidi), nebo si najít [mentora](practice.md#najdi-si-mentora).
{% endcall %}

## Kde a jak se ptát

Neboj se ptát, ale zároveň se nauč formulovat dotazy správně. **Žádná otázka není hloupá, může však být hloupě položená.** Než se někde začneš ptát, přečti si [nejslavnější návod na internetu o psaní dotazů](https://www.root.cz/texty/jak-se-spravne-ptat/), nebo alespoň [tento krátký návod od Stack Overflow](https://stackoverflow.com/help/how-to-ask).

<div class="link-cards">
  {{ link_card(
    'Klub junior.guru',
    pages|docs_url('club.md')|url,
    'Ptej se v klubu pro začátečníky, kde najdeš nejen pomoc, ale i motivaci, kamarády, práci.',
    badge_icon='discord',
    badge_text='Discord',
  ) }}

  {{ link_card(
    'Stack Overflow',
    'https://stackoverflow.com',
    'Ptej se na celosvětově největším webu s otázkami a odpovědmi ohledně programování.'
  ) }}

  {{ link_card(
    'Pyonýři',
    'https://www.facebook.com/groups/pyonieri/',
    'Ptej na se české a slovenské Python komunity na Facebooku.',
    badge_icon='facebook',
    badge_text='Facebook',
  ) }}

  {{ link_card(
    'Programátoři začátečníci',
    'https://www.facebook.com/groups/144621756262987/',
    'Ptej se ve Facebookové skupině pro začátečníky v programování.',
    badge_icon='facebook',
    badge_text='Facebook',
  ) }}

  {{ link_card(
    'Python CZ/SK',
    'https://discord.gg/yUbgArVAyF',
    'Ptej na Discordu české a slovenské Python komunity.',
    badge_icon='discord',
    badge_text='Discord',
  ) }}

  {{ link_card(
    'r/learnpython',
    'https://www.reddit.com/r/learnpython/',
    'Pokládej dotazy komunitě pro začátečníky s Pythonem.',
    badge_icon='reddit',
    badge_text='Reddit',
  ) }}

  {{ link_card(
    'r/learnprogramming',
    'https://www.reddit.com/r/learnprogramming/',
    'Pokládej dotazy komunitě pro začátečníky v programování.',
    badge_icon='reddit',
    badge_text='Reddit',
  ) }}
</div>

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }} Tuto stránku Honza právě přepisuje. Brzy tady bude jiný text, lepší, voňavější, nápomocnější.
{% endcall %}
