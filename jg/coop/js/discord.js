function interceptDiscordLinks() {
  const discordLinks = document.querySelectorAll(
    'a[href*="discord.com"][href*="769966886598737931"]',
  );
  const dialog = document.querySelector(".discord-dialog");
  if (!discordLinks.length || !dialog) return;

  dialog.addEventListener("click", function (event) {
    const rect = dialog.getBoundingClientRect();
    const isInDialog =
      rect.top <= event.clientY &&
      event.clientY <= rect.top + rect.height &&
      rect.left <= event.clientX &&
      event.clientX <= rect.left + rect.width;
    if (!isInDialog) dialog.close();
  });

  const continueLink = dialog.querySelector(".discord-dialog-continue");
  const clubLink = dialog.querySelector(".discord-dialog-club");

  continueLink.addEventListener("click", function () {
    dialog.close();
  });

  discordLinks.forEach((link) => {
    link.addEventListener("click", function (event) {
      event.preventDefault();
      continueLink.setAttribute("href", link.href);
      continueLink.setAttribute("target", link.target);
      dialog.showModal();
      clubLink.focus();
    });
  });
}

document.addEventListener("DOMContentLoaded", interceptDiscordLinks);
