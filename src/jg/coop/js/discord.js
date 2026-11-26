import { addUtmParams, getUtmParams } from "./checkout-utm";

function setupDiscordLinks() {
  // Links opening an openable item, e.g. a manual job, only fall back
  // to Discord when JavaScript doesn't work, so they don't need the dialog
  const discordLinks = document.querySelectorAll(
    'a[href*="discord.com"][href*="769966886598737931"]:not([data-openable-action])',
  );
  const dialog = document.querySelector(".discord-dialog");
  if (!discordLinks.length || !dialog) return;

  const continueLink = dialog.querySelector(".discord-dialog-continue");
  const clubLink = dialog.querySelector(".discord-dialog-club");
  const clubUrl = clubLink.href;

  // The dialog has no padding, its content does, so clicks targeting
  // the dialog itself are clicks on the backdrop
  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) dialog.close();
  });
  continueLink.addEventListener("click", () => dialog.close());

  discordLinks.forEach((link) => {
    link.addEventListener("click", (event) => {
      event.preventDefault();
      continueLink.href = link.href;
      continueLink.target = link.target;
      clubLink.href = getClubUrl(clubUrl, link.dataset.discordDialogUtm);
      dialog.showModal();
      clubLink.focus();
    });
  });
}

/**
 * Adds UTM params to the dialog's link to the club page
 *
 * The params come from the clicked Discord link, e.g. a manual job sets
 * `data-discord-dialog-utm="utm_source=jobs-manual&…"`, so that
 * a signup can be traced back to where the person clicked.
 */
export function getClubUrl(clubUrl, utmQuery) {
  const utmParams = getUtmParams(new URLSearchParams(utmQuery ?? ""));
  return utmParams ? addUtmParams(clubUrl, utmParams) : clubUrl;
}

document.addEventListener("DOMContentLoaded", setupDiscordLinks);
