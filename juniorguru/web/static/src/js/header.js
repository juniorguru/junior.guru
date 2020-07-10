const MIN_SCROLL = 10;
let lastScrollTop = 0;

onScroll(function (event) {
  const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
  if (Math.abs(lastScrollTop - scrollTop) <= MIN_SCROLL) return;
  const header = document.getElementsByClassName('header')[0];

  if (scrollTop > lastScrollTop) { // down
    header.classList.add('header--optional');
  } else if (scrollTop <= 0) { // up to top
    header.classList.add('header--optional');
  } else { // up
    header.classList.remove('header--optional');
  }

  lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
});

document.addEventListener('DOMContentLoaded', function () {
  const header = document.getElementsByClassName('header')[0];
  header.classList.add('header--optional');
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
