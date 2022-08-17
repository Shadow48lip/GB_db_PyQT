import os
import subprocess
import sys
from random import randint
from time import sleep


PYTHON_PATH = sys.executable
BASE_PATH = os.path.dirname(os.path.abspath(__file__))


def get_subprocess(file_with_args):
    sleep(0.2)
    script_name = f'{BASE_PATH}/tmp_{randint(10, 400)}_.sh'
    file_full_path = f"{PYTHON_PATH} {BASE_PATH}/{file_with_args}"

    with open(script_name, "w") as f:
        f.write(f'#!/bin/zsh\n{file_full_path}')
    os.chmod(script_name, 0o755)

    args = ['/usr/bin/open', '-n', '-a', 'Terminal.app', script_name]
    subprocess.Popen(args, shell=False, preexec_fn=os.setpgrp)
    sleep(1)
    os.remove(script_name)

    return


process = []
while True:
    TEXT_FOR_INPUT = "Выберите действие: q - выход, s - запустить сервер, c - клиенты, x - завершить работу: "
    action = input(TEXT_FOR_INPUT)

    if action == "q":
        break
    elif action == "s":

        get_subprocess("server.py")

    elif action == "c":
        for i in range(2):
            get_subprocess("client.py -m send")

        for i in range(2):
            get_subprocess("client.py -m listen")

    elif action == "x":
        sys.exit(1)