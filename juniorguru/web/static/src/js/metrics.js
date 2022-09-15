function setupMetricsUtm(link) {
  const url = new URL(link.href);
  try {
    if (!url.searchParams.has('utm_source')) {
      url.searchParams.set('utm_source', 'juniorguru');
    }
    if (!url.searchParams.has('utm_medium')) {
      const medium = link.dataset.metricsUtmMedium || 'content';
      url.searchParams.set('utm_medium', medium);
    }
    if (!url.searchParams.has('utm_campaign')) {
      const campaign = link.dataset.metricsUtmCampaign || 'juniorguru';
      url.searchParams.set('utm_campaign', campaign);
    }
    link.href = '' + url;
  } catch (error) {
    if (console.error) {
      console.error("Couldn't modify link", link.href, 'to contain UTM params', error);
    }
  }
}

document.addEventListener('DOMContentLoaded', function () {
  Array.from(document.querySelectorAll('*[data-metrics-utm]'))
    .forEach(setupMetricsUtm);
});
