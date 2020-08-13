// document.addEventListener('DOMContentLoaded', function () {

// });

onScroll(function () {
  const toc = document.getElementsByClassName('toc__content')[0];
  const footer = document.getElementsByClassName('footer')[0];
  if (!footer || !toc) { return; }

  console.log(toc.getBoundingClientRect().bottom, footer.getBoundingClientRect().top);
  if (toc.getBoundingClientRect().bottom > footer.getBoundingClientRect().top) {
    toc.classList.add('toc__content--irrelevant');
  } else {
    toc.classList.remove('toc__content--irrelevant');
  }
});

function onScroll(fn) {
  let scrolled = false;

  window.addEventListener('scroll', function (event) {
    scrolled = true;
  });

  setInterval(function () {
    if (scrolled) {
      fn();
      scrolled = false;
    }
  }, 250);
}

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
