# ========================= Аспекты безопасности ==============================

# ------------- Простая аутентификация клиента. Реализация клиента -------------
import hashlib
import os
import hmac
from socket import socket, AF_INET, SOCK_STREAM

SECRET_KEY = b'our_secret_key'


def client_authenticate(connection, secret_key):
    """
    Аутентификация клиента на удалённом сервисе.
    Параметр connection - сетевое соединение (сокет)
    secret_key - ключ шифрования, известный клиенту и серверу
    """

    # принимаем случайное послание от сервера
    message = connection.recv(4096)
    print('message: ', message)

    # вычисляем HMAC-функцию
    # <hmac.HMAC object at 0x000000BACEF3D278>
    # b'?\xa0\x85\x94`\xb9[\xe8\x865\x97\xb6\x06\x1e\xefj'
    hash = hmac.new(secret_key, message, hashlib.sha256)
    print('hash:   ', hash)
    digest = hash.digest()
    print('digest: ', digest)

    # отправляем ответ серверу
    connection.send(digest)


# ------------------------------ Клиент ----------------------------- #

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('localhost', 9999))

# проходим аутентификацию
client_authenticate(sock, SECRET_KEY)

sock.send(b'Hello, my secure server_dist!')
resp = sock.recv(4096)

print(f'Сервер ответил: {resp.decode()}')
