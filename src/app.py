from src.interfaces.midi_interface.midi_interface import MidiInterface
from src.controller.controller import Controller
from src.interfaces.footswitch_interface.footswitch_interface import FootSwitch
from src.view.view import View
from src.recorder.recorder import Recorder
from src.interfaces.midi_interface.midi_data import SONG_START, SONG_STOP, TIMING_CLOCK
from src.midi_clock.midi_clock import MidiClock
from src.interfaces.ethernet_interface.ethernet_interface import EthernetOutputInterface
import time


class App:

    def __init__(self, controller, midi_interface, controller_map, viewer_map, ethernet_port, ethernet_ip):

        # Interfaces initialization
        self.control_interface = MidiInterface(
            controller['midi_in'],
            controller['midi_out'],
            'control_interface'
        )
        self.view_interface = self.control_interface
        self.controller = Controller(self.control_interface, controller_map)
        self.view = View(self.view_interface, viewer_map)

        # Recorder
        self.channels = controller_map.channels
        self.memory_clips = controller_map.memory_clips
        self.recorder = Recorder(
            channels=self.channels,
            memory_clips=self.memory_clips,
            combine_channels=True
        )

        # Midi out interface
        self.midi_out_interface = MidiInterface(
            midi_interface['midi_in'],
            midi_interface['midi_out'],
            'midi_out_interface'
        )

        # Midi clock
        self.midi_clock = MidiClock(bpm=100)

        # Midi out ethernet interface
        self.eth_out = EthernetOutputInterface(host=ethernet_ip, port=ethernet_port)

        # Footswitch controller
        self.footswitch = FootSwitch()

        # Parameters
        self.is_play = False
        self.is_triplets = False
        self.pressed_notes = {}
        self.triplet_notes = {}
        self.channel_pressure = 0

        self.is_rec = False
        self.is_tick = True
        self.tick = 1

        # External tick parameters
        self.ext_tick = 1
        self.t0_ext_tick_24 = None

    def loop(self):
        """
        Main loop applications, determines the execution flow of the program step by step determining in which processes
        will be executed.
        :return: None
        """
        while True:

            # Controller's input user interactions.
            control_interaction = self.controller.get_interaction()
            # Footswitch (keyboard)'s input user interactions.
            footswitch_interaction = self.footswitch.get_interaction()

            if self.is_play:
                # Get tick from internal clock or none if the current time doesn't correspond to a tick event.
                tick = self.midi_clock.get_tick()

                if tick:
                    # Update tick values and flags, and send external sync messages.
                    self.tick_event()

            if control_interaction:
                # Execute function due to input device interaction
                self.exec_control(control_interaction)
                # Send feedback to control interface.
                self.view.draw_feedback(control_interaction)

            if footswitch_interaction:
                # Execute funtion due to footswitch interaction
                self.exec_control(footswitch_interaction)
                # Send feedback to control interface.
                self.view.draw_feedback(footswitch_interaction)

            if self.is_tick:
                # Execute time-synced processes
                self.process_tick()
                # Get quantized notes being played by saved loops or from real time playing.
                notes_to_play = self.recorder.get_quantized_notes(self.tick)
                # Enqueue notes to be sent to midi out interface
                self.midi_out_interface.enqueue_many(notes_to_play)
                # Enqueue notes to be sent to ethernet out interface
                self.eth_out.enqueue_many(notes_to_play)
                # Display note on/off feedback
                self.view.notes_feedback(notes_to_play)
                # Set is_tick flag to False
                self.is_tick = False

            # Flush buffers and send midi messages to corresponding out interfaces, or sleep if buffers are empty.
            self.flush_buffers()

    def flush_buffers(self):
        """
        This method releases one single midi event from any of the midi interfaces with a certain priority. USB midi
        interface is the one in charge of sending midi notes produced by the code so it has highest priority. Harmony
        interface receive midi events (notes and controls) to visual feedback so it have the lowest priority.
        :return:
        """

        # If USB midi interface has pending midi events to be released
        if not self.midi_out_interface.is_empty() or not self.eth_out.is_empty():

            if not self.midi_out_interface.is_empty():
                self.midi_out_interface.send_first()
            if not self.eth_out.is_empty():
                self.eth_out.send_first()

        # Otherwise, if harmony has pending midi events to be released
        elif not self.view_interface.is_empty():
            self.view_interface.send_first()

        # If no messages in buffers and still enough time to next tick, sleep to reduce process time
        elif (self.midi_clock.tick_time - 0.005) > (self.midi_clock.timer() - self.midi_clock.t0) or not self.is_play:
            time.sleep(0.001)

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
        """
        Process note on event from device and sends if play is active to recorder object. Every note on is tracked in
        self.pressed_notes parameter to be used in other places of the code.
        :param message: Midi message with channel, note and velocity.
        :return: None
        """
        # todo: not compatiblewith kompo since channels are not the same in kompo and evoorg. Set index as constant.
        self.pressed_notes[message[1]] = message
        self.recorder.channels_to_mute[message[1]] = False

        if self.is_play:
            self.recorder.rec_quantized_note(
                current_tick=self.tick,
                event_to_rec_on_tick=message,
                channel=message[1]
            )

        else:
            self.midi_out_interface.enqueue(message)
            self.eth_out.enqueue(message)

    def note_off(self, message):
        """
        Process note off event from device and sends if play is active to recorder object. Corresponding note is removed
        from self.pressed_notes and from self.triplet_notes.
        :param message: Midi message with channel, note and velocity.
        :return: None
        """
        # Remove from triplet notes
        self.pressed_notes.pop(message[1], None)
        self.triplet_notes.pop(message[1], None)
        self.recorder.channels_to_mute.pop(message[1], None)

        if self.is_play:
            self.recorder.rec_quantized_note(
                current_tick=self.tick,
                event_to_rec_on_tick=message,
                channel=message[1],
                tick_offset=3
            )

        else:
            self.midi_out_interface.enqueue(message)
            self.eth_out.enqueue(message)

    def set_channel_pressure(self, message):
        """
        Set pressure value coming from any note pad pressed.
        :param message: Pressure message from device.
        :return: None
        """
        self.channel_pressure = message[1]

    def tick_event(self):
        """
        This method is called every time the execution time coincides with a tick clock event. Here, the tick counter
        is updated and self.is_tick flag set to let the execution entering corresponding processes. External devices
        sync messages are sent from here too.
        :return: None
        """
        self.tick = self.tick % 96 + 1
        self.is_tick = True

        # Send sync messages
        self.eth_out.send([TIMING_CLOCK])
        self.midi_out_interface.send([TIMING_CLOCK])

    def process_tick(self):
        """
        Here are performed actions sensitives to time sync, such as triplets functionality and tempo depending flickers.
        :return: None
        """

        if self.tick % 24 == 1:
            self.view.time_sync_feedback_on()
        elif self.tick % 24 == 3:
            self.view.time_sync_feedback_off()

        if self.is_triplets:
            triplets_entry = self.tick % 12
            if triplets_entry == 0 or triplets_entry == 10 or triplets_entry == 11 or triplets_entry == 1 or triplets_entry == 2:
                self.triplet_notes.update(self.pressed_notes)

            if self.tick % 4 == 1:
                for triplet_note in self.triplet_notes:
                    self.recorder.rec_quantized_note(
                        current_tick=self.tick,
                        event_to_rec_on_tick=(153, triplet_note, self.channel_pressure),
                        channel=triplet_note,
                        quantization=24
                    )

                    self.recorder.rec_quantized_note(
                        current_tick=self.tick,
                        event_to_rec_on_tick=(137, triplet_note, 0),
                        channel=triplet_note,
                        quantization=24,
                        tick_offset=2
                    )

        else:
            mute_entry = self.tick % 6

    def internal_play_stop(self):
        """
        Switches play and stop modes. Function to be called by a non toggle button (momentary button).
        :return: None
        """

        if self.is_play:
            self.stop()
        else:
            self.play()

    def stop(self):
        """
        Stops internal play and sends corresponding midi messages through both midi and ethernet interfaces.
        :return: None
        """
        self.is_play = False

        self.eth_out.send([SONG_STOP])
        self.midi_out_interface.send([SONG_STOP])

        self.midi_clock.stop()
        self.view.stop()

    def play(self):
        """
        Set internal play and sends corresponding midi messages through both midi and ethernet interfaces.
        :return: None
        """
        self.tick = 1
        self.ext_tick = 1
        self.is_play = True
        self.midi_clock.start()

        self.eth_out.send([SONG_START])
        self.midi_out_interface.send([SONG_START])

        self.view.play()

    def set_rec_on_off(self):
        """
        Switches rec mode on/off. Function to be called by a non toggle button (momentary button).
        :return: None
        """

        if self.is_rec:
            self.set_rec(state='off')
        else:
            self.set_rec(state='on')

    def set_rec(self, state):
        """
        Set rec to state mode on/off and calls to corresponding recording objects methods.
        :param state: String on/off
        :return: None
        """
        if state == 'on':
            self.is_rec = True
            self.recorder.is_recording = True

        elif state == 'off':
            self.is_rec = False
            self.recorder.leave_recording()

    def set_global_rec(self, state):
        """
        Set rec to state mode on/off by calling set_rec methods after sending corresponding value through ethernet to
        perform same action on listening devics.
        :param state: String on/off
        :return: None
        """
        if state == 'on':
            message = [176, 120, 127]
            self.eth_out.send(message)

        elif state == 'off':
            message = [176, 120, 0]
            self.eth_out.send(message)

        self.set_rec(state)

    def increase_bpm(self, message):
        """
        Transforms and applies a factor to midi CC message value and call to midi_clock.increase_bpm:
            - Transformations:
                Values between 64 and 127 corresponds to negative values: value - 128
                Values between 1 and 64 corresponds to positive values: value
            - Factor applied to all transformed values: 0.1

        :param message: Midi CC message
        :return: None
        """
        value = message[2]
        if value > 64:
            delta = (float(value) - 128) * 0.1
        else:
            delta = float(value) * 0.1

        self.midi_clock.increase_bpm(delta)

    def external_tick(self):
        """
        If a external midi sync message is received, this method is called, so time is stored every note 4th and bpm of
        the internal clock is recalculated, but clock is always internal.
        :return: None
        """
        self.ext_tick = self.ext_tick % 96 + 1

        if self.ext_tick % 24 == 1:
            t_now = time.time()

            # If previous note 4th stored, new bpm is calculated.
            if self.t0_ext_tick_24:
                t_24 = t_now - self.t0_ext_tick_24
                bpm = 60. / t_24
                self.midi_clock.set_bpm(bpm)

            self.t0_ext_tick_24 = t_now

    def set_triplets_on_off(self):
        """
        Switches triplets mode on/off. Function to be called by a non toggle button (momentary button).
        :return: None
        """
        if self.is_triplets:
            self.set_triplets('off')
        else:
            self.set_triplets('on')

    def set_triplets(self, state):
        """
        Sets triplets mode to indicated state. When triplets is active, pressed notes will be played at 24th note,
        :param state:
        :return:
        """
        if state == 'on':
            self.is_triplets = True
        elif state == 'off':
            self.is_triplets = False

    def save_clip(self, message):
        self.recorder.save_preset(self.channels, message[1])

    def play_clip(self, message):
        self.recorder.play_channel_clip(self.channels, message[1])

    def delete_clip(self, message):
        self.recorder.delete_channel_clip(self.channels, message[1])

    def delete_note(self, message):
        self.recorder.delete_current_loop(channel=message[1])
