#!/bin/bash

# --- FIRMA DEL AUTOR ---
echo "    ╔══════════════════════════════════════════════════════════════════════╗"
echo "    ║                                                                      ║"
echo "    ║      ██╗     ██╗  █████╗ ██████╗  ██████╗ ██╗     ██╗                ║"
echo "    ║      ██║     ██║ ██╔══██╗██╔══██╗██╔═══██╗██║     ██║                ║"
echo "    ║      ██║     ██║ ███████║██████╔╝██║   ██║██║     ██║                ║"
echo "    ║ ██╗  ██║██╗  ██║ ██╔══██║██╔══██╗██║   ██║██║     ██║                ║"
echo "    ║ ╚█████╔╝╚█████╔╝ ██║  ██║██║  ██║╚██████╔╝███████╗███████╗           ║"
echo "    ║  ╚════╝  ╚════╝  ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝           ║"
echo "    ║                                                                      ║"
echo "    ║   (AI)terEgo v1.2.0 - \"Dando vida a los píxeles.\"                  ║"
echo "    ║   GitHub: github.com/JJaroll                                         ║"
echo "    ║                                                                      ║"
echo "    ╚══════════════════════════════════════════════════════════════════════╝"
echo ""
echo "==================================================="
echo " Preparando el entorno de AIterEgo..."
echo "==================================================="

# Asegurar que estamos en la carpeta correcta
cd "$(dirname "$0")"
APP_DIR="$HOME/.AIterEgo_Core"
mkdir -p "$APP_DIR"
cp -r * "$APP_DIR/" 2>/dev/null

cd "$APP_DIR"

# 1. Crear entorno y activar
echo "[1/4] Configurando entorno virtual..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip > /dev/null

# 2. Instalar IA detectando hardware
OS_NAME=$(uname -s)
echo "[2/4] Sistema detectado: $OS_NAME"

if [ "$OS_NAME" == "Linux" ]; then
    if command -v nvidia-smi &> /dev/null || lspci | grep -i nvidia &> /dev/null; then
        echo "[INFO] GPU NVIDIA detectada. Descargando CUDA..."
        pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
    else
        echo "[INFO] Usando motor de CPU para Linux..."
        pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
    fi
else
    echo "[INFO] Instalando motor IA para macOS..."
    pip install torch torchvision torchaudio
fi

# 3. Instalar requirements filtrando torch
echo "[3/4] Instalando dependencias del sistema..."
grep -iv "torch" requirements.txt > req_temp.txt
pip install -r req_temp.txt
rm req_temp.txt

# 4. Crear accesos nativos (.app para Mac, .desktop para Linux)
echo "[4/4] Creando accesos directos..."
if [ "$OS_NAME" == "Darwin" ]; then
    MAC_APP="$HOME/Applications/AIterEgo.app"
    mkdir -p "$MAC_APP/Contents/MacOS"
    mkdir -p "$MAC_APP/Contents/Resources"
    
    # Script ejecutable de la app
    echo "#!/bin/bash" > "$MAC_APP/Contents/MacOS/AIterEgo"
    echo "cd \"$APP_DIR\"" >> "$MAC_APP/Contents/MacOS/AIterEgo"
    echo "source venv/bin/activate" >> "$MAC_APP/Contents/MacOS/AIterEgo"
    echo "python3 main.py" >> "$MAC_APP/Contents/MacOS/AIterEgo"
    chmod +x "$MAC_APP/Contents/MacOS/AIterEgo"
    
    # Copiar icono
    cp assets/app_icon.icns "$MAC_APP/Contents/Resources/" 2>/dev/null
    echo "[INFO] AIterEgo instalado en tu carpeta de Aplicaciones."
elif [ "$OS_NAME" == "Linux" ]; then
    DESKTOP_FILE="$HOME/.local/share/applications/AIterEgo.desktop"
    mkdir -p "$HOME/.local/share/applications/"
    
    echo "[Desktop Entry]" > "$DESKTOP_FILE"
    echo "Type=Application" >> "$DESKTOP_FILE"
    echo "Name=AIterEgo" >> "$DESKTOP_FILE"
    echo "Exec=bash -c 'cd $APP_DIR && source venv/bin/activate && python3 main.py'" >> "$DESKTOP_FILE"
    echo "Icon=$APP_DIR/assets/IA.png" >> "$DESKTOP_FILE"
    echo "Categories=Utility;" >> "$DESKTOP_FILE"
    chmod +x "$DESKTOP_FILE"
    echo "[INFO] AIterEgo añadido a tu menú de aplicaciones."
fi

echo "==================================================="
echo " ¡Instalación completada con éxito!"
echo " Iniciando AIterEgo por primera vez..."
echo "==================================================="
python3 main.py