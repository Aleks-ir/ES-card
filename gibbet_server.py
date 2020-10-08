
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
import socket
class Server:



    def send_result(self, result, sender):
        for s in set(self.connections):
            if s != sender:
                s.send(bytes(result, "utf-8"))

    def count_result(self, first_message, second_message):
        if first_message == second_message:
            self.send_result('DRAW' + '_' + first_message, self.first_sender)
            self.send_result('DRAW' + '_' + second_message, self.second_sender)
        elif first_message == 'EMPEROR' and second_message == 'SLAVE':
            self.send_result('WIN' + '_' + first_message, self.first_sender)
            self.send_result('DEFEAT' + '_' + second_message, self.second_sender)
        elif first_message == 'SLAVE' and second_message == 'EMPEROR':
            self.send_result('DEFEAT' + '_' + first_message, self.first_sender)
            self.send_result('WIN' + '_' + second_message, self.second_sender)
        elif first_message == 'CITIZER' and second_message == 'SLAVE' or first_message == 'EMPEROR' and second_message == 'CITIZER':
            self.send_result('DEFEAT' + '_' + first_message, self.first_sender)
            self.send_result('WIN' + '_' + second_message, self.second_sender)
        elif first_message == 'SLAVE' and second_message == 'CITIZER' or first_message == 'CITIZER' and second_message == 'EMPEROR':
            self.send_result('WIN' + '_' + first_message, self.first_sender)
            self.send_result('DEFEAT' + '_' + second_message, self.second_sender)
        self.del_data()

    def del_data(self):
        self.first_sender = None
        self.second_sender = None
        self.array_messages.clear()

    def save_data(self, sender, message):
        self.array_messages.append(message)
        if len(self.array_messages) == 1:
            self.first_sender = sender
            self.send_result("WAIT", sender)
        elif len(self.array_messages) == 2:
            self.second_sender = sender
            self.count_result(self.array_messages[0], self.array_messages[1])

    def sender(self, server, q):
        while self.run:
            try:
                sender, message = q.get(timeout=1)
                if sender != self.first_sender:
                    self.save_data(sender, message)
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
        if len(self.connections) == 1:
            type_game = settings.type_game
        else:
            type_game = 'Emperor' if settings.type_game == 'Slave' else 'Slave'
        message = "connected" + '_' + type_game + '_' + str(settings.count_round) + '_' + settings.mode_game
        client.send(bytes(message, "utf-8"))

    def send_start_info(self, connections):
        for s in set(connections):
            s.send(bytes("START", "utf-8"))

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
                if len(connections) < 2:
                    self.connect(client, connections, q)
                    self.send_settings(client)
                    if len(connections) == 2:
                        self.send_start_info(connections)
                else:
                    client.send(bytes("no_connected", "utf-8"))





    def __init__(self):
        self.OS_NAME = platform.system()

        HOST = socket.gethostbyname(socket.gethostname())
        PORT = 1080

        self.first_sender = None
        self.second_sender = None
        self.run = True
        print('Запуск...')
        q = queue.Queue()
        self.connections = []
        self.array_messages = []
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