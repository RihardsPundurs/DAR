from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QFormLayout,
    QLineEdit, QDateEdit, QDoubleSpinBox, QTextEdit,
    QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt, QDate
from database.db_connection import DatabaseConnection

class RegularModeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Darba Uzskaite - Parasts Režīms")
        self.setFixedSize(500, 400)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Form for worker data
        form = QFormLayout()
        
        self.name_input = QLineEdit()
        self.date_input = QDateEdit(QDate.currentDate())
        self.hours_input = QDoubleSpinBox()
        self.hours_input.setRange(0, 24)
        self.hours_input.setSingleStep(0.5)
        self.work_input = QTextEdit()
        
        form.addRow("Vārds Uzvārds:", self.name_input)
        form.addRow("Datums:", self.date_input)
        form.addRow("Nostrādātās stundas:", self.hours_input)
        form.addRow("Paveiktais darbs:", self.work_input)
        
        submit_btn = QPushButton("Saglabāt")
        submit_btn.clicked.connect(self.save_worker_data)
        
        login_btn = QPushButton("Pieslēgties kā administrators")
        login_btn.clicked.connect(self.show_login)
        
        layout.addLayout(form)
        layout.addWidget(submit_btn)
        layout.addWidget(login_btn)
    
    def save_worker_data(self):
        """Save worker data to database"""
        try:
            db = DatabaseConnection().get_connection()
            cursor = db.cursor()
            
            cursor.execute(
                "INSERT INTO stradnieka_apkopojums "
                "(vards_uzvards, datums, nostradatas_stundas, padaritais_darbs) "
                "VALUES (%s, %s, %s, %s)",
                (
                    self.name_input.text(),
                    self.date_input.date().toString("yyyy-MM-dd"),
                    self.hours_input.value(),
                    self.work_input.toPlainText()
                )
            )
            
            db.commit()
            QMessageBox.information(self, "Veiksmīgi", "Dati saglabāti!")
            
            # Clear inputs
            self.name_input.clear()
            self.work_input.clear()
            self.hours_input.setValue(0)
            
        except Exception as e:
            QMessageBox.critical(self, "Kļūda", f"Neizdevās saglabāt datus: {e}")
    
    def show_login(self):
        """Switch to login window"""
        from ui.login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()