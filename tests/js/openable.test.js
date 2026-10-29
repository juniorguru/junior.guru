import { describe, it, expect, beforeEach } from "vitest";

import { setupOpenables } from "../../src/jg/coop/js/openable";

describe("openable.js", () => {
  let item;

  beforeEach(() => {
    document.body.innerHTML = `
      <div data-openable class="open">
        <a href="https://example.com" data-openable-action="open" data-openable-visible="closed">Title</a>
        <button data-openable-action="close" data-openable-visible="open" hidden>Close</button>
        <div data-openable-visible="open" hidden>Details</div>
      </div>
    `;
    item = document.querySelector("[data-openable]");
    setupOpenables();
  });

  const isVisible = (selector) => !item.querySelector(selector).hidden;

  it("starts closed", () => {
    expect(item.classList.contains("open")).toBe(false);
  });

  it("opens", () => {
    item.querySelector('[data-openable-action="open"]').click();
    expect([
      item.classList.contains("open"),
      isVisible("a"),
      isVisible("button"),
      isVisible("div"),
    ]).toEqual([true, false, true, true]);
  });

  it("prevents following the link when opening", () => {
    const event = new MouseEvent("click", { cancelable: true });
    item.querySelector("a").dispatchEvent(event);
    expect(event.defaultPrevented).toBe(true);
  });

  it("closes", () => {
    item.querySelector('[data-openable-action="open"]').click();
    item.querySelector('[data-openable-action="close"]').click();
    expect([
      item.classList.contains("open"),
      isVisible("a"),
      isVisible("button"),
      isVisible("div"),
    ]).toEqual([false, true, false, false]);
  });
});
