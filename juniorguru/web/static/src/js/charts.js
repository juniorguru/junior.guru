import Chart from 'chart.js/auto';
import annotationPlugin from 'chartjs-plugin-annotation';

const DEFAULT_OPTIONS = {
  locale: 'cs',
};

Chart.register(annotationPlugin);

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.chart').forEach((canvas) => {
    new Chart(canvas.getContext('2d'), {
      type: canvas.dataset.chartType,
      data: JSON.parse(canvas.dataset.chart),
      options: {
        ...DEFAULT_OPTIONS,
        ...(canvas.dataset.chartOptions ? JSON.parse(canvas.dataset.chartOptions) : {}),
      }
    });
  });
});
