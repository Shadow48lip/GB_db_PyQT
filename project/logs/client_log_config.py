""" Логирование клиентского модуля """

import os
import sys
import logging
from common.variables import LOGGING_LEVEL

# Создаём объект-логер с именем app.client
log = logging.getLogger('app.client')

# Создаём объект форматирования:
_formatter = logging.Formatter("%(asctime)s  %(levelname)-8s  %(module)-10s  %(message)s")
_formatter_stream = logging.Formatter("%(levelname)-8s  %(message)s ")

# Создаём файловый обработчик логирования (можно задать кодировку):
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'client.log')
fh = logging.FileHandler(PATH, encoding='utf-8')
# fh.setLevel(logging.DEBUG)
fh.setFormatter(_formatter)

# Вывод критических ошибок
sh = logging.StreamHandler(sys.stderr)
sh.setFormatter(_formatter_stream)
sh.setLevel(logging.WARNING)

# Добавляем в логер новый обработчик событий и устанавливаем уровень логирования
log.addHandler(fh)
log.addHandler(sh)
log.setLevel(LOGGING_LEVEL)

if __name__ == '__main__':
    # Создаём потоковый обработчик логирования (по умолчанию sys.stderr):
    stream_hand = logging.StreamHandler()
    # console.setLevel(logging.DEBUG)
    stream_hand.setFormatter(_formatter)
    log.addHandler(stream_hand)
    # В логирование передаем имя текущей функции и имя вызвавшей функции
    log.debug('Отладочное сообщение')