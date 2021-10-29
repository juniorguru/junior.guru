const ACTIVE_CLASS = 'active';


document.addEventListener('DOMContentLoaded', function() {
  const current = document.querySelector('.tocbar-current');
  const toc = {
    bar: document.querySelector('.tocbar'),
    current,
    currentInitialValue: current ? current.innerHTML : null,
    headings: Array.from(document.querySelectorAll('.document h2')),
    items: getItemsByIDs('.toc-subitem', '.toc-sublink'),
  };

  if (toc.bar && toc.current && toc.headings.length) {
    onScroll(updateToC, [toc]);
  }
});


function getItemsByIDs(itemSelector, linkSelector) {
  const items = Array.from(document.querySelectorAll(itemSelector));
  const ids = items
    .map(item => item.querySelector(linkSelector))
    .map(link => link ? link.href : null)
    .map(href => href ? href.split('#')[1] : null)
  return items.reduce((map, item, index) => {
    const id = ids[index];
    if (id) { map[id] = item; }
    return map;
  }, {});
}


function onScroll(fn, args) {
  let scrolled = false;

  window.addEventListener('scroll', function (event) {
    scrolled = true;
  });

  setInterval(function () {
    if (scrolled) {
      fn(...args);
      scrolled = false;
    }
  }, 250);
}


function updateToC(toc) {
  const heading = getCurrentHeading(toc.headings, getPosition(toc.bar));
  if (heading) {
    toc.current.innerHTML = heading.childNodes[0].textContent;

    Object.values(toc.items).forEach(item => item.classList.remove(ACTIVE_CLASS));
    if (toc.items[heading.id]) { toc.items[heading.id].classList.add(ACTIVE_CLASS); }
  } else {
    toc.current.innerHTML = toc.currentInitialValue;
  }
}


function getCurrentHeading(headings, position) {
  const pastHeadings = getPastElements(headings, position);
  if (pastHeadings.length <= 1) { return pastHeadings[0] || null; }
  return getLastElement(pastHeadings);
}


function getPastElements(elements, position) {
  return elements.filter(element => getPosition(element) < position);
}


function getLastElement(elements) {
  return elements.reduce((latestElement, element) => {
    return getPosition(latestElement) > getPosition(element) ? latestElement : element;
  })
}


function getPosition(element) {
  return element.getBoundingClientRect().bottom;
}
