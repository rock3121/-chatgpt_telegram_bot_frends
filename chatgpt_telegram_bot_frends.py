# Импорт необходимых модулей
import telebot
import openai

# Задаем токен бота Telegram и модель chatgpt.
openai.api_key = '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'
bot = telebot.TeleBot('6299211280:AAHQYwN58y4ODPvYZyh-Dg2uMq8S6Fxehkw')
MODEL_NAME = 'text-davinci-003'

# обработчик команды /start
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.reply_to(message, 'Здравствуйте! Я бот, готовый помочь вам. Напишите мне, чтобы начать диалог.')

# общий обработчик сообщений
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    try:
        # отправляем запрос на сервер chatgpt и получаем ответ
        response = openai.Completion.create(
            engine = MODEL_NAME,
            prompt = f'{message.text.strip()}\nAI: ',
            temperature = 0.6,
            max_tokens = 4000,
            top_p = 1,
            frequency_penalty = 0,
            presence_penalty = 0
        )

        # парсинг ответа модели
        answer = response.choices[0].text.strip()

    except Exception as e:
        # если произошла ошибка, отправляем сообщение об ошибке пользователю
        error_message = f'Произошла ошибка при работе с моделью: {e}'
        print(error_message)
        bot.reply_to(message, error_message)
        return

    # если модель не может ответить на вопрос пользователя, отправляем стандартный ответ
    answer = answer or 'Я не могу ответить на этот вопрос'

    # отправка ответа пользователю
    bot.send_message(message.chat.id, answer)

# запуск бота Telegram
if __name__ == "__main__":
    bot.polling(none_stop=True)