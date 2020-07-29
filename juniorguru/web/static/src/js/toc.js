function toggleToc(toc, tocToggle) {
  if (tocToggle.checked) {
    toc.classList.add('toc--visible');
  } else {
    toc.classList.remove('toc--visible');
  }
}

document.addEventListener('DOMContentLoaded', function () {
  const toc = document.getElementById('toc');
  const tocToggle = document.getElementById('toc-toggle');

  if (toc && tocToggle) {
    tocToggle.addEventListener('change', function (event) {
      toggleToc(toc, tocToggle);
    });
    toggleToc(toc, tocToggle);

    document.addEventListener('click', function (event) {
      let el = event.target;
      while (el) {
        if (el.classList.contains('toc-toggle') || el.classList.contains('toc')) {
          event.stopPropagation();
          return;
        }
        el = el.parentElement;
      }
      tocToggle.checked = false;
      tocToggle.dispatchEvent(new Event('change'));
    });
  }
});
