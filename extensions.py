import json
import requests

from Config import *

class ConvertExeption(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(value):
        if len(value) != 3:
            raise ConvertExeption('Неверное количество параметров')
        base, quote, amount = value

        if quote == base:
            raise ConvertExeption('Выбрана одна валюта')

        try:
            base_formatted = currency[base]
        except KeyError:
            raise ConvertExeption(f'Не удалось обработать валюту {base}')

        try:
            quote_formatted = currency[quote]
        except KeyError:
            raise ConvertExeption(f'Не удалось обработать валюту {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertExeption(f'Не удалось обработать количество {amount}')

        r = requests.get(f'http://api.currencylayer.com/live?access_key={TOKEN_API}')
        rez = json.loads(r.content)

        if base_formatted == 'USD':
            kurs = rez['quotes']['USD' + quote_formatted]
        elif quote_formatted == 'USD':
            kurs = rez['quotes']['USD' + base_formatted]
        else:
            kurs = rez['quotes']['USD' + base_formatted] / rez['quotes']['USD' + quote_formatted]

        total = float(amount) * float(kurs)

        return kurs, round(total, 3)

