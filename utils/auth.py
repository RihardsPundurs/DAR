import hashlib
from database.db_connection import DatabaseConnection
import bcrypt

def hash_password(password: str):
    # Atgriež hash un salt
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8'), salt.decode('utf-8')

def verify_password(stored_hash, salt, input_password):
    # Verificē paroli
    return bcrypt.checkpw(input_password.encode('utf-8'), stored_hash.encode('utf-8'))

def authenticate_user(username, password):
    #Autentificē lietotāju pret datubāzi
    try:
        db = DatabaseConnection().get_connection()
        cursor = db.cursor(dictionary=True)
        
        cursor.execute(
            "SELECT password_hash, salt, is_admin FROM users WHERE username = %s",
            (username,)
        )
        
        result = cursor.fetchone()
        if not result:
            return None
            
        stored_hash = result['password_hash']
        salt = result['salt']
        
        if verify_password(stored_hash, salt, password):
            return {
                'username': username,
                'is_admin': result['is_admin']
            }
            
        return None
    
        
    except Exception as e:
        print(f"Authentication error for user {username}: {e}")
        import traceback
        traceback.print_exc()
        return None