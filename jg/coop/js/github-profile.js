function setupGitHubProfileForm() {
  const form = document.querySelector("#github-profile-form");
  const input = form.querySelector("#github-profile-input");
  const titleInput = form.querySelector('[name="title"]');
  const bodyInput = form.querySelector('[name="body"]');

  if (!form || !input || !titleInput || !bodyInput) return;

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
      form.reset();
      input.value = `@${username}`;
    }, 100);
  });
}

document.addEventListener("DOMContentLoaded", setupGitHubProfileForm);
