import sqlite3
from abstract_repository import AbstractUserRepository

class SQLiteUserRepository(AbstractUserRepository):
    DB_NAME = "userSS.db"

    # Инициализация базы данных
    def __init__(self):
        self._init_db()

    # Создание таблиц "users" и "user_servers" в базе данных
    def _init_db(self):
        conn = sqlite3.connect(self.DB_NAME)  # Подключаемся к базе данных
        cursor = conn.cursor()  # Создаем курсор для выполнения SQL-запросов

        # Таблица пользователей
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            chat_id INTEGER NOT NULL UNIQUE,
            receive_notifications TEXT CHECK(receive_notifications IN ('yes', 'no')) DEFAULT 'yes'
        )
        """)

        # Таблица отслеживаемых серверов
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_servers (
            user_id INTEGER NOT NULL,
            server_name TEXT NOT NULL,
            PRIMARY KEY (user_id, server_name),
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
        """)

        conn.commit()
        conn.close()

    def add_user(self, username, chat_id):
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()
        try:
            cursor.execute("""
            INSERT INTO users (username, chat_id, receive_notifications)
            VALUES (?, ?, 'yes')
            """, (username, chat_id))
            conn.commit()
        except sqlite3.IntegrityError:  # Обрабатываем ошибку, если пользователь с таким chat_id уже существует
            print(f"User with chat_id {chat_id} already exists.")
        finally:
            conn.close()

    def add_server(self, chat_id, server_name):
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()
        try:
            # Получаем ID пользователя
            cursor.execute("SELECT id FROM users WHERE chat_id = ?", (chat_id,))
            user_id = cursor.fetchone()

            if user_id:
                cursor.execute("""
                INSERT OR IGNORE INTO user_servers (user_id, server_name)
                VALUES (?, ?)
                """, (user_id[0], server_name))
                conn.commit()
            else:
                print(f"User with chat_id {chat_id} not found.")
        finally:
            conn.close()

    def remove_server(self, chat_id, server_name):
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()
        try:
            # Получаем ID пользователя
            cursor.execute("SELECT id FROM users WHERE chat_id = ?", (chat_id,))
            user_id = cursor.fetchone()

            if user_id:
                cursor.execute("""
                DELETE FROM user_servers
                WHERE user_id = ? AND server_name = ?
                """, (user_id[0], server_name))
                conn.commit()
            else:
                print(f"User with chat_id {chat_id} not found.")
        finally:
            conn.close()

    def remove_all_servers(self, chat_id):
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()
        try:
            # Получаем ID пользователя
            cursor.execute("SELECT id FROM users WHERE chat_id = ?", (chat_id,))
            user_id = cursor.fetchone()

            if user_id:
                # Удаляем все записи для пользователя из таблицы user_servers
                cursor.execute("""
                DELETE FROM user_servers
                WHERE user_id = ?
                """, (user_id[0],))
                conn.commit()
            else:
                print(f"User with chat_id {chat_id} not found.")
        finally:
            conn.close()

    def has_no_servers(self, chat_id):
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()
        try:
            # Проверяем, есть ли у пользователя записи в таблице user_servers
            cursor.execute("""
            SELECT COUNT(*)
            FROM user_servers
            WHERE user_id = (SELECT id FROM users WHERE chat_id = ?)
            """, (chat_id,))
            count = cursor.fetchone()[0]
            return count == 0
        finally:
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
        SELECT username, chat_id
        FROM users
        WHERE receive_notifications = 'yes'
        """)
        users = cursor.fetchall()
        conn.close()
        return users

    def get_servers_for_user(self, chat_id):
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
        SELECT server_name
        FROM user_servers
        WHERE user_id = (SELECT id FROM users WHERE chat_id = ?)
        """, (chat_id,))
        servers = cursor.fetchall()
        conn.close()
        return [server[0] for server in servers]  # Преобразуем список кортежей в список строк
