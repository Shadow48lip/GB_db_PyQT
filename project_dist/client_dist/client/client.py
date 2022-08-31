""" Клиент JIM (JSON instant messaging) """

import sys
import os
import argparse
from Cryptodome.PublicKey import RSA
from common.variables import *
from common.decorators import log
from common.errors import ServerError
import logging
import logs.client_log_config
from PyQt5.QtWidgets import QApplication, QMessageBox
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
    parser.add_argument('-p', '--password', default='', nargs='?', help='пароль пользователя')
    args = parser.parse_args()

    if args.port < 1024 or args.port > 65536:
        LOG.warning('Номер порта должен быть указан в пределах 1024 - 65635')
        exit(1)

    return args.addr, args.port, args.name, args.password


if __name__ == '__main__':
    # Загружаем параметры командной строки
    server_address, server_port, client_name, client_passwd = arg_parser()

    # Создаём клиентское приложение
    client_app = QApplication(sys.argv)

    start_dialog = UserNameDialog()
    # Если имя пользователя не было указано в командной строке, то запросим его
    if not client_name or not client_passwd:
        client_app.exec_()
        # Если пользователь ввёл имя и нажал ОК, то сохраняем ведённое и удаляем объект.
        # Иначе - выходим
        if start_dialog.ok_pressed:
            client_name = start_dialog.client_name.text()
            client_passwd = start_dialog.client_passwd.text()
            LOG.debug(f'Входные данные: USERNAME = {client_name}, PASSWD = {client_passwd}.')
        else:
            exit(0)

    # Записываем логи
    LOG.info(
        f'Запущен клиент с параметрами: адрес сервера: {server_address} , '
        f'порт: {server_port}, имя пользователя: {client_name}')

    # Загружаем ключи с файла, если же файла нет, то генерируем новую пару.
    dir_path = os.path.dirname(os.path.realpath(__file__))
    key_file = os.path.join(dir_path, f'{client_name}.key')
    if not os.path.exists(key_file):
        keys = RSA.generate(2048, os.urandom)
        with open(key_file, 'wb') as key:
            key.write(keys.export_key())
    else:
        with open(key_file, 'rb') as key:
            keys = RSA.import_key(key.read())

    # !!!keys.publickey().export_key()
    LOG.debug("Keys successfully loaded.")
    # Создаём объект базы данных
    database = ClientDatabase(client_name)
    # Создаём объект - транспорт и запускаем транспортный поток
    try:
        transport = ClientTransport(
            server_port,
            server_address,
            database,
            client_name,
            client_passwd,
            keys)
        LOG.debug("Transport ready.")
    except ServerError as error:
        message = QMessageBox()
        message.critical(start_dialog, 'Ошибка сервера', error.text)
        exit(1)
    transport.daemon = True
    transport.start()

    # Удалим объект диалога за ненадобностью
    del start_dialog

    # Создаём GUI
    main_window = ClientMainWindow(database, transport, keys)
    main_window.make_connection(transport)
    main_window.setWindowTitle(f'GB-Чат Программа - {client_name}')
    client_app.exec_()

    # Раз графическая оболочка закрылась, закрываем транспорт
    transport.transport_shutdown()
    transport.join()
