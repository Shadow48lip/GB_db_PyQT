"""Функции модуля os"""

import os
import platform

# когда нужно переименовать файл или папку
os.rename("new_dir", "old_dir")
os.rename("old_dir", "new_dir")

# Метод os.startfile() позволяет нам «запустить»
# файл в привязанной к нему программе.

if platform.system().lower() == 'windows':
    os.startfile("Сложность алгоритмов.png")
else:
    file_path = os.path.join(os.getcwd(), 'Сложность алгоритмов.png')
    os.system(f"eog '{file_path}'")

PATH = "dirs"

"""
\dirs
\dirs\d1\f1.txt
\dirs\d2\f2.txt
\dirs\d3\f3.txt
"""

# root - очередной внутренний путь к папке, включая текущую
# dirs - список папок в каждом пути root
# files - список файлов в каждом пути root
for root, dirs, files in os.walk(PATH):
    print('-' * 50)
    print(root)
    print(dirs)
    print(files)

print()
print('=' * 50)
for root, dirs, files in os.walk(PATH):
    print(root, dirs, files)
