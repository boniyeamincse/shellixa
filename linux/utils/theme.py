from utils.config import Config


THEMES = {
    "dark": {
        "window": "#1a1b26",
        "panel": "#16161e",
        "surface": "#24283b",
        "surface_alt": "#2f3549",
        "border": "#414868",
        "text": "#a9b1d6",
        "muted": "#565f89",
        "accent": "#7aa2f7",
        "accent_alt": "#2ac3de",
        "success": "#9ece6a",
        "danger": "#f7768e",
    },
    "graphite": {
        "window": "#202427",
        "panel": "#181b1d",
        "surface": "#2c3136",
        "surface_alt": "#363d44",
        "border": "#4a5560",
        "text": "#d3dae3",
        "muted": "#8b97a4",
        "accent": "#6fb1ff",
        "accent_alt": "#58d1b3",
        "success": "#91d18b",
        "danger": "#ff7d96",
    },
    "light": {
        "window": "#f4f1ea",
        "panel": "#ebe5d9",
        "surface": "#fffdf7",
        "surface_alt": "#e3dccf",
        "border": "#c8bea9",
        "text": "#352f25",
        "muted": "#7d7362",
        "accent": "#2f6fed",
        "accent_alt": "#168b99",
        "success": "#36824f",
        "danger": "#c24d5d",
    },
    "sand": {
        "window": "#f7f3e8",
        "panel": "#efe8d5",
        "surface": "#fffaf0",
        "surface_alt": "#ddd4bf",
        "border": "#b9ab8c",
        "text": "#3b3323",
        "muted": "#7b6f57",
        "accent": "#b65c2d",
        "accent_alt": "#3c8d7b",
        "success": "#4d8757",
        "danger": "#bf4a3e",
    },
}


class ThemeManager:
    def __init__(self, config=None):
        self.config = config or Config()

    def available_themes(self):
        return list(THEMES.keys())

    def resolve_palette(self, theme_name=None):
        name = theme_name or self.config.get("theme")
        return THEMES.get(name, THEMES["dark"])

    def build_stylesheet(self, theme_name=None):
        palette = self.resolve_palette(theme_name)
        font_family = self.config.get("font_family")
        font_size = self.config.get("font_size")
        return f"""
            QMainWindow {{ background-color: {palette['window']}; }}
            QWidget {{
                background-color: {palette['window']};
                color: {palette['text']};
                font-family: '{font_family}', sans-serif;
                font-size: {font_size}pt;
            }}
            QToolBar {{
                background-color: {palette['panel']};
                border-bottom: 1px solid {palette['border']};
                spacing: 10px;
                padding: 5px;
            }}
            QTabWidget::pane {{
                border: 1px solid {palette['border']};
                top: -1px;
                background-color: {palette['window']};
            }}
            QTabBar::tab {{
                background: {palette['surface']};
                padding: 10px 20px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
            }}
            QTabBar::tab:selected {{
                background: {palette['surface_alt']};
                color: {palette['accent']};
                border-bottom: 2px solid {palette['accent']};
            }}
            QPushButton, QComboBox, QLineEdit, QTextEdit, QPlainTextEdit, QListWidget, QTreeWidget, QTableWidget {{
                background-color: {palette['surface']};
                border: 1px solid {palette['border']};
                border-radius: 4px;
                color: {palette['text']};
            }}
            QWidget[class='sidebar'] {{
                background-color: {palette['panel']};
                border-right: 1px solid {palette['border']};
            }}
            QFrame[class='card'] {{
                background-color: {palette['surface']};
                border: 1px solid {palette['border']};
                border-radius: 8px;
            }}
            QPushButton {{
                padding: 5px 12px;
            }}
            QPushButton:hover {{
                background-color: {palette['surface_alt']};
            }}
            QPushButton[class='primary'] {{
                background-color: {palette['accent']};
                color: {palette['window']};
                font-weight: bold;
            }}
            QPushButton[class='danger'] {{
                color: {palette['danger']};
            }}
            QHeaderView::section {{
                background-color: {palette['panel']};
                color: {palette['text']};
                border: 1px solid {palette['border']};
                padding: 6px;
            }}
            QLabel[class='muted'] {{
                color: {palette['muted']};
            }}
            QLabel[class='accent'] {{
                color: {palette['accent']};
            }}
        """

    def apply_theme(self, widget, theme_name=None):
        resolved_name = theme_name or self.config.get("theme")
        self.config.set("theme", resolved_name)
        widget.setStyleSheet(self.build_stylesheet(resolved_name))
