# ========================= Аспекты безопасности ==============================
# ---------------------------- SQL-инъекции -----------------------------------

import os
import sqlite3
from pprint import pprint


def create_db(db_file):
    """
    Создание БД для демонстрации
    """
    if os.path.exists(db_file):
        os.remove(db_file)

    conn = sqlite3.connect(db_file)
    curr = conn.cursor()

    sql_create_user = """CREATE TABLE IF NOT EXISTS USER
                   (id INTEGER PRIMARY KEY,
                    login TEXT, 
                    password TEXT);"""
    curr.execute(sql_create_user)

    sql_insert = "INSERT INTO USER (login, password) VALUES (?, ?);"
    auth_data = {'admin': '21232f297a57a5a743894a0e4a801fc3',
                 'user': 'ee11cbb19052e40b07aac0ca060c23ee',
                 'guest': '084e0343a0486ff05530df6c705c8bb4'}
    for login, password in auth_data.items():
        curr.execute(sql_insert, (login, password))

    conn.commit()
    conn.close()


def sql_injection_1(user_id):
    """
    Пример простой SQL-инъекции
    """

    # Строка подобного рода уязвима к SQL-инъекциям:
    week_select_1 = "SELECT * FROM USER WHERE id = "
    week_select_1_2 = "SELECT * FROM USER WHERE id = {}"

    conn = sqlite3.connect(db_file)
    curr = conn.cursor()
    curr.execute(week_select_1 + (user_id))
    res = curr.fetchall()
    print('Результат первой уязвимой строки с запросом: ')
    pprint(res)

    curr.execute(week_select_1_2.format(user_id))
    res = curr.fetchall()
    print('Результат первой модифицированной уязвимой строки с запросом: ')
    pprint(res)
    conn.close()


if __name__ == '__main__':
    # Сначала создадим БД для демонстрации:
    db_file = 'strong.sqlite3'
    create_db(db_file)

    # Логическое выражение 1=1 всегда является истинным,
    # поэтому SELECT выберет все данные из таблицы:
    # SELECT * FROM Users WHERE id = 1 or 1=1
    sql_injection_1('1 OR 1=1')
    print('1 OR 1=1')
