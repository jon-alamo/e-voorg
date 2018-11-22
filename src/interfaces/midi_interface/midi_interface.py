import rtmidi
import time


SLEEP_AFTER_NOTE_OFF_BUFFER_FLUSH = 0.001
SLEEP_AFTER_NOTE_ON_BUFFER_FLUSH = 0.001
SLEEP_TIME = 0.001


class MidiInterface(object):

    def __init__(self, input_device_name, output_device_name, name=''):

        # Save name
        self.name = name

        self.input_device_name = input_device_name
        self.output_device_name = output_device_name

        if self.output_device_name:
            # print('self.output_device_name: {output_device_name}'.format(output_device_name=self.output_device_name))
            self.midi_out = rtmidi.MidiOut()
            # I/O Midi ports to work with in this interfafe.
            self.output_port = self.search_device(self.output_device_name, self.midi_out)
            # Open ports
            self.midi_out.open_port(self.output_port)

        if self.input_device_name:
            # print('self.input_device_name: {input_device_name}'.format(input_device_name=self.input_device_name))
            self.midi_in = rtmidi.MidiIn()
            self.input_port = self.search_device(self.input_device_name, self.midi_in)
            # Ignore types in midi_in
            self.midi_in.ignore_types(True, False, True)
            self.midi_in.open_port(self.input_port)

        # Midi queue
        self.queue = []

    @staticmethod
    def search_device(device_name, interface):
        """
        Search the device name in the I/O interface and returns the integer id of the port.
        :param device_name: Midi device name to look for.
        :param interface: Midi interface I/O to look for device name port.
        :return: Port id or False
        """
        available_ports = interface.get_ports()
        # print('Available midi ports: {}'.format(available_ports))

        for port_index in range(len(available_ports)):
            if device_name in available_ports[port_index]:
                # print(device_name)
                return port_index

        return False

    def receive(self):
        """
        Receive input midi messages and store them in the midi_in_buffer dictionary.
        :return: None
        """
        message = self.midi_in.get_message()
        if message:
            return tuple(message[0])

    def send(self, midi_message):
        """
        Sends input midi message to the output.
        :param midi_message: Message list to be sent like [heading, value...]
        :return: None
        """
        message = self.midi_out.send_message(midi_message)

    def enqueue(self, midi_message):
        self.queue.append(midi_message)

    def enqueue_many(self, midi_messages):
        self.queue.extend(midi_messages)

    def send_first(self):
        self.send(self.queue.pop(0))

    def is_empty(self):
        return self.queue == []


def get_devices():
    midi_out = rtmidi.MidiOut()
    midi_in = rtmidi.MidiIn()

    midi_devices = {
        'midi_out': midi_out.get_ports(),
        'midi_in': midi_in.get_ports()
    }

    return midi_devices


if __name__ == '__main__':
    m = MidiInterface('MPD218', 'MPD218')

    while True:
        msg = m.receive()

        if msg:
            print(msg)