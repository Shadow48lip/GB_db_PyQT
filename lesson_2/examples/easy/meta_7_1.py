"""
Код взят мной из примера в stackoverflow:
https://stackoverflow.com/questions/100003/what-are-metaclasses-in-python

Здесь показано, как при создании нового класса метакласс изменяет
все буквы в именах атрибутов на заглавные (исключая "дендер"-атрибуты)

"""
from pprint import pprint


def upper_attr(future_class_name, future_class_parents, future_class_attrs):
    """
      Return a class object, with the list of its attribute turned
      into uppercase.
    """
    # pick up any attribute that doesn't start with '__' and uppercase it
    uppercase_attrs = {
        attr if attr.startswith("__") else attr.upper(): v
        for attr, v in future_class_attrs.items()
    }

    # let `type` do the class creation
    return type(future_class_name, future_class_parents, uppercase_attrs)


__metaclass__ = upper_attr  # this will affect all classes in the module


class Foo(metaclass=upper_attr):  # global __metaclass__ won't work with "object" though
    # but we can define __metaclass__ here instead to affect only this class
    # and this will work with "object" children
    bar = 'bip'


print("hasattr(Foo, 'bar'): ", hasattr(Foo, 'bar'))
print("hasattr(Foo, 'BAR'): ", hasattr(Foo, 'BAR'))

try:
    print(Foo.bar)
except Exception as e:
    print(f'Exception: {e}')

print('Foo.BAR =', Foo.BAR)
pprint(Foo.__dict__)
