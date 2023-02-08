import requests
import json
from const import keys
import math


class ConvertionException(Exception):
    pass


class Convert:
    @staticmethod
    def get_price(quote: str, base: str, amount: int):
        if quote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}')

        try:
            quote_ticker = keys[quote.lower()]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}.')

        try:
            base_ticker = keys[base.lower()]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}.')
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}.')

        r = requests.get(f' https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_bas = json.loads(r.content)[keys[base]]
        total_base = total_bas * amount

        return round(total_base, 2)