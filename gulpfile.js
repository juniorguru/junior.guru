const gulp = require('gulp');
const concat = require('gulp-concat');
const sass = require('gulp-sass');
const csso = require('gulp-csso');
const imagemin = require('gulp-imagemin');
const gulpIf = require('gulp-if');
const changed = require('gulp-changed');
const sourcemaps = require('gulp-sourcemaps');
const htmlmin = require('gulp-html-minifier');
const connect = require('gulp-connect');
const { rollup } = require('rollup');
const resolve = require('rollup-plugin-node-resolve');
const { terser } = require('rollup-plugin-terser');
const { spawn } = require('child_process');

sass.compiler = require('node-sass');


const isLocalDevelopment = process.argv[2] === 'serve';


function freezeFlask() {
  return spawn('pipenv', ['run', 'freeze']);
}

function minifyHTML() {
  return gulp.src('./build/**/*.html')
    .pipe(htmlmin({
      minifyCSS: true,
      minifyJS: true,
      removeComments: true,
      removeAttributeQuotes: true,
      removeEmptyAttributes: true,
      removeOptionalTags: true,
      removeRedundantAttributes: true,
      useShortDoctype: true,
      collapseWhitespace: true,
      collapseBooleanAttributes: true,
      caseSensitive: true,
    }))
    .pipe(gulp.dest('./build/'));
}

function copyFavicon() {
  return gulp.src('./juniorguru/static/src/images/favicon.ico')
    .pipe(gulp.dest('./build/'))
}

const buildWeb = gulp.series(
  freezeFlask,
  gulp.parallel(minifyHTML, copyFavicon),
)

function watchWeb() {
  return gulp.watch([
    './juniorguru/**/*.html',
    './juniorguru/**/*.py',
    './juniorguru/**/*.json',
    './data/**/*',
  ], buildWeb);
}

function serveWeb(callback) {
  connect.server({ root: './build/', port: 5000, livereload: true });
  gulp.watch('./build/').on('change', (path) =>
    gulp.src(path, { read: false }).pipe(connect.reload())
  );
  callback();
}

async function buildJS() {
  const bundle = await rollup({
    input: './juniorguru/static/src/js/main.js',
    plugins: [resolve(), terser()],
  });
  return bundle.write({
    file: './juniorguru/static/bundle.js',
    format: 'iife',
    sourceMap: isLocalDevelopment,
  });
}

function watchJS() {
  return gulp.watch('./juniorguru/static/src/js/*.js', buildJS);
}

function buildCSS() {
  return gulp.src('./juniorguru/static/src/css/*.*css')
    .pipe(gulpIf(isLocalDevelopment, sourcemaps.init()))
    .pipe(sass().on('error', sass.logError))
    .pipe(csso())
    .pipe(gulpIf(isLocalDevelopment, sourcemaps.write()))
    .pipe(concat('bundle.css'))
    .pipe(gulp.dest('./juniorguru/static/'));
}

function watchCSS() {
  return gulp.watch('./juniorguru/static/src/css/*.*css', buildCSS);
}

function buildImages() {
  return gulp.src([
      './juniorguru/static/src/images/**/*.png',
      './juniorguru/static/src/images/**/*.jpg',
      './juniorguru/static/src/images/**/*.gif',
      './juniorguru/static/src/images/**/*.svg',
    ])
    .pipe(changed('./juniorguru/static/images/'))
    .pipe(gulpIf(!isLocalDevelopment, imagemin({ verbose: true })))
    .pipe(gulp.dest('./juniorguru/static/images/'))
}

function watchImages() {
  return gulp.watch([
    './juniorguru/static/src/images/**/*.png',
    './juniorguru/static/src/images/**/*.jpg',
    './juniorguru/static/src/images/**/*.gif',
    './juniorguru/static/src/images/**/*.svg',
  ], buildImages);
}


const build = gulp.series(
  gulp.parallel(
    buildJS,
    buildCSS,
    buildImages,
  ),
  buildWeb,
);

const serve = gulp.series(
  build,
  gulp.parallel(
    watchJS,
    watchCSS,
    watchImages,
    watchWeb,
    serveWeb,
  )
);


module.exports = { default: build, build, serve };
