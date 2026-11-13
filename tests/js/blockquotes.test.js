import { describe, it, expect, vi, afterEach } from "vitest";

import {
  debounce,
  getActiveIndex,
  parseCssDuration,
} from "../../src/jg/coop/js/blockquotes";

describe("blockquotes.js", () => {
  describe("parseCssDuration()", () => {
    it.each([
      ["4s", 4000],
      ["0.5s", 500],
      [".5s", 500],
      ["300ms", 300],
      ["  2s  ", 2000],
      ["", 1000],
      ["fast", 1000],
      ["5", 1000],
    ])("parses %j", (value, expected) => {
      expect(parseCssDuration(value, 1000)).toBe(expected);
    });
  });

  describe("getActiveIndex()", () => {
    it.each([
      [0, 0],
      [2, 2],
      [3, 0],
      [4, 1],
    ])("returns active index for %i", (index, expected) => {
      expect(getActiveIndex(index, 3)).toBe(expected);
    });
  });

  describe("debounce()", () => {
    afterEach(() => {
      vi.useRealTimers();
    });

    it("calls the function once after the calls stop", () => {
      vi.useFakeTimers();
      const fn = vi.fn();
      const debounced = debounce(fn, 100);

      debounced(1);
      vi.advanceTimersByTime(50);
      debounced(2);
      vi.advanceTimersByTime(100);

      expect(fn.mock.calls).toEqual([[2]]);
    });
  });
});
