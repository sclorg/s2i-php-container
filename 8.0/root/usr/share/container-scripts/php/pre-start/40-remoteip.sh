# Enable mod_remoteip for X-Forwarded-For handling behind reverse proxies
# Activated by setting HTTPD_ENABLE_REMOTEIP=1

if [ "${HTTPD_ENABLE_REMOTEIP:-}" == "1" ]; then
  log_info 'Enabling mod_remoteip for X-Forwarded-For handling...'
  cat > "${HTTPD_CONFIGURATION_PATH}/remoteip.conf" <<'EOF'
# mod_remoteip - Handle X-Forwarded-For from trusted proxies
# https://httpd.apache.org/docs/2.4/mod/mod_remoteip.html
LoadModule remoteip_module modules/mod_remoteip.so

RemoteIPHeader X-Forwarded-For
# Private IP ranges - safe for Docker/Kubernetes internal networks
RemoteIPTrustedProxy 10.0.0.0/8
RemoteIPTrustedProxy 172.16.0.0/12
RemoteIPTrustedProxy 192.168.0.0/16
RemoteIPTrustedProxy 169.254.0.0/16
RemoteIPTrustedProxy 127.0.0.0/8
EOF
fi
