"""Связь с дочерним процессом с помощью метода communicate()"""
import platform
from subprocess import Popen, PIPE
import chardet

for url in ["google.com", "a"]:
    param = "-n" if platform.system().lower() == 'windows' else "-c"
    command = ["ping", param, "2", url]
    process = Popen(command, stdout=PIPE, stderr=PIPE)

    # communicate - связь с созданным процессом
    # None – это результат stderr, а это значит, что ошибок не найдено
    stdout_data, stderr_data = process.communicate()
    print('stdout_data: ', stdout_data)
    print('stderr_data: ', stderr_data)

    result = chardet.detect(stdout_data)
    if result['encoding'] is not None:
        out = stdout_data.decode(result.get('encoding', None))
        print(out)

    print(50 * '=')
