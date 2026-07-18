"""
(AI)terEgo - Theme Manager
-----------------------------
Sistema de temas visuales para la ventana de Configuración:
Oscuro, Claro, Alto Contraste y Daltónico (colorblind-friendly).
"""

__author__ = "JJaroll"
__version__ = "1.2.0"
__maintainer__ = "JJaroll"
__status__ = "Production"

from PyQt6.QtCore import QObject, pyqtSignal

DEFAULT_THEME = "dark"

THEME_ORDER = ["dark", "light", "high_contrast", "colorblind"]

THEMES = {
    "dark": {
        "label_key": "theme.dark",
        "bg": "#1e1e1e", "pane_bg": "#252525", "tab_bg": "#333333", "tab_text": "#aaaaaa",
        "tab_selected_bg": "#252525", "tab_selected_text": "#ffffff",
        "text": "#dddddd", "text_dim": "#888888", "border": "#333333", "group_border": "#444444",
        "input_bg": "#333333", "input_border": "#444444", "input_text": "#ffffff",
        "btn_bg": "#3a3a3a", "btn_text": "#ffffff", "btn_border": "#555555",
        "btn_hover": "#4a4a4a", "btn_hover_border": "#777777",
        "accent": "#007ACC", "accent_text": "#ffffff",
        "table_bg": "#2b2b2b", "table_border": "#444444", "table_grid": "#383838",
        "header_bg": "#333333", "header_text": "#cccccc",
        "level_colors": ["#00E64D", "#FFFF00", "#FF8800", "#FF3333"],
        "warn_bg": "rgba(120, 30, 30, 0.35)", "warn_border": "#5a1f1f", "warn_text": "#ffb3b3",
    },
    "light": {
        "label_key": "theme.light",
        "bg": "#f2f2f2", "pane_bg": "#ffffff", "tab_bg": "#e2e2e2", "tab_text": "#555555",
        "tab_selected_bg": "#ffffff", "tab_selected_text": "#111111",
        "text": "#222222", "text_dim": "#666666", "border": "#cccccc", "group_border": "#cccccc",
        "input_bg": "#ffffff", "input_border": "#bbbbbb", "input_text": "#111111",
        "btn_bg": "#e8e8e8", "btn_text": "#111111", "btn_border": "#bbbbbb",
        "btn_hover": "#dcdcdc", "btn_hover_border": "#999999",
        "accent": "#0072D6", "accent_text": "#ffffff",
        "table_bg": "#ffffff", "table_border": "#cccccc", "table_grid": "#e5e5e5",
        "header_bg": "#e8e8e8", "header_text": "#333333",
        "level_colors": ["#1E9E4A", "#C9A200", "#E06E00", "#D33131"],
        "warn_bg": "rgba(211, 49, 49, 0.12)", "warn_border": "#d33131", "warn_text": "#8a1f1f",
    },
    "high_contrast": {
        "label_key": "theme.high_contrast",
        "bg": "#000000", "pane_bg": "#000000", "tab_bg": "#000000", "tab_text": "#ffffff",
        "tab_selected_bg": "#000000", "tab_selected_text": "#ffff00",
        "text": "#ffffff", "text_dim": "#e0e0e0", "border": "#ffffff", "group_border": "#ffffff",
        "input_bg": "#000000", "input_border": "#ffffff", "input_text": "#ffffff",
        "btn_bg": "#000000", "btn_text": "#ffffff", "btn_border": "#ffffff",
        "btn_hover": "#333333", "btn_hover_border": "#ffff00",
        "accent": "#ffff00", "accent_text": "#000000",
        "table_bg": "#000000", "table_border": "#ffffff", "table_grid": "#ffffff",
        "header_bg": "#000000", "header_text": "#ffff00",
        "level_colors": ["#00FFFF", "#FFFF00", "#FFA500", "#FFFFFF"],
        "warn_bg": "#330000", "warn_border": "#ffffff", "warn_text": "#ffff00",
    },
    "colorblind": {
        "label_key": "theme.colorblind",
        "bg": "#1b1f2a", "pane_bg": "#232838", "tab_bg": "#2f3650", "tab_text": "#b8c0d8",
        "tab_selected_bg": "#232838", "tab_selected_text": "#ffffff",
        "text": "#e4e8f2", "text_dim": "#9099b5", "border": "#39415c", "group_border": "#454e6e",
        "input_bg": "#2f3650", "input_border": "#454e6e", "input_text": "#ffffff",
        "btn_bg": "#2f3650", "btn_text": "#ffffff", "btn_border": "#454e6e",
        "btn_hover": "#3c4568", "btn_hover_border": "#5a659a",
        "accent": "#3399FF", "accent_text": "#ffffff",
        "table_bg": "#232838", "table_border": "#454e6e", "table_grid": "#39415c",
        "header_bg": "#2f3650", "header_text": "#e4e8f2",
        "level_colors": ["#3399FF", "#66CCFF", "#FFAA00", "#FF6600"],
        "warn_bg": "rgba(255, 102, 0, 0.18)", "warn_border": "#FF6600", "warn_text": "#ffdcb3",
    },
}


class ThemeManager(QObject):
    theme_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.current = DEFAULT_THEME

    def set_theme(self, name):
        if name not in THEMES:
            name = DEFAULT_THEME
        if name == self.current:
            return
        self.current = name
        self.theme_changed.emit(name)

    def colors(self):
        return THEMES[self.current]

    def level_colors(self):
        return THEMES[self.current]["level_colors"]

    def stylesheet(self):
        c = THEMES[self.current]
        return f"""
            QDialog {{ background-color: {c['bg']}; color: {c['text']}; }}
            QTabWidget::pane {{ border: 1px solid {c['border']}; background: {c['pane_bg']}; border-radius: 8px; }}
            QTabBar::tab {{ background: {c['tab_bg']}; color: {c['tab_text']}; padding: 10px 15px; border-top-left-radius: 8px; border-top-right-radius: 8px; margin-right: 4px; font-weight: bold; }}
            QTabBar::tab:selected {{ background: {c['tab_selected_bg']}; color: {c['tab_selected_text']}; border-bottom: 2px solid {c['accent']}; }}
            QLabel {{ color: {c['text']}; font-size: 13px; }}
            QGroupBox {{ border: 1px solid {c['group_border']}; border-radius: 8px; margin-top: 20px; font-weight: bold; color: {c['text']}; padding-top: 15px; }}
            QGroupBox::title {{ subcontrol-origin: margin; left: 10px; padding: 0 5px; }}
            QPushButton {{ background-color: {c['btn_bg']}; color: {c['btn_text']}; border-radius: 6px; padding: 8px; font-weight: bold; border: 1px solid {c['btn_border']}; }}
            QPushButton:hover {{ background-color: {c['btn_hover']}; border-color: {c['btn_hover_border']}; }}
            QPushButton:disabled {{ color: {c['text_dim']}; }}
            QSlider::groove:horizontal {{ border: 1px solid {c['border']}; height: 6px; background: {c['input_bg']}; border-radius: 3px; }}
            QSlider::handle:horizontal {{ background: {c['accent']}; width: 16px; margin: -5px 0; border-radius: 8px; }}
            QComboBox {{ background: {c['input_bg']}; color: {c['input_text']}; border: 1px solid {c['input_border']}; padding: 6px; border-radius: 4px; }}
            QComboBox QAbstractItemView {{ background-color: {c['input_bg']}; color: {c['input_text']}; selection-background-color: {c['accent']}; border: 1px solid {c['border']}; outline: none; }}
            QComboBox QAbstractItemView::item {{ background-color: {c['input_bg']}; color: {c['input_text']}; padding: 4px; }}
            QComboBox QAbstractItemView::item:selected {{ background-color: {c['accent']}; color: {c['accent_text']}; }}
            QComboBox::drop-down {{ border: none; }}
            QScrollArea {{ border: none; background: transparent; }}
            QTableWidget {{ background-color: {c['table_bg']}; border: 1px solid {c['table_border']}; border-radius: 6px; gridline-color: {c['table_grid']}; color: {c['text']}; }}
            QHeaderView::section {{ background-color: {c['header_bg']}; color: {c['header_text']}; padding: 5px; border: none; font-weight: bold; }}
            QTableWidget::item {{ padding: 5px; }}
            QLineEdit {{ background-color: {c['input_bg']}; color: {c['input_text']}; border: 1px solid {c['input_border']}; padding: 4px; }}
            QCheckBox, QRadioButton {{ color: {c['text']}; }}
        """

    def close_button_style(self):
        c = THEMES[self.current]
        return f"background-color: {c['accent']}; border: none; color: {c['accent_text']};"


theme_manager = ThemeManager()
