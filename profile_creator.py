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

import os
import shutil
import zipfile
import json
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QFileDialog, QMessageBox, QGridLayout, QScrollArea, QWidget)
from PyQt6.QtCore import Qt

from i18n import tr
from theme_manager import theme_manager

class ProfileCreatorDialog(QDialog):
    def __init__(self, parent=None, avatars_dir="avatars", edit_profile_name=None):
        super().__init__(parent)
        self.edit_mode = edit_profile_name is not None
        self.setStyleSheet(theme_manager.stylesheet())
        self.edit_profile_name = edit_profile_name

        title = tr("creator.edit_title", name=edit_profile_name) if self.edit_mode else tr("creator.create_title")
        self.setWindowTitle(title)
        self.resize(500, 600)
        self.avatars_dir = avatars_dir
        self.selected_files = {}

        self.layout = QVBoxLayout(self)

        # Sección 1: Nombre
        self.layout.addWidget(QLabel(tr("creator.name_label")))
        self.name_input = QLineEdit()

        if self.edit_mode:
            self.name_input.setText(edit_profile_name)
            self.name_input.setReadOnly(True)
            self.name_input.setEnabled(False)
        else:
            self.name_input.setPlaceholderText(tr("creator.name_placeholder"))

        self.layout.addWidget(self.name_input)

        self.layout.addSpacing(10)
        self.layout.addWidget(QLabel(tr("creator.assign_images")))

        # Sección 2: Grid
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { background: transparent; }")
        content = QWidget()
        content.setStyleSheet("background-color: transparent;")
        self.grid = QGridLayout(content)

        self.slots = [
            (f"{tr('emotion.neutral')} - {tr('state.closed')}", "neutral_closed"),
            (f"{tr('emotion.neutral')} - {tr('state.open')}", "neutral_open"),
            (f"{tr('emotion.happy')} - {tr('state.closed')}", "happy_closed"),
            (f"{tr('emotion.happy')} - {tr('state.open')}", "happy_open"),
            (f"{tr('emotion.angry')} - {tr('state.closed')}", "angry_closed"),
            (f"{tr('emotion.angry')} - {tr('state.open')}", "angry_open"),
            (f"{tr('emotion.sad')} - {tr('state.closed')}", "sad_closed"),
            (f"{tr('emotion.sad')} - {tr('state.open')}", "sad_open"),
            (f"{tr('emotion.surprise')} - {tr('state.closed')}", "surprise_closed"),
            (f"{tr('emotion.surprise')} - {tr('state.open')}", "surprise_open"),
            (f"{tr('emotion.disgust')} - {tr('state.closed')}", "disgust_closed"),
            (f"{tr('emotion.disgust')} - {tr('state.open')}", "disgust_open"),
            (f"{tr('emotion.fear')} - {tr('state.closed')}", "fear_closed"),
            (f"{tr('emotion.fear')} - {tr('state.open')}", "fear_open"),
        ]

        self.labels = {}
        for i, (text, key) in enumerate(self.slots):
            self.grid.addWidget(QLabel(text), i, 0)
            lbl_status = QLabel(tr("creator.no_image"))
            lbl_status.setStyleSheet("color: gray; font-style: italic;")
            self.labels[key] = lbl_status
            self.grid.addWidget(lbl_status, i, 1)
            btn = QPushButton(tr("creator.select_btn"))
            btn.clicked.connect(lambda _, k=key: self.select_image(k))
            self.grid.addWidget(btn, i, 2)

        scroll.setWidget(content)
        self.layout.addWidget(scroll)

        # Pre-cargar imágenes si estamos editando
        if self.edit_mode:
            self.load_existing_images()

        # Sección 3: Botones
        btns = QHBoxLayout()
        cancel_btn = QPushButton(tr("common.cancel"))
        cancel_btn.clicked.connect(self.reject)

        btn_text = tr("creator.save_changes") if self.edit_mode else tr("creator.save_create")
        save_btn = QPushButton(btn_text)
        save_btn.setStyleSheet("background-color: #28C840; color: white; font-weight: bold; padding: 6px;")
        save_btn.clicked.connect(self.save_profile)

        btns.addWidget(cancel_btn)
        btns.addWidget(save_btn)
        self.layout.addLayout(btns)

    def load_existing_images(self):
        profile_path = os.path.join(self.avatars_dir, self.edit_profile_name)
        if not os.path.exists(profile_path): return

        for _, key in self.slots:
            img_path = os.path.join(profile_path, f"{key}.PNG")
            if os.path.exists(img_path):
                self.selected_files[key] = img_path
                self.labels[key].setText(tr("creator.current_image"))
                self.labels[key].setStyleSheet("color: #00E64D; font-weight: bold;")

    def select_image(self, key):
        path, _ = QFileDialog.getOpenFileName(self, tr("creator.select_png_title"), "", tr("creator.png_filter"))
        if path:
            self.selected_files[key] = path
            filename = os.path.basename(path)
            self.labels[key].setText(tr("creator.new_image", filename=filename))
            self.labels[key].setStyleSheet("color: #00E64D; font-weight: bold;")

    def save_profile(self):
        # --- Verificación de límite ---
        if not self.edit_mode:
            current_skins = [d for d in os.listdir(self.avatars_dir) if os.path.isdir(os.path.join(self.avatars_dir, d))]
            user_skins = [p for p in current_skins if p != "Default"]
            if len(user_skins) >= 12:
                QMessageBox.warning(self, tr("creator.limit_title"), tr("creator.limit_msg"))
                return

        name = self.name_input.text().strip()
        if not name:
            return QMessageBox.warning(self, tr("common.error"), tr("creator.name_required"))

        target_dir = os.path.join(self.avatars_dir, name)

        if not self.edit_mode and os.path.exists(target_dir):
            return QMessageBox.warning(self, tr("common.error"), tr("creator.name_exists"))

        has_neutral = ("neutral_closed" in self.selected_files and "neutral_open" in self.selected_files)

        if not has_neutral:
             return QMessageBox.warning(self, tr("creator.incomplete_title"), tr("creator.incomplete_msg"))

        try:
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            # Copiar imágenes
            for _, key in self.slots:
                if key in self.selected_files:
                    src = self.selected_files[key]
                    dst = os.path.join(target_dir, f"{key}.PNG")

                    # Evitar copiarse a sí mismo si no ha cambiado
                    if os.path.abspath(src) != os.path.abspath(dst):
                         shutil.copy2(src, dst)

            msg = tr("creator.update_success") if self.edit_mode else tr("creator.create_success", name=name)
            QMessageBox.information(self, tr("common.success"), msg)

            # Solo preguntar exportar si es nuevo
            if not self.edit_mode:
                reply = QMessageBox.question(
                    self, tr("creator.export_prompt_title"),
                    tr("creator.export_prompt_msg"),
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )

                if reply == QMessageBox.StandardButton.Yes:
                    self.export_ptuber(name, target_dir)

            self.accept()
        except Exception as e:
            QMessageBox.critical(self, tr("download.error_title"), tr("creator.save_fatal_error", error=e))

    def export_ptuber(self, name, source_dir):
        save_path, _ = QFileDialog.getSaveFileName(
            self, tr("creator.save_compact_title"), f"{name}.ptuber", tr("skin.filter")
        )
        if not save_path: return

        try:
            meta = { "name": name, "version": "1.0", "author": "Usuario" }
            meta_path = os.path.join(source_dir, "meta.json")
            with open(meta_path, "w") as f:
                json.dump(meta, f, indent=4)

            with zipfile.ZipFile(save_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(meta_path, "meta.json")
                for filename in os.listdir(source_dir):
                    if filename.endswith(".PNG") or filename.endswith(".png"):
                        zipf.write(os.path.join(source_dir, filename), filename)

            os.remove(meta_path)
            QMessageBox.information(self, tr("creator.exported_title"), tr("creator.exported_msg", path=save_path))

        except Exception as e:
            QMessageBox.critical(self, tr("creator.export_error_title"), tr("creator.export_fatal_error", error=e))
