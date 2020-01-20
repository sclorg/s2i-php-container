$table_prefix = 'wp_';

define( 'WPLANG', 'es_ES' );
//define( 'WP_LANG_DIR', dirname(__FILE__) . 'wordpress/languages' );

define('FORCE_SSL_ADMIN', true);
define('FORCE_SSL_LOGIN', true);

define( 'AUTOMATIC_UPDATER_DISABLED', true );
define( 'WP_AUTO_UPDATE_CORE', false );

// define('WP_HOME', 'http://' . $_SERVER['HTTP_HOST'] . '/');
// define('WP_SITEURL', 'http://' . $_SERVER['HTTP_HOST'] . '/');

if (strpos($_SERVER['HTTP_X_FORWARDED_PROTO'], 'https') !== false) $_SERVER['HTTPS']='on';

define('FS_METHOD', 'direct');


