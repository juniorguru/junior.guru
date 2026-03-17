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

  function readCssDurationMs(variableName, fallbackMs) {
    const value = window
      .getComputedStyle(roll)
      .getPropertyValue(variableName)
      .trim();

    if (!value) {
      return fallbackMs;
    }

    if (value.endsWith("ms")) {
      return Number.parseFloat(value);
    }

    if (value.endsWith("s")) {
      return Number.parseFloat(value) * 1000;
    }

    return fallbackMs;
  }

  function getStepDurationMs() {
    return readCssDurationMs("--blockquotes-roll-step-duration", 4000);
  }

  function getColumnsCount() {
    return breakpoint.matches ? 2 : 1;
  }

  function getDotsCount() {
    return testimonials.length;
  }

  function updateActiveDot() {
    dots.querySelectorAll(".blockquotes-roll-dot").forEach((dot, index) => {
      const isActive = index === firstVisibleIndex;
      dot.classList.toggle("active", isActive);
      dot.setAttribute("aria-pressed", isActive ? "true" : "false");
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
      .forEach((clone) => {
        clone.remove();
      });
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

    if (animated) {
      track.classList.add("is-animating");
    } else {
      track.classList.remove("is-animating");
    }

    track.style.transform = `translateX(${-offset}px)`;
  }

  function updateStageHeight() {
    const maxHeight = testimonials.reduce((result, testimonial) => {
      return Math.max(result, testimonial.getBoundingClientRect().height);
    }, 0);

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
    const dotsCount = getDotsCount();

    dots.innerHTML = "";

    for (let index = 0; index < dotsCount; index += 1) {
      const dot = document.createElement("button");
      dot.type = "button";
      dot.className = "blockquotes-roll-dot";
      dot.setAttribute("aria-label", `Zobrazit recenzi ${index + 1}`);
      dot.setAttribute("aria-pressed", "false");
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
    firstVisibleIndex = firstVisibleIndex % testimonials.length;
    ensureClones();
    updateStageHeight();
    setTrackPosition(false);
    renderDots();
    startAutoplay();
  });

  reducedMotion.addEventListener("change", startAutoplay);
  window.addEventListener("resize", () => {
    updateStageHeight();
    setTrackPosition(false);
  });
}

function setupBlockquotesRolls() {
  document
    .querySelectorAll(".blockquotes-roll.animated")
    .forEach(setupAnimatedBlockquotesRoll);
}

document.addEventListener("DOMContentLoaded", setupBlockquotesRolls);
