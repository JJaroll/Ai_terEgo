FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias base, compiladores y herramientas de AppImage
RUN apt-get update && apt-get install -y \
    python3-pip python3-venv binutils fuse libgl1-mesa-glx \
    libxcb1 libx11-xcb1 libxkbcommon-x11-0 libxcb-icccm4 \
    libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 \
    libxcb-shape0 libxcb-xfixes0 libxcb-xinerama0 libxcb-xkb1 \
    wget curl file portaudio19-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt pyinstaller
COPY . .

# Comando maestro: Compila y empaqueta en una sola línea
CMD ["bash", "-c", "pyinstaller --noconfirm --onedir --windowed --name AIterEgo --add-data 'assets:assets' --add-data 'avatars:avatars' --icon 'assets/IA.png' --collect-all transformers --hidden-import numpy --hidden-import pyaudio main.py && \
    mkdir -p AIterEgo.AppDir/usr/bin && \
    cp -r dist/AIterEgo/* AIterEgo.AppDir/usr/bin/ && \
    cp assets/IA.png AIterEgo.AppDir/IA.png && \
    ln -s usr/bin/AIterEgo AIterEgo.AppDir/AppRun && \
    printf '[Desktop Entry]\nType=Application\nName=AIterEgo\nExec=AIterEgo\nIcon=IA\nCategories=Utility;' > AIterEgo.AppDir/AIterEgo.desktop && \
    wget -q https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage && \
    chmod +x appimagetool-x86_64.AppImage && \
    ./appimagetool-x86_64.AppImage --appimage-extract-and-run AIterEgo.AppDir AIterEgo-Linux.AppImage"]