'use strict';


const gulp = require('gulp');
const fs = require('fs-extra');



const srcpath = '/opt/app-root/src/wp-content';
const dstpath = '/silo/wordpress';

// Async/Await:
async function moverwpcontent (srcpath,dstpath) {
  try {
    await fs.copy( srcpath, dstpath, {overwrite: true});
    console.log('success!');
  } catch (err) {
    console.error(err);
  }
}
 

async function crearlinkwpcontent (srcpath, dstpath) {
  try {
    await fs.ensureSymlink(srcpath, dstpath);
    console.log('success!');
  } catch (err) {
    console.error(err);
  }
}

gulp.task('mover', function() {
  gulp.series('moverwpcontent', 'crearlinkwpcontent');
  
});

gulp.task('watch',  function() {
  gulp.watch('/opt/app-root/src/wp-content',gulp.series('moverwpcontent', 'crearlinkwpcontent'));
});

gulp.task('default',  gulp.parallel('mover', 'watch'));
