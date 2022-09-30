const gulp = require('gulp');
const concat = require('gulp-concat');
const sass = require('gulp-dart-sass');
const csso = require('gulp-csso');
const imagemin = require('gulp-imagemin');
const gulpIf = require('gulp-if');
const rename = require('gulp-rename');
const changed = require('gulp-changed');
const sourcemaps = require('gulp-sourcemaps');
const resizer = require('gulp-images-resizer');
const connect = require('gulp-connect');
const purgecss = require('gulp-purgecss');
const { rollup } = require('rollup');
const resolve = require('rollup-plugin-node-resolve');
const { terser } = require('rollup-plugin-terser');
const del = require('del');
const { spawn } = require('child_process');


const isLocalDevelopment = process.argv[2] === 'serve';


function cleanStatic() {
  return del([
    'juniorguru/web/static/**/*',
    '!juniorguru/web/static/src',
  ]);
}


async function buildJS() {
  const bundle = await rollup({
    input: 'juniorguru/web/static/src/js/index.js',
    plugins: [resolve(), terser()],
  });
  return bundle.write({
    file: 'juniorguru/web/static/bundle.js',
    format: 'iife',
    sourcemap: isLocalDevelopment,
  });
}

const buildCSS = gulp.parallel(buildFlaskCSS, copyIconFont, buildMkDocsCSS)

function copyIconFont() {
  return gulp.src('node_modules/bootstrap-icons/font/fonts/*.*')
    .pipe(rename({ dirname: 'fonts' }))
    .pipe(gulp.dest('juniorguru/web/static/'))
}

function buildFlaskCSS() {
  return gulp.src('juniorguru/web/static/src/css/index.scss')
    .pipe(gulpIf(isLocalDevelopment, sourcemaps.init()))
    .pipe(sass().on('error', sass.logError))
    .pipe(gulpIf(isLocalDevelopment, sourcemaps.write()))
    .pipe(concat('bundle.css'))
    .pipe(gulp.dest('juniorguru/web/static/'));
}

function buildMkDocsCSS() {
  return gulp.src('juniorguru/scss/index.scss')
    .pipe(gulpIf(isLocalDevelopment, sourcemaps.init()))
    .pipe(sass().on('error', sass.logError))
    .pipe(gulpIf(isLocalDevelopment, sourcemaps.write()))
    .pipe(concat('bundle-mkdocs.css'))
    .pipe(gulp.dest('juniorguru/web/static/'));
}

function minifyCSS() {
  return gulp.src('public/static/*.css')
  .pipe(gulpIf(isLocalDevelopment, sourcemaps.init()))
    .pipe(purgecss({
      content: ['public/**/*.html', 'public/**/*.js'],
      fontFace: true,
      keyframes: true,
      variables: true,
    }))
    .pipe(csso())
    .pipe(gulpIf(isLocalDevelopment, sourcemaps.write()))
    .pipe(gulp.dest('public/static/'));
}

function buildImages() {
  return gulp.src([
      'juniorguru/images/**/*',
      'juniorguru/web/static/src/images/**/*',
      '!juniorguru/web/static/src/images/screenshots*/**/*',
      '!juniorguru/web/static/src/images/stories/**/*'
    ])
    .pipe(changed('juniorguru/web/static/images/'))
    .pipe(gulpIf(!isLocalDevelopment, imagemin({ verbose: true })))
    .pipe(gulp.dest('juniorguru/web/static/images/'))
}

function buildStories() {
  return gulp.src('juniorguru/web/static/src/images/stories/**/*')
    .pipe(rename({ dirname: 'stories' }))
    .pipe(changed('juniorguru/web/static/images/'))
    .pipe(resizer({ width: 100, height: 100 }))
    .pipe(gulpIf(!isLocalDevelopment, imagemin({ verbose: true })))
    .pipe(gulp.dest('juniorguru/web/static/images/'))
}

function copyScreenshots() {
  return gulp.src('juniorguru/web/static/src/images/screenshots*/**/*')
    .pipe(rename({ dirname: 'screenshots' }))
    .pipe(changed('juniorguru/web/static/images/'))
    .pipe(gulp.dest('juniorguru/web/static/images/'))
}

function buildStatic() {
  // optimization, gets called when 'freezeFlask' is unnecessary overkill
  return gulp.src([
      'juniorguru/web/static/**/*.*',
      '!juniorguru/web/static/src/**',
    ])
    .pipe(changed('public/static/', { hasChanged: changed.compareContents }))
    .pipe(gulp.dest('public/static/'))
}

function freezeFlask() {
  // also does everything 'buildStatic' does
  const proc = spawn('poetry', ['run', 'inv', 'web.freeze'], { stdio: 'inherit' });
  return new Promise((resolve, reject) => {
    proc.on('exit', (code) => { code ? reject(new Error(`Exit code ${code}`)) : resolve(code); });
    proc.on('error', (error) => { reject(error); });
  });
}


function buildMkDocsFiles() {
  const proc = spawn('poetry', ['run', 'inv', 'web.mkdocs'], { stdio: 'inherit' });
  return new Promise((resolve, reject) => {
    proc.on('exit', (code) => { code ? reject(new Error(`Exit code ${code}`)) : resolve(code); });
    proc.on('error', (error) => { reject(error); });
  });
}


function overwriteWithMkDocs() {
  return gulp.src([
    'public/mkdocs/**/*',
    '!public/mkdocs/sitemap.*',
    '!public/mkdocs/search',
    '!public/mkdocs/search/**/*',
  ])
    .pipe(gulp.dest('public/'));
}


function copyThumbnailsForMkDocs() {
  return gulp.src('juniorguru/web/static/images/thumbnails/**/*')
    .pipe(changed('public/static/images/thumbnails/'))
    .pipe(gulp.dest('public/static/images/thumbnails/'))
}


function cleanMkDocsFiles() {
  return del(['public/mkdocs/']);
}


const buildMkDocs = gulp.series(
  buildMkDocsFiles,
  copyThumbnailsForMkDocs,
  overwriteWithMkDocs,
  cleanMkDocsFiles,
)


function copyFavicon() {
  return gulp.src('juniorguru/web/static/src/images/favicon.ico')
    .pipe(gulp.dest('public/'))
}

const buildWeb = isLocalDevelopment
  ? gulp.series(freezeFlask, buildMkDocs)
  : gulp.series(freezeFlask, buildMkDocs, minifyCSS, copyFavicon);

async function watchWeb() {
  gulp.watch([
    'package-lock.json',
    'juniorguru/web/static/src/js/',
  ], buildJS);
  gulp.watch([
    'juniorguru/web/static/src/css/',
    'juniorguru/scss/',
  ], buildCSS);
  gulp.watch([
    'juniorguru/web/static/src/images/screenshots/',
    'juniorguru/web/static/src/images/screenshots-overrides/',
  ], copyScreenshots);
  gulp.watch([
    'juniorguru/web/static/src/images/stories/'
  ], buildStories);
  gulp.watch([
    'juniorguru/images/',
    'juniorguru/web/static/src/images/',
    '!juniorguru/web/static/src/images/screenshots*/**/*',
    '!juniorguru/web/static/src/images/stories/**/*'
  ], buildImages);
  gulp.watch([
    'juniorguru/web/static/*.js',
    'juniorguru/web/static/*.css',
    'juniorguru/web/static/images/',
  ], buildStatic);
  gulp.watch([
    'juniorguru/web/**/*.html',
    'juniorguru/web/**/*.py',
    'juniorguru/models/**/*.py',
    'juniorguru/lib/**/*.py',
    'juniorguru/data/data.db',
    'juniorguru/data/*.yml',
    'juniorguru/mkdocs/**/*',
  ], buildWeb);
}

async function serveWeb() {
  connect.server({ root: 'public/', port: 5000, livereload: true });
  gulp.watch('public/', { delay: 100 }).on('change', (path) =>
    gulp.src(path, { read: false }).pipe(connect.reload())
  );
}


const clean = gulp.series(
  cleanStatic,
);

const build = gulp.series(
  gulp.parallel(buildJS, buildCSS, buildImages, buildStories, copyScreenshots),
  buildWeb,
);

const serve = gulp.series(
  build,
  gulp.parallel(watchWeb, serveWeb),
);


module.exports = { clean, default: build, build, serve };
