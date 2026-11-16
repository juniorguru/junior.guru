import { describe, it, expect, vi } from "vitest";

// Chart.js needs a canvas, which jsdom doesn't have
vi.mock("chart.js/auto", () => ({ default: { register: () => {} } }));

const {
  mergeOptions,
  parseMilestonesOffset,
  markPartialLast,
  partialTitle,
  fadeColor,
} = await import("../../src/jg/coop/js/charts");

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

  describe("markPartialLast()", () => {
    const data = {
      labels: ["2026-09", "2026-10", "2026-11"],
      datasets: [{ data: [1, 2, 3], borderColor: "#1755d1" }],
    };

    it.each([
      [0, undefined],
      [1, [4, 4]],
    ])("dashes line segment ending at index %j+1", (p0DataIndex, expected) => {
      const [dataset] = markPartialLast(data, "line").datasets;
      expect(
        dataset.segment.borderDash({
          p0DataIndex,
          p1DataIndex: p0DataIndex + 1,
        }),
      ).toEqual(expected);
    });

    it.each([
      [1, "#1755d1"],
      [2, "rgba(23, 85, 209, 0.4)"],
    ])("fades bar at index %j", (dataIndex, expected) => {
      const barData = {
        labels: data.labels,
        datasets: [{ data: [1, 2, 3], backgroundColor: "#1755d1" }],
      };
      const [dataset] = markPartialLast(barData, "bar").datasets;
      expect(dataset.backgroundColor({ dataIndex })).toBe(expected);
    });

    it("respects dataset type over chart type", () => {
      const mixed = {
        labels: data.labels,
        datasets: [{ type: "line", data: [1, 2, 3] }],
      };
      const [dataset] = markPartialLast(mixed, "bar").datasets;
      expect(dataset.segment.borderDash({ p1DataIndex: 2 })).toEqual([4, 4]);
    });

    it("doesn't modify the original data", () => {
      markPartialLast(data, "line");
      expect(data.datasets[0]).toEqual({
        data: [1, 2, 3],
        borderColor: "#1755d1",
      });
    });
  });

  describe("partialTitle()", () => {
    it.each([
      [[{ label: "2026-10", dataIndex: 1 }], "2026-10"],
      [[{ label: "2026-11", dataIndex: 2 }], "2026-11 (neúplný měsíc)"],
      [[], ""],
    ])("titles %j", (items, expected) => {
      expect(partialTitle(items, 2)).toBe(expected);
    });
  });

  describe("fadeColor()", () => {
    it.each([
      ["#1755d1", "rgba(23, 85, 209, 0.4)"],
      ["#FFFFFF", "rgba(255, 255, 255, 0.4)"],
      ["red", "red"],
      [undefined, undefined],
    ])("fades %j", (color, expected) => {
      expect(fadeColor(color, 0.4)).toBe(expected);
    });
  });
});
