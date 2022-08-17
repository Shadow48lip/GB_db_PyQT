""" Decorators """
import inspect
from functools import wraps
import logging
import logs.client_log_config
import logs.server_log_config
import sys


def log(func):
    """ Этот декортор фиксирует кто вызвал функцию и логирует это событие """
    logger = 'app.server' if 'server.py' in sys.argv[0] else 'app.client'
    LOG = logging.getLogger(logger)

    @wraps(func)
    def wrap(*args, **kwargs):
        f = func(*args, **kwargs)

        """ кто вызвал нашу функцию """
        current_frame = inspect.currentframe()
        # получи фрейм объект, который его вызвал
        caller_frame = current_frame.f_back
        # возьми у вызвавшего фрейма исполняемый в нём объект типа "код" (code object)
        code_obj = caller_frame.f_code
        # и получи его имя
        code_obj_name = code_obj.co_name

        LOG.info(f'вызов {func.__name__}() с параметрами {args} {kwargs} из функции {code_obj_name}')

        return f
    return wrap

