import socket
import threading
import json
import struct
from bubenis_network import *

connections = []

# создаем сокет
sock = socket.socket()
# выбираем ip по-умолчанию и порт 9090 (можно и другой)
sock.bind(('', 9070))
# максимальное количество ожидающих подключений
sock.listen(50)
# ждем, пока к нам кто то подключится

clients = {}


def action(message, conn):
    global clients
    print(clients.get(conn))
    if "id" in message:
        clients[conn] = message["id"]
    if clients[conn] == "ADMIN":
        print(clients)
        for conn in clients:
            if clients[conn] != "ADMIN":
                try:
                    send_string(conn, message["message"])
                except Exception as e:
                    print("1No", e)
        try:
            send_string(conn, "recived")
        except Exception as e:
            print("2No", e)
            del clients[conn]


def process_client(conn):
    try:
        while True:
            data = receive_json(conn)
            action(data, conn)
    except Exception as e:
        print(e)
        print("error check")


while True:
    conn, addr = sock.accept()
    clients[conn] = '-1'
    try:
        threading.Thread(target=process_client, args=[conn]).start()
    except:
        print("error")
