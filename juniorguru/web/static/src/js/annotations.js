import { annotate } from 'rough-notation';


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
  annotations = annotations.concat(Array.from(document.querySelectorAll('*[data-annotate]'))
    .map(function (element, i) {
      const id = i.toString();
      const annotation = annotate(element, {
        type: 'underline',
        color: '#1755d1',
        animationDuration: 1600,
      });
      if (observer) {
        element.dataset.annotateId = id;
        observer.observe(element);
      } else {
        annotation.show();
      }
      return { id: id, annotation: annotation };
    }));
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
