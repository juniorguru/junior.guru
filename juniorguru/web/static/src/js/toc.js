let header;
let footer;

let toc;
let tocHeading;
let tocHeadingInitialValue;

let sectionHeadings = [];
let subsectionHeadings = [];

// set variables
document.addEventListener('DOMContentLoaded', function () {
  header = document.getElementsByClassName('header')[0];
  footer = document.getElementsByClassName('footer')[0];

  toc = document.getElementsByClassName('toc__content')[0];
  tocHeading = document.getElementsByClassName('header__tocbar-heading')[0];
  tocHeadingInitialValue = tocHeading ? tocHeading.innerHTML : undefined;

  sectionHeadings = findHeadings([
    'engage__heading',
    'main__section-heading',
  ]);
  subsectionHeadings = findHeadings([
    'engage__heading',
    'main__section-heading',
    'main__subsection-heading',
  ]);
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
      const sectionHeading = getCurrentHeading(sectionHeadings, position);
      if (sectionHeading) {
        tocHeading.innerHTML = sectionHeading.innerHTML;
      } else {
        tocHeading.innerHTML = tocHeadingInitialValue;
      }
    }

    const subsectionHeading = getCurrentHeading(subsectionHeadings, position);
    if (toc && subsectionHeading) {
      const id = getId(subsectionHeading);
      const link = document.querySelectorAll('.toc__item a[href="#' + id + '"]')[0];

      Array.from(document.getElementsByClassName('toc__item--active')).forEach(function (item) {
        item.classList.remove('toc__item--active');
      });
      const item = getParent(link, 'toc__item');
      if (item) { item.classList.add('toc__item--active'); }

      Array.from(document.getElementsByClassName('toc__subitem--active')).forEach(function (subitem) {
        subitem.classList.remove('toc__subitem--active');
      });
      const subitem = getParent(link, 'toc__subitem');
      if (subitem) { subitem.classList.add('toc__subitem--active'); }
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

function findHeadings(classNames) {
  return classNames.map(function (className) {
    return Array.from(document.getElementsByClassName(className));
  }).reduce(function (acc, arr) {
    return acc.concat(arr);
  }, []);
}

function getCurrentHeading(headings, position) {
  position = (position || 0) + 120; // should be same as in SCSS' $target-offset

  // headers preceding the current position
  //
  // (except subheadings inside .more-collapsed, because they can somehow
  // appear to be positioned somewhere else ¯\_(ツ)_/¯)
  const tuples = headings.map(function (heading) {
    const position = heading.getBoundingClientRect().bottom;
    return [heading, position];
  }).filter(function (tuple) {
    return (!tuple[0].classList.contains('main__subsection-heading')
      || !getParent(tuple[0], 'more--collapsed'));
  }).filter(function (tuple) {
    return tuple[1] < position;
  });
  // console.log(tuples.map(function (t) {
  //   return t[0].innerHTML + ' (' + parseInt(t[1]) + ')';
  // }));
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

function getParent(el, className) {
  while (el) {
    if (el.classList.contains(className)) {
      return el;
    }
    el = el.parentElement;
  }
}
