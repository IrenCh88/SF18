import telebot
import const
from const import keys, token
from currency import ConvertionException, Convert



bot = telebot.TeleBot(const.token)


@bot.message_handler(commands=["start", "help"])
def help(message: telebot.types.Message):
    print('start/ help')
    text = "Чтобы начать работу с ботом, введите команду в одной строке: " \
           "\n 1. Имя валюты " \
           "\n 2. Имя конвертируемой валюты " \
           "\n 3. Количество первой валюты " \
           "\n Увидеть список доступной валюты: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values', ])
def values(message: telebot.types.Message):
    text = "Доступные валюты: "
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionException('Не дописали команду.')

        quote, base, amount = values
        total_base = Convert.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ой! Что-то не правильно ввели!\n {e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n {e}')
    else:
        text = f'Цена {amount} {quote} в {base} = {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
