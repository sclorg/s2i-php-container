'use strict';


const gulp = require('gulp');
const fs = require('fs-extra');
var concat = require('gulp-concat');
var shell = require('shelljs');



const srcwpcontent = '/opt/app-root/src/wp-content';
const srcwpcontentpriv = '/opt/app-root/silo/wordpress/wp-content';
const dstwpcontent = '/silo/wordpress/wp-content';
const srcwphtcaccess = '/opt/app-root/src/.htcaccess';
const srcwphtcaccesspriv = '/opt/app-root/silo/wordpress/.htcaccess';
const dstwphtcaccessdev = '/silo/wordpress/dev/.htcaccess-dev.php';
const dstwphtcaccess = '/silo/wordpress/.htcaccess';
const srcwpconfig = '/opt/app-root/src/wp-config.php';
const srcwpconfigpriv = '/opt/app-root/silo/wordpress/wp-config.php';
const dstwpconfig = '/silo/wordpress/wp-config.php';
const dstwpconfigdev = '/silo/wordpress/dev/wp-config-dev.php';

///// wp-content


gulp.task('tmoverwpcontentpriv',async function(done)  {
  try {
    const existe = await fs.pathExists(srcwpcontentpriv);
    if ( existe ){
      await fs.move( srcwpcontentpriv, dstwpcontent, {overwrite: true});
      await fs.remove(srcwpcontent);
      console.log('success!');
    } else {
      console.log("No existe la carpeta ", srcwpcontentpriv);
    }
  } catch (err) {
    console.error(err);
  };
  done();
});


gulp.task('tmoverwpcontent',async function(done)  {
  try {
    const existe = await fs.pathExists(srcwpcontent);
    if ( existe) {
      await fs.move( srcwpcontent, dstwpcontent, {overwrite: true});
      console.log('success!');
    } else {
      console.log("No existe la carpeta ",srcwpcontent);
    }
  } catch (err) {
    console.error(err);
  };
  done();
});


gulp.task('tcreateSymlinkwpcontent', async function(done) {
  try {
    const existe = await fs.pathExists(dstwpcontent);
    if (existe) {
      await fs.remove( srcwpcontent );
      await fs.ensureSymlink( dstwpcontent,  srcwpcontent, 'dir');
      console.log('success!');
    } else {
      console.log("No existe el archivo ", dstwpcontent);
    }
  } catch (err) {
    console.error(err);
  };
  done();
});






//////// .htcaccess

gulp.task('tmoverwphtcaccesspriv',async function(done)  {
  try {
    const existe = await fs.pathExists(srcwphtcaccesspriv);
    if ( existe ){
      await fs.move( srcwphtcaccesspriv, dstwphtcaccess, {overwrite: true});
      console.log('success!');
    } else {
      console.log("No existe el archivo ", srcwphtcaccesspriv);
    }
  } catch (err) {
    console.error(err);
  };
  done();
});



gulp.task('tmoverwphtcaccess',async function(done)  {
  try {
    const existe = await fs.pathExists(srcwphtcaccess);
    if ( existe ){
      await fs.move( srcwphtcaccess, dstwphtcaccess, {overwrite: true});
      console.log('success!');
    } else {
      console.log("No existe el archivo ", srcwphtcaccess);
    }
  } catch (err) {
    console.error(err);
  };
  done();
});



gulp.task('tcreateSymlinkwphtcaccess', async function(done) {
  try {
    const existe = await fs.pathExists(dstwphtcaccessdev);
    if (existe) {
      await fs.remove( srcwphtcaccess );
      await fs.ensureSymlink( dstwphtcaccessdev,  srcwphtcaccess, 'file');
      console.log('success!');
    } else {
      console.log("No existe el archivo ", dstwphtcaccessdev);
    }
  } catch (err) {
    console.error(err);
  };
  done();
});


//////// wp-config



// Async/Await:
gulp.task('tmoverwpconfigpriv',async function () {
  try {
    const existe = await fs.pathExists(srcwpconfigpriv);
    if ( existe ){
      await fs.move( srcwpconfigpriv, dstwpconfig, {overwrite: true});
      console.log('success!');
    } else {
      console.log("No existe el archivo ", srcwpconfigpriv);
    }
  } catch (err) {
    console.error(err);
  };
  done();
});



gulp.task('twpconfigdev', async function(done) {
  try{
    const existe = await fs.pathExists(srcwpconfig);
    const existedev = await fs.pathExists(dstwpconfigdev);
    if (existedev) {
      await fs.remove(dstwpconfigdev);
    }
    if (existe) {
      return gulp.src([srcwpconfig,'/opt/app-root/src/add-wp-config-dev-php'],{allowEmpty:true})
        .pipe(concat( 'wp-config-dev.php'))
        .pipe(gulp.dest(dstwpconfigdev));

    } else {
      return console.log("Nada por hacer. ");
    }

  } catch (err) {
    console.error(err);
  };
  done();
})


gulp.task('twpconfig', async function(done) {
  try{
    const existe = await fs.pathExists(srcwpconfig);
    const existeprod = await fs.pathExists(dstwpconfig);
    if (existeprod) {
      await fs.remove(dstwpconfig);
    }
    if (existe) {
      return gulp.src([srcwpconfig,'/opt/app-root/src/add-wp-config-prod-php'],{allowEmpty:true})
        .pipe(concat( 'wp-config-prod.php'))
        .pipe(gulp.dest(dstwpconfig));

    } else {
      return console.log("Nada por hacer. ");
    }

  } catch (err) {
    console.error(err);
  };
  done();
})

gulp.task('twpconfigchangedebug', async function(done) {
  shell.sed('-i', /^.*define\(.*WP_DEBUG.*/, 'define( \'WP_DEBUG\', true );' , dstwpconfig);
});


gulp.task('twpconfigchangehost', async function(done) {
  shell.sed('-i', /^.*define\(.*DB_HOST.*/, 'define( \'DB_HOST\', \'localhost\' );' , dstwpconfig);
});


gulp.task('tcreateSymlinkwpconfig', async function(done) {
  try {
    const existe = await fs.pathExists(dstwpconfigdev);
    const existe1 = await fs.pathExists(srcwpconfig);
    if (! existe1 ) {
      if (existe) {
        // await fs.remove( srcwpconfig );
        await fs.ensureSymlink( dstwpconfigdev,  srcwpconfig, 'file');
        console.log('success!');
      } else {
        console.log("No existe el archivo ", dstwpconfigdev);
      }
    } else {
      console.log("Nada por hacer.");
    }
  } catch (err) {
    console.error(err);
  };
  done();
});


///////////



// gulp.task('enlacesSymlinkpriv', gulp.series('createSymlinkwpconfig','createSymlinkhtcaccess'));


          

// gulp.task('task-kill', function() {
//   console.log("before kill task");

//    process.exit(0);

//   console.log("after kill task");
// });


gulp.task('watch',  function(done) {
  // gulp.watch('/opt/app-root/src/wp-content',gulp.series('tmoverwpcontent'));
  // gulp.watch('/opt/app-root/src/.htcaccess',gulp.series('tmoverwphtcaccess'));
  gulp.watch('/opt/app-root/src/**/wp-confi?.php',  gulp.series('twpconfigdev','twpconfig','createSymlinkwpconfig'));
  // gulp.watch('/silo/wordpdres/*',  gulp.series('createSymlinkwpconfig', 'createSymlinkhtcaccess'));
  // gulp.watch('/opt/silo/wordpdres/*',  gulp.series('createSymlinkwpconfig', 'createSymlinkhtcaccess', 'task-kill'));

  // gulp.watch('/opt/app-root/src/wp-config.php',  { ignoreInitial: false },{events: ['add']},  gulp.series('tmoveyaddwpconfig'));
  done();
});

gulp.task('default',  gulp.series('watch'));

