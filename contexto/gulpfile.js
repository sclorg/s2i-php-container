'use strict';


const gulp = require('gulp');
const fs = require('fs-extra');



const srcwpcontent = '/opt/app-root/src/wp-content';
const dstwpcontent = '/silo/wordpress/wp-content';
const srcwphtcaccess = '/opt/app-root/src/.htcaccess';
const dstwphtcaccess = '/silo/wordpress/.htcaccess';
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
async function linkremovewpcontentwpconfightcaccess () {
  try {
    await fs.remove(srcwpcontent);
    await fs.remove(srcwpconfig);
    await fs.ensureSymlink( dstwpcontent,  srcwpcontent, 'dir');
    await fs.ensureSymlink( dstwpconfig,  srcwpconfig, 'file');
    if ( ! fs.pathExists(dstwphtcaccess)) {
      try {
        await fs.remove(srcwphtcaccess);
        await fs.ensureSymlink( dstwphtcaccess,  srcwphtcaccess, 'file');
        console.log('success!');
      } catch (err) {
        console.error(err);
      }
    } else {
      console.log("No existe el archivo ", dstwphtcaccess);
    }

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
    // await fs.remove(srcwpcontent);
    // await fs.ensureSymlink( dstwpcontent,  srcwpcontent, 'dir');
    console.log('success!');
  } catch (err) {
    console.error(err);
  }
}

// Async/Await:
async function moverwpconfig () {

  if ( ! fs.pathExists(srcwpconfig)) {
    try {
      await fs.move( srcwpconfig, dstwpconfig, {overwrite: true});
      // await fs.remove(srcwpconfig);
      await fs.ensureSymlink( dstwpconfig,  srcwpconfig, 'file');
      console.log('success!');
    } catch (err) {
      console.error(err);
    }
  } else {
    console.log("No existe el archivo ", srcwpconfig);
  }
   
}

// Async/Await:
async function moverwphtcaccess () {
  if ( ! fs.pathExists(srcwphtcaccess)) {
  try {
    await fs.move( srcwphtcaccess, dstwphtcaccess, {overwrite: true});
    // await fs.remove(srcwphtcaccess);
    await fs.ensureSymlink( dstwphtaccess,  srcwphtaccess, 'file');
    console.log('success!');
  } catch (err) {
    console.error(err);
  }
  } else {
     console.log("No existe el archivo ", srcwphtcaccess);
  }
}

// async function crearlinkwpcontent () {
//   try {
//     await fs.ensureSymlink(    srcwpcontent, dstwpcontent, 'dir');
//     console.log('success!');
//   } catch (err) {
//     console.error(err);
//   }
// }
 

// async function crearlinkwpconfig () {
//   try {
//     await fs.ensureSymlink(  dstwpconfig, srcwpconfig);
//     console.log('success!');
//   } catch (err) {
//     console.error(err);
//   }
// }

// async function crearlinkwphtcaccess () {
//   try {
//     await fs.ensureSymlink (srcwphtaccess, dstwphtaccess);
//     console.log('success!');
//   } catch (err) {
//     console.error(err);
//   }
// }


gulp.task('tlinkremovewpcontentwpconfightcaccess', function(done) {
  linkremovewpcontentwpconfightcaccess();
  done();
});


gulp.task('tmoverwpcontent', function(done) {
  moverwpcontent();
  done();
});

gulp.task('tmoverwpconfig', function(done) {
  moverwpconfig();
  done();
});

gulp.task('tmoverwphtcaccess', function(done) {
  moverwphtcaccess();
  done();
});



gulp.task('watch',  function(done) {
  // gulp.watch('/opt/app-root/src/wp-content',gulp.series('tmoverwpcontent'));
  // gulp.watch('/opt/app-root/src/.htcaccess',gulp.series('tmoverwphtcaccess'));
  gulp.watch('/opt/app-root/src/wp-config.php',gulp.series('tmoverwpconfig', 'tmoverwpcontent', 'tmoverhtcaccess'));
  done();
});

gulp.task('default',  gulp.parallel('watch'));
