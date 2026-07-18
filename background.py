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
from PyQt6.QtWidgets import QMenu, QWidget, QVBoxLayout, QLabel, QSlider, QWidgetAction, QFileDialog, QMessageBox
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt

from i18n import tr

class BackgroundManager:
    def __init__(self, main_window, profile_manager, config_manager):
        self.main_window = main_window
        self.profile_manager = profile_manager
        self.config_manager = config_manager
        self.central_widget = main_window.central_widget

    def show_context_menu(self, position):
        menu = QMenu(self.main_window)

        # 1. ACCIÓN RÁPIDA: MUTE
        mute_action = QAction(tr("menu.mute"), self.main_window)
        mute_action.setCheckable(True)
        mute_action.setChecked(self.main_window.is_muted)
        mute_action.triggered.connect(lambda checked: self.main_window.set_muted(checked))
        menu.addAction(mute_action)

        menu.addSeparator()

        # 2. SUBMENÚ: APARIENCIA / FONDO
        bg_menu = menu.addMenu(tr("menu.background"))

        # Opciones de apariencias
        actions = [
            (tr("appearance.bg.transparent"), "transparent"),
            (tr("appearance.bg.semi"), "rgba(0, 0, 0, 100)"),
            (tr("appearance.bg.green"), "#07FD01"),
            (tr("appearance.bg.blue"), "#0000FE")
        ]

        for name, color in actions:
            a = QAction(name, self.main_window)
            if color == self.main_window.current_background:
                a.setCheckable(True)
                a.setChecked(True)
            a.triggered.connect(lambda _, c=color: self.change_background(c))
            bg_menu.addAction(a)

        bg_menu.addSeparator()

        # Opción de Sombra
        shadow_action = QAction(tr("menu.shadow"), self.main_window)
        shadow_action.setCheckable(True)
        shadow_action.setChecked(self.main_window.shadow_enabled)
        shadow_action.triggered.connect(lambda checked: self.main_window.set_shadow_enabled(checked))
        bg_menu.addAction(shadow_action)

        # 3. SUBMENÚ: SKINS (Solo Lista)
        skin_menu = menu.addMenu(tr("menu.skins"))

        # Lista de perfiles
        self.profile_manager.scan_profiles()
        for profile in self.profile_manager.profiles:
            action = QAction(profile, self.main_window)
            if profile == self.profile_manager.current_profile:
                action.setCheckable(True)
                action.setChecked(True)
                # Resaltamos el perfil actual
                f = action.font()
                f.setBold(True)
                action.setFont(f)

            action.triggered.connect(lambda _, p=profile: self.change_profile(p))
            skin_menu.addAction(action)

        menu.addSeparator()

        # 4. SUBMENÚ: REBOTE (Solo Toggle)
        bounce_menu = menu.addMenu(tr("menu.bounce"))
        bounce_toggle = QAction(tr("appearance.bounce_enable"), self.main_window)
        bounce_toggle.setCheckable(True)
        bounce_toggle.setChecked(self.main_window.bounce_enabled)
        bounce_toggle.triggered.connect(lambda checked: self.main_window.set_bounce_enabled(checked))
        bounce_menu.addAction(bounce_toggle)

        menu.addSeparator()

        # 5. ACCESO A CONFIGURACIÓN COMPLETA
        settings_action = QAction(tr("menu.open_settings"), self.main_window)
        settings_action.triggered.connect(self.main_window.open_settings_window)
        menu.addAction(settings_action)

        menu.exec(self.main_window.mapToGlobal(position))

    # --- LÓGICA DE CAMBIOS ---
    def change_background(self, color):
        self.main_window.current_background = color

        if color == "transparent":
            self.central_widget.setStyleSheet("background: transparent;")
        else:
            # Si es semitransparente o color sólido, aplicamos estilo con bordes redondeados suaves
            self.central_widget.setStyleSheet(f"background-color: {color}; border-radius: 20px;")

        self.config_manager.set("background_color", color)

    def change_profile(self, profile_name):
        self.profile_manager.set_profile(profile_name)
        self.main_window.update_avatar()
        self.config_manager.set("current_profile", profile_name)

    def open_creator(self):
        from profile_creator import ProfileCreatorDialog
        dialog = ProfileCreatorDialog(self.main_window)
        if dialog.exec():
            self.profile_manager.scan_profiles()

    def open_editor(self, profile_name):
        from profile_creator import ProfileCreatorDialog
        dialog = ProfileCreatorDialog(self.main_window, edit_profile_name=profile_name)
        if dialog.exec():
            self.profile_manager.scan_profiles()
            # Si estamos editando el perfil actual, forzar actualización visual
            if self.profile_manager.current_profile == profile_name:
                self.main_window.update_avatar()

    def import_skin_dialog(self):
        path, _ = QFileDialog.getOpenFileName(self.main_window, tr("skin.import_dialog_title"), "", tr("skin.filter"))
        if path:
            success, res = self.profile_manager.import_skin_package(path)
            if success:
                self.change_profile(res)
                QMessageBox.information(self.main_window, tr("common.success"), tr("skin.import_success", name=res))
            else:
                QMessageBox.critical(self.main_window, tr("common.error"), tr("skin.import_error", error=res))

    def export_current_skin(self):
        current_name = self.profile_manager.current_profile
        path, _ = QFileDialog.getSaveFileName(self.main_window, tr("skin.export_dialog_title"), f"{current_name}.ptuber", tr("skin.filter"))
        if path:
            success, msg = self.profile_manager.export_skin_package(current_name, path)
            if success:
                QMessageBox.information(self.main_window, tr("common.success"), tr("skin.export_success", path=path))
            else:
                QMessageBox.critical(self.main_window, tr("common.error"), tr("skin.export_error", error=msg))
