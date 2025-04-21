import sys
import hashlib
import secrets
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt
import mysql.connector
from mysql.connector import Error

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Darba uzskaites sistēma - Pieslēgšanās")
        self.setFixedSize(400, 300)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # UI Elements
        self.title_label = QLabel("Administrātora pieslēgšanās")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        self.username_label = QLabel("Lietotājvārds:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Ievadiet lietotājvārdu")
        
        self.password_label = QLabel("Parole:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Ievadiet paroli")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.login_button = QPushButton("Pieslēgties")
        self.login_button.clicked.connect(self.authenticate_user)
        
        # Add widgets to layout
        layout.addWidget(self.title_label)
        layout.addSpacing(20)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addSpacing(20)
        layout.addWidget(self.login_button)
        
        # Database connection
        self.db_connection = self.create_db_connection()
        
        # Create admin user if not exists (for first run)
        self.create_default_admin()
    
    def create_db_connection(self):
        """Create database connection following best practices"""
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='your_username',
                password='your_password',
                database='darba_apkopojums'
            )
            return connection
        except Error as e:
            QMessageBox.critical(self, "Kļūda", f"Nevar pieslēgties datu bāzei: {e}")
            return None
    
    def hash_password(self, password, salt=None):
        """Securely hash password with salt"""
        if not salt:
            salt = secrets.token_hex(16)
        salted_password = password + salt
        hash_obj = hashlib.sha256(salted_password.encode())
        return hash_obj.hexdigest(), salt
    
    def create_default_admin(self):
        """Create default admin user if none exists"""
        if not self.db_connection:
            return
            
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT * FROM users WHERE is_admin = TRUE")
            if not cursor.fetchone():
                # No admin exists, create one
                username = "admin"
                password = "default_admin_password"
                password_hash, salt = self.hash_password(password)
                
                cursor.execute(
                    "INSERT INTO users (username, password_hash, salt, is_admin) "
                    "VALUES (%s, %s, %s, %s)",
                    (username, password_hash, salt, True)
                )
                self.db_connection.commit()
                
                QMessageBox.information(
                    self, "Noklusējuma administrators", 
                    f"Izveidots noklusējuma administrators:\nLietotājvārds: {username}\nParole: {password}\n\nLŪDZU MAINIET PAROLI PĒC PIERAKSTĪŠANĀS!"
                )
        except Error as e:
            QMessageBox.critical(self, "Kļūda", f"Neizdevās izveidot administratoru: {e}")
    
    def authenticate_user(self):
        """Authenticate user against database"""
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Trūkst informācijas", "Lūdzu ievadiet lietotājvārdu un paroli!")
            return
            
        if not self.db_connection:
            QMessageBox.critical(self, "Kļūda", "Nav savienojuma ar datu bāzi!")
            return
            
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "SELECT password_hash, salt, is_admin FROM users WHERE username = %s",
                (username,))
            result = cursor.fetchone()
            
            if not result:
                QMessageBox.warning(self, "Neveiksmīga pieslēgšanās", "Nepareizs lietotājvārds vai parole!")
                return
                
            stored_hash, salt, is_admin = result
            input_hash, _ = self.hash_password(password, salt)
            
            if input_hash == stored_hash:
                if is_admin:
                    QMessageBox.information(self, "Veiksmīga pieslēgšanās", "Administrātors autentificēts!")
                    self.open_admin_panel()
                else:
                    QMessageBox.information(self, "Veiksmīga pieslēgšanās", "Lietotājs autentificēts!")
                    # Open regular user interface
            else:
                QMessageBox.warning(self, "Neveiksmīga pieslēgšanās", "Nepareizs lietotājvārds vai parole!")
                
        except Error as e:
            QMessageBox.critical(self, "Kļūda", f"Autentifikācijas kļūda: {e}")
    
    def open_admin_panel(self):
        """Open admin control panel"""
        from admin_panel import AdminPanel  # We'll create this next
        self.admin_panel = AdminPanel(self.db_connection)
        self.admin_panel.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application style for consistent look across platforms
    app.setStyle('Fusion')
    
    login_window = LoginWindow()
    login_window.show()
    
    sys.exit(app.exec())
