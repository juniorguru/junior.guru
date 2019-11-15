import 'details-element-polyfill';

function onDocumentLoad() {
  const detailsList = Array.from(document.getElementsByTagName('details'));
  detailsList.forEach(function (details) {
    details.addEventListener('toggle', function () {
      if (details.open) details.scrollIntoView(true);
    });
  });
}

document.addEventListener('DOMContentLoaded', onDocumentLoad);
