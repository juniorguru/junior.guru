import { describe, it, expect } from "vitest";
import { getGitHubProfileUsername } from "../../src/jg/coop/js/github-profile";

describe("github-profile.js", () => {
  describe("getGitHubProfileUsername()", () => {
    it("parses username as-is", () => {
      expect(getGitHubProfileUsername("honzajavorek")).toBe("honzajavorek");
    });

    it("parses username with whitespace", () => {
      expect(
        getGitHubProfileUsername("      honzajavorek      \t        "),
      ).toBe("honzajavorek");
    });

    it("parses @username", () => {
      expect(getGitHubProfileUsername("@honzajavorek")).toBe("honzajavorek");
    });

    it("parses @username with whitespace", () => {
      expect(
        getGitHubProfileUsername("      @honzajavorek      \t        "),
      ).toBe("honzajavorek");
    });

    it("parses repository link", () => {
      expect(
        getGitHubProfileUsername(
          "https://github.com/honzajavorek/honzajavorek.cz",
        ),
      ).toBe("honzajavorek");
    });

    it("parses GitHub profile link", () => {
      expect(getGitHubProfileUsername("https://github.com/honzajavorek/")).toBe(
        "honzajavorek",
      );
    });

    it("parses GitHub profile link without protocol", () => {
      expect(getGitHubProfileUsername("github.com/honzajavorek/")).toBe(
        "honzajavorek",
      );
    });

    it("parses GitHub profile link without HTTPS", () => {
      expect(getGitHubProfileUsername("http://github.com/honzajavorek/")).toBe(
        "honzajavorek",
      );
    });

    it("parses GitHub profile link with www.", () => {
      expect(
        getGitHubProfileUsername("http://www.github.com/honzajavorek/"),
      ).toBe("honzajavorek");
    });

    it("parses GitHub profile link with parameters", () => {
      expect(
        getGitHubProfileUsername(
          "https://github.com/honzajavorek?tab=projects",
        ),
      ).toBe("honzajavorek");
    });
  });
});
