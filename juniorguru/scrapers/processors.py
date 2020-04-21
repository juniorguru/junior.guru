def absolute_url(url, loader_context):
    return loader_context['response'].urljoin(url)
