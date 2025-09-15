from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt


class ThemeManager:
    def __init__(self):
        # Визначаємо основні кольори один раз, щоб легко їх змінювати
        self.PRIMARY_COLOR = QColor("#007BFF")
        self.LIGHT_BACKGROUND = QColor("#F5F7FA")
        self.LIGHT_TEXT = QColor("#212529")

        self.DARK_BACKGROUND = QColor("#212529")
        self.DARK_TEXT = QColor("#E9ECEF")
        self.DARK_WIDGET_BACKGROUND = QColor("#343A40")

    def get_light_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, self.LIGHT_BACKGROUND)
        palette.setColor(QPalette.ColorRole.WindowText, self.LIGHT_TEXT)
        palette.setColor(QPalette.ColorRole.Base, QColor("#FFFFFF"))  # Для полів вводу
        palette.setColor(QPalette.ColorRole.AlternateBase, self.LIGHT_BACKGROUND)
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#FFFFFF"))
        palette.setColor(QPalette.ColorRole.ToolTipText, self.LIGHT_TEXT)
        palette.setColor(QPalette.ColorRole.Text, self.LIGHT_TEXT)
        palette.setColor(QPalette.ColorRole.Button, self.LIGHT_BACKGROUND)
        palette.setColor(QPalette.ColorRole.ButtonText, self.LIGHT_TEXT)

        # --- Єдиний колір для акцентів ---
        palette.setColor(QPalette.ColorRole.BrightText, self.PRIMARY_COLOR)
        palette.setColor(QPalette.ColorRole.Link, self.PRIMARY_COLOR)
        palette.setColor(QPalette.ColorRole.Highlight, self.PRIMARY_COLOR)
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#FFFFFF"))

        return palette

    def get_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, self.DARK_BACKGROUND)
        palette.setColor(QPalette.ColorRole.WindowText, self.DARK_TEXT)
        palette.setColor(QPalette.ColorRole.Base, self.DARK_WIDGET_BACKGROUND)
        palette.setColor(QPalette.ColorRole.AlternateBase, self.DARK_BACKGROUND)
        palette.setColor(QPalette.ColorRole.ToolTipBase, self.DARK_WIDGET_BACKGROUND)
        palette.setColor(QPalette.ColorRole.ToolTipText, self.DARK_TEXT)
        palette.setColor(QPalette.ColorRole.Text, self.DARK_TEXT)
        palette.setColor(QPalette.ColorRole.Button, self.DARK_WIDGET_BACKGROUND)
        palette.setColor(QPalette.ColorRole.ButtonText, self.DARK_TEXT)

        # --- Єдиний колір для акцентів ---
        palette.setColor(QPalette.ColorRole.BrightText, self.PRIMARY_COLOR.lighter(120))
        palette.setColor(QPalette.ColorRole.Link, self.PRIMARY_COLOR.lighter(120))
        palette.setColor(QPalette.ColorRole.Highlight, self.PRIMARY_COLOR)
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#FFFFFF"))

        return palette

    def get_stylesheet(self, theme):
        primary_color = self.PRIMARY_COLOR.name()

        if theme == "dark":
            return f"""
                QWidget {{
                    background-color: {self.DARK_BACKGROUND.name()};
                    color: {self.DARK_TEXT.name()};
                    font-family: Segoe UI, sans-serif; /* Більш сучасний шрифт */
                }}
                QGroupBox {{
                    font-weight: bold;
                    border: 1px solid #495057; /* М'якша рамка */
                    border-radius: 8px;
                    margin-top: 10px;
                    background-color: {self.DARK_WIDGET_BACKGROUND.name()};
                }}
                QGroupBox::title {{
                    subcontrol-origin: margin;
                    subcontrol-position: top center;
                    padding: 0 10px;
                }}
                QLineEdit, QTextEdit, QComboBox, QDateEdit {{
                    padding: 8px;
                    border: 1px solid #495057;
                    border-radius: 6px;
                    background-color: {self.DARK_WIDGET_BACKGROUND.name()};
                    color: {self.DARK_TEXT.name()};
                    selection-background-color: {primary_color};
                }}
                QPushButton {{
                    background-color: {primary_color};
                    color: white;
                    border: none;
                    padding: 10px 20px; /* Більше "повітря" */
                    border-radius: 6px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {self.PRIMARY_COLOR.darker(110).name()}; /* Затемнення при наведенні */
                }}
                QPushButton:pressed {{
                    background-color: {self.PRIMARY_COLOR.darker(120).name()};
                }}
                QListWidget, QTableView {{
                    border: 1px solid #495057;
                    border-radius: 6px;
                    background-color: {self.DARK_WIDGET_BACKGROUND.name()};
                    alternate-background-color: {self.DARK_BACKGROUND.name()};
                }}
                QTabWidget::pane {{
                    border: 1px solid #495057;
                    border-radius: 6px;
                }}
                QTabBar::tab {{
                    background-color: transparent;
                    color: {self.DARK_TEXT.name()};
                    padding: 8px 16px;
                    border-bottom: 2px solid transparent; /* Підкреслення замість фону */
                }}
                QTabBar::tab:hover {{
                    background-color: {self.DARK_WIDGET_BACKGROUND.name()};
                }}
                QTabBar::tab:selected {{
                    color: {primary_color};
                    border-bottom: 2px solid {primary_color};
                }}
            """
        else:  # Light theme
            return f"""
                QWidget {{
                    background-color: {self.LIGHT_BACKGROUND.name()};
                    color: {self.LIGHT_TEXT.name()};
                    font-family: Segoe UI, sans-serif;
                }}
                QGroupBox {{
                    font-weight: bold;
                    border: 1px solid #DEE2E6; /* Дуже світла рамка */
                    border-radius: 8px;
                    margin-top: 10px;
                    background-color: #FFFFFF;
                }}
                QGroupBox::title {{
                    subcontrol-origin: margin;
                    subcontrol-position: top center;
                    padding: 0 10px;
                }}
                QLineEdit, QTextEdit, QComboBox, QDateEdit {{
                    padding: 8px;
                    border: 1px solid #CED4DA;
                    border-radius: 6px;
                    background-color: #FFFFFF;
                    selection-background-color: {primary_color};
                }}
                QPushButton {{
                    background-color: {primary_color};
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 6px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {self.PRIMARY_COLOR.darker(110).name()};
                }}
                QPushButton:pressed {{
                    background-color: {self.PRIMARY_COLOR.darker(120).name()};
                }}
                QListWidget, QTableView {{
                    border: 1px solid #DEE2E6;
                    border-radius: 6px;
                    background-color: #FFFFFF;
                    alternate-background-color: {self.LIGHT_BACKGROUND.name()};
                }}
                QTabWidget::pane {{
                    border-top: 1px solid #DEE2E6;
                }}
                QTabBar::tab {{
                    background-color: transparent;
                    color: #495057;
                    padding: 8px 16px;
                    border-bottom: 2px solid transparent;
                }}
                QTabBar::tab:hover {{
                    background-color: #E9ECEF;
                }}
                QTabBar::tab:selected {{
                    color: {primary_color};
                    border-bottom: 2px solid {primary_color};
                }}
            """