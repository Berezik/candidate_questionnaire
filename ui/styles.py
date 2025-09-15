from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt


class ThemeManager:
    def __init__(self):
        self.current_theme = "light"

    def get_light_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(33, 37, 41))
        palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(248, 249, 250))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(33, 37, 41))
        palette.setColor(QPalette.ColorRole.Text, QColor(33, 37, 41))
        palette.setColor(QPalette.ColorRole.Button, QColor(248, 249, 250))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(33, 37, 41))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Link, QColor(13, 110, 253))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(13, 110, 253))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        return palette

    def get_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(26, 29, 33))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(224, 229, 234))
        palette.setColor(QPalette.ColorRole.Base, QColor(35, 39, 46))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(48, 54, 64))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(35, 39, 46))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(224, 229, 234))
        palette.setColor(QPalette.ColorRole.Text, QColor(224, 229, 234))
        palette.setColor(QPalette.ColorRole.Button, QColor(48, 54, 64))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(224, 229, 234))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Link, QColor(61, 139, 255))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(61, 139, 255))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        return palette

    def get_stylesheet(self, theme):
        if theme == "dark":
            return self.get_dark_stylesheet()
        else:
            return self.get_light_stylesheet()

    def get_dark_stylesheet(self):
        return """
        /* --- Загальний стиль вікна та віджетів --- */
        QWidget {
            background-color: #1a1d21;
            color: #e0e5ea;
            font-family: "Segoe UI", Arial, sans-serif;
            font-size: 14px;
            border: none;
        }

        /* --- Меню --- */
        QMenuBar {
            background-color: #23272e;
            padding: 5px;
            border: none;
        }
        QMenuBar::item {
            padding: 6px 12px;
            background-color: transparent;
            border-radius: 4px;
            color: #e0e5ea;
        }
        QMenuBar::item:selected {
            background-color: #303640;
        }
        QMenu {
            background-color: #303640;
            border: 1px solid #414955;
            padding: 5px;
        }
        QMenu::item {
            padding: 8px 20px;
            color: #e0e5ea;
        }
        QMenu::item:selected {
            background-color: #3d8bff;
            color: #ffffff;
        }
        QMenu::separator {
            height: 1px;
            background-color: #414955;
            margin: 5px 0;
        }

        /* --- Лейбли та заголовки --- */
        QLabel {
            color: #9099a2;
            padding: 2px;
        }

        /* --- Групи елементів --- */
        QGroupBox {
            font-weight: bold;
            border: 1px solid #414955;
            border-radius: 6px;
            margin-top: 10px;
            padding-top: 20px;
            background-color: #23272e;
            color: #e0e5ea;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 0 5px;
            background-color: #23272e;
            color: #e0e5ea;
        }

        /* --- Поля вводу --- */
        QLineEdit, QTextEdit, QComboBox, QDateEdit {
            background-color: #2d3138;
            color: #e0e5ea;
            border: 1px solid #414955;
            border-radius: 4px;
            padding: 6px;
            selection-background-color: #3d8bff;
        }
        QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QDateEdit:focus {
            border: 1px solid #3d8bff;
        }

        /* --- Список кандидатів --- */
        QListWidget {
            background-color: #23272e;
            border: 1px solid #414955;
            border-radius: 4px;
            padding: 2px;
        }
        QListWidget::item {
            padding: 6px;
            border-radius: 3px;
        }
        QListWidget::item:hover {
            background-color: #303640;
        }
        QListWidget::item:selected {
            background-color: #3d8bff;
            color: #ffffff;
        }

        /* --- Вкладки --- */
        QTabWidget::pane {
            border: 1px solid #414955;
            background-color: #23272e;
        }
        QTabBar::tab {
            background: #23272e;
            color: #9099a2;
            padding: 8px 12px;
            border: 1px solid #414955;
            border-bottom: none;
        }
        QTabBar::tab:hover {
            background: #303640;
            color: #e0e5ea;
        }
        QTabBar::tab:selected {
            background: #1a1d21;
            color: #3d8bff;
            border-bottom: 2px solid #3d8bff;
        }

        /* --- Кнопки --- */
        QPushButton {
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
            min-height: 30px;
        }

        /* Основні кнопки */
        QPushButton.primary-button {
            background-color: #3d8bff;
            color: white;
            border: none;
        }
        QPushButton.primary-button:hover {
            background-color: #529bff;
        }
        QPushButton.primary-button:pressed {
            background-color: #2a75e8;
        }

        /* Другорядні кнопки */
        QPushButton.secondary-button {
            background-color: transparent;
            color: #e0e5ea;
            border: 1px solid #414955;
        }
        QPushButton.secondary-button:hover {
            background-color: #303640;
            border-color: #5a6575;
        }

        /* Небезпечні кнопки */
        QPushButton.destructive-button {
            background-color: transparent;
            color: #e53935;
            border: 1px solid #e53935;
        }
        QPushButton.destructive-button:hover {
            background-color: #e53935;
            color: white;
        }

        /* --- Статус бар --- */
        QStatusBar {
            background-color: #23272e;
            color: #9099a2;
            padding: 5px;
            border-top: 1px solid #414955;
        }

        /* --- Скролбари --- */
        QScrollBar:vertical {
            border: none;
            background: #23272e;
            width: 10px;
        }
        QScrollBar::handle:vertical {
            background: #414955;
            min-height: 20px;
            border-radius: 5px;
        }
        """

    def get_light_stylesheet(self):
        return """
        /* --- Загальний стиль вікна та віджетів --- */
        QWidget {
            background-color: #f5f5f5;
            color: #333333;
            font-family: "Segoe UI", Arial, sans-serif;
            font-size: 14px;
            border: none;
        }

        /* --- Меню --- */
        QMenuBar {
            background-color: #f8f9fa;
            padding: 5px;
            border-bottom: 1px solid #dee2e6;
        }
        QMenuBar::item {
            padding: 6px 12px;
            background-color: transparent;
            border-radius: 4px;
            color: #333333;
        }
        QMenuBar::item:selected {
            background-color: #e9ecef;
        }
        QMenu {
            background-color: #ffffff;
            border: 1px solid #dee2e6;
            padding: 5px;
            border-radius: 4px;
        }
        QMenu::item {
            padding: 8px 20px;
            color: #333333;
        }
        QMenu::item:selected {
            background-color: #0d6efd;
            color: #ffffff;
        }

        /* --- Лейбли та заголовки --- */
        QLabel {
            color: #495057;
            padding: 2px;
        }

        /* --- Групи елементів --- */
        QGroupBox {
            font-weight: bold;
            border: 1px solid #dee2e6;
            border-radius: 6px;
            margin-top: 10px;
            padding-top: 20px;
            background-color: #ffffff;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 0 5px;
            background-color: #ffffff;
        }

        /* --- Поля вводу --- */
        QLineEdit, QTextEdit, QComboBox, QDateEdit {
            background-color: #ffffff;
            color: #333333;
            border: 1px solid #ced4da;
            border-radius: 4px;
            padding: 6px;
            selection-background-color: #0d6efd;
        }
        QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QDateEdit:focus {
            border: 1px solid #0d6efd;
        }

        /* --- Список кандидатів --- */
        QListWidget {
            background-color: #ffffff;
            border: 1px solid #ced4da;
            border-radius: 4px;
            padding: 2px;
        }
        QListWidget::item {
            padding: 6px;
            border-radius: 3px;
            border-bottom: 1px solid #f8f9fa;
        }
        QListWidget::item:hover {
            background-color: #e9ecef;
        }
        QListWidget::item:selected {
            background-color: #0d6efd;
            color: #ffffff;
        }

        /* --- Вкладки --- */
        QTabWidget::pane {
            border: 1px solid #dee2e6;
            background-color: #ffffff;
        }
        QTabBar::tab {
            background: #f8f9fa;
            color: #6c757d;
            padding: 8px 12px;
            border: 1px solid #dee2e6;
            border-bottom: none;
        }
        QTabBar::tab:hover {
            background: #e9ecef;
            color: #495057;
        }
        QTabBar::tab:selected {
            background: #ffffff;
            color: #0d6efd;
            border-bottom: 2px solid #0d6efd;
        }

        /* --- Кнопки --- */
        QPushButton {
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
            min-height: 30px;
        }

        /* Основні кнопки */
        QPushButton.primary-button {
            background-color: #0d6efd;
            color: white;
            border: none;
        }
        QPushButton.primary-button:hover {
            background-color: #0b5ed7;
        }
        QPushButton.primary-button:pressed {
            background-color: #0a58ca;
        }

        /* Другорядні кнопки */
        QPushButton.secondary-button {
            background-color: #ffffff;
            color: #0d6efd;
            border: 1px solid #0d6efd;
        }
        QPushButton.secondary-button:hover {
            background-color: #f8f9fa;
            border-color: #0b5ed7;
            color: #0b5ed7;
        }

        /* Небезпечні кнопки */
        QPushButton.destructive-button {
            background-color: #ffffff;
            color: #dc3545;
            border: 1px solid #dc3545;
        }
        QPushButton.destructive-button:hover {
            background-color: #dc3545;
            color: white;
        }

        /* --- Статус бар --- */
        QStatusBar {
            background-color: #f8f9fa;
            color: #6c757d;
            padding: 5px;
            border-top: 1px solid #dee2e6;
        }

        /* --- Скролбари --- */
        QScrollBar:vertical {
            border: none;
            background: #f8f9fa;
            width: 10px;
        }
        QScrollBar::handle:vertical {
            background: #ced4da;
            min-height: 20px;
            border-radius: 5px;
        }
        """