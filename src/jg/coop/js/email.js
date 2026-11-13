function setupEmail() {
  const form = document.querySelector("#email-form");
  const subscribed = document.querySelector("#email-subscribed");
  const confirmed = document.querySelector("#email-confirmed");
  if (!form || !subscribed || !confirmed) return;

  function render() {
    const searchParams = new URLSearchParams(window.location.search);
    const state = getEmailState(searchParams);
    form.hidden = state !== "form";
    subscribed.hidden = state !== "subscribed";
    confirmed.hidden = state !== "confirmed";
  }

  document.querySelector("#email-reset")?.addEventListener("click", (event) => {
    event.preventDefault();
    const url = new URL(window.location.href);
    url.searchParams.delete("email_address");
    window.history.pushState({}, "", url);
    render();
  });
  window.addEventListener("popstate", render);
  render();
}

/**
 * Decides which state of the newsletter sign up to show, based on the URL
 *
 * - subscribed: https://junior.guru/news/?email_address=example@example.com
 * - confirmed: https://junior.guru/news/?email_address=confirmed
 * - form: anything else
 */
export function getEmailState(searchParams) {
  const emailAddress = searchParams.get("email_address") ?? "";
  if (emailAddress === "confirmed") return "confirmed";
  if (emailAddress.includes("@")) return "subscribed";
  return "form";
}

document.addEventListener("DOMContentLoaded", setupEmail);
