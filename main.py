import sys
import os
from PyQt6.QtWidgets import QApplication, QMenu
from PyQt6.QtGui import QAction


# Додаємо шляхи для імпортів
sys.path.append(os.path.join(os.path.dirname(__file__)))


def main():
    app = QApplication(sys.argv)

    from ui.main_window import CandidateManagementApp
    window = CandidateManagementApp()
    window.show()

    # Запускаємо додаток
    app.exec()


if __name__ == "__main__":
    main()