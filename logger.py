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

        # Логирование в файл
        with open(f'{server_name}_logs.txt', 'a', encoding='utf-8') as log_file:
            log_file.write(log_message + '\n')

        # Отправляем уведомления о критической ошибке
        if is_error:
            notify_error(server_name, log_message)

        time.sleep(10)


# Функция для отправки уведомлений о критических ошибках
def notify_error(server_name, message):
    # Получаем активных пользователей
    users = user_repository.get_active_users()

    # Проходим по всем пользователям и отправляем уведомления
    for user in users:
        username, chat_id, current_server = user
        if current_server == server_name:
            try:
                bot.send_message(chat_id=chat_id, text=message)
            except Exception as e:
                print(f"Ошибка при отправке уведомления пользователю {username}: {e}")

'''def notify_error(server_name, message):
    # Получаем активных пользователей
    users = user_repository.get_active_users()

    # Проходим по всем пользователям и отправляем уведомления
    for user in users:
        username, chat_id, current_server = user
        if current_server == server_name:
            try:
                # Логирование перед отправкой сообщения
                print(f"Sending error message to {username} (chat_id: {chat_id}) for server {server_name}")
                bot.send_message(chat_id=chat_id, text=message)
            except Exception as e:
                # Логирование ошибок при отправке
                print(f"Ошибка при отправке уведомления пользователю {username} (chat_id: {chat_id}): {e}")
'''
