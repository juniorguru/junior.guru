import Chart from 'chart.js/auto';

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.chart').forEach((canvas) => {
    const context = canvas.getContext('2d');
    const chart = new Chart(context, {
      type: canvas.dataset.chartType,
      data: JSON.parse(canvas.dataset.chart),
      options: {locale: 'cs'}
    });
  });
});
