import json
import socket
import struct
import threading
from bubenis_network import *
import io
import sys


def init_command(name):
    return {
        "id": name,
        "message": "init"
    }


def done_command(name):
    return {
        "id": name,
        "message": "done!"
    }


# Функция выполнения задачи
def execute_task(task):
    # Redirect stdout to a StringIO object
    output = io.StringIO()
    sys.stdout = output
    print(task)
    try:
        # Execute the script code
        exec(task)
    except Exception as e:
        # Print the exception if an error occurs
        print(e)

    # Restore stdout and get the captured output
    sys.stdout = sys.__stdout__
    result = output.getvalue()
    output.close()

    return result


name = "2"
while True:
    while True:
        try:
            print("try to connect")
            sock = socket.socket()
            sock.connect(('127.0.0.1', 9070))
            break
        except ConnectionRefusedError:
            print("Connection error")

    print("Connect!")
    cmd = init_command(name)
    send_json(sock, cmd)
    print(f"Login as {name}")
    # print(cmd)

    while True:
        data = receive_string(sock)
        print(f"get text {data}")

        result = (
            execute_task(data))

        try:
            send_json(sock, done_command(name))
        except:
            print("exiting")
            sock.close()
            break
