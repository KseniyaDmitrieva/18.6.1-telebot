from config import Config

import requests
import json


class Currencies:
    def __init__(self):
        self.currencies = ['usd', 'rub', 'eur']

    def get_values(self):
        return self.currencies


class ApiException(Exception):
    def __init__(self, text, bot, message):
        super().__init__(text)
        bot.reply_to(message, text)


class API:
    def __init__(self):
        self.domain = 'https://min-api.cryptocompare.com'
        self.api_key = Config().api_key

    def get_price(self, base, quote, amount):
        r = requests.get(f'{self.domain}/data/price?fsym={base}&tsyms={quote}&api_key={self.api_key}')
        if r.status_code == 200:
            price = json.loads(r.text)
            return float(price[quote.upper()]) * amount
        else:
            print(r.text) ## потенциально может быть указана важная информация
