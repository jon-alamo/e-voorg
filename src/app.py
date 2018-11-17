from src.interfaces.midi_interface.midi_interface import MidiInterface
from src.controller.controller import Controller
from src.controller.controller_maps.mpd232 import controller_map
from src.view.view import View
from src.view.view_maps.mpd232 import view_map
from src.recorder.recorder import Recorder
import time


class App:

    def __init__(self, control_interface_name, midi_out_interface_name, is_external_clock=True):

        # Interfaces initialization
        self.control_interface = MidiInterface(control_interface_name, control_interface_name, 'control_interface')
        self.view_interface = self.control_interface

        self.controller = Controller(self.control_interface, controller_map)
        self.view = View(self.view_interface, view_map)

        # Recorder
        channels = list(range(36, 100))
        memory_clips = list(range(36, 100))
        self.recorder = Recorder(channels=channels, memory_clips=memory_clips, combine_channels=True)

        # Midi out interface
        self.midi_out_interface = MidiInterface(None, midi_out_interface_name, 'midi_out_interface')

        # Parameters
        self.is_play = False
        self.is_rec = False
        self.is_tick = True
        self.is_external_clock = is_external_clock
        self.tick = 1
        self.channels = range(36, 100)

    def loop(self):

        while True:

            control_interaction = self.controller.get_interaction()

            if control_interaction:
                # Execute function
                self.exec_control(control_interaction)
                # Send feedback to harmony interface
                self.view.draw_feedback(control_interaction)

            if self.is_tick:
                notes_to_play = self.recorder.get_quantized_notes(self.tick)
                self.midi_out_interface.enqueue_many(notes_to_play)
                self.is_tick = False

            self.flush_buffers()

    def flush_buffers(self):
        """
        This method releases one single midi event from any of the midi interfaces with a certain priority. USB midi
        interface is the one in charge of sending midi notes produced by the code so it has highest priority. Harmony
        interface receive midi events (notes and controls) to visual feedback so it have the lowest priority.
        :return:
        """

        # If USB midi interface has pending midi events to be released
        if not self.midi_out_interface.is_empty():
            self.midi_out_interface.send_first()

        # Otherwise, if harmony has pending midi events to be released
        elif not self.view_interface.is_empty():
            self.view_interface.send_first()

    def exec_control(self, control):
        """
        This method provide bindings between functionalities and user interactions coming from harmony interface, passed
        by harmony_input. To make binding between a functionality and the harmony interface, harmony input must contain
        the name of an existing method in this class and a dictionary with all the arguments of the method.

        :param control: Dictionary with mandatory keys 'fcn' and 'kwargs'. fcn value should be a name of any of
        the methods in this class in order to be used from harmony interface. kwargs must coincide with the arguments
        the that method.

        :return: None
        """
        # Functionality to be handled from harmony interface --> name of a method from this class
        functionality = control['fcn']
        # Keyword arguments to be passed to the method
        kwargs = control['kwargs']

        # If the fcn name passed matches with a method from this class
        if hasattr(self, functionality):
            # Get local reference to the method
            fcn = getattr(self, functionality)

            # Call the method with keyword arguments
            fcn(**kwargs)

    def note_on(self, message):

        if self.is_play:
            self.recorder.rec_quantized_note(
                current_tick=self.tick,
                event_to_rec_on_tick=message,
                channel=message[1]
            )

        else:
            self.midi_out_interface.enqueue(message)

    def note_off(self, message):

        if self.is_play:
            self.recorder.rec_quantized_note(
                current_tick=self.tick,
                event_to_rec_on_tick=message,
                channel=message[1],
                tick_offset=1
            )

        else:
            self.midi_out_interface.enqueue(message)

    def external_tick(self):
        self.tick = self.tick % 96 + 1
        self.is_tick = True

    def stop(self):
        self.is_play = False

    def play(self):
        self.tick = 1
        self.is_play = True

    def set_rec_on_off(self):
        self.is_rec = bool(abs(self.is_rec) - 1)

        if self.is_rec:
            self.recorder.is_recording = True
        else:
            self.recorder.leave_recording()

    def cc(self, message):
        pass

    def set_tripplets_on_off(self):
        pass

    def save_clip(self, message):
        self.recorder.save_preset(self.channels, message[1])

    def play_clip(self, message):
        self.recorder.play_channel_clip(self.channels, message[1])

    def delete_clip(self, message):
        self.recorder.delete_channel_clip(self.channels, message[1])

    def delete_note(self, message):
        self.recorder.delete_current_loop(channel=message[1])


if __name__ == '__main__':
    app = App('MPD232', 'MIDIOUT3')
    app.loop()
