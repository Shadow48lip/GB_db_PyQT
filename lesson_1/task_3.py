"""
Написать функцию host_range_ping_tab(), возможности которой основаны на функции из примера 2.
Но в данном случае результат должен быть итоговым по всем ip-адресам, представленным в табличном формате
(использовать модуль tabulate).
"""

from ipaddress import IPv4Address
from task_1 import host_ping
from time import perf_counter
from tabulate import tabulate


def host_range_ping_tab(ip_addr_start, ip_addr_range):
    try:
        ip_start_ob = IPv4Address(ip_addr_start)
    except ValueError:
        print('Вы ввели не верный формат ip адреса')
        return False

    if not isinstance(ip_addr_range, int):
        raise ValueError('Количество адресов нужно указать числом')

    max_ip_range = 255 - int(ip_addr_start.split('.')[-1])
    if ip_addr_range > max_ip_range:
        print(f'Ввели слишком большой диапазон адресов проверки. Максимум {max_ip_range}.')
        return False

    # лист ip адресов для проверки
    list_ips = [str(ip_start_ob + i) for i in range(ip_addr_range)]

    print('Проверка запущена...')

    t_s = perf_counter()
    result_list = host_ping(list_ips)
    t_work = perf_counter() - t_s
    print(f"Проверка заняла {t_work:0.4f} секунд")
    print()

    list_ok = []
    list_err = []

    for addr in result_list:
        if addr[1]:
            list_ok.append(addr[0])
        else:
            list_err.append(addr[0])

    tabulate_dict = {'Reachable': list_ok, 'Unreachable': list_err}
    print(tabulate(tabulate_dict, headers='keys', tablefmt='pipe'))


if __name__ == "__main__":
    ip_start = input('Введите первоначальный IPv4 адрес: ')
    ip_range = int(input('Сколько адресов проверить? '))

    host_range_ping_tab(ip_start, ip_range)