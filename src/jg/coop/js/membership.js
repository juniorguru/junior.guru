function setupMembershipSuccess() {
  const searchParams = new URLSearchParams(window.location.search);
  const isSuccess = isMembershipSuccess(searchParams);
  document.querySelectorAll(".membership-success").forEach((element) => {
    element.hidden = !isSuccess;
  });
}

/**
 * Checks whether the URL says the user has just successfully signed up
 *
 * Memberful redirects to e.g. https://junior.guru/membership/?state=success
 */
export function isMembershipSuccess(searchParams) {
  return searchParams.get("state") === "success";
}

document.addEventListener("DOMContentLoaded", setupMembershipSuccess);
