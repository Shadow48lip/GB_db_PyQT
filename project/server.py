""" Сервер JIM (JSON instant messaging """
# текущая версия сервера принимает сообщения от одних клиентов и тут же рассылает их всем, кто читает

import argparse
import configparser  # https://docs.python.org/3/library/configparser.html
import os
import sys
import time
import threading
from select import select
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from common.variables import *
from common.utils import get_message, send_message
from common.decorators import log
import logging
import logs.server_log_config
from common.descriptors import Port
from common.metaclasses import ServerMaker
from db.server_db import ServerDB
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QTimer
from server_gui import MainWindow, gui_create_model, HistoryWindow, create_stat_model, ConfigWindow

LOG = logging.getLogger('app.server')

# Флаг, что был подключён новый пользователь, нужен чтобы не мучать BD
# постоянными запросами на обновление
new_connection = False
conflag_lock = threading.Lock()


@log
def arg_parser(default_port, default_address):
    """
    Разбор параметров командной строки.
    server.py -p 8888 -a 127.0.0.1
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', default=default_address, nargs='?',
                        help=f'Server address. Default - all net interfaces')
    parser.add_argument('-p', default=default_port, type=int, nargs='?',
                        help=f'Server port 1024-65535. Default {default_port}')
    args = parser.parse_args()

    # перенесено в дескрипторы
    # if not 1023 < args.p < 65536:
    #     LOG.warning('Номер порта должен быть указан в пределах 1024 - 65635')
    #     exit(1)

    return args.a, args.p


# Основной класс сервера
class Server(threading.Thread, metaclass=ServerMaker):
    # отправляем порт на проверку в дескриптор common.descriptors
    port = Port()

    def __init__(self, listen_address, listen_port, database):
        # Параметры подключения
        self.addr = listen_address
        self.port = listen_port

        # База данных сервера
        self.database = database

        # Будущий объект сокета в init_socket()
        self.sock = None

        # Сокеты подключённых клиентов.
        self.all_clients = []

        # Список сообщений на отправку.
        self.messages = []

        # Словарь содержащий сопоставленные имена и соответствующие им сокеты.
        self.names = {}

        # Конструктор предка для работы методов Тредов
        super().__init__()

    def init_socket(self):
        """ Подготовка сокета """
        s = socket(AF_INET, SOCK_STREAM)
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # Несколько приложений может слушать сокет
        s.bind((self.addr, self.port))
        s.settimeout(CONNECTION_TIMEOUT)
        print(f'Server ready. Listen connect on {self.addr}:{self.port}')
        LOG.info(f'Server start. Listen connect on {self.addr}:{self.port}')

        # Начинаем слушать сокет
        self.sock = s
        self.sock.listen(MAX_CONNECTIONS)

    def run(self):
        # Инициализация Сокета
        self.init_socket()

        # listen clients connections
        while True:
            try:
                client_socket, client_address = self.sock.accept()
            except OSError as err:  # timeout
                # print(err.errno)
                pass
            else:
                LOG.info(f'Получен запрос на соединение от {str(client_address)}')
                print(f"Получен запрос на соединение от {str(client_address)}")
                self.all_clients.append(client_socket)

            wait = 0.1
            clients_read = []
            clients_write = []

            # Асинхронное ожидание клиента
            # имеет смысл проверять select, если есть клиенты в пуле
            if self.all_clients:
                try:
                    clients_read, clients_write, errors = select(self.all_clients, self.all_clients, [], wait)
                except OSError:
                    pass
                except Exception as e:
                    print('ошибка в select:', e)

            # обработка входящих сообщений и если ошибка, то отключаем и закрываем сокет
            if clients_read:
                for client_with_message in clients_read:
                    try:
                        print(f'пришло сообщение от {client_with_message.getpeername()}')
                        self.process_client_message(get_message(client_with_message), client_with_message)

                    # process_client_message пытался ответить клиенту кодом доставки, но связь разорвана
                    except (OSError, Exception):
                        print('Отправитель отключился')
                        # поиск имени клиента по сокету
                        for name in self.names:
                            if self.names[name] == client_with_message:
                                self.database.user_logout(name)
                                del self.names[name]
                                LOG.info(f'Отправитель {name} отключился от сервера.')
                                break

                        self.all_clients.remove(client_with_message)
                        client_with_message.close()

            # обработка слушающих клиентов (отправка сообщений)
            if self.messages:
                for _ in range(len(self.messages)):
                    msg = self.messages.pop()

                    try:
                        self.process_message(msg, clients_write)
                    except Exception:
                        LOG.info(f'Связь с клиентом с именем {msg[DESTINATION]} была потеряна')
                        self.all_clients.remove(self.names[msg[DESTINATION]])
                        self.database.user_logout(msg[DESTINATION])
                        self.names[msg[DESTINATION]].close()
                        del self.names[msg[DESTINATION]]

    def process_message(self, message, listen_socks):
        """
        Функция адресной отправки сообщения определённому клиенту. Принимает словарь сообщение
        и слушающие сокеты. Список зарегистрированных пользователей берет из глобального __init__.
        Ничего не возвращает.
        :param message:
        :param listen_socks:
        :return:
        """

        if message[DESTINATION] not in self.names:
            message_dict = {
                ACTION: MESSAGE,
                SENDER: 'Server',
                DESTINATION: message[SENDER],
                TIME: time.time(),
                MESSAGE_TEXT: f'Пользователь {message[DESTINATION]} не зарегистрирован.'
            }
            send_message(self.names[message[SENDER]], message_dict)
            LOG.error(
                f'Пользователь {message[DESTINATION]} не зарегистрирован online на сервере, отправка сообщения невозможна.')
            return

        if self.names[message[DESTINATION]] not in listen_socks:
            raise ConnectionError

        send_message(self.names[message[DESTINATION]], message)
        LOG.info(f'Отправлено сообщение пользователю {message[DESTINATION]} от пользователя {message[SENDER]}.')

    def process_client_message(self, message, sock):
        """
        Обрабатывает принятые сообщения от клиентов на соответствие протоколу JIM и возвращает словарь с ответом.
        messages, all_clients, names берутся из __init__
        :param message: словарь с новым сообщением
        :param sock: сокет  с новым сообщением
        :return:
        """

        global new_connection

        if __debug__:
            LOG.debug(f'Разбор входящего сообщения: {message}')

        if ACTION not in message or TIME not in message:
            if __debug__:
                LOG.warning(f'Пришли неизвестные данные - {message}. Ответ - Bad request')
            return {RESPONSE: 400, ERROR: 'Bad request'}

        # Код по молчанию
        return_code = 200

        # Присутствие клиента online;
        # регистрация пользователя, если он новый
        if message[ACTION] == PRESENCE and ACCOUNT_NAME in message[USER]:
            new_user = message[USER][ACCOUNT_NAME]

            if new_user not in self.names.keys():
                if __debug__:
                    LOG.debug(f'Зарегистрировали нового пользователя {new_user}')
                self.names[new_user] = sock

                # записываем в базу информацию о новом коннекте
                client_ip, client_port = sock.getpeername()
                self.database.user_login(new_user, client_ip, client_port)

                send_message(sock, {RESPONSE: return_code})
                with conflag_lock:
                    new_connection = True
                return True
            else:
                return_code = 400
                if __debug__:
                    LOG.debug(f'Пользователь уже добавлен. Код {return_code}')
                send_message(sock, {RESPONSE: return_code, ERROR: f'Пользователь {new_user} уже зарегистрирован.'})
                # self.all_clients.remove(sock)
                # sock.close()
                return True

        # получили сообщение, добавляем в очередь и пишем статистику в БД
        elif message[ACTION] == MESSAGE and MESSAGE_TEXT in message and DESTINATION in message and SENDER in message \
                and self.names[message[SENDER]] == sock:
            self.messages.append(message)
            self.database.process_message(message[SENDER], message[DESTINATION])
            send_message(sock, {RESPONSE: return_code})
            return True

        # клиент отключается
        elif message[ACTION] == EXIT and ACCOUNT_NAME in message and self.names[message[ACCOUNT_NAME]] == sock:
            self.database.user_logout(message[ACCOUNT_NAME])
            self.all_clients.remove(self.names[message[ACCOUNT_NAME]])
            del self.names[message[ACCOUNT_NAME]]
            LOG.info(f'Пользователь {message[ACCOUNT_NAME]} прислал команду выхода')
            sock.close()
            with conflag_lock:
                new_connection = True
            return

        # Если это запрос контакт-листа
        elif message[ACTION] == GET_CONTACTS and USER in message and \
                self.names[message[USER]] == sock:
            return_code = 202
            response = {
                RESPONSE: return_code,
                LIST_INFO: self.database.get_contacts(message[USER])
            }
            send_message(sock, response)
            return

        # Если это добавление контакта
        elif message[ACTION] == ADD_CONTACT and ACCOUNT_NAME in message and USER in message \
                and self.names[message[USER]] == sock:
            self.database.add_contact(message[USER], message[ACCOUNT_NAME])
            send_message(sock, {RESPONSE: return_code})
            return

        # Если это удаление контакта
        elif message[ACTION] == REMOVE_CONTACT and ACCOUNT_NAME in message and USER in message \
                and self.names[message[USER]] == sock:
            self.database.remove_contact(message[USER], message[ACCOUNT_NAME])
            send_message(sock, {RESPONSE: return_code})
            return

        # Если это запрос известных пользователей
        elif message[ACTION] == USERS_REQUEST and ACCOUNT_NAME in message \
                and self.names[message[ACCOUNT_NAME]] == sock:
            return_code = 202
            response = {
                RESPONSE: return_code,
                LIST_INFO: [user[0] for user in self.database.users_list()]
            }
            send_message(sock, response)
            return

        # для неизвестных экшенов
        return_code = 400
        LOG.info(f'Ответ клиенту на {PRESENCE}. Код {return_code}. Неизвестный {ACTION}')
        send_message(sock, {RESPONSE: return_code, ERROR: f'Action {message[ACTION]} not support'})
        return True


def main():
    # Загрузка файла конфигурации сервера
    config = configparser.ConfigParser()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config.read(f"{dir_path}/{'server.ini'}")

    # Загрузка параметров командной строки, если нет параметров,
    # то задаём значения по умолчанию.
    listen_address, listen_port = arg_parser(config['SETTINGS']['default_port'], config['SETTINGS']['listen_address'])

    # Инициализация базы данных
    database = ServerDB(os.path.join(config['SETTINGS']['database_path'], config['SETTINGS']['database_file']))

    # Фоновый поток - Создание экземпляра класса сервера и запускаем
    server = Server(listen_address, listen_port, database)
    server.daemon = True
    server.start()

    # поток должен успеть запустится и отчитаться о запуске
    time.sleep(0.5)

    # Основной поток с GUI.
    # Создаём графическое окружение для сервера:
    server_app = QApplication(sys.argv)
    main_window = MainWindow()

    # Инициализируем параметры окна при старте
    main_window.statusBar().showMessage('сервер запущен')
    main_window.active_clients_table.setModel(gui_create_model(database))
    main_window.active_clients_table.resizeColumnsToContents()
    main_window.active_clients_table.resizeRowsToContents()

    # Функция, обновляющая список подключённых, проверяет флаг подключения, и
    # если надо обновляет список
    def list_update():
        global new_connection
        if new_connection:
            main_window.active_clients_table.setModel(gui_create_model(database))
            main_window.active_clients_table.resizeColumnsToContents()
            main_window.active_clients_table.resizeRowsToContents()
            with conflag_lock:
                new_connection = False

    # Функция, создающая окно со статистикой клиентов
    def show_statistics():
        global stat_window
        stat_window = HistoryWindow()
        stat_window.history_table.setModel(create_stat_model(database))
        stat_window.history_table.resizeColumnsToContents()
        stat_window.history_table.resizeRowsToContents()
        stat_window.show()

    # Функция создающая окно с настройками сервера.
    def server_config():
        global config_window
        # Создаём окно и заносим в него текущие параметры
        config_window = ConfigWindow()
        config_window.db_path.insert(config['SETTINGS']['Database_path'])
        config_window.db_file.insert(config['SETTINGS']['Database_file'])
        config_window.port.insert(config['SETTINGS']['Default_port'])
        config_window.ip.insert(config['SETTINGS']['Listen_Address'])
        config_window.save_btn.clicked.connect(save_server_config)

    # Функция сохранения настроек
    def save_server_config():
        global config_window
        message = QMessageBox()
        config['SETTINGS']['database_path'] = config_window.db_path.text()
        config['SETTINGS']['database_file'] = config_window.db_file.text()
        try:
            port = int(config_window.port.text())
        except ValueError:
            message.warning(config_window, 'Ошибка', 'Порт должен быть числом')
        else:
            config['SETTINGS']['listen_address'] = config_window.ip.text()
            if 1023 < port < 65536:
                config['SETTINGS']['default_port'] = str(port)
                print(port)
                with open('server.ini', 'w') as conf:
                    config.write(conf)
                    message.information(
                        config_window, 'OK', 'Настройки успешно сохранены!')
            else:
                message.warning(
                    config_window,
                    'Ошибка',
                    'Порт должен быть от 1024 до 65536')

    # Таймер, обновляющий список клиентов 1 раз в секунду
    timer = QTimer()
    timer.timeout.connect(list_update)
    timer.start(1000)

    # Связываем кнопки с процедурами
    main_window.refresh_button.triggered.connect(list_update)
    main_window.show_history_button.triggered.connect(show_statistics)
    main_window.config_btn.triggered.connect(server_config)

    # Запускаем GUI
    server_app.exec_()


if __name__ == '__main__':
    main()
