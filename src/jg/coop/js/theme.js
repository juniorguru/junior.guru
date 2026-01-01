const STORAGE_KEY = "theme";
const THEME_ATTR = "data-theme";
const THEME_TOGGLE_SELECTOR = "[data-theme-toggle]";

const prefersDark = window.matchMedia("(prefers-color-scheme: dark)");

const normalizeTheme = (value) =>
  value === "dark" || value === "light" ? value : null;

const getStoredTheme = () => {
  try {
    return normalizeTheme(localStorage.getItem(STORAGE_KEY));
  } catch (error) {
    return null;
  }
};

const setStoredTheme = (theme) => {
  try {
    localStorage.setItem(STORAGE_KEY, theme);
  } catch (error) {}
};

const getSystemTheme = () => (prefersDark.matches ? "dark" : "light");

const updateToggle = (theme) => {
  const toggle = document.querySelector(THEME_TOGGLE_SELECTOR);
  if (!toggle) {
    return;
  }

  const isDark = theme === "dark";
  toggle.setAttribute("aria-pressed", String(isDark));

  const label = isDark
    ? toggle.dataset.themeLabelLight
    : toggle.dataset.themeLabelDark;
  if (label) {
    toggle.setAttribute("aria-label", label);
  }

  toggle.dataset.themeState = theme;
};

const applyTheme = (theme) => {
  document.documentElement.setAttribute(THEME_ATTR, theme);
  updateToggle(theme);
};

const initTheme = () => {
  const stored = getStoredTheme();
  applyTheme(stored || getSystemTheme());

  if (!stored) {
    const handleChange = () => applyTheme(getSystemTheme());
    if (typeof prefersDark.addEventListener === "function") {
      prefersDark.addEventListener("change", handleChange);
    } else if (typeof prefersDark.addListener === "function") {
      prefersDark.addListener(handleChange);
    }
  }
};

const setupToggle = () => {
  const toggle = document.querySelector(THEME_TOGGLE_SELECTOR);
  if (!toggle) {
    return;
  }

  toggle.addEventListener("click", () => {
    const current =
      normalizeTheme(document.documentElement.getAttribute(THEME_ATTR)) ||
      getSystemTheme();
    const next = current === "dark" ? "light" : "dark";
    setStoredTheme(next);
    applyTheme(next);
  });
};

initTheme();
document.addEventListener("DOMContentLoaded", setupToggle);
