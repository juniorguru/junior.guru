function onHash() {
  if (!window.location.hash) return;

  var hash = window.location.hash.replace(/^#/, '');
  var element = document.getElementById(hash);

  while (element instanceof HTMLElement) {
    var tagName = element.tagName.toLowerCase();
    if (tagName === 'details') {
      element.setAttribute('open', '');
      return;
    }
    if (tagName === 'main') return;
    if (tagName === 'body') return;
    if (tagName === 'html') return;
    element = element.parentNode;
  }
}

window.addEventListener('hashchange', onHash);
document.addEventListener('DOMContentLoaded', onHash);
