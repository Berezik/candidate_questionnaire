import os
import shutil
from datetime import datetime
import pandas as pd
from database.database import DatabaseManager


class BackupManager:
    def __init__(self):
        self.backup_dir = "backups"
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    def create_backup(self):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(self.backup_dir, f"backup_{timestamp}.db")
            shutil.copy2("candidates.db", backup_file)
            return True, f"Резервну копію створено: {backup_file}"
        except Exception as e:
            return False, f"Помилка створення резервної копії: {e}"

    def restore_backup(self, backup_file):
        try:
            shutil.copy2(backup_file, "candidates.db")
            return True, "Резервну копію відновлено"
        except Exception as e:
            return False, f"Помилка відновлення резервної копії: {e}"

    def get_backup_files(self):
        backups = []
        for file in os.listdir(self.backup_dir):
            if file.endswith(".db"):
                file_path = os.path.join(self.backup_dir, file)
                file_time = os.path.getmtime(file_path)
                backups.append((file_path, datetime.fromtimestamp(file_time)))
        return sorted(backups, key=lambda x: x[1], reverse=True)


class DataImporter:
    def import_from_excel(self, file_path):
        try:
            db_manager = DatabaseManager()
            df = pd.read_excel(file_path)

            success_count = 0
            for _, row in df.iterrows():
                candidate_data = {
                    'last_name': row.get('Прізвище', ''),
                    'first_name': row.get('Ім\'я', ''),
                    'middle_name': row.get('По батькові', ''),
                    'tax_number': row.get('РНОКПП', ''),
                    'email': row.get('Email', ''),
                }

                if candidate_data['last_name'] and candidate_data['first_name']:
                    db_manager.add_candidate(candidate_data)
                    success_count += 1

            return True, f"Імпортовано {success_count} кандидатів"

        except Exception as e:
            return False, f"Помилка імпорту: {e}"