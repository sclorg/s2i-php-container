if [ -d "/run/php-fpm" ]; then
  log_info "Starting FPM - pre-start"
  /usr/sbin/php-fpm --daemonize
else
  log_info "Using mod_php"
fi
