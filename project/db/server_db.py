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


# БД сервера
class ServerDB:
    Base = declarative_base()

    class AllUsers(Base):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        user = Column(String, unique=True)
        last_conn = Column(DateTime)

        def __init__(self, user):
            self.user = user
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

    class UsersContacts(Base):
        __tablename__ = 'users_contacts'
        id = Column(Integer, primary_key=True)
        user = Column(String, ForeignKey('users.id'))
        contact = Column(String, ForeignKey('users.id'))

        def __init__(self, user, contact):
            self.user = user
            self.contact = contact

    class UsersHistory(Base):
        __tablename__ = 'users_history'
        id = Column(Integer, primary_key=True)
        user = Column(String, ForeignKey('users.id'))
        sent = Column(Integer)
        accepted = Column(Integer)

        def __init__(self, user):
            self.user = user
            self.sent = 0
            self.accepted = 0

    def __init__(self, path):
        self.engine = create_engine(f'sqlite:///{path}', echo=False, pool_recycle=7200,
                                    connect_args={'check_same_thread': False})

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
        rez = self.session.query(self.AllUsers).filter_by(user=username)
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
            user_in_history = self.UsersHistory(user.id)
            self.session.add(user_in_history)

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
        user = self.session.query(self.AllUsers).filter_by(user=username).first()

        # Удаляем его из таблицы активных пользователей.
        # Удаляем запись из таблицы ActiveUsers
        self.session.query(self.ActiveUsers).filter_by(user=user.id).delete()

        # Применяем изменения
        self.session.commit()

    # Функция фиксирует передачу сообщения и обновляет счетчики в БД истории пользователя
    def process_message(self, sender, recipient):
        # Получаем ID отправителя и получателя
        sender = self.session.query(self.AllUsers).filter_by(user=sender).first().id
        recipient = self.session.query(self.AllUsers).filter_by(user=recipient).first().id
        # Запрашиваем строки из истории и увеличиваем счётчики
        sender_row = self.session.query(self.UsersHistory).filter_by(user=sender).first()
        sender_row.sent += 1
        recipient_row = self.session.query(self.UsersHistory).filter_by(user=recipient).first()
        recipient_row.accepted += 1

        self.session.commit()

    # Функция добавляет контакт для пользователя.
    def add_contact(self, user, contact):
        # самому себя контактом нельзя
        if user == contact:
            return

        # Получаем ID пользователей
        try:
            user_id = self.session.query(self.AllUsers).filter_by(user=user).first().id
            contact_id = self.session.query(self.AllUsers).filter_by(user=contact).first().id
        except AttributeError:
            if __debug__:
                LOG.debug(f'Добавление контакта - юзер {user} или {contact} не найден')
                print(f'Добавление контакта - юзер {user} или {contact} не найден')
            return

        # Проверяем что не дубль и что контакт может существовать (полю пользователь мы доверяем)
        if not contact or self.session.query(self.UsersContacts).filter_by(user=user_id, contact=contact_id).count():
            return

        # Создаём объект и заносим его в базу
        contact_row = self.UsersContacts(user_id, contact_id)
        self.session.add(contact_row)
        self.session.commit()

    # Функция удаляет контакт из базы данных
    def remove_contact(self, user, contact):
        # Получаем ID пользователей
        user = self.session.query(self.AllUsers).filter_by(user=user).first()
        contact = self.session.query(self.AllUsers).filter_by(user=contact).first()

        # Проверяем что контакт может существовать (полю пользователь мы доверяем)
        if not contact:
            return

        # Удаляем требуемое
        # print(self.session.query(self.UsersContacts).filter(
        #     self.UsersContacts.user == user.id,
        #     self.UsersContacts.contact == contact.id
        # ).delete())
        self.session.query(self.UsersContacts).filter_by(user=user.id, contact=contact.id).delete()
        self.session.commit()

    # Функция возвращает список контактов пользователя.
    def get_contacts(self, username):
        # Запрашиваем указанного пользователя
        user = self.session.query(self.AllUsers).filter_by(user=username).one()

        # Запрашиваем его список контактов
        query = self.session.query(self.UsersContacts, self.AllUsers.user). \
            filter_by(user=user.id). \
            join(self.AllUsers, self.UsersContacts.contact == self.AllUsers.id)

        # выбираем только имена пользователей и возвращаем их.
        return [contact[1] for contact in query.all()]

    # Функция возвращает список известных пользователей со временем последнего входа.
    def users_list(self):
        query = self.session.query(
            self.AllUsers.user,
            self.AllUsers.last_conn,
        )
        # Возвращаем список кортежей
        return query.all()

    # Функция возвращает список активных пользователей
    def active_users_list(self):
        # Запрашиваем соединение таблиц и собираем тюплы имя, адрес, порт, время.
        query = self.session.query(
            self.AllUsers.user,
            self.ActiveUsers.ip,
            self.ActiveUsers.port,
            self.ActiveUsers.time_conn
        ).join(self.AllUsers)
        # Возвращаем список кортежей
        return query.all()

    # Функция возвращает историю входов по пользователю или по всем пользователям
    def login_history(self, username=None):
        # Запрашиваем историю входа
        query = self.session.query(self.AllUsers.user,
                                   self.LoginHistory.last_conn,
                                   self.LoginHistory.ip,
                                   self.LoginHistory.port
                                   ).join(self.AllUsers)
        # Если было указано имя пользователя, то фильтруем по нему
        if username:
            query = query.filter(self.AllUsers.user == username)
        return query.all()

    # Функция возвращает количество переданных и полученных сообщений
    def message_history(self):
        query = self.session.query(
            self.AllUsers.user,
            self.AllUsers.last_conn,
            self.UsersHistory.sent,
            self.UsersHistory.accepted
        ).join(self.AllUsers)
        # Возвращаем список кортежей
        return query.all()

"""
                            SQLAlchemy
all()	Возвращает результат запроса (объект Query) в виде списка
count()	Возвращает общее количество записей в запросе
first()	Возвращает первый результат из запроса или None, если записей нет
scalar()	Возвращает первую колонку первой записи или None, если результат пустой. Если записей несколько, то бросает исключение MultipleResultsFound
one	Возвращает одну запись. Если их несколько, бросает исключение MutlipleResultsFound. Если данных нет, бросает NoResultFound
get(pk)	Возвращает объект по первичному ключу (pk) или None, если объект не был найден
filter(*criterion)	Возвращает экземпляр Query после применения оператора WHERE
limit(limit)	Возвращает экземпляр Query после применения оператора LIMIT
offset(offset)	Возвращает экземпляр Query после применения оператора OFFSET
order_by(*criterion)	Возвращает экземпляр Query после применения оператора ORDER BY
join(*props, **kwargs)	Возвращает экземпляр Query после создания SQL INNER JOIN
outerjoin(*props, **kwargs)	Возвращает экземпляр Query после создания SQL LEFT OUTER JOIN
group_by(*criterion)	Возвращает экземпляр Query после добавления оператора GROUP BY к запросу
having(criterion)	Возвращает экземпляр Query после добавления оператора HAVING
"""


if __name__ == '__main__':
    from pprint import pprint
    PATH = os.path.dirname(os.path.abspath(__file__))
    PATH = os.path.join(PATH, 'server_base.db3')

    # тестирование
    db = ServerDB(PATH)
    db.user_login('test_user1', '192.168.1.4', 65600)
    db.user_login('test_user2', '192.168.1.5', 65500)
    # выводим список кортежей - активных пользователей
    print('Должно быть 2 активных юзера. Проверяем: ', len(db.active_users_list()))
    pprint(db.active_users_list())

    # lesson 4
    print('=' * 50)
    print('Написали сообщение. Счетчики в истори должны увеличится')
    db.process_message('test_user1', 'test_user2')
    print('Message history')
    pprint(db.message_history())

    db.add_contact('test_user2', 'test_user1')
    db.add_contact('test_user1', 'test_user2')
    print('Контакты test_user1', db.get_contacts('test_user1'))
    db.remove_contact('test_user1', 'test_user2')
    print('Контакты test_user1 после удаления одного', db.get_contacts('test_user1'))

    print('=' * 50)


    # # выполняем 'отключение' пользователя
    db.user_logout('test_user1')
    print('Отключили. Должен остаться 1. Проверяем: ', len(db.active_users_list()))
    print('Общий список. Тут должны быть 2 наших test_user. Метод users_list')
    pprint(db.users_list())
    # еще одного отключаем
    # db.user_logout('test_user2')
    print('Отключили и второго. В общем списке без изменений')
    print(db.users_list())
    print('А вот активных должно стать Ноль')
    print(db.active_users_list())
    # история
    print('='*50)
    print('В истории наши тесты тоже засветились')
    print('история test_user1', db.login_history('test_user1'))
    print('история test_user2', db.login_history('test_user2'))
    print('история всех')
    pprint(db.login_history())
    # очищаем за собой
    # exit(5)
    user = db.session.query(db.AllUsers).filter_by(user='test_user1').first()
    print(user)
    if user:
        db.session.query(db.LoginHistory).filter_by(user=user.id).delete()
        db.session.query(db.ActiveUsers).filter_by(user=user.id).delete()
        db.session.query(db.UsersHistory).filter_by(user=user.id).delete()
        db.session.query(db.UsersContacts).filter_by(user=user.id).delete()
        db.session.query(db.AllUsers).filter_by(id=user.id).delete()
    user = db.session.query(db.AllUsers).filter_by(user='test_user2').first()
    if user:
        db.session.query(db.LoginHistory).filter_by(user=user.id).delete()
        db.session.query(db.ActiveUsers).filter_by(user=user.id).delete()
        db.session.query(db.UsersHistory).filter_by(user=user.id).delete()
        db.session.query(db.UsersContacts).filter_by(user=user.id).delete()
        db.session.query(db.AllUsers).filter_by(id=user.id).delete()
    db.session.commit()
