import { describe, it, expect } from "vitest";

import { addUtmParams } from "../../src/jg/coop/js/metrics";

describe("metrics.js", () => {
  describe("addUtmParams()", () => {
    it("adds default UTM params", () => {
      expect(addUtmParams("https://example.com/")).toBe(
        "https://example.com/?utm_source=juniorguru&utm_medium=content&utm_campaign=juniorguru",
      );
    });

    it("adds custom medium and campaign", () => {
      expect(
        addUtmParams("https://example.com/", {
          medium: "job",
          campaign: "jobs",
        }),
      ).toBe(
        "https://example.com/?utm_source=juniorguru&utm_medium=job&utm_campaign=jobs",
      );
    });

    it("keeps existing UTM params and other params", () => {
      expect(
        addUtmParams("https://example.com/?a=1&utm_source=foo#bar", {}),
      ).toBe(
        "https://example.com/?a=1&utm_source=foo&utm_medium=content&utm_campaign=juniorguru#bar",
      );
    });

    it("throws on invalid URL", () => {
      expect(() => addUtmParams("nonsense")).toThrow(TypeError);
    });
  });
});
