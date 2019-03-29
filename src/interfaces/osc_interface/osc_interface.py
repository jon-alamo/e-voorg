import socket
from src.interfaces.midi_interface.midi_data import NOTE_ON, NOTE_OFF, SONG_START, SONG_STOP, TIMING_CLOCK
from pythonosc.osc_message import OscMessage
from pythonosc.osc_message_builder import OscMessageBuilder


class OscOutput:
    MIDI_ADDRESS = '/midi'

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.queue = []
        self.channels_queue = {channel: [] for channel in range(16)}

        self.notes_on = NOTE_ON
        self.notes_off = NOTE_OFF

    def send(self, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        osc_message = self.build_osc_message(message)
        sock.sendto(osc_message, (self.host, self.port))

    def build_osc_message(self, message):

        osc_message = OscMessageBuilder(self.MIDI_ADDRESS)

        for value in message:
            osc_message.add_arg(value)

        return osc_message.build().dgram

    def enqueue(self, midi_message):
        self.queue.append(midi_message)

    def enqueue_many(self, midi_messages):
        self.queue.extend(midi_messages)

    def send_first(self):
        self.send(self.queue.pop(0))

    def enqueue_many_channel(self, channel, midi_messages):
        self.channels_queue[channel].extend(midi_messages)

    def send_first_channel(self, channel):
        message = list(self.channels_queue[channel].pop(0))

        if message[0] in NOTE_ON:
            message[0] = self.notes_on[channel]
        elif message[0] in NOTE_OFF:
            message[0] = self.notes_off[channel]

        self.send(tuple(message))

    def is_channel_empty(self, channel):
        return self.channels_queue[channel] == []

    def is_empty(self):
        return self.queue == []


class OscInput:

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
            osc_msg = OscMessage(data)
            return tuple(osc_msg.params)

        except socket.timeout:
            return None


if __name__ == '__main__':
    o = OscInput('localhost', 5555)

    while True:
        msg = o.receive()
        if msg:
            print(msg)