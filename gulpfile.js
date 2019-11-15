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


async function buildJS() {
  const bundle = await rollup({
    input: './juniorguru/web/static/src/js/main.js',
    plugins: [resolve(), terser()],
  });
  return bundle.write({
    file: './juniorguru/web/static/bundle.js',
    format: 'iife',
    sourceMap: isLocalDevelopment,
  });
}

function buildCSS() {
  return gulp.src('./juniorguru/web/static/src/css/*.*ss')
    .pipe(gulpIf(isLocalDevelopment, sourcemaps.init()))
    .pipe(sass().on('error', sass.logError))
    .pipe(csso())
    .pipe(gulpIf(isLocalDevelopment, sourcemaps.write()))
    .pipe(concat('bundle.css'))
    .pipe(gulp.dest('./juniorguru/web/static/'));
}

function buildImages() {
  return gulp.src([
      './juniorguru/web/static/src/images/**/*.png',
      './juniorguru/web/static/src/images/**/*.jpg',
      './juniorguru/web/static/src/images/**/*.gif',
      './juniorguru/web/static/src/images/**/*.svg',
    ])
    .pipe(changed('./juniorguru/web/static/images/'))
    .pipe(gulpIf(!isLocalDevelopment, imagemin({ verbose: true })))
    .pipe(gulp.dest('./juniorguru/web/static/images/'))
}

function freezeFlask() {
  return spawn('pipenv', ['run', 'freeze'], { stdio: 'inherit' });
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
  return gulp.src('./juniorguru/web/static/src/images/favicon.ico')
    .pipe(gulp.dest('./build/'))
}

const buildWeb = gulp.series(
  freezeFlask,
  gulp.parallel(minifyHTML, copyFavicon),
)

async function watchWeb() {
  gulp.watch('./juniorguru/web/static/src/js/', buildJS);
  gulp.watch('./juniorguru/web/static/src/css/', buildCSS);
  gulp.watch('./juniorguru/web/static/src/images/', buildImages);
  gulp.watch([
    './juniorguru/web/**/*.html',
    './juniorguru/web/**/*.py',
    './juniorguru/web/static/bundle.*',
    './juniorguru/web/static/images/',
    './juniorguru/data/',
  ], buildWeb);
}

async function serveWeb() {
  connect.server({ root: './build/', port: 5000, livereload: true });
  gulp.watch('./build/').on('change', (path) =>
    gulp.src(path, { read: false }).pipe(connect.reload())
  );
}


const build = gulp.series(
  gulp.parallel(buildJS, buildCSS, buildImages),
  buildWeb,
);

const serve = gulp.series(
  build,
  gulp.parallel(watchWeb, serveWeb),
);


module.exports = { default: build, build, serve };
