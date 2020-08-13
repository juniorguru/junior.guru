let header;
let footer;

let toc;
let tocHeading;
let tocHeadingInitialValue;

let headings = [];

// set variables
document.addEventListener('DOMContentLoaded', function () {
  header = document.getElementsByClassName('header')[0];
  footer = document.getElementsByClassName('footer')[0];

  toc = document.getElementsByClassName('toc__content')[0];
  tocHeading = document.getElementsByClassName('header__tocbar-heading')[0];
  tocHeadingInitialValue = tocHeading ? tocHeading.innerHTML : undefined;

  headings = [
    'engage__heading',
    'main__section-heading',
  ].map(function (className) {
    return Array.from(document.getElementsByClassName(className));
  }).reduce(function (acc, arr) {
    return acc.concat(arr);
  }, []);
});

onScroll(function () {
  // hiding of the ToC if scrolling to the bottom
  if (footer && toc) {
    if (toc.getBoundingClientRect().bottom > footer.getBoundingClientRect().top) {
      toc.classList.add('toc__content--irrelevant');
    } else {
      toc.classList.remove('toc__content--irrelevant');
    }
  }

  // updating current heading
  if (header) {
    const position = header.getBoundingClientRect().bottom;
    if (tocHeading) {
      const currentHeading = getCurrentHeading(position);
      tocHeading.innerHTML = currentHeading ? currentHeading.innerHTML : tocHeadingInitialValue;

      // const id = getId(currentHeading);
      // const tocItems = Array.from(document.getElementsByClassName('toc__item'));
      // tocItems.forEach(function (tocItem) {
      //   tocItem.classList.remove('toc__item--active');
      //   const links = tocItem.getElementsByTagName('a');
      //   if (links.length && links[0].href.match('#' + id)) {
      //     tocItem.classList.add('toc__item--active');
      //   }
      // });
    }
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

function getCurrentHeading(position) {
  position = (position || 0) + 100;

  // headers preceding the current position
  const tuples = headings.map(function (heading) {
    const position = heading.getBoundingClientRect().bottom;
    return [heading, position];
  }).filter(function (tuple) {
    return tuple[1] < position;
  })
  if (tuples.length < 1) { return null; }
  if (tuples.length == 1) { return tuples[0][0]; }

  // header with the most bottom position
  return tuples.reduce(function (result, tuple) {
    return result[1] > tuple[1] ? result : tuple;
  })[0];
}

function getId(el) {
  while (el) {
    if (el.id) {
      return el.id;
    }
    el = el.parentElement;
  }
}
