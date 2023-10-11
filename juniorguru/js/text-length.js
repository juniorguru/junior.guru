function assignClass(element) {
  const threshold = element.dataset.dataTextLengthThreshold || 50;
  element.classList.add(element.textContent.length > threshold ? 'long' : 'short');
}

document.addEventListener('DOMContentLoaded', function () {
  Array.from(document.querySelectorAll('*[data-text-length]'))
    .forEach(assignClass);
});
