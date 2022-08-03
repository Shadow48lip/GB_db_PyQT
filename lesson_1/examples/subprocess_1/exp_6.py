"""Пинг ресурса"""

import locale
import platform
from subprocess import Popen, PIPE

ENCODING = locale.getpreferredencoding()


def ping_ip(ip_address):
    """
    Ping IP address and return tuple:
    On success:
        * True
        * command output (stdout)
    On failure:
        * False
        * error output (stderr)
    """
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    args = ['ping', param, '5', ip_address]
    reply = Popen(args, stdout=PIPE, stderr=PIPE)

    print(reply)
    code = reply.wait()
    if code == 0:
        return True, reply.stdout.read().decode(ENCODING)
    else:
        return False, reply.stderr.read().decode(ENCODING)


print(ping_ip('yandex.ru'))
print(ping_ip('a'))
