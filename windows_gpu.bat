@echo off
chcp 437 > nul
title AIterEgo - Compilador GPU (NVIDIA CUDA)
color 0B

echo.
echo ษออออออออออออออออออออออออออออออออออออออออออออออออออออออออออออออออออออออป
echo บ                                                                      บ
echo บ      ÛÛป     ÛÛป  ÛÛÛÛÛป ÛÛÛÛÛÛป  ÛÛÛÛÛÛป ÛÛป     ÛÛป                บ
echo บ      ÛÛบ     ÛÛบ ÛÛษออÛÛปÛÛษออÛÛปÛÛษอออÛÛปÛÛบ     ÛÛบ                บ
echo บ      ÛÛบ     ÛÛบ ÛÛÛÛÛÛÛบÛÛÛÛÛÛษผÛÛบ   ÛÛบÛÛบ     ÛÛบ                บ
echo บ ÛÛป  ÛÛบÛÛป  ÛÛบ ÛÛษออÛÛบÛÛษออÛÛปÛÛบ   ÛÛบÛÛบ     ÛÛบ                บ
echo บ ศÛÛÛÛÛษผศÛÛÛÛÛษผ ÛÛบ  ÛÛบÛÛบ  ÛÛบศÛÛÛÛÛÛษผÛÛÛÛÛÛÛปÛÛÛÛÛÛÛป           บ
echo บ  ศออออผ  ศออออผ  ศอผ  ศอผศอผ  ศอผ ศอออออผ ศออออออผศออออออผ           บ
echo บ                                                                      บ
echo บ   (AI)terEgo v1.1.0 - "Dando vida a los pกxeles."                    บ
echo บ   GitHub: github.com/JJaroll                                         บ
echo บ                                                                      บ
echo ศออออออออออออออออออออออออออออออออออออออออออออออออออออออออออออออออออออออผ
echo.

echo ===================================================
echo   Construyendo (AI)terEgo - Version GPU (NVIDIA)
echo ===================================================
echo.

echo [1/6] Verificando entorno virtual (venv_gpu)...
if not exist venv_gpu (
    echo Creando nuevo entorno virtual...
    python -m venv venv_gpu
)

echo.
echo [2/6] Activando entorno e instalando dependencias (CUDA)...
call venv_gpu\Scripts\activate.bat
python -m pip install --upgrade pip
echo Instalando PyTorch CUDA 12.1 (Para tarjetas NVIDIA)...
pip install torch==2.2.1+cu121 torchaudio==2.2.1+cu121 --index-url https://download.pytorch.org/whl/cu121
echo Instalando dependencias del sistema...
pip install "numpy<2" "transformers<4.40" pyaudio sounddevice librosa PyQt6 pyinstaller

echo.
echo [3/6] REPARACION AUTOMATICA DE ICONO (Multicapa)...
python -c "from PIL import Image; img=Image.open('assets/IA.png'); img.save('assets/app_icon.ico', format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])"

echo.
echo [4/6] Limpiando caches de compilacion...
if exist build rmdir /s /q build
if exist dist\AIterEgo_GPU rmdir /s /q dist\AIterEgo_GPU
if exist AIterEgo_GPU.spec del /f /q AIterEgo_GPU.spec

echo.
echo [5/6] Compilando con PyInstaller (Modo GPU)...
pyinstaller --clean --noconfirm --onedir --windowed --name "AIterEgo_GPU" ^
    --add-data "assets;assets" ^
    --add-data "avatars;avatars" ^
    --icon "assets/app_icon.ico" ^
    --hidden-import numpy ^
    --hidden-import pyaudio ^
    --hidden-import sounddevice ^
    --collect-all transformers ^
    main.py

echo.
echo [6/6] Comprimiendo la aplicacion en un archivo .zip para distribucion...
powershell -command "Compress-Archive -Path 'dist\AIterEgo_GPU' -DestinationPath 'Ai_terego_Windows_GPU.zip' -Force"

echo.
echo ========================================================
echo   Compilacion GPU finalizada con exito.
echo   Tu ejecutable esta en: dist\AIterEgo_GPU
echo.
echo   ADVERTENCIA: Esta carpeta pesara mas de 3 GB debido 
echo   a las librerias nativas de NVIDIA CUDA.
echo ========================================================
pause