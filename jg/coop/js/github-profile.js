function setupGitHubProfileForm() {
  const form = document.querySelector("#github-profile-form");
  const input = form.querySelector("#github-profile-input");
  const titleInput = form.querySelector('[name="title"]');
  const bodyInput = form.querySelector('[name="body"]');

  if (!form || !input || !titleInput || !bodyInput) return;

  const defaultTitle = titleInput.value;
  const defaultBody = bodyInput.value;

  form.addEventListener("submit", (event) => {
    const username = input.value
      .trim()
      .replace(/^https?:\/\//, "")
      .replace(/^www\./, "")
      .replace(/^github\.com/, "")
      .replace(/^@/, "")
      .replace(/^\/+/, "")
      .replace(/\/+$/, "");
    titleInput.value += ` ${username}`;
    bodyInput.value = bodyInput.value.replace("@", `@${username}`);

    setTimeout(() => {
      titleInput.value = defaultTitle;
      bodyInput.value = defaultBody;
      input.value = `@${username}`;
    }, 100);
  });
}

document.addEventListener("DOMContentLoaded", setupGitHubProfileForm);
