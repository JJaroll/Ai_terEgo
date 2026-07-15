# 🎙️ (AI)terEgo (Python + PyTorch)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-red) ![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey) ![License](https://img.shields.io/badge/License-MIT-green) ![Version](https://img.shields.io/badge/Version-1.1.0-blue)

**(AI)terEgo** es una aplicación de avatar virtual inteligente y moderna escrita en Python. A diferencia de los PNGTubers tradicionales que solo reaccionan al volumen, este proyecto utiliza **Inteligencia Artificial (Wav2Vec2)** para analizar tu tono de voz en tiempo real y cambiar la expresión de tu avatar automáticamente.

Ideal para streamers, creadores de contenido o simplemente para divertirse en Discord/Zoom.

## ✨ Características Principales

* **🧠 Cerebro IA Multi-Modelo:**
    *   **Español (SomosNLP):** Detecta *Neutral, Feliz, Triste, Enojado*.
    *   **Inglés/Global (XLS-R):** Detecta *Neutral, Feliz, Triste, Enojado, Sorpresa, Asco, Miedo*.
    *   *Nota: Puedes cambiar de modelo en tiempo real desde los Ajustes.*
* **🗣️ Lip Sync:** Movimiento de boca reactivo al volumen del micrófono.
* **🐇 Efectos Visuales:**
    *   **Rebote (Bounce):** El avatar salta sutilmente cuando hablas.
    *   **Sombra Suave:** Sombra realista debajo del avatar.
    *   **Efecto Espejo (Flip):** Voltea tu avatar instantáneamente.
* **🎨 Sistema de Skins (.ptuber):**
    *   Crea tus propios avatares con el **Creador Integrado**.
    *   Soporte para hasta **7 emociones** y estados de boca (cerrada/abierta).
    *   Importa y exporta skins fácilmente para compartir con amigos.
* **⚙️ Configuración Personalizable:**
    * **Pestaña Sistema:** Selector de modelo IA y control de actualizaciones automáticas.
    * **Atajos:** Configura teclas globales para cada emoción.
    * **Persistencia:** Guarda automáticamente tu micrófono, sensibilidad y colores.
    *   La aplicación puede minimizarse a la bandeja del sistema para ejecutarse en segundo plano sin estorbar.
* **🔋 Mejoras y Utilidades:**
    *   **Descarga Fácil:** Descarga y gestión de modelos IA con ventana de progreso integrada.
    *   **Persistencia:** Guarda automáticamente tu micrófono, sensibilidad, colores y perfiles elegidos.
    *   **Atajos Globales:** Controla todo a través de atajos de teclado configurables, sin necesidad de tener la ventana activa.
* **🖥️ Interfaz Moderna:**
    *   Ventana principal sin bordes (Frameless) con fondo transparente.
    *   **Notificaciones:** Alertas discretas tipo "pill" cuando hay actualizaciones nuevas.

---

## 📥 Descarga e Instalación (Binarios)

¡(AI)terEgo está disponible de forma nativa para todas las plataformas! Elige la versión correspondiente a tu sistema operativo para descargar la aplicación lista para usar (no requiere Python).

### 🍎 macOS
* **Apple Silicon (M1 o superior):** [Descargar (AI)terEgo_Apple_Silicon.dmg](https://github.com/JJaroll/Ai_terEgo/releases/download/v1.0.0/AI.terEgo_Apple_Silicon.dmg)
* **Intel:** [Descargar (AI)terEgo_Intel.dmg](https://github.com/JJaroll/Ai_terEgo/releases/download/v1.0.0/AI.terEgo_Intel.dmg)
  > **Instalación:** Abre el archivo `.dmg` y arrastra la aplicación a tu carpeta de Aplicaciones. Al abrirla por primera vez, macOS te solicitará permisos para usar el micrófono; debes aceptarlos para que el avatar reaccione.

### 🪟 Windows
* **Versión CPU (Ligera - Recomendada):** [Descargar (AI)terEgo_CPU_Win-x64.zip](https://github.com/JJaroll/Ai_terEgo/releases/download/v1.0.0/AI.terEgo_CPU_Win-x64.zip)
* **Versión GPU (Nvidia CUDA):** [Descargar (AI)terEgo_GPU_Win-64.zip](https://drive.google.com/file/d/154DRv8xT6BG37Fc4wkSMSnRo75FLDeco/view?usp=sharing)
  > **Instalación:** Descomprime el archivo `.zip` en una carpeta de tu preferencia y ejecuta el archivo `.exe`. No requiere instalación en el sistema.

### 🐧 Linux
* **Instalador Ubuntu/Debian (.deb):** [Descargar (AI)terEgo_Linux.deb](https://drive.google.com/file/d/1M58WQORh9opAXnKeB_XMSg9TbYqwVaKT/view?usp=sharing)
  > **Instalación:** Ejecuta `sudo dpkg -i "(AI)terEgo_Linux.deb"` en tu terminal, o ábrelo con tu gestor de paquetes favorito (como GDebi).
* **Portable Universal (.tar.gz):** [Descargar (AI)terEgo_Linux.tar.gz](https://drive.google.com/file/d/1gDADFmzQ2V3r7FkVYRP3aJ6KtWv8xVfJ/view?usp=sharing)
  > **Instalación y Ejecución:** Esta versión no requiere instalación. Abre una terminal en la carpeta de descarga y ejecuta:
  > 1. `tar -xzf "(AI)terEgo_Linux.tar.gz"`
  > 2. `cd "(AI)terEgo"`
  > 3. `./"(AI)terEgo"`

*Nota Importante: La primera vez que abras la aplicación en cualquier sistema, podría tardar unos segundos adicionales (o mostrar una pantalla de carga) mientras los modelos de Inteligencia Artificial se descargan o se inicializan en la memoria de tu equipo.*

---

## 🛠️ Compilación desde el Código Fuente

Si eres desarrollador y prefieres correr o modificar el código fuente directamente:

### Requisitos Previos
* Python 3.10 o superior.
* Un micrófono.

### Pasos
1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/JJaroll/Ai_terEgo.git
    cd Ai_terEgo
    ```

2.  **Crear un entorno virtual (Recomendado):**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instalar dependencias:**
    *(Nota: PyTorch puede requerir una instalación específica según tu sistema. Revisa [pytorch.org](https://pytorch.org))*
    ```bash
    pip install -r requirements.txt
    ```
    *Si no tienes el archivo requirements.txt, las librerías principales son:*
    `PyQt6`, `torch`, `torchaudio`, `transformers`, `huggingface_hub`, `pyaudio`, `numpy`.

4.  **Instalar PyAudio (Si da error):**
    * **Windows:** `pip install pipwin && pipwin install pyaudio`
    * **macOS:** `brew install portaudio && pip install pyaudio`
    * **Linux:** `sudo apt-get install python3-pyaudio`

## 🚀 Uso

Ejecuta el archivo principal:

```bash
python main.py
```

## 🎨 Controles

*   **Clic Izquierdo + Arrastrar:** Mover al personaje por la pantalla.
*   **Clic Derecho:** Abrir el Menú Contextual (Ajustes rápidos).
*   **Esquina Inferior Derecha:** Redimensionar al personaje.
*   **Botones Inferiores (Dock):**
    *   🔊: Silenciar/Activar micrófono.
    *   🔄: Voltear Avatar Horizontalmente (Efecto Espejo).
    *   ⚙️: Abrir ventana de configuración completa.
    *   🤖: Activar **Modo IA** (Automático).
    *   😐, 😄, etc.: Forzar una emoción manualmente.
    *   *Nota: Las emociones no soportadas por el modelo actual aparecerán ocultas en un botón de expansión `›` pero activables manualmente.*

### Atajos de Teclado (Por defecto)
*   **1-4:** Emociones básicas (Neutral, Feliz, Triste, Enojado).
*   **7-9:** Emociones extra (Sorpresa, Miedo, Asco).
*   **X:** Activar Modo IA.
*   **M:** Mutear micrófono.
*   **Ctrl+F / Cmd+F:** Efecto Espejo (Flip Horizontal).

### Configuración Avanzada (Clic Derecho -> Ajustes)
Desde aquí puedes controlar todo:
*   **Sistema:** Cambiar Modelo IA (Español/Inglés), verificar actualizaciones.
*   **Audio:** Ajustar sensibilidad y umbral de silencio.
*   **Apariencia:** Cambiar color de fondo (Transparente/Chroma), activar sombra, etc.
*   **Avatar:** Gestionar y editar perfiles de Skins.
*   **Atajos:** Personalizar de manera global las teclas rápidas.

## 📁 Estructura del Proyecto

* **main.py:** Punto de entrada. Conecta la interfaz con la lógica.
* **core_systems.py:** El Cerebro. Contiene los hilos de Audio (PyAudio) y de Descarga e IA (Transformers).
* **background.py:** Gestiona el menú contextual visual del avatar.
* **profile_manager.py:** Lógica para guardar, cargar, importar y exportar skins (.ptuber).
* **profile_creator.py:** Interfaz GUI para la creación de avatares.
* **config_manager.py:** Sistema de guardado y persistencia (settings.json).
* **settings_window.py:** Gestión de la ventana de configuración completa.
* **ui_components.py:** Contiene los modales y componentes reusables de UI.
* **update_manager.py:** Verifica si existen actualizaciones en GitHub.
* **hotkey_manager.py:** Conecta las pulsaciones globales con acciones de la aplicación.

## 🤝 Contribuir

¡Las contribuciones son bienvenidas!

1.  Haz un **Fork** del proyecto.
2.  Crea una rama (`git checkout -b feature/NuevaFuncion`).
3.  Haz tus cambios y commits.
4.  Haz Push a la rama (`git push origin feature/NuevaFuncion`).
5.  Abre un **Pull Request**.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

Creado con ❤️ por **JJaroll**
