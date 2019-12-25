'use strict';


const gulp = require('gulp');
const fs = require('fs-extra');
var concat = require('gulp-concat');
var shell = require('shelljs');



const srcwpcontent = '/opt/app-root/src/wp-content';
const srcwpcontentpriv = '/opt/app-root/silo/wordpress/wp-content';
const dstwpcontent = '/silo/wordpress/wp-content';
const srcwphtaccess = '/opt/app-root/src/.htaccess';
const srcwphtaccesspriv = '/opt/app-root/silo/wordpress/.htaccess';
const dstwphtaccessdev = '/silo/wordpress/dev/.htaccess-dev';
const dstwphtaccess = '/silo/wordpress/.htaccess';
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
    const existe1 = await fs.pathExists(dstwpcontent);
    if (! existe1 ){
      if ( existe) {
        await fs.move( srcwpcontent, dstwpcontent, {overwrite: true});
        console.log('success!');
      } else {
        console.log("No existe la carpeta ",srcwpcontent);
      }
    }
  } catch (err) {
    console.error(err);
  };
  done();
});


gulp.task('tcreateSymlinkwpcontent', async function(done) {
  try {
    const existe = await fs.pathExists(dstwpcontent);
    const existe1 = await fs.pathExists(srcwpcontent);
    if (! existe1) {
      if (existe) {
        // await fs.remove( srcwpcontent );
        await fs.ensureSymlink( dstwpcontent,  srcwpcontent, 'dir');
        console.log('success!');
      } else {
        console.log("No existe el archivo. ", dstwpcontent);
      }
    }
  } catch (err) {
    console.error(err);
  };
  done();
});


//////// .htaccess

gulp.task('tmoverwphtaccesspriv',async function(done)  {
  try {
    const existe = await fs.pathExists(srcwphtaccesspriv);
    if ( existe ){
      await fs.move( srcwphtaccesspriv, dstwphtaccess, {overwrite: true});
      console.log('success!');
    } else {
      console.log("No existe el archivo ", srcwphtaccesspriv);
    }
  } catch (err) {
    console.error(err);
  };
  done();
});



gulp.task('tmoverwphtaccess',async function(done)  {
  try {
    const existe1 = await fs.pathExists(dstwphtaccessdev);
    const existe = await fs.pathExists(srcwphtaccess);
    if (! existe1 ){
      if (existe) {
        await fs.copy( srcwphtaccess, dstwphtaccess, {overwrite: true});
        await fs.move( srcwphtaccess, dstwphtaccessdev, {overwrite: true});
        console.log('success!');
      } else {
        console.log("No existe el archivo ", srcwphtaccess);
      }
    }
  } catch (err) {
    console.error(err);
  };
  done();
});



gulp.task('tcreateSymlinkwphtaccess', async function(done) {
  try {
    const existe = await fs.pathExists(dstwphtaccessdev);
    const existe1 = await fs.pathExists(srcwphtaccess);
    if (! existe1) {
      if (existe) {
       //  await fs.remove( srcwphtaccess );
        await fs.ensureSymlink( dstwphtaccessdev,  srcwphtaccess, 'file');
        console.log('success!');
      } else {
        console.log("No existe el archivo ", dstwphtaccessdev);
      }
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

gulp.task('tmoverwpconfig',async function (done) {
  try {
    const existe1 = await fs.pathExists(dstwpconfigdev);
    const existe = await fs.pathExists(srcwpconfig);
    if (! existe1 ) {
      if (existe) {
        await fs.copy( srcwpconfig, dstwpconfig, {overwrite: true});
        await fs.move( srcwpconfig, dstwpconfigdev, {overwrite: true});
        console.log('success!');
      } else {
        console.log("No existe el archivo ", srcwpconfig);
      }
    }
  } catch (err) {
    console.error(err);
  };
  done();
});


gulp.task('twpconfigchange', async function(done) {
  try {
    const existe = await fs.pathExists(dstwpconfigdev);
    const existe1 = await fs.pathExists(dstwpconfig);
    if ( existe ){
      shell.sed('-i', /^.*define\(.*DB_COLLATE.*/, 'define( \'DB_COLLATE\', \'utf8_general_ci\' );' , dstwpconfigdev);
      shell.sed('-i', /.*table_prefix.*/, shell.cat ('wp_config.js') , dstwpconfigdev);
      shell.sed( '-i', /^.*define\(.*WP_DEBUG.*/, shell.cat('wp_config_dev.js') , dstwpconfigdev);
      console.log('success!');
    }
    if (existe1 ) {
      shell.sed('-i', /^.*define\(.*DB_HOST.*/, 'define( \'DB_HOST\', \'localhost\' );' , dstwpconfig);
      shell.sed('-i', /^.*define\(.*DB_COLLATE.*/, 'define( \'DB_COLLATE\', \'utf8_general_ci\' );' , dstwpconfig);
      shell.sed('-i', /.*table_prefix.*/, shell.cat ('wp_config.js') , dstwpconfig);
      console.log('success!');
    } 
  } catch (err) {
    console.error(err);
  };
  done();
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



gulp.task('watch',  function(done) {
  gulp.watch('/opt/app-root/src/**/wp-confi?.php',  gulp.series('tmoverwpconfig','twpconfigchange', 'tcreateSymlinkwpconfig'));
  gulp.watch('/opt/app-root/src/**/.htacces?',  gulp.series('tmoverwphtaccess', 'tcreateSymlinkwphtaccess'));
  
  
  done();
});

gulp.task('default',  gulp.series('watch'));

// gulp.task('union', gulp.series('tmoverwpconfig','twpconfigchange', 'tcreateSymlinkwpconfig'));

// gulp.task('unionh', gulp.series('tmoverwphtaccess', 'tcreateSymlinkwphtaccess'));

gulp.task('tmovelinkwpcontent', gulp.series('tmoverwpcontent', 'tcreateSymlinkwpcontent'));
