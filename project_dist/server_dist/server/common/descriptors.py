import logging
LOG = logging.getLogger('app.server')


# Дескриптор для описания порта:
class Port:
    def __set__(self, instance, value):
        # instance - экземпляр класса - <__main__.Server object at 0x000000D582740C50>
        # value - значение переменной self.name - 7777
        if not 1023 < value < 65536:
            LOG.critical(
                f'Попытка запуска сервера с указанием неподходящего порта {value}. Допустимы адреса с 1024 до 65535.')
            exit(1)
        # Если порт прошёл проверку, добавляем его в список атрибутов экземпляра
        instance.__dict__[self.name] = value

    # тут прилетит имя переменной по которой работает дескриптор
    def __set_name__(self, owner, name):
        # owner - класс владелец атребута - <class '__main__.Server'>
        # name - имя переменной, с нашем случае - port
        self.name = name

