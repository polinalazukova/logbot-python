import telebot
from database import init_db, add_user, update_user_server, get_active_users, update_user_notifications

# Инициализация базы данных
init_db()

# Инициализация бота
bot = telebot.TeleBot('7643285854:AAEu6YoNuEBt_yfK6tskNXYrYt3miHLiIXY')

# Доступные сервера
AVAILABLE_SERVERS = ["Сервер 1", "Сервер 2"]

# Устанавливаем команды для бота
bot.set_my_commands([
    telebot.types.BotCommand("/start", "Начать работу с ботом"),
    telebot.types.BotCommand("/help", "Информация о командах бота"),
    telebot.types.BotCommand("/server", "Выбрать сервер для мониторинга"),
    telebot.types.BotCommand("/notifications", "Включить/выключить уведомления"),
])


@bot.message_handler(commands=['start'])
def send_welcome(message):
    username = message.from_user.username or "unknown"
    chat_id = message.chat.id

    # Добавляем пользователя в базу данных
    add_user(username, chat_id)

    bot.send_message(
        chat_id,
        f"Привет, {username}! Ты добавлен в систему мониторинга.\n"
        "Теперь ты можешь получать уведомления о работе серверов.\n"
        "Используй /help, чтобы узнать, что я умею."
    )


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(
        message.chat.id,
        "Вот что я умею:\n\n"
        "/start - Начать работу с ботом\n"
        "/help - Справка по командам\n"
        "/server - Выбрать сервер для мониторинга\n"
        "/notifications - Управление уведомлениями\n"
    )


@bot.message_handler(commands=['server'])
def choose_server(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for server in AVAILABLE_SERVERS:
        keyboard.add(server)

    bot.send_message(
        message.chat.id,
        "Выберите сервер, от которого хотите получать уведомления:",
        reply_markup=keyboard
    )


@bot.message_handler(func=lambda message: message.text in AVAILABLE_SERVERS)
def set_server(message):
    selected_server = message.text
    update_user_server(message.chat.id, selected_server)
    bot.send_message(
        message.chat.id,
        f"Вы выбрали {selected_server}. Теперь вы будете получать уведомления от этого сервера.",
        reply_markup=telebot.types.ReplyKeyboardRemove()
    )


@bot.message_handler(commands=['notifications'])
def notifications_settings(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add("Включить уведомления", "Отключить уведомления")

    bot.send_message(
        message.chat.id,
        "Выберите, хотите ли вы получать уведомления:",
        reply_markup=keyboard
    )


@bot.message_handler(func=lambda message: message.text in ["Включить уведомления", "Отключить уведомления"])
def toggle_notifications(message):
    choice = message.text
    if choice == "Включить уведомления":
        update_user_notifications(message.chat.id, "yes")
        bot.send_message(
            message.chat.id,
            "Уведомления включены.",
            reply_markup=telebot.types.ReplyKeyboardRemove()
        )
    elif choice == "Отключить уведомления":
        update_user_notifications(message.chat.id, "no")
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
