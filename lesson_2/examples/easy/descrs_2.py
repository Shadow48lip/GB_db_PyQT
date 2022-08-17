"""
Пытаемся решить проблему традиционным способом - через геттеры и сеттеры
"""


class Worker:
    """Делаем атрибуты защищенными"""
    def __init__(self, name, surname, hours, rate):
        self.name = name
        self.surname = surname
        if hours < 0:
            raise ValueError('This value must be positive!!!')
        self._hours = hours
        if rate < 0:
            raise ValueError('This value must be positive!!!')
        self._rate = rate

    # Для создания свойства-геттера над свойством ставится аннотация @property
    @property
    def hours(self):
        """Геттер"""
        return self._hours

    # сеттер
    # Для создания свойства-сеттера над свойством устанавливается
    # аннотация имя_свойства_геттера.setter
    @hours.setter
    def hours(self, value):
        """Сеттер"""
        if value < 0:
            raise ValueError('This value must be positive!!!')
        self._hours = value

    @property
    def rate(self):
        """Геттер"""
        return self._rate

    @rate.setter
    def rate(self, value):
        """Сеттер"""
        if value < 0:
            raise ValueError('This value must be positive!!!')
        self._rate = value

    def total_profit(self):
        """Вычисляем зарплату"""
        return self.hours * self.rate


iiv = Worker('Иван', 'Иванов', 10, 100)
print(iiv.total_profit())

iiv.hours = 10
iiv.rate = 100
print(iiv.total_profit())

# проблема вроде решена?
# увы, но нет
# сеттер здесь не сработает
# iiv = Worker('Иван', 'Иванов', -10, 100)
# print(iiv.total_profit())

# а здесь вроде решена,
# но не будем же мы на каждый атрибут делать геттер и сеттер
# это избыточность кода, т.е. проблема в целом не решена
# iiv.hours = 10
# iiv.rate = -100
# print(iiv.total_profit())
