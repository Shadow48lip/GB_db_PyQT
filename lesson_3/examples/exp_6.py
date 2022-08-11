"""
ORM с помощью SQLAalchemy.
ВАРИАНТ 1: ТРАДИЦИОННЫЙ СТИЛЬ"

ВНИМАНИЕ! SQLAalchemy требует предварительной установки:

pip install sqlalchemy
"""

# import sqlalchemy
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.orm import mapper, sessionmaker

# Проверим версию SQLAlchemy
try:
    import sqlalchemy

    print("Версия SQLAlchemy:", sqlalchemy.__version__)
except ImportError:
    print('Библиотека SQLAlchemy не найдена')
    exit(13)


# -----------------------Создание подключений к БД-------------------------------- #
# ENGINE = create_engine('sqlite:///:memory:', echo=False)
engine = create_engine('sqlite:///traditional_style_base.db3', echo=True)

# Создание подключения к локальной базе данных PostgreSQL
# engine_1 = create_engine('postgresql+psycopg2://username:password@localhost:5432/mydb')

# Создание подключения к удалённой базе данных MySQL
# engine_2 = create_engine('mysql+pymysql://cookiemonster:chocolatechip@mysql01.monster.internal/cookies',
# pool_recycle=3600)

print(engine)  # -> Engine(sqlite:///traditional_style_base.db3)

# -----------------------------Создание таблиц------------------------------------ #
metadata = MetaData()
users_table = Table('users', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('name', String),
                    Column('surname', String),
                    Column('password', String)
                    )

metadata.create_all(engine)


# ----------------------Определение класса Python для отображения в таблицу--------------------- #
# т.е. создаём шаблон записи таблицы БД

class User:
    def __init__(self, name, surname, password):
        self.name = name
        self.surname = surname
        self.password = password

    def __repr__(self):
        return f'<User({self.name}, {self.surname}, {self.password})>'


# ---------------------------------Настройка отображения----------------------------------------- #
# Связываем данные и таблицу с помощью mapper
mapper(User, users_table)

# ------------------------------------Создание сессии-------------------------------------------- #
# С помощью конструктора sessionmaker создаем класс-сессия
Session = sessionmaker(bind=engine)
print('Session:', Session)

# и далее создаем экземпляр класса сессия Session
sess = Session()

# вот теперь все хорошо
if __name__ == '__main__':
    user = User("Иван", "Иванов", "pass_Ivan")
    sess.add(user)
    sess.commit()
    print(user.id)  # -> 1
    print(user.name)  # -> Иван
