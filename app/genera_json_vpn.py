from routeros_api import RouterOsApiPool
import json
from datetime import datetime

# ▶️ Configuración MikroTik
MIKROTIK_IP = '192.168.88.1'     # Cambiar por tu IP
USUARIO = 'Chato'                # Tu usuario MikroTik
CLAVE = 'chato1976'                # Tu contraseña

# 📁 Archivos
JSON_DATOS = 'datosvpn.json'
ESTADO_ANTERIOR = 'estado_anterior.json'
LOG = 'log.txt'
MAX_EVENTOS_LOG = 100

# ⏮️ Cargar estado anterior
try:
    with open(ESTADO_ANTERIOR, 'r') as f:
        estado_prev = json.load(f)
except FileNotFoundError:
    estado_prev = {}

# 🔌 Conexión al MikroTik
api_pool = RouterOsApiPool(
    host=MIKROTIK_IP,
    username=USUARIO,
    password=CLAVE,
    plaintext_login=True
)
api = api_pool.get_api()
sessions = api.get_resource('/interface/l2tp-server/session')

# 🧮 Preparar datos actuales
datos_actuales = []
eventos_log = []
ahora_iso = datetime.now().isoformat()
ahora_legible = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

for sesion in sessions.get():
    nombre = sesion.get("name", "sin-nombre")
    conectado = sesion.get("running", False)
    rx = int(sesion.get("rx-byte", 0))
    tx = int(sesion.get("tx-byte", 0))
    uptime = sesion.get("uptime", "0s")

    estado_antes = estado_prev.get(nombre, {})
    conectado_antes = estado_antes.get("connected", None)

    if not conectado and conectado_antes:
        hora_descon = ahora_legible
        eventos_log.append(f"[{hora_legible}] ❌ Desconexión: {nombre}")
    elif conectado and conectado_antes is False:
        hora_descon = estado_antes.get("last_disconnected", "--")
        eventos_log.append(f"[{hora_legible}] ✅ Reconexión: {nombre}")
    else:
        hora_descon = estado_antes.get("last_disconnected", "--")

    datos_actuales.append({
        "name": nombre,
        "connected": conectado,
        "rx": rx,
        "tx": tx,
        "uptime": uptime,
        "last_disconnected": hora_descon
    })

# 💾 Guardar estado actualizado
estado_guardado = {
    d["name"]: {
        "connected": d["connected"],
        "last_disconnected": d["last_disconnected"]
    } for d in datos_actuales
}
with open(ESTADO_ANTERIOR, 'w') as f:
    json.dump(estado_guardado, f, indent=2)

# 📤 Exportar datos JSON para panel
with open(JSON_DATOS, 'w') as f:
    json.dump(datos_actuales, f, indent=2)

# 🪵 Actualizar log.txt con últimos eventos
try:
    with open(LOG, 'r') as f:
        historial = f.readlines()
except FileNotFoundError:
    historial = []

historial.extend([linea + "\n" for linea in eventos_log])
historial = historial[-MAX_EVENTOS_LOG:]  # Mantener los últimos N eventos

with open(LOG, 'w') as f:
    f.writelines(historial)

print(f"[{ahora_legible}] ✅ Datos actualizados y exportados.")
