'use strict';

const gulp = require('gulp');
const json5 = require('gulp-json5-to-json');
var jsonlint = require('gulp-jsonlint');
var plumber = require('gulp-plumber');
var beeper = require('beeper');
var log = require('fancy-log');
var myCustomReporter = function (file) {
  log('File ' + file + ' is not valid JSON.');
};



// Error Helper
// function onError(err) {
//   beeper();
//   console.log(err);
// }

 
gulp.task('convertirajson', () => {
  return gulp.src('./*.json5')
    .pipe(json5({ beautify: true }))
    .pipe(gulp.dest('./build'));
  
});

//No necesario ya te lo corrige o te muestra
// gulp.task('comprobarjson', () => {
//   return gulp.src('./example_2HU.json.json')
//     .pipe(plumber({
//       errorHandler: onError
//     }))
//     .pipe(jsonlint())
//     .pipe(jsonlint.reporter(myCustomReporter))
// });



gulp.task('watch',  function(done) {
  // gulp.watch('/opt/app-root/src/wp-content',gulp.series('tmoverwpcontent'));
  // gulp.watch('/opt/app-root/src/.htcaccess',gulp.series('tmoverwphtcaccess'));
  gulp.watch('*.json5',gulp.series('convertirajson'));
  done();
});

gulp.task('default', gulp.parallel('watch'));


