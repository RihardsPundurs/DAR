from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTabWidget,
    QTableWidget, QTableWidgetItem, QPushButton, QHeaderView,
    QMessageBox, QFormLayout, QLineEdit, QComboBox, QDoubleSpinBox
)
from PyQt6.QtCore import Qt, QDate
from database.db_connection import DatabaseConnection

class AdminPanel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Darba Uzskaite - Administrācija")
        self.setMinimumSize(800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        self.create_worker_tab()
        self.create_employer_tab()
        
        logout_btn = QPushButton("Iziet")
        logout_btn.clicked.connect(self.logout)
        layout.addWidget(logout_btn)
    
    def create_worker_tab(self):
        tab = QWidget()
        self.tabs.addTab(tab, "Strādnieku dati")
        
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        self.worker_table = QTableWidget()
        self.worker_table.setColumnCount(5)
        self.worker_table.setHorizontalHeaderLabels([
            "ID", "Vārds Uzvārds", "Datums", "Stundas", "Darbs"
        ])
        self.worker_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        refresh_btn = QPushButton("Atjaunot datus")
        refresh_btn.clicked.connect(self.load_worker_data)
        
        layout.addWidget(self.worker_table)
        layout.addWidget(refresh_btn)
        
        self.load_worker_data()
    
    def create_employer_tab(self):
        tab = QWidget()
        self.tabs.addTab(tab, "Uzņēmēju dati")
        
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Employer form
        form = QFormLayout()
        
        self.emp_name_input = QLineEdit()
        self.emp_rating_input = QComboBox()
        self.emp_rating_input.addItems(["ļoti slikti", "slikti", "viduvēji", "labi", "ļoti labi"])
        self.emp_salary_input = QDoubleSpinBox()
        self.emp_salary_input.setRange(0, 10000)
        self.emp_salary_input.setPrefix("€ ")
        
        form.addRow("Vārds Uzvārds:", self.emp_name_input)
        form.addRow("Izvērtējums:", self.emp_rating_input)
        form.addRow("Alga:", self.emp_salary_input)
        
        submit_btn = QPushButton("Saglabāt")
        submit_btn.clicked.connect(self.save_employer_data)
        
        # Employer table
        self.employer_table = QTableWidget()
        self.employer_table.setColumnCount(4)
        self.employer_table.setHorizontalHeaderLabels([
            "ID", "Vārds Uzvārds", "Izvērtējums", "Alga"
        ])
        
        layout.addLayout(form)
        layout.addWidget(submit_btn)
        layout.addWidget(self.employer_table)
        
        self.load_employer_data()
    
    def load_worker_data(self):
        try:
            db = DatabaseConnection().get_connection()
            cursor = db.cursor(dictionary=True)
            
            cursor.execute("""
            SELECT id, vards_uzvards, datums, nostradatas_stundas, padaritais_darbs 
            FROM stradnieka_apkopojums 
            ORDER BY created_at DESC
            """)
            
            workers = cursor.fetchall()
            self.worker_table.setRowCount(len(workers))
            
            for row_idx, worker in enumerate(workers):
                self.worker_table.setItem(row_idx, 0, QTableWidgetItem(str(worker['id'])))
                self.worker_table.setItem(row_idx, 1, QTableWidgetItem(worker['vards_uzvards']))
                self.worker_table.setItem(row_idx, 2, QTableWidgetItem(str(worker['datums'])))
                self.worker_table.setItem(row_idx, 3, QTableWidgetItem(str(worker['nostradatas_stundas'])))
                self.worker_table.setItem(row_idx, 4, QTableWidgetItem(worker['padaritais_darbs']))
                
        except Exception as e:
            QMessageBox.critical(self, "Kļūda", f"Nevar ielādēt strādnieku datus: {e}")
    
    def load_employer_data(self):
        try:
            db = DatabaseConnection().get_connection()
            cursor = db.cursor(dictionary=True)
            
            cursor.execute("SELECT id, vards_uzvards, izvertejums, alga FROM uzņemeja_apkopojums")
            
            employers = cursor.fetchall()
            self.employer_table.setRowCount(len(employers))
            
            for row_idx, employer in enumerate(employers):
                self.employer_table.setItem(row_idx, 0, QTableWidgetItem(str(employer['id'])))
                self.employer_table.setItem(row_idx, 1, QTableWidgetItem(employer['vards_uzvards']))
                self.employer_table.setItem(row_idx, 2, QTableWidgetItem(employer['izvertejums']))
                self.employer_table.setItem(row_idx, 3, QTableWidgetItem(str(employer['alga'])))
                
        except Exception as e:
            QMessageBox.critical(self, "Kļūda", f"Nevar ielādēt uzņēmēju datus: {e}")
    
    def save_employer_data(self):
        try:
            db = DatabaseConnection().get_connection()
            cursor = db.cursor()
            
            cursor.execute(
                "INSERT INTO uzņemeja_apkopojums "
                "(vards_uzvards, izvertejums, alga) "
                "VALUES (%s, %s, %s)",
                (
                    self.emp_name_input.text(),
                    self.emp_rating_input.currentText(),
                    self.emp_salary_input.value()
                )
            )
            
            db.commit()
            QMessageBox.information(self, "Veiksmīgi", "Uzņēmēja dati saglabāti!")
            
            # Clear inputs and refresh table
            self.emp_name_input.clear()
            self.emp_salary_input.setValue(0)
            self.load_employer_data()
            
        except Exception as e:
            QMessageBox.critical(self, "Kļūda", f"Neizdevās saglabāt datus: {e}")
    
    def logout(self):
        from ui.regular_mode import RegularModeWindow
        self.regular_window = RegularModeWindow()
        self.regular_window.show()
        self.close()