import { describe, it, expect } from "vitest";

import { getStudentPassEventName } from "../../src/jg/coop/js/student-pass";

describe("student-pass.js", () => {
  describe("getStudentPassEventName()", () => {
    it("returns event with the slug", () => {
      expect(getStudentPassEventName("czechitas")).toBe(
        "student_pass_czechitas",
      );
    });

    it.each([undefined, ""])("returns generic event for slug %j", (slug) => {
      expect(getStudentPassEventName(slug)).toBe("student_pass");
    });
  });
});
