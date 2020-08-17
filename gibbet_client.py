import socket
from threading import Thread


class Client:

    def __init__(self):
        HOST = socket.gethostbyname(socket.gethostname())
        self.sock = socket.socket()
        self.sock.connect((HOST, 1080))
        self.data = ''
        #Thread(target=self.read_sock).start()

    def write_sock(self, mess):
        self.sock.send(mess.encode())

    def read_sock(self, exit=True):
        try:
            while exit:
                self.data = self.sock.recv(1024)
                print(self.data.decode('utf-8'))
                #time.sleep(0.2)
        except:
                pass
    def conected(self):
        return self.sock.recv(1024).decode('utf-8')

    def read(self):
        return self.sock.recv(1024).decode('utf-8')

    def close_sock(self):
        self.read_sock(False)
        self.sock.close()
