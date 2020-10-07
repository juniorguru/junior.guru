import { annotate } from 'rough-notation';


document.addEventListener('DOMContentLoaded', function () {
  Array.from(document.querySelectorAll('*[data-annotate]')).forEach(function (element) {
    const annotation = annotate(element, {
      type: 'circle',
      color: '#1755d1',
      padding: 20,
    });
    annotation.show();
  });
});
