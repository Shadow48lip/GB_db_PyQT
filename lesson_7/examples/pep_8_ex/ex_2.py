# правильно
import os
import sys

# можно
from subprocess import Popen, PIPE

# неправильно
import os, sys

# при импорте объектов из модуля, например классов, можно писать
from myclass import MyClass
from foo.bar.yourclass import YourClass
