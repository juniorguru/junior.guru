const Pageres = require('pageres');

const url = process.argv[2];
const size = '1366x768'; // pageres-cli defaults to this
const script = `
const img = document.createElement('img');
img.classList.add('juniorguru-cover-image')
img.src = document.querySelector('[aria-label*="cover" i]').querySelector('img').src;
img.style.position = 'absolute';
img.style.top = 0;
img.style.left = 0;
img.style.zIndex = 9999;
document.body.appendChild(img);
`;

const pageres = new Pageres({
  delay: 2,
  filename: '<%= url %>',
  crop: true,
  overwrite: true,
  format: 'jpg',
  script: script,
  selector: '.juniorguru-cover-image',
});

(async () => {
	await pageres.src(url, [size]).dest(process.cwd()).run();
})();
