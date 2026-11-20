import { describe, it, expect } from "vitest";

import { addUtmParams, getUtmParams } from "../../src/jg/coop/js/checkout-utm";

describe("checkout-utm.js", () => {
  describe("getUtmParams()", () => {
    it.each([
      ["", null],
      ["?foo=bar", null],
      ["?utm_medium=email", null],
      ["?utm_source=", null],
      ["?utm_source=test", { utm_source: "test" }],
      [
        "?utm_source=winback&utm_medium=email&utm_campaign=2027-01&foo=bar",
        { utm_source: "winback", utm_medium: "email", utm_campaign: "2027-01" },
      ],
      ["?utm_source=test&utm_medium=", { utm_source: "test" }],
    ])("returns result for %j", (search, expected) => {
      expect(getUtmParams(new URLSearchParams(search))).toEqual(expected);
    });
  });

  describe("addUtmParams()", () => {
    it("adds params to a checkout link", () => {
      expect(
        addUtmParams("https://juniorguru.memberful.com/checkout?plan=143775", {
          utm_source: "gh-check",
          utm_medium: "github",
        }),
      ).toBe(
        "https://juniorguru.memberful.com/checkout?plan=143775&utm_source=gh-check&utm_medium=github",
      );
    });

    it("replaces existing UTM params", () => {
      expect(
        addUtmParams(
          "https://juniorguru.memberful.com/checkout?plan=1&utm_source=old&utm_campaign=old",
          { utm_source: "new" },
        ),
      ).toBe("https://juniorguru.memberful.com/checkout?plan=1&utm_source=new");
    });
  });
});
