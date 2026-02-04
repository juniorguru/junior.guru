import * as popperjs from "@popperjs/core";
import * as bootstrap from "bootstrap";

function setupCandidatesTags() {
  const container = document.querySelector(".candidates-filters");
  if (container) {
    container
      .querySelectorAll(".candidates-tag:not(.disabled)")
      .forEach(function (tag) {
        tag.addEventListener("click", function () {
          tag.classList.toggle("active");
          filterCandidates();
        });
        showElement(tag);
      });
    updateCandidatesTagsUI();
    container.classList.remove("noscript");
  }
  document
    .querySelectorAll(".candidates-noscript")
    .forEach(function (noscript) {
      noscript.remove();
    });
}

function setupCandidates() {
  const badges = document.querySelectorAll(".candidates-badge[title]");
  [...badges].map((badge) => new bootstrap.Tooltip(badge));

  document
    .querySelectorAll(".candidates-item.openable")
    .forEach(function (candidate) {
      candidate.classList.remove("open");

      const titleLink = candidate.querySelector(".candidates-title-link");
      const close = candidate.querySelector(".candidates-close");

      const inside = [close].concat(
        Array.from(
          candidate.querySelectorAll(
            ".candidates-title-text, .candidates-actions, .candidates-details, .candidates-action-email, .candidates-projects",
          ),
        ),
      );
      const outside = [titleLink].concat(
        Array.from(candidate.querySelectorAll(".candidates-open")),
      );

      titleLink.addEventListener("click", function (event) {
        event.preventDefault();
        candidate.classList.add("open");
        inside.forEach(showElement);
        outside.forEach(hideElement);
      });

      close.addEventListener("click", function () {
        candidate.classList.remove("open");
        inside.forEach(hideElement);
        outside.forEach(showElement);
      });
    });

  const subscribe = document.querySelector(".candidates-subscribe");
  if (subscribe) {
    subscribe.addEventListener("click", function () {
      hideElement(subscribe);
    });
  }
}

function filterCandidates() {
  const activeTags = Array.from(
    document.querySelectorAll(".candidates-filters .candidates-tag.active"),
  );
  const activeTagsByType = activeTags.reduce((mapping, tag) => {
    mapping[tag.dataset.candidatesTagType] ||= [];
    mapping[tag.dataset.candidatesTagType].push(tag.dataset.candidatesTag);
    return mapping;
  }, {});
  Object.values(activeTagsByType).forEach((tags) => tags.sort());

  const url = new URL(window.location.href);
  Array.from(url.searchParams.keys()).forEach((type) =>
    url.searchParams.delete(type),
  );
  Object.entries(activeTagsByType).forEach(([type, tags]) => {
    if (tags.length === 0) {
      return;
    }
    url.searchParams.set(type, tags.join("|"));
  });
  window.history.pushState({}, "", url);

  const candidates = Array.from(
    document.querySelectorAll(".candidates-item.tagged"),
  );
  const allCandidateTags = Array.from(
    document.querySelectorAll(".candidates-item.tagged .candidates-tag"),
  );

  if (Object.keys(activeTagsByType).length === 0) {
    candidates.forEach(showElement);
    allCandidateTags.forEach((tag) => tag.classList.remove("matching"));
    return;
  }

  allCandidateTags.forEach((tag) => {
    if (
      activeTagsByType[tag.dataset.candidatesTagType]?.includes(
        tag.dataset.candidatesTag,
      )
    ) {
      tag.classList.add("matching");
    } else {
      tag.classList.remove("matching");
    }
  });

  const count = candidates
    .map((candidate) => {
      const candidateTags = Array.from(
        candidate.querySelectorAll(".candidates-tag"),
      );
      const candidateSlugs = candidateTags.map(
        (tag) => tag.dataset.candidatesTag,
      );
      const isRelevant = Object.entries(activeTagsByType).every(
        ([type, tags]) => tags.some((tag) => candidateSlugs.includes(tag)),
      );
      if (isRelevant) {
        showElement(candidate);
        return 1;
      }
      hideElement(candidate);
      return 0;
    })
    .reduce((a, b) => a + b, 0);

  const empty = document.querySelector(".candidates-empty");
  if (count === 0) {
    showElement(empty);
  } else {
    hideElement(empty);
  }
}

function updateCandidatesTagsUI() {
  const url = new URL(window.location.href);
  const activeSlugsByType = Array.from(url.searchParams.keys()).reduce(
    (mapping, type) => {
      mapping[type] = url.searchParams.get(type).split("|");
      return mapping;
    },
    { location: [] },
  );
  const container = document.querySelector(".candidates-filters");
  container.querySelectorAll(".candidates-tag").forEach((tag) => {
    const activeSlugs = activeSlugsByType[tag.dataset.candidatesTagType] || [];
    const isActive = activeSlugs.includes(tag.dataset.candidatesTag);
    if (isActive) {
      tag.classList.add("active");
    } else {
      tag.classList.remove("active");
    }
  });
  filterCandidates();
}

function showElement(element) {
  element.removeAttribute("hidden");
}

function hideElement(element) {
  element.setAttribute("hidden", "");
}

document.addEventListener("DOMContentLoaded", setupCandidatesTags);
document.addEventListener("DOMContentLoaded", setupCandidates);
window.addEventListener("popstate", updateCandidatesTagsUI);
