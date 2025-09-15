import os
import pandas as pd
from fpdf import FPDF
from datetime import datetime
from database.database import DatabaseManager


class PDFExporter:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)

    def export_candidate_to_pdf(self, candidate_data, output_path):
        try:
            self.pdf.add_page()

            # Заголовок
            self.pdf.set_font("Arial", 'B', 16)
            self.pdf.cell(0, 10, "АНКЕТА КАНДИДАТА", 0, 1, 'C')
            self.pdf.ln(5)

            # Особиста інформація
            self.pdf.set_font("Arial", 'B', 12)
            self.pdf.cell(0, 10, "Особиста інформація", 0, 1)
            self.pdf.set_font("Arial", '', 10)

            info_data = [
                ["Прізвище", candidate_data.get('last_name', '')],
                ["Ім'я", candidate_data.get('first_name', '')],
                ["По батькові", candidate_data.get('middle_name', '')],
                ["Дата народження", str(candidate_data.get('birth_date', ''))],
                ["Місце народження", candidate_data.get('birth_place', '')],
                ["РНОКПП", candidate_data.get('tax_number', '')],
                ["Стать", candidate_data.get('gender', '')],
                ["Національність", candidate_data.get('nationality', '')],
                ["Громадянство", candidate_data.get('citizenship', '')]
            ]

            for label, value in info_data:
                if value:
                    self.pdf.cell(50, 6, f"{label}:", 0, 0)
                    self.pdf.cell(0, 6, value, 0, 1)

            self.pdf.ln(5)

            # Контактна інформація
            self.pdf.set_font("Arial", 'B', 12)
            self.pdf.cell(0, 10, "Контактна інформація", 0, 1)
            self.pdf.set_font("Arial", '', 10)

            contact_data = [
                ["Email", candidate_data.get('email', '')],
                ["Адреса реєстрації", candidate_data.get('registration_address', '')],
                ["Адреса проживання", candidate_data.get('actual_address', '')]
            ]

            for label, value in contact_data:
                if value:
                    self.pdf.cell(50, 6, f"{label}:", 0, 0)
                    self.pdf.multi_cell(0, 6, value)

            self.pdf.ln(5)

            # Зберігаємо PDF
            self.pdf.output(output_path)
            return True

        except Exception as e:
            print(f"Помилка при експорті в PDF: {e}")
            return False


class ExcelExporter:
    def export_all_to_excel(self, output_path):
        try:
            db_manager = DatabaseManager()
            candidates = db_manager.get_all_candidates()

            data = []
            for candidate in candidates:
                data.append({
                    'Прізвище': candidate.last_name,
                    'Ім\'я': candidate.first_name,
                    'По батькові': candidate.middle_name,
                    'РНОКПП': candidate.tax_number,
                    'Дата народження': candidate.birth_date,
                    'Email': candidate.email,
                    'Телефон': candidate.phones[0].phone_number if candidate.phones else '',
                    'Дата додавання': candidate.created_date
                })

            df = pd.DataFrame(data)
            df.to_excel(output_path, index=False)
            return True

        except Exception as e:
            print(f"Помилка при експорті в Excel: {e}")
            return False