import sys
from PyQt6.QtWidgets import QApplication
from ui.regular_mode import RegularModeWindow
from database.db_connection import DatabaseConnection

def initialize_application():
    try:
        db = DatabaseConnection()
        return True
    except Exception as e:
        print(f"Application initialization failed: {e}")
        return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    if not initialize_application():
        sys.exit(1)
    
    regular_window = RegularModeWindow()
    regular_window.show()
    
    sys.exit(app.exec())