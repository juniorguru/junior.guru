const MIN_SCROLL = 10;

let lastScrollTop = 0;
let headings = [];

document.addEventListener('DOMContentLoaded', function () {
  headings = Array.from(document.querySelectorAll('h1, h2'));
});

onScroll(function () {
  const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
  if (Math.abs(lastScrollTop - scrollTop) <= MIN_SCROLL) return;
  const header = document.getElementsByClassName('header')[0];

  if (scrollTop > lastScrollTop) { // down
    header.classList.add('header--optional');
  } else { // up
    header.classList.remove('header--optional');
  }
  lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;

  const currentHeading = getCurrentHeading(header.getBoundingClientRect().bottom);
  document.getElementById('toc-heading').innerHTML = currentHeading.innerHTML;
});

function getCurrentHeading(topBound) {
  topBound = topBound || 0;

  const tuples = headings.map(function (heading) {
    const position = heading.getBoundingClientRect().bottom;
    return [heading, position];
  })
  const firstTuple = tuples[0]; // first heading

  return tuples.filter(function (tuple) {
    return tuple[1] < topBound;
  }).reduce(function (result, tuple) {
    return result[1] > tuple[1] ? result : tuple;
  }, firstTuple)[0];
}

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
