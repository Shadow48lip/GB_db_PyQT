"""
Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться доступность сетевых узлов.
Аргументом функции является список, в котором каждый сетевой узел должен быть представлен именем хоста или ip-адресом.
В функции необходимо перебирать ip-адреса и проверять их доступность с выводом соответствующего сообщения
(«Узел доступен», «Узел недоступен»). При этом ip-адрес сетевого узла должен создаваться с помощью функции ip_address().
(Внимание! Аргументом сабпроцеса должен быть список, а не строка!!! Для уменьшения времени работы скрипта при проверке
нескольких ip-адресов, решение необходимо выполнить с помощью потоков)
"""

import platform
from socket import gethostbyname
from subprocess import Popen, PIPE
from ipaddress import ip_address
from pprint import pprint
from threading import Thread



def ping_ip(ip, result_list):
    """
    Ping IP address and return Boolean status
    :param ip: ip address
    :param result_list: список с результатами проверки
    """

    param = '-n' if platform.system().lower() == 'windows' else '-c'
    args = ['ping', param, '2', ip]
    reply = Popen(args, stdout=PIPE, stderr=PIPE)

    code = reply.wait()
    # print(ip, code)
    result_list.append((ip, True if code == 0 else False))

    return True if code == 0 else False


def host_ping(addresses, print_result=False):
    """
    Проверяет доступность сетевых адресов по icmp
    :param addresses: список ip адресов или DNS имен хостов
    :param print_result: boolean выводить ли на экран репорт
    :return: list
    """
    if not isinstance(addresses, list):
        raise ValueError('тип аргумент должен быть list')

    # результативный список
    result_list = []
    # потоки
    threads = []

    for addr in addresses:
        try:
            ip = ip_address(addr)
        except ValueError:
            try:
                ip = ip_address(gethostbyname(addr))
            except:
                result_list.append((addr, False))
                # пропуск неправильных узлов, не отправляем их на проверку
                continue

        # запуск потоков с проверками
        thread = Thread(target=ping_ip, args=[str(ip), result_list, ])
        thread.start()
        threads.append(thread)

    if print_result:
        print('Проверка запущена...')

    # ожидаем пока все потоки закончат работу
    for thread in threads:
        thread.join()

    # вывод результатов проверки
    if print_result:
        for addr_result in result_list:
            status_report = 'доступен' if addr_result[1] else 'недоступен'
            print(f'Узел {addr_result[0]} {status_report}')

    return result_list


if __name__ == "__main__":
    result = host_ping(['bad_address_.gb', '8.8.8.8', 'ya.ru', '8.8.8.1'], True)
    # pprint(result)

