document.addEventListener('DOMContentLoaded', function() {
  const currentHeading = document.querySelector('.tocbar-current');
  const toc = {
    bar: document.querySelector('.tocbar'),
    currentHeading,
    currentHeadingInitialValue: currentHeading ? currentHeading.innerHTML : null,
    headings: Array.from(document.querySelectorAll('.document h2')),
  };

  if (toc.bar && toc.currentHeading && toc.headings.length) {
    onScroll(updateToC, [toc]);
  }
});


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
    toc.currentHeading.innerHTML = heading.childNodes[0].textContent;
  } else {
    toc.currentHeading.innerHTML = toc.currentHeadingInitialValue;
  }
}


function getCurrentHeading(headings, position) {
  const pastHeadings = getPastElements(headings, position);
  if (pastHeadings.length == 1) { return pastHeadings[0]; }
  if (pastHeadings.length > 1) { return getLastElement(pastHeadings); }
  return null;
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
