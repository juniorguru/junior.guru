import { Tooltip } from "bootstrap";

import { setupTagFilter } from "./tag-filter";

function setupCandidates() {
  setupTagFilter("candidates");

  document
    .querySelectorAll(".candidates-badge[title]")
    .forEach((badge) => new Tooltip(badge));
}

document.addEventListener("DOMContentLoaded", setupCandidates);
