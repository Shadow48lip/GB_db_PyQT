"""БД и обработка ошибок"""

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

# -----------------------------Обработка ошибок---------------------------- #

try:
    sql_statement = "INSERT INTO Artist VALUES (1, 'A Aagrh!')"
    crs.execute(sql_statement)
    result = crs.fetchall()
except sqlite3.DatabaseError as err:
    print("Error: ", err)  # -> Error:  UNIQUE constraint failed: Artist.ArtistId
else:
    connection.commit()

"""
ВАЖНО!!!
Дополнительная информация по типам исключений находится в методичке!
"""
