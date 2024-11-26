import telebot
import requests

# Инициализация бота с токеном
bot = telebot.TeleBot('7643285854:AAEu6YoNuEBt_yfK6tskNXYrYt3miHLiIXY')

# Список команд с описанием
commands = [
    telebot.types.BotCommand("/start", "Get a welcome message"),
    telebot.types.BotCommand("/help", "Info how to use this bot"),
    telebot.types.BotCommand("/checkserver", "Check server")
]

# Устанавливаем команды для бота
bot.set_my_commands(commands)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я бот для мониторинга ошибок.\nЯ буду отправлять вам уведомления о критических ошибках, обнаруженных в логах.")

# Обработчик команды /help
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(
        message.chat.id,
        "Я могу помочь тебе с основными функциями. Вот что я умею:\n\n"
        "/start - Начать разговор и сбросить настройки.\n"
        "/help - Получить информацию о командах."
    )

@bot.message_handler(commands=['checkserver'])
def check_server(message):
    try:
        response = requests.get('http://localhost:5000/ping')
        if response.status_code == 200:
            bot.send_message(message.chat.id, f"Сервер работает: {response.json()['message']}")
        else:
            bot.send_message(message.chat.id, "Не удалось подключиться к серверу.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при подключении к серверу: {e}")

@bot.message_handler(func=lambda message: True)
def handle_unknown(message):
    bot.send_message(message.chat.id, "Я не знаю такой команды...")

# Запуск бота
bot.polling(none_stop=True)





