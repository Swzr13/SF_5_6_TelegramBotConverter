import telebot
from Config import TOKEN, currency
from extensions import Converter, ConvertExeption

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'],)
def message_hello(message: telebot.types.Message):
    text = """Для конвертации валюты введите Валюта1 Валюта2 Количество
    Валюта1 - из которой конвентировать
    Валюта2 - в какую конвентировать
    Количество - сколько перевести
    Пример: руб доллар 100
    Список валюты - /values"""
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def message_values(message: telebot.types.Message):
    text = 'Доступные валюты\n'
    text += '\n'.join(f'{i+1}) {key} - {currency.get(key)}' for i, key in enumerate(currency.keys()))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    value = message.text.split(' ')
    value = list(map(str.lower, value))

    try:
        kurs, rez = Converter.get_price(value)
    except ConvertExeption as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Ошибка обработки команды\n{e}')
    else:
        base, quote, amount = value #что бы код читать проще
        text = f'1 {quote} = {kurs} {base}\n{amount} {quote} = {rez} {base}'
        bot.reply_to(message, text)

bot.polling(none_stop=True)