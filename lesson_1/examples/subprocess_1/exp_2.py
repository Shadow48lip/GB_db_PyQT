"""Дочерний процесс запуска стороннего приложения"""
import platform
from subprocess import call

# call - выполняет указанную команду.
# Ожидает завершения команды, а затем возвращает код возврата.

# запускаем приложение
# и ждем, пока оно не будет закрыто
# (а Popen не ждёт)
# проверяем код возврата

command = 'notepad.exe' if platform.system().lower() == 'windows' else 'libreoffice'
return_code = call(command)
if return_code == 0:
    print("Все хорошо!")
else:
    print("Ошибка!")
