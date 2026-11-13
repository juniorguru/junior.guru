function setupMetricsUtm(link) {
  try {
    link.href = addUtmParams(link.href, {
      medium: link.dataset.metricsUtmMedium,
      campaign: link.dataset.metricsUtmCampaign,
    });
  } catch (error) {
    console.error(
      "Couldn't modify link",
      link.href,
      "to contain UTM params",
      error,
    );
  }
}

/**
 * Returns the URL with UTM params added, keeping any UTM params it already has
 */
export function addUtmParams(href, { medium, campaign } = {}) {
  const url = new URL(href);
  const defaults = {
    utm_source: "juniorguru",
    utm_medium: medium || "content",
    utm_campaign: campaign || "juniorguru",
  };
  for (const [name, value] of Object.entries(defaults)) {
    if (!url.searchParams.has(name)) {
      url.searchParams.set(name, value);
    }
  }
  return url.toString();
}

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-metrics-utm]").forEach(setupMetricsUtm);
});
