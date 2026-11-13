function setupGitHubProfileForm() {
  const form = document.querySelector("#github-profile-form");
  const input = form?.querySelector("#github-profile-input");
  if (!input) return;

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const username = getGitHubProfileUsername(input.value);
    const url = getGitHubProfileIssueURL(
      form.action,
      new FormData(form),
      username,
    );
    window.sa_event?.("github_profile_check");
    window.open(url, "_blank", "noopener");
    input.value = `@${username}`;
  });
}

export function getGitHubProfileUsername(inputValue) {
  const match = inputValue.match(/github\.com\/([^/?]+)/);
  if (match) {
    return match[1];
  }
  return inputValue.trim().replace(/^@/, "");
}

/**
 * Builds URL of a new GitHub issue, which asks the bot to check the profile
 *
 * Takes the form fields and fills the username into the title and body.
 * The body contains a lone "@" as a placeholder for the username.
 */
export function getGitHubProfileIssueURL(action, fields, username) {
  const url = new URL(action);
  for (const [name, value] of fields) {
    if (name === "title") {
      url.searchParams.set(name, `${value} @${username}`);
    } else if (name === "body") {
      url.searchParams.set(name, value.replace("@", `@${username}`));
    } else {
      url.searchParams.set(name, value);
    }
  }
  return url.toString();
}

document.addEventListener("DOMContentLoaded", setupGitHubProfileForm);
