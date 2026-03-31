@echo off
REM ============================================
REM Spotify Better Algorithm - OpenClaw Script
REM Para Windows - Automatización desde WhatsApp
REM ============================================

echo 🎵 Iniciando Spotify Better Algorithm...
echo.

REM Obtener directorio del script
set SCRIPT_DIR=%~dp0
set PROJECT_DIR=%SCRIPT_DIR%..

REM Cambiar al directorio del proyecto
cd /d "%PROJECT_DIR%"

echo 📁 Directorio del proyecto: %PROJECT_DIR%
echo.

REM Verificar si existe Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python no está instalado o no está en PATH
    echo 💡 Instala Python desde https://python.org
    pause
    exit /b 1
)

REM Verificar si existe Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Node.js no está instalado o no está en PATH
    echo 💡 Instala Node.js desde https://nodejs.org
    pause
    exit /b 1
)

echo ✅ Python y Node.js detectados
echo.

REM Verificar si existe el entorno virtual
if not exist ".venv" (
    echo 🔧 Creando entorno virtual de Python...
    python -m venv .venv
    if errorlevel 1 (
        echo ❌ Error creando entorno virtual
        pause
        exit /b 1
    )
)

REM Activar entorno virtual
echo 🔄 Activando entorno virtual...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Error activando entorno virtual
    pause
    exit /b 1
)

REM Instalar dependencias de Python (si es necesario)
if not exist ".venv\Lib\site-packages\fastapi" (
    echo 📦 Instalando dependencias de Python...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Error instalando dependencias de Python
        pause
        exit /b 1
    )
)

REM Instalar Playwright Chromium (si es necesario)
if not exist ".venv\Lib\site-packages\playwright" (
    echo 🌐 Instalando Playwright Chromium...
    playwright install chromium
    if errorlevel 1 (
        echo ⚠️ Advertencia: Error instalando Playwright
    )
)

REM Verificar e instalar dependencias de frontend
cd front
if not exist "node_modules" (
    echo 📦 Instalando dependencias de frontend...
    npm install
    if errorlevel 1 (
        echo ❌ Error instalando dependencias de frontend
        cd ..
        pause
        exit /b 1
    )
)

echo 🔨 Compilando frontend...
npm run build
if errorlevel 1 (
    echo ❌ Error compilando frontend
    cd ..
    pause
    exit /b 1
)

cd ..

echo.
echo 🚀 Iniciando servidor...
echo.
echo 📱 Interfaces disponibles:
echo    - Local: http://localhost:5173
echo    - Red local: http://%COMPUTERNAME%:5173
echo.
echo 💡 Para usar desde WhatsApp/OpenClaw:
echo    - Configura OpenClaw para ejecutar este script
echo    - Accede desde cualquier dispositivo en tu red
echo.
echo ⏹️ Para detener: Presiona Ctrl+C
echo.

REM Obtener IP local para mostrar
for /f "tokens=2 delims=:" %%i in ('ipconfig ^| findstr /i "IPv4"') do (
    for /f "tokens=1" %%j in ("%%i") do (
        echo 🌐 También disponible en: http://%%j:5173
    )
)

echo.

REM Iniciar servidor FastAPI
python run_server.py

echo.
echo 🛑 Servidor detenido
pause