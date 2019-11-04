'use strict';


const gulp = require('gulp');
const fs = require('fs-extra');



const srcwpcontent = '/opt/app-root/src/wp-content';
const dstwpcontent = '/silo/wordpress/wp-content';
const srcwphtaccess = '/opt/app-root/src/.httaccess';
const dstwphtaccess = '/silo/wordpress/.htaccess';
const srcwpconfig = '/opt/app-root/src/wp-config.php' ;
const dstwpconfig = '/silo/wordpress/wp-config.php';

// With async/await:
async function createdirwpcontent () {
  try {
    await fs.emptyDir('/silo/wordpress,wp-content');
    console.log('success!');
  } catch (err) {
    console.error(err);
  }
}



// Async/Await:
async function moverwpcontent () {
  try {
    createdirwpcontent();
    await fs.move( srcwpcontent, dstwpcontent, {overwrite: true});
    console.log('success!');
  } catch (err) {
    console.error(err);
  }
}

// Async/Await:
async function moverwpconfig () {
  try {
    await fs.move( srcwpconfig, dstwpconfig, {overwrite: true});
    console.log('success!');
  } catch (err) {
    console.error(err);
  }
}

// Async/Await:
async function moverwphtcaccess () {
  try {
    await fs.move( srcwphtaccess, dstwphtaccess, {overwrite: true});
    console.log('success!');
  } catch (err) {
    console.error(err);
  }
}

async function crearlinkwpcontent () {
  try {
    await fs.ensureSymlink(dstwpcontent, srcwpcontent);
    console.log('success!');
  } catch (err) {
    console.error(err);
  }
}
 

async function crearlinkwpconfig () {
  try {
    await fs.ensureSymlink(dstwpconfig, srcwpconfig);
    console.log('success!');
  } catch (err) {
    console.error(err);
  }
}

async function crearlinkwphtcaccess () {
  try {
    await fs.ensureSymlink(dstwphtaccess, srcwphtaccess);
    console.log('success!');
  } catch (err) {
    console.error(err);
  }
}




gulp.task('tmoverwpcontent', function(done) {
  moverwpcontent();
  crearlinkwpcontent();
  done();
});

gulp.task('tmoverwpconfig', function(done) {
  moverwpconfig();
  crearlinkwpconfig();
  done();
});

gulp.task('tmoverwphtcaccess', function(done) {
  moverwphtcaccess();
  crearlinkwphttcacces();
  done();
});



gulp.task('watch',  function(done) {
  gulp.watch('/opt/app-root/src/wp-content',gulp.series('tmoverwpcontent');
  gulp.watch('/opt/app-root/src/.htcaccess',gulp.series('tmoverwphtcaccess'));
  gulp.watch('/opt/app-root/src/wp-config.php',gulp.series('tmoverwpconfig'));
  gulp.watch('/silo/wordpress/wp-content', 'tcrearlinkwpcontent');
  gulp.watch('/silo/wordpress/.htcaccess', 'tcrearlinkwphtcaccess');
  gulp.watch('/silo/wordpress/wp-config.php', 'tcrearlinkwpconfig');
  done();
});

gulp.task('default',  gulp.parallel('watch'));
