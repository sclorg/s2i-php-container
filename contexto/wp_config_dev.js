define( 'WP_MEMORY_LIMIT', '256M' );

define( 'WP_MAX_MEMORY_LIMIT', '256M' );

if ( defined( 'WP_CLI' ) ) {
  $_SERVER['HTTP_HOST'] = 'localhost';
};

if ( ! defined( 'WP_CLI' ) ) {
  // remove x-pingback HTTP header
  add_filter('wp_headers', function($headers) {
    unset($headers['X-Pingback']);
    return $headers;
  });
  // disable pingbacks
  add_filter( 'xmlrpc_methods', function( $methods ) {
    unset( $methods['pingback.ping'] );
    return $methods;
  });
  add_filter( 'auto_update_translation', '__return_false' );
};


define( 'WP_DEBUG', true );

define( 'WP_DISABLE_FATAL_ERROR_HANDLER', true );   // 5.2 and later

// define('WP_DEBUG_LOG', true); // wp-content/debug.log

define('WP_DEBUG_LOG', '/silo/wordpress/dev/wp_error.log'); // /silo/wordpress/dev/wp-error.log
@ini_set( 'log_errors', 'On' );
ini_set( 'error_log', '/silo/wordpress/dev/wp_error.log' );

define('WP_DEBUG_DISPLAY', true ); //para que se muestren en html
@ini_set('display_errors', 'On');


define( 'SCRIPT_DEBUG', true ); // usa js y css no comprimidos para debug

define( 'CONCATENATE_SCRIPTS', false ); //no se agrupen js scripts


// define('SAVEQUERIES', true); // El array se almacena en la global $wpdb->queries.


