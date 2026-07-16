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
echo "    ║   (AI)terEgo v1.1.0 - \"Dando vida a los píxeles.\"                    ║"
echo "    ║   GitHub: github.com/JJaroll                                         ║"
echo "    ║                                                                      ║"
echo "    ╚══════════════════════════════════════════════════════════════════════╝"

# --- CONFIGURACIÓN ---
APP_NAME="(AI)terEgo"
ENTRY_POINT="main.py"
ICON_PATH="assets/app_icon.icns"
ENTITLEMENTS="entitlements.plist"
DMG_NAME="Ai_terego_Silicon.dmg"
VENV_NAME="pngtuberIA"

# Asegurar que el script se ejecute desde su propia ubicación
cd "$(dirname "$0")"

# --- ACTIVACIÓN DEL ENTORNO ---
if [ -f "$VENV_NAME/bin/activate" ]; then
    echo "🐍 Activando entorno virtual ($VENV_NAME)..."
    source "$VENV_NAME/bin/activate"
else
    echo "❌ Error: No se encontró '$VENV_NAME/bin/activate'. Revisa el nombre de tu carpeta de entorno."
    exit 1
fi

echo "🚀 Iniciando proceso de empaquetado para $APP_NAME..."

# 1. Limpieza
rm -rf build dist *.spec
rm -f "$DMG_NAME"

# 2. Compilación (Usando el módulo de python para asegurar compatibilidad)
echo "📦 Compilando binario con PyInstaller..."
python3 -m PyInstaller --noconfirm --onedir --windowed \
    --name "$APP_NAME" \
    --add-data "assets:assets" \
    --add-data "avatars:avatars" \
    --hidden-import numpy \
    --hidden-import pyaudio \
    --collect-all transformers \
    --icon "$ICON_PATH" \
    "$ENTRY_POINT"

# 3. Permisos de Micrófono (Info.plist)
PLIST_PATH="dist/$APP_NAME.app/Contents/Info.plist"
if [ -f "$PLIST_PATH" ]; then
    echo "🎫 Configurando Info.plist..."
    plutil -insert NSMicrophoneUsageDescription -string "Se requiere acceso al micrófono para analizar tu voz en tiempo real." "$PLIST_PATH"
fi

# 4. Firma Ad-hoc
echo "✍️  Firmando la App..."
codesign --force --deep --sign - --entitlements "$ENTITLEMENTS" "dist/$APP_NAME.app"

# 5. Creación del DMG
if command -v create-dmg &> /dev/null
then
    echo "💿 Generando DMG con acceso directo a Aplicaciones..."
    create-dmg \
      --volname "$APP_NAME Installer" \
      --volicon "$ICON_PATH" \
      --window-pos 200 120 \
      --window-size 600 400 \
      --icon-size 100 \
      --icon "$APP_NAME.app" 175 120 \
      --app-drop-link 425 120 \
      --hide-extension "$APP_NAME.app" \
      "$DMG_NAME" \
      "dist/$APP_NAME.app"
    
    echo "✅ ¡Listo! Instalador creado: ./$DMG_NAME"
else
    echo "❌ Error: Instala create-dmg con 'brew install create-dmg'"
    exit 1
fi