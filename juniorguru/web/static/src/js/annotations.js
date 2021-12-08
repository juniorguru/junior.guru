import { annotate } from 'rough-notation';


document.addEventListener('DOMContentLoaded', function () {
  Array.from(document.querySelectorAll('.masthead .lead strong'))
    .forEach(function (element) {
      const annotation = annotate(element, {
        type: 'underline',
        color: '#1755d1',
        multiline: true,
        animationDuration: 1600,
      });
      annotation.show();
    })
});


const observer = IntersectionObserver
  ? new IntersectionObserver(handleIntersection, { threshold: [1] })
  : null;
let annotations;


document.addEventListener('DOMContentLoaded', function () {
  annotations = Array.from(document.querySelectorAll('*[data-annotate-circle]'))
    .map(function (element, i) {
      const id = i.toString();
      const annotation = annotate(element, {
        type: 'circle',
        color: '#1755d1',
        padding: 20,
        animationDuration: 1600,
      });
      if (observer) {
        element.dataset.annotateId = id;
        observer.observe(element);
      } else {
        annotation.show();
      }
      return { id: id, annotation: annotation };
    });
});


function handleIntersection(entries, observer) {
  entries.filter(function (entry) {
    return entry.isIntersecting;
  }).forEach(function (entry) {
    const element = entry.target;
    const annotation = annotations.filter(function (item) {
      return item.id === element.dataset.annotateId;
    })[0].annotation;
    if (annotation) {
      annotation.show();
    } else {
      console.error("Couldn't find annotation");
    }
  });
}
