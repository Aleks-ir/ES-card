import socket

class Client:

    def __init__(self, HOST):
        #HOST = socket.gethostbyname(socket.gethostname())
        self.sock = socket.socket()
        self.sock.connect((HOST, 1080))
        self.data = ''

    def write_sock(self, mess):
        self.sock.send(mess.encode())

    def read(self):
        return self.sock.recv(1024).decode('utf-8')

    def close_sock(self):
        self.sock.close()
