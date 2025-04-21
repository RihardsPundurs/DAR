import os
import mysql.connector
from mysql.connector import Error
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class DatabaseConnection:
    def __init__(self):
        self.connection = None
        self._initialize_database()

    def _get_base_connection(self):
        """Establish connection without specific database"""
        try:
            return mysql.connector.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD', ''),
                port=os.getenv('DB_PORT', '3306'),
                auth_plugin='mysql_native_password'
            )
        except Error as e:
            print(f"❌ Connection failed: {e}")
            raise

    def _initialize_database(self):
        """Initialize database structure"""
        try:
            self.connection = self._get_base_connection()
            cursor = self.connection.cursor()
            
            # Create database if needed
            cursor.execute("CREATE DATABASE IF NOT EXISTS darba_apkopojums")
            cursor.execute("USE darba_apkopojums")
            
            # Check if users table exists
            cursor.execute("""
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_schema = 'darba_apkopojums'
                AND table_name = 'users'
            """)
            
            if cursor.fetchone()[0] == 0:
                print("⚠️ Users table missing - initializing schema...")
                sql_file = Path(__file__).parent / 'darba_apkopojums.sql'
                if sql_file.exists():
                    with open(sql_file, 'r', encoding='utf-8') as file:
                        for statement in file.read().split(';'):
                            if statement.strip():
                                cursor.execute(statement)
                    print("✅ Database schema initialized")
                else:
                    print(f"⚠️ SQL file not found: {sql_file}")
            else:
                print("✅ Database already initialized")

            self.connection.commit()
            
        except Error as e:
            print(f"❌ Initialization failed: {e}")
            raise
        finally:
            if cursor:
                cursor.close()

    def get_connection(self):
        """Get authenticated connection to the database"""
        try:
            conn = mysql.connector.connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                database='darba_apkopojums',
                auth_plugin='mysql_native_password'
            )
            print("🔑 Database connection established")
            return conn
        except Error as e:
            print(f"❌ Authentication failed: {e}")
            raise