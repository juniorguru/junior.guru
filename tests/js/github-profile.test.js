import { describe, it, expect } from "vitest";
import { getGitHubProfileUsername } from "../../jg/coop/js/github-profile";

describe("github-profile.js", () => {
  describe("getGitHubProfileUsername()", () => {
    it("parses username as-is", () => {
      expect(getGitHubProfileUsername("honzajavorek")).toBe("honzajavorek");
    });
  });
});
