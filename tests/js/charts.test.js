import { describe, it, expect, vi } from "vitest";

// Chart.js needs a canvas, which jsdom doesn't have
vi.mock("chart.js/auto", () => ({ default: { register: () => {} } }));

const { mergeOptions, parseMilestonesOffset } =
  await import("../../src/jg/coop/js/charts");

describe("charts.js", () => {
  describe("mergeOptions()", () => {
    const defaults = {
      locale: "cs",
      scales: { x: {}, y: {} },
      plugins: { annotation: { annotations: {} } },
    };

    it("merges nested objects", () => {
      expect(
        mergeOptions(defaults, {
          scales: { y: { min: 0 } },
          plugins: { legend: { display: false } },
        }),
      ).toEqual({
        locale: "cs",
        scales: { x: {}, y: { min: 0 } },
        plugins: {
          annotation: { annotations: {} },
          legend: { display: false },
        },
      });
    });

    it("replaces values which aren't plain objects", () => {
      expect(
        mergeOptions({ a: [1, 2], b: { c: 1 } }, { a: [3], b: 5 }),
      ).toEqual({ a: [3], b: 5 });
    });

    it("doesn't share defaults between results", () => {
      const options = mergeOptions(defaults, {});
      options.scales.y.grid = { color: "red" };
      options.plugins.annotation.annotations.label = { type: "label" };

      expect(defaults).toEqual({
        locale: "cs",
        scales: { x: {}, y: {} },
        plugins: { annotation: { annotations: {} } },
      });
    });
  });

  describe("parseMilestonesOffset()", () => {
    it.each([
      [undefined, 0.2],
      ["0", 0],
      ["50", 0.5],
    ])("parses %j", (value, expected) => {
      expect(parseMilestonesOffset(value)).toBe(expected);
    });
  });
});
