import { describe, it, expect } from "vitest";

import { getClubUrl } from "../../src/jg/coop/js/discord";

describe("discord.js", () => {
  describe("getClubUrl()", () => {
    it("keeps the club URL without UTM params", () => {
      expect(getClubUrl("https://junior.guru/club/", undefined)).toBe(
        "https://junior.guru/club/",
      );
    });

    it("adds UTM params to the club URL", () => {
      expect(
        getClubUrl(
          "https://junior.guru/club/",
          "utm_source=jobs-manual&utm_medium=web&utm_campaign=jaro",
        ),
      ).toBe(
        "https://junior.guru/club/?utm_source=jobs-manual&utm_medium=web&utm_campaign=jaro",
      );
    });

    it("ignores other params", () => {
      expect(
        getClubUrl(
          "https://junior.guru/club/",
          "utm_source=jobs-manual&foo=bar",
        ),
      ).toBe("https://junior.guru/club/?utm_source=jobs-manual");
    });
  });
});
