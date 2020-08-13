/*
document.addEventListener('DOMContentLoaded', function () {
  const body = document.body;
  const header = document.getElementsByClassName('header')[0];
  const toc = document.getElementById('toc');
  const checkbox = document.getElementById('toc-toggle-checkbox');

  if (toc && checkbox) {
    checkbox.addEventListener('change', function (event) {
      if (checkbox.checked) {
        toc.classList.add('toc--visible');
      } else {
        toc.classList.remove('toc--visible');
        header.classList.add('header--collapsed');
      }
    });

    if (checkbox.checked) {
      toc.classList.add('toc--visible');
    }

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
*/
