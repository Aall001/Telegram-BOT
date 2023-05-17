import telebot
from config import keys, TOKEN
from extensions import ConvertionExctption, ValutConventer
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    text = 'Чтобы начать работу с ботом введите команду в следующем формате:\n\n <имя валюты цену которой Вы хотите узнать>\
<имя валюты в которой надо узнать цену первой валюты>\
<количество первой валюты> \n \n Пример для ввода: доллар рубль 1\
\n \n Чтобы увидеть список всех доступных валют нажмите: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def value(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionExctption('Введено не верное количество или значение параметров\n\nПример для ввода: доллар рубль 1')

        quote, base, amount = values
        total_base = ValutConventer.convert(quote, base, amount)
    except ConvertionExctption as e:
        bot.reply_to(message, f'Ошибка пользователя \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать валюту \n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()