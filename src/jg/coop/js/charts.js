import Chart from "chart.js/auto";
import annotationPlugin from "chartjs-plugin-annotation";

const PARTIAL_DASH = [4, 4];

const PARTIAL_ALPHA = 0.4;

const PARTIAL_LABEL = "neúplný měsíc";

const DEFAULT_OPTIONS = {
  locale: "cs",
  scales: { x: {}, y: {} },
  plugins: { annotation: { annotations: {} } },
};

Chart.register(annotationPlugin);

function setupChart(canvas) {
  const context = canvas.getContext("2d");
  const type = canvas.dataset.chartType;
  let data = JSON.parse(canvas.dataset.chart);
  const options = mergeOptions(
    DEFAULT_OPTIONS,
    JSON.parse(canvas.dataset.chartOptions ?? "{}"),
  );

  if (canvas.dataset.chartPartialLast !== undefined) {
    data = markPartialLast(data, type);
    options.plugins.tooltip = {
      ...options.plugins.tooltip,
      callbacks: {
        ...options.plugins.tooltip?.callbacks,
        title: (items) => partialTitle(items, data.labels.length - 1),
      },
    };
  }

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
 * Marks the last value of each dataset as partial, e.g. the month in progress
 *
 * Lines get the last segment dashed, bars get the last bar faded.
 * Returns new data, the original stays untouched.
 */
export function markPartialLast(data, type) {
  const lastIndex = data.labels.length - 1;
  return {
    ...data,
    datasets: data.datasets.map((dataset) => {
      if ((dataset.type ?? type) === "bar") {
        const color = dataset.backgroundColor;
        return {
          ...dataset,
          backgroundColor: (ctx) =>
            ctx.dataIndex === lastIndex
              ? fadeColor(color, PARTIAL_ALPHA)
              : color,
        };
      }
      return {
        ...dataset,
        segment: {
          ...dataset.segment,
          borderDash: (ctx) =>
            ctx.p1DataIndex === lastIndex ? PARTIAL_DASH : undefined,
        },
      };
    }),
  };
}

/**
 * Builds tooltip title, noting when the hovered value is partial
 */
export function partialTitle(items, lastIndex) {
  if (items.length === 0) {
    return "";
  }
  const { label, dataIndex } = items[0];
  return dataIndex === lastIndex ? `${label} (${PARTIAL_LABEL})` : label;
}

/**
 * Turns a hex color into rgba() with given opacity
 *
 * Other color formats are returned as they are.
 */
export function fadeColor(color, alpha) {
  const match = /^#([0-9a-f]{6})$/i.exec(color ?? "");
  if (!match) {
    return color;
  }
  const number = parseInt(match[1], 16);
  const [r, g, b] = [number >> 16, (number >> 8) & 255, number & 255];
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
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
