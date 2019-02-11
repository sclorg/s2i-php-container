config_httpd_conf() {
  sed -i "s/^Listen 80/Listen 0.0.0.0:8080/" ${HTTPD_MAIN_CONF_PATH}/httpd.conf
  sed -i "s/^User apache/User default/" ${HTTPD_MAIN_CONF_PATH}/httpd.conf
  sed -i "s/^Group apache/Group root/" ${HTTPD_MAIN_CONF_PATH}/httpd.conf
  sed -i "s%^DocumentRoot \"${HTTPD_DATA_ORIG_PATH}/html\"%#DocumentRoot \"${APP_DATA}\"%" ${HTTPD_MAIN_CONF_PATH}/httpd.conf
  sed -i "s%^<Directory \"${HTTPD_DATA_ORIG_PATH}/html\"%<Directory \"${APP_DATA}\"%" ${HTTPD_MAIN_CONF_PATH}/httpd.conf
  sed -i "s%^<Directory \"${HTTPD_VAR_PATH}/html\"%<Directory \"${APP_DATA}\"%" ${HTTPD_MAIN_CONF_PATH}/httpd.conf
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
  sed -i '/php_value session.save_/d' ${HTTPD_MAIN_CONF_D_PATH}/${PHP_HTTPD_CONF_FILE}
  head -n151 ${HTTPD_MAIN_CONF_PATH}/httpd.conf | tail -n1 | grep "AllowOverride All" || exit 1
  echo "IncludeOptional ${APP_ROOT}/etc/conf.d/*.conf" >> ${HTTPD_MAIN_CONF_PATH}/httpd.conf
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

# Copy config files from application to the location where httpd expects them
# Param sets the directory where to look for files
# This function was taken from httpd container
process_config_files() {
  local dir=${1:-.}
  if [ -d ${dir}/httpd-cfg ]; then
    echo "---> Copying httpd configuration files..."
    if [ "$(ls -A ${dir}/httpd-cfg/*.conf)" ]; then
      cp -v ${dir}/httpd-cfg/*.conf "${HTTPD_CONFIGURATION_PATH}"/
      rm -rf ${dir}/httpd-cfg
    fi
  fi
}

# Copy SSL files provided in application source
# This function was taken from httpd container
process_ssl_certs() {
  local dir=${1:-.}
  if [ -d ${dir}/httpd-ssl/private ] && [ -d ${dir}/httpd-ssl/certs ]; then
    echo "---> Looking for SSL certs for httpd..."
    cp -r ${dir}/httpd-ssl ${APP_ROOT}
    local ssl_cert="$(ls -A ${APP_ROOT}/httpd-ssl/certs/*.pem | head -n 1)"
    local ssl_private="$(ls -A ${APP_ROOT}/httpd-ssl/private/*.pem | head -n 1)"
    if [ -f "${ssl_cert}" ] ; then
      # do sed for SSLCertificateFile and SSLCertificateKeyFile
      echo "---> Setting SSL cert file for httpd..."
      sed -i -e "s|^SSLCertificateFile .*$|SSLCertificateFile ${ssl_cert}|" ${HTTPD_MAIN_CONF_D_PATH}/ssl.conf
      if [ -f "${ssl_private}" ]; then
        echo "---> Setting SSL key file for httpd..."
        sed -i -e "s|^SSLCertificateKeyFile .*$|SSLCertificateKeyFile ${ssl_private}|" ${HTTPD_MAIN_CONF_D_PATH}/ssl.conf
      else
        echo "---> Removing SSL key file settings for httpd..."
        sed -i '/^SSLCertificateKeyFile .*/d'  ${HTTPD_MAIN_CONF_D_PATH}/ssl.conf
      fi
    fi
    rm -rf ${dir}/httpd-ssl
  fi
}

