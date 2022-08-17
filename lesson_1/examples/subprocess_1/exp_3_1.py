"""
Получение кода завершения подпроцесса
Вариант 1: процесс запускается и программа выполняется дальше
"""

import platform
from subprocess import Popen

'''
Здесь мы создали переменную под названием program и назначили ей значение notepad.exe. 
После этого мы передали её классу Popen. После запуска этого кода, вы увидите, 
что он мгновенно вернет объект subprocess.Popen, а вызванное приложение будет выполняться. 
'''

# сравните = не ждать закрытия приложения
command = 'notepad.exe' if platform.system().lower() == 'windows' else 'libreoffice'
process = Popen(command)

print(process)

