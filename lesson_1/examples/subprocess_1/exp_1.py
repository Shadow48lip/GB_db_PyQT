"""Дочерний процесс запуска консольной команды"""
import platform
from subprocess import call, Popen, PIPE
import chardet

# Класс subprocess.Popen() - Выполняет программу в новом процессе
# Popen не дожидается конца выполнения вызванного процесса
# (он завершается, а запущенное приложение 'висит')

# stdin и stdout это файлоподобные объекты, предоставляемые OS.
# stdout=PIPE - стандартный поток вывода
# вывод результатов выполнения команды с декодированием

# shell=True - выполнение кода через оболочку

command = 'dir' if platform.system().lower() == 'windows' else 'ls'

# мы не знаем в чем нужно декодировать
# но нам помогает модуль chardet
process = Popen(command, shell=True, stdout=PIPE)
data = process.stdout.read()
result = chardet.detect(data)
print(result)
out = data.decode(result['encoding'])
print(out)

# Popen поддерживает менеджеры контекста
with Popen(command, shell=True, stdout=PIPE) as p:
    out = p.stdout.read().decode(result['encoding'])
    print(out)
