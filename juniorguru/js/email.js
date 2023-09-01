function setupForm() {
  switch (window.location.hash) {
    case '#email-subscribed':
      document.querySelector('#email-form').setAttribute('hidden', '');
      document.querySelector('#email-subscribed').removeAttribute('hidden');
      document.querySelector('#email-confirmed').setAttribute('hidden', '');
      break;
    case '#email-confirmed':
      document.querySelector('#email-form').setAttribute('hidden', '');
      document.querySelector('#email-subscribed').setAttribute('hidden', '');
      document.querySelector('#email-confirmed').removeAttribute('hidden');
      break;
    default:
      document.querySelector('#email-form').removeAttribute('hidden');
      document.querySelector('#email-subscribed').setAttribute('hidden', '');
      document.querySelector('#email-confirmed').setAttribute('hidden', '');
      break;
  }
}

function setupResetButton() {
  const resetButton = document.querySelector('#email-reset');
  if (!resetButton) return;
  resetButton.addEventListener('click', function(event) {
    event.preventDefault();
    window.history.pushState({}, '', window.location.pathname);
    setupForm();
  });
}

document.addEventListener('DOMContentLoaded', setupForm);
document.addEventListener('hashchange', setupForm);
document.addEventListener('popstate', setupForm);
document.addEventListener('DOMContentLoaded', setupResetButton);
