"""
Для того, чтобы свободно чувствовать себя с любой БД
необходимо овладеть операциями CRUD:

C - Create
R - Retrieve/Read
U - Update
D - Delete

"""

from exp_6 import User, sess


# create
# user_2 = User("Пётр", "Петров", "pass_Petrov")
# sess.add(user_2)
#
# sess.add_all([
#     User("kolia", "Cool Kolian[S.A.]","kolia$$$"),
#     User("zina", "Zina Korzina", "zk18")
# ])
#
# sess.commit()


# # Retrieve
result = sess.query(User).filter_by(name='Иван')
print('rows count: ', result.count())
print('rows data: ', result.all())

# # Update 1 row
result.first().password = '4444'
print('Wait: ', sess.new)
sess.commit()
#
# # Update multiple lines simultaneously var #1
# for row in result.all():
#     row.password += "1"
# sess.commit()
#
# # Update multiple lines simultaneously variant #2
# result.update({User.password: 6666})
# sess.commit()
#
# # Delete
# print('count before delete: ', result.count())
# print('rows before delete: ', result.all())
# result.delete()
# sess.commit()

"""
**************************** ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ *************************************
Более подробно о всех командах и методах можно прочитать в англоязычном
https://www.sqlalchemy.org/
или в русскоязычном описании SQAlchemy
https://lectureswww.readthedocs.io/6.www.sync/2.codding/9.databases/2.sqlalchemy/
********************************************************************************************
"""
