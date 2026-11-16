{% from 'macros.html' import breadcrumbs, lead with context %}

{{ breadcrumbs(
  parent_title=(page|parent_page).title,
  parent_href=(page|parent_page).url|url,
  parent_url=(page|parent_page).canonical_url,
  title=newsletter_issue.subject,
  url=page.canonical_url,
) }}

# {{ newsletter_issue.subject }}

{% call lead() %}
Prohrabáváš se archivem zdejšího newsletteru a koukáš na jedno ze starších vydání.
Pokud chceš, aby ti takové e-maily chodily za čerstva, [přihlaš se k odebírání](../news.jinja)!
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
