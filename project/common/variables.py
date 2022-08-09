""" Константы проекта """

import logging

# сокет
DEFAULT_PORT = 7777
DEFAULT_IP_ADDRESS = '127.0.0.1'
MAX_CONNECTIONS = 5
MAX_PACKET_LENGTH = 1024
ENCODING = 'utf-8'
CONNECTION_TIMEOUT = 0.5
# Текущий уровень логирования
LOGGING_LEVEL = logging.DEBUG

# протокол JIM
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
SENDER = 'from'
DESTINATION = 'to'

PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
MESSAGE = 'msg'
MESSAGE_TEXT = 'message'
EXIT = 'exit'
