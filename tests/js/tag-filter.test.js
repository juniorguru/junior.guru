import { describe, it, expect, beforeEach } from "vitest";

import {
  createTags,
  formatTags,
  hasTag,
  matchesTags,
  mergeTags,
  parseTags,
  setupTagFilter,
  toggleTag,
} from "../../src/jg/coop/js/tag-filter";

const KNOWN_TAGS = new Map([
  ["tech", new Set(["java", "python"])],
  ["location", new Set(["brno", "remote"])],
]);

describe("tag-filter.js", () => {
  describe("createTags()", () => {
    it("groups tags by type", () => {
      expect(
        createTags([
          { type: "tech", slug: "python" },
          { type: "location", slug: "brno" },
          { type: "tech", slug: "java" },
        ]),
      ).toEqual(
        new Map([
          ["tech", new Set(["python", "java"])],
          ["location", new Set(["brno"])],
        ]),
      );
    });
  });

  describe("parseTags()", () => {
    it("parses tags separated by pipe", () => {
      const params = new URLSearchParams("tech=java|python&location=remote");
      expect(parseTags(params, KNOWN_TAGS)).toEqual(
        new Map([
          ["tech", new Set(["java", "python"])],
          ["location", new Set(["remote"])],
        ]),
      );
    });

    it("ignores unknown params", () => {
      const params = new URLSearchParams("utm_source=newsletter");
      expect(parseTags(params, KNOWN_TAGS)).toEqual(new Map());
    });

    it("ignores unknown tags", () => {
      const params = new URLSearchParams("tech=cobol|python&location=");
      expect(parseTags(params, KNOWN_TAGS)).toEqual(
        new Map([["tech", new Set(["python"])]]),
      );
    });
  });

  describe("formatTags()", () => {
    it("formats tags sorted and separated by pipe", () => {
      const tags = new Map([["tech", new Set(["python", "java"])]]);
      expect(formatTags(new URLSearchParams(), KNOWN_TAGS, tags)).toBe(
        "tech=java%7Cpython",
      );
    });

    it("orders types as known tags", () => {
      const tags = new Map([
        ["location", new Set(["brno"])],
        ["tech", new Set(["python"])],
      ]);
      expect(formatTags(new URLSearchParams(), KNOWN_TAGS, tags)).toBe(
        "tech=python&location=brno",
      );
    });

    it("replaces previous tags and keeps unknown params", () => {
      const params = new URLSearchParams(
        "tech=java&location=brno&utm_source=x",
      );
      const tags = new Map([["tech", new Set(["python"])]]);
      expect(formatTags(params, KNOWN_TAGS, tags)).toBe(
        "utm_source=x&tech=python",
      );
    });

    it("roundtrips with parseTags()", () => {
      const tags = new Map([
        ["location", new Set(["brno", "remote"])],
        ["tech", new Set(["python"])],
      ]);
      const params = new URLSearchParams(formatTags("", KNOWN_TAGS, tags));
      expect(parseTags(params, KNOWN_TAGS)).toEqual(tags);
    });
  });

  describe("toggleTag()", () => {
    it("adds missing tag", () => {
      expect(toggleTag(new Map(), { type: "tech", slug: "python" })).toEqual(
        new Map([["tech", new Set(["python"])]]),
      );
    });

    it("removes present tag and drops empty type", () => {
      const tags = new Map([["tech", new Set(["python"])]]);
      expect(toggleTag(tags, { type: "tech", slug: "python" })).toEqual(
        new Map(),
      );
    });

    it("doesn't mutate the original", () => {
      const tags = new Map([["tech", new Set(["python"])]]);
      toggleTag(tags, { type: "tech", slug: "java" });
      expect(tags).toEqual(new Map([["tech", new Set(["python"])]]));
    });
  });

  describe("mergeTags()", () => {
    it("merges tags of the same type", () => {
      expect(
        mergeTags(
          new Map([["location", new Set(["brno"])]]),
          new Map([
            ["location", new Set(["remote"])],
            ["tech", new Set(["python"])],
          ]),
        ),
      ).toEqual(
        new Map([
          ["location", new Set(["brno", "remote"])],
          ["tech", new Set(["python"])],
        ]),
      );
    });
  });

  describe("hasTag()", () => {
    const tags = new Map([["tech", new Set(["python"])]]);

    it.each([
      [{ type: "tech", slug: "python" }, true],
      [{ type: "tech", slug: "java" }, false],
      [{ type: "location", slug: "python" }, false],
    ])("checks %o", (tag, expected) => {
      expect(hasTag(tags, tag)).toBe(expected);
    });
  });

  describe("matchesTags()", () => {
    const itemTags = [
      { type: "tech", slug: "python" },
      { type: "location", slug: "brno" },
    ];

    it.each([
      ["no active tags", new Map(), true],
      ["one matching tag", new Map([["tech", new Set(["python"])]]), true],
      [
        "any tag of a type",
        new Map([["tech", new Set(["java", "python"])]]),
        true,
      ],
      ["no tag of a type", new Map([["tech", new Set(["java"])]]), false],
      [
        "all types",
        new Map([
          ["tech", new Set(["python"])],
          ["location", new Set(["brno"])],
        ]),
        true,
      ],
      [
        "only some types",
        new Map([
          ["tech", new Set(["python"])],
          ["location", new Set(["remote"])],
        ]),
        false,
      ],
    ])("matches %s", (_, activeTags, expected) => {
      expect(matchesTags(itemTags, activeTags)).toBe(expected);
    });
  });
  describe("setupTagFilter()", () => {
    const select = (selector) => document.querySelector(selector);
    const isHidden = (selector) => select(selector).hidden;

    beforeEach(() => {
      window.history.replaceState({}, "", "/jobs/brno/");
      document.body.innerHTML = `
        <dl class="jobs-filters noscript">
          <button class="jobs-tag" data-jobs-tag="remote" data-jobs-tag-type="location" aria-pressed="false" hidden></button>
          <button class="jobs-tag active disabled" data-jobs-tag="brno" data-jobs-tag-type="location" aria-pressed="true" disabled></button>
          <button class="jobs-tag" data-jobs-tag="python" data-jobs-tag-type="tech" aria-pressed="false" hidden></button>
          <span class="jobs-noscript">Error</span>
        </dl>
        <ul>
          <li class="jobs-item tagged" id="brno-java">
            <span class="jobs-tag" data-jobs-tag="brno" data-jobs-tag-type="location"></span>
            <span class="jobs-tag" data-jobs-tag="java" data-jobs-tag-type="tech"></span>
          </li>
          <li class="jobs-item tagged" id="praha-python">
            <span class="jobs-tag" data-jobs-tag="praha" data-jobs-tag-type="location"></span>
            <span class="jobs-tag" data-jobs-tag="python" data-jobs-tag-type="tech"></span>
          </li>
          <li class="jobs-empty" hidden></li>
        </ul>
      `;
      setupTagFilter("jobs");
    });

    it("shows selectable tags and removes noscript fallbacks", () => {
      expect([
        isHidden("[data-jobs-tag='remote']"),
        isHidden("[data-jobs-tag='python']"),
        select(".jobs-filters").classList.contains("noscript"),
        select(".jobs-noscript"),
      ]).toEqual([false, false, false, null]);
    });

    it("filters by the fixed tag", () => {
      expect([
        isHidden("#brno-java"),
        isHidden("#praha-python"),
        isHidden(".jobs-empty"),
        select("#brno-java [data-jobs-tag='brno']").classList.contains(
          "matching",
        ),
      ]).toEqual([false, true, true, true]);
    });

    it("toggles a tag on click", () => {
      const button = select(".jobs-filters [data-jobs-tag='python']");
      button.click();
      expect([
        button.classList.contains("active"),
        button.getAttribute("aria-pressed"),
      ]).toEqual([true, "true"]);
    });

    it("writes clicked tags to the URL without the fixed tag", () => {
      select(".jobs-filters [data-jobs-tag='python']").click();
      select(".jobs-filters [data-jobs-tag='remote']").click();
      expect(window.location.search).toBe("?location=remote&tech=python");
    });

    it("shows the empty state when nothing matches", () => {
      select(".jobs-filters [data-jobs-tag='python']").click();
      expect([
        isHidden("#brno-java"),
        isHidden("#praha-python"),
        isHidden(".jobs-empty"),
      ]).toEqual([true, true, false]);
    });

    it("restores the filter from the URL on popstate", () => {
      select(".jobs-filters [data-jobs-tag='python']").click();
      window.history.replaceState({}, "", "/jobs/brno/");
      window.dispatchEvent(new PopStateEvent("popstate"));
      expect([
        select(".jobs-filters [data-jobs-tag='python']").classList.contains(
          "active",
        ),
        isHidden("#brno-java"),
        isHidden(".jobs-empty"),
      ]).toEqual([false, false, true]);
    });
  });
});
