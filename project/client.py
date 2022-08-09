""" Клиент JIM (JSON instant messaging """

import json
import time
import argparse
import threading
from socket import socket, AF_INET, SOCK_STREAM
from common.utils import get_message, send_message
from common.variables import DEFAULT_PORT, DEFAULT_IP_ADDRESS, ACTION, USER, ACCOUNT_NAME, \
    TIME, RESPONSE, ERROR, PRESENCE, MESSAGE, MESSAGE_TEXT, SENDER, DESTINATION, EXIT
from common.decorators import log
import logging
import logs.client_log_config
from common.metaclasses import ClientMaker

LOG = logging.getLogger('app.client')


# Класс формировки и отправки сообщений на сервер и взаимодействия с пользователем.
class ClientSender(threading.Thread, metaclass=ClientMaker):
    def __init__(self, account_name, sock):
        self.account_name = account_name
        self.sock = sock
        super().__init__()


    # Функция создаёт словарь с сообщением о выходе.
    def create_exit_message(self):
        message_dict = {
            ACTION: EXIT,
            TIME: time.time(),
            ACCOUNT_NAME: self.account_name
        }

        try:
            send_message(self.sock, message_dict)
            LOG.info(f'Завершение работы по команде пользователя.')
            # Задержка необходима, чтобы успело уйти сообщение о выходе
            time.sleep(0.5)
            exit(1)
        except (ConnectionResetError, ConnectionError, ConnectionAbortedError) as e:
            print(e)
            LOG.critical('Потеряно соединение с сервером.')
            exit(1)

    # Функция запрашивает текст сообщения или команду завершения. Отправляет сформированный словарь
    def create_message(self):
        while True:
            to_user = input('Введите получателя сообщения: ')
            if to_user:
                break

        while True:
            message = input('Введите сообщение для отправки: ')
            if message:
                break

        message_dict = {
            ACTION: MESSAGE,
            SENDER: self.account_name,
            DESTINATION: to_user,
            TIME: time.time(),
            MESSAGE_TEXT: message
        }

        if __debug__:
            LOG.debug(f'Сформирован словарь сообщения: {message_dict}')

        try:
            send_message(self.sock, message_dict)
            LOG.info(f'Отправлено сообщение для пользователя {to_user}')
            print('Сообщение отправлено.')
        except (ConnectionResetError, ConnectionError, ConnectionAbortedError) as e:
            print(e)
            LOG.critical('Потеряно соединение с сервером.')
            exit(1)

    # Вывод поддерживаемых команд
    def print_help(self):
        help_message = """Поддерживаемые команды:
        message - отправить сообщение. Кому и текст будет запрошены отдельно.
        help - вывести подсказки по командам
        exit - выход из программы
        """
        print(help_message)

    # Функция взаимодействия с пользователем, запрашивает команды, отправляет сообщения
    def run(self):
        self.print_help()
        while True:
            command = input('Введите команду: ')
            if command == 'message':
                self.create_message()
                # print(help_message)
            elif command == 'help':
                self.print_help()
            elif command == 'exit':
                self.create_exit_message()
                break
            else:
                print('Команда не распознана, попробуйте снова. help - вывести поддерживаемые команды.')


# Класс-приёмник сообщений с сервера. Принимает сообщения, выводит в консоль.
class ClientReader(threading.Thread, metaclass=ClientMaker):
    def __init__(self, account_name, sock):
        self.account_name = account_name
        self.sock = sock
        super().__init__()

    # Основной цикл приёмника сообщений, принимает сообщения, выводит в консоль. Завершается при потере соединения.
    def run(self):
        while True:
            try:
                message = get_message(self.sock)
                if ACTION in message and message[ACTION] == MESSAGE and SENDER in message and DESTINATION in message \
                        and MESSAGE_TEXT in message and message[DESTINATION] == self.account_name:
                    print(f'\nПолучено сообщение от пользователя {message[SENDER]}:'
                          f'\n{message[MESSAGE_TEXT]}')
                    LOG.info(f'Получено сообщение от пользователя {message[SENDER]}: {message[MESSAGE_TEXT]}')
                else:
                    LOG.error(f'Получено некорректное сообщение с сервера: {message}')
            except TypeError:
                # пришло пустое сообщение
                pass
            except ValueError as e:
                LOG.error(f'Не удалось декодировать полученное сообщение. {e}')
            except (OSError, ConnectionError, ConnectionAbortedError, ConnectionResetError, json.JSONDecodeError):
                LOG.critical(f'Потеряно соединение с сервером.')
                break


# Проверка ответа сервера. Обязательно должен быть код ответа в response
@log
def process_ans(message):
    """
    :param message:
    :return:
    """
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            if __debug__:
                LOG.debug(f'Успешный ответ от сервера с кодом {message[RESPONSE]}')
            return '200 : OK'

        LOG.error(f'Ошибочный ответ сервера: код {message[RESPONSE]} - {message[ERROR]}')
        return f'Error code {message[RESPONSE]} : {message[ERROR]}'

    LOG.error(f'Не верный ответ сервера! Не подошел ни один формат ответа. {message}')
    raise ValueError(f'В принятом словаре отсутствуют обязательные поля')


# Присутствие. Сервисное сообщение для извещения сервера о присутствии клиента online и регистрации;
@log
def create_presence(sock, account_name='Guest'):
    """
    Создает словарь с сообщением к серверу о присутствии клиента онлайн и отправляет его.
    :param sock:
    :param account_name:
    :return:
    """

    message_dict = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }

    if __debug__:
        LOG.debug(f'Создан запрос присутствия для клиента {account_name}')

    try:
        send_message(sock, message_dict)
        LOG.info(f'Отправлен запрос присутствия {account_name}')
    except (ConnectionResetError, ConnectionError, ConnectionAbortedError) as e:
        print(e)
        LOG.critical('Потеряно соединение с сервером.')
        exit(1)


# Разбор параметров командной строки.
@log
def arg_parser():
    """
    client.py 127.0.0.1 8888 -m send
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?',
                        help=f'Server address. Default {DEFAULT_IP_ADDRESS}')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?',
                        help=f'Server port 1024-65535. Default {DEFAULT_PORT}')
    parser.add_argument('-n', '--name', default='', nargs='?', help='имя пользователя в чате')
    args = parser.parse_args()

    if args.port < 1024 or args.port > 65536:
        LOG.warning('Номер порта должен быть указан в пределах 1024 - 65635')
        exit(1)

    return args.addr, args.port, args.name


def main():
    # Получаем параметры из командной строки
    server_address, server_port, client_name = arg_parser()

    while True:
        if not client_name:
            client_name = input('Имя пользователя в чате: ')
        else:
            break

    LOG.info(f'Клиент чата запущен со следующими параметрами:'
             f' {server_address}:{server_port}, Пользователь: {client_name}')

    # создаем socket
    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((server_address, server_port))
    except (ConnectionRefusedError, ConnectionError):
        LOG.critical(
            f'Не удалось подключиться к серверу {server_address}:{server_port}, '
            f'конечный компьютер отверг запрос на подключение.')
        exit(1)

    # отправка приветствия и получение ответа
    create_presence(s, client_name)

    try:
        msg_in = get_message(s)
        print(f'Установлено соединение с сервером. Ответ {process_ans(msg_in)}. Пользователь: {client_name}')
    except TypeError as e:
        LOG.critical(e)
        s.close()
        exit(1)
    except(ValueError, json.JSONDecodeError) as e:
        LOG.error(e)
        s.close()
        exit(1)

    # Соединение полностью установлено. Запускаем потоки на чтение и отправку.

    # чтение
    module_receiver = ClientReader(client_name, s)
    module_receiver.daemon = True
    module_receiver.start()

    # отправка с интерактивом
    module_sender = ClientSender(client_name, s)
    module_sender.daemon = True
    module_sender.start()

    if __debug__:
        LOG.debug('Потоки запущены')

    # Watchdog основной цикл, если один из потоков завершён в результате ошибок соединения или выхода пользователя
    # Поскольку все события обрабатываются в зомби в потоках, достаточно просто завершить цикл.
    while True:
        time.sleep(0.5)
        if module_receiver.is_alive() and module_sender.is_alive():
            continue
        break


if __name__ == '__main__':
    main()
