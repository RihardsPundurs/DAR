from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt
from utils.auth import authenticate_user
from ui.admin_panel import AdminPanel

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Darba Uzskaite - Pieslēgšanās")
        self.setFixedSize(400, 300)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        self.title_label = QLabel("Administrātora Pieslēgšanās")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Lietotājvārds")
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Parole")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.login_btn = QPushButton("Pieslēgties")
        self.login_btn.clicked.connect(self.authenticate)
        
        self.back_btn = QPushButton("Atgriezties parastajā režīmā")
        self.back_btn.clicked.connect(self.back_to_regular)
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_btn)
        layout.addWidget(self.back_btn)
    
    def authenticate(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Trūkst informācijas", "Lūdzu ievadiet lietotājvārdu un paroli!")
            return
        
        user = authenticate_user(username, password)
        
        if user and user.get('is_admin'):
            self.admin_panel = AdminPanel()
            self.admin_panel.show()
            self.close()
        else:
            QMessageBox.warning(self, "Neveiksmīga pieslēgšanās", "Nepareizs lietotājvārds vai parole!")
    
    def back_to_regular(self):
        from ui.regular_mode import RegularModeWindow
        self.regular_window = RegularModeWindow()
        self.regular_window.show()
        self.close()