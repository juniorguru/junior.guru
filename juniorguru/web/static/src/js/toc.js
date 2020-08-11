function toggleToc(header, toc, checkbox) {
  if (checkbox.checked) {
    toc.classList.add('toc--visible');
    header.classList.add('header--always-collapsed');
  } else {
    toc.classList.remove('toc--visible');
    header.classList.add('header--collapsed');
    header.classList.remove('header--always-collapsed');
  }
}

document.addEventListener('DOMContentLoaded', function () {
  const header = document.getElementsByClassName('header')[0];
  const toc = document.getElementById('toc');
  const checkbox = document.getElementById('toc-toggle-checkbox');

  if (toc && checkbox) {
    checkbox.addEventListener('change', function (event) {
      toggleToc(header, toc, checkbox);
    });
    toggleToc(header, toc, checkbox);

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
