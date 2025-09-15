from datetime import datetime, timedelta
from database.database import DatabaseManager
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import QVBoxLayout, QWidget


class StatisticsManager:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def get_candidate_count(self):
        candidates = self.db_manager.get_all_candidates()
        return len(candidates)

    def get_candidates_by_date(self, days=30):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        candidates = self.db_manager.get_all_candidates()
        date_count = {}

        for candidate in candidates:
            if candidate.created_at:
                candidate_date = candidate.created_at.date()
                if start_date.date() <= candidate_date <= end_date.date():
                    date_str = candidate_date.strftime("%Y-%m-%d")
                    date_count[date_str] = date_count.get(date_str, 0) + 1

        return date_count

    def get_gender_stats(self):
        candidates = self.db_manager.get_all_candidates()
        gender_count = {'Чоловік': 0, 'Жінка': 0}

        for candidate in candidates:
            if candidate.gender:
                gender_count[candidate.gender.value] = gender_count.get(candidate.gender.value, 0) + 1

        return gender_count


class ChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = plt.Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

    def create_bar_chart(self, data, title, xlabel, ylabel):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        keys = list(data.keys())
        values = list(data.values())

        bars = ax.bar(keys, values)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        # Додаємо значення на стовпці
        for bar, value in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                    f'{value}', ha='center', va='bottom')

        plt.xticks(rotation=45)
        self.figure.tight_layout()
        self.canvas.draw()

    def create_pie_chart(self, data, title):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        labels = list(data.keys())
        sizes = list(data.values())

        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        ax.set_title(title)

        self.canvas.draw()