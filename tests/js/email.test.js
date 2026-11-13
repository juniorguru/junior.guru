import { describe, it, expect } from "vitest";

import { getEmailState } from "../../src/jg/coop/js/email";

describe("email.js", () => {
  describe("getEmailState()", () => {
    it.each([
      ["", "form"],
      ["?email_address=example@example.com", "subscribed"],
      ["?email_address=confirmed", "confirmed"],
      ["?email_address=nonsense", "form"],
      ["?email_address=", "form"],
      ["?foo=bar", "form"],
    ])("returns state for %j", (search, expected) => {
      expect(getEmailState(new URLSearchParams(search))).toBe(expected);
    });
  });
});
