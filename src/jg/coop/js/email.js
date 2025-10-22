function setupEmailForm() {
  const form = document.querySelector("#email-form");
  const subscribed = document.querySelector("#email-subscribed");
  const confirmed = document.querySelector("#email-confirmed");

  if (!form || !subscribed || !confirmed) return;

  const status = new URLSearchParams(window.location.search).get("status");
  switch (status) {
    case "subscribed":
      form.setAttribute("hidden", "");
      subscribed.removeAttribute("hidden");
      confirmed.setAttribute("hidden", "");
      break;
    case "confirmed":
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

function setupEmailResetButton() {
  const resetButton = document.querySelector("#email-reset");
  if (!resetButton) return;
  resetButton.addEventListener("click", function (event) {
    event.preventDefault();
    const url = new URL(window.location.href);
    url.searchParams.delete("status");
    window.history.pushState({}, "", url.pathname + url.search);
    setupEmailForm();
  });
}

document.addEventListener("DOMContentLoaded", setupEmailForm);
document.addEventListener("popstate", setupEmailForm);
document.addEventListener("DOMContentLoaded", setupEmailResetButton);
