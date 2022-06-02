from extensions import Currencies
from extensions import API
from extensions import ApiException
from config import Config

import telebot


API_TOKEN = Config().bot_token

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Этот бот умеет считать стоимость валют. Напишите строку в виде\
 *<имя валюты, цену которой хотите узнать> <имя валюты, в которой надо узнать цену первой валюты>\
  <количество первой валюты>*
""")


@bot.message_handler(commands=['values'])
def send_values(message):
    currencies = Currencies().get_values()
    currencies_str = ''
    for currency in currencies:
        currencies_str += f'- *{currency}*\n'
    bot.reply_to(message, f"""\
        Используемые для подсчета валюты:
{currencies_str}
""", parse_mode='markdown')


@bot.message_handler(func=lambda message: True)
def message_handler(message):
    message_parts = message.text.split()
    if len(message_parts) == 3:
        currencies = Currencies().get_values()
        if message_parts[0].lower() in currencies and message_parts[1].lower() in currencies:
            try:
                price = API().get_price(message_parts[0], message_parts[1], float(message_parts[2]))
                bot.reply_to(message, price)
            except ValueError:
                ApiException('Неверно указано количество валюты', bot, message)

        else:
            ApiException('Укажите поддерживаемые валюты', bot, message)
    else:
        ApiException('Неверно указано количество переменных в запросе', bot, message)


bot.infinity_polling()
