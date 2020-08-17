
'''
import queue
import socket
import threading


class Server:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('localhost', 1080))
        self.sock.listen(2)
        self.queue = queue.SimpleQueue()
        threading.Thread(target=self.sender).start()

    def sender(self):
        while True:
            connection, address = self.sock.accept()
            print("new connection from {address}".format(address=address))

            data = connection.recv(1024).decode('utf-8')
            
            #self.list.append(data.decode('utf-8'),address)

            connection.send(bytes('Hello from server!', encoding='UTF-8'))

            if self.queue.empty():
                self.queue.put((data, connection))
            else:
                pl_1_ = self.queue.get()
                pl_2_ = (data, connection)
                if pl_1_[0] == pl_2_[0]:
                    pl_1_[1].send(bytes("DRAW", encoding='UTF-8'))
                    pl_2_[1].send(bytes("DRAW", encoding='UTF-8'))

                elif pl_1_[0] == 'EMPEROR' and pl_2_[0] == 'SLAVE':
                    pl_1_[1].send(bytes("WIN", encoding='UTF-8'))
                    pl_2_[1].send(bytes("DEFEAT", encoding='UTF-8'))
                #connection.close()
'''
import time

import settings

'''
import queue
import threading
import socketserver


class GibbetHandler(socketserver.BaseRequestHandler):

    def handle(self,cor):
        if self.cor.empty():
            self.data = self.request.recv(1024).decode()
            print("Клиент {} сообщает: {}".format(self.client_address[1], self.data))
            cor = ((self.client_address[1], self.data))
            #self.request.sendall(bytes(self.data, "utf-8"))
        else:
            self.data = self.request.recv(1024).decode()
            print('sds')


class Server:
    def __init__(self):
        HOST = 'localhost'
        PORT = 1080
        server = socketserver.TCPServer((HOST, PORT), GibbetHandler)
        print("Сервер запущен")
        self.cor = queue.Queue()
        threading.Thread(target=server.serve_forever, args=self.cor).start()
'''

import socket
import threading
import queue
import platform
# Определяем константу содержащую имя ОС
# для учёта особенностей данной операционной системы
from gibbet_client import Client
import socket
class Server:



    def send(self, first_mess, second_mess):
        self.first_player.send(bytes(first_mess, "utf-8"))
        self.second_player.send(bytes(second_mess, "utf-8"))

    def count_result(self, first_message, second_message):
        if first_message == second_message:
            self.send('DRAW', 'DRAW')
        elif first_message == 'EMPEROR' and second_message == 'SLAVE':
            self.send("DEFEAT", "WIN")
        elif first_message == 'SLAVE' and second_message == 'EMPEROR':
            self.send("WIN", "DEFEAT")
        elif first_message == 'SITIZER' and second_message == 'SLAVE' or first_message == 'EMPEROR' and second_message == 'SITIZER':
            self.send("WIN", "DEFEAT")
        elif first_message == 'SLAVE' and second_message == 'SITIZER' or first_message == 'SITIZER' and second_message == 'EMPEROR':
            self.send("DEFEAT", "WIN")

    def save_data(self, data):
        if self.is_first_message:
            self.first_player, self.first_message = data
            self.is_first_message = False
        else:
            self.second_player, self.second_message = data
            self.is_first_message = True
            self.count_result(self.first_message, self.second_message)

    def sender(self, server, q):
        while self.run:
            try:
                data = q.get(timeout=1)
                self.save_data(data)
            except queue.Empty:
                pass
        self.shutdown_socket(server)


    def shutdown_socket(self, s):
        if self.OS_NAME == 'Linux':
            s.shutdown(socket.SHUT_RDWR)
        s.close()

    def reciver(self, client, q):
        while self.run:
            try:
                data, addres = client.recvfrom(1024)
                if data:
                    q.put((client, data.decode()))
                    print('{} отправил: {}'.format(client.getpeername(), data.decode()))
            except:
                break
        client.close()

    def send_settings(self, client):
        message = "connected" + '_' + settings.type_game + '_' + str(settings.count_round)
        client.send(bytes(message, "utf-8"))

    def connect(self, client, connections, q):
        with threading.Lock():
            connections.append(client)
        threading.Thread(target=self.reciver, args=(client, q)).start()
        print('Подключено: ', len(connections))

    def accepter(self, server, connections, q):
        while self.run:
            try:
                client, addr = server.accept()
            except OSError as e:
                if (self.OS_NAME == 'Windows' and e.errno != 10038) or (self.OS_NAME == 'Linux' and e.errno != 22):
                    raise
            else:
                if len(connections) != 2:
                    self.connect(client, connections, q)
                    self.send_settings(client)
                else:
                    client.send(bytes("no", "utf-8"))




    def __init__(self):
        self.OS_NAME = platform.system()

        HOST = socket.gethostbyname(socket.gethostname())
        PORT = 1080

        self.run = True
        self.is_first_message = True
        print('Запуск...')
        q = queue.Queue()
        self.connections = []

        server = socket.socket()
        server.bind((HOST, PORT))
        server.listen(2)

        print(u'Сервер запущен на {}\n'.format(server.getsockname()))

        threading.Thread(target=self.accepter, args=(server, self.connections, q)).start()
        threading.Thread(target=self.sender, args=(server, q)).start()


    def stop(self):
        self.run = False
        for s in self.connections:
            self.shutdown_socket(s)