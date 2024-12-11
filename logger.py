import time
import random
from sqlite_repository import SQLiteUserRepository
from bot import bot

# Инициализируем репозиторий пользователей
user_repository = SQLiteUserRepository()


# Имитируем генерацию логов
def generate_logs(server_name):
    while True:
        is_error = random.choice([True, False])
        log_message = f"[{server_name}] Критическая ошибка: код {random.randint(1000, 9999)}" if is_error else f"[{server_name}] Сервер работает без ошибок."

        # Отправляем уведомления о критической ошибке
        if is_error:
            notify_error(server_name, log_message)

        time.sleep(10)


# Функция для отправки уведомлений о критических ошибках
def notify_error(server_name, message):
    # Получаем активных пользователей
    users = user_repository.get_active_users()

    # Проходим по всем активным пользователям
    for user in users:
        username, chat_id = user[0], user[1]

        # Получаем список серверов, которые отслеживает пользователь
        tracked_servers = user_repository.get_servers_for_user(chat_id)

        # Если пользователь не отслеживает сервера, пропускаем его
        if not tracked_servers:
            continue

        # Если пользователь отслеживает данный сервер, отправляем уведомление
        if server_name in tracked_servers:
            try:
                bot.send_message(chat_id=chat_id, text=message)
            except Exception as e:
                print(f"Ошибка при отправке уведомления пользователю {username}: {e}")