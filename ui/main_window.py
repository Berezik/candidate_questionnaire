import sys
import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QSplitter, QListWidget, QLineEdit, QPushButton,
                             QGroupBox, QTabWidget, QMessageBox, QListWidgetItem,
                             QMenuBar, QStatusBar, QFileDialog, QDialog, QLabel,
                             QMenu)
from PyQt6.QtGui import QAction, QPixmap, QActionGroup
from PyQt6.QtCore import Qt, QDate, QSettings

# Додаємо шлях до батьківської директорії для імпортів
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import DatabaseManager
from ui.personal_info_tab import PersonalInfoTab
from utils.exporters import PDFExporter, ExcelExporter
from utils.backup_manager import BackupManager, DataImporter
from utils.reports import StatisticsManager
from ui.styles import ThemeManager


class CandidateManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Анкета кандидата - Система управління")
        self.setGeometry(100, 100, 1400, 800)
        self.current_candidate_id = None

        # Ініціалізація бази даних
        self.db_manager = DatabaseManager()
        self.db_manager.init_db()

        # Додаємо менеджер тем
        self.theme_manager = ThemeManager()

        # Завантажуємо збережену тему
        settings = QSettings("CandidateApp", "Questionnaire")
        saved_theme = settings.value("theme", "light")
        self.current_theme = saved_theme

        # Додаємо менеджери утиліт
        self.backup_manager = BackupManager()
        self.data_importer = DataImporter()
        self.statistics_manager = StatisticsManager()

        self.init_ui()
        self.apply_theme(self.current_theme)
        self.refresh_list()

    def init_ui(self):
        # Центральний віджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Основний layout
        main_layout = QVBoxLayout(central_widget)

        # Створюємо роздільник
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Ліва частина - пошук і список кандидатів
        left_widget = self.create_left_panel()

        # Права частина - вкладки з інформацією
        self.tab_widget = QTabWidget()
        self.personal_info_tab = PersonalInfoTab()
        self.tab_widget.addTab(self.personal_info_tab, "Персональна інформація")

        # Додаємо інші вкладки
        self.tab_widget.addTab(QWidget(), "Військова інформація")
        self.tab_widget.addTab(QWidget(), "Сімейний стан")
        self.tab_widget.addTab(QWidget(), "Освіта")
        self.tab_widget.addTab(QWidget(), "Медична інформація")
        self.tab_widget.addTab(QWidget(), "Загальна інформація")

        # Додаємо віджети в роздільник
        splitter.addWidget(left_widget)
        splitter.addWidget(self.tab_widget)
        splitter.setSizes([300, 1100])

        # Кнопки збереження
        save_widget = self.create_save_buttons()

        # Додаємо все до головного layout
        main_layout.addWidget(splitter)
        main_layout.addWidget(save_widget)

        # Підключення сигналів
        self.connect_signals()

        # Додаємо меню
        self.create_menu_bar()

        # Додаємо статус бар
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.update_status_bar()

    def create_left_panel(self):
        left_widget = QWidget()
        left_widget.setMaximumWidth(350)
        left_layout = QVBoxLayout(left_widget)

        # Поле пошуку
        search_group = QGroupBox("Пошук кандидата")
        search_layout = QVBoxLayout(search_group)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("ПІБ, телефон, ІПН, посада...")
        self.search_input.textChanged.connect(self.on_search_changed)
        search_layout.addWidget(self.search_input)

        # Список кандидатів
        candidates_group = QGroupBox("Список кандидатів")
        candidates_layout = QVBoxLayout(candidates_group)
        self.candidates_list = QListWidget()
        self.candidates_list.itemClicked.connect(self.on_candidate_selected)
        candidates_layout.addWidget(self.candidates_list)

        # Кнопки управління
        button_layout = QHBoxLayout()
        self.add_btn = QPushButton("Додати")
        self.add_btn.setObjectName("primary-button")
        self.delete_btn = QPushButton("Видалити")
        self.delete_btn.setObjectName("destructive-button")
        self.refresh_btn = QPushButton("Оновити")
        self.refresh_btn.setObjectName("secondary-button")
        self.clear_btn = QPushButton("Очистити")
        self.clear_btn.setObjectName("secondary-button")

        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(self.refresh_btn)
        button_layout.addWidget(self.clear_btn)

        left_layout.addWidget(search_group)
        left_layout.addWidget(candidates_group)
        left_layout.addLayout(button_layout)

        return left_widget

    def create_save_buttons(self):
        save_widget = QWidget()
        save_layout = QHBoxLayout(save_widget)
        self.save_btn = QPushButton("Зберегти")
        self.save_btn.setObjectName("primary-button")
        self.save_new_btn = QPushButton("Зберегти та додати нового")
        self.save_new_btn.setObjectName("primary-button")
        save_layout.addWidget(self.save_btn)
        save_layout.addWidget(self.save_new_btn)
        save_layout.addStretch()
        return save_widget

    def create_menu_bar(self):
        menu_bar = QMenuBar()

        # Меню Файл
        file_menu = QMenu("Файл", self)

        export_pdf_action = QAction("Експорт в PDF", self)
        export_pdf_action.triggered.connect(self.export_to_pdf)
        file_menu.addAction(export_pdf_action)

        export_excel_action = QAction("Експорт в Excel", self)
        export_excel_action.triggered.connect(self.export_to_excel)
        file_menu.addAction(export_excel_action)

        file_menu.addSeparator()

        backup_action = QAction("Створити резервну копію", self)
        backup_action.triggered.connect(self.create_backup)
        file_menu.addAction(backup_action)

        restore_action = QAction("Відновити з резервної копії", self)
        restore_action.triggered.connect(self.restore_backup)
        file_menu.addAction(restore_action)

        file_menu.addSeparator()

        import_action = QAction("Імпорт з Excel", self)
        import_action.triggered.connect(self.import_from_excel)
        file_menu.addAction(import_action)

        file_menu.addSeparator()

        exit_action = QAction("Вихід", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Меню Вигляд
        view_menu = QMenu("Вигляд", self)

        self.light_theme_action = QAction("🌞 Світла тема", self)
        self.light_theme_action.triggered.connect(lambda: self.apply_theme("light"))
        self.light_theme_action.setCheckable(True)

        self.dark_theme_action = QAction("🌙 Темна тема", self)
        self.dark_theme_action.triggered.connect(lambda: self.apply_theme("dark"))
        self.dark_theme_action.setCheckable(True)

        # Групуємо дії теми
        theme_group = QActionGroup(self)
        theme_group.addAction(self.light_theme_action)
        theme_group.addAction(self.dark_theme_action)
        theme_group.setExclusive(True)

        view_menu.addAction(self.light_theme_action)
        view_menu.addAction(self.dark_theme_action)

        # Меню Звіти
        reports_menu = QMenu("Звіти", self)

        stats_action = QAction("Статистика", self)
        stats_action.triggered.connect(self.show_statistics)
        reports_menu.addAction(stats_action)

        # Додаємо меню до меню бару
        menu_bar.addMenu(file_menu)
        menu_bar.addMenu(view_menu)
        menu_bar.addMenu(reports_menu)

        self.setMenuBar(menu_bar)

        # Оновлюємо вибір теми в меню
        self.update_theme_menu()

    def update_theme_menu(self):
        self.light_theme_action.setChecked(self.current_theme == "light")
        self.dark_theme_action.setChecked(self.current_theme == "dark")

    def connect_signals(self):
        self.add_btn.clicked.connect(self.add_candidate)
        self.delete_btn.clicked.connect(self.delete_candidate)
        self.refresh_btn.clicked.connect(self.refresh_list)
        self.clear_btn.clicked.connect(self.clear_form)
        self.save_btn.clicked.connect(self.save_candidate)
        self.save_new_btn.clicked.connect(self.save_and_new_candidate)

    def apply_theme(self, theme_name):
        self.current_theme = theme_name
        theme_manager = ThemeManager()

        # Зберігаємо вибір теми
        settings = QSettings("CandidateApp", "Questionnaire")
        settings.setValue("theme", theme_name)

        # Застосовуємо палітру кольорів
        if theme_name == "dark":
            self.setPalette(theme_manager.get_dark_theme())
        else:
            self.setPalette(theme_manager.get_light_theme())

        # Застосовуємо стилі
        self.setStyleSheet(theme_manager.get_stylesheet(theme_name))

        # Оновлюємо вибір у меню
        self.update_theme_menu()

        # Оновлюємо статус бар
        self.update_status_bar()

        print(f"Застосовано тему: {theme_name}")

    def add_candidate(self):
        self.clear_form()
        self.current_candidate_id = None
        self.candidates_list.clearSelection()
        print("Режим додавання нового кандидата")

    def delete_candidate(self):
        if not self.candidates_list.currentItem():
            QMessageBox.warning(self, "Помилка", "Виберіть кандидата для видалення")
            return

        candidate_id = self.candidates_list.currentItem().data(Qt.ItemDataRole.UserRole)

        reply = QMessageBox.question(
            self, "Підтвердження",
            "Ви впевнені, що хочете видалити цього кандидата?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            if self.db_manager.delete_candidate(candidate_id):
                QMessageBox.information(self, "Успіх", "Кандидата видалено")
                self.refresh_list()
            else:
                QMessageBox.warning(self, "Помилка", "Не вдалося видалити кандидата")

    def refresh_list(self):
        self.candidates_list.clear()
        candidates = self.db_manager.get_all_candidates()
        if not candidates:
            print("В базі даних ще немає кандидатів")
            self.update_status_bar()
            return

        for candidate in candidates:
            item_text = f"{candidate.last_name} {candidate.first_name}"
            if candidate.middle_name:
                item_text += f" {candidate.middle_name}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, candidate.id)
            self.candidates_list.addItem(item)

        self.update_status_bar()

    def update_status_bar(self):
        count = self.statistics_manager.get_candidate_count()
        self.status_bar.showMessage(f"Загальна кількість кандидатів: {count}")

    def on_search_changed(self):
        search_term = self.search_input.text().strip()
        if not search_term:
            self.refresh_list()
            return

        self.candidates_list.clear()
        candidates = self.db_manager.search_candidates(search_term)
        for candidate in candidates:
            item_text = f"{candidate.last_name} {candidate.first_name}"
            if candidate.middle_name:
                item_text += f" {candidate.middle_name}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, candidate.id)
            self.candidates_list.addItem(item)

    def on_candidate_selected(self, item):
        candidate_id = item.data(Qt.ItemDataRole.UserRole)
        self.current_candidate_id = candidate_id

        # Завантажуємо дані кандидата
        candidate, phones = self.db_manager.get_candidate_by_id(candidate_id)
        if candidate:
            self.load_candidate_data(candidate, phones)

    def load_candidate_data(self, candidate, phones):
        """Завантажує дані кандидата у форму"""
        from PyQt6.QtGui import QPixmap

        # Основна інформація
        self.personal_info_tab.last_name_input.setText(candidate.last_name or "")
        self.personal_info_tab.first_name_input.setText(candidate.first_name or "")
        self.personal_info_tab.middle_name_input.setText(candidate.middle_name or "")
        self.personal_info_tab.tax_number_input.setText(candidate.tax_number or "")

        if candidate.birth_date:
            from PyQt6.QtCore import QDate
            self.personal_info_tab.birth_date_edit.setDate(
                QDate(candidate.birth_date.year, candidate.birth_date.month, candidate.birth_date.day))

        self.personal_info_tab.birth_place_input.setText(candidate.birth_place or "")

        # Стать
        if candidate.gender:
            if candidate.gender.value == "Чоловік":
                self.personal_info_tab.gender_male.setChecked(True)
            else:
                self.personal_info_tab.gender_female.setChecked(True)

        # Документи
        if candidate.document_type:
            if candidate.document_type.value == "passport":
                self.personal_info_tab.passport_rb.setChecked(True)
                self.personal_info_tab.passport_series_input.setText(candidate.passport_series or "")
                self.personal_info_tab.passport_number_input.setText(candidate.passport_number or "")
                self.personal_info_tab.passport_issued_input.setText(candidate.passport_issued_by or "")
                if candidate.passport_issue_date:
                    from PyQt6.QtCore import QDate
                    self.personal_info_tab.passport_issue_date.setDate(
                        QDate(candidate.passport_issue_date.year, candidate.passport_issue_date.month,
                              candidate.passport_issue_date.day))
            else:
                self.personal_info_tab.id_card_rb.setChecked(True)
                self.personal_info_tab.id_number_input.setText(candidate.id_card_number or "")
                self.personal_info_tab.id_issued_by_input.setText(candidate.id_card_issued_by or "")
                if candidate.id_card_issue_date:
                    from PyQt6.QtCore import QDate
                    self.personal_info_tab.id_issue_date.setDate(
                        QDate(candidate.id_card_issue_date.year, candidate.id_card_issue_date.month,
                              candidate.id_card_issue_date.day))

        # Адреси
        self.personal_info_tab.registration_address_input.setPlainText(candidate.registration_address or "")
        self.personal_info_tab.actual_address_input.setPlainText(candidate.actual_address or "")

        # Контактна інформація
        self.personal_info_tab.email_input.setText(candidate.email or "")

        # Телефони
        if phones:
            if len(phones) > 0:
                self.personal_info_tab.phone_input.setText(phones[0].phone_number or "")
            if len(phones) > 1:
                self.personal_info_tab.phone2_input.setText(phones[1].phone_number or "")
                self.personal_info_tab.phone2_input.setVisible(True)
                self.personal_info_tab.add_phone_btn.setEnabled(False)

        # Додаткова інформація
        self.personal_info_tab.nationality_input.setText(candidate.nationality or "")
        self.personal_info_tab.citizenship_input.setText(candidate.citizenship or "")
        self.personal_info_tab.vpo_status_input.setText(candidate.vpo_status or "")

        if candidate.religion_forbids_weapons is not None:
            self.personal_info_tab.religion_forbids_weapons.setChecked(candidate.religion_forbids_weapons)

        # Релігія
        if candidate.religion:
            religion_index = self.personal_info_tab.religion_combo.findText(candidate.religion.value)
            if religion_index >= 0:
                self.personal_info_tab.religion_combo.setCurrentIndex(religion_index)
                if candidate.religion.value == "Інше" and candidate.alternative_religion:
                    self.personal_info_tab.alternative_religion_input.setText(candidate.alternative_religion)
                    self.personal_info_tab.alternative_religion_input.setVisible(True)

        # Банківська інформація
        if candidate.bank_name:
            bank_index = self.personal_info_tab.bank_combo.findText(candidate.bank_name)
            if bank_index >= 0:
                self.personal_info_tab.bank_combo.setCurrentIndex(bank_index)

        self.personal_info_tab.iban_input.setText(candidate.iban or "")

        if candidate.has_credit is not None:
            self.personal_info_tab.has_credit_check.setChecked(candidate.has_credit)

        # Транспорт
        self.personal_info_tab.driver_license_input.setText(candidate.driver_license or "")
        self.personal_info_tab.vehicle_input.setText(candidate.personal_vehicle or "")

        if candidate.extreme_driving_experience is not None:
            self.personal_info_tab.extreme_driving_check.setChecked(candidate.extreme_driving_experience)

        # Фото
        if candidate.photo_path and os.path.exists(candidate.photo_path):
            self.personal_info_tab.photo_path = candidate.photo_path
            pixmap = QPixmap(candidate.photo_path)
            if not pixmap.isNull():
                from PyQt6.QtCore import Qt
                scaled_pixmap = pixmap.scaled(150, 200, Qt.AspectRatioMode.KeepAspectRatio,
                                              Qt.TransformationMode.SmoothTransformation)
                self.personal_info_tab.photo_label.setPixmap(scaled_pixmap)

    def clear_form(self):
        self.personal_info_tab.clear_form()

    def save_candidate(self):
        """
        Зберігає дані кандидата до бази даних
        """
        try:
            print("Початок збереження кандидата...")

            # Отримуємо дані з форми
            candidate_data = self.personal_info_tab.get_form_data()
            if not candidate_data:
                print("Дані форми не валідні або скасовано")
                return

            print(f"Отримано дані кандидата: {candidate_data.keys()}")

            # Перевіряємо обов'язкові поля
            if not candidate_data.get('last_name') or not candidate_data.get('first_name') or not candidate_data.get(
                    'tax_number'):
                QMessageBox.warning(self, "Помилка", "Заповніть обов'язкові поля: Прізвище, Ім'я, РНОКПП(ІПН)")
                return

            try:
                if self.current_candidate_id:
                    # Оновлення існуючого кандидата
                    print(f"Оновлення кандидата з ID: {self.current_candidate_id}")
                    if self.db_manager.update_candidate(self.current_candidate_id, candidate_data):
                        QMessageBox.information(self, "Успіх", "Дані кандидата оновлено")
                        print("Кандидат успішно оновлений")
                        self.refresh_list()
                    else:
                        QMessageBox.warning(self, "Помилка", "Не вдалося оновити дані кандидата")
                        print("Помилка оновлення кандидата")
                else:
                    # Додавання нового кандидата
                    print("Додавання нового кандидата")
                    candidate_id = self.db_manager.add_candidate(candidate_data)
                    if candidate_id:
                        QMessageBox.information(self, "Успіх", "Кандидата додано до бази даних")
                        print(f"Кандидат успішно доданий з ID: {candidate_id}")
                        self.refresh_list()
                    else:
                        QMessageBox.warning(self, "Помилка", "Не вдалося зберегти кандидата")
                        print("Помилка додавання кандидата")

            except Exception as db_error:
                print(f"Помилка бази даних: {db_error}")
                QMessageBox.critical(
                    self,
                    "Помилка бази даних",
                    f"Сталася помилка при роботі з базою даних:\n{str(db_error)}"
                )

        except Exception as e:
            print(f"Критична помилка в save_candidate: {e}")
            import traceback
            error_details = traceback.format_exc()
            print(f"Traceback: {error_details}")

            QMessageBox.critical(
                self,
                "Критична помилка",
                f"Сталася критична помилка:\n{str(e)}\n\nДеталі:\n{error_details}"
            )

    def save_and_new_candidate(self):
        self.save_candidate()
        self.add_candidate()

    def export_to_pdf(self):
        if not self.current_candidate_id:
            QMessageBox.warning(self, "Помилка", "Виберіть кандидата для експорту")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Зберегти PDF", f"candidate_{self.current_candidate_id}.pdf", "PDF Files (*.pdf)"
        )

        if file_path:
            candidate, phones = self.db_manager.get_candidate_by_id(self.current_candidate_id)
            if candidate:
                # Конвертуємо об'єкт candidate у словник
                candidate_dict = {}
                for column in candidate.__table__.columns:
                    value = getattr(candidate, column.name)
                    candidate_dict[column.name] = value

                # Додаємо телефони
                candidate_dict['phones'] = [phone.phone_number for phone in phones]

                exporter = PDFExporter()
                if exporter.export_candidate_to_pdf(candidate_dict, file_path):
                    QMessageBox.information(self, "Успіх", "PDF успішно експортовано")
                else:
                    QMessageBox.warning(self, "Помилка", "Не вдалося експортувати PDF")

    def export_to_excel(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Зберегти Excel", "candidates.xlsx", "Excel Files (*.xlsx)"
        )

        if file_path:
            exporter = ExcelExporter()
            if exporter.export_all_to_excel(file_path):
                QMessageBox.information(self, "Успіх", "Excel успішно експортовано")
            else:
                QMessageBox.warning(self, "Помилка", "Не вдалося експортувати Excel")

    def create_backup(self):
        success, message = self.backup_manager.create_backup()
        if success:
            QMessageBox.information(self, "Успіх", message)
        else:
            QMessageBox.warning(self, "Помилка", message)

    def restore_backup(self):
        backups = self.backup_manager.get_backup_files()
        if not backups:
            QMessageBox.information(self, "Інформація", "Немає доступних резервних копій")
            return

        file_path, _ = QFileDialog.getOpenFileName(
            self, "Виберіть резервну копію", self.backup_manager.backup_dir, "Backup Files (*.db)"
        )

        if file_path:
            reply = QMessageBox.question(
                self, "Підтвердження",
                "Ви впевнені, що хочете відновити з цієї резервної копії? Поточні дані будуть втрачені.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                success, message = self.backup_manager.restore_backup(file_path)
                if success:
                    QMessageBox.information(self, "Успіх", message)
                    self.refresh_list()
                else:
                    QMessageBox.warning(self, "Помилка", message)

    def import_from_excel(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Відкрити Excel", "", "Excel Files (*.xlsx *.xls)"
        )

        if file_path:
            success, message = self.data_importer.import_from_excel(file_path)
            if success:
                QMessageBox.information(self, "Успіх", message)
                self.refresh_list()
            else:
                QMessageBox.warning(self, "Помилка", message)

    def show_statistics(self):
        stats_dialog = QDialog(self)
        stats_dialog.setWindowTitle("Статистика кандидатів")
        stats_dialog.setMinimumSize(600, 400)

        layout = QVBoxLayout()

        # Загальна статистика
        total_count = self.statistics_manager.get_candidate_count()
        count_label = QLabel(f"Загальна кількість кандидатів: {total_count}")
        count_label.setStyleSheet("font-size: 14px; font-weight: bold; margin: 10px;")
        layout.addWidget(count_label)

        # Статистика за статтю
        gender_stats = self.statistics_manager.get_gender_stats()
        if gender_stats:
            gender_label = QLabel("Розподіл за статтю:")
            gender_label.setStyleSheet("font-size: 12px; font-weight: bold; margin: 5px;")
            layout.addWidget(gender_label)

            for gender, count in gender_stats.items():
                gender_info = QLabel(f"{gender}: {count} кандидатів")
                layout.addWidget(gender_info)

        # Статистика за датою
        date_stats = self.statistics_manager.get_candidates_by_date(30)
        if date_stats:
            date_label = QLabel("Кандидати за останні 30 днів:")
            date_label.setStyleSheet("font-size: 12px; font-weight: bold; margin: 5px;")
            layout.addWidget(date_label)

            for date, count in date_stats.items():
                date_info = QLabel(f"{date}: {count} кандидатів")
                layout.addWidget(date_info)

        # Кнопка закриття
        close_btn = QPushButton("Закрити")
        close_btn.setObjectName("primary-button")
        close_btn.clicked.connect(stats_dialog.accept)
        layout.addWidget(close_btn)

        stats_dialog.setLayout(layout)
        stats_dialog.exec()


# Додаємо цей блок для запуску файлу напряму
if __name__ == "__main__":
    # Додаємо шляхи для імпортів
    import sys
    import os

    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = CandidateManagementApp()
    window.show()
    sys.exit(app.exec())