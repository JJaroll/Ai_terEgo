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

# --- CONFIGURACIÓN PARA INTEL ---
APP_NAME="(AI)terEgo"
ENTRY_POINT="main.py"
ICON_PATH="assets/app_icon.icns"
ENTITLEMENTS="entitlements.plist"
DMG_NAME="Ai_terego_Intel.dmg"
VENV_NAME="pngtuberIA_intel"
BACKGROUND_PATH="assets/dmg_background.png"

cd "$(dirname "$0")"

if [ -f "$VENV_NAME/bin/activate" ]; then
    echo "🐍 Activando entorno virtual ($VENV_NAME)..."
    source "$VENV_NAME/bin/activate"
else
    echo "❌ Error: No se encontró '$VENV_NAME/bin/activate'."
    exit 1
fi

echo "🚀 Iniciando proceso de empaquetado (INTEL x86_64) para $APP_NAME..."

rm -rf build dist *.spec
rm -f "$DMG_NAME"

# Se fuerza la arquitectura x86_64 para evitar cruces con binarios de Silicon
echo "📦 Compilando binario con PyInstaller..."
python3 -m PyInstaller --noconfirm --onedir --windowed --target-architecture x86_64 \
    --name "$APP_NAME" \
    --add-data "assets:assets" \
    --add-data "avatars:avatars" \
    --hidden-import numpy \
    --icon "$ICON_PATH" \
    "$ENTRY_POINT"

PLIST_PATH="dist/$APP_NAME.app/Contents/Info.plist"
if [ -f "$PLIST_PATH" ]; then
    echo "🎫 Configurando Info.plist..."
    plutil -insert NSMicrophoneUsageDescription -string "Se requiere acceso al micrófono para analizar tu voz en tiempo real." "$PLIST_PATH"
fi

echo "✍️  Firmando la App..."
codesign --force --deep --sign - --entitlements "$ENTITLEMENTS" "dist/$APP_NAME.app"

if command -v create-dmg &> /dev/null
then
    echo "💿 Generando DMG..."
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
    echo "❌ Error: Instala create-dmg"
    exit 1
fi