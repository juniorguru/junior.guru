import onScroll from './onScroll';

let header;
let footer;

let toc;
let tocHeading;
let tocHeadingInitialValue;

let sectionHeadings = [];
let subsectionHeadings = [];

let targetOffset;

// set variables
document.addEventListener('DOMContentLoaded', function () {
  if(!document.getElementsByClassName('body__container').length) {
    return;  // turn off on new pages
  }

  header = document.getElementsByClassName('header')[0];
  footer = document.getElementsByClassName('footer')[0];

  toc = document.getElementsByClassName('toc__content')[0];
  tocHeading = document.getElementsByClassName('header__tocbar-heading')[0];
  tocHeadingInitialValue = tocHeading ? tocHeading.innerHTML : undefined;

  sectionHeadings = findHeadings([
    'engage__heading',
    'content__section-heading',
  ]);
  subsectionHeadings = findHeadings([
    'engage__heading',
    'content__section-heading',
    'content__subsection-heading',
  ]);

  const targetOffsetElement = document.querySelector([
    // this selector be in sync with main.scss
    '.content__target',
    '.content__section[id]',
    '.content__section-heading[id]',
    '.content__subsection-heading[id]',
  ].join(', '));
  if (targetOffsetElement) {
    const targetOffsetElementStyle = getComputedStyle(targetOffsetElement, '::before');
    targetOffset = parseInt(targetOffsetElementStyle.getPropertyValue('height'), 10);
  } else {
    targetOffset = 0;
  }

  updateToC();

  // add permalinks
  if (toc) {
    const permalinkHeadings = document.querySelectorAll('.content__section-heading, .content__subsection-heading');
    Array.from(permalinkHeadings).forEach(addPermalink);
  }
});

onScroll(updateToC);

function updateToC() {
  if(!document.getElementsByClassName('body__container').length) {
    return;  // turn off on new pages
  }

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
    const position = header.getBoundingClientRect().top + targetOffset;

    if (tocHeading) {
      const sectionHeading = getCurrentHeading(sectionHeadings, position);
      if (sectionHeading) {
        tocHeading.innerHTML = sectionHeading.innerHTML;
      } else {
        tocHeading.innerHTML = tocHeadingInitialValue;
      }
    }

    Array.from(document.getElementsByClassName('toc__item--active')).forEach(function (item) {
      item.classList.remove('toc__item--active');
    });
    const subsectionHeading = getCurrentHeading(subsectionHeadings, position);
    if (toc && subsectionHeading) {
      const id = getId(subsectionHeading);
      const link = document.querySelectorAll('.toc__item a[href="#' + id + '"]')[0];

      const item = getParent(link, 'toc__item');
      if (item) { item.classList.add('toc__item--active'); }

      Array.from(document.getElementsByClassName('toc__subitem--active')).forEach(function (subitem) {
        subitem.classList.remove('toc__subitem--active');
      });
      const subitem = getParent(link, 'toc__subitem');
      if (subitem) { subitem.classList.add('toc__subitem--active'); }
    }
  }
}

function addPermalink(heading) {
  const a = document.createElement('a');
  a.classList.add('toc-permalink');
  a.textContent = 'odkaz sem';
  a.href = '#' + getId(heading);
  heading.appendChild(a);
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
    return (!tuple[0].classList.contains('content__subsection-heading')
      || !getParent(tuple[0], 'more--collapsed'));
  }).filter(function (tuple) {
    return tuple[1] < position;
  });

  // evaluate results
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
