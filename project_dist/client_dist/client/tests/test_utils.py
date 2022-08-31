""" Тестирование клиентского модуля """
import json
import sys
import os
import unittest

# для корректных импортов
sys.path.append(os.path.join(os.getcwd(), '..'))

from common.variables import *
from common.utils import *


class TestSocket:
    """ Тестовый сокет для методов send, recv. При создании экземпляра требуется словарь с данными. """

    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_msg = None
        self.received_msg = None

    def send(self, msg):
        """ Эмуляция отправки сообщения с сохранением данных в атрибутах объекта """
        json_test_msg = json.dumps(self.test_dict)
        self.encoded_msg = json_test_msg.encode(ENCODING)
        self.received_msg = msg

    def recv(self, max_len):
        """ Эмуляция получения данных из сокета """
        json_test_msg = json.dumps(self.test_dict)
        return json_test_msg.encode(ENCODING)


class TestClientClass(unittest.TestCase):
    """ Тестирование функций утилит """

    test_dict_send = {ACTION: PRESENCE, TIME: 122.33, USER: {ACCOUNT_NAME: 'Stuff'}}
    test_dict_recv_ok = {RESPONSE: 200}
    test_dict_recv_error = {RESPONSE: 400, ERROR: 'Bad Request'}

    def test_send_message_ok(self):
        """ Проверка корректной отправки в сокет через send_message() """
        # тестовый сокет, экземпляр класса со словарем (данными)
        test_socket = TestSocket(self.test_dict_send)
        # вызов функции, результаты будут сохранены в объекте сокета
        send_message(test_socket, self.test_dict_send)
        # сравниваем строки закодированные send_message() и закодированные эталонно в сокете
        self.assertEqual(test_socket.received_msg, test_socket.encoded_msg)

    def test_send_message_exception(self):
        """ Проверка отправки в сокет через send_message() произвольной строки """
        # тестовый сокет, экземпляр класса со словарем (данными)
        test_socket = TestSocket(self.test_dict_send)
        # сравниваем строки закодированные send_message() и закодированные эталонно в сокете
        self.assertRaises(TypeError, send_message, test_socket, 'string string')

    def test_get_message_ok(self):
        """ Проверка корректного ответа функции get_message() """
        test_socket = TestSocket(self.test_dict_recv_ok)
        # функция должна вернуть такой же словарь, который отправили
        self.assertEqual(get_message(test_socket), self.test_dict_recv_ok)

    def test_get_message_error(self):
        """ Проверка корректного ответа функции get_message() """
        test_socket = TestSocket(self.test_dict_recv_error)
        # функция должна вернуть такой же словарь, который отправили
        self.assertEqual(get_message(test_socket), self.test_dict_recv_error)


# Запустить тестирование
if __name__ == '__main__':
    unittest.main()
