# additional arbitrary httpd configuration provided by user using s2i

log_info 'Processing additional arbitrary httpd configuration provided by s2i ...'

process_extending_config_files ${APP_DATA}/httpd-cfg/ ${PHP_CONTAINER_SCRIPTS_PATH}/httpd-cnf/

