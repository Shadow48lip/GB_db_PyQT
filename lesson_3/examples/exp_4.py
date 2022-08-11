"""БД и курсор как итератор"""

# Подключение библиотеки, соответствующей типу требуемой базы данных
import os
import sqlite3

db_full_path = os.path.join(os.path.dirname(__file__), "demo.sqlite")

# Создание соединения с базой данных
# В данном случае это файл базы
connection = sqlite3.connect(db_full_path)
# connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)

# Создаем курсор — это специальный объект,
# который делает запросы и получает их результаты
crs = connection.cursor()

# ---------------------------Курсор как итератор-------------------------- #
# Использование курсора как итератора
fetch = crs.execute('SELECT Name FROM Artist ORDER BY Name LIMIT 3')
print(fetch)
print(list(fetch))
print('=' * 50)

# Извлечение элементов из crs с помощью цикла for
for row in crs.execute('SELECT Name FROM Artist ORDER BY Name LIMIT 3'):
    print(row)

# Полученный результат:
'''
('A Cor Do Som',)
('AC/DC',)
('Aaron Copland & London Symphony Orchestra',)
'''
