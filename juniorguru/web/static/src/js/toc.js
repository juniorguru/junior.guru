function toggleToc(toc, checkbox) {
  if (checkbox.checked) {
    toc.classList.add('toc--visible');
  } else {
    toc.classList.remove('toc--visible');
  }
}

document.addEventListener('DOMContentLoaded', function () {
  const toc = document.getElementById('toc');
  const toggle = document.getElementsByClassName('toc-toggle')[0];
  const checkbox = document.getElementById('toc-toggle-checkbox');

  if (toc && toggle && checkbox) {
    checkbox.addEventListener('change', function (event) {
      if (checkbox.checked) {
        toggle.classList.remove('toc-toggle--unused');
      }
      toggleToc(toc, checkbox);
    });

    if (!checkbox.checked) {
      toggle.classList.add('toc-toggle--unused');
    }
    toggleToc(toc, checkbox);

    document.addEventListener('click', function (event) {
      let el = event.target;
      while (el) {
        if (el.classList.contains('toc-toggle') || el.classList.contains('toc')) {
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
