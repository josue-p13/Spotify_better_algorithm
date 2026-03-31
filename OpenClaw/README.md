# 📱 OpenClaw - Automatización desde WhatsApp

Esta carpeta contiene scripts para automatizar el inicio del **Spotify Better Algorithm** usando **OpenClaw**, permitiendo controlarlo desde **WhatsApp** u otras aplicaciones móviles.

---

## 🚀 Scripts Disponibles

### 🪟 Windows
- **Archivo**: `windows_start.bat`
- **Uso**: Doble click o desde OpenClaw
- **Características**: 
  - ✅ Verificación automática de Python y Node.js
  - 🔧 Instalación automática de dependencias
  - 🌐 Muestra todas las IPs disponibles
  - 📱 Optimizado para redes locales

### 🐧 Linux
- **Archivo**: `linux_start.sh`  
- **Uso**: `bash linux_start.sh` o desde OpenClaw
- **Características**:
  - ✅ Soporte para Python3 y Python
  - 🎨 Output colorizado en terminal
  - 🔧 Instalación automática de dependencias
  - 🌐 Detección inteligente de IPs de red

---

## 📲 Configuración en OpenClaw

### Paso 1: Instalar OpenClaw
1. Descarga OpenClaw desde [su sitio oficial](https://openclaw.com)
2. Instala en tu dispositivo Android/iOS
3. Configura conexión con tu PC/servidor

### Paso 2: Configurar Comando
1. Abre OpenClaw
2. Crea un nuevo comando:
   - **Nombre**: "Spotify Better Algorithm"  
   - **Comando Windows**: `"C:\ruta\completa\OpenClaw\windows_start.bat"`
   - **Comando Linux**: `bash /ruta/completa/OpenClaw/linux_start.sh`
   - **Alias**: "musica", "spotify", "music"

### Paso 3: Uso desde WhatsApp
1. Envía mensaje a OpenClaw: `!musica`
2. El sistema se iniciará automáticamente
3. Recibirás las URLs disponibles:
   - `http://localhost:5173` (local)
   - `http://192.168.1.X:5173` (red)

---

## 🔧 Características de los Scripts

### ✅ Verificaciones Automáticas
- **Python** instalado y accesible
- **Node.js** para el frontend
- **Dependencias** de Python y npm
- **Playwright** para web scraping

### 🛠️ Instalación Automática
- **Entorno virtual** de Python (.venv)
- **Dependencias** desde requirements.txt  
- **Playwright Chromium** para scraping
- **Frontend** compilado y optimizado

### 📡 Información de Red
- **IP local** del dispositivo
- **Hostname** para conexión fácil
- **Múltiples interfaces** de red
- **Acceso desde cualquier dispositivo** en la red

### 🎯 Experiencia Optimizada
- **Mensajes claros** sobre el progreso
- **Manejo de errores** descriptivo
- **Colores** en terminales Linux
- **Pausa automática** en Windows para ver errores

---

## 🌐 Acceso Remoto

Una vez iniciado el script, podrás acceder desde:

### 📱 Dispositivos Móviles
- iPhone/Android en la misma WiFi
- Tablets y otros dispositivos
- Cualquier navegador web moderno

### 💻 Otras Computadoras
- Laptops en la red local  
- Otros PCs/Macs
- Dispositivos IoT con navegador

### 🔗 URLs Típicas
```
Local:      http://localhost:5173
Red WiFi:   http://192.168.1.100:5173  
Ethernet:   http://10.0.0.50:5173
Hotspot:    http://192.168.43.1:5173
```

---

## 🚨 Requisitos de Red

### 🔥 Firewall
**Windows**: Permitir Python en firewall cuando se solicite
**Linux**: Verificar que puerto 5173 esté abierto:
```bash
sudo ufw allow 5173
```

### 📡 Router
- Dispositivos deben estar en la **misma red WiFi**
- **Aislamiento AP** debe estar deshabilitado  
- Puerto **5173** no debe estar bloqueado

### 🔒 Seguridad
- ⚠️ **Solo usar en redes confiables** (casa, oficina)
- 🚫 **No exponer a internet** públicamente
- 🔐 **Configurar firewall** apropiadamente

---

## 🛠️ Troubleshooting

### ❌ "Python no está instalado"
```bash
# Windows
# Descargar desde: https://python.org

# Linux Ubuntu/Debian  
sudo apt update && sudo apt install python3 python3-pip

# Linux CentOS/RHEL
sudo yum install python3 python3-pip
```

### ❌ "Node.js no está instalado"  
```bash
# Windows
# Descargar desde: https://nodejs.org

# Linux
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### ❌ "Error instalando dependencias"
```bash
# Limpiar cache y reinstalar
rm -rf .venv node_modules
# Ejecutar script nuevamente
```

### ❌ "No se puede acceder desde móvil"
1. Verificar que PC y móvil estén en misma WiFi
2. Desactivar temporalmente firewall para probar
3. Usar IP mostrada por el script (no localhost)
4. Verificar que puerto 5173 esté disponible

---

## 📋 Ejemplo de Uso Completo

### 1. WhatsApp → OpenClaw
```
Usuario: !musica
OpenClaw: ✅ Ejecutando Spotify Better Algorithm...
```

### 2. Script se ejecuta
```
🎵 Iniciando Spotify Better Algorithm...
✅ Python y Node.js detectados
🔧 Creando entorno virtual...
📦 Instalando dependencias...
🔨 Compilando frontend...
🚀 Iniciando servidor...

📱 Interfaces disponibles:
   - Local: http://localhost:5173
   - Red local: http://192.168.1.100:5173
```

### 3. Acceso desde móvil
1. Abrir navegador en iPhone/Android
2. Ir a `http://192.168.1.100:5173`
3. Configurar credenciales de Spotify
4. ¡Disfrutar del sistema!

---

## 💡 Tips y Trucos

### 🚀 Optimización
- **Deja el script corriendo** - no consumes muchos recursos
- **Usa marcadores** en el navegador para acceso rápido
- **Configura múltiples alias** en OpenClaw: "music", "spotify", "musica"

### 📱 Móvil
- **Agrega a pantalla de inicio** como webapp
- **Usa Chrome/Safari** para mejor compatibilidad
- **Mantén pantalla activa** durante uso intensivo

### 🔄 Automatización
- **Configura inicio automático** al encender PC
- **Usa con Tasker** (Android) para automatización avanzada
- **Combina con otros comandos** de OpenClaw

---

*¡Controla tu música desde cualquier lugar de tu casa! 🎶📱*