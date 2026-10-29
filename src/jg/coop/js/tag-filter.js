/**
 * Filters a list of items, such as jobs or candidates, by tags
 *
 * Expects markup with class names starting with the given prefix, e.g. "jobs":
 *
 * - `.jobs-filters` container with `.jobs-tag` buttons, one per tag
 * - `.jobs-item.tagged` items, each containing `.jobs-tag` elements
 * - `.jobs-empty` element, shown when no item matches
 * - `.jobs-noscript` elements, removed once the filtering works
 *
 * Each tag has `data-jobs-tag` (slug) and `data-jobs-tag-type` attributes.
 * Tags of the same type combine with OR, tags of different types with AND.
 * The selected tags are kept in the URL, e.g. `?tech=java|python&location=remote`.
 * Disabled buttons are fixed tags, e.g. the region on a region listing page.
 * They're always active and they don't get written to the URL.
 */
export function setupTagFilter(prefix) {
  const container = document.querySelector(`.${prefix}-filters`);
  if (!container) return;

  const readTag = (element) => ({
    element,
    type: element.getAttribute(`data-${prefix}-tag-type`),
    slug: element.getAttribute(`data-${prefix}-tag`),
  });
  const buttons = Array.from(
    container.querySelectorAll(`.${prefix}-tag`),
    readTag,
  );
  const items = Array.from(
    document.querySelectorAll(`.${prefix}-item.tagged`),
    (element) => ({
      element,
      tags: Array.from(element.querySelectorAll(`.${prefix}-tag`), readTag),
    }),
  );
  const empty = document.querySelector(`.${prefix}-empty`);

  const fixedTags = createTags(
    buttons.filter(({ element }) => element.disabled),
  );
  const selectableTags = createTags(
    buttons.filter(({ element }) => !element.disabled),
  );
  const readURL = () =>
    parseTags(new URL(window.location.href).searchParams, selectableTags);
  let selectedTags = readURL();

  function render() {
    const activeTags = mergeTags(fixedTags, selectedTags);
    for (const button of buttons) {
      const isActive = hasTag(activeTags, button);
      button.element.classList.toggle("active", isActive);
      button.element.setAttribute("aria-pressed", isActive);
    }
    let visibleCount = 0;
    for (const item of items) {
      const isVisible = matchesTags(item.tags, activeTags);
      item.element.hidden = !isVisible;
      visibleCount += isVisible ? 1 : 0;
      for (const tag of item.tags) {
        tag.element.classList.toggle("matching", hasTag(activeTags, tag));
      }
    }
    if (empty) {
      empty.hidden = activeTags.size === 0 || visibleCount > 0;
    }
  }

  for (const button of buttons) {
    if (button.element.disabled) continue;
    button.element.addEventListener("click", () => {
      selectedTags = toggleTag(selectedTags, button);
      const url = new URL(window.location.href);
      url.search = formatTags(url.searchParams, selectableTags, selectedTags);
      window.history.pushState({}, "", url);
      render();
    });
    button.element.hidden = false;
  }
  window.addEventListener("popstate", () => {
    selectedTags = readURL();
    render();
  });
  render();

  container.classList.remove("noscript");
  document
    .querySelectorAll(`.${prefix}-noscript`)
    .forEach((element) => element.remove());
}

/**
 * Creates a mapping of tag types to sets of tag slugs from a list of tags
 */
export function createTags(tags) {
  const result = new Map();
  for (const { type, slug } of tags) {
    result.set(type, new Set(result.get(type)).add(slug));
  }
  return result;
}

/**
 * Reads tags from URL search params, ignoring any tags not known in advance
 */
export function parseTags(searchParams, knownTags) {
  const result = new Map();
  for (const [type, knownSlugs] of knownTags) {
    const slugs = (searchParams.get(type)?.split("|") ?? []).filter((slug) =>
      knownSlugs.has(slug),
    );
    if (slugs.length > 0) {
      result.set(type, new Set(slugs));
    }
  }
  return result;
}

/**
 * Writes tags to URL search params, replacing any previous tags of known types
 *
 * Types are in the order of the known tags and tags are sorted, so that
 * the same filter always has the same URL.
 */
export function formatTags(searchParams, knownTags, tags) {
  const result = new URLSearchParams(searchParams);
  for (const type of knownTags.keys()) {
    result.delete(type);
  }
  for (const type of knownTags.keys()) {
    if (tags.has(type)) {
      result.set(type, Array.from(tags.get(type)).sort().join("|"));
    }
  }
  return result.toString();
}

/**
 * Returns new tags with the given tag added if missing, or removed if present
 */
export function toggleTag(tags, { type, slug }) {
  const result = new Map(tags);
  const slugs = new Set(tags.get(type));
  if (slugs.has(slug)) {
    slugs.delete(slug);
  } else {
    slugs.add(slug);
  }
  if (slugs.size > 0) {
    result.set(type, slugs);
  } else {
    result.delete(type);
  }
  return result;
}

export function mergeTags(...tagsList) {
  const result = new Map();
  for (const tags of tagsList) {
    for (const [type, slugs] of tags) {
      result.set(type, new Set([...(result.get(type) ?? []), ...slugs]));
    }
  }
  return result;
}

export function hasTag(tags, { type, slug }) {
  return tags.get(type)?.has(slug) ?? false;
}

/**
 * Checks whether an item with given tags matches the active tags
 *
 * For each type of the active tags, the item must have at least one of them.
 */
export function matchesTags(itemTags, activeTags) {
  return Array.from(activeTags).every(([type, slugs]) =>
    itemTags.some((tag) => tag.type === type && slugs.has(tag.slug)),
  );
}
