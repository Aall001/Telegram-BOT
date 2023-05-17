import json
import requests
from config import keys

class ConvertionExctption(Exception):
    pass


class ValutConventer:
    @staticmethod
    def convert(quote : str, base : str, amount : str):
        if quote == base:
            raise ConvertionExctption(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_tiker = keys[quote.lower()]
        except KeyError:
            raise ConvertionExctption(f'Не удалось обработать валюту {quote}')

        try:
            base_tiker = keys[base.lower()]
        except KeyError:
            raise ConvertionExctption(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionExctption(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_tiker}&tsyms={base_tiker}')
        total_base = json.loads(r.content)[keys[base.lower()]]

        return int(total_base)*amount
