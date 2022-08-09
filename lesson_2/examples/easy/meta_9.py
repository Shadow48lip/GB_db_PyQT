"""
Пример метакласса, переопределяющего поведение методов __new__, __init__ и __call__ своих классов
"""


class MyMetaClass(type):

    def __new__(cls, name, bases, dict):
        new_class = super(MyMetaClass, cls).__new__(cls, name, bases, dict)
        print(f'__new__({name}, {bases}, {dict}) -> {new_class}')
        return new_class

    def __init__(cls, name, bases, dict):
        super(MyMetaClass, cls).__init__(name, bases, dict)
        print(f'__init__({name}, {bases}, {dict})')

    def __call__(cls, *args, **kwargs):
        obj = super(MyMetaClass, cls).__call__(*args, **kwargs)
        print(f'__call__({args}, {kwargs}) -> {obj}')
        return obj


class Test(metaclass=MyMetaClass):
    pass


T_OBJ = Test()

"""
__new__() вызывается для создания класса;
__init__() для инициализации объектов класса;
__call__() вызывается при создании объектов класса;
"""
