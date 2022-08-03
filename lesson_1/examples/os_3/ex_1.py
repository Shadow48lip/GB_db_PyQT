"""Функции модуля os"""

import os
import platform

from pprint import pprint

# информация о платформе
# ‘posix’, ‘nt’, ‘os2’, ‘ce’, ‘java’, ‘riscos’
# ответ: nt для Windows

print('os.name = ', os.name)

# дает вам полезную информацию, такую как: количество процессоров
# тип ОЗУ, имя компьютера, и так далее
print(os.environ)
pprint(list(os.environ.keys()))

# узнать, сколько процессорных ядер в системе
if platform.system().lower() == 'windows':
    print(os.environ["NUMBER_OF_PROCESSORS"])
else:
    print('cpu_count: ', os.cpu_count())

# какой путь вы в данный момент используете
print('current directory: ', os.getcwd())
path_dir = os.path.dirname(os.path.abspath('__file__'))
print('current directory for a specific file: ', path_dir)

# изменяем текущий путь
# NEW_PATH = os.path.join(os.getcwd(), 'lesson_1/examples/os_3/new_dir')
NEW_PATH = os.path.join(os.getcwd(), 'new_dir')
print('new_dir: ', NEW_PATH)
os.chdir(NEW_PATH)
print('current directory: ', os.getcwd())

# создаем папку в новом текущем каталоге new_dir
# это папка my_dir
# но сначала проверяем, вдруг эта папка уже существует
if not os.path.exists(os.path.join(NEW_PATH, 'my_dir')):
    os.mkdir("my_dir")
    print('The dir "my_dir" was created!')

# удаление папки
# но сначала проверяем, существует ли эта папка
if os.path.exists(os.path.join(NEW_PATH, 'my_dir')):
    os.rmdir("my_dir")
    print('The dir "my_dir" was removed!')


# добавление файла
# но сначала проверяем, существует ли этот файл
# ВАЖНО! для этой операции необходимы права root
if not os.path.exists(os.path.join(NEW_PATH, 'test.txt')):
    if platform.system().lower() == 'linux':
        os.mknod("test.txt")
    else:
        open("test.txt", 'w').close()
    print('The file "test.txt" was created!')

# удаление файла
# если файл существует, мы его удаляем
if os.path.exists(os.path.join(NEW_PATH, 'test.txt')):
    os.remove("test.txt")
    print('The file "test.txt" was removed!')
