@echo off
:: Cambiar a codificación UTF-8 para que el ASCII y los acentos se rendericen bien
chcp 65001 >nul
title AIterEgo - Preparando Entorno de Inteligencia Artificial
pushd "%~dp0"

echo     ╔══════════════════════════════════════════════════════════════════════╗
echo     ║                                                                      ║
echo     ║      ██╗     ██╗  █████╗ ██████╗  ██████╗ ██╗     ██╗                ║
echo     ║      ██║     ██║ ██╔══██╗██╔══██╗██╔═══██╗██║     ██║                ║
echo     ║      ██║     ██║ ███████║██████╔╝██║   ██║██║     ██║                ║
echo     ║ ██╗  ██║██╗  ██║ ██╔══██║██╔══██╗██║   ██║██║     ██║                ║
echo     ║ ╚█████╔╝╚█████╔╝ ██║  ██║██║  ██║╚██████╔╝███████╗███████╗           ║
echo     ║  ╚════╝  ╚════╝  ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝           ║
echo     ║                                                                      ║
echo     ║   (AI)terEgo v1.2.0 - "Dando vida a los píxeles."                    ║
echo     ║   GitHub: github.com/JJaroll                                         ║
echo     ║                                                                      ║
echo     ╚══════════════════════════════════════════════════════════════════════╝
echo.
echo ===================================================
echo  Configurando AIterEgo por primera vez...
echo  Por favor, no cierres esta ventana.
echo ===================================================
echo AIterEgoを初めてセットアップしています...
echo このウィンドウを閉じないでください。
echo ===================================================
echo Setting up AIterEgo for the first time...
echo  Please do not close this window.
echo ===================================================


cd /d "%~dp0"
set MODE=%1

:: 1. DESCOMPRESIÓN DEL MOTOR PORTABLE
if not exist "python" mkdir python
echo Descomprimiendo motor Python...
echo Pythonエンジンをデプロイしています...
echo Deploying Python Engine...
powershell -Command "Expand-Archive -Path 'python-embed.zip' -DestinationPath 'python' -Force"

:: 2. HABILITAR PIP Y SITE-PACKAGES (El problema del ._pth)
echo Desbloqueando entorno portable...
echo ポータブル環境のロックを解除しています...
echo Unlocking Portable Environment...
(
echo python312.zip
echo .
echo import site
) > python\python312._pth

:: 3. BOOTSTRAP DE HERRAMIENTAS (Pip y Virtualenv)
echo Descargando instalador de pip...
echo pipインストーラーをダウンロードしています...
echo Downloading pip installer...
powershell -Command "Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -OutFile 'python\get-pip.py'"

echo Instalando pip...
echo pipをインストールしています...
echo Installing pip...
.\python\python.exe python\get-pip.py

echo Instalando virtualenv...
.\python\python.exe -m pip install virtualenv

:: 4. CREACIÓN DEL VENV
echo Creando entorno virtual...
echo バーチャル環境を作成しています...
echo Creating virtual environment...
.\python\python.exe -m virtualenv venv

:: 5. LÓGICA CONDICIONAL CPU/GPU
set "TORCH_URL=https://download.pytorch.org/whl/cpu"
if "%~1"=="GPU" (
    echo Instalando PyTorch en MODO GPU...
    echo PyTorchをGPUモードでインストールしています...
    echo Installing PyTorch in GPU MODE...
    set "TORCH_URL=https://download.pytorch.org/whl/cu124"
) else (
    echo Instalando PyTorch en MODO CPU...
    echo PyTorchをCPUモードでインストールしています...
    echo Installing PyTorch in CPU MODE...
)

:: 6. INSTALACIÓN DE DEPENDENCIAS (Orden seguro para evitar conflictos)
echo Instalando dependencias...
echo 依存関係をインストールしています...
echo Installing dependencies...
.\venv\Scripts\python.exe -m pip install -r requirements.txt

:: Luego los parches específicos de Windows
echo Aplicando parches de compatibilidad Windows...
echo Windows互換性パッチを適用しています...
echo Applying Windows compatibility patches...
.\venv\Scripts\python.exe -m pip install --force-reinstall transformers==4.41.2 tokenizers==0.19.1 huggingface-hub==0.23.0

:: 7. INSTALACIÓN DE TORCH CON URL ESPECÍFICA
echo Instalando motor de IA...
echo AIエンジンをインストールしています...
echo Installing AI engine...
.\venv\Scripts\python.exe -m pip install torch torchvision torchaudio --index-url %TORCH_URL%

:: 8. CIERRE SEGURO
echo ======================================
echo Configuración completada con éxito!
echo 設定が正常に完了しました！
echo Configuration completed successfully!
echo ======================================
echo Gracias por descargar (AI)terEgo
echo ありがとうございます (AI)terEgo
echo Thank you for downloading (AI)terEgo
echo ======================================
echo     ^<3 JJaroll
echo ======================================
pause