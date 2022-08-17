"""Новый протокол дескрипторов"""


class NonNegative:

    def __get__(self, instance, owner):
        return instance.__dict__[self.my_attr]

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError("Не может быть отрицательным")
        instance.__dict__[self.my_attr] = value

    def __delete__(self, instance):
        del instance.__dict__[self.my_attr]

    def __set_name__(self, owner, my_attr):
        # owner - владелец атрибута - <class '__main__.Worker'>
        # my_attr - имя атрибута владельца - hours, rate
        self.my_attr = my_attr


class Worker:
    # имя атрибута, который делаем дескриптором, в конструктор не передаем
    hours = NonNegative()
    rate = NonNegative()

    def __init__(self, name, surname, hours, rate):
        self.name = name
        self.surname = surname
        self.hours = hours
        self.rate = rate

    def total_profit(self):
        return self.hours * self.rate


iiv = Worker('Иван', 'Иванов', 10, 100)
print(iiv.total_profit())

iiv.hours = 10
iiv.rate = 100
print(iiv.total_profit())

# работает, как надо
# iiv = Worker('Иван', 'Иванов', -10, 100)
# print(OBJ.total_profit())

# iiv.hours = 10
# iiv.rate = -100
# print(OBJ.total_profit())

# работает, как требуется
# проблема решена
