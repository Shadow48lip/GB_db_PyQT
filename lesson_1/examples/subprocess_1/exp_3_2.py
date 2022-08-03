"""
Получение кода завершения подпроцесса
Вариант 2: благодаря методу .wait() Popen ведёт себя подобно Call
(программа ждёт завершения процесса)
"""

import platform
from subprocess import Popen

'''
Здесь мы создали переменную под названием program и назначили ей значение notepad.exe. 
После этого мы передали её классу Popen. После запуска этого кода, вы увидите, 
что он мгновенно вернет объект subprocess.Popen. 
А после закрытия приложения - возвращается код возврата. 
'''

command = 'notepad.exe' if platform.system().lower() == 'windows' else 'libreoffice'


# и это = ждать закрытия приложения
process = Popen(command)
code = process.wait()

print(process)
print(code)
