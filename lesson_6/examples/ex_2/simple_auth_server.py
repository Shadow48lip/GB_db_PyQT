"""
# ========================= Аспекты безопасности ==============================

# ------------- Простая аутентификация клиента. Реализация сервера -------------

HMAC - Keyed-Hashing for Message Authentication.
Модуль hmac служит для вычисления хэш-функции с ключом от сообщения.
Такой подход используется для аутентификации сообщений.
Подробное описание алгоритма содержится в RFC 2104 (https://tools.ietf.org/html/rfc2104.html).

Возможности данного модуля могут применены для аутентификации клиента.

                           Общая схема работы
                СЕКРЕТ известен только клиенту и серверу (ключ)
----------------------                           ----------------------------
|       Клиент        |                         |           Сервер           |
|-------------------- |  запрос_аутентификации  |----------------------------|
|                     | ----------------------> |      Генерация rnd_msg     |
|                     |         rnd_msg         |                            |
|                     | <---------------------  |                            |
|     Вычисление      |                         |         Вычисление         |
|HMAC(СЕКРЕТ, rnd_msg)|                         |    HMAC(СЕКРЕТ, rnd_msg)   |
|                     |                         |                            |
|                     |       HMAC_клиент       |                            |
|                     | ----------------------> |         Сравнение          |
|                     |                         | HMAC_клиент == HMAC_сервер |
|                     |                         |            |  |            |
|                     |       свой (доверие) <--------------да   нет         |
|                     | <====================== |                 |--> чужой |
-----------------------                          ----------------------------


hmac.new(key, msg=None, digestmod=None)
key - byte-строка, представляющая ключ
msg - сообщение, для которого нужно вычислить хэш
digestmod - имя хэш-функции, которая будет применена для вычисления (sha-1, sha-256, ...)
"""

import hashlib
import os
import hmac
from socket import socket, AF_INET, SOCK_STREAM

SECRET_KEY = b'our_secret_key'


# ------------------- Функция аутентификации клиента на сервере -------------------- #
def server_authenticate(connection, secret_key):
    """
    Запрос аутентификаии клиента.
    connection - сетевое соединение (сокет);
    secret_key - ключ шифрования, известный клиенту и серверу
    """

    # 1. Создаётся случайное послание и отсылается клиенту
    # urandom(n) - генерирует зависимые от операционной системы случайные байты,
    # которые спокойно можно назвать криптографически надежными
    message = os.urandom(32)
    # message - b'\xea(\xf0i\xd1\x1fB\xba.\xea\xef?\x91l\xf2\x89\x91\xcd\xb1\xd6\x9b1x\xd6\x01\xa9}"@\xfdt\x8f'
    # type(message)- <class 'bytes'>
    connection.send(message)

    # 2. Вычисляется HMAC-функция (локальный результат) от послания с использованием секретного ключа
    # secret_key - b'our_secret_key'
    hash = hmac.new(secret_key, message, hashlib.sha256)
    # hash - <hmac.HMAC object at 0x00000055E6EAF518>
    # type(hash) - <class 'hmac.HMAC'>
    digest = hash.digest()
    # digest - b'\xf8\xbc5h\\\xf3\x10\xfc\x1c\xc1\x905\x95#.\xa3'

    # 3. Пришедший ответ от клиента сравнивается с локальным результатом HMAC
    response = connection.recv(len(digest))
    # response - b'\x10]\x82\xc7\xf8\xc7m)\x7fF\xd11\x1f\x8d\xf7\xb6'
    return hmac.compare_digest(digest, response)


# Выдержка из официальной документации, которая советует для сравнения хэш-сумм
# использовать крипто-безопасную функцию hmac.compare_digest, а не оператор ==
# ---------------------------------------------------------------------
# Warning:
# When comparing the output of digest() to an externally-supplied digest
# during a verification routine, it is recommended to use 
# the compare_digest() function instead of the == operator 
# to reduce the vulnerability to timing attacks. 
# ---------------------------------------------------------------------


# ---------------------------- Эхо-сервер ----------------------------- #


def echo_handler(client_sock):
    """
    Эхо-обработка.
    Проводит аутентификацию клиента и отсылает его же запрос обратно (эхо).
    """

    if not server_authenticate(client_sock, SECRET_KEY):
        client_sock.close()
        return
    while True:
        msg = client_sock.recv(4096)
        print(msg)
        if not msg:
            break
        client_sock.send(msg)


def echo_server(address):
    """
    Эхо-сервер.
    "Слушает" указанный адрес и общается с клиентом через echo_handler.
    """

    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    sock.listen(5)
    while True:
        conn, addr = sock.accept()
        echo_handler(conn)


echo_server(('', 9999))
