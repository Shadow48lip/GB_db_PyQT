from setuptools import setup, find_packages

setup(name="sh_py_mess_server",
      version="0.0.2",
      description="GeekBrains Mess Server. Coursework in a programming language.",
      author="Ivan Ivanov",
      author_email="iv.iv@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'],
      scripts=['server/server_run']
      )
