Server module
=============

Приложение Server служит для взаимодействия с клиентскими модулями.
Сервер осуществляет хранение пользовательских учетных записей, их контактов, истории и статистики.

**Параметры запуска:**

``python server.py --help``

*выдаст справку по все командам*

Простой синтаксис ``python server.py`` запустит сервер с параметрами по умолчанию.

.. automodule:: server
   :members:
   :undoc-members:
   :show-inheritance:

server.add_user module
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: server.add_user.RegisterUser
	:members:

server.config_window module
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: server.config_window.ConfigWindow
	:members:

server.core module
~~~~~~~~~~~~~~~~~~

.. autoclass:: server.core.MessageProcessor
	:members:

server.database module
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: server.database.ServerStorage
	:members:

server.main_window module
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: server.main_window.MainWindow
	:members:

server.stat_window module
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: server.stat_window.StatWindow
	:members:

server.remove_user module
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: server.remove_user.DelUserDialog
	:members: