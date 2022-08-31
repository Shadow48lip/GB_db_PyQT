""" Логирование серверного модуля """

import os
import sys
import logging
from logging.handlers import TimedRotatingFileHandler
from common.variables import LOGGING_LEVEL

# Создаём объект-логер с именем app.server
log = logging.getLogger('app.server')

# Создаём объект форматирования:
_formatter = logging.Formatter("%(asctime)s  %(levelname)-8s  %(module)-10s  %(message)s")
_formatter_stream = logging.Formatter("%(levelname)-8s  %(message)s ")

# Создаём файловый обработчик логирования (можно задать кодировку):
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'server.log')
fh = TimedRotatingFileHandler(PATH, when='midnight', backupCount='3', encoding='utf-8')

# fh.setLevel(logging.DEBUG)
fh.setFormatter(_formatter)

# Вывод критических ошибок
sh = logging.StreamHandler(sys.stderr)
sh.setFormatter(_formatter_stream)
sh.setLevel(logging.ERROR)

# Добавляем в логер новый обработчик событий и устанавливаем уровень логирования
log.addHandler(fh)
log.addHandler(sh)
log.setLevel(LOGGING_LEVEL)

if __name__ == '__main__':
    log.error('Отладочное сообщение')

