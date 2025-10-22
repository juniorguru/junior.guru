function setupEmailForm() {
  const form = document.querySelector("#email-form");
  const subscribed = document.querySelector("#email-subscribed");
  const confirmed = document.querySelector("#email-confirmed");

  if (!form || !subscribed || !confirmed) return;

  const emailAddress = new URLSearchParams(window.location.search).get("email_address");
  if (emailAddress && emailAddress.includes("@")) {
    // subscribed: https://junior.guru/news/?email_address=example@example.com
    form.setAttribute("hidden", "");
    subscribed.removeAttribute("hidden");
    confirmed.setAttribute("hidden", "");
  } else if (emailAddress) {
    // confirmed: https://junior.guru/news/?email_address=confirmed
    form.setAttribute("hidden", "");
    subscribed.setAttribute("hidden", "");
    confirmed.removeAttribute("hidden");
  } else {
    form.removeAttribute("hidden");
    subscribed.setAttribute("hidden", "");
    confirmed.setAttribute("hidden", "");
  }
}

function setupEmailResetButton() {
  const resetButton = document.querySelector("#email-reset");
  if (!resetButton) return;
  resetButton.addEventListener("click", function (event) {
    event.preventDefault();
    const url = new URL(window.location.href);
    url.searchParams.delete("email_address");
    window.history.pushState({}, "", url.pathname + url.search);
    setupEmailForm();
  });
}

document.addEventListener("DOMContentLoaded", setupEmailForm);
document.addEventListener("popstate", setupEmailForm);
document.addEventListener("DOMContentLoaded", setupEmailResetButton);
