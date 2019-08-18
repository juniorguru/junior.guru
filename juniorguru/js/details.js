document.addEventListener('DOMContentLoaded', function () {
  var elements = Array.from(document.getElementsByTagName('details'));
  elements.forEach(function (element) {
    element.addEventListener('toggle', function () {
      if (element.open) element.scrollIntoView(true);
    });
  });
});
