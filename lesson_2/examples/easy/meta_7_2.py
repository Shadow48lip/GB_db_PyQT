"""
Предыдущий пример, на этот раз выполненный с помощью класса UpperAttr
(вместо функции upper_attr)

С помощью dunder method __new__ мы можем изменять свойства отрибутов классов,
производных от метакласса UpperAttr.
"""
from pprint import pprint


class UpperAttr(type):
    # Вызывается для создания экземпляра класса, перед вызовом __init__
    def __new__(cls, future_class_name, future_class_parents, future_class_attrs):
        """
          Return a class object, with the list of its attribute turned
          into uppercase.
        """
        # pick up any attribute that doesn't start with '__' and uppercase it
        uppercase_attrs = {
            attr if attr.startswith("__") else attr.upper(): v
            for attr, v in future_class_attrs.items()
        }
        return type.__new__(cls, future_class_name, future_class_parents, uppercase_attrs)


class Foo(metaclass=UpperAttr):  # global __metaclass__ won't work with "object" though
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
