function onHashChange() {
  if (!window.location.hash) return;

  const hash = window.location.hash.replace(/^#/, '');
  const element = document.getElementById(hash);

  while (element instanceof HTMLElement) {
    const tagName = element.tagName.toLowerCase();
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

window.addEventListener('hashchange', onHashChange);
document.addEventListener('DOMContentLoaded', onHashChange);
