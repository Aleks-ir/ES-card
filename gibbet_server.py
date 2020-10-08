import constants
import settings
import threading
import queue
import platform
import socket
class Server:



    def send_message(self, mess, sender):
        for s in set(self.connections):
            if s != sender:
                try:
                    s.send(bytes(mess, "utf-8"))
                except:
                    with threading.Lock():
                        self.connections.remove(s)

    def count_result(self, first_message, second_message):
        if first_message == second_message:
            self.send_message(constants.DRAW + '_' + first_message, self.first_sender)
            self.send_message(constants.DRAW + '_' + second_message, self.second_sender)
        elif first_message == constants.EMPEROR and second_message == constants.SLAVE:
            self.send_message(constants.WIN + '_' + first_message, self.first_sender)
            self.send_message(constants.DEFEAT + '_' + second_message, self.second_sender)
        elif first_message == constants.SLAVE and second_message == constants.EMPEROR:
            self.send_message(constants.DEFEAT + '_' + first_message, self.first_sender)
            self.send_message(constants.WIN + '_' + second_message, self.second_sender)
        elif first_message == constants.CITIZER and second_message == constants.SLAVE or first_message == constants.EMPEROR and second_message == constants.CITIZER:
            self.send_message(constants.DEFEAT + '_' + first_message, self.first_sender)
            self.send_message(constants.WIN + '_' + second_message, self.second_sender)
        elif first_message == constants.SLAVE and second_message == constants.CITIZER or first_message == constants.CITIZER and second_message == constants.EMPEROR:
            self.send_message(constants.WIN + '_' + first_message, self.first_sender)
            self.send_message(constants.DEFEAT + '_' + second_message, self.second_sender)
        self.del_data()

    def del_data(self):
        self.first_sender = None
        self.second_sender = None
        self.array_messages.clear()

    def save_data(self, sender, message):
        self.array_messages.append(message)
        if len(self.array_messages) == 1:
            self.first_sender = sender
            self.send_message(constants.WAIT, sender)
        elif len(self.array_messages) == 2:
            self.second_sender = sender
            self.count_result(self.array_messages[0], self.array_messages[1])

    def sender(self, server, q):
        while self.run:
            try:
                sender, message = q.get(timeout=1)
                if message == constants.SHUTDOWN:
                    self.send_message(message, sender)
                    self.shutdown_socket(server)
                    self.stop()
                elif sender != self.first_sender:
                    self.save_data(sender, message)
            except queue.Empty:
                pass

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
                    # print('{} отправил: {}'.format(client.getpeername(), data.decode()))
            except:
                break
        client.close()

    def send_settings(self, client):
        if len(self.connections) == 1:
            type_game = settings.type_game
        else:
            type_game = constants.EMPEROR if settings.type_game == constants.SLAVE else constants.SLAVE
        message = constants.CONNECTED + '_' + type_game + '_' + str(settings.count_round) + '_' + settings.mode_game
        client.send(bytes(message, "utf-8"))

    def send_start_info(self, connections):
        for s in set(connections):
            s.send(bytes(constants.START, "utf-8"))

    def connect(self, client, connections, q):
        with threading.Lock():
            connections.append(client)
        threading.Thread(target=self.reciver, args=(client, q)).start()
        # print('Подключено: ', len(connections))


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
                    client.send(bytes(constants.NO_CONNECTED, "utf-8"))





    def __init__(self):
        self.OS_NAME = platform.system()

        HOST = socket.gethostbyname(socket.gethostname())
        PORT = 1080

        self.first_sender = None
        self.second_sender = None
        self.run = True
        # print('Запуск...')
        q = queue.Queue()
        self.connections = []
        self.array_messages = []
        server = socket.socket()
        server.bind((HOST, PORT))
        server.listen(2)

        # print(u'Сервер запущен на {}\n'.format(server.getsockname()))

        threading.Thread(target=self.accepter, args=(server, self.connections, q)).start()
        threading.Thread(target=self.sender, args=(server, q)).start()


    def stop(self):
        self.run = False
        for s in self.connections:
            self.shutdown_socket(s)