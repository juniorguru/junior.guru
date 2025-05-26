function setupGitHubProfileForm() {
  const form = document.querySelector("#github-profile-form");

  if (!form) return;

  const input = form.querySelector("#github-profile-input");
  const titleInput = form.querySelector('[name="title"]');
  const bodyInput = form.querySelector('[name="body"]');

  if (!input || !titleInput || !bodyInput) return;

  const defaultTitle = titleInput.value;
  const defaultBody = bodyInput.value;

  form.addEventListener("submit", (event) => {
    const username = getGitHubProfileUsername(input.value);
    titleInput.value += ` @${username}`;
    bodyInput.value = bodyInput.value.replace("@", `@${username}`);

    setTimeout(() => {
      titleInput.value = defaultTitle;
      bodyInput.value = defaultBody;
      input.value = `@${username}`;
    }, 100);
  });
}

export function getGitHubProfileUsername(inputValue) {
  const match = inputValue.match(/github\.com\/([^\/?]+)/);
  if (match) {
    return match[1];
  }
  return inputValue.trim().replace(/^@/, "");
}

document.addEventListener("DOMContentLoaded", setupGitHubProfileForm);
