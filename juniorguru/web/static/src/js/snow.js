import Snowflakes from 'magic-snowflakes';

document.addEventListener('DOMContentLoaded', function () {
  const snow = document.getElementById('snow');
  if (snow) {
    const snowflakes = new Snowflakes({
      color: '#fff',
      container: document.getElementById('snow'),
      count: 50,
      minSize: 5,
      maxSize: 15,
      speed: 0.5
    });
    snowflakes.start();
  }
});
