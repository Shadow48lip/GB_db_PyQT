""" Клиент JIM (JSON instant messaging """

import json
import sys
import time
import argparse
import threading
from socket import socket, AF_INET, SOCK_STREAM
from common.utils import get_message, send_message
from common.variables import *
from common.decorators import log
from common.errors import ServerError
import logging
import logs.client_log_config
from common.metaclasses import ClientMaker
from db.client_db import ClientDB
from PyQt5.QtWidgets import QApplication
from client.database import ClientDatabase
from client.transport import ClientTransport
from client.main_window import ClientMainWindow
from client.start_dialog import UserNameDialog

LOG = logging.getLogger('app.client')


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


if __name__ == '__main__':
    # Загружаем параметы коммандной строки
    server_address, server_port, client_name = arg_parser()

    # Создаём клиентокое приложение
    client_app = QApplication(sys.argv)

    # Если имя пользователя не было указано в командной строке, то запросим его
    if not client_name:
        start_dialog = UserNameDialog()
        client_app.exec_()
        # Если пользователь ввёл имя и нажал ОК, то сохраняем ведённое и удаляем объект.
        # Иначе - выходим
        if start_dialog.ok_pressed:
            client_name = start_dialog.client_name.text()
            del start_dialog
        else:
            exit(0)

    # Записываем логи
    LOG.info(
        f'Запущен клиент с парамертами: адрес сервера: {server_address} , '
        f'порт: {server_port}, имя пользователя: {client_name}')

    # Создаём объект базы данных
    database = ClientDatabase(client_name)

    # Создаём объект - транспорт и запускаем транспортный поток
    try:
        transport = ClientTransport(server_port, server_address, database, client_name)
    except ServerError as error:
        print(error.text)
        exit(1)
    transport.daemon = True
    transport.start()

    # Создаём GUI
    main_window = ClientMainWindow(database, transport)
    main_window.make_connection(transport)
    main_window.setWindowTitle(f'Чат Программа alpha release - {client_name}')
    client_app.exec_()

    # Раз графическая оболочка закрылась, закрываем транспорт
    transport.transport_shutdown()
    transport.join()
