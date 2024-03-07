function setupMembershipSuccess() {
  if (window.location.search.includes("state=success")) {
    const elements = document.querySelectorAll(".membership-success");
    Array.from(elements).forEach(function (element) {
      element.removeAttribute("hidden");
    });
  }
}

document.addEventListener("DOMContentLoaded", setupMembershipSuccess);
