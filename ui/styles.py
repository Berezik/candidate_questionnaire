def get_light_style():
    return """
    QMainWindow, QWidget {
        background-color: #f5f5f5;
    }
    QGroupBox {
        font-weight: bold;
        border: 1px solid #cccccc;
        border-radius: 5px;
        margin-top: 10px;
        padding-top: 10px;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px 0 5px;
    }
    QPushButton {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 5px 10px;
        border-radius: 3px;
    }
    QPushButton:hover {
        background-color: #45a049;
    }
    QLineEdit, QTextEdit, QComboBox, QDateEdit {
        padding: 5px;
        border: 1px solid #cccccc;
        border-radius: 3px;
    }
    QListWidget {
        border: 1px solid #cccccc;
        border-radius: 3px;
        background-color: white;
    }
    """

def get_dark_style():
    return """
    QMainWindow, QWidget {
        background-color: #2d2d2d;
        color: #ffffff;
    }
    QGroupBox {
        font-weight: bold;
        border: 1px solid #555555;
        border-radius: 5px;
        margin-top: 10px;
        padding-top: 10px;
        color: #ffffff;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px 0 5px;
        color: #ffffff;
    }
    QPushButton {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 5px 10px;
        border-radius: 3px;
    }
    QPushButton:hover {
        background-color: #45a049;
    }
    QLineEdit, QTextEdit, QComboBox, QDateEdit {
        padding: 5px;
        border: 1px solid #555555;
        border-radius: 3px;
        background-color: #3d3d3d;
        color: #ffffff;
    }
    QListWidget {
        border: 1px solid #555555;
        border-radius: 3px;
        background-color: #3d3d3d;
        color: #ffffff;
    }
    """