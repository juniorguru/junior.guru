const STORAGE_KEY = "jg-theme"
const THEME_CYCLE = ["auto", "light", "dark"]

const ICONS = {
  auto: "circle-half",
  light: "sun-fill",
  dark: "moon-fill",
}

const LABELS = {
  auto: "Motiv: automaticky",
  light: "Motiv: světlý",
  dark: "Motiv: tmavý",
}

function getStoredPreference() {
  try {
    return localStorage.getItem(STORAGE_KEY) || "auto"
  } catch {
    return "auto"
  }
}

function setStoredPreference(preference) {
  try {
    localStorage.setItem(STORAGE_KEY, preference)
  } catch {
    // localStorage unavailable (private browsing)
  }
}

function getSystemPreference() {
  return window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light"
}

function getEffectiveTheme(preference) {
  if (preference === "light" || preference === "dark") {
    return preference
  }
  return getSystemPreference()
}

function applyTheme(preference) {
  const theme = getEffectiveTheme(preference)
  document.documentElement.setAttribute("data-bs-theme", theme)
  updateToggleUI(preference)
}

function updateToggleUI(preference) {
  const toggles = document.querySelectorAll(".theme-toggle")
  if (!toggles.length) return

  toggles.forEach((toggle) => {
    const icon = toggle.querySelector("i")
    if (icon) {
      icon.className = `bi bi-${ICONS[preference]}`
    }
    toggle.setAttribute("aria-label", LABELS[preference])
    toggle.setAttribute("title", LABELS[preference])
  })
}

function cycleTheme() {
  const current = getStoredPreference()
  const currentIndex = THEME_CYCLE.indexOf(current)
  const nextIndex = (currentIndex + 1) % THEME_CYCLE.length
  const next = THEME_CYCLE[nextIndex]

  setStoredPreference(next)
  applyTheme(next)
}

function setupThemeToggle() {
  const toggles = document.querySelectorAll(".theme-toggle")
  if (!toggles.length) return

  // Initial UI update
  updateToggleUI(getStoredPreference())

  // Click handlers
  toggles.forEach((toggle) => {
    toggle.addEventListener("click", cycleTheme)
  })

  // Listen for system preference changes (only affects 'auto' mode)
  window
    .matchMedia("(prefers-color-scheme: dark)")
    .addEventListener("change", () => {
      if (getStoredPreference() === "auto") {
        applyTheme("auto")
      }
    })

  // Cross-tab synchronization
  window.addEventListener("storage", (event) => {
    if (event.key === STORAGE_KEY) {
      applyTheme(event.newValue || "auto")
    }
  })
}

document.addEventListener("DOMContentLoaded", setupThemeToggle)
