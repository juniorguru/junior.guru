document.addEventListener('DOMContentLoaded', function () {
  // if the subnav scrolls horizontally, set it to the middle or to make
  // the active tab visible so it's clear on small screens that users can
  // scroll it and no tabs get hidden
  const subnav = Array.from(document.getElementsByClassName('header__subnav'))[0];
  const activeTab = Array.from(document.getElementsByClassName('header__subnav-tab-control--active'))[0];

  if (subnav && activeTab && subnav.scrollWidth > window.innerWidth) {
    subnav.scrollLeft = Math.max(
      (subnav.scrollWidth - window.innerWidth) / 2,
      activeTab.getBoundingClientRect().left - 10
    );
  }
});

/*
const MIN_SCROLL = 10;

let headings = [];
let tocHeading;

document.addEventListener('DOMContentLoaded', function () {
  // set variables
  tocHeading = document.getElementById('toc-heading');
  headings = [
    'intro__title',
    'engage__heading',
    'main__section-heading',
  ].map(function (className) {
    return Array.from(document.getElementsByClassName(className));
  }).reduce(function (acc, arr) {
    return acc.concat(arr);
  }, []);
});

onScroll(function () {
  const header = document.getElementsByClassName('header--collapsible')[0];
  if (!header) { return; }
  const position = header.getBoundingClientRect().bottom;

  const intro = document.getElementsByClassName('intro')[0];
  if (intro) {
    if (position > intro.getBoundingClientRect().bottom) {
      header.classList.add('header--collapsed');
    } else {
      header.classList.remove('header--collapsed');
    }
  }

  if (tocHeading) {
    const currentHeading = getCurrentHeading(position);
    tocHeading.innerHTML = currentHeading.innerHTML;

    const id = getId(currentHeading);
    const tocItems = Array.from(document.getElementsByClassName('toc__item'));
    tocItems.forEach(function (tocItem) {
      tocItem.classList.remove('toc__item--active');
      const links = tocItem.getElementsByTagName('a');
      if (links.length && links[0].href.match('#' + id)) {
        tocItem.classList.add('toc__item--active');
      }
    });
  }
});

function getCurrentHeading(position) {
  position = (position || 0) + 100;

  const tuples = headings.map(function (heading) {
    const position = heading.getBoundingClientRect().bottom;
    return [heading, position];
  })
  const firstTuple = tuples[0]; // first heading

  return tuples.filter(function (tuple) {
    return tuple[1] < position;
  }).reduce(function (result, tuple) {
    return result[1] > tuple[1] ? result : tuple;
  }, firstTuple)[0];
}

function getId(el) {
  while (el) {
    if (el.id) {
      return el.id;
    }
    el = el.parentElement;
  }
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
*/
