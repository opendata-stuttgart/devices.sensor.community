require('es6-promise').polyfill();

// Defining base pathes
var basePaths = {
  packages: './node_modules/',
  temp: './tmp/',
  target: './static/',
  assets: './assets/'
};

// requirements
var gulp = require('gulp');
var concat = require('gulp-concat');
var cssnano = require('gulp-cssnano');
var googleWebFonts = require('gulp-google-webfonts');
var plumber = require('gulp-plumber');
var rename = require('gulp-rename');
var replace = require('gulp-replace');
var rimraf = require('gulp-rimraf');
var sass = require('gulp-sass');
var uglify = require('gulp-uglify');
var watch = require('gulp-watch');

// gulp clean
gulp.task('clean', function() {
  gulp.src(basePaths.temp, { read: false })
    .pipe(rimraf());
});

// gulp watch
gulp.task('watch', function () {
  // JS
  gulp.watch(basePaths.assets + 'js/*.js', function(){ gulp.run('copy-assets-webapp-js', 'concat-js' ); });
  // CSS
  gulp.watch(basePaths.assets + 'sass/*.scss', function(){ gulp.run('copy-assets-webapp-css', 'sass', 'concat-css' ); });
});

// gulp sass
gulp.task('sass', function () {
  gulp.src(basePaths.temp + 'sass/*.scss')
    .pipe(plumber())
    .pipe(sass({noCache: true}))
    .pipe(gulp.dest(basePaths.temp + 'css/'));
});

// gulp concat-css
gulp.task('concat-css', function() {
  return gulp.src(basePaths.temp + 'css/base.css')
    .pipe(plumber())
    .pipe(rename({suffix: '.min'}))
    .pipe(cssnano({discardComments: {removeAll: true}})) // comment out for devel
    .pipe(concat('webapp.min.css'))
    .pipe(gulp.dest(basePaths.target + 'css/'));
});

// helper cleancss
gulp.task('cleancss', function() {
  return gulp.src(basePaths.temp + 'css/*.min.css', { read: false })
    .pipe(rimraf());
});

// gulp scripts
gulp.task('concat-js', function() {
  gulp.src([
    basePaths.temp + 'js/jquery/jquery.js',
    basePaths.temp + 'js/tether/tether.js',
    basePaths.temp + 'js/bootstrap/bootstrap.js',
    basePaths.temp + 'js/mapbox-gl/mapbox-gl-dev.js',
    basePaths.temp + 'js/bootstrap-multiselect/bootstrap-multiselect.js',
    basePaths.temp + 'js/bootstrap-multiselect/bootstrap-multiselect-collapsible-groups.js',
    basePaths.temp + 'js/webapp/webapp.js'
  ])
  .pipe(concat('webapp.min.js'))
  .pipe(uglify()) // comment out for devel
  .pipe(gulp.dest(basePaths.target + './js/'));
});

// helper cleanjs
gulp.task('cleanjs', function() {
  return gulp.src(basePaths.temp + 'js/**/*.min.js', { read: false }) 
    .pipe(rimraf());
});


gulp.task('copy-assets', function() {

  /********** JS **********/
  // jQuery
  gulp.src(basePaths.packages + 'jquery/dist/*.js')
    .pipe(gulp.dest(basePaths.temp + 'js/jquery'));
  
  // Tether
  gulp.src(basePaths.packages + 'tether/dist/js/tether.js')
    .pipe(gulp.dest(basePaths.temp + 'js/tether'));
  
  // Bootstrap
  gulp.src(basePaths.packages + 'bootstrap/dist/js/bootstrap.js')
    .pipe(gulp.dest(basePaths.temp + 'js/bootstrap'));
  
  // Bootstrap Multiselect
  gulp.src(basePaths.packages + 'bootstrap-multiselect/dist/js/*.js')
    .pipe(gulp.dest(basePaths.temp + 'js/bootstrap-multiselect'));
  
  // Mapbox GL
  gulp.src(basePaths.packages + 'mapbox-gl/dist/mapbox-gl-dev.js')
    .pipe(gulp.dest(basePaths.temp + 'js/mapbox-gl'));
  
  // LiveSearch
  gulp.src(basePaths.assets + 'js/livesearch.js')
    .pipe(gulp.dest(basePaths.temp + 'js/livesearch/'));
		
  // Own JS Assets
  gulp.src(basePaths.assets + 'js/webapp.js')
    .pipe(gulp.dest(basePaths.temp + 'js/webapp/'));

  /********** SASS **********/
  
  // Base
  gulp.src(basePaths.assets + 'base/base.scss')
    .pipe(gulp.dest(basePaths.temp + 'sass/'));
  
  // Normalize
  gulp.src(basePaths.packages + 'normalize.css/normalize.css')
    .pipe(rename('normalize.scss'))
    .pipe(gulp.dest(basePaths.temp + 'sass/normalize.css/'));
  
  // Tether
  gulp.src(basePaths.packages + 'tether/dist/css/tether.css')
    .pipe(rename('tether.scss'))
    .pipe(gulp.dest(basePaths.temp + 'sass/tether/'));
  
  // Bootstrap
  gulp.src(basePaths.packages + 'bootstrap/scss/**/*.scss')
    .pipe(gulp.dest(basePaths.temp + 'sass/bootstrap/'));
  
  // Bootstrap Multiselect
  gulp.src(basePaths.packages + 'bootstrap-multiselect/dist/css/bootstrap-multiselect.css')
    .pipe(rename('bootstrap-multiselect.scss'))
    .pipe(gulp.dest(basePaths.temp + 'sass/bootstrap-multiselect/'));
  
  // Font Awesome
  gulp.src(basePaths.packages + 'font-awesome/scss/*.scss')
    .pipe(gulp.dest(basePaths.temp + 'sass/font-awesome/'));

  // Mapbox GL
  gulp.src(basePaths.packages + 'mapbox-gl/dist/mapbox-gl.css')
    .pipe(rename('mapbox-gl.scss'))
    .pipe(gulp.dest(basePaths.temp + 'sass/mapbox-gl'));
  
  // Own CSS Assets
  gulp.src(basePaths.assets + 'sass/**/*.scss')
    .pipe(gulp.dest(basePaths.temp + 'sass/webapp/'));
  
  
  /********** Fonts **********/
  
  // Google Fonts
  gulp.src(basePaths.assets + 'fonts.list')
		.pipe(googleWebFonts({
      fontsDir: basePaths.target + 'fonts/google-fonts/',
      cssDir: basePaths.temp + 'pre-sass/google-fonts/',
      cssFilename: 'google-fonts.scss'
    }))
		.pipe(gulp.dest('./'));
  
  gulp.src(basePaths.temp + 'pre-sass/google-fonts/google-fonts.scss')
    .pipe(replace('webapp', ''))
    .pipe(gulp.dest(basePaths.temp + 'sass/google-fonts/'));
    
  // Font Awesome Fonts
  gulp.src(basePaths.packages + 'font-awesome/fonts/**/*.{ttf,woff,woff2,eof,svg}')
    .pipe(gulp.dest(basePaths.target + 'fonts/font-awesome/'));

    
  /********** Images **********/
  // Mapbox Images
  gulp.src(basePaths.packages + 'mapbox.js/images/*')
    .pipe(gulp.dest(basePaths.target + 'images/mapbox.js/'));
});

gulp.task('copy-assets-webapp-css', [], function() {
  gulp.src(basePaths.assets + 'sass/**/*.scss')
    .pipe(gulp.dest(basePaths.temp + 'sass/webapp/'));
});

gulp.task('copy-assets-webapp-js', function() {
  // Own JS Assets
  return gulp.src(basePaths.assets + 'js/webapp.js')
    .pipe(gulp.dest(basePaths.temp + 'js/webapp/'));
});