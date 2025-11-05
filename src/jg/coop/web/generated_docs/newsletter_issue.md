{% from 'macros.html' import lead with context %}

# {title}

{% call lead() %}
Prohrabáváš se archivem zdejšího newsletteru a koukáš na jedno ze starších vydání.
Pokud chceš, aby ti takové e-maily chodily čerstvé, [přihlaš se k odebírání](../news.jinja)!
{% endcall %}

<div class="newsletter-issue">
<p class="newsletter-issue-date">Odesláno {{ "{:%-d.%-m.%Y}".format(newsletter_issue.published_on) }}</p>
{{ newsletter_issue.content_html }}
</div>

<div class="pagination">
  <div class="pagination-control">
    <a href="{{ (page|parent_page).url|url }}" class="pagination-button">
      {{ 'arrow-left'|icon }}
      Všechna vydání
    </a>
  </div>
</div>
