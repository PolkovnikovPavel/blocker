import time
from pywinauto import Desktop
import telebot
import threading


class Bot(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        for i in range(10):
            try:
                start_polling()
            except Exception:
                print('Ошибка подключения')
                time.sleep(5)


bot = telebot.TeleBot('1772570477:AAHD_RuVGv6yEw6SecPIor91ULdSL2YBDOc')
is_checking = True
path_data = 'C:/Users/python/programs/blocker/data'


windows = Desktop(backend="uia").windows()
print([w.window_text() for w in windows])


def check_black_list(black_list):
    windows = Desktop(backend="uia").windows()
    rez = False
    for window in windows:
        for i in black_list:
            if i in window.window_text():
                window.close()
                rez = window.window_text()
    return rez


@bot.message_handler(content_types=['text'])
def echo_all(message):
    global is_checking
    text = 'У меня такой команды нет!'
    if message.text.lower() == 'информация':
        text = 'Информация'
    elif message.text.lower() == 'проверить':
        rez = check_black_list(black_list)
        if rez:
            text = f'закрыто {rez}'
        else:
            text = 'ничего нет'
    elif message.text.lower() == 'логи':
        text = '\n\n'.join(log)
    elif message.text.lower() == 'сверить':
        is_checking = True
        text = 'В ближайшее время данные будут сверены'
    elif message.text.lower() == 'стоп':
        with open(path_data, encoding='utf8') as f:
            text = f.read()
        new_text = '0\n' + '\n'.join(text.split('\n')[1::])
        with open(path_data, encoding='utf8', mode='w') as f:
            f.write(new_text)
        is_checking = True
        text = 'В ближайшее время проверка прекратиться'
    elif message.text.lower() == 'старт':
        with open(path_data, encoding='utf8') as f:
            text = f.read()
        new_text = '1\n' + '\n'.join(text.split('\n')[1::])
        with open(path_data, encoding='utf8', mode='w') as f:
            f.write(new_text)
        is_checking = True
        text = 'В ближайшее время начнётся проверка'

    bot.send_message(message.chat.id, text)


def start_polling():
    bot.polling()


bot_puling = Bot()
bot_puling.start()
mode = 0
black_list = []
log = ['* Это начало логов *']

while True:
    time.sleep(2)
    if is_checking:
        with open(path_data, encoding='utf8') as f:
            text = f.read()
        mode = int(text.split('\n')[0])
        black_list = []
        for word in text.split('\n')[1::]:
            black_list.append(word)
        print(mode, black_list)
        is_checking = False
    if mode == 1:
        rez = check_black_list(black_list)
        if rez:
            print(f'закрыто {rez}')
            log.append(f'закрыто {rez}')
        else:
            print('ничего нет')

