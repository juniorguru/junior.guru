function onHashChange() {
  if (!window.location.hash) return;
  if (!document.body.className.match(/\bpage-jobs\b/)) return;

  const hash = window.location.hash.replace(/^#/, '');
  const link = document.getElementById(hash).getElementsByTagName('a')[0];
  link.className = "active " + link.className;
}

window.addEventListener('hashchange', onHashChange);
document.addEventListener('DOMContentLoaded', onHashChange);
