"""Python для сетевых инженеров"""

# операции с объектом-сетью
from ipaddress import ip_network
from pprint import pprint

# Функция ipaddress.ip_network() позволяет создать объект,
# который описывает сеть (IPv4 или IPv6)

# атрибут получения широковещательного адреса для сети - broadcast_address
# пакет посланный по этому адресу получат все машины в этой сети
# https://ru.wikipedia.org/wiki/Широковещательный_адрес
# https://ru.wikipedia.org/wiki/Бесклассовая_адресация

SUBNET = ip_network('80.0.1.0/28')
BA = SUBNET.broadcast_address
print('широковещательный адрес данной сети', BA)

# просмотр всех хостов для объекта-сети - метод hosts()
pprint(list(SUBNET.hosts()))

# разбиение сети на подсети (по умолчанию на 2) - метод subnets()
print(list(SUBNET.subnets()))

# обращение к любому адресу в сети
# объект-сеть в Python представляется в виде списка ip-адресов, к каждому из которых
# можно обратиться по индексу
print(SUBNET[1])
print('============ Получаем подсети ===============')
subs = list(SUBNET.subnets())
print('------ и список адресов каждой подсети ------')
print('-- подсеть subs[0] = ', subs[0])
pprint(list(subs[0].hosts()))
print('-- подсеть subs[1] = ', subs[1])
pprint(list(subs[1].hosts()))
