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
      dialog.showModal();
      clubLink.focus();
    });
  });
}

document.addEventListener("DOMContentLoaded", setupDiscordLinks);
