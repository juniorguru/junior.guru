document.addEventListener('DOMContentLoaded', function () {
  if (!gtag && console.log) {
    console.error('GA not available, junior.guru metrics turned off');
  }
  if (!document.querySelectorAll) {
    console.error('document.querySelectorAll() not available, junior.guru metrics turned off');
    return;
  }

  Array.from(document.querySelectorAll('*[data-metrics]')).forEach(function (link) {
    const url = link.dataset.metricsPageUrl ? window.location.href : link.href;
    const name = link.dataset.metricsName;
    link.addEventListener('mousedown', function (event) {
      try {
        gtag('event', 'click', {
          'event_category': name,
          'event_label': url,
          'transport_type': 'beacon',
        });
      } catch (error) {
        if (console.error) {
          console.error("Couldn't send event", name, 'with URL', url);
        }
      }
    });
  });

  Array.from(document.querySelectorAll('*[data-metrics-utm]')).forEach(function (link) {
    const url = new URL(link.href);
    try {
      if (!url.searchParams.has('utm_source')) {
        url.searchParams.set('utm_source', 'juniorguru');
      }
      if (!url.searchParams.has('utm_medium')) {
        const medium = link.dataset.metricsUtmMedium || 'job_board';
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
  });
});
