FROM python:3.9-slim

# Instalar cron y supervisord
RUN apt-get update \
 && apt-get install -y --no-install-recommends cron supervisor \
 && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo y logs
WORKDIR /app
RUN mkdir -p /var/www/html /var/log/cron

# Dependencias Python
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar script Python
COPY app/genera_json_vpn.py /app/

# Copiar dashboard con index.html
COPY dashboard/ /var/www/html/

# Supervisord y entrypoint
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY entrypoint.sh    /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Exponer el puerto 8088
EXPOSE 8088

ENTRYPOINT ["/entrypoint.sh"]
