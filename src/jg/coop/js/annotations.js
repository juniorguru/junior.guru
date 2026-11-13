import { annotate } from "rough-notation";

const COLOR = "#1755d1";

function setupAnnotations() {
  document.querySelectorAll(".masthead .lead strong").forEach((element) => {
    annotate(element, {
      type: "underline",
      color: COLOR,
      multiline: true,
      animationDuration: 1600,
    }).show();
  });

  const annotations = new Map();
  const observer = new IntersectionObserver(
    (entries) => {
      entries
        .filter((entry) => entry.isIntersecting)
        .forEach((entry) => {
          observer.unobserve(entry.target);
          annotations.get(entry.target).show();
        });
    },
    { threshold: [1] },
  );
  document.querySelectorAll("[data-annotate-circle]").forEach((element) => {
    const annotation = annotate(element, {
      type: "circle",
      color: COLOR,
      padding: 20,
      animationDuration: 1600,
    });
    annotations.set(element, annotation);
    observer.observe(element);
  });
}

document.addEventListener("DOMContentLoaded", setupAnnotations);
