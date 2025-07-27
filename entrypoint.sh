#!/bin/bash
set -e

# Crear tarea cron cada 2 minutos
echo "*/2 * * * * python3 /app/genera_json_vpn.py >> /var/log/cron/fetch.log 2>&1" \
  > /etc/cron.d/fetch-cron
chmod 0644 /etc/cron.d/fetch-cron

# Iniciar cron y servidor web
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
