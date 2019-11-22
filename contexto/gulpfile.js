'use strict';


const gulp = require('gulp');
const fs = require('fs-extra');
var concat = require('gulp-concat');



const srcwpcontent = '/opt/app-root/src/wp-content';
const srcwpcontentpriv = '/opt/app-root/silo/wordpress/wp-content';
const dstwpcontent = '/silo/wordpress/wp-content';
const srcwphtcaccess = '/opt/app-root/src/.htcaccess';
const srcwphtcaccesspriv = '/opt/app-root/silo/wordpress/.htcaccess';
const dstwphtcaccess = '/silo/wordpress/.htcaccess';
const srcwpconfig = '/opt/app-root/src/wp-config.php' ;
const srcwpconfigpriv = '/opt/app-root/silo/wordpress/wp-config.php' ;
const dstwpconfig = '/silo/wordpress/wp-config.php';


// // With async/await:
// async function createdirwpcontent () {
//   try {
//     await fs.emptyDir('/silo/wordpress,wp-content');
//     console.log('success!');
//   } catch (err) {
//     console.error(err);
//   }
// }


// Async/Await:
async function moverwpcontentpriv () {
  if ( fs.pathExists(srcwpcontentpriv)) {
    try {
      // createdirwpcontent();
      await fs.move( srcwpcontentpriv, dstwpcontent, {overwrite: true});
      await fs.remove(srcwpcontent);
      // await fs.remove(srcwpcontent);
      // await fs.ensureSymlink( dstwpcontent,  srcwpcontent, 'dir');
      console.log('success!');
    } catch (err) {
      console.error(err);
    }
  } else {
    console.log("No existe el archivo ", moverwpcontentpriv);
  } 
}


// Async/Await:
async function moverwpcontent () {
  if ( fs.pathExists(srcwpcontent)) {
    try {
      // createdirwpcontent();
      await fs.move( srcwpcontent, dstwpcontent, {overwrite: true});
      // await fs.remove(srcwpcontent);
      // await fs.ensureSymlink( dstwpcontent,  srcwpcontent, 'dir');
      console.log('success!');
    } catch (err) {
      console.error(err);
    }
  } else {
    console.log("No existe el archivo ", moverwpcontent);
  } 
}



gulp.task('tmoverwpcontent', function(done) {
  moverwpcontent();
  done();
});

gulp.task('tmoverwpcontentpriv', function(done) {
  moverwpcontentpriv();
  done();
});




// Async/Await:
async function moverwpconfigpriv () {

  if ( fs.pathExists(srcwpconfigpriv)) {
    try {
      await fs.move( srcwpconfigpriv, dstwpconfig, {overwrite: true});
      await fs.remove( '/opt/app-root/src/wp-config-sample.php');
      // await fs.remove(srcwpconfig);
      // await fs.ensureSymlink( dstwpconfig,  srcwpconfig, 'file');
      console.log('success!');
    } catch (err) {
      console.error(err);
    }
  } else {
    console.log("No existe el archivo ", srcwpconfigpriv);
  }
  
}


// Async/Await:
async function moverwpconfig () {

  if ( fs.pathExists(srcwpconfig)) {
    try {
      await fs.move( srcwpconfig, dstwpconfig, {overwrite: true});
      fs.remove( '/opt/app-root/src/wp-config-sample.php');
      // await fs.remove(srcwpconfig);
      // await fs.ensureSymlink( dstwpconfig,  srcwpconfig, 'file');
      console.log('success!');
    } catch (err) {
      console.error(err);
    }
  } else {
    console.log("No existe el archivo ", srcwpconfig);
  }
  
}

gulp.task('tmoverwpconfigpriv', function(done) {
  moverwpconfigpriv();
  done();
});


gulp.task('tmoverwpconfig', function(done) {
  moverwpconfig();
  done();
});


// Async/Await:
async function moverwphtcaccesspriv () {
  if ( fs.pathExists(srcwphtcaccesspriv)) {
    try {
      await fs.move( srcwphtcaccesspriv, dstwphtcaccess, {overwrite: true});
      await fs.remove(srcwphtcaccess);
      //await fs.ensureSymlink( dstwphtcaccess,  srcwphtcaccess, 'file');
      console.log('success!');
    } catch (err) {
      console.error(err);
    }
  } else {
    console.log("No existe el archivo ", srcwphtcaccesspriv);
  }
}


// Async/Await:
async function moverwphtcaccess () {
  if ( fs.pathExists(srcwphtcaccess)) {
    try {
      await fs.move( srcwphtcaccess, dstwphtcaccess, {overwrite: true});
      await fs.remove(srcwphtcaccess);
      //await fs.ensureSymlink( dstwphtcaccess,  srcwphtcaccess, 'file');
      console.log('success!');
    } catch (err) {
      console.error(err);
    }
  } else {
    console.log("No existe el archivo ", srcwphtcaccesspriv);
  }
}


gulp.task('tmoverwphtcaccesspriv', function(done) {
  moverwphtcaccesspriv();
  done();
});

gulp.task('tmoverwphtcaccess', function(done) {
  moverwphtcaccess();
  done();
});

gulp.task('createSymlinkwpconfig', async function(done) {
  
  if ( fs.pathExists(dstwpconfig)) {
    try {
      await fs.ensureSymlink( dstwpconfig,  srcwpconfig, 'file');
      console.log('success!');
    } catch (err) {
      console.error(err);
    }
  } else {
    console.log("No existe el archivo ", srcwpconfig);
  };
  done();
});

gulp.task('createSymlinkhtcaccess', async function(done) {
  
  if ( fs.pathExists(dstwpconfig)) {
    try {
      await fs.ensureSymlink( dstwphtcaccess,  srcwphtcaccess, 'file');
      console.log('success!');
    } catch (err) {
      console.error(err);
    }
  } else {
    console.log("No existe el archivo ", srcwpconfig);
  };
  done();
});



gulp.task('removewpconfig', async function(done) {
  
  if ( fs.pathExists(srcwpconfig)) {
    try {
      await fs.remove(srcwpconfig);
      console.log('success!');
    } catch (err) {
      console.error(err);
    }
  } else {
    console.log("No existe el archivo ", srcwpconfig);
  };
  done();
});
         

gulp.task('tmoveyaddwpconfig', function() {
  if ( (fs.pathExists(srcwpconfig)) && (! fs.existsSync(dstwpconfig) )) {
    // return gulp.src([srcwpconfig,'/opt/app-root/src/add-wp-config-php'],{ sourcemaps: true }, {allowEmpty:true})
    return gulp.src([srcwpconfig,'/opt/app-root/src/add-wp-config-php'],{allowEmpty:true})
    .pipe(concat( 'wp-config.php'))
    // .pipe(concat({ path: 'wp-config.php', stat: { mode: '0777' }}))
    .pipe(gulp.dest('/silo/wordpress'));
   } else {
     return console.log("Nada por hacer. ");
   };
  
});


gulp.task('enlacesSymlinkpriv', gulp.series('createSymlinkwpconfig','createSymlinkhtcaccess'));


          

gulp.task('task-kill', function() {
  console.log("before kill task");

  // process.exit(0);

  console.log("after kill task");
});


gulp.task('watch',  function(done) {
  // gulp.watch('/opt/app-root/src/wp-content',gulp.series('tmoverwpcontent'));
  // gulp.watch('/opt/app-root/src/.htcaccess',gulp.series('tmoverwphtcaccess'));
  gulp.watch('/opt/app-root/src/**/wp-confi?.php',  gulp.series('tmoveyaddwpconfig','removewpconfig','createSymlinkwpconfig', 'tmoverwpcontent','tmoverwphtcaccess','createSymlinkhtcaccess',));
  // gulp.watch('/silo/wordpdres/*',  gulp.series('createSymlinkwpconfig', 'createSymlinkhtcaccess'));
  // gulp.watch('/opt/silo/wordpdres/*',  gulp.series('createSymlinkwpconfig', 'createSymlinkhtcaccess', 'task-kill'));

  // gulp.watch('/opt/app-root/src/wp-config.php',  { ignoreInitial: false },{events: ['add']},  gulp.series('tmoveyaddwpconfig'));
  done();
});

gulp.task('default',  gulp.series('watch'));



//##########################################################

// // With async/await:
// async function createdirwpcontent () {
//   try {
//     await fs.emptyDir('/silo/wordpress,wp-content');
//     console.log('success!');
//   } catch (err) {
//     console.error(err);
//   }
// }


// // Async/Await:
// async function linkremovewpcontentwpconfightcaccess () {
//   try {
//     await fs.remove(srcwpcontent);
//     await fs.remove(srcwpconfig);
//     await fs.ensureSymlink( dstwpcontent,  srcwpcontent, 'dir');
//     await fs.ensureSymlink( dstwpconfig,  srcwpconfig, 'file');
//     if ( fs.pathExists(dstwphtcaccess)) {
//       try {
//         await fs.remove(srcwphtcaccess);
//         await fs.ensureSymlink( dstwphtcaccess,  srcwphtcaccess, 'file');
//         console.log('success!');
//       } catch (err) {
//         console.error(err);
//       }
//     } else {
//       console.log("No existe el archivo ", dstwphtcaccess);
//     }

//     console.log('success!');
//   } catch (err) {
//     console.error(err);
//   }
// }



// // Async/Await:
// async function moverwpcontent () {
//   try {
//     createdirwpcontent();
//     await fs.move( srcwpcontent, dstwpcontent, {overwrite: true});
//     // await fs.remove(srcwpcontent);
//     // await fs.ensureSymlink( dstwpcontent,  srcwpcontent, 'dir');
//     console.log('success!');
//   } catch (err) {
//     console.error(err);
//   }
// }

// // Async/Await:
// async function moverwpconfig () {

//   if ( fs.pathExists(srcwpconfig)) {
//     try {
//       await fs.move( srcwpconfig, dstwpconfig, {overwrite: true});
//       // await fs.remove(srcwpconfig);
//       await fs.ensureSymlink( dstwpconfig,  srcwpconfig, 'file');
//       console.log('success!');
//     } catch (err) {
//       console.error(err);
//     }
//   } else {
//     console.log("No existe el archivo ", srcwpconfig);
//   }
   
// }

// // Async/Await:
// async function moverwphtcaccess () {
//   if ( fs.pathExists(srcwphtcaccess)) {
//   try {
//     await fs.move( srcwphtcaccess, dstwphtcaccess, {overwrite: true});
//     // await fs.remove(srcwphtcaccess);
//     await fs.ensureSymlink( dstwphtcaccess,  srcwphtcaccess, 'file');
//     console.log('success!');
//   } catch (err) {
//     console.error(err);
//   }
//   } else {
//      console.log("No existe el archivo ", srcwphtcaccess);
//   }
// }

// // async function crearlinkwpcontent () {
// //   try {
// //     await fs.ensureSymlink(    srcwpcontent, dstwpcontent, 'dir');
// //     console.log('success!');
// //   } catch (err) {
// //     console.error(err);
// //   }
// // }
 

// // async function crearlinkwpconfig () {
// //   try {
// //     await fs.ensureSymlink(  dstwpconfig, srcwpconfig);
// //     console.log('success!');
// //   } catch (err) {
// //     console.error(err);
// //   }
// // }

// // async function crearlinkwphtcaccess () {
// //   try {
// //     await fs.ensureSymlink (srcwphtaccess, dstwphtaccess);
// //     console.log('success!');
// //   } catch (err) {
// //     console.error(err);
// //   }
// // }


// gulp.task('tlinkremovewpcontentwpconfightcaccess', function(done) {
//   linkremovewpcontentwpconfightcaccess();
//   done();
// });


// gulp.task('tmoverwpcontent', function(done) {
//   moverwpcontent();
//   done();
// });

// gulp.task('tmoverwpconfig', function(done) {
//   moverwpconfig();
//   done();
// });

// gulp.task('tmoverwphtcaccess', function(done) {
//   moverwphtcaccess();
//   done();
// });



// gulp.task('watch',  function(done) {
//   // gulp.watch('/opt/app-root/src/wp-content',gulp.series('tmoverwpcontent'));
//   // gulp.watch('/opt/app-root/src/.htcaccess',gulp.series('tmoverwphtcaccess'));
//   gulp.watch('/opt/app-root/src/wp-config.php',gulp.series('tmoverwpconfig', 'tmoverwpcontent', 'tmoverwphtcaccess'));
//   done();
// });

// gulp.task('default',  gulp.parallel('watch'));
