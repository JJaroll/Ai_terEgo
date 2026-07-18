"""
(AI)terEgo
-----------
Una aplicación de avatar virtual controlada por voz e Inteligencia Artificial.

Desarrollado por: JJaroll
GitHub: https://github.com/JJaroll
Fecha: 10/02/2026
Licencia: MIT
"""

__author__ = "JJaroll"
__version__ = "1.2.0"
__maintainer__ = "JJaroll"
__status__ = "Production"

import sys
import os
import torch

import platform
if platform.system() == "Windows":
    os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
    os.environ["HF_HUB_DISABLE_SYMLINKS"] = "1"

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"✅ Sistema iniciado en modo: {device.upper()}")

import multiprocessing
import numpy as np
import ctypes
from PyQt6.QtWidgets import (QApplication, QLabel, QMainWindow, QVBoxLayout, 
                             QWidget, QHBoxLayout, QSizeGrip, QGraphicsDropShadowEffect, 
                             QPushButton, QSizePolicy, QMessageBox, QSystemTrayIcon, QMenu, QSplashScreen)
from PyQt6.QtCore import Qt, QTimer, QUrl, QPoint, QPropertyAnimation, QEasingCurve, QSize
from PyQt6.QtGui import (QPixmap, QPainter, QColor, QTransform, QShortcut, 
                         QKeySequence, QDesktopServices, QPen, QFont, QBrush, QIcon, QAction)

# --- IMPORTS LOCALES ---
from profile_manager import AvatarProfileManager
from background import BackgroundManager
from mac_gui import MacWindowControls
from config_manager import ConfigManager
from hotkey_manager import HotkeyManager
from core_systems import AudioMonitorThread, EmotionThread, SUPPORTED_MODELS, ModelDownloaderThread, is_model_cached
from update_manager import UpdateChecker, CURRENT_VERSION
from settings_window import SettingsDialog
from ui_components import PillProgressBar, DownloadDialog, TutorialOverlay
from i18n import tr, i18n
from theme_manager import theme_manager

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class PNGTuberApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configuración
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
        self.current_version = CURRENT_VERSION

        # Idioma y Tema (deben establecerse antes de construir cualquier widget)
        i18n.language = self.config.get("language", "es")
        theme_manager.current = self.config.get("theme", "dark")
        i18n.language_changed.connect(self.retranslate_ui)

        # Estado
        self.current_emotion = "neutral"
        self.is_speaking = False
        self.is_muted = self.config.get("is_muted", False)
        self.mic_sensitivity = self.config.get("mic_sensitivity", 1.0)
        self.audio_threshold = self.config.get("audio_threshold", 0.02)
        
        # Visual
        self.bounce_enabled = self.config.get("bounce_enabled", True)
        self.bounce_amplitude = self.config.get("bounce_amplitude", 10)
        self.bounce_speed = self.config.get("bounce_speed", 0.3)
        self.bounce_phase = 0
        self.shadow_enabled = self.config.get("shadow_enabled", True)
        self.current_background = self.config.get("background_color", "transparent")
        self.is_flipped = False
        self.always_on_top = self.config.get("always_on_top", True)

        # Gestores
        self.profile_manager = AvatarProfileManager()
        profile_name = self.config.get("current_profile", "Default")
        self.profile_manager.set_profile(profile_name)

        self.init_ui()

        # Audio e IA
        saved_mic = self.config.get("microphone_index")
        try:
            self.audio_thread = AudioMonitorThread(device_index=saved_mic, threshold=self.audio_threshold, sensitivity=self.mic_sensitivity)
            self.audio_thread.volume_signal.connect(self.update_mouth)
            self.audio_thread.audio_data_signal.connect(self.handle_audio)
            self.audio_thread.start()
        except Exception as e:
            print(f"⚠️ Advertencia: No se pudo inicializar el audio (Modo WSL/Sin Micrófono): {e}")
            self.audio_thread = None

        self.emotion_thread = None
        QTimer.singleShot(100, self.check_initial_model)

        # Update Checker
        self.update_checker = None
        if self.config_manager.get("check_updates", True):
            self.update_checker = UpdateChecker()   
            self.update_checker.update_available.connect(self.on_update_found) 
            self.update_checker.start()

        # Animación
        self.bounce_timer = QTimer()
        self.bounce_timer.timeout.connect(self.animate_bounce)
        QTimer.singleShot(1000, lambda: self.bounce_timer.start(50)) 
 
        # Hotkeys
        self.ai_mode = True
        self.hotkey_manager = HotkeyManager(self.config_manager)
        self.hotkey_manager.hotkey_triggered.connect(self.handle_hotkey)
        QTimer.singleShot(1000, self.hotkey_manager.start_listening)
        
        self.update_avatar()

        # Timer para animación de "Thinking" (AI Mode)
        self.ai_pulse_timer = QTimer()
        self.ai_pulse_timer.timeout.connect(self.animate_ai_pulse)
        self.ai_pulse_alpha = 0
        self.ai_pulse_direction = 1

        self.flip_shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        self.flip_shortcut.activated.connect(self.toggle_flip)

        if not self.config.get("tutorial_completed", False):
            QTimer.singleShot(500, self.show_tutorial)

        # System Tray
        self.init_system_tray()
        self.will_quit = False
        self.tray_message_shown = False

    def init_ui(self):

        if os.name == 'nt':  # Si es Windows
            icon_name = "app_icon.ico"
        else:                # Si es macOS o Linux
            icon_name = "app_icon.icns"
            
        icon_path = resource_path(f"assets/{icon_name}")
        self.setWindowIcon(QIcon(icon_path))

        # Flags Cruciales para Mac
        self.setWindowFlags(self.base_window_flags())
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.resize(600, 600)
        self.setMinimumSize(600, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(5, 5, 5, 5)

        # --- BARRA SUPERIOR ---
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(13, 13, 13, 0) 
        
        # 1. Controles Mac
        self.mac_controls = MacWindowControls(self)
        self.mac_controls.close_signal.connect(self.close)
        self.mac_controls.minimize_signal.connect(self.showMinimized)
        top_bar.addWidget(self.mac_controls)
        
        # 2. Espacio flexible
        top_bar.addStretch()

        # 3. Botón de Actualización
        self.update_btn = QPushButton(tr("update.badge_default"))
        self.update_btn.setVisible(False) 
        self.update_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_btn.setFixedHeight(24)
        
        self.update_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 120);
                color: #ffffff;
                border: 1px solid rgba(255, 255, 255, 30);
                border-radius: 12px;
                padding-left: 10px;
                padding-right: 10px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 180);
                border: 1px solid rgba(255, 255, 255, 80);
            }
        """)
        self.update_btn.clicked.connect(self.confirm_update)
        
        top_bar.addWidget(self.update_btn)
        
        self.layout.addLayout(top_bar)

        # --- AVATAR ---
        self.avatar_label = QLabel(self)
        self.avatar_label.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
        self.avatar_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.layout.addWidget(self.avatar_label, 1)

        # --- DOCK INFERIOR ---
        self.bottom_container = QWidget()
        self.bottom_container.setFixedHeight(60)
        self.bottom_container.setStyleSheet("""
            QWidget {
                background-color: rgba(30, 30, 30, 220);
                border-radius: 30px;
                border: 1px solid rgba(255, 255, 255, 30);
            }
        """)
        
        bottom_layout = QHBoxLayout(self.bottom_container)
        bottom_layout.setContentsMargins(15, 5, 15, 5)
        bottom_layout.setSpacing(10)

        btn_style = """
            QPushButton { 
                background-color: rgba(255,255,255,200); 
                border-radius: 18px; 
                border: none;
                font-size: 16px;
            } 
            QPushButton:hover { background-color: rgba(255,255,255,255); }
            QPushButton:pressed { background-color: rgba(200,200,200,255); }
        """

        # --- GRUPO 1: UTILIDADES ---
        self.mute_btn = QPushButton("🔇" if self.is_muted else "🔊")
        self.mute_btn.setFixedSize(36, 36)
        self.mute_btn.setCheckable(True)
        self.mute_btn.setChecked(self.is_muted)
        self.mute_btn.setToolTip(tr("tooltip.mute"))
        self.mute_btn.setStyleSheet(btn_style + "QPushButton:checked { background-color: #ff5555; color: white; }")
        self.mute_btn.clicked.connect(lambda: self.set_muted(not self.is_muted)) # Fix Lambda logic
        bottom_layout.addWidget(self.mute_btn)

        self.flip_btn = QPushButton("🔄")
        self.flip_btn.setFixedSize(36, 36)
        self.flip_btn.setToolTip(tr("tooltip.flip"))
        self.flip_btn.setStyleSheet(btn_style)
        self.flip_btn.clicked.connect(self.toggle_flip)
        bottom_layout.addWidget(self.flip_btn)

        self.settings_btn = QPushButton("⚙️")
        self.settings_btn.setFixedSize(36, 36)
        self.settings_btn.setToolTip(tr("tooltip.settings"))
        self.settings_btn.setStyleSheet(btn_style)
        self.settings_btn.clicked.connect(self.open_settings_window)
        bottom_layout.addWidget(self.settings_btn)

        line = QWidget()
        line.setFixedSize(1, 25)
        line.setStyleSheet("background-color: rgba(255,255,255,50);")
        bottom_layout.addWidget(line)

        # --- GRUPO 2: EMOCIONES ---
        self.emotions_layout = QHBoxLayout() 
        self.emotions_layout.setSpacing(10)
        bottom_layout.addLayout(self.emotions_layout) 

        self.expand_btn = QPushButton("›")
        self.expand_btn.setFixedSize(24, 36)
        self.expand_btn.setToolTip(tr("tooltip.more_emotions"))
        self.expand_btn.setStyleSheet("""
            QPushButton { 
                background-color: rgba(255,255,255,50); 
                border-radius: 12px; 
                border: none;
                color: white;
                font-size: 20px;
                font-weight: bold;
                padding-bottom: 3px;
            } 
            QPushButton:hover { background-color: rgba(255,255,255,100); }
        """)
        self.expand_btn.clicked.connect(self.toggle_emotions_menu)
        bottom_layout.addWidget(self.expand_btn)

        self.extra_emotion_btns = [] 

        # --- GRUPO 3: VOLUMEN ---
        self.volume_bar = PillProgressBar()
        self.volume_bar.setFixedWidth(100)
        self.volume_bar._bg_color = QColor("#000000") 
        bottom_layout.addWidget(self.volume_bar)
        
        center_dock_layout = QHBoxLayout()
        center_dock_layout.addStretch()
        center_dock_layout.addWidget(self.bottom_container)
        center_dock_layout.addStretch()
        
        self.layout.addLayout(center_dock_layout)
        self.layout.addSpacing(10)

        self.last_color_hex = "#00E64D"

        self.shadow_effect = QGraphicsDropShadowEffect()
        self.shadow_effect.setBlurRadius(20)
        self.shadow_effect.setColor(QColor(0, 0, 0, 150))
        self.shadow_effect.setOffset(0, 5)
        self.set_shadow_enabled(self.shadow_enabled)

        self.sizegrip = QSizeGrip(self)
        self.sizegrip.setStyleSheet("QSizeGrip { background-color: transparent; width: 20px; height: 20px; }")

        self.bg_manager = BackgroundManager(self, self.profile_manager, self.config_manager)
        self.bg_manager.change_background(self.current_background)

    def update_dock_buttons(self):
        while self.emotions_layout.count():
            item = self.emotions_layout.takeAt(0)
            widget = item.widget()
            if widget: widget.deleteLater()

        self.extra_emotion_btns = []

        current_model_key = self.config_manager.get("ai_model", "spanish")
        model_data = SUPPORTED_MODELS.get(current_model_key)
        if model_data:
            supported_states = set(model_data["avatar_states"])
        else:
            supported_states = {"neutral"}

        master_emotions = [
            ("neutral", "😐", tr("emotion.neutral")),
            ("happy", "😄", tr("emotion.happy")),
            ("sad", "😢", tr("emotion.sad")),
            ("angry", "😠", tr("emotion.angry")),
            ("fear", "😨", tr("emotion.fear")),
            ("disgust", "🤢", tr("emotion.disgust")),
            ("surprise", "😲", tr("emotion.surprise"))
        ]

        base_style = """
            QPushButton { 
                background-color: rgba(255,255,255,200); 
                border-radius: 18px; 
                border: none;
                font-size: 16px;
            } 
            QPushButton:hover { background-color: rgba(255,255,255,255); }
        """
        
        disabled_style = """
            QPushButton { 
                background-color: rgba(60,60,60,150); 
                border-radius: 18px; 
                border: none;
                font-size: 16px;
                color: rgba(255,255,255,50);
            } 
        """

        self.btn_ai = QPushButton("🤖")
        self.btn_ai.setFixedSize(36, 36)
        self.btn_ai.setToolTip(tr("tooltip.ai_mode"))
        self.btn_ai.setStyleSheet(base_style)
        self.btn_ai.clicked.connect(lambda: self.handle_hotkey("ai_mode"))
        self.emotions_layout.addWidget(self.btn_ai)

        for state, icon, name in master_emotions:
            btn = QPushButton(icon)
            btn.setFixedSize(36, 36)
            btn.clicked.connect(lambda _, s=state: self.handle_hotkey(s))
            
            if state in supported_states:
                btn.setEnabled(True)
                btn.setToolTip(name)
                btn.setStyleSheet(base_style)
                self.emotions_layout.addWidget(btn)
            else:
                btn.setEnabled(False)
                btn.setToolTip(tr("tooltip.emotion_unavailable", name=name))
                btn.setStyleSheet(disabled_style)
                btn.setVisible(False)
                self.emotions_layout.addWidget(btn)
                self.extra_emotion_btns.append(btn)
        
        if hasattr(self, 'expand_btn'):
            self.expand_btn.setVisible(len(self.extra_emotion_btns) > 0)
            self.expand_btn.setText("›")
            self.expand_btn.setToolTip(tr("tooltip.more_emotions"))

    def toggle_flip(self):
        self.is_flipped = not self.is_flipped
        self.update_avatar()

    def open_settings_window(self):
        dialog = SettingsDialog(self)
        dialog.exec()

    def toggle_emotions_menu(self):
        if not self.extra_emotion_btns: return
        should_show = not self.extra_emotion_btns[0].isVisible()
        for btn in self.extra_emotion_btns:
            btn.setVisible(should_show)
            
        current_width = self.width()
        target_width = current_width
        
        if should_show:
            self.setMinimumWidth(750)
            self.expand_btn.setText("‹")
            self.expand_btn.setToolTip(tr("tooltip.less_emotions"))
            if current_width < 750:
                target_width = 750
        else:
            self.setMinimumWidth(600)
            self.expand_btn.setText("›")
            self.expand_btn.setToolTip(tr("tooltip.more_emotions"))
        
        if target_width != current_width:
            self.animation = QPropertyAnimation(self, b"size")
            self.animation.setDuration(300)
            self.animation.setStartValue(QSize(current_width, self.height()))
            self.animation.setEndValue(QSize(target_width, self.height()))
            self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
            self.animation.start()

    def animate_bounce(self):
        if self.bounce_enabled and self.is_speaking:
            self.bounce_phase += self.bounce_speed
            offset = int(abs(np.sin(self.bounce_phase)) * self.bounce_amplitude)
            self.avatar_label.setContentsMargins(0, 0, 0, offset)
        elif self.bounce_phase != 0:
            self.bounce_phase = 0
            self.avatar_label.setContentsMargins(0, 0, 0, 0)

    def animate_ai_pulse(self):
        if not self.ai_mode or not hasattr(self, 'btn_ai'):
            self.ai_pulse_timer.stop()
            return

        self.ai_pulse_alpha += 5 * self.ai_pulse_direction
        
        if self.ai_pulse_alpha >= 100:
            self.ai_pulse_alpha = 100
            self.ai_pulse_direction = -1
        elif self.ai_pulse_alpha <= 0:
            self.ai_pulse_alpha = 0
            self.ai_pulse_direction = 1
            
        glow_color = f"rgba(0, 200, 255, {self.ai_pulse_alpha})"
        border_color = f"rgba(255, 255, 255, {50 + self.ai_pulse_alpha})"
        
        style = f"""
            QPushButton {{ 
                background-color: rgba(255,255,255,200); 
                border-radius: 18px; 
                border: 2px solid {glow_color};
                background-color: {border_color};
                font-size: 16px;
            }} 
            QPushButton:hover {{ background-color: rgba(255,255,255,255); }}
        """
        self.btn_ai.setStyleSheet(style)

    def update_avatar(self):
        try:
            state = "open" if self.is_speaking else "closed"
            path = None
            if hasattr(self, 'profile_manager'):
                path = self.profile_manager.get_image_path(self.current_emotion, state)
            
            pix = None
            if path and isinstance(path, str):
                pix = QPixmap(path)
            
            if not pix or pix.isNull():
                pix = QPixmap(200, 200)
                pix.fill(QColor("transparent"))
                painter = QPainter(pix)
                painter.setBrush(QBrush(QColor(255, 50, 50, 150)))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawEllipse(10, 10, 180, 180)
                painter.setPen(QPen(QColor("white")))
                font = QFont("Arial", 40, QFont.Weight.Bold)
                painter.setFont(font)
                painter.drawText(pix.rect(), Qt.AlignmentFlag.AlignCenter, "?")
                painter.end()

            if self.is_flipped:
                pix = pix.transformed(QTransform().scale(-1, 1))

            w = self.avatar_label.width()
            h = self.avatar_label.height()
            if w > 0 and h > 0:
                self.avatar_label.setPixmap(pix.scaled(w, h, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
                
        except Exception as e:
            print(f"⚠️ Error controlado en update_avatar: {e}")
   
    def handle_audio(self, chunk):
        if not self.is_muted:
            if self.ai_mode and self.emotion_thread is not None:
                 self.emotion_thread.add_audio(chunk)

            try:
                rms = np.sqrt(np.mean(chunk**2))
                level = int(rms * 500) 
                level = min(100, max(0, level))
                
                self.volume_bar.setValue(level)

                ok, mid, high, danger = theme_manager.level_colors()
                new_color = ok
                if level > 80: new_color = danger
                elif level > 60: new_color = high
                elif level > 40: new_color = mid

                if new_color != self.last_color_hex:
                    self.volume_bar.set_color_hex(new_color)
                    self.last_color_hex = new_color

            except Exception: pass
        else:
            self.volume_bar.setValue(0)

    def update_mouth(self, speaking):
        if self.is_muted: speaking = False
        if self.is_speaking != speaking:
            self.is_speaking = speaking
            self.update_avatar()

    def update_emotion(self, emo):
        if self.ai_mode and self.current_emotion != emo:
            self.current_emotion = emo
            self.update_avatar()

    def handle_hotkey(self, action):
        print(f"Hotkey: {action}")
        
        if action == "mute_toggle":
            self.set_muted(not self.is_muted)
        elif action == "ai_mode":
            self.ai_mode = True
            self.current_emotion = "neutral"
            self.update_avatar()
            self.ai_pulse_timer.start(50)
            print("🤖 Modo IA Activado")
        else:
            alias_map = {
                "happiness": "happy",
                "sadness": "sad",
                "anger": "angry", 
                "neutral": "neutral",
                "fear": "fear",
                "disgust": "disgust",
                "surprise": "surprise"
            }
            target_state = alias_map.get(action, action)
            
            # Verificación más robusta
            current_model_key = self.config_manager.get("ai_model", "spanish")
            supported_states = []
            if current_model_key in SUPPORTED_MODELS:
                supported_states = SUPPORTED_MODELS[current_model_key]["avatar_states"]

            final_state = None
            if target_state:
                final_state = target_state
                if target_state not in supported_states:
                     print(f"⚠️ Emoción '{target_state}' no soportada oficialmente, forzando.")

            if final_state:
                self.ai_mode = False 
                self.ai_pulse_timer.stop()
                if hasattr(self, 'btn_ai'):
                    self.btn_ai.setStyleSheet("""
                        QPushButton { 
                            background-color: rgba(255,255,255,200); 
                            border-radius: 18px; 
                            border: none;
                            font-size: 16px;
                        } 
                        QPushButton:hover { background-color: rgba(255,255,255,255); }
                    """)
                self.current_emotion = final_state
                self.update_avatar()
            else:
                print(f"❌ Acción desconocida: {action}")

    def set_microphone(self, index):
        print(f"🎤 Cambiando micrófono a ID: {index}")
        self.audio_thread.change_device(index)
        self.config_manager.set("microphone_index", index)

    def set_mic_sensitivity(self, value):
        self.mic_sensitivity = value
        self.audio_thread.set_sensitivity(value)
        self.config_manager.set("mic_sensitivity", value)

    def check_initial_model(self):
        current_model_key = self.config_manager.get("ai_model", "spanish")
        model_config = SUPPORTED_MODELS.get(current_model_key, SUPPORTED_MODELS["spanish"])
        
        if not is_model_cached(model_config["id"]):
            print("🚀 Primera ejecución detectada: Descargando modelo...")
            self.start_model_download(current_model_key, model_config["name"], model_config["id"])
        else:
            self.start_emotion_system(current_model_key)

    def start_emotion_system(self, model_key):
        if self.emotion_thread is not None:
            self.emotion_thread.stop()
            
        self.emotion_thread = EmotionThread()
        self.emotion_thread.set_model(model_key)
        self.emotion_thread.emotion_signal.connect(self.update_emotion)
        self.emotion_thread.start()
        print(f"✅ Sistema de emociones iniciado con: {model_key}")
        self.config_manager.set("ai_model", model_key)
        self.update_dock_buttons()
        if self.ai_mode:
            self.ai_pulse_timer.start(50)

    def change_ai_model(self, model_key):
        model_config = SUPPORTED_MODELS.get(model_key)
        if not model_config: return

        if is_model_cached(model_config["id"]):
            self.start_emotion_system(model_key)
        else:
            self.start_model_download(model_key, model_config["name"], model_config["id"])

    def start_model_download(self, model_key, model_name, model_id):
        self.download_dialog = DownloadDialog(model_name, self)
        self.downloader = ModelDownloaderThread(model_id)
        
        self.downloader.finished_signal.connect(lambda success, msg: self.on_download_finished(success, msg, model_key))
        self.downloader.progress_update.connect(self.download_dialog.update_progress)
        self.downloader.log_update.connect(self.download_dialog.append_log)
        
        self.download_dialog.btn_cancel.clicked.connect(self.downloader.cancel)
        
        self.downloader.start()
        self.download_dialog.exec()

    def on_download_finished(self, success, msg, model_key):
        if hasattr(self, 'download_dialog'):
            self.download_dialog.close()
        
        if success:
            QMessageBox.information(self, tr("download.complete_title"), tr("download.complete_msg"))
            self.config_manager.set("ai_model", model_key)
            self.start_emotion_system(model_key)
        else:
            QMessageBox.critical(self, tr("download.error_title"), tr("download.error_msg", error=msg))

    def set_audio_threshold(self, value):
        self.audio_threshold = value
        self.audio_thread.set_threshold(value)
        self.config_manager.set("audio_threshold", value)

    def set_muted(self, muted):
        self.is_muted = muted
        self.mute_btn.setChecked(muted)
        self.mute_btn.setText("🔇" if muted else "🔊")
        self.config_manager.set("is_muted", muted)
        if muted:
            self.is_speaking = False
            self.update_avatar()

    def set_bounce_enabled(self, enabled):
        self.bounce_enabled = enabled
        self.config_manager.set("bounce_enabled", enabled)
        if not enabled:
            self.bounce_phase = 0
            self.avatar_label.setContentsMargins(0, 0, 0, 0)

    def set_bounce_amplitude(self, value):
        self.bounce_amplitude = value
        self.config_manager.set("bounce_amplitude", value)

    def set_bounce_speed(self, value):
        self.bounce_speed = value
        self.config_manager.set("bounce_speed", value)

    def base_window_flags(self):
        flags = Qt.WindowType.FramelessWindowHint
        if self.always_on_top:
            flags |= Qt.WindowType.WindowStaysOnTopHint
        return flags

    def set_always_on_top(self, enabled):
        self.always_on_top = enabled
        self.config_manager.set("always_on_top", enabled)

        was_visible = self.isVisible()
        self.setWindowFlags(self.base_window_flags())
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        if was_visible:
            self.show()

    def set_shadow_enabled(self, enabled):
        self.shadow_enabled = enabled
        self.config_manager.set("shadow_enabled", enabled)
        if enabled:
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(20)
            shadow.setColor(QColor(0, 0, 0, 150))
            shadow.setOffset(0, 5)
            self.avatar_label.setGraphicsEffect(shadow)
        else:
            self.avatar_label.setGraphicsEffect(None)

    def resizeEvent(self, event):
        rect = self.rect()
        self.sizegrip.move(rect.right() - self.sizegrip.width(), rect.bottom() - self.sizegrip.height())
        self.update_avatar()
        try:
            if hasattr(self, 'tutorial') and self.tutorial and self.tutorial.isVisible():
                self.tutorial.setGeometry(rect)
        except RuntimeError:
            self.tutorial = None
        super().resizeEvent(event)

    def contextMenuEvent(self, event):
        self.bg_manager.show_context_menu(event.pos())

    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(100, lambda: self.resize(self.width() + 1, self.height()))
        QTimer.singleShot(200, lambda: self.resize(self.width() - 1, self.height()))

    def closeEvent(self, event):
        if self.will_quit:
             self.stop_threads()
             event.accept()
        elif self.tray_icon.isVisible():
            tutorial_done = self.config_manager.get("tutorial_completed", False)
            if not tutorial_done and not self.tray_message_shown:
                QMessageBox.information(self, "(AI)terEgo",
                                        tr("app.tray_info_msg"))
                self.tray_message_shown = True
            self.hide()
            event.ignore()
        else:
            self.stop_threads()
            event.accept()

    def stop_threads(self):
        self.hotkey_manager.stop_listening()
        if hasattr(self, 'audio_thread') and self.audio_thread:
            self.audio_thread.stop()
        if self.emotion_thread:
            self.emotion_thread.stop()
        if self.update_checker: 
             self.update_checker.terminate()
    
    def quit_application(self):
        self.will_quit = True
        self.stop_threads()
        QApplication.quit()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_pos)
            event.accept()

    def show_update_dialog(self, url):
        msg = QMessageBox(self)
        msg.setWindowTitle(tr("update.tray_title"))
        msg.setText(tr("update.dialog_text"))
        msg.setInformativeText(tr("update.dialog_info"))
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setDefaultButton(QMessageBox.StandardButton.Yes)
        
        if msg.exec() == QMessageBox.StandardButton.Yes:
            QDesktopServices.openUrl(QUrl(url))

    def show_tutorial(self):
        self.tutorial = TutorialOverlay(self)
        self.tutorial.show()

    def mark_tutorial_completed(self):
        print("✅ Tutorial completado")
        self.config_manager.set("tutorial_completed", True)

    def init_system_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        # Icono seguro (P)
        painter = QPainter(pixmap)
        painter.setBrush(QBrush(QColor("#00E64D"))) 
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, 0, 32, 32)
        painter.setPen(QPen(QColor("white")))
        font = QFont("Arial", 20, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "A")
        painter.end()
        
        icon_path = resource_path("assets/tray_icon.png")
        self.tray_icon.setIcon(QIcon(icon_path))
        
        tray_menu = QMenu()

        self.tray_show_action = QAction(tr("tray.toggle_visibility"), self)
        self.tray_show_action.triggered.connect(self.toggle_window_visibility)
        tray_menu.addAction(self.tray_show_action)

        tray_menu.addSeparator()

        self.tray_mute_action = QAction(tr("tray.mute_mic"), self)
        self.tray_mute_action.setCheckable(True)
        self.tray_mute_action.setChecked(self.is_muted)
        self.tray_mute_action.triggered.connect(lambda c: self.set_muted(c))
        self.mute_btn.clicked.connect(lambda: self.tray_mute_action.setChecked(self.is_muted))
        tray_menu.addAction(self.tray_mute_action)

        self.tray_ai_action = QAction(tr("tray.ai_mode"), self)
        self.tray_ai_action.setCheckable(True)
        self.tray_ai_action.setChecked(self.ai_mode)
        self.tray_ai_action.triggered.connect(self.toggle_ai_mode_tray)
        tray_menu.addAction(self.tray_ai_action)

        tray_menu.addSeparator()

        self.tray_quit_action = QAction(tr("tray.quit"), self)
        self.tray_quit_action.triggered.connect(self.quit_application)
        tray_menu.addAction(self.tray_quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.show()

    def toggle_window_visibility(self):
        if self.isVisible():
            self.hide()
        else:
            self.showNormal()
            self.activateWindow()

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.toggle_window_visibility()

    def toggle_ai_mode_tray(self, checked):
        if checked:
            self.handle_hotkey("ai_mode")
        else:
             self.handle_hotkey("neutral")

    def retranslate_ui(self, lang=None):
        self.mute_btn.setToolTip(tr("tooltip.mute"))
        self.flip_btn.setToolTip(tr("tooltip.flip"))
        self.settings_btn.setToolTip(tr("tooltip.settings"))
        self.update_dock_buttons()

        if hasattr(self, 'pending_update_version'):
            self.update_btn.setText(tr("update.badge_found", version=self.pending_update_version))
        else:
            self.update_btn.setText(tr("update.badge_default"))

        if hasattr(self, 'tray_show_action'):
            self.tray_show_action.setText(tr("tray.toggle_visibility"))
            self.tray_mute_action.setText(tr("tray.mute_mic"))
            self.tray_ai_action.setText(tr("tray.ai_mode"))
            self.tray_quit_action.setText(tr("tray.quit"))

    def on_update_found(self, url, version):
        self.pending_update_url = url
        self.pending_update_version = version
        self.update_btn.setText(tr("update.badge_found", version=version))
        self.update_btn.setVisible(True)
        print(f"Update detected: {version}")

        if self.tray_icon.isVisible():
            self.tray_icon.showMessage(
                tr("update.tray_title"),
                tr("update.tray_msg", version=version),
                QSystemTrayIcon.MessageIcon.Information,
                3000
            )

    def confirm_update(self):
        msg = QMessageBox(self)
        msg.setWindowTitle(tr("update.tray_title"))
        msg.setText(tr("update.dialog_text"))
        msg.setInformativeText(tr("update.dialog_info"))
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setDefaultButton(QMessageBox.StandardButton.Yes)

        if msg.exec() == QMessageBox.StandardButton.Yes:
            if hasattr(self, 'pending_update_url'):
                QDesktopServices.openUrl(QUrl(self.pending_update_url))

def print_signature():
    if getattr(sys, 'frozen', False):
        import datetime
        print(f"=== (AI)terEgo v1.2.0 iniciado {datetime.datetime.now().isoformat(timespec='seconds')} ===")
        return

    signature = """
    ╔══════════════════════════════════════════════════════════════════════╗
    ║                                                                      ║
    ║      ██╗     ██╗  █████╗ ██████╗  ██████╗ ██╗     ██╗                ║
    ║      ██║     ██║ ██╔══██╗██╔══██╗██╔═══██╗██║     ██║                ║
    ║      ██║     ██║ ███████║██████╔╝██║   ██║██║     ██║                ║
    ║ ██╗  ██║██╗  ██║ ██╔══██║██╔══██╗██║   ██║██║     ██║                ║
    ║ ╚█████╔╝╚█████╔╝ ██║  ██║██║  ██║╚██████╔╝███████╗███████╗           ║
    ║  ╚════╝  ╚════╝  ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝           ║
    ║                                                                      ║
    ║   (AI)terEgo v1.2.0 - "Dando vida a los píxeles."                    ║
    ║   GitHub: github.com/JJaroll                                         ║
    ║                                                                      ║
    ╚══════════════════════════════════════════════════════════════════════╝
    """
    try:
        print(signature)
    except UnicodeEncodeError:
        # Si la consola de Windows no soporta los caracteres, simplemente lo ignoramos
        pass

def setup_app_environment():

    if getattr(sys, 'frozen', False):
        if sys.platform == "darwin":
            log_dir = os.path.join(os.path.expanduser("~"), "Library", "Logs", "AIterEgo")
        elif os.name == "nt":
            log_dir = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "AIterEgo", "Logs")
        else:
            log_dir = os.path.join(os.path.expanduser("~"), ".local", "share", "AIterEgo", "logs")

        try:
            os.makedirs(log_dir, exist_ok=True)
            log_path = os.path.join(log_dir, "aiterego.log")
            log_file = open(log_path, "a", encoding="utf-8", buffering=1)
            sys.stdout = log_file
            sys.stderr = log_file
        except Exception:
            # Si ni siquiera se puede abrir el log, no bloqueamos el arranque.
            sys.stdout = open(os.devnull, 'w', encoding='utf-8')
            sys.stderr = open(os.devnull, 'w', encoding='utf-8')

        current_dir = os.path.dirname(sys.executable)
        os.chdir(current_dir)

if __name__ == "__main__":
    import traceback  # Importamos traceback aquí para rastrear el error exacto
    
    try:
        multiprocessing.freeze_support()
        setup_app_environment()
        print_signature() 
        
        if os.name == 'nt':
            import ctypes
            myappid = u'jjaroll.aiterego.avatar.v1' 
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        
        app = QApplication(sys.argv)
        
        if os.name == 'nt':
            icon_path = resource_path("assets/app_icon.ico")
        else:
            icon_path = resource_path("assets/app_icon.icns")
        
        app_icon = QIcon(icon_path)
        app.setWindowIcon(app_icon)

        app.setQuitOnLastWindowClosed(False) 

        # ==========================================
        # 🚀 SPLASH SCREEN (VENTANA DE CARGA)
        # ==========================================
        splash_pix = QPixmap(resource_path("assets/IA.png"))
        splash_pix = splash_pix.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        
        splash = QSplashScreen(splash_pix, Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        splash.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        splash.show()
        
        app.processEvents() 
        
        window = PNGTuberApp()
        window.show()
        splash.finish(window)
        
        sys.exit(app.exec())
        
    except Exception as e:
        print("\n" + "="*50)
        print("🚨 ¡ERROR FATAL DETECTADO EN EL ARRANQUE! 🚨")
        print("="*50)
        traceback.print_exc()
        print("="*50)
        input("Presiona Enter para cerrar...") # Evita que WSL cierre la terminal de golpe
        sys.exit(1)