"""
Запуск скрипта-дочернего процесса
1. Создаём процесс в модуле test_ex.py
2. Запускаем этот процесс (т.е. запускаем другой модуль!) как подпроцесс текущего модуля
"""

import platform
from subprocess import Popen, PIPE

process = Popen('python test_ex.py', shell=True, stdout=PIPE, stderr=PIPE)

# получить tuple('stdout', 'stderr')
result = process.communicate()
print(process.returncode)
if process.returncode == 0:
    print(result)
print('result:', result[0])
