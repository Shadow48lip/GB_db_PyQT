"""Получение кода завершения подпроцесса"""

import platform
from subprocess import Popen

program = 'notepad.exe' if platform.system().lower() == 'windows' else 'libreoffice'
process = Popen(program)
