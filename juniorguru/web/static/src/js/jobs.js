function onHashChange() {
  if (!window.location.hash) return;
  if (!document.body.className.match(/\bpage-jobs\b/)) return;

  const hash = window.location.hash.replace(/^#/, '');
  const link = document.getElementById(hash).getElementsByTagName('a')[0];
  link.className = "active " + link.className;
}

window.addEventListener('hashchange', onHashChange);
document.addEventListener('DOMContentLoaded', onHashChange);

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

function onLoad() {
  if (!gtag) return;
  if (document.body.className != 'page-job') return;
  const applyButton = document.getElementById('apply');
  if (!applyButton) return;
  applyButton.addEventListener('mousedown', function (event) {
    onApply(window.location.href);
  });
}

document.addEventListener('DOMContentLoaded', onLoad);
