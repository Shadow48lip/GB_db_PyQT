# ========================= Аспекты безопасности ==============================
# ---------------------------- SQL-инъекции -----------------------------------

import os
import sqlite3
from sql_injection_1 import create_db


def sql_injection_3(user_id):
    """Простая SQL-инъекция с большими возможностями"""

    week_select_3 = "SELECT * FROM USER WHERE id = {}"

    conn = sqlite3.connect(db_file)
    curr = conn.cursor()
    # curr.execute(week_select_3.format(user_id))
    curr.executescript(week_select_3.format(user_id))
    res = curr.fetchall()
    print('Результат третьей уязвимой строки с запросом: ')
    print(res)


if __name__ == '__main__':
    # Сначала создадим БД для демонстрации:
    db_file = 'strong.sqlite3'
    create_db(db_file)

    # Для некоторых СУБД может быть выполнен следующий запрос:
    sql_injection_3('1; DROP TABLE USER;')
    # Будет сформирован запрос:
    # SELECT * FROM USER WHERE id = 1; DROP TABLE USER;
    # который приведёт к удалению таблицы USER


"""
 ----------------------------- Выводы ----------------------------------------
 Для защиты от SQL-инъекций стоит:
 
 1. Использовать параметры в SQL-запросах, например:
 Инструкция SQL с параметром может выглядеть следующим образом,
 где «?» представляет параметр для идентификатора автора:
     week_select_1 = "SELECT * FROM USER WHERE id = ?;"
     curr.execute(week_select_1, user_id)
     
 2. Проводить фильтрацию пользовательского ввода до передачи в SQL-запрос
"""