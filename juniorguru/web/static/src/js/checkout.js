document.addEventListener('DOMContentLoaded', function () {
  if (!document.querySelectorAll) {
    console.error('document.querySelectorAll() not available, degraded experience');
    return;
  }
  
  const checkout = Array.from(document.querySelectorAll('.checkout'))[0];
  const control = Array.from(document.querySelectorAll('.checkout__control'))[0];
  
  if (!checkout || !control) {
    return;
  }

  control.addEventListener('click', function (event) {
    event.preventDefault();
    checkout.classList.add('checkout--active'); 
  });
});