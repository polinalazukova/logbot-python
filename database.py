import sqlite3

DB_NAME = "users.db"

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect(DB_NAME)
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

def add_user(username, chat_id, current_server=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO users (username, chat_id, current_server, receive_notifications)
        VALUES (?, ?, ?, 'yes')
        """, (username, chat_id, current_server))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Пользователь с chat_id {chat_id} уже существует.")
    finally:
        conn.close()

def update_user_server(chat_id, server_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE users
    SET current_server = ?
    WHERE chat_id = ?
    """, (server_name, chat_id))
    conn.commit()
    conn.close()

def get_active_users():
    """
    Возвращает список активных пользователей, подписанных на уведомления.
    :return: список пользователей [(username, chat_id, current_server)]
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT username, chat_id, current_server 
    FROM users 
    WHERE receive_notifications = 'yes'
    """)
    users = cursor.fetchall()
    conn.close()
    return users

def get_available_servers():
    return ["Сервер 1", "Сервер 2"]

def update_user_notifications(chat_id, status):
    """
    Обновляет статус получения уведомлений для пользователя.
    :param chat_id: Идентификатор чата пользователя
    :param status: 'yes' для включения уведомлений, 'no' для отключения
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE users
    SET receive_notifications = ?
    WHERE chat_id = ?
    """, (status, chat_id))
    conn.commit()
    conn.close()