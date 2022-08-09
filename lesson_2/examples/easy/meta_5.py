"""
Все, что вы видите в Python – объекты.
В том числе и строки, числа, классы и функции.
ЭТО ВЕДЬ КЛАССЫ! ОКАЗЫВАЕТСЯ У КАЖДОГО ИЗ ЭТИХ КЛАССОВ ТОЖЕ ЕСТЬ КЛАСС - СВЕРХКЛАСС

https://realpython.com/python-metaclasses/

Tim Peters, the Python guru who authored the Zen of Python:
"Metaclasses are deeper magic than 99% of users should ever worry about.
If you wonder whether you need them, you don’t (the people who actually need them
know with certainty that they need them, and don’t need an explanation about why)."

(Полезная статья на эту тему:
https://stackoverflow.com/questions/100003/what-are-metaclasses-in-python
"""

# начнём
AGE = 35
print(AGE.__class__)

NAME = 'Иван'
print(NAME.__class__)


def my_func():
    pass


print(my_func.__class__)


class MyClass(object):
    pass


MC = MyClass()
print(MC.__class__)


# Получается каждый из этих объектов относится к классу
# это мы знаем


print('=' * 50)
print(AGE.__class__.__class__)
print(NAME.__class__.__class__)
print(my_func.__class__.__class__)
print(MC.__class__.__class__)


# А что является метаклассом метакласса type?
print('=' * 50)
print(AGE.__class__.__class__.__class__)
print(NAME.__class__.__class__.__class__)
print(my_func.__class__.__class__.__class__)
print(MC.__class__.__class__.__class__)

"""
<class 'int'>
<class 'str'>
<class 'function'>
<class '__main__.MyClass'>

<class 'type'>
<class 'type'>
<class 'type'>
<class 'type'>
"""

# Получается у каждого из стандартных классов тоже есть класс-метакласс type
