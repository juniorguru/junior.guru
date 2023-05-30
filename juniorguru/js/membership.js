document.addEventListener('DOMContentLoaded', function () {
  const engage = document.querySelector('.content__section--hidden');
  if (engage && window.location.search.includes('state=success')) {
    engage.style.display = 'block';
  }
});
