import sys
import os
from PyQt6.QtWidgets import QApplication

# Додаємо теку ui до шляху пошуку модулів
sys.path.append(os.path.join(os.path.dirname(__file__), 'ui'))


def main():
    try:
        # Створюємо додаток
        app = QApplication(sys.argv)

        # Імпортуємо та створюємо головне вікно
        from ui.main_window import CandidateManagementApp
        window = CandidateManagementApp()
        window.show()

        print("Програма запущена успішно")
        print("База даних ініціалізована")

        # Запускаємо головний цикл подій
        return app.exec()

    except Exception as e:
        print(f"Сталася помилка: {e}")
        import traceback
        traceback.print_exc()
        input("Натисніть Enter для виходу...")
        return 1


if __name__ == "__main__":
    sys.exit(main())