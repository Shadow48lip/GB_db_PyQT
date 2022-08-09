""" Тестирование серверного модуля """
import sys
import os
import unittest

# для корректных импортов
sys.path.append(os.path.join(os.getcwd(), '..'))

from common.variables import *
from server import process_client_message


class TestServerClass(unittest.TestCase):
    """ Тестирование функции process_client_message() """

    def test_is_dict(self):
        """Возвращает всегда dict"""
        self.assertIsInstance(process_client_message({}), dict)
        self.assertIsInstance(process_client_message(' '), dict)

    def test_required_fields(self):
        """Тест на отсутствие необходимых параметров """
        test = process_client_message({ACTION: PRESENCE})
        self.assertEqual(test, {RESPONSE: 400, ERROR: 'Bad request'})
        test = process_client_message({TIME: 11223})
        self.assertEqual(test, {RESPONSE: 400, ERROR: 'Bad request'})

    def test_account_name(self):
        """Проверка недопустимого имени пользователя"""
        test = process_client_message({ACTION: PRESENCE, TIME: 1234,
                                       USER:{ACCOUNT_NAME: 'Stuff'}
                                       })
        self.assertEqual(test[RESPONSE], 401)

        test = process_client_message({ACTION: PRESENCE, TIME: 1234,
                                       USER: {ACCOUNT_NAME: 'Guest'}
                                       })
        self.assertEqual(test[RESPONSE], 200)

    def test_unknown_action(self):
        """Проверка на неизвестный экшен"""
        test = process_client_message({ACTION: 'unknown', TIME: 4432.33})
        self.assertEqual(test[RESPONSE], 400)

# Запустить тестирование
if __name__ == '__main__':
    unittest.main()