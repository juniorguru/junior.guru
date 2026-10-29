/**
 * Sets up items which can be opened in place to show more details
 *
 * Expects `[data-openable]` items containing:
 *
 * - `[data-openable-action="open"]` and `[data-openable-action="close"]` controls
 * - `[data-openable-visible="open"]` elements, shown only when the item is open
 * - `[data-openable-visible="closed"]` elements, shown only when the item is closed
 *
 * The open item gets the `open` class.
 */
export function setupOpenables(root = document) {
  root.querySelectorAll("[data-openable]").forEach(setupOpenable);
}

function setupOpenable(item) {
  item.querySelectorAll('[data-openable-action="open"]').forEach((element) => {
    element.addEventListener("click", (event) => {
      event.preventDefault();
      setOpen(item, true);
    });
  });
  item.querySelectorAll('[data-openable-action="close"]').forEach((element) => {
    element.addEventListener("click", () => setOpen(item, false));
  });
  setOpen(item, false);
}

export function setOpen(item, isOpen) {
  item.classList.toggle("open", isOpen);
  item.querySelectorAll("[data-openable-visible]").forEach((element) => {
    element.hidden = (element.dataset.openableVisible === "open") !== isOpen;
  });
}

document.addEventListener("DOMContentLoaded", () => setupOpenables());
