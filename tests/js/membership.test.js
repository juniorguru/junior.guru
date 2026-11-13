import { describe, it, expect } from "vitest";

import { isMembershipSuccess } from "../../src/jg/coop/js/membership";

describe("membership.js", () => {
  describe("isMembershipSuccess()", () => {
    it.each([
      ["?state=success", true],
      ["?foo=bar&state=success", true],
      ["", false],
      ["?state=successful", false],
      ["?mystate=success", false],
      ["?state=failure", false],
    ])("returns result for %j", (search, expected) => {
      expect(isMembershipSuccess(new URLSearchParams(search))).toBe(expected);
    });
  });
});
