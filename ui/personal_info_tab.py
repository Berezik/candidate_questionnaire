from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QGroupBox, QLineEdit, QDateEdit, QRadioButton,
                             QButtonGroup, QTextEdit, QCheckBox, QComboBox,
                             QLabel, QFileDialog, QMessageBox, QScrollArea,
                             QPushButton, QStackedWidget)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPixmap

# Додаємо шлях для імпортів
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import GenderEnum, DocumentTypeEnum, ReligionEnum


class PersonalInfoTab(QWidget):
    def __init__(self):
        super().__init__()
        self.photo_path = None
        self.init_ui()

    def init_ui(self):
        # Створюємо scroll area для можливості прокрутки
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)

        # Основна інформація
        basic_info_group = QGroupBox("Основна інформація")
        basic_info_layout = QFormLayout(basic_info_group)

        self.last_name_input = QLineEdit()
        self.first_name_input = QLineEdit()
        self.middle_name_input = QLineEdit()
        self.birth_date_edit = QDateEdit()
        self.birth_date_edit.setDate(QDate(1990, 1, 1))
        self.birth_date_edit.setCalendarPopup(True)
        self.birth_place_input = QLineEdit()
        self.tax_number_input = QLineEdit()

        # Стать
        gender_layout = QHBoxLayout()
        self.gender_male = QRadioButton("Чоловік")
        self.gender_female = QRadioButton("Жінка")
        gender_group = QButtonGroup()
        gender_group.addButton(self.gender_male)
        gender_group.addButton(self.gender_female)
        self.gender_male.setChecked(True)
        gender_layout.addWidget(self.gender_male)
        gender_layout.addWidget(self.gender_female)

        basic_info_layout.addRow("Прізвище:", self.last_name_input)
        basic_info_layout.addRow("Ім'я:", self.first_name_input)
        basic_info_layout.addRow("По батькові:", self.middle_name_input)
        basic_info_layout.addRow("Стать:", gender_layout)
        basic_info_layout.addRow("Дата народження:", self.birth_date_edit)
        basic_info_layout.addRow("Місце народження:", self.birth_place_input)
        basic_info_layout.addRow("РНОКПП (ІПН):", self.tax_number_input)

        # Документи
        docs_group = QGroupBox("Документи")
        docs_layout = QVBoxLayout(docs_group)

        # Вибір типу документа
        doc_type_layout = QHBoxLayout()
        self.passport_rb = QRadioButton("Паспорт книжечка")
        self.id_card_rb = QRadioButton("ID-картка")
        self.passport_rb.setChecked(True)
        doc_type_layout.addWidget(self.passport_rb)
        doc_type_layout.addWidget(self.id_card_rb)
        docs_layout.addLayout(doc_type_layout)

        # StackedWidget для різних типів документів
        self.docs_stacked = QStackedWidget()

        # Віджет для паспорта
        passport_widget = QWidget()
        passport_layout = QFormLayout(passport_widget)
        self.passport_series_input = QLineEdit()
        self.passport_number_input = QLineEdit()
        self.passport_issued_input = QLineEdit()
        self.passport_issue_date = QDateEdit()
        self.passport_issue_date.setDate(QDate.currentDate())
        self.passport_issue_date.setCalendarPopup(True)
        passport_layout.addRow("Серія:", self.passport_series_input)
        passport_layout.addRow("Номер:", self.passport_number_input)
        passport_layout.addRow("Ким і коли виданий:", self.passport_issued_input)
        passport_layout.addRow("Дата видачі:", self.passport_issue_date)

        # Віджет для ID-картки
        id_card_widget = QWidget()
        id_card_layout = QFormLayout(id_card_widget)
        self.id_number_input = QLineEdit()
        self.id_issue_date = QDateEdit()
        self.id_issue_date.setDate(QDate.currentDate())
        self.id_issue_date.setCalendarPopup(True)
        self.id_issued_by_input = QLineEdit()
        id_card_layout.addRow("Номер:", self.id_number_input)
        id_card_layout.addRow("Дата видачі:", self.id_issue_date)
        id_card_layout.addRow("Ким виданий:", self.id_issued_by_input)

        self.docs_stacked.addWidget(passport_widget)
        self.docs_stacked.addWidget(id_card_widget)
        docs_layout.addWidget(self.docs_stacked)

        # Адреси
        address_group = QGroupBox("Адреси")
        address_layout = QFormLayout(address_group)

        self.registration_address_input = QTextEdit()
        self.registration_address_input.setMaximumHeight(70)
        self.actual_address_input = QTextEdit()
        self.actual_address_input.setMaximumHeight(70)

        address_layout.addRow("Адреса реєстрації:", self.registration_address_input)
        address_layout.addRow("Адреса фактичного проживання:", self.actual_address_input)

        # Контактна інформація
        contact_group = QGroupBox("Контактна інформація")
        contact_layout = QVBoxLayout(contact_group)

        # Телефони
        phone_widget = QWidget()
        phone_layout = QFormLayout(phone_widget)
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("+380XXXXXXXXX")
        self.add_phone_btn = QPushButton("+ Додати ще телефон")
        phone_layout.addRow("Телефон:", self.phone_input)
        phone_layout.addRow("", self.add_phone_btn)

        self.phone2_input = QLineEdit()
        self.phone2_input.setPlaceholderText("Додатковий телефон (необов'язково)")
        self.phone2_input.setVisible(False)
        phone_layout.addRow("", self.phone2_input)

        # Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("example@mail.com")
        phone_layout.addRow("Email:", self.email_input)

        contact_layout.addWidget(phone_widget)

        # Додаткова інформація
        additional_group = QGroupBox("Додаткова інформація")
        additional_layout = QFormLayout(additional_group)

        self.nationality_input = QLineEdit()
        self.citizenship_input = QLineEdit()

        # Релігія
        religion_layout = QHBoxLayout()
        self.religion_forbids_weapons = QCheckBox(
            "Належність до релігійних організацій, вчення яких забороняє брати в руки зброю")
        religion_layout.addWidget(self.religion_forbids_weapons)

        # Віросповідання
        religion_combo_layout = QHBoxLayout()
        self.religion_combo = QComboBox()
        religions = [religion.value for religion in ReligionEnum]
        self.religion_combo.addItems(religions)
        self.alternative_religion_input = QLineEdit()
        self.alternative_religion_input.setPlaceholderText("Вкажіть ваше віросповідання")
        self.alternative_religion_input.setVisible(False)
        religion_combo_layout.addWidget(self.religion_combo)
        religion_combo_layout.addWidget(self.alternative_religion_input)

        # ВПО статус
        self.vpo_status_input = QLineEdit()
        self.vpo_status_input.setPlaceholderText("№ та адреса згідно довідки")

        additional_layout.addRow("Національність:", self.nationality_input)
        additional_layout.addRow("Громадянство:", self.citizenship_input)
        additional_layout.addRow("", religion_layout)
        additional_layout.addRow("Віросповідання:", religion_combo_layout)
        additional_layout.addRow("Статус ВПО:", self.vpo_status_input)

        # Банківська інформація
        bank_group = QGroupBox("Банківська інформація")
        bank_layout = QFormLayout(bank_group)

        self.bank_combo = QComboBox()
        banks = [
            "ПриватБанк", "Ощадбанк", "Укрексімбанк", "Raiffeisen Bank",
            "UTB Bank of Ukraine", "First Ukrainian International Bank (ПУМБ)",
            "Sense Bank", "Укрсиббанк", "Універсал Банк", "Crédit Agricole",
            "ОТП Банк", "Cidadebank", "КредоБанк", "Укргазбанк", "Південний", "Такомбанк"
        ]
        self.bank_combo.addItem("-- Оберіть банк --")  # Додали пустий варіант
        self.bank_combo.addItems(banks)

        self.iban_input = QLineEdit()
        self.iban_input.setPlaceholderText("UAXXXXXXXXXXXXXXXXXXXXXXXXX")
        self.has_credit_check = QCheckBox("Так, є кредит")

        bank_layout.addRow("Банк обслуговування:", self.bank_combo)
        bank_layout.addRow("IBAN рахунок:", self.iban_input)
        bank_layout.addRow("Чи є кредит?:", self.has_credit_check)

        # Транспортна інформація
        transport_group = QGroupBox("Транспорт")
        transport_layout = QFormLayout(transport_group)

        self.driver_license_input = QLineEdit()
        self.driver_license_input.setPlaceholderText("Категорія, стаж")
        self.vehicle_input = QLineEdit()
        self.vehicle_input.setPlaceholderText("Марка, номери")
        self.extreme_driving_check = QCheckBox("Так, є досвід екстремального водіння")

        transport_layout.addRow("Водійські права:", self.driver_license_input)
        transport_layout.addRow("Власний транспортний засіб:", self.vehicle_input)
        transport_layout.addRow("Досвід екстремального водіння:", self.extreme_driving_check)

        # Фото
        photo_group = QGroupBox("Фото кандидата")
        photo_layout = QVBoxLayout(photo_group)

        self.photo_label = QLabel()
        self.photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.photo_label.setFixedSize(150, 200)
        self.photo_label.setStyleSheet("border: 1px solid gray; background-color: #f0f0f0;")
        self.photo_label.setText("Фото не завантажено")

        photo_btn_layout = QHBoxLayout()
        self.upload_photo_btn = QPushButton("Завантажити фото")
        self.delete_photo_btn = QPushButton("Видалити фото")
        photo_btn_layout.addWidget(self.upload_photo_btn)
        photo_btn_layout.addWidget(self.delete_photo_btn)

        photo_layout.addWidget(self.photo_label, alignment=Qt.AlignmentFlag.AlignCenter)
        photo_layout.addLayout(photo_btn_layout)

        # Додаємо всі групи до layout
        layout.addWidget(basic_info_group)
        layout.addWidget(docs_group)
        layout.addWidget(address_group)
        layout.addWidget(contact_group)

        # Два стовпці для нижньої частини
        bottom_widget = QWidget()
        bottom_layout = QHBoxLayout(bottom_widget)
        bottom_layout.addWidget(additional_group)
        bottom_layout.addWidget(bank_group)

        layout.addWidget(bottom_widget)
        layout.addWidget(transport_group)
        layout.addWidget(photo_group)

        scroll.setWidget(content_widget)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(scroll)

        # Підключення сигналів
        self.passport_rb.toggled.connect(self.toggle_document_type)
        self.id_card_rb.toggled.connect(self.toggle_document_type)
        self.add_phone_btn.clicked.connect(self.add_phone_field)
        self.religion_combo.currentTextChanged.connect(self.toggle_religion_field)
        self.upload_photo_btn.clicked.connect(self.upload_photo)
        self.delete_photo_btn.clicked.connect(self.delete_photo)

    def toggle_document_type(self):
        if self.passport_rb.isChecked():
            self.docs_stacked.setCurrentIndex(0)
        else:
            self.docs_stacked.setCurrentIndex(1)

    def add_phone_field(self):
        self.phone2_input.setVisible(True)
        self.add_phone_btn.setEnabled(False)

    def toggle_religion_field(self):
        if self.religion_combo.currentText() == "Інше":
            self.alternative_religion_input.setVisible(True)
        else:
            self.alternative_religion_input.setVisible(False)

    def upload_photo(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Виберіть фото", "",
            "Images (*.png *.jpg *.jpeg *.bmp *.tiff);;All Files (*)"
        )
        if file_path:
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(150, 200, Qt.AspectRatioMode.KeepAspectRatio,
                                              Qt.TransformationMode.SmoothTransformation)
                self.photo_label.setPixmap(scaled_pixmap)
                self.photo_path = file_path
                print(f"Фото завантажено: {file_path}")
            else:
                QMessageBox.warning(self, "Помилка", "Не вдалося завантажити фото")

    def delete_photo(self):
        self.photo_label.clear()
        self.photo_label.setText("Фото не завантажено")
        self.photo_path = None
        print("Фото видалено")

    def clear_form(self):
        # Очищаємо всі поля форми
        self.last_name_input.clear()
        self.first_name_input.clear()
        self.middle_name_input.clear()
        self.birth_date_edit.setDate(QDate(1990, 1, 1))
        self.birth_place_input.clear()
        self.tax_number_input.clear()
        self.gender_male.setChecked(True)

        self.passport_series_input.clear()
        self.passport_number_input.clear()
        self.passport_issued_input.clear()
        self.passport_issue_date.setDate(QDate.currentDate())

        self.id_number_input.clear()
        self.id_issue_date.setDate(QDate.currentDate())
        self.id_issued_by_input.clear()

        self.registration_address_input.clear()
        self.actual_address_input.clear()

        self.phone_input.clear()
        self.phone2_input.clear()
        self.phone2_input.setVisible(False)
        self.add_phone_btn.setEnabled(True)
        self.email_input.clear()

        self.nationality_input.clear()
        self.citizenship_input.clear()
        self.religion_forbids_weapons.setChecked(False)
        self.religion_combo.setCurrentIndex(0)
        self.alternative_religion_input.clear()
        self.alternative_religion_input.setVisible(False)
        self.vpo_status_input.clear()

        self.bank_combo.setCurrentIndex(0)
        self.iban_input.clear()
        self.has_credit_check.setChecked(False)

        self.driver_license_input.clear()
        self.vehicle_input.clear()
        self.extreme_driving_check.setChecked(False)

        self.delete_photo()

        print("Форма очищена")

    def validate_form(self):
        try:
            print("Перевірка обов'язкових полів...")

            # Перевіряємо тільки обов'язкові поля
            if not self.last_name_input.text().strip():
                print("Помилка: не заповнено прізвище")
                QMessageBox.warning(self, "Помилка", "Введіть прізвище")
                self.last_name_input.setFocus()
                return False

            if not self.first_name_input.text().strip():
                print("Помилка: не заповнено ім'я")
                QMessageBox.warning(self, "Помилка", "Введіть ім'я")
                self.first_name_input.setFocus()
                return False

            if not self.tax_number_input.text().strip():
                print("Помилка: не заповнено РНОКПП")
                QMessageBox.warning(self, "Помилка", "Введіть РНОКПП (ІПН)")
                self.tax_number_input.setFocus()
                return False

            # Перевірка IBAN (якщо введено)
            iban = self.iban_input.text().strip()
            if iban and (len(iban) != 29 or not iban.startswith('UA')):
                print("Помилка: невірний формат IBAN")
                QMessageBox.warning(self, "Помилка", "IBAN має починатися з UA та мати 29 символів")
                self.iban_input.setFocus()
                return False

            print("Валідація пройдена успішно")
            return True

        except Exception as e:
            print(f"Помилка в validate_form: {e}")
            import traceback
            traceback.print_exc()
            return False

    def get_form_data(self):
        try:
            if not self.validate_form():
                print("Валідація форми не пройдена")
                return None

            print("Валідація форми пройдена успішно")

            # Збираємо дані з форми (обробляємо пусті значення)
            data = {
                'last_name': self.last_name_input.text().strip() or None,
                'first_name': self.first_name_input.text().strip() or None,
                'middle_name': self.middle_name_input.text().strip() or None,
                'tax_number': self.tax_number_input.text().strip() or None,
                'birth_date': self.birth_date_edit.date().toPyDate() if self.birth_date_edit.date() != QDate(1990, 1,
                                                                                                             1) else None,
                'birth_place': self.birth_place_input.text().strip() or None,
                'gender': GenderEnum.MALE if self.gender_male.isChecked() else GenderEnum.FEMALE if self.gender_female.isChecked() else None,
                'registration_address': self.registration_address_input.toPlainText().strip() or None,
                'actual_address': self.actual_address_input.toPlainText().strip() or None,
                'email': self.email_input.text().strip() or None,
                'nationality': self.nationality_input.text().strip() or None,
                'citizenship': self.citizenship_input.text().strip() or None,
                'religion_forbids_weapons': self.religion_forbids_weapons.isChecked() if self.religion_forbids_weapons.isChecked() else None,
                'vpo_status': self.vpo_status_input.text().strip() or None,
                'bank_name': self.bank_combo.currentText() if self.bank_combo.currentIndex() > 0 else None,
                'iban': self.iban_input.text().strip() or None,
                'has_credit': self.has_credit_check.isChecked() if self.has_credit_check.isChecked() else None,
                'driver_license': self.driver_license_input.text().strip() or None,
                'personal_vehicle': self.vehicle_input.text().strip() or None,
                'extreme_driving_experience': self.extreme_driving_check.isChecked() if self.extreme_driving_check.isChecked() else None,
                'photo_path': self.photo_path or None,
            }

            # Документи
            if self.passport_rb.isChecked():
                data['document_type'] = DocumentTypeEnum.PASSPORT
                data['passport_series'] = self.passport_series_input.text().strip() or None
                data['passport_number'] = self.passport_number_input.text().strip() or None
                data['passport_issued_by'] = self.passport_issued_input.text().strip() or None
                data[
                    'passport_issue_date'] = self.passport_issue_date.date().toPyDate() if self.passport_issue_date.date() != QDate.currentDate() else None
            else:
                data['document_type'] = DocumentTypeEnum.ID_CARD
                data['id_card_number'] = self.id_number_input.text().strip() or None
                data[
                    'id_card_issue_date'] = self.id_issue_date.date().toPyDate() if self.id_issue_date.date() != QDate.currentDate() else None
                data['id_card_issued_by'] = self.id_issued_by_input.text().strip() or None

            # Релігія
            religion_text = self.religion_combo.currentText()
            if religion_text != "Не вибрано":
                for religion in ReligionEnum:
                    if religion.value == religion_text:
                        data['religion'] = religion
                        break

                if religion_text == "Інше":
                    data['alternative_religion'] = self.alternative_religion_input.text().strip() or None

            # Телефони
            phones = []
            if self.phone_input.text().strip():
                phones.append({
                    'phone_number': self.phone_input.text().strip(),
                    'phone_type': 'personal'
                })
            if self.phone2_input.isVisible() and self.phone2_input.text().strip():
                phones.append({
                    'phone_number': self.phone2_input.text().strip(),
                    'phone_type': 'additional'
                })
                # Додаємо phones до даних
                data['phones'] = phones

                return data

            if phones:
                data['phones'] = phones

            print(f"Дані форми успішно зібрано: {len(data)} полів")
            return data

        except Exception as e:
            print(f"Помилка в get_form_data: {e}")
            import traceback
            traceback.print_exc()
            return None