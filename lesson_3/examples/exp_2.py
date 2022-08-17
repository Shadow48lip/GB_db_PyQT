"""БД и запросы на изменение"""

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

# ---------------------------Запрос на изменение----------------------------- #

# Выполняется INSERT-запрос к базе данных с обычным SQL-синтаксисом
crs.execute("INSERT INTO Artist VALUES (Null, 'A Aagrh!') ")

# Если выполняются изменения в базе данных, необходимо сохранить транзакцию
connection.commit()

# Проверка результатов
crs.execute("SELECT Name FROM Artist ORDER BY Name LIMIT 3")
result = crs.fetchall()
print(result)  # -> [('A Aagrh!',), ('A Cor Do Som',), ('AC/DC',)]

# ==============================================================

# А можно ли выполнить несколько запросов за раз???

# crs.execute("""
#     INSERT INTO Artist VALUES (Null, 'A Aagrh!');
#     INSERT INTO Artist VALUES (Null, 'A Aagrh-2!');
# """)


# Будет ошибка
# sqlite3.Warning: You can only execute one statement at a time.


# ==============================================================

# Что же делать?
# Вариант есть!


# crs.executescript("""
#     INSERT INTO Artist VALUES (Null, 'A Aagrh!');
#     INSERT INTO Artist VALUES (Null, 'A Aagrh-2!');
# """)


