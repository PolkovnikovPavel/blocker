import time, psutil
from pywinauto import Desktop
import telebot
import threading


class Bot(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        my_timer = time.time()
        while True:
            try:
                start_polling()
            except Exception:
                print('Ошибка подключения')
                time.sleep(5)
            if time.time() - my_timer > 3570:
                break


bot = telebot.TeleBot('1986341221:AAEFvlugCI3dkM_yGPEtL613zaJ68-01htw')
is_checking = True
path_data = 'data'


windows = Desktop(backend="uia").windows()
print([w.window_text() for w in windows])


def close_other_launchers():
    process_iter = list(psutil.process_iter())
    launcher_p = []
    for process in process_iter:
        if 'launcher' in process.name():
            launcher_p.append(process)
    if len(launcher_p) > 2:
        need_time = max(map(lambda x: x.create_time(), launcher_p))
        for process in launcher_p:
            if process.create_time() != need_time:
                process.terminate()


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
    elif message.text.lower() == 'версия':
        try:
            with open('version.txt', encoding='utf8') as f:
                text = f.read()
                text = f'Версия: {text.split(":")[0]}'
        except Exception:
            text = 'По каким то причинам не получилось узнать версию'
    elif message.text.lower() == 'чс':
        with open(path_data, encoding='utf8') as f:
            ls = f.read().split('\n')[1::]
            text = '* чёрный список *\n\n' + '\n'.join(list(map(lambda x: f'{x}) {ls[x]}', range(len(ls)))))
    elif 'удалить ' in message.text.lower():
        try:
            num = int(message.text.lower().split('удалить ')[-1])
            with open(path_data, encoding='utf8') as f:
                ls = f.read().split('\n')[1::]
            del ls[num]
            if len(ls) > 0:
                new_text = f'{mode}\n' + '\n'.join(ls)
                with open(path_data, encoding='utf8', mode='w') as f:
                    f.write(new_text)
                is_checking = True
                text = 'В ближайшее время чёрный список будет обновлён'
            else:
                text = 'Нельзя полностью чистить чёрный список'
        except Exception:
            text = 'Введены некоректно данные'
    elif 'добавить ' in message.text.lower():
        name = message.text.split('обавить ')[-1]
        with open(path_data, encoding='utf8') as f:
            ls = f.read().split('\n')[1::]
        ls.append(name)
        new_text = f'{mode}\n' + '\n'.join(ls)
        with open(path_data, encoding='utf8', mode='w') as f:
            f.write(new_text)
        is_checking = True
        text = 'В ближайшее время чёрный список будет обновлён'
    elif message.text.lower() == 'показать приложения':
        rez = []
        for w in Desktop(backend="uia").windows():
            if w.window_text() != '':
                rez.append(w.window_text())
        text = '* Открытые окна *\n' + '\n\n'.join(rez)
    elif message.text.lower() == 'показать процессы':
        process_iter = list(psutil.process_iter())
        process_iter.sort(key=lambda x: x.name())
        rez = list(map(lambda x: x.name(), process_iter))
        text = '* Процессы *\n' + '\n\n'.join(rez)


    elif message.text.lower() == 'состояние':
        text = mode




    bot.send_message(message.chat.id, text)


def start_polling():
    bot.polling()


bot_puling = Bot()
bot_puling.start()
mode = 0
black_list = []
log = ['* Это начало логов *']
close_other_launchers()
bot.send_message(668018945, 'Запуск блокера')

while True:
    time.sleep(5)
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

