import { setupTagFilter } from "./tag-filter";

function setupJobs() {
  setupTagFilter("jobs", { onRender: placeClubBox });

  const subscribe = document.querySelector(".jobs-subscribe");
  subscribe?.addEventListener("click", () => {
    subscribe.hidden = true;
  });
}

/**
 * Moves the club box after the given number of visible regular jobs
 *
 * The server puts the box at the right position, but filters hide jobs,
 * so the box would end up next to the top or the bottom of the list.
 * The position is in the box's `data-jobs-club-position` attribute.
 * If there aren't enough visible regular jobs, the box goes at the end.
 */
export function placeClubBox() {
  const clubBox = document.querySelector(".jobs-item.club");
  if (!clubBox) return;

  const position = Number(clubBox.dataset.jobsClubPosition);
  const regularJobs = Array.from(
    document.querySelectorAll(".jobs-item.tagged:not(.highlighted)"),
  ).filter((element) => !element.hidden);
  const anchor = regularJobs[position - 1];
  if (anchor) {
    anchor.after(clubBox);
  } else {
    clubBox.parentElement.append(clubBox);
  }
}

document.addEventListener("DOMContentLoaded", setupJobs);
