import { setupTagFilter } from "./tag-filter";

function setupJobs() {
  setupTagFilter("jobs", { onRender: placeBoxes });

  const subscribe = document.querySelector(".jobs-subscribe");
  subscribe?.addEventListener("click", () => {
    subscribe.hidden = true;
  });
}

/**
 * Moves boxes such as the club box after given numbers of visible regular jobs
 *
 * The server puts the boxes at the right positions, but filters hide jobs,
 * so the boxes would end up next to the top or the bottom of the list.
 * Each position is in the box's `data-jobs-box-position` attribute.
 * If there aren't enough visible regular jobs, the box goes at the end.
 */
export function placeBoxes() {
  const boxes = Array.from(document.querySelectorAll(".jobs-item.jobs-box"));
  if (!boxes.length) return;

  const regularJobs = Array.from(
    document.querySelectorAll(".jobs-item.tagged:not(.highlighted)"),
  ).filter((element) => !element.hidden);
  boxes
    .sort((a, b) => getBoxPosition(a) - getBoxPosition(b))
    .forEach((box) => {
      const anchor = regularJobs[getBoxPosition(box) - 1];
      if (anchor) {
        anchor.after(box);
      } else {
        box.parentElement.append(box);
      }
    });
}

function getBoxPosition(box) {
  return Number(box.dataset.jobsBoxPosition);
}

document.addEventListener("DOMContentLoaded", setupJobs);
