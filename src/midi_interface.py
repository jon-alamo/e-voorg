import rtmidi
import time
import src.midi_data as midi_data
import threading

SLEEP_AFTER_NOTE_OFF_BUFFER_FLUSH = 0.001
SLEEP_AFTER_NOTE_ON_BUFFER_FLUSH = 0.001
SLEEP_TIME = 0.001


class MidiInterface(object):

    def __init__(self, device_name):

        # Midi ports initialization
        self.midi_out = rtmidi.MidiOut()
        self.midi_in = rtmidi.MidiIn()

        # I/O Midi ports to work with in this interfafe.
        self.output_port = self.search_device(device_name, self.midi_out)
        self.input_port = self.search_device(device_name, self.midi_in)

        # Ignore types in midi_in
        self.midi_in.ignore_types(True, False, True)

        # Open ports
        self.midi_out.open_port(self.output_port)
        self.midi_in.open_port(self.input_port)

        # Midi note off buffer
        self.midi_buffer = {}

    @staticmethod
    def search_device(device_name, interface):
        """
        Search the device name in the I/O interface and returns the integer id of the port.
        :param device_name: Midi device name to look for.
        :param interface: Midi interface I/O to look for device name port.
        :return: Port id or False
        """
        available_ports = interface.get_ports()
        print('Available midi ports: {}'.format(available_ports))

        for port_index in range(len(available_ports)):
            if device_name in available_ports[port_index]:
                return port_index

        return False

    def play_notes(self, notes, velocity, channel):
        """
        Append notes to the note on. All note off queries are grouped together and sent at once every midi
        clock event if the buffer is not empty.
        :param notes: List of note numbers to play.
        :param velocity: Velocity to apply to all the notes (0 - 127)
        :param channel: Channel where the notes will be played
        :return: None
        """
        for note_on in notes:
            if midi_data.MIN_NOTE < note_on < midi_data.MAX_NOTE:
                note_on_message = [midi_data.NOTE_ON[channel], note_on, velocity]
                self.note_on_buffer[(channel, note_on)] = note_on_message

    def release_notes(self, notes, channel):
        """
        Append notes to the note off buffer. All note off queries are grouped together and sent at once every midi
        clock event if the buffer is not empty.
        :param notes: List of note numbers to release.
        :param channel: Integer of channel number (0 - 15)
        :return: None
        """
        for note_off in notes:
            if midi_data.MIN_NOTE < note_off < midi_data.MAX_NOTE:
                note_off_message = [midi_data.NOTE_ON[channel], note_off, 0]
                self.note_off_buffer[(channel, note_off)] = note_off_message

    def control_change(self, control_change, value, channel):
        """
        Append control changes to the control change buffer. All contorl change queries are grouped together and
        sent at once every midi clock event if the buffer is not empty.
        :param control_change: Midi control change id.
        :param value: Midi control change value (0 - 127)
        :param channel: Midi control change channel (0xB0 - 0xBF)
        :return: None
        """
        control_change_message = [midi_data.CONTROL_CHANGE[channel], control_change, value]
        self.control_change_buffer[(channel, control_change)] = control_change_message
        # self.midi_out.send_message(midi_message)

    def pitch_bend(self, value, channel):
        self.pitch_bend_buffer[224] = [midi_data.PITCH_BEND[channel], 0, value]

    def flush_note_on_buffer(self):
        """
        Sends midi notes in note on buffer and remove from buffer.
        :return: None
        """
        self.flush_midi_buffer(self.note_on_buffer)
        # This sleep lets the midi driver finish processing all note releases. Otherwise, some messages may be lost.
        # time.sleep(self.SLEEP_AFTER_NOTE_ON_BUFFER_FLUSH)

    def flush_note_off_buffer(self):
        """
        Sends midi notes in release notes buffer and remove from buffer.
        :return: None
        """
        self.flush_midi_buffer(self.note_off_buffer)
        # This sleep lets the midi driver finish processing all note releases. Otherwise, some messages may be lost.
        time.sleep(self.SLEEP_AFTER_NOTE_OFF_BUFFER_FLUSH)

    def flush_control_change_buffer(self):
        """
        Sends control changes in buffer and remove from buffer.
        :return: None
        """
        self.flush_midi_buffer(self.control_change_buffer)

    def flush_pitch_bend_buffer(self):
        self.flush_midi_buffer(self.pitch_bend_buffer)

    def flush_midi_buffer(self, buffer_key='instant'):
        """
        Flush any base midi buffer stored in this interface like: {key1: midi_message_1, key2:midi_message_2}
        :param midi_buffer: Dictionary of any key and midi_messages like { key: [channel, control/note, value]}
        :return: None
        """
        for key in self.midi_buffer[buffer_key]:
            self.midi_out.send_message(self.midi_buffer.pop(key))

    def receive(self):
        """
        Receive input midi messages and store them in the midi_in_buffer dictionary.
        :return: None
        """
        message = self.midi_in.get_message()
        if message:
            return message[0]

    def receive_thread(self):
        """
        Receive input midi messages and store them in the midi_in_buffer dictionary.
        :return: None
        """
        while True:
            message = self.midi_in.get_message()
            if message:
                if len(message[0]) == 1:
                    self.midi_in_buffer[(message[0][0],)] = message[0]
                elif len(message[0]) > 1:
                    self.midi_in_buffer[tuple(message[0][:2])] = message[0]

    def get_midi_in_buffer_keys(self):
        """
        Returns stored keys in midi_in dictionary. The keys represent the first or two first elments of a midi message.
        :return: List of midi_in_buffer keys.
        """
        return self.midi_in_buffer.keys()

    def get_midi_in_buffer_message(self, key):
        """
        Return the message associated to a midi_in_buffer key.
        :param key: Tuple that is key of the dictionary midi_in_buffer
        :return: Midi message if the passed key exists or None.
        """
        if key in self.midi_in_buffer:
            return self.midi_in_buffer.pop(key)
        else:
            return None

    def get_all_midi_in_buffer(self):
        """
        Return and removes the midi_in_buffer by returning the whole dictionary.
        :return: Dictionary with all midi_in_buffer data.
        """
        buffer = self.midi_in_buffer
        self.midi_in_buffer = {}
        return buffer

    def send(self, midi_message):
        """
        Sends input midi message to the output.
        :param midi_message: Message list to be sent like [heading, value...]
        :return: None
        """
        message = self.midi_out.send_message(midi_message)


if __name__ == '__main__':
    midi = MidiInterface('Launchpad')
    b = []

