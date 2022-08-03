"""Функции модуля os"""

import os

# Функция basename вернет название файла пути
# Это очень полезная функция, особенно в тех случаях,
# когда нужно использовать имя файла для наименования того
# или иного связанного с работой файла, например лог-файл.
# ТакAая ситуация возникает часто при работе с файлами данных.

FILE_PATH = os.path.join(os.path.dirname(os.path.realpath('__file__')), 'ex_3.py')
print('FILE_PATH = ', FILE_PATH)
# FILE_PATH = '/home/su/Projects/GeekBrains/data-base-and-PyQt/lesson_1/examples/os_3/ex_4.py'
basename_for_FILE_PATH = os.path.basename(FILE_PATH)
print('basename_for_FILE_PATH =', basename_for_FILE_PATH)

# Функция dirname возвращает только часть каталога пути.
# В данном примере мы просто возвращаем путь к каталогу.
# Это также полезно, когда вам нужно сохранить другие файлы рядом с тем,
# который вы обрабатываете в данный момент. Как и в случае с лог-файлом, упомянутым выше.

dirname_for_FILE_PATH = os.path.dirname(os.path.abspath('__file__'))
# "/home/su/Projects/GeekBrains/data-base-and-PyQt/lesson_1/examples/os_3/ex_4.py")
print('dirname_for_FILE_PATH = ', dirname_for_FILE_PATH)

# Функция exists говорит нам, существует ли файл, или нет.
print('is exists FILE_PATH: ', os.path.exists(FILE_PATH))

# Функция isfile говорит нам, является ли объект файлом
print('isfile FILE_PATH: ', os.path.isfile(FILE_PATH))

# Функция isdir говорит нам, является ли объект файлом
print('isdir FILE_PATH: ', os.path.isdir(FILE_PATH))

# Метод join позволяет вам совместить несколько путей при помощи присвоенного разделителя.
# К примеру, в Windows, в роли разделителя выступает бэкслэш (косая черта, указывающая назад),
# однако в Linux функция разделителя присвоена косой черте, указывающей вперед (forward slash).
print('method join: ', os.path.join(os.path.dirname(os.path.realpath('__file__')), "ex_3.py"))

# Метод split разъединяет путь на tuple, который содержит и файл, и каталог.
print('method split: ', os.path.split(
    "/home/su/Projects/GeekBrains/data-base-and-PyQt/lesson_1/examples/os_3/ex_3.py"))

# Метод listdir выдаёт список файлов и папок ('.' - означает текущую директорию)
DIR_STRUCT = os.listdir('.')
print('current dir: ', os.getcwd())
print(DIR_STRUCT)
