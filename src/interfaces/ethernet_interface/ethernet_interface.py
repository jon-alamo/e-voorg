import socket


class EthernetOutputInterface:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.queue = []

    def send(self, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(str(message).encode(), (self.host, self.port))

    def enqueue(self, midi_message):
        self.queue.append(midi_message)

    def enqueue_many(self, midi_messages):
        self.queue.extend(midi_messages)

    def send_first(self):
        self.send(self.queue.pop(0))

    def is_empty(self):
        return self.queue == []


class EthernetInputInterface:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.buffer_size = 1024

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        self.sock.bind((self.host, self.port))
        self.sock.settimeout(0.001)

    def receive(self):

        try:
            data, address = self.sock.recvfrom(self.buffer_size)
            return eval(data.decode())

        except socket.timeout:
            return None
