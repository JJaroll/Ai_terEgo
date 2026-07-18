"""
(AI)terEgo - Settings Window
Ventana de configuración corregida para macOS y PyInstaller.
"""

import os
import sys
import platform
import numpy as np
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QComboBox, QSlider, QCheckBox, QTabWidget, QStyleFactory, QStyledItemDelegate, 
                             QWidget, QPushButton, QGroupBox, QFormLayout, 
                             QRadioButton, QButtonGroup, QScrollArea, QGridLayout, QFrame,
                             QTableWidget, QTableWidgetItem, QHeaderView, 
                             QMenu, QInputDialog, QMessageBox, QColorDialog)
from PyQt6.QtGui import QAction, QFont, QDesktopServices
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QUrl, QTimer
from PyQt6.QtGui import QPixmap, QIcon, QColor, QPainter, QPainterPath

from ui_components import PillProgressBar
from hotkey_gui import HotkeyRecorderDialog
from core_systems import SUPPORTED_MODELS, get_model_path
from i18n import tr, i18n, LANGUAGES
from theme_manager import theme_manager, THEME_ORDER

# --- WIDGET PERSONALIZADO: TARJETA DE AVATAR ---
class AvatarCard(QFrame):
    clicked = pyqtSignal(str) 
    rename_requested = pyqtSignal(str)
    edit_requested = pyqtSignal(str)
    delete_requested = pyqtSignal(str)

    def __init__(self, name, image_path, is_active, parent=None):
        super().__init__(parent)
        self.name = name
        self.setFixedSize(140, 180) 
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        c = theme_manager.colors()
        border_color = c['accent'] if is_active else c['group_border']
        bg_color = c['btn_hover'] if is_active else c['btn_bg']
        border_width = "2px" if is_active else "1px"
        
        self.setStyleSheet(f"""
            AvatarCard {{
                background-color: {bg_color};
                border: {border_width} solid {border_color};
                border-radius: 15px;
            }}
            AvatarCard:hover {{
                background-color: {c['tab_bg']};
                border: 2px solid {c['border']};
            }}
            QLabel {{ border: none; background: transparent; }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        self.img_lbl = QLabel()
        self.img_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        pix = QPixmap(image_path)
        if not pix.isNull():
            pix = pix.scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.img_lbl.setPixmap(pix)
        else:
            self.img_lbl.setText("❓")
            self.img_lbl.setStyleSheet("font-size: 40px;")
            
        layout.addWidget(self.img_lbl)

        self.name_lbl = QLabel(name)
        self.name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_lbl.setStyleSheet("font-weight: bold; color: white; font-size: 13px;")
        layout.addWidget(self.name_lbl)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.name)
        super().mousePressEvent(event)

    def show_context_menu(self, pos):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu { background-color: #333; color: white; border: 1px solid #555; }
            QMenu::item { padding: 5px 20px; }
            QMenu::item:selected { background-color: #007ACC; }
        """)
        
        rename_action = QAction(tr("avatar.rename"), self)
        rename_action.triggered.connect(lambda: self.rename_requested.emit(self.name))
        menu.addAction(rename_action)

        edit_action = QAction(tr("avatar.edit_images"), self)
        edit_action.triggered.connect(lambda: self.edit_requested.emit(self.name))
        menu.addAction(edit_action)

        if self.name != "Default":
            menu.addSeparator()
            delete_action = QAction(tr("avatar.delete_skin"), self)
            delete_action.triggered.connect(lambda: self.delete_requested.emit(self.name))
            menu.addAction(delete_action)
        
        menu.exec(self.mapToGlobal(pos))


# --- VENTANA PRINCIPAL DE AJUSTES ---
class SettingsDialog(QDialog):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.bg_manager = main_window.bg_manager
        self.fusion_style = QStyleFactory.create("Fusion")
        
        self.setMinimumSize(640, 520)
        saved_size = main_window.config_manager.get("settings_window_size", None)
        if isinstance(saved_size, list) and len(saved_size) == 2:
            self.resize(max(saved_size[0], 640), max(saved_size[1], 520))
        else:
            self.resize(700, 600)

        layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        import copy
        self.original_config = copy.deepcopy(self.main_window.config_manager.config_cache)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.save_btn = QPushButton()
        self.save_btn.clicked.connect(self.save_and_close)
        
        self.cancel_btn = QPushButton()
        self.cancel_btn.clicked.connect(self.cancel_and_close)
        
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        self.last_color_hex = "#00E64D"

        self.retranslate_ui()
        self.apply_theme()

        i18n.language_changed.connect(self.on_language_changed)
        theme_manager.theme_changed.connect(self.on_theme_changed)

    def save_and_close(self):
        self.main_window.config_manager._save_to_disk_actual()
        self.close()

    def cancel_and_close(self):
        self.main_window.config_manager.config_cache = self.original_config
        self.main_window.config_manager.save_timer.start()

        try:
            self.main_window.set_shadow_enabled(self.original_config.get("shadow_enabled", True))
            self.main_window.set_bounce_enabled(self.original_config.get("bounce_enabled", True))
            self.main_window.set_bounce_amplitude(self.original_config.get("bounce_amplitude", 10))
            self.main_window.set_bounce_speed(self.original_config.get("bounce_speed", 0.3))
            self.main_window.bg_manager.change_background(self.original_config.get("background_color", "transparent"))
            
            theme_manager.set_theme(self.original_config.get("theme", "dark"))
            i18n.set_language(self.original_config.get("language", "es"))
            
            self.main_window.set_always_on_top(self.original_config.get("always_on_top", True))
            
            if hasattr(self.main_window, 'audio_thread') and self.main_window.audio_thread:
                if self.main_window.audio_thread.device_index != self.original_config.get("microphone_index"):
                    self.main_window.update_microphone(self.original_config.get("microphone_index"))
            
            self.main_window.hotkey_manager.load_hotkeys()
            
            prof = self.original_config.get("current_profile", "Default")
            if prof != self.main_window.profile_manager.current_profile:
                self.main_window.bg_manager.change_profile(prof)

        except Exception as e:
            print(f"Error reverting config: {e}")

        self.close()

    def retranslate_ui(self):
        self.setWindowTitle(tr("settings.window_title"))

        current_tab_index = self.tabs.currentIndex()
        while self.tabs.count():
            widget = self.tabs.widget(0)
            self.tabs.removeTab(0)
            widget.deleteLater()

        self.tabs.addTab(self.create_audio_tab(), tr("tab.audio"))
        self.tabs.addTab(self.create_visual_tab(), tr("tab.appearance"))
        self.tabs.addTab(self.create_avatar_tab(), tr("tab.avatar"))
        self.tabs.addTab(self.create_hotkeys_tab(), tr("tab.hotkeys"))
        self.tabs.addTab(self.create_system_tab(), tr("tab.system"))
        self.tabs.addTab(self.create_about_tab(), tr("tab.about"))

        if 0 <= current_tab_index < self.tabs.count():
            self.tabs.setCurrentIndex(current_tab_index)

        self.save_btn.setText(tr("settings.save_close"))
        self.cancel_btn.setText(tr("common.cancel"))
        self.save_btn.setStyleSheet(theme_manager.close_button_style())
        self.cancel_btn.setStyleSheet(theme_manager.close_button_style())

    def apply_theme(self):
        self.setStyleSheet(theme_manager.stylesheet())
        self.save_btn.setStyleSheet(theme_manager.close_button_style())
        self.cancel_btn.setStyleSheet(theme_manager.close_button_style())

    def dim_color(self):
        return theme_manager.colors()['text_dim']

    def on_language_changed(self, lang):
        self.retranslate_ui()

    def on_theme_changed(self, theme_name):
        self.apply_theme()
        self.retranslate_ui()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.main_window.config_manager.set("settings_window_size", [self.width(), self.height()])

    def showEvent(self, event):
        self.main_window.audio_thread.audio_data_signal.connect(self.update_audio_bar)
        super().showEvent(event)

    def closeEvent(self, event):
        try:
            self.main_window.audio_thread.audio_data_signal.disconnect(self.update_audio_bar)
        except: pass
        try:
            i18n.language_changed.disconnect(self.on_language_changed)
        except: pass
        try:
            theme_manager.theme_changed.disconnect(self.on_theme_changed)
        except: pass
        super().closeEvent(event)

    def update_audio_bar(self, chunk):
        try:
            rms = np.sqrt(np.mean(chunk**2))
            level = int(rms * 500)
            level = min(100, max(0, level))

            if hasattr(self, 'audio_test_bar'):
                self.audio_test_bar.setValue(level)
                ok, mid, high, danger = theme_manager.level_colors()
                new_color = ok
                if level > 80: new_color = danger
                elif level > 60: new_color = high
                elif level > 40: new_color = mid

                if new_color != self.last_color_hex:
                    self.audio_test_bar.set_color_hex(new_color)
                    self.last_color_hex = new_color
        except: pass

    # --- PESTAÑA AUDIO ---
    def create_audio_tab(self):
        tab = QWidget()
        layout = QFormLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        self.mic_combo = QComboBox()
        self.mic_combo.setStyle(self.fusion_style)
        self.mic_combo.setItemDelegate(QStyledItemDelegate())
        devices = self.main_window.audio_thread.list_devices()
        current_idx = self.main_window.audio_thread.device_index
        idx_map = {}
        for i, (dev_idx, name) in enumerate(devices):
            self.mic_combo.addItem(f"{name[:35]}...", dev_idx)
            idx_map[dev_idx] = i 
        if current_idx in idx_map:
            self.mic_combo.setCurrentIndex(idx_map[current_idx])
        self.mic_combo.currentIndexChanged.connect(self.on_mic_changed)
        layout.addRow(tr("audio.device"), self.mic_combo)

        self.sens_slider = QSlider(Qt.Orientation.Horizontal)
        self.sens_slider.setRange(1, 50) 
        self.sens_slider.setValue(int(self.main_window.mic_sensitivity * 10))
        self.sens_label = QLabel(f"{self.main_window.mic_sensitivity:.1f}")
        self.sens_slider.valueChanged.connect(lambda v: self.on_sensitivity(v))
        sens_layout = QHBoxLayout()
        sens_layout.addWidget(self.sens_slider)
        sens_layout.addWidget(self.sens_label)
        layout.addRow(tr("audio.sensitivity"), sens_layout)

        self.thres_slider = QSlider(Qt.Orientation.Horizontal)
        self.thres_slider.setRange(1, 100) 
        self.thres_slider.setValue(int(self.main_window.audio_threshold * 1000))
        self.thres_label = QLabel(f"{self.main_window.audio_threshold:.3f}")
        self.thres_slider.valueChanged.connect(lambda v: self.on_threshold(v))
        thres_layout = QHBoxLayout()
        thres_layout.addWidget(self.thres_slider)
        thres_layout.addWidget(self.thres_label)
        layout.addRow(tr("audio.threshold"), thres_layout)
        layout.addRow(QLabel(" "))
        lbl_test = QLabel(tr("audio.test"))
        lbl_test.setStyleSheet("font-weight: bold;") 
        self.audio_test_bar = PillProgressBar()
        bar_container = QWidget()
        bar_layout = QHBoxLayout(bar_container)
        bar_layout.setContentsMargins(0, 0, 0, 0)
        bar_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter) 
        bar_layout.addWidget(self.audio_test_bar)
        layout.addRow(lbl_test, bar_container)
        return tab

    # --- PESTAÑA APARIENCIA ---
    def create_visual_tab(self):
        outer_tab = QWidget()
        outer_tab.setStyleSheet("background-color: transparent;")
        outer_layout = QVBoxLayout(outer_tab)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { background: transparent; }")
        
        tab = QWidget()
        tab.setStyleSheet("background-color: transparent;")
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        
        scroll.setWidget(tab)
        outer_layout.addWidget(scroll)
        
        bg_group = QGroupBox(tr("appearance.bg_group"))
        bg_layout = QVBoxLayout()

        self.bg_radios = QButtonGroup(self)

        opts = [
            (tr("appearance.bg.transparent"), "transparent"),
            (tr("appearance.bg.green"), "#07FD01"),
            (tr("appearance.bg.blue"), "#0000FE"),
            (tr("appearance.bg.semi"), "rgba(0, 0, 0, 100)")
        ]
        
        grid_opts = QGridLayout()
        row = 0
        col = 0
        
        for name, val in opts:
            rb = QRadioButton(name)
            self.bg_radios.addButton(rb)
            
            if self.main_window.current_background == val: 
                rb.setChecked(True)
                
            rb.toggled.connect(lambda checked, v=val: self.bg_manager.change_background(v) if checked else None)
            grid_opts.addWidget(rb, row, col)
            
            col += 1
            if col > 1:
                col = 0
                row += 1
        
        bg_layout.addLayout(grid_opts)

        custom_layout = QHBoxLayout()
        self.rb_custom = QRadioButton(tr("appearance.bg.custom"))
        self.bg_radios.addButton(self.rb_custom)

        current_bg = self.main_window.current_background
        is_standard = any(val == current_bg for _, val in opts)
        if not is_standard:
            self.rb_custom.setChecked(True)

        self.btn_pick_color = QPushButton(tr("appearance.pick_color"))
        self.btn_pick_color.setFixedSize(100, 35)
        self.btn_pick_color.setStyleSheet("")
        self.btn_pick_color.clicked.connect(self.open_color_picker)
        
        self.rb_custom.toggled.connect(lambda checked: self.btn_pick_color.setEnabled(True))

        custom_layout.addWidget(self.rb_custom)
        custom_layout.addWidget(self.btn_pick_color)
        custom_layout.addStretch()
        
        bg_layout.addLayout(custom_layout)
        bg_group.setLayout(bg_layout)
        layout.addWidget(bg_group)

        self.shadow_cb = QCheckBox(tr("appearance.shadow"))
        self.shadow_cb.setChecked(self.main_window.shadow_enabled)
        self.shadow_cb.toggled.connect(self.main_window.set_shadow_enabled)
        layout.addWidget(self.shadow_cb)

        bounce_group = QGroupBox(tr("appearance.bounce_group"))
        bounce_layout = QFormLayout()
        self.bounce_cb = QCheckBox(tr("appearance.bounce_enable"))
        self.bounce_cb.setChecked(self.main_window.bounce_enabled)
        self.bounce_cb.toggled.connect(self.main_window.set_bounce_enabled)
        bounce_layout.addRow(self.bounce_cb)
        self.amp_slider = QSlider(Qt.Orientation.Horizontal)
        self.amp_slider.setRange(0, 50)
        self.amp_slider.setValue(self.main_window.bounce_amplitude)
        self.amp_slider.valueChanged.connect(self.main_window.set_bounce_amplitude)
        bounce_layout.addRow(tr("appearance.bounce_force"), self.amp_slider)
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setRange(1, 20)
        self.speed_slider.setValue(int(self.main_window.bounce_speed * 10))
        self.speed_slider.valueChanged.connect(lambda v: self.main_window.set_bounce_speed(v/10))
        bounce_layout.addRow(tr("appearance.bounce_speed"), self.speed_slider)
        bounce_group.setLayout(bounce_layout)
        layout.addWidget(bounce_group)

        theme_group = QGroupBox(tr("appearance.theme_group"))
        theme_layout = QGridLayout()
        self.theme_radios = QButtonGroup(self)
        current_theme = self.main_window.config_manager.get("theme", "dark")

        theme_row, theme_col = 0, 0
        for theme_key in THEME_ORDER:
            rb = QRadioButton(tr(f"theme.{theme_key}"))
            self.theme_radios.addButton(rb)
            if theme_key == current_theme:
                rb.setChecked(True)
            rb.toggled.connect(lambda checked, t=theme_key: self.on_theme_selected(t) if checked else None)
            theme_layout.addWidget(rb, theme_row, theme_col)
            theme_col += 1
            if theme_col > 1:
                theme_col = 0
                theme_row += 1

        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)

        layout.addStretch()
        return outer_tab

    def on_theme_selected(self, theme_key):
        self.main_window.config_manager.set("theme", theme_key)
        theme_manager.set_theme(theme_key)

    def open_color_picker(self):
        color = QColorDialog.getColor(initial=QColor(self.main_window.current_background), parent=None, title=tr("appearance.color_dialog_title"), options=QColorDialog.ColorDialogOption.DontUseNativeDialog)
        if color.isValid():
            rgba = f"rgba({color.red()}, {color.green()}, {color.blue()}, {color.alpha()})"
            self.bg_manager.change_background(rgba)
            self.rb_custom.setChecked(True)

    # --- PESTAÑA AVATAR ---
    def create_avatar_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)

        lbl = QLabel(tr("avatar.title"))
        lbl.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(lbl)

        hint = QLabel(tr("avatar.hint"))
        hint.setStyleSheet(f"color: {self.dim_color()}; font-size: 11px; margin-bottom: 5px;")
        layout.addWidget(hint)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color: transparent;")
        
        self.grid_container = QWidget()
        self.grid_container.setStyleSheet("background-color: transparent;")
        self.avatar_grid = QGridLayout(self.grid_container)
        self.avatar_grid.setSpacing(15)
        self.avatar_grid.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        scroll.setWidget(self.grid_container)
        layout.addWidget(scroll)

        layout.addSpacing(10)

        self.btn_create = QPushButton(tr("avatar.create_new_count", count=0, limit=12))
        self.btn_create.setMinimumHeight(45)
        self.btn_create.setCursor(Qt.CursorShape.PointingHandCursor)
        c = theme_manager.colors()
        self.btn_create_style = f"""
            QPushButton {{
                background-color: {c['btn_bg']};
                border: 1px dashed {c['border']};
                border-radius: 10px;
                font-size: 14px;
                color: {c['text_dim']};
            }}
            QPushButton:hover {{
                background-color: {c['btn_hover']};
                color: {c['text']};
                border: 1px dashed {c['accent']};
            }}
        """
        self.btn_create.setStyleSheet(self.btn_create_style)
        self.btn_create.clicked.connect(self.open_creator_refresh)
        layout.addWidget(self.btn_create)

        h_layout = QHBoxLayout()
        btn_import = QPushButton(tr("avatar.import"))
        btn_import.clicked.connect(self.import_refresh)
        btn_export = QPushButton(tr("avatar.export"))
        btn_export.clicked.connect(self.bg_manager.export_current_skin)
        
        h_layout.addWidget(btn_import)
        h_layout.addWidget(btn_export)
        layout.addLayout(h_layout)

        self.refresh_avatar_grid()
        return tab

    def refresh_avatar_grid(self):
        for i in reversed(range(self.avatar_grid.count())): 
            self.avatar_grid.itemAt(i).widget().setParent(None)

        self.main_window.profile_manager.scan_profiles()
        profiles = self.main_window.profile_manager.profiles
        current_profile = self.main_window.profile_manager.current_profile
        root_folder = self.main_window.profile_manager.root_folder

        # Excluir 'Default' del conteo visual
        user_skins = [p for p in profiles if p != "Default"]
        count = len(user_skins)
        limit = 12
        if count >= limit:
            self.btn_create.setEnabled(False)
            self.btn_create.setText(tr("avatar.limit_reached", count=count, limit=limit))
            c = theme_manager.colors()
            self.btn_create.setStyleSheet(f"""
                QPushButton {{
                    background-color: {c['warn_bg']};
                    border: 1px solid {c['warn_border']};
                    border-radius: 10px;
                    font-size: 14px;
                    color: {c['warn_text']};
                }}
            """)
            self.btn_create.setToolTip(tr("avatar.limit_tooltip"))
        else:
            self.btn_create.setEnabled(True)
            self.btn_create.setText(tr("avatar.create_new_count", count=count, limit=limit))
            self.btn_create.setStyleSheet(self.btn_create_style)
            self.btn_create.setToolTip("")

        col_count = 3
        row = 0
        col = 0

        for profile in profiles:
            image_path = os.path.join(root_folder, profile, "neutral_open.PNG")
            if not os.path.exists(image_path):
                image_path = os.path.join(root_folder, profile, "neutral_closed.PNG")
            
            is_active = (profile == current_profile)
            
            card = AvatarCard(profile, image_path, is_active)
            card.clicked.connect(self.on_avatar_selected)
            card.rename_requested.connect(self.rename_avatar)
            card.edit_requested.connect(self.edit_avatar)
            card.delete_requested.connect(self.delete_avatar)
            
            self.avatar_grid.addWidget(card, row, col)
            
            col += 1
            if col >= col_count:
                col = 0
                row += 1

    def on_avatar_selected(self, profile_name):
        self.bg_manager.change_profile(profile_name)
        QTimer.singleShot(0, self.refresh_avatar_grid)
    
    def edit_avatar(self, profile_name):
        self.bg_manager.open_editor(profile_name)
        self.refresh_avatar_grid()
    
    def rename_avatar(self, old_name):
        new_name, ok = QInputDialog.getText(self, tr("avatar.rename_title"),
                                          tr("avatar.rename_label", name=old_name),
                                          text=old_name)

        if ok and new_name:
            new_name = new_name.strip()
            if not new_name: return
            if new_name == old_name: return

            success, msg = self.main_window.profile_manager.rename_profile(old_name, new_name)

            if success:
                if self.main_window.profile_manager.current_profile == new_name:
                     self.main_window.config_manager.set("current_profile", new_name)

                self.refresh_avatar_grid()
                QMessageBox.information(self, tr("common.success"), tr("avatar.rename_success", name=new_name))
            else:
                QMessageBox.warning(self, tr("common.error"), msg)

    def delete_avatar(self, profile_name):
        reply = QMessageBox.question(self, tr("avatar.delete_title"),
            tr("avatar.delete_confirm", name=profile_name),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            success, msg = self.main_window.profile_manager.delete_profile(profile_name)

            if success:
                if self.main_window.config_manager.get("current_profile") == profile_name:
                     self.main_window.config_manager.set("current_profile", "Default")

                self.refresh_avatar_grid()
                QMessageBox.information(self, tr("avatar.deleted_title"), tr("avatar.deleted_msg", name=profile_name))
            else:
                QMessageBox.warning(self, tr("common.error"), msg)

    def open_creator_refresh(self):
        self.bg_manager.open_creator()
        self.refresh_avatar_grid()

    def import_refresh(self):
        self.bg_manager.import_skin_dialog()
        self.refresh_avatar_grid()

    # --- PESTAÑA ATAJOS ---
    def create_hotkeys_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)

        lbl = QLabel(tr("hotkeys.description"))
        lbl.setStyleSheet(f"color: {self.dim_color()}; margin-bottom: 10px;")
        layout.addWidget(lbl)

        self.hotkey_table = QTableWidget()
        self.hotkey_table.setColumnCount(3)
        self.hotkey_table.setHorizontalHeaderLabels([tr("hotkeys.col_action"), tr("hotkeys.col_key"), ""])
        
        self.hotkey_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.hotkey_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.hotkey_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed) 
        self.hotkey_table.setColumnWidth(2, 130) 
        
        self.hotkey_table.verticalHeader().setDefaultSectionSize(45) 
        self.hotkey_table.verticalHeader().setVisible(False)
        self.hotkey_table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.hotkey_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        
        layout.addWidget(self.hotkey_table)

        self.refresh_hotkey_list()
        return tab

    def refresh_hotkey_list(self):
        self.hotkey_table.setRowCount(0)
        hotkeys = self.main_window.config_manager.get("hotkeys", {})
        
        friendly_names = {
            "mute_toggle": tr("hotkeys.mute_toggle"),
            "ai_mode": tr("hotkeys.ai_mode"),
            "neutral": tr("hotkeys.neutral"),
            "disgust": tr("hotkeys.disgust"),
            "fear": tr("hotkeys.fear"),
            "happiness": tr("hotkeys.happiness"),
            "sadness": tr("hotkeys.sadness"),
            "anger": tr("hotkeys.anger"),
            "surprise": tr("hotkeys.surprise")
        }
        
        order = ["mute_toggle", "ai_mode", "neutral", "happiness", "sadness", "anger", "fear", "disgust", "surprise"]
        
        row = 0
        for action in order:
            if action in hotkeys:
                self.add_hotkey_row(row, action, friendly_names.get(action, action), hotkeys[action])
                row += 1
                
        for action, key in hotkeys.items():
            if action not in order:
                self.add_hotkey_row(row, action, friendly_names.get(action, action), key)
                row += 1

    def add_hotkey_row(self, row, action, name, key_str):
        self.hotkey_table.insertRow(row)
        
        item_name = QTableWidgetItem(name)
        item_name.setFlags(Qt.ItemFlag.ItemIsEnabled) 
        self.hotkey_table.setItem(row, 0, item_name)
        
        display_key = str(key_str).upper() if key_str else "---"
        item_key = QTableWidgetItem(display_key)
        item_key.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        item_key.setFlags(Qt.ItemFlag.ItemIsEnabled)
        
        c = theme_manager.colors()
        if key_str:
            item_key.setForeground(QColor(c['level_colors'][0]))
            item_key.setFont(self.get_bold_font())
        else:
            item_key.setForeground(QColor(c['text_dim']))

        self.hotkey_table.setItem(row, 1, item_key)

        btn = QPushButton(tr("hotkeys.change_btn"))
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFixedSize(100, 30)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['btn_bg']};
                border: 1px solid {c['btn_border']};
                border-radius: 4px;
                font-size: 12px;
                color: {c['btn_text']};
            }}
            QPushButton:hover {{
                background-color: {c['btn_hover']};
                border-color: {c['btn_hover_border']};
                color: {c['text']};
            }}
        """)
        btn.clicked.connect(lambda _, a=action: self.record_key(a))
        
        container = QWidget()
        l = QHBoxLayout(container)
        l.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l.setContentsMargins(0, 0, 0, 0)
        l.addWidget(btn)
        self.hotkey_table.setCellWidget(row, 2, container)

    def record_key(self, action):
        dialog = HotkeyRecorderDialog(self)
        if dialog.exec():
            new_key = dialog.key_result
            if new_key:
                self.main_window.hotkey_manager.update_hotkey(action, new_key)
                self.refresh_hotkey_list()

    def get_bold_font(self):
        f = self.font()
        f.setBold(True)
        return f

    def on_mic_changed(self, index):
        dev_index = self.mic_combo.currentData()
        self.main_window.set_microphone(dev_index)

    def on_sensitivity(self, val):
        real_val = val / 10.0
        self.sens_label.setText(f"{real_val:.1f}")
        self.main_window.set_mic_sensitivity(real_val)

    def on_threshold(self, val):
        real_val = val / 1000.0
        self.thres_label.setText(f"{real_val:.3f}")
        self.main_window.set_audio_threshold(real_val)

    def on_model_changed(self, index):
        key = self.model_combo.currentData()
        if key:
            self.main_window.change_ai_model(key)
            self.update_model_info(key)

    def update_model_info(self, model_key):
        model_config = SUPPORTED_MODELS.get(model_key)
        if not model_config: return

        # 1. Rutas
        if hasattr(self, 'lbl_model_path'):
            path = get_model_path(model_config["id"])
            if path:
                self.lbl_model_path.setText(f"📂 {path}")
                self.lbl_model_path.setToolTip(path)
                self.btn_open_model.setEnabled(True)
                self.current_model_path = path
            else:
                self.lbl_model_path.setText(tr("system.model_not_downloaded"))
                self.btn_open_model.setEnabled(False)
                self.current_model_path = None

        # 2. Emociones
        if hasattr(self, 'lbl_emotions'):
            emotions = ", ".join(model_config["avatar_states"])
            self.lbl_emotions.setText(tr("system.emotions_label", emotions=emotions))

    def open_model_folder(self):
        if hasattr(self, 'current_model_path') and self.current_model_path:
            QDesktopServices.openUrl(QUrl.fromLocalFile(self.current_model_path))

    # --- PESTAÑA SISTEMA ---
    def create_system_tab(self):
        tab = QWidget()
        outer_layout = QVBoxLayout(tab)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color: transparent;")
        outer_layout.addWidget(scroll)

        content = QWidget()
        content.setStyleSheet("background-color: transparent;")
        layout = QVBoxLayout(content)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        lang_group = QGroupBox(tr("system.language_group"))
        lang_layout = QFormLayout()
        self.lang_combo = QComboBox()
        self.lang_combo.setStyle(self.fusion_style)
        self.lang_combo.setItemDelegate(QStyledItemDelegate())
        current_lang = self.main_window.config_manager.get("language", "es")
        for code, label in LANGUAGES.items():
            self.lang_combo.addItem(label, code)
            if code == current_lang:
                self.lang_combo.setCurrentIndex(self.lang_combo.count() - 1)
        self.lang_combo.currentIndexChanged.connect(self.on_language_selected)
        lang_layout.addRow(tr("system.language_label"), self.lang_combo)
        lang_group.setLayout(lang_layout)
        layout.addWidget(lang_group)

        window_group = QGroupBox(tr("system.window_group"))
        window_layout = QVBoxLayout()
        self.chk_always_on_top = QCheckBox(tr("system.always_on_top"))
        self.chk_always_on_top.setChecked(self.main_window.config_manager.get("always_on_top", True))
        self.chk_always_on_top.toggled.connect(lambda v: self.main_window.set_always_on_top(v))
        window_layout.addWidget(self.chk_always_on_top)
        window_group.setLayout(window_layout)
        layout.addWidget(window_group)

        ai_group = QGroupBox(tr("system.ai_group"))
        ai_layout = QFormLayout()

        self.model_combo = QComboBox()
        self.model_combo.setStyle(self.fusion_style)
        self.model_combo.setItemDelegate(QStyledItemDelegate())
        current_model = self.main_window.config_manager.get("ai_model", "spanish")

        for key, config in SUPPORTED_MODELS.items():
            self.model_combo.addItem(f"{config['name']}", key)
            if key == current_model:
                self.model_combo.setCurrentIndex(self.model_combo.count() - 1)

        self.model_combo.setMinimumWidth(400)

        self.model_combo.currentIndexChanged.connect(self.on_model_changed)

        ai_layout.addRow(tr("system.voice_model"), self.model_combo)
        lbl_info = QLabel(tr("system.model_note"))
        lbl_info.setStyleSheet(f"color: {self.dim_color()}; font-size: 11px; font-style: italic;")
        ai_layout.addRow("", lbl_info)

        self.lbl_model_path = QLabel(tr("system.loading_path"))
        self.lbl_model_path.setStyleSheet(f"color: {self.dim_color()}; font-family: monospace; font-size: 10px;")
        self.lbl_model_path.setWordWrap(True)

        self.btn_open_model = QPushButton("📂")
        self.btn_open_model.setFixedSize(30, 30)
        self.btn_open_model.setToolTip(tr("system.open_in_explorer"))
        self.btn_open_model.clicked.connect(self.open_model_folder)

        path_layout = QHBoxLayout()
        path_layout.addWidget(self.lbl_model_path)
        path_layout.addWidget(self.btn_open_model)

        ai_layout.addRow(QLabel(tr("system.model_path")))
        ai_layout.addRow(path_layout)

        self.lbl_emotions = QLabel()
        self.lbl_emotions.setWordWrap(True)
        self.lbl_emotions.setStyleSheet(f"color: {self.dim_color()}; font-size: 11px;")

        ai_layout.addRow(QLabel(tr("system.emotions_supported")))
        ai_layout.addRow(self.lbl_emotions)

        # Inicializar info con el modelo actual
        self.update_model_info(current_model)

        ai_group.setLayout(ai_layout)
        layout.addWidget(ai_group)

        path_group = QGroupBox(tr("system.project_location"))
        project_path_layout = QVBoxLayout()
        current_path = os.getcwd()
        lbl_path = QLabel(f"{current_path}")
        lbl_path.setWordWrap(True)
        lbl_path.setStyleSheet(f"color: {self.dim_color()}; font-family: monospace;")
        project_path_layout.addWidget(lbl_path)

        btn_open_folder = QPushButton(tr("system.open_folder"))
        btn_open_folder.setFixedSize(120, 30)
        btn_open_folder.clicked.connect(lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(current_path)))
        project_path_layout.addWidget(btn_open_folder)
        path_group.setLayout(project_path_layout)
        layout.addWidget(path_group)

        size_group = QGroupBox(tr("system.storage_group"))
        size_layout = QFormLayout()

        # Checkbox de actualizaciones
        self.chk_updates = QCheckBox(tr("system.check_updates"))
        self.chk_updates.setChecked(self.main_window.config_manager.get("check_updates", True))
        self.chk_updates.toggled.connect(lambda v: self.main_window.config_manager.set("check_updates", v))
        size_layout.addRow("", self.chk_updates)

        # --- Evitamos os.walk en modo empaquetado ---
        if getattr(sys, 'frozen', False):
            size_layout.addRow(tr("system.total_size"), QLabel(tr("system.calc_disabled")))
            size_layout.addRow(tr("system.files_count"), QLabel(tr("system.hidden_perf")))
        else:
            try:
                total_size = 0
                file_count = 0
                exclude_dirs = {'venv', '.git', '__pycache__', '.idea', '.vscode'}

                for dirpath, dirnames, filenames in os.walk(current_path):
                    dirnames[:] = [d for d in dirnames if d not in exclude_dirs]
                    for f in filenames:
                        fp = os.path.join(dirpath, f)
                        if not os.path.islink(fp):
                            total_size += os.path.getsize(fp)
                            file_count += 1

                size_str = f"{total_size / (1024*1024):.2f} MB"
                size_layout.addRow(tr("system.total_size"), QLabel(size_str))
                size_layout.addRow(tr("system.files_count"), QLabel(str(file_count)))
            except Exception as e:
                size_layout.addRow(tr("system.calc_status"), QLabel(tr("system.calc_error")))

        size_group.setLayout(size_layout)
        layout.addWidget(size_group)

        tech_group = QGroupBox(tr("system.env_group"))
        tech_layout = QFormLayout()

        tech_layout.addRow(tr("system.os_label"), QLabel(f"{platform.system()} {platform.release()}"))
        tech_layout.addRow(tr("system.arch_label"), QLabel(platform.machine()))
        tech_layout.addRow(tr("system.python_version_label"), QLabel(platform.python_version()))

        tech_group.setLayout(tech_layout)
        layout.addWidget(tech_group)

        layout.addStretch()

        scroll.setWidget(content)
        return tab

    def on_language_selected(self, index):
        code = self.lang_combo.currentData()
        if code:
            self.main_window.config_manager.set("language", code)
            i18n.set_language(code)

    # --- PESTAÑA ABOUT ---
    def create_about_tab(self):
        outer_tab = QWidget()
        outer_tab.setStyleSheet("background-color: transparent;")
        outer_layout = QVBoxLayout(outer_tab)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { background: transparent; }")
        
        tab = QWidget()
        tab.setStyleSheet("background-color: transparent;")
        layout = QVBoxLayout(tab)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(15)
        
        scroll.setWidget(tab)
        outer_layout.addWidget(scroll)

        icon_layout = QHBoxLayout()
        icon_layout.addStretch()

        lbl_icon = QLabel()
        lbl_icon.setFixedSize(128, 128)
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "IA.png")
        
        if os.path.exists(icon_path):
            pix = QPixmap(icon_path)
            if not pix.isNull():
                lbl_icon.setPixmap(pix.scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            else:
                lbl_icon.setText("🎙️")
                lbl_icon.setStyleSheet("font-size: 64px;")
        else:
            lbl_icon.setText("🎙️")
            lbl_icon.setStyleSheet("font-size: 64px;")

        lbl_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_layout.addWidget(lbl_icon)
        icon_layout.addStretch()
        
        layout.addLayout(icon_layout)

        c = theme_manager.colors()

        lbl_title = QLabel("(AI)terEgo")
        lbl_title.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {c['text']};")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_title)

        if hasattr(self.main_window, 'current_version'):
            version_text = tr("about.version", version=self.main_window.current_version)
        else:
            version_text = tr("about.version_unknown")

        lbl_ver = QLabel(version_text)
        lbl_ver.setStyleSheet(f"color: {c['text_dim']}; font-size: 14px;")
        lbl_ver.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_ver)

        lbl_desc = QLabel(tr("about.description"))
        lbl_desc.setWordWrap(True)
        lbl_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_desc.setStyleSheet(f"color: {c['text_dim']}; margin: 10px 0;")
        layout.addWidget(lbl_desc)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet(f"background-color: {c['border']};")
        layout.addWidget(line)

        lbl_credits = QLabel(tr("about.developed_by"))
        lbl_credits.setStyleSheet(f"color: {c['text']};")
        lbl_credits.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_credits)

        lbl_tech = QLabel(tr("about.powered_by"))
        lbl_tech.setStyleSheet(f"color: {c['text_dim']}; font-size: 11px;")
        lbl_tech.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_tech)

        lbl_license = QLabel(tr("about.license"))
        lbl_license.setStyleSheet(f"color: {c['text_dim']}; font-size: 11px; font-style: italic;")
        lbl_license.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_license)

        btn_terms = QPushButton("Terms of Service & Privacy Policy")
        btn_terms.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {c['text_dim']};
                border: none;
                font-size: 11px;
                font-style: italic;
                text-decoration: underline;
            }}
            QPushButton:hover {{ color: {c['text']}; }}
        """)
        btn_terms.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_terms.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/JJaroll/Ai_terEgo/blob/main/TERMS.md")))
        layout.addWidget(btn_terms, alignment=Qt.AlignmentFlag.AlignHCenter)

        layout.addSpacing(20)

        btn_kofi = QPushButton(tr("about.support_kofi"))
        btn_kofi.setFixedWidth(250)
        btn_kofi.setStyleSheet("""
            QPushButton {
                background-color: #FF5E5B;
                color: white;
                border: 1px solid #E04B48;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #ff7a77; }
        """)
        btn_kofi.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_kofi.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://ko-fi.com/jjaroll")))
        layout.addWidget(btn_kofi, alignment=Qt.AlignmentFlag.AlignHCenter)

        btn_github = QPushButton("💻 " + tr("about.view_github"))
        btn_github.setFixedWidth(250)
        btn_github.setStyleSheet("""
            QPushButton {
                background-color: #24292e;
                color: white;
                border: 1px solid #444;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #2f363d; }
        """)
        btn_github.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_github.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/JJaroll/Ai_terego")))

        btn_bug = QPushButton(tr("about.report_bug"))
        btn_bug.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {c['text_dim']};
                border: none;
                text-decoration: underline;
            }}
            QPushButton:hover {{ color: {c['text']}; }}
        """)
        btn_bug.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_bug.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/JJaroll/Ai_terEgo/issues/new")))

        layout.addWidget(btn_github, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(btn_bug, alignment=Qt.AlignmentFlag.AlignHCenter)

        layout.addStretch()
        return outer_tab