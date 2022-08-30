# ========================= Аспекты безопасности ==============================
# ---------------------------- SQL-инъекции -----------------------------------

import os
import sqlite3
from pprint import pprint

from sql_injection_1 import create_db


def sql_injection_2(user_id, user_login):
    """
    Попытка защититься, экранировав кавычками отдельные параметры запроса
    """

    # Однако такая строка тоже может быть уязвима:
    week_select_2 = 'SELECT * FROM USER WHERE id = "{}" AND login = "{}"'

    conn = sqlite3.connect(db_file)
    curr = conn.cursor()
    curr.execute(week_select_2.format(user_id, user_login))
    res = curr.fetchall()
    print('Результат второй уязвимой строки с запросом: ')
    pprint(res)
    conn.close()


if __name__ == '__main__':
    # Сначала создадим БД для демонстрации:
    db_file = 'strong.sqlite3'
    create_db(db_file)

    # В примере ниже будет сформирован запрос:
    # SELECT * FROM Users WHERE id ="" or ""="" AND login ="" or ""=""
    # Выражение or ""="" всегда истинно, поэтому запрос вернёт все записи из таблицы
    sql_injection_2('" or ""="', '" or ""="')
