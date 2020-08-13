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
