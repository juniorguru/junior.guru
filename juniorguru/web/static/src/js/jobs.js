function onJobLinkClick(url) {
  try {
    gtag('event', 'click', {
      'event_category': 'job',
      'event_label': url,
      'transport_type': 'beacon',
    });
  } catch (error) {
    // do nothing, sending the event to GA is just 'nice to have'
  }
}

function isExternalLink(href) {
  if (!href || !href.match(/^http/)) {
    return false;
  }

  try {
    const url = new URL(href);
    const hostname = url.hostname.replace('www.', '');
    return !!(hostname != 'localhost' && hostname != 'junior.guru');
  } catch (error) {
    return false;
  }
}

function onJobsLoad() {
  if (!gtag) return;
  if (!document.body.className.match(/\bpage-jobs\b/)) return;
  const links = Array.from(document.getElementsByTagName('a'));
  links
    .filter(function (link) {
      return link.rel == 'nofollow' && link.target == '_blank';
    })
    .forEach(function (link) {
      if (isExternalLink(link.href)) {
        link.addEventListener('mousedown', function (event) {
          onJobLinkClick(link.href);
        });
      }
    });
}

document.addEventListener('DOMContentLoaded', onJobsLoad);


function onApply(url) {
  try {
    gtag('event', 'click', {
      'event_category': 'apply',
      'event_label': url,
      'transport_type': 'beacon',
    });
  } catch (error) {
    // do nothing, sending the event to GA is just 'nice to have'
  }
}

function onJobLoad() {
  if (!gtag) return;
  if (!document.body.className.match(/\bpage-job\b/)) return;
  const applyButton = document.getElementById('apply');
  if (!applyButton) return;
  applyButton.addEventListener('mousedown', function (event) {
    onApply(window.location.href);
  });
}

document.addEventListener('DOMContentLoaded', onJobLoad);
