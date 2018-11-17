import socket
UDP_IP = '0.0.0.0'
UDP_PORT = 5005


class EthernetServerInterface:

    def __init__(self, host, port):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.is_running = True
        self.socket.listen(1)
        self.note_4th = 1

    def send(self, message):
        connection, address = self.socket.accept()
        connection.send(str(message).encode())
