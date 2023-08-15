{% from 'macros.html' import lead with context %}

<nav aria-label="breadcrumb">
  <ol class="breadcrumb">
    <li class="breadcrumb-item">
      <a href="{{ parent_page.url|url }}">
        {{ parent_page.title }}
      </a>
    </li>
    <li class="breadcrumb-item active" aria-current="page">
      {{ event.title }}
    </li>
  </ol>
</nav>

# {{ event.title }}

{% call lead() %}
  <!-- TODO Tady je aspoň základní info, které ti pomůže s rozhodováním. -->
{% endcall %}
