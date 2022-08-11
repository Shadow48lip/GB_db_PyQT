# Описание серверверной части базы данных с использованием декларативного стиля SQLAlchemy

import logging
import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

LOG = logging.getLogger('app.server')

# Проверим версию SQLAlchemy
try:
    import sqlalchemy

    if __debug__:
        LOG.debug(f'SQLAlchemy: {sqlalchemy.__version__} подключена')
except ImportError:
    LOG.critical('Библиотека SQLAlchemy не найдена')
    exit(13)

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'server_base.db3')


# БД сервера
class ServerDB:
    Base = declarative_base()

    class AllUsers(Base):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        login = Column(String, unique=True)
        last_conn = Column(DateTime)

        def __init__(self, login):
            self.login = login
            self.last_conn = datetime.datetime.now()

    class ActiveUsers(Base):
        __tablename__ = 'users_active'
        id = Column(Integer, primary_key=True)
        user = Column(String, ForeignKey('users.id'), unique=True)
        ip = Column(String(50))
        port = Column(Integer)
        time_conn = Column(DateTime)

        def __init__(self, user, ip, port):
            self.user = user
            self.ip = ip
            self.port = port
            self.time_conn = datetime.datetime.now()

    class LoginHistory(Base):
        __tablename__ = 'users_login_history'
        id = Column(Integer, primary_key=True)
        user = Column(String, ForeignKey('users.id'))
        ip = Column(String)
        port = Column(Integer)
        last_conn = Column(DateTime)

        def __init__(self, user, ip, port):
            self.user = user
            self.ip = ip
            self.port = port
            self.last_conn = datetime.datetime.now()

    def __init__(self):
        # self.engine = create_engine('sqlite:///server_base.db3', echo=False, pool_recycle=7200)

        db_path = os.path.join("db", "server_base.db3")
        self.engine = create_engine('sqlite:///' + PATH, echo=False, pool_recycle=7200)

        self.Base.metadata.create_all(self.engine)
        session = sessionmaker(bind=self.engine)
        self.session = session()

        # Если в таблице активных пользователей есть записи, то их необходимо удалить
        # Когда устанавливаем соединение, очищаем таблицу активных пользователей
        self.session.query(self.ActiveUsers).delete()
        self.session.commit()

    # Функция выполняется при входе пользователя, фиксирует в базе сам факт входа
    def user_login(self, username, ip_address, port):
        # Запрос в таблицу пользователей на наличие там пользователя с таким именем
        rez = self.session.query(self.AllUsers).filter_by(login=username)
        # print(type(rez))
        # Если имя пользователя уже присутствует в таблице, обновляем время последнего входа
        if rez.count():
            user = rez.first()
            user.last_conn = datetime.datetime.now()
        # Если нет, то создаём нового пользователя
        else:
            # Создаем экземпляр класса self.AllUsers, через который передаем данные в таблицу
            user = self.AllUsers(username)
            self.session.add(user)
        # Коммит здесь нужен, чтобы в db записался ID
        self.session.commit()

        # Теперь можно создать запись в таблицу активных пользователей о факте входа.
        # Создаем экземпляр класса self.ActiveUsers, через который передаем данные в таблицу
        new_active_user = self.ActiveUsers(user.id, ip_address, port)
        self.session.add(new_active_user)

        # и сохранить в историю входов
        # Создаем экземпляр класса self.LoginHistory, через который передаем данные в таблицу
        history = self.LoginHistory(user.id, ip_address, port)
        self.session.add(history)

        # Сохраняем изменения
        self.session.commit()

    # Функция фиксирует отключение пользователя
    def user_logout(self, username):
        # Запрашиваем пользователя, что покидает нас
        # получаем запись из таблицы AllUsers
        user = self.session.query(self.AllUsers).filter_by(login=username).first()

        # Удаляем его из таблицы активных пользователей.
        # Удаляем запись из таблицы ActiveUsers
        self.session.query(self.ActiveUsers).filter_by(user=user.id).delete()

        # Применяем изменения
        self.session.commit()

    # Функция возвращает список известных пользователей со временем последнего входа.
    def users_list(self):
        query = self.session.query(
            self.AllUsers.login,
            self.AllUsers.last_conn,
        )
        # Возвращаем список тюплов
        return query.all()

    # Функция возвращает список активных пользователей
    def active_users_list(self):
        # Запрашиваем соединение таблиц и собираем тюплы имя, адрес, порт, время.
        query = self.session.query(
            self.AllUsers.login,
            self.ActiveUsers.ip,
            self.ActiveUsers.port,
            self.ActiveUsers.time_conn
        ).join(self.AllUsers)
        # Возвращаем список тюплов
        return query.all()

    # Функция возвращает историю входов по пользователю или по всем пользователям
    def login_history(self, username=None):
        # Запрашиваем историю входа
        query = self.session.query(self.AllUsers.login,
                                   self.LoginHistory.last_conn,
                                   self.LoginHistory.ip,
                                   self.LoginHistory.port
                                   ).join(self.AllUsers)
        # Если было указано имя пользователя, то фильтруем по нему
        if username:
            query = query.filter(self.AllUsers.login == username)
        return query.all()


if __name__ == '__main__':
    # тестирование
    db = ServerDB()
    db.user_login('test_user1', '192.168.1.4', 65600)
    db.user_login('test_user2', '192.168.1.5', 65500)
    # выводим список кортежей - активных пользователей
    print('Должно быть 2 активных юзера. Проверяем: ', len(db.active_users_list()))
    print(db.active_users_list())
    # # выполняем 'отключение' пользователя
    db.user_logout('test_user1')
    print('Должен остаться 1. Проверяем: ', len(db.active_users_list()))
    print('Общий список. Тут должны быть 2 наших test_user')
    print(db.users_list())
    # еще одного отключаем
    db.user_logout('test_user2')
    print('В общем списке без изменений')
    print(db.users_list())
    print('А вот активных должно стать Ноль')
    print(db.active_users_list())
    # история
    print('В истории наши тесты тоже засветились')
    print(db.login_history('test_user1'))
    print(db.login_history('test_user2'))
    print(db.login_history())
    # очищаем за собой
    user = db.session.query(db.AllUsers).filter_by(login='test_user1').first()
    print(user)
    if user:
        db.session.query(db.LoginHistory).filter_by(user=user.id).delete()
        db.session.query(db.ActiveUsers).filter_by(user=user.id).delete()
        db.session.query(db.AllUsers).filter_by(id=user.id).delete()
    user = db.session.query(db.AllUsers).filter_by(login='test_user2').first()
    if user:
        db.session.query(db.LoginHistory).filter_by(user=user.id).delete()
        db.session.query(db.ActiveUsers).filter_by(user=user.id).delete()
        db.session.query(db.AllUsers).filter_by(id=user.id).delete()
    db.session.commit()