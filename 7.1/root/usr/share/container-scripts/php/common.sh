config_httpd_conf() {
  sed -i "s/^Listen 80/Listen 0.0.0.0:8080/" ${HTTPD_MAIN_CONF_PATH}/httpd.conf
  sed -i "s/^User apache/User default/" ${HTTPD_MAIN_CONF_PATH}/httpd.conf
  sed -i "s/^Group apache/Group root/" ${HTTPD_MAIN_CONF_PATH}/httpd.conf
  sed -i "s%^DocumentRoot \"/opt/rh/httpd24/root/var/www/html\"%#DocumentRoot \"/opt/app-root/src\"%" ${HTTPD_MAIN_CONF_PATH}/httpd.conf
  sed -i "s%^<Directory \"/opt/rh/httpd24/root/var/www/html\"%<Directory \"/opt/app-root/src\"%" ${HTTPD_MAIN_CONF_PATH}/httpd.conf
  sed -i "s%^<Directory \"/opt/rh/httpd24/root/var/html\"%<Directory \"/opt/app-root/src\"%" ${HTTPD_MAIN_CONF_PATH}/httpd.conf
  sed -i "s%^ErrorLog \"logs/error_log\"%ErrorLog \"|/usr/bin/cat\"%" ${HTTPD_MAIN_CONF_PATH}/httpd.conf
  sed -i "s%CustomLog \"logs/access_log\"%CustomLog \"|/usr/bin/cat\"%" ${HTTPD_MAIN_CONF_PATH}/httpd.conf
  sed -i "151s%AllowOverride None%AllowOverride All%" ${HTTPD_MAIN_CONF_PATH}/httpd.conf
}

config_ssl_conf() {
  sed -i -E "s/^Listen 443/Listen 0.0.0.0:8443/" ${HTTPD_MAIN_CONF_D_PATH}/ssl.conf
  sed -i -E "s/_default_:443/_default_:8443/" ${HTTPD_MAIN_CONF_D_PATH}/ssl.conf
  sed -i -E "s!^(\s*CustomLog)\s+\S+!\1 |/usr/bin/cat!" ${HTTPD_MAIN_CONF_D_PATH}/ssl.conf
  sed -i -E "s!^(\s*TransferLog)\s+\S+!\1 |/usr/bin/cat!" ${HTTPD_MAIN_CONF_D_PATH}/ssl.conf
  sed -i -E "s!^(\s*ErrorLog)\s+\S+!\1 |/usr/bin/cat!" ${HTTPD_MAIN_CONF_D_PATH}/ssl.conf
}

config_general() {
  config_httpd_conf
  config_ssl_conf
  sed -i '/php_value session.save_path/d' /opt/rh/httpd24/root/etc/httpd/conf.d/rh-php71-php.conf
  head -n151 /opt/rh/httpd24/root/etc/httpd/conf/httpd.conf | tail -n1 | grep "AllowOverride All" || exit 1
  echo "IncludeOptional /opt/app-root/etc/conf.d/*.conf" >> /opt/rh/httpd24/root/etc/httpd/conf/httpd.conf
}

function log_info {
  echo "---> `date +%T`     $@"
}

function log_and_run {
  log_info "Running $@"
  "$@"
}

function log_volume_info {
  CONTAINER_DEBUG=${CONTAINER_DEBUG:-}
  if [[ "${CONTAINER_DEBUG,,}" != "true" ]]; then
    return
  fi

  log_info "Volume info for $@:"
  set +e
  log_and_run mount
  while [ $# -gt 0 ]; do
    log_and_run ls -alZ $1
    shift
  done
  set -e
}

# get_matched_files finds file for image extending
function get_matched_files() {
  local custom_dir default_dir
  custom_dir="$1"
  default_dir="$2"
  files_matched="$3"
  find "$default_dir" -maxdepth 1 -type f -name "$files_matched" -printf "%f\n"
  [ -d "$custom_dir" ] && find "$custom_dir" -maxdepth 1 -type f -name "$files_matched" -printf "%f\n"
}

# process_extending_files process extending files in $1 and $2 directories
# - source all *.sh files
#   (if there are files with same name source only file from $1)
function process_extending_files() {
  local custom_dir default_dir
  custom_dir=$1
  default_dir=$2

  while read filename ; do
    echo "=> sourcing $filename ..."
    # Custom file is prefered
    if [ -f $custom_dir/$filename ]; then
      source $custom_dir/$filename
    elif [ -f $default_dir/$filename ]; then
      source $default_dir/$filename
    fi
  done <<<"$(get_matched_files "$custom_dir" "$default_dir" '*.sh' | sort -u)"
}

# process extending config files in $1 and $2 directories
# - expand variables in *.conf and copy the files into /opt/app-root/etc/httpd.d directory
#   (if there are files with same name source only file from $1)
function process_extending_config_files() {
  local custom_dir default_dir
  custom_dir=$1
  default_dir=$2

  while read filename ; do
    echo "=> sourcing $filename ..."
    # Custom file is prefered
    if [ -f $custom_dir/$filename ]; then
       envsubst < $custom_dir/$filename > ${HTTPD_CONFIGURATION_PATH}/$filename
    elif [ -f $default_dir/$filename ]; then
       envsubst < $default_dir/$filename > ${HTTPD_CONFIGURATION_PATH}/$filename
    fi
  done <<<"$(get_matched_files "$custom_dir" "$default_dir" '*.conf' | sort -u)"
}

