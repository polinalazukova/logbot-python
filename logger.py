from database import get_active_users
import time
import random

# Имитируем генерацию логов
def generate_logs(server_name):
    while True:
        is_error = random.choice([True, False])
        log_message = f"[{server_name}] Критическая ошибка: код {random.randint(1000, 9999)}" if is_error else f"[{server_name}] Сервер работает без ошибок."

        # Логирование в файл
        with open(f'{server_name}_logs.txt', 'a') as log_file:
            log_file.write(log_message + '\n')

        # Отправляем уведомления о критической ошибке
        if is_error:
            notify_error(server_name, log_message)

        time.sleep(10)

def notify_error(server_name, message):
    from bot import bot  # Импортируем бота
    users = get_active_users()
    for user in users:
        username, chat_id, current_server = user
        if current_server == server_name:
            try:
                bot.send_message(chat_id=chat_id, text=message)
            except Exception as e:
                print(f"Ошибка при отправке уведомления пользователю {username}: {e}")