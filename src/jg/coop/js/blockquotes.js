function setupAnimatedBlockquotesRoll(roll) {
  const testimonials = Array.from(
    roll.querySelectorAll(":scope > .blockquote-container"),
  );

  if (testimonials.length < 2) {
    return;
  }

  const breakpoint = window.matchMedia("(min-width: 768px)");
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  const stage = document.createElement("div");
  stage.className = "blockquotes-roll-stage";

  const track = document.createElement("div");
  track.className = "blockquotes-roll-track";

  testimonials.forEach((testimonial) => {
    track.appendChild(testimonial);
  });

  stage.appendChild(track);
  roll.prepend(stage);

  const dots = document.createElement("div");
  dots.className = "blockquotes-roll-dots";
  roll.appendChild(dots);

  let isManual = false;
  let firstVisibleIndex = 0;
  let autoplayIntervalId = null;
  let transitionEndHandler = null;

  function getStepDurationMs() {
    const value = window
      .getComputedStyle(roll)
      .getPropertyValue("--blockquotes-roll-step-duration");
    return parseCssDuration(value, 4000);
  }

  function getColumnsCount() {
    return breakpoint.matches ? 2 : 1;
  }

  function updateActiveDot() {
    dots.querySelectorAll(".blockquotes-roll-dot").forEach((dot, index) => {
      const isActive =
        index === getActiveIndex(firstVisibleIndex, testimonials.length);
      dot.classList.toggle("active", isActive);
      if (isActive) {
        dot.setAttribute("aria-current", "true");
      } else {
        dot.removeAttribute("aria-current");
      }
    });
  }

  function getUnitWidth() {
    const firstItem = track.querySelector(".blockquote-container");
    const gapValue = window.getComputedStyle(track).columnGap;
    const gap = Number.parseFloat(gapValue) || 0;

    if (!firstItem) {
      return 0;
    }

    return firstItem.getBoundingClientRect().width + gap;
  }

  function clearTransitionEndHandler() {
    if (!transitionEndHandler) {
      return;
    }

    track.removeEventListener("transitionend", transitionEndHandler);
    transitionEndHandler = null;
  }

  function clearClones() {
    track
      .querySelectorAll(".blockquote-container.is-clone")
      .forEach((clone) => clone.remove());
  }

  function ensureClones() {
    clearClones();

    for (let index = 0; index < getColumnsCount(); index += 1) {
      const source = testimonials[index % testimonials.length];
      const clone = source.cloneNode(true);
      clone.classList.add("is-clone");
      track.appendChild(clone);
    }
  }

  function setTrackPosition(animated) {
    const unitWidth = getUnitWidth();
    const offset = firstVisibleIndex * unitWidth;

    clearTransitionEndHandler();

    track.classList.toggle("is-animating", animated);

    track.style.transform = `translateX(${-offset}px)`;
  }

  function updateStageHeight() {
    const maxHeight = Math.max(
      ...testimonials.map(
        (testimonial) => testimonial.getBoundingClientRect().height,
      ),
    );

    roll.style.setProperty(
      "--blockquotes-roll-stage-height",
      `${Math.ceil(maxHeight)}px`,
    );
  }

  function stopAutoplay() {
    if (autoplayIntervalId) {
      window.clearInterval(autoplayIntervalId);
      autoplayIntervalId = null;
    }
  }

  function stepForward() {
    firstVisibleIndex += 1;
    setTrackPosition(true);
    updateActiveDot();

    if (firstVisibleIndex < testimonials.length) {
      return;
    }

    transitionEndHandler = () => {
      firstVisibleIndex = 0;
      setTrackPosition(false);
      updateActiveDot();
    };
    track.addEventListener("transitionend", transitionEndHandler, {
      once: true,
    });
  }

  function startAutoplay() {
    stopAutoplay();

    if (reducedMotion.matches || isManual) {
      return;
    }

    autoplayIntervalId = window.setInterval(stepForward, getStepDurationMs());
  }

  function renderDots() {
    dots.replaceChildren();

    for (let index = 0; index < testimonials.length; index += 1) {
      const dot = document.createElement("button");
      dot.type = "button";
      dot.className = "blockquotes-roll-dot";
      dot.setAttribute("aria-label", `Zobrazit recenzi ${index + 1}`);
      dot.addEventListener("click", () => {
        isManual = true;
        stopAutoplay();
        firstVisibleIndex = index;
        setTrackPosition(true);
        updateActiveDot();
      });
      dots.appendChild(dot);
    }

    updateActiveDot();
  }

  ensureClones();
  renderDots();
  updateStageHeight();
  setTrackPosition(false);
  startAutoplay();

  breakpoint.addEventListener("change", () => {
    firstVisibleIndex = getActiveIndex(firstVisibleIndex, testimonials.length);
    ensureClones();
    updateStageHeight();
    setTrackPosition(false);
    renderDots();
    startAutoplay();
  });

  reducedMotion.addEventListener("change", startAutoplay);
  window.addEventListener(
    "resize",
    debounce(() => {
      updateStageHeight();
      setTrackPosition(false);
    }, 100),
  );
}

/**
 * Parses a CSS duration such as "4s" or "300ms" to milliseconds
 *
 * Returns the fallback if the value is empty or not a duration.
 */
export function parseCssDuration(value, fallbackMs) {
  const match = value.trim().match(/^(\d*\.?\d+)(ms|s)$/);
  if (!match) return fallbackMs;
  const number = Number.parseFloat(match[1]);
  return match[2] === "s" ? number * 1000 : number;
}

/**
 * Returns index of the testimonial being shown first
 *
 * After the last testimonial, the track shows clones of the first ones,
 * so the index can get past the number of testimonials for a moment.
 */
export function getActiveIndex(firstVisibleIndex, count) {
  return firstVisibleIndex % count;
}

/**
 * Returns a function which calls the given function only after it stops
 * being called for the given number of milliseconds
 */
export function debounce(fn, ms) {
  let timeoutId = null;
  return (...args) => {
    window.clearTimeout(timeoutId);
    timeoutId = window.setTimeout(() => fn(...args), ms);
  };
}

function setupBlockquotesRolls() {
  document
    .querySelectorAll(".blockquotes-roll.animated")
    .forEach(setupAnimatedBlockquotesRoll);
}

document.addEventListener("DOMContentLoaded", setupBlockquotesRolls);
