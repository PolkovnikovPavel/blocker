import time, psutil

import requests, os


def update():
    global version
    with open('version.txt', encoding='utf-8') as f:
        version, name = f.read().split(':')

    all_versions = requests.get('https://raw.githubusercontent.com/PolkovnikovPavel/blocker/master/all_versions').text
    new_version = all_versions.split('\n')[0]
    #new_version = '1.0.1'

    if version != new_version:
        for data in all_versions.split('\n')[1::]:
            v, url = data.split(' - ')
            if v == new_version:
                r = requests.get(url)
                with open(name, 'wb') as f:
                    f.write(r.content)
                with open('version.txt', 'w', encoding='utf-8') as f:
                    f.write(f'{new_version}:{name}')
                version = new_version
                print('Обновление прошло успешно')
                break
    elif version == new_version:
        print('Уже установлена последняя версия')

with open('version.txt', encoding='utf-8') as f:
    version, name = f.read().split(':')


update()
os.startfile(name)
while True:
    time.sleep(60 * 60)   # 1 час
    for program in psutil.process_iter():
        if name == program.name():
            program.terminate()
    os.startfile(name)
    time.sleep(60 * 60)   # 1 час
    for program in psutil.process_iter():
        if name == program.name():
            program.terminate()
    update()
    os.startfile(name)




