---
title: Pro přednášející
description: Máš přednášet v klubu junior.guru? Tady najdeš všechno co potřebuješ
template: main.html
---

{% from 'macros.html' import note with context %}

# Pro přednášející

<div class="mirror">
  <noscript>
    {%- call note(standout=True) -%}
      {{ 'exclamation-circle'|icon }} Kameru se nedaří spustit. Buď nemáš kameru povolenou pro tento prohlížeč, nebo to nepodporuje, nebo se něco pokazilo. Zkontroluj prosím nastavení, nebo zkus jiný prohlížeč.
    {%- endcall -%}
  </noscript>
  <div class="standout text-center">
    <button type="button" class="mirror-run">Spustit zrcadlo</button>
    <button type="button" class="mirror-expand">Roztáhnout zrcadlo</button>
  </div>
</div>
