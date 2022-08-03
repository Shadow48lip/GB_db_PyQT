"""
Python для сетевых инженеров
https://docs.python.org/3/howto/ipaddress.html#defining-networks
"""

# создание объектов IPv4Interface или IPv6Interface
from ipaddress import ip_interface, ip_network

# Функция ipaddress.ip_interface() позволяет создавать
# объект IPv4Interface или IPv6Interface соответственно
IPV4_INT = ip_interface('10.0.1.1/24')

# получение адреса, маски, сети интерфейса
print(type(IPV4_INT))
print('IPV4_INT:         ', IPV4_INT)
print('IPV4_INT.ip:      ', IPV4_INT.ip)
print('IPV4_INT.netmask: ', IPV4_INT.netmask)
print('IPV4_INT.network: ', IPV4_INT.network)

# проверка типа адреса
IP_1 = '10.0.1.1/24'  # эта запись означает: адрес хоста '10.0.1.1' в сети '10.0.1.0/24'
IP_2 = '10.0.1.0/24'  # адрес (описание) сети


def ip_network_check(ip_addr):
    """Проверка, является ли адрес адресом сети или хоста"""
    try:
        ip_network(ip_addr)
        return True
    except ValueError:
        return False


print(ip_network_check(IP_1))
print(ip_network_check(IP_2))
