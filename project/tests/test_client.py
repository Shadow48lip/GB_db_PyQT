""" Тестирование клиентского модуля """
import sys
import os
import unittest

# для корректных импортов
sys.path.append(os.path.join(os.getcwd(), '..'))

from common.variables import *
from client import create_presence, process_ans


class TestClientClass(unittest.TestCase):
    """ Тестирование функции create_presence() """

    def test_create_presence_dic(self):
        """ Ответ должен быть всегда словарем """
        self.assertIsInstance(create_presence(), dict)

    def test_create_presence_answer(self):
        """ Корректность ответа """
        test = create_presence('Alex')
        test[TIME] = 8432
        # print(test)
        self.assertEqual(test, {'action': 'presence', 'time': 8432, 'user': {'account_name': 'Alex'}})

    """ Тестирование функции process_ans() """

    def test_process_ans_ok(self):
        """ Корректный ответ на 200 код"""
        self.assertIn('200', process_ans({RESPONSE: 200}))

    def test_process_ans_error_code(self):
        """ Ответ при получении ошибки с сервера """
        self.assertEqual(process_ans({RESPONSE: 401,ERROR: 'Not auth'}), 'Error code 401 : Not auth')

    def test_test_process_ans_exception(self):
        """ Проверка выпадения ошибки на отсутствие обязательного поля """
        self.assertRaises(ValueError, process_ans, 'value')


# Запустить тестирование
if __name__ == '__main__':
    unittest.main()
