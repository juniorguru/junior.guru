function toggleToc(toc, checkbox) {
  if (checkbox.checked) {
    toc.classList.add('toc--visible');
  } else {
    toc.classList.remove('toc--visible');
  }
}

document.addEventListener('DOMContentLoaded', function () {
  const toc = document.getElementById('toc');
  const checkbox = document.getElementById('toc-toggle-checkbox');

  if (toc && checkbox) {
    checkbox.addEventListener('change', function (event) {
      toggleToc(toc, checkbox);
    });
    toggleToc(toc, checkbox);

    toc.addEventListener('click', function (event) {
      let el = event.target;
      while (el) {
        if (el.classList.contains('toc__content')) {
          event.stopPropagation();
          return;
        }
        el = el.parentElement;
      }
      checkbox.checked = false;
      checkbox.dispatchEvent(new Event('change'));
    });
  }
});
