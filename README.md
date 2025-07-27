# Mikrotik Dashboard

Dashboard ligero para monitorear y visualizar el estado de dispositivos MikroTik en tiempo real, basado en HTML + scripts personalizados.

## 📌 Características

- 🔍 Monitoreo del estado de red, IP y VPN
- 🧠 Integración con scripts de consulta vía API MikroTik
- 📈 Visualización en dashboard HTML con íconos personalizados
- 🚨 Alertas por Telegram (opcional)
- 📦 Fácil despliegue en Docker o servidor local

## ⚙️ Requisitos

- Dispositivo MikroTik con acceso API habilitado
- Servidor Linux con Python 3 y cron
- HTML5 compatible (para dashboard visual)
- Acceso a red interna o VPN hacia el router

## 🚀 Instalación

```bash
git clone https://github.com/dotworking/mikrotik-dashboard.git
cd mikrotik-dashboard
# Ejecutar script principal o configurar en cron
python3 monitor.py
