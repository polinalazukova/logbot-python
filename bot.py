from collections import defaultdict
import telebot
import os
from sqlite_repository import SQLiteUserRepository

# Initialize repository
user_repository = SQLiteUserRepository()

# Initialize bot
bot = telebot.TeleBot(os.environ['LOGGER_BOT_TOKEN'])

AVAILABLE_SERVERS = ["Сервер 1", "Сервер 2"]


# Создаем словарь для хранения состояния пользователей
user_states = defaultdict(str)  # по умолчанию состояние пустое

# Устанавливаем команды для бота
bot.set_my_commands([
    telebot.types.BotCommand("/start", "Начать работу с ботом"),
    telebot.types.BotCommand("/help", "Информация о командах бота"),
    telebot.types.BotCommand("/servers", "Управление серверами для мониторинга"),
    telebot.types.BotCommand("/notifications", "Включить/выключить уведомления"),
])

@bot.message_handler(commands=['start'])
def send_welcome(message):
    username = message.from_user.username or "unknown"
    chat_id = message.chat.id
    user_repository.add_user(username, chat_id)
    bot.send_message(chat_id, f"Привет, {username}! Ты добавлен в систему мониторинга.\n"
        "Теперь ты можешь получать уведомления о работе серверов.\n"
        "Используй /help, чтобы узнать, что я умею.")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(
        message.chat.id,
        "Вот что я умею:\n\n"
        "/start - Начать работу с ботом\n"
        "/help - Справка по командам\n"
        "/servers - Управление серверами для мониторинга\n"
        "/notifications - Управление уведомлениями\n"
    )

@bot.message_handler(commands=['servers'])
def manage_servers(message):
    user_servers = user_repository.get_servers_for_user(message.chat.id)
    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add("Отписаться от всех", "Показать сервера", "Отмена")
    if not user_servers:
        bot.send_message(
            message.chat.id,
            "Вы не подписаны на серверы. Выберите, что хотите сделать:",reply_markup=keyboard
        )
    else:
        # Если пользователь уже подписан на сервера

        bot.send_message(
            message.chat.id,
            "Вы подписаны на следующие серверы:\n" + "\n".join(user_servers) + "\n\nВыберите действие:",
            reply_markup=keyboard
        )

@bot.message_handler(func=lambda message: message.text == "Отмена")
def cancel_action(message):
    bot.send_message(message.chat.id, "Действие отменено.", reply_markup=telebot.types.ReplyKeyboardRemove())

@bot.message_handler(func=lambda message: message.text == "Отписаться от всех")
def unsubscribe_from_all(message):
    if user_repository.has_no_servers(message.chat.id):
        bot.send_message(message.chat.id, "Вы не подписаны на серверы.")
    else:
        user_repository.remove_all_servers(message.chat.id)
        bot.send_message(message.chat.id, "Вы отписались от всех серверов.")

@bot.message_handler(func=lambda message: message.text == "Показать сервера")
def servers_actions(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for server in AVAILABLE_SERVERS:
        keyboard.add(server)
    keyboard.add("Отмена")
    user_servers = user_repository.get_servers_for_user(message.chat.id)
    bot.send_message(message.chat.id,"Вы подписаны на следующие серверы:\n" + "\n".join(user_servers) + "\n\nВыберите удалить или добавить следующие серверы:"
                     ,reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text in AVAILABLE_SERVERS)
def manage_server(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add("Отмена")
    user_servers = user_repository.get_servers_for_user(message.chat.id)
    if message.text in user_servers:
        user_repository.remove_server(message.chat.id, message.text)
        bot.send_message(message.chat.id, f"Вы удалили сервер: {message.text}")
    else:
        user_repository.add_server(message.chat.id, message.text)
        bot.send_message(message.chat.id, f"Вы подписались на сервер: {message.text}")

# @bot.message_handler(func=lambda message: message.text == "Удалить сервер")
# def remove_server(message):
#     user_servers = user_repository.get_servers_for_user(message.chat.id)
#
#     if not user_servers:
#         bot.send_message(message.chat.id, "Вы не подписаны на серверы, чтобы их удалить.")
#     else:
#         keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
#         for server in user_servers:
#             keyboard.add(server)
#         keyboard.add("Отмена")
#         bot.send_message(
#             message.chat.id,
#             "Выберите сервер для удаления:",
#             reply_markup=keyboard
#         )
#
# @bot.message_handler(func=lambda message: message.text in user_repository.get_servers_for_user(message.chat.id))
# def handle_remove_selected_server(message):
#     user_servers = user_repository.get_servers_for_user(message.chat.id)
#
#     # Проверка, является ли выбранный сервер добавленным или удаляемым
#     if message.text not in user_servers:
#         bot.send_message(message.chat.id, "Вы не подписаны на этот сервер.")
#     else:
#         user_repository.remove_server(message.chat.id, message.text)
#         bot.send_message(message.chat.id, f"Вы удалили сервер: {message.text}")

@bot.message_handler(commands=['notifications'])
def notifications_settings(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add("Включить уведомления", "Отключить уведомления", "Отмена")
    bot.send_message(message.chat.id, "Выберите, хотите ли вы получать уведомления:", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text in ["Включить уведомления", "Отключить уведомления"])
def toggle_notifications(message):
    choice = message.text
    if choice == "Включить уведомления":
        user_repository.update_user_notifications(message.chat.id, "yes")
        bot.send_message(
            message.chat.id,
            "Уведомления включены.",
            reply_markup=telebot.types.ReplyKeyboardRemove()
        )
    elif choice == "Отключить уведомления":
        user_repository.update_user_notifications(message.chat.id, "no")
        bot.send_message(
            message.chat.id,
            "Уведомления отключены.",
            reply_markup=telebot.types.ReplyKeyboardRemove()
        )

@bot.message_handler(func=lambda message: True)
def handle_unknown(message):
    bot.send_message(message.chat.id, "Неизвестная команда. Используйте /help для получения списка команд.")

if __name__ == '__main__':
    bot.polling(none_stop=True)
