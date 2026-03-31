#!/bin/bash

# ============================================
# Spotify Better Algorithm - OpenClaw Script
# Para Linux - Automatización desde WhatsApp
# ============================================

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${PURPLE}🎵 Iniciando Spotify Better Algorithm...${NC}"
echo ""

# Obtener directorio del script y del proyecto
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Cambiar al directorio del proyecto
cd "$PROJECT_DIR"

echo -e "${BLUE}📁 Directorio del proyecto: $PROJECT_DIR${NC}"
echo ""

# Verificar si existe Python
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo -e "${RED}❌ Error: Python no está instalado${NC}"
        echo -e "${YELLOW}💡 Instala Python: sudo apt update && sudo apt install python3 python3-pip${NC}"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Verificar si existe Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Error: Node.js no está instalado${NC}"
    echo -e "${YELLOW}💡 Instala Node.js: curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - && sudo apt-get install -y nodejs${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python y Node.js detectados${NC}"
echo ""

# Verificar si existe el entorno virtual
if [ ! -d ".venv" ]; then
    echo -e "${CYAN}🔧 Creando entorno virtual de Python...${NC}"
    $PYTHON_CMD -m venv .venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Error creando entorno virtual${NC}"
        exit 1
    fi
fi

# Activar entorno virtual
echo -e "${CYAN}🔄 Activando entorno virtual...${NC}"
source .venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Error activando entorno virtual${NC}"
    exit 1
fi

# Instalar dependencias de Python (si es necesario)
if [ ! -f ".venv/lib/python*/site-packages/fastapi" ]; then
    echo -e "${CYAN}📦 Instalando dependencias de Python...${NC}"
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Error instalando dependencias de Python${NC}"
        exit 1
    fi
fi

# Instalar Playwright Chromium (si es necesario)
if [ ! -d ".venv/lib/python*/site-packages/playwright" ]; then
    echo -e "${CYAN}🌐 Instalando Playwright Chromium...${NC}"
    playwright install chromium
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}⚠️ Advertencia: Error instalando Playwright${NC}"
    fi
fi

# Verificar e instalar dependencias de frontend
cd front

if [ ! -d "node_modules" ]; then
    echo -e "${CYAN}📦 Instalando dependencias de frontend...${NC}"
    npm install
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Error instalando dependencias de frontend${NC}"
        cd ..
        exit 1
    fi
fi

echo -e "${CYAN}🔨 Compilando frontend...${NC}"
npm run build
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Error compilando frontend${NC}"
    cd ..
    exit 1
fi

cd ..

echo ""
echo -e "${GREEN}🚀 Iniciando servidor...${NC}"
echo ""
echo -e "${BLUE}📱 Interfaces disponibles:${NC}"
echo -e "   - Local: http://localhost:5173"
echo -e "   - Red local: http://$(hostname -I | awk '{print $1}'):5173"
echo ""
echo -e "${YELLOW}💡 Para usar desde WhatsApp/OpenClaw:${NC}"
echo -e "   - Configura OpenClaw para ejecutar este script"
echo -e "   - Accede desde cualquier dispositivo en tu red"
echo ""
echo -e "${YELLOW}⏹️ Para detener: Presiona Ctrl+C${NC}"
echo ""

# Obtener todas las IPs locales
echo -e "${CYAN}🌐 También disponible en:${NC}"
hostname -I | tr ' ' '\n' | grep -E "^192\.|^10\.|^172\." | head -3 | while read ip; do
    echo -e "   - http://$ip:5173"
done

echo ""

# Función para manejar la señal SIGINT (Ctrl+C)
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Deteniendo servidor...${NC}"
    exit 0
}

# Registrar la función de limpieza para SIGINT
trap cleanup SIGINT

# Iniciar servidor FastAPI
$PYTHON_CMD run_server.py

echo ""
echo -e "${YELLOW}🛑 Servidor detenido${NC}"