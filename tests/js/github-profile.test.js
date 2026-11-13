import { describe, it, expect } from "vitest";

import {
  getGitHubProfileIssueURL,
  getGitHubProfileUsername,
} from "../../src/jg/coop/js/github-profile";

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

  describe("getGitHubProfileIssueURL()", () => {
    it("fills the username into title and body", () => {
      const fields = [
        ["template", "check.md"],
        ["title", "Zpětná vazba na profil"],
        ["body", "Kuřátko, mrkni prosím na @, díky!"],
      ];
      const url = new URL(
        getGitHubProfileIssueURL(
          "https://github.com/juniorguru/eggtray/issues/new",
          fields,
          "honzajavorek",
        ),
      );

      expect([url.origin + url.pathname, ...url.searchParams]).toEqual([
        "https://github.com/juniorguru/eggtray/issues/new",
        ["template", "check.md"],
        ["title", "Zpětná vazba na profil @honzajavorek"],
        ["body", "Kuřátko, mrkni prosím na @honzajavorek, díky!"],
      ]);
    });
  });
});
