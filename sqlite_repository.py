import sqlite3
from abstract_repository import AbstractUserRepository

class SQLiteUserRepository(AbstractUserRepository):
    DB_NAME = "userSS.db"

    def __init__(self):
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            chat_id INTEGER NOT NULL UNIQUE,
            current_server TEXT,
            receive_notifications TEXT CHECK(receive_notifications IN ('yes', 'no')) DEFAULT 'yes'
        )
        """)
        conn.commit()
        conn.close()

    def add_user(self, username, chat_id, current_server=None):
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()
        try:
            cursor.execute("""
            INSERT INTO users (username, chat_id, current_server, receive_notifications)
            VALUES (?, ?, ?, 'yes')
            """, (username, chat_id, current_server))
            conn.commit()
        except sqlite3.IntegrityError:
            print(f"User with chat_id {chat_id} already exists.")
        finally:
            conn.close()

    def update_user_server(self, chat_id, server_name):
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE users
        SET current_server = ?
        WHERE chat_id = ?
        """, (server_name, chat_id))
        conn.commit()
        conn.close()

    def update_user_notifications(self, chat_id, status):
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE users
        SET receive_notifications = ?
        WHERE chat_id = ?
        """, (status, chat_id))
        conn.commit()
        conn.close()

    def get_active_users(self):
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
        SELECT username, chat_id, current_server 
        FROM users 
        WHERE receive_notifications = 'yes'
        """)
        users = cursor.fetchall()
        conn.close()
        return users