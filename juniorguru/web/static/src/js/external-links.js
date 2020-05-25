function onExternalLinkClick(url) {
  try {
    console.log('click');
    gtag('event', 'click', {
      'event_category': 'outbound',
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

function onLoad() {
  if (!gtag) return;
  const links = Array.from(document.getElementsByTagName('a'));
  links.forEach(function (link) {
    if (isExternalLink(link.href)) {
      link.addEventListener('mousedown', function (event) {
        onExternalLinkClick(link.href);
      });
    }
  });
}

document.addEventListener('DOMContentLoaded', onLoad);
