import { describe, it, expect, beforeEach } from "vitest";

import { placeClubBox } from "../../src/jg/coop/js/jobs";

const ids = () =>
  Array.from(document.querySelectorAll(".jobs-item"), (element) => element.id);

const regularJob = (id, hidden = false) =>
  `<li class="jobs-item tagged" id="${id}"${hidden ? " hidden" : ""}></li>`;

describe("jobs.js", () => {
  describe("placeClubBox()", () => {
    beforeEach(() => {
      document.body.innerHTML = `
        <ul>
          <li class="jobs-item tagged highlighted" id="h1"></li>
          <li class="jobs-item manual highlighted" id="m1"></li>
          <li class="jobs-item club" id="club" data-jobs-club-position="2"></li>
          ${regularJob("r1", true)}
          ${regularJob("r2")}
          ${regularJob("r3", true)}
          ${regularJob("r4")}
          ${regularJob("r5")}
        </ul>
      `;
    });

    it("moves the box after the given number of visible regular jobs", () => {
      placeClubBox();

      expect(ids()).toEqual(["h1", "m1", "r1", "r2", "r3", "r4", "club", "r5"]);
    });

    it("moves the box to the end if there aren't enough visible regular jobs", () => {
      document.querySelector("#r4").hidden = true;
      document.querySelector("#r5").hidden = true;
      placeClubBox();

      expect(ids()).toEqual(["h1", "m1", "r1", "r2", "r3", "r4", "r5", "club"]);
    });

    it("does nothing without the box", () => {
      document.querySelector("#club").remove();
      placeClubBox();

      expect(ids()).toEqual(["h1", "m1", "r1", "r2", "r3", "r4", "r5"]);
    });
  });
});
