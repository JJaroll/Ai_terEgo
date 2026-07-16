@echo off
:: Cambiar a codificación UTF-8 para que el ASCII y los acentos se rendericen bien
chcp 65001 >nul
title AIterEgo - Preparando Entorno de Inteligencia Artificial

echo     ╔══════════════════════════════════════════════════════════════════════╗
echo     ║                                                                      ║
echo     ║      ██╗     ██╗  █████╗ ██████╗  ██████╗ ██╗     ██╗                ║
echo     ║      ██║     ██║ ██╔══██╗██╔══██╗██╔═══██╗██║     ██║                ║
echo     ║      ██║     ██║ ███████║██████╔╝██║   ██║██║     ██║                ║
echo     ║ ██╗  ██║██╗  ██║ ██╔══██║██╔══██╗██║   ██║██║     ██║                ║
echo     ║ ╚█████╔╝╚█████╔╝ ██║  ██║██║  ██║╚██████╔╝███████╗███████╗           ║
echo     ║  ╚════╝  ╚════╝  ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝           ║
echo     ║                                                                      ║
echo     ║   (AI)terEgo v1.1.0 - "Dando vida a los píxeles."                    ║
echo     ║   GitHub: github.com/JJaroll                                         ║
echo     ║                                                                      ║
echo     ╚══════════════════════════════════════════════════════════════════════╝
echo.
echo ===================================================
echo  Configurando AIterEgo por primera vez...
echo  Por favor, no cierres esta ventana.
echo ===================================================

cd /d "%~dp0"

:: 1. Descomprimir Python Portable si no existe
if not exist "python\python.exe" (
    echo [1/4] Extrayendo motor de Python...
    powershell -command "Expand-Archive -Path 'python-embed.zip' -DestinationPath 'python' -Force"
    
    :: Habilitar 'import site' en el entorno portable
    powershell -command "(Get-Content .\python\python312._pth) -replace '#import site', 'import site' | Set-Content .\python\python312._pth"
    
    echo [2/4] Instalando gestor de descargas...
    curl -sSL https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    .\python\python.exe get-pip.py
    del get-pip.py
)

:: 2. Detección de Hardware (GPU vs CPU)
echo [3/4] Analizando hardware (Buscando GPU NVIDIA)...
wmic path win32_VideoController get name | findstr /i "NVIDIA" >nul

if %errorlevel%==0 (
    echo [INFO] Tarjeta NVIDIA detectada. Descargando motor CUDA (Pesado - 2.5GB)...
    .\python\python.exe -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
) else (
    echo [INFO] No se detectó NVIDIA dedicada. Descargando motor CPU (Ligero - 150MB)...
    .\python\python.exe -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
)

:: 3. Instalar librerías de AIterEgo
echo [4/4] Instalando dependencias del sistema...
findstr /v /i "torch" requirements.txt > requirements_win.txt
.\python\python.exe -m pip install -r requirements_win.txt
del requirements_win.txt

echo ===================================================
echo  ¡Instalación completada con éxito!
echo  Ya puedes iniciar AIterEgo desde tu escritorio.
echo ===================================================
timeout /t 5