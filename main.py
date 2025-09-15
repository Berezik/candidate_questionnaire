import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QSettings

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