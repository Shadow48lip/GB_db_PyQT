"""
tabulate - это модуль, который позволяет красиво отображать табличные данные.

ВАЖНО!!!
Пакет требует предварительной установки:

pip install tabulate

"""
#

from tabulate import tabulate

# генерация таблицы без шапки
print(' === генерация таблицы без шапки ===')
print()
TUPLES_LIST = [('Python', 'interpreted', '1991'),
               ('JAVA', 'compiled', '1995'),
               ('С', 'compiled', '1972')]

print(tabulate(TUPLES_LIST))

print()

# генерация таблицы с шапкой
print(' === генерация таблицы с шапкой ===')
print()
TUPLES_LIST = [('Python', 'interpreted', '1991'),
               ('JAVA', 'compiled', '1995'),
               ('С', 'compiled', '1972')]

COLUMNS = ['programming language', 'type', 'year']
print(tabulate(TUPLES_LIST, headers=COLUMNS))

print()

# генерация таблицы с шапкой, где шапка - первый элемент списка
print('=== генерация таблицы с шапкой, где шапка - первый элемент списка === ')
print('===                    headers="firstrow"                         === ')
print()
TUPLES_LIST = [('programming language', 'type', 'year'),
               ('Python', 'interpreted', '1991'),
               ('JAVA', 'compiled', '1995'),
               ('С', 'compiled', '1972')]

# Указание первой строки таблицы как набора заголовков
print(tabulate(TUPLES_LIST, headers='firstrow'))

print()

# если данные - список словарей, значение параметра headers является оператор keys
print('=== если данные - список словарей, значение параметра headers является оператор keys ===')
print()
DICTS_LIST = [{'programming language': 'Python',
               'type': 'interpreted',
               'year': '1991'},
              {'programming language': 'JAVA',
               'type': 'compiled',
               'year': '1995'},
              {'programming language': 'С',
               'type': 'compiled',
               'year': '1972'}]

# Табличное представление списка словарей
print(tabulate(DICTS_LIST, headers='keys'))
