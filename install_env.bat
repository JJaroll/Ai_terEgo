@echo off
:: Cambiar a codificación UTF-8 para que el ASCII y los acentos se rendericen bien
chcp 65001 >nul
title AIterEgo - Preparando Entorno de Inteligencia Artificial
pushd "%~dp0"

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
set MODE=%1

:: 1. Preparación de entorno
.\python\python.exe -m venv venv 2>nul
if not exist "venv\Scripts\python.exe" (
    .\python\python.exe -m pip install virtualenv
    .\python\python.exe -m virtualenv venv
)

:: 2. Detección de hardware e instalación de PyTorch por partes
echo [1/3] Instalando PyTorch (%MODE%) con timeout extendido...
IF "%MODE%"=="GPU" (
    set "TORCH_INDEX=https://download.pytorch.org/whl/cu121"
) ELSE (
    set "TORCH_INDEX=https://download.pytorch.org/whl/cpu"
)

.\venv\Scripts\pip.exe install --default-timeout=600 torch --index-url %TORCH_INDEX%
.\venv\Scripts\pip.exe install --default-timeout=600 torchvision --index-url %TORCH_INDEX%
.\venv\Scripts\pip.exe install --default-timeout=600 torchaudio --index-url %TORCH_INDEX%

:: 3. Instalación de dependencias del sistema excluyendo torch
echo [2/3] Instalando dependencias del sistema...
if exist "requirements.txt" (
    findstr /v /i "torch" requirements.txt > requirements_win.txt
    .\venv\Scripts\pip.exe install -r requirements_win.txt
    del requirements_win.txt
)

:: 4. Parches de compatibilidad obligatorios (tokenizers + transformers 4.35)
echo [3/3] Aplicando parches de compatibilidad...
.\venv\Scripts\pip.exe install tokenizers==0.19.1 --only-binary=:all:
.\venv\Scripts\pip.exe install transformers==4.35.0 --no-deps
powershell -Command "(Get-Content 'venv\Lib\site-packages\transformers\dependency_versions_table.py') -replace '\"tokenizers\": \"tokenizers>=0.14,<0.15\"', '\"tokenizers\": \"tokenizers>=0.14,<=0.20\"' | Set-Content 'venv\Lib\site-packages\transformers\dependency_versions_table.py'"


:: 5. Limpieza final
echo [5/5] Limpieza final...
del /s /q "%USERPROFILE%\.cache\huggingface\hub\*"
echo ===================================================
echo  ¡Instalación completada con éxito!
echo  Ya puedes iniciar AIterEgo desde tu escritorio.
echo ===================================================
pause