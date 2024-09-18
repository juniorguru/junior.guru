function setupForm() {
  const form = document.querySelector("#email-form");
  const subscribed = document.querySelector("#email-subscribed");
  const confirmed = document.querySelector("#email-confirmed");

  if (!form || !subscribed || !confirmed) return;

  switch (window.location.hash) {
    case "#email-subscribed":
      form.setAttribute("hidden", "");
      subscribed.removeAttribute("hidden");
      confirmed.setAttribute("hidden", "");
      break;
    case "#email-confirmed":
      form.setAttribute("hidden", "");
      subscribed.setAttribute("hidden", "");
      confirmed.removeAttribute("hidden");
      break;
    default:
      form.removeAttribute("hidden");
      subscribed.setAttribute("hidden", "");
      confirmed.setAttribute("hidden", "");
      break;
  }
}

function setupResetButton() {
  const resetButton = document.querySelector("#email-reset");
  if (!resetButton) return;
  resetButton.addEventListener("click", function (event) {
    event.preventDefault();
    window.history.pushState({}, "", window.location.pathname);
    setupForm();
  });
}

document.addEventListener("DOMContentLoaded", setupForm);
document.addEventListener("hashchange", setupForm);
document.addEventListener("popstate", setupForm);
document.addEventListener("DOMContentLoaded", setupResetButton);
