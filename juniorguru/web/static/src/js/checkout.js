document.addEventListener('DOMContentLoaded', function () {
  // when browser caches the resource, onload attribute in HTML won't happen
  if (Stripe) { document.dispatchEvent(new Event('StripeLoaded')); }

  if (!document.querySelectorAll) {
    console.error('document.querySelectorAll() not available, degraded experience');
    return;
  }

  Array.from(document.querySelectorAll('.checkout--placeholder')).forEach(function (checkout) {
    const control = Array.from(checkout.querySelectorAll('.checkout__control'))[0];
    if (!control) { return; }

    control.addEventListener('click', function (event) {
      event.preventDefault();
      checkout.classList.add('checkout--active');
    });
  });

  if (window.location.hash.substr(1) == 'checkout-canceled') {
    Array.from(document.querySelectorAll('.checkout--enabled')).forEach(function (checkout) {
      checkout.classList.add('checkout--error');
    });
  }
});

Promise.all([
  new Promise(function(resolve) { document.addEventListener('DOMContentLoaded', resolve, false); }),
  new Promise(function(resolve) { document.addEventListener('StripeLoaded', resolve, false); }),
]).then(function() {
  Array.from(document.querySelectorAll('.checkout--enabled')).forEach(function (checkout) {
    if (!checkout.dataset.stripeApiKey) { throw new Error('Stripe API key not set'); }
    const checkoutUrl = window.location.href.split('#')[0];
    const stripe = Stripe(checkout.dataset.stripeApiKey);
    const control = Array.from(checkout.querySelectorAll('.checkout__control'))[0];
    if (!control) { return; }

    control.addEventListener('click', function (event) {
      event.preventDefault();
      checkout.classList.remove('checkout--error');
      if (!control.dataset.stripePrice) { throw new Error('Stripe price not set'); }
      stripe.redirectToCheckout({
        lineItems: [{price: control.dataset.stripePrice, quantity: 1}],
        mode: 'subscription',
        successUrl: checkoutUrl + '#checkout-success',
        cancelUrl: checkoutUrl + '#checkout-canceled',
        billingAddressCollection: 'required',
      }).then(function (result) {
        if (result.error) {
          checkout.classList.add('checkout--error');
          const error = Array.from(checkout.querySelectorAll('.checkout__error'))[0];
          if (!error) { return; }
          error.textContent = result.error.message;
        }
      });
    });
  });
});