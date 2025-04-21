from utils.auth import hash_password
from database.db_connection import DatabaseConnection

def create_admin_account(username="admin", password="admin123"):
    password_hash, salt = hash_password(password)
    
    try:
        db = DatabaseConnection().get_connection()
        cursor = db.cursor()
        
        # Izdzēst veco adminu ja eksistē
        cursor.execute("DELETE FROM users WHERE username = 'admin'")
        
        # Izveidot jaunu adminu
        cursor.execute(
            "INSERT INTO users (username, password_hash, salt, is_admin) "
            "VALUES (%s, %s, %s, %s)",
            (username, password_hash, salt, True)
        )
        db.commit()
        print(f"Created admin user: {username}/{password}")
        
    except Exception as e:
        print(f"Error creating admin: {e}")
    finally:
        cursor.close()

if __name__ == "__main__":

    # Ja atstāts tukšs, izmantot admin/admin123
    name=input("Ievadi jaunu lietotājvārdu (ja atstāts tukšs, tiks izmantots \"admin\")")
    passw=input("Ievadi jaunu paroli (ja atstāts tukšs, tiks izmantots \"admin123\")")
    if name == "":
        name = "admin"
    if passw == "":
        passw = "admin123"
    create_admin_account(name,passw)