import Chart from "chart.js/auto";
import annotationPlugin from "chartjs-plugin-annotation";

const DEFAULT_OPTIONS = {
  locale: "cs",
  scales: { x: {}, y: {} },
  plugins: { annotation: { annotations: {} } },
};

Chart.register(annotationPlugin);

function setupChart(canvas) {
  const context = canvas.getContext("2d");
  const type = canvas.dataset.chartType;
  const data = JSON.parse(canvas.dataset.chart);
  const options = mergeOptions(
    DEFAULT_OPTIONS,
    JSON.parse(canvas.dataset.chartOptions ?? "{}"),
  );

  Object.values(options.plugins.annotation.annotations)
    .filter((annotation) => annotation.type === "label")
    .forEach((annotation) => {
      annotation.yValue = (ctx) => ctx.chart.scales.y.max;
    });

  if (canvas.dataset.chartZeroLine !== undefined) {
    options.scales.y.grid = {
      ...options.scales.y.grid,
      color: (ctx) => (ctx.tick.value === 0 ? "#666" : "rgba(0, 0, 0, 0.1)"),
    };
  }

  const chart = new Chart(context, { type, data, options });

  const offset = parseMilestonesOffset(canvas.dataset.chartMilestonesOffsetPtc);
  if (offset) {
    chart.options.scales.y.max = chart.scales.y.max * (1 + offset);
    chart.update();
  }
}

/**
 * Deeply merges custom chart options into defaults, returning a new object
 *
 * Plain objects get merged, anything else from the custom options
 * replaces the default. The defaults get copied, so they're never shared
 * between charts and never modified.
 */
export function mergeOptions(defaults, custom) {
  const result = structuredClone(defaults);
  for (const [key, value] of Object.entries(custom)) {
    result[key] =
      isPlainObject(value) && isPlainObject(result[key])
        ? mergeOptions(result[key], value)
        : value;
  }
  return result;
}

/**
 * Parses how much space above the highest value to leave for milestones
 *
 * Takes percents as a string and returns a ratio, e.g. "20" → 0.2.
 * Defaults to 20 % if the value is missing.
 */
export function parseMilestonesOffset(value) {
  return Number(value ?? 20) / 100;
}

function isPlainObject(value) {
  return (
    typeof value === "object" &&
    value !== null &&
    Object.getPrototypeOf(value) === Object.prototype
  );
}

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".chart").forEach(setupChart);
});
