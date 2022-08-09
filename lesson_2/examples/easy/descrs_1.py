"""Простой класс с атрибутами и методом"""


class Worker:
    """Класс-работник"""
    def __init__(self, name, surname, hours, rate):
        self.name = name
        self.surname = surname
        self.hours = hours
        self.rate = rate

    def total_profit(self):
        """Расчет зарплаты"""
        return self.hours * self.rate


iiv = Worker('Иван', 'Иванов', 10, 100)
print(iiv.total_profit())

iiv.hours = 10
iiv.rate = 100
print(iiv.total_profit())

# теперь попробуем присвоить какому-либо из атрибутов отрицательное значение

iiv = Worker('Иван', 'Иванов', -10, 100)
print(iiv.total_profit())

iiv.hours = 10
iiv.rate = -100
print(iiv.total_profit())

# проблема очевидна: значение атрибута при присвоении не проходит валидацию,
# следовательно, скрипт может отрабатывать некорректно
