document.addEventListener('DOMContentLoaded', function () {
  if (!document.querySelectorAll) {
    console.error('document.querySelectorAll() not available, degraded experience');
    return;
  }

  Array.from(document.querySelectorAll('.checkout')).forEach(function (checkout) {
    const control = Array.from(checkout.querySelectorAll('.checkout__control'))[0];
    if (!control) { return; }

    control.addEventListener('click', function (event) {
      event.preventDefault();
      checkout.classList.add('checkout--active');
    });
  });
});