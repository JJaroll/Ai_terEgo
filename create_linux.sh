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
PKG_NAME="aiterego"
VERSION="1.1.0"
TAR_NAME="Ai_terEgo_Linux_CPU.tar.gz"
DEB_NAME="Ai_terEgo_Linux_CPU.deb"

cd "$(dirname "$0")"

# 1. Activación del Entorno (Asumimos venv clásico de Linux)
if [ -f "venv/bin/activate" ]; then
    echo "🐍 Activando entorno virtual..."
    source venv/bin/activate
else
    echo "⚠️  Aviso: No se encontró 'venv/bin/activate'. Asegúrate de tener las dependencias instaladas."
fi

echo "🚀 Iniciando proceso de empaquetado para LINUX..."

# 2. Limpieza
echo "🧹 Limpiando compilaciones anteriores..."
rm -rf build dist build_deb *.spec
rm -f "$TAR_NAME" "$DEB_NAME"

# 3. Compilación Base con PyInstaller
# En Linux no usamos icono en el .exe, lo manejamos desde el sistema operativo
echo "📦 Compilando binario con PyInstaller..."
python3 -m PyInstaller --noconfirm --onedir --windowed \
    --name "$APP_NAME" \
    --add-data "assets:assets" \
    --add-data "avatars:avatars" \
    --hidden-import numpy \
    "$ENTRY_POINT"

# ---------------------------------------------------------
# 4. CREACIÓN DEL ARCHIVO .TAR.GZ (PORTABLE)
# ---------------------------------------------------------
echo "🗜️ Generando paquete portable (.tar.gz)..."
cd dist
tar -czf "../$TAR_NAME" "$APP_NAME"
cd ..
echo "✅ Portable creado: $TAR_NAME"

# ---------------------------------------------------------
# 5. CREACIÓN DEL INSTALADOR .DEB (UBUNTU/DEBIAN)
# ---------------------------------------------------------
echo "💿 Generando instalador .deb..."
DEB_DIR="build_deb/${PKG_NAME}_${VERSION}_amd64"

# Crear estructura de carpetas de Linux
mkdir -p "$DEB_DIR/DEBIAN"
mkdir -p "$DEB_DIR/opt/$PKG_NAME"
mkdir -p "$DEB_DIR/usr/share/applications"
mkdir -p "$DEB_DIR/usr/share/pixmaps"
mkdir -p "$DEB_DIR/usr/bin"

# A. Copiar los archivos de la app a /opt/ (Estándar para apps de terceros)
cp -r dist/"$APP_NAME"/* "$DEB_DIR/opt/$PKG_NAME/"

# B. Crear script de lanzamiento global en /usr/bin/
cat << 'EOF' > "$DEB_DIR/usr/bin/$PKG_NAME"
#!/bin/bash
cd /opt/aiterego
exec "./(AI)terEgo" "$@"
EOF
chmod +x "$DEB_DIR/usr/bin/$PKG_NAME"

# C. Crear Acceso Directo (.desktop) para el Menú de Aplicaciones
cat << EOF > "$DEB_DIR/usr/share/applications/$PKG_NAME.desktop"
[Desktop Entry]
Version=$VERSION
Name=$APP_NAME
Comment=Avatar Virtual con Inteligencia Artificial
Exec=$PKG_NAME
Icon=$PKG_NAME
Terminal=false
Type=Application
Categories=AudioVideo;Utility;
EOF

# D. Copiar Icono (Usaremos IA.png de tus assets)
cp assets/IA.png "$DEB_DIR/usr/share/pixmaps/$PKG_NAME.png"

# E. Crear archivo de Control (Metadatos del paquete)
cat << EOF > "$DEB_DIR/DEBIAN/control"
Package: $PKG_NAME
Version: $VERSION
Section: utils
Priority: optional
Architecture: amd64
Depends: libportaudio2
Maintainer: JJaroll <https://github.com/JJaroll>
Description: $APP_NAME - Avatar Virtual Reactivo
 Una aplicacion de avatar virtual controlada por voz e Inteligencia Artificial
 que reacciona a tu tono de voz en tiempo real usando PyTorch.
EOF

# F. Construir el paquete .deb usando dpkg-deb
if command -v dpkg-deb &> /dev/null; then
    dpkg-deb --build "$DEB_DIR" > /dev/null
    mv "build_deb/${PKG_NAME}_${VERSION}_amd64.deb" "./$DEB_NAME"
    echo "✅ Instalador .deb creado: $DEB_NAME"
else
    echo "⚠️ Aviso: dpkg-deb no está instalado. El instalador .deb no pudo ser creado."
    echo "   (El .tar.gz sí fue creado correctamente)."
fi

echo "🎉 ¡Proceso finalizado! Revisa tu carpeta para ver los archivos de Linux."