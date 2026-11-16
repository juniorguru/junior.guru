const UTM_PARAM_NAMES = [
  "utm_source",
  "utm_medium",
  "utm_campaign",
  "utm_term",
  "utm_content",
];

const STORAGE_KEY = "utm-params";

const CHECKOUT_LINKS_SELECTOR =
  'a[href^="https://juniorguru.memberful.com/checkout"]';

function setupCheckoutUtm() {
  const utmParams = rememberUtmParams(
    new URLSearchParams(window.location.search),
  );
  if (!utmParams) return;
  document.querySelectorAll(CHECKOUT_LINKS_SELECTOR).forEach((link) => {
    link.href = addUtmParams(link.href, utmParams);
  });
}

/**
 * Stores UTM params from the current URL, or loads the ones stored earlier in this tab
 */
function rememberUtmParams(searchParams) {
  try {
    const utmParams = getUtmParams(searchParams);
    if (utmParams) {
      window.sessionStorage.setItem(STORAGE_KEY, JSON.stringify(utmParams));
      return utmParams;
    }
    return JSON.parse(window.sessionStorage.getItem(STORAGE_KEY));
  } catch {
    return getUtmParams(searchParams);
  }
}

/**
 * Picks UTM params from the URL, returns null if there's no utm_source
 *
 * Without utm_source the campaign can't be attributed, so the rest is ignored.
 */
export function getUtmParams(searchParams) {
  if (!searchParams.get("utm_source")) return null;
  return Object.fromEntries(
    UTM_PARAM_NAMES.filter((name) => searchParams.get(name)).map((name) => [
      name,
      searchParams.get(name),
    ]),
  );
}

/**
 * Adds UTM params to the URL, overwriting any it already has
 */
export function addUtmParams(href, utmParams) {
  const url = new URL(href);
  UTM_PARAM_NAMES.forEach((name) => url.searchParams.delete(name));
  Object.entries(utmParams).forEach(([name, value]) =>
    url.searchParams.set(name, value),
  );
  return url.toString();
}

document.addEventListener("DOMContentLoaded", setupCheckoutUtm);
