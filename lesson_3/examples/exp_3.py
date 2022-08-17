"""БД и подстановка значений в запрос и SQL-инъекции"""

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


# --------------------------Подстановка значений в запрос------------------------- #
# Такая задача требуется очень часто. Как ее решить?

# 1. С подстановкой по порядку на места знаков вопросов:
crs.execute("SELECT Name FROM Artist ORDER BY Name LIMIT ?", '2')
result = crs.fetchall()
print(result)  # -> [('A Cor Do Som',), ('AC/DC',)]

# 2. С использованием именованных замен:
crs.execute("SELECT Name from Artist ORDER BY Name LIMIT :limit", {"limit": 2})
result = crs.fetchall()
print(result)  # -> [('A Cor Do Som',), ('AC/DC',)]

# 3. С использованием подстановки через %:
crs.execute("SELECT Name FROM Artist ORDER BY Name LIMIT %s" % '2')
result = crs.fetchall()
print(result)  # -> [('A Cor Do Som',), ('AC/DC',)]


# Вариант 1 - параметризованный запрос защитит нас от SQL-инъекций
# лучше исп-ть его

# ====================== Пример SQL-инъекции ======================
# sql_injection = '2; DROP TABLE Artist'
# crs.executescript("SELECT Name FROM Artist ORDER BY Name LIMIT %s" % sql_injection)
# result = crs.fetchall()
# print(result)  # -> []


# Множественная подстановка значений
# Для подстановки списка значений в запрос используется метод курсора executemany():
new_artists = [
    ('A Aagrh!',),
    ('A Aagrh!-2',),
    ('A Aagrh!-3',),
]
crs.executemany("insert into Artist values (Null, ?);", new_artists)