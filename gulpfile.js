require('es6-promise').polyfill();

// Defining base pathes
var basePaths = {
  packages: './node_modules/',
  target: './static/',
  assets: './assets/'
};

// requirements
var gulp = require('gulp');
var concat = require('gulp-concat');
var cssnano = require('gulp-cssnano');
var googleWebFonts = require('gulp-google-webfonts');
var rename = require('gulp-rename');
var replace = require('gulp-replace');
var rimraf = require('gulp-rimraf');
var sass = require('gulp-sass');
var uglify = require('gulp-uglify');
var watch = require('gulp-watch');

// gulp watch
gulp.task('watch', ['js', 'sass'], function () {
  // JS
  gulp.watch(basePaths.assets + 'js/*.js', ['js']);

  // CSS
  gulp.watch(basePaths.assets + 'sass/*.scss', ['sass']);
});

// gulp sass
gulp.task('sass', ['fonts'], function () {
  gulp.src([
    basePaths.packages + 'tether/dist/css/tether.css',
    basePaths.packages + 'bootstrap-multiselect/dist/css/bootstrap-multiselect.css',
    basePaths.assets + 'sass/base.scss',
  ])
  .pipe(sass({
    noCache: true,
    includePaths: ['node_modules', 'assets', 'static'],
    importer: require('node-sass-tilde-importer')
  }))
  .pipe(cssnano({discardComments: {removeAll: true}})) // comment out for devel
  .pipe(concat('webapp.min.css'))
  .pipe(gulp.dest(basePaths.target + 'css/'));
});

// gulp scripts
gulp.task('js', function() {
  gulp.src([
    basePaths.packages + 'jquery/dist/jquery.js',
    basePaths.packages + 'tether/dist/js/tether.js',
    basePaths.packages + 'bootstrap/dist/js/bootstrap.js',
    basePaths.packages + 'bootstrap-multiselect/dist/js/bootstrap-multiselect.js',
    basePaths.packages + 'bootstrap-multiselect/dist/js/bootstrap-multiselect-collapsible-groups.js',
    basePaths.assets + 'js/webapp/webapp.js'
  ])
  .pipe(concat('webapp.min.js'))
  .pipe(uglify()) // comment out for devel
  .pipe(gulp.dest(basePaths.target + './js/'));
});

gulp.task('fonts', function() {
  gulp.src(basePaths.assets + 'fonts.list')
    .pipe(googleWebFonts({
      fontsDir: basePaths.target + 'fonts/',
      cssDir: basePaths.target + 'fonts/',
      cssFilename: 'google-fonts.scss',
      relativePaths: true,
    }))
    .pipe(replace('url(static', 'url(/static'))
    .pipe(gulp.dest('./'));

  // Font Awesome Fonts
  gulp.src(basePaths.packages + 'font-awesome/fonts/**/*.{ttf,woff,woff2,eof,svg}')
    .pipe(gulp.dest(basePaths.target + 'fonts/font-awesome/'));
});
