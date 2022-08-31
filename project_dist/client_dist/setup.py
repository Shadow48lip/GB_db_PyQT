from setuptools import setup, find_packages

setup(name="sh_py_mess_client",
      version="0.0.1",
      description="GeekBrains Mess Client. Coursework in a programming language.",
      author="Ivan Ivanov",
      author_email="iv.iv@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
