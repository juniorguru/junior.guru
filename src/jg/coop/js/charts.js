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
  const options = {
    ...DEFAULT_OPTIONS,
    ...(canvas.dataset.chartOptions
      ? JSON.parse(canvas.dataset.chartOptions)
      : {}),
  };

  Object.values(options.plugins.annotation.annotations)
    .filter((annotation) => annotation.type == "label")
    .forEach((annotation) => {
      annotation.yValue = yValue;
    });

  const chart = new Chart(context, { type, data, options });

  const milestonesOffsetPtc =
    (canvas.dataset.chartMilestonesOffsetPtc || 20) / 100;
  if (milestonesOffsetPtc) {
    chart.options.scales.y.max =
      chart.scales.y.max + chart.scales.y.max * milestonesOffsetPtc;
  }

  chart.update();
}

function yValue(context) {
  return context.chart.scales.y.max;
}

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".chart").forEach(setupChart);
});
