# Changelog

Todas las versiones, cambios notables y mejoras de este proyecto serán documentados en este archivo.

## [v1.2.0] - 2026-07-18
### Fixes & Mejoras
- **Instaladores Refinados:** Múltiples ajustes en los flujos de instalación. Soporte para Web Installer ligero en Windows (Inno Setup) y binarios empaquetados (PyInstaller) para macOS y Linux.
- **Selección de Hardware:** Implementación de asistente de instalación para elegir entre modo GPU (CUDA/NVIDIA) y modo CPU para optimizar la compatibilidad.
- **Mejoras Multiidioma en Configuración:** El instalador de Windows ahora detecta el idioma del sistema operativo (Inglés, Español o Japonés) e inicializa `config.json` nativamente.
- **Docker AppImage:** Aislamiento del entorno de compilación en Linux a través de un contenedor Docker para generar AppImages estables y evitar librerías host ruidosas.
- **Prevención de Bugs:** Solución al problema del anidamiento de carpetas generado por PyInstaller (`dist/AIterEgo/AIterEgo`) en macOS y Linux.
- **Arranque Seguro:** Lógica a prueba de fallos para arranques sin dispositivos de audio o entornos WSL, controlando y registrando excepciones para evitar cierres súbitos.

## [v1.1.1] - 2026-07-16
### Fixes
- Ajustes de estabilización rápida post-lanzamiento para los scripts de los instaladores.
- Soporte multiidioma añadido a la documentación técnica de los repositorios.

## [v1.1.0] - 2026-07-16
### Release Mayor
- Lanzamiento de la versión 1.1.0.
- Actualización mayor de la documentación y organización del repositorio.

## [v1.0.1] - 2026-02-25
### Empaquetado & Compilación
- Desarrollo y validación de los scripts de compilación `.yml` para automatizar los ejecutables (Windows GPU/CPU, Linux, y macOS Intel).
- Integración de script de creación de imágenes de disco `.dmg` para Apple.
- Separación correcta de entornos de desarrollo (ignorado de `venv` en `.gitignore`).

## [v1.0.0] - 2026-02-15 (y desarrollo inicial)
### Release Inicial & Funciones Base
- **Core de Inteligencia Artificial:** Integración de hilos asíncronos (`AudioMonitorThread` y `EmotionThread`) para inferir emociones a partir del reconocimiento de voz nativo en español.
- **Interfaz (UI):** Diseño estilizado inspirado en macOS. Implementación de una bandeja del sistema (System Tray), menús contextuales y controles flotantes con animaciones.
- **Gestión de Perfiles y Skins:** Módulo dedicado para leer, reparar, importar y exportar skins (PNGTuber) dinámicamente.
- **Atajos Globales:** Control manual mediante el teclado utilizando `multiprocessing` para interceptar comandos sin importar si la app está en primer plano.
- **Sistema de Preferencias:** Ventana de ajustes dedicada y persistencia en `settings.json` (sensibilidad de audio, comportamiento de la interfaz, opacidad y colores de fondo).
- **Widgets Dinámicos:** Integración de barras medidoras (píldoras de volumen), notificaciones de actualización y tutorial de onboarding.
