{% from 'macros.html' import note with context %}

# {{ partner.name }}

Stránka popisující partnerství junior.guru s firmou {{ partner.name }}.

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }} Tuto stránku Honza právě připravuje. Brzy tady něco bude.
{% endcall %}
