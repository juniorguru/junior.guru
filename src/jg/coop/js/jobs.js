import { setupTagFilter } from "./tag-filter";

function setupJobs() {
  setupTagFilter("jobs");

  const subscribe = document.querySelector(".jobs-subscribe");
  subscribe?.addEventListener("click", () => {
    subscribe.hidden = true;
  });
}

document.addEventListener("DOMContentLoaded", setupJobs);
