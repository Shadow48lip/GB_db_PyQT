# ========================= Аспекты безопасности ==============================
# ------------- Модуль PyCrypto для криптографических функций в Python --------

# ------------------------- Шифрование сообщений ------------------------------


# Библиотека PyCrypto реализует криптографические примитивы и функции на Python.
# Однако данная библиотека не обновляется с 2014 года. 
# PyCryptodome (PyCryptoDomeEx) - это fork библиотеки PyCrypto, развивается.
# Код проекта: https://github.com/Legrandin/pycryptodome

# УСТАНОВКА ПАКЕТА:  pip install pycryptodomex

# PyCryptodome совместима по API с PyCrypto, 
# PyCryptoDomeEx - дополняет/изменяет исходный API.


import os
from binascii import hexlify
from Cryptodome.Cipher import AES

# Для шифрования данных в PyCryptodome есть поддержка нескольких алгоритмов:
#  - блочные шифры: AES, DES, 3DES, Blowfish
#  - поточные шифры: Salsa20, ChaCha20


def padding_text(text: bytes):
    """
    Выравнивание сообщения до длины кратной 16 байтам.
    В данном случае исходное сообщение дополняется пробелами.
    """

    pad_len = 16 - len(text) % 16
    return text + b' ' * pad_len


def _encrypt(plaintext: bytes, key: bytes):
    """
    Шифрование сообщения plaintext ключом key.

    Атрибут iv - вектор инициализации для алгоритма шифрования.
    Если не задаётся явно при создании объекта-шифра, то генерируется случайно.
    Его следует добавить в качестве префикса к финальному шифру,
    чтобы была возможность правильно расшифровать сообщение.
    """
    # Создать новый шифр AES
    # new() функция на уровне модуля под Crypto.Cipher инициализирует новый
    # объект CBC шифра для соответствующего базового алгоритма.

    cipher = AES.new(key, AES.MODE_CBC)
    # cipher - <Cryptodome.Cipher._mode_cbc.CbcMode object at 0x000000EFCDC8FE10>

    ciphered_text = cipher.iv + cipher.encrypt(plaintext)
    # ciphertext - b'\xd2o\xba!\xa6\xd3i\xd2\x8a\x94m,\xcb\xaa\x14\x0c]\xa5\x88\xdd,
    # \x9by\xf6*l\xb3-\x93\xbb\xf8\x99ciYY\xa0\x07N\xcd\xd3GI\n%\xae0\xa5'
    return ciphered_text


def _decrypt(ciphered_text, key):
    """
    Расшифровка шифра ciphertext ключом key

    Вектор инициализации берётся из исходного шифра.
    Его длина для большинства режимов шифрования всегда 16 байт.
    Расшифровываться будет оставшаяся часть шифра.
    """
    # ciphered_text - b'\xba\x0b\x0c\xad\x1f\x99\x12\'\xf11\xe3\x80\xfdl\xb9_\x01+\x9d\xd5\xc4\x00\x03J\xbb|
    # \x7f\x1d\x8bVz\xfeX\n\x8e\xb1"\xa2\x81$\x9a\x07\x11\xc9\xb6\xa30\xf6'

    # :16 - вектор инициализации
    cipher = AES.new(key, AES.MODE_CBC, iv=ciphered_text[:16])
    # cipher - <Cryptodome.Cipher._mode_cbc.CbcMode object at 0x000000036E6BB2B0>
    # 16: - само сообщение
    msg = cipher.decrypt(ciphered_text[16:])
    # msg - b'The rain in Spain               '

    # убираем пробелы, добавленные ранее для соблюдения условия кратности 16-ти
    msg = msg.decode().strip().encode()
    # msg - b'The rain in Spain'
    return msg


if __name__ == '__main__':
    # Осуществим шифрование сообщения алгоритмом AES
    # шифруемое сообщение
    plaintext = b'The rain in Spain'

    # key (строка байтов) - секретный ключ для симметричного шифрования.
    # Ключ должен быть длиной 16 (AES-128), 24 (AES-192) или 32 (AES-256) байта.
    key = b'Super Secret Key'
    print('len(key) =', len(key))

    # Длина сообщения должна быть кратна 16, поэтому выполним выравнивание.
    plaintext = padding_text(plaintext)

    # Выполним шифрование
    ciphered_text = _encrypt(plaintext, key)
    print('encrypted message: ', ciphered_text)

    # Выполним дешифрование
    msg = _decrypt(ciphered_text, key)
    print('decrypted message: ', msg)
