from src.midi_clock import MidiClock
from src.interfaces.midi_interface import MidiInterface
from src.recorder import Recorder
from src.interfaces.ethernet_interface.ethernet_interface import EthernetServerInterface
import src.interfaces.midi_interface.midi_data as midi_data
import time
import copy

LONG_PRESS_TIME = 0.1


class Rhythm(object):

    def __init__(
            self,
            usb_midi_interface=None,
            drum_pad_interface=None,
            midi_map=None,
            metronome_note=37,
            note_channel=9,
            control_channel=0,
            poly_pressure_heading=None,
            note_on_heading=None,
            note_off_heading=None,
            control_change_heading=None,
            note_on_feedback=None,
            host='0.0.0.0',
            port=5000
    ):

        # Place arguments
        self.usb_midi_interface = usb_midi_interface
        self.drum_pad_interface = drum_pad_interface
        self.midi_map = midi_map

        self.poly_pressure_heading = poly_pressure_heading
        self.note_on_heading = note_on_heading
        self.note_off_heading = note_off_heading
        self.control_change_heading = control_change_heading
        self.note_channel = note_channel
        self.control_channel = control_channel
        self.metronome_note = int(metronome_note)
        self.loud_metronome_message = [midi_data.NOTE_ON[self.note_channel], self.metronome_note, 110]
        self.weak_metronome_message = [midi_data.NOTE_ON[self.note_channel], self.metronome_note, 90]

        # Note on arrays to relate note loops with playing notes
        self.playing_notes = list(filter(lambda x: self.midi_map[self.note_on_heading][x]['function'] == 'note_on',
                                         self.midi_map[self.note_on_heading]))
        self.note_loops = list(filter(lambda x: self.midi_map[self.note_on_heading][x]['function'] == 'delete',
                                      self.midi_map[self.note_on_heading]))

        # INITIALIZE MIDI INTERFACES
        self.main_midi = MidiInterface(usb_midi_interface)
        self.main_midi = EthernetServerInterface(host=host, port=port)

        # Initialize drum pad.
        self.drum_pad = MidiInterface(drum_pad_interface)

        # INITIALIZE MIDI CLOCK
        self.clock = MidiClock(120)

        # INITIALIZE RECORDER
        self.recorder = Recorder(self.playing_notes, self.note_loops)

        # REFERENCE TO EXTERNAL PACKAGES METHODS
        self.timer = time.perf_counter

        # INITIALIZE PARAMETERS
        self.is_recording = False
        # Notes to play quantized on next note 16th
        self.next_note_16th_buffer = {}
        # Notes to be appended to previous note 16th
        self.last_note_16th_buffer = {}
        # Note on feedback
        self.note_on_feedback = eval(note_on_feedback)
        # Feedback notes buffer
        self.feedback_note_buffer = {}
        # Current notes on
        self.current_notes_lighted = {}
        # Notes to play on current clock event
        self.notes_to_play_now = {}
        # Pressed notes
        self.pressed_notes = {}
        # Pressed presets
        self.pressed_presets = {}
        # Control of main loop execution
        self.is_running = True
        # Control during play
        self.is_play = 0
        # Metronome activation control
        self.is_metronome = False
        # Triplets activation control
        self.is_triplets = False
        # Current clock event position within a bar, from step 1 to 96 (0 before start).
        self.clock_event_position = 1
        # Quantity of the current groove pattern to be applied.
        self.groove = 0
        # Max and min bpm to be controlled by user.
        self.max_bpm = 160
        self.min_bpm = 60
        # Interface state
        self.interface_state = {}
        # Saved presets
        self.saved_presets = {}
        self.current_playing_preset = None
        self.metronome_lighted = False
        # Note Mutes
        self.note_mutes = {key: False for key in range(36, 52)}

    def main_loop(self):
        """
        This method is the main loop and sequences all the steps to be executed by the instrument in order, either when
        the state is play or not.
        :return: None
        """

        # Enter main loop
        while self.is_running:

            # Get tick for current instant
            tick = self.clock.get_tick()

            # If tick is not None, process tick event for this tick count
            if tick:
                if self.is_play == 2:
                    self.main_midi.send([midi_data.SONG_START])
                    self.is_play = 1
                elif self.is_play == 1:
                    self.main_midi.send([midi_data.TIMING_CLOCK])

                self.process_tick_event(tick)

            # Get midi inputs
            midi_message = self.drum_pad.receive()

            if midi_message:
                # Get interactions
                interaction = self.get_interaction_from_midi_message(midi_message)
                # Process interaction
                self.process_interaction(interaction, midi_message, tick)

    def process_interaction(self, interaction, midi_message, tick):
        """
        This method process every user interaction received by the pad midi interface. Interactions can be notes on/off,
        control change and poly pressure channel on each individual note.
        :param interaction: External interaction value
        :param midi_message: Midi message.
        :return: None
        """

        # If the input is not none and has a meaning...
        if interaction:
            # Note on messages mapped to a note_on interaction type, are quantized to the next 16th note by placing
            # every note interaction to the note 16th buffer. At the same time, the same midi message is placed to the
            # pressed_notes dictionary to operate related long press functionalities.
            if interaction['function'] == 'note_on':
                note = midi_message[1]
                self.pressed_notes[note] = midi_message

                # Quantization: place note in next or last 16th note depending on current tick value.
                if tick % 6 == 1 or tick == 2:
                    self.last_note_16th_buffer[note] = midi_message
                else:
                    self.next_note_16th_buffer[note] = midi_message

            # Play stop switch the play state to the opposite.
            elif interaction['function'] == 'play_stop':
                self.play_stop()
            elif interaction['function'] == 'play_stop_feedback':
                self.play_stop_feedback()

            # A note off interaction is meant to be a release for the long press functionalities, since note_on
            # interactions manage their own note off midi messages.
            elif interaction['function'] == 'note_off':
                note = midi_message[1]
                self.pressed_notes[note] = 0
                self.pressed_notes.pop(note)

                self.note_mutes[note] = False


            # Pressure interactions are used to perform triplets on the note with the same id of the pressure message.
            elif interaction['function'] == 'pressure':
                note = midi_message[1]
                self.pressed_notes[note] = midi_message

            # Delete interaction removes if exists the entire corresponding note loop playing in that moment.
            elif interaction['function'] == 'delete':
                self.recorder.delete_loop(midi_message[1])

            # A loop pressed mark a time to the pressed pad and will count the time elapsed until its release.
            elif interaction['function'] == 'loop_pressed':
                self.pressed_presets[midi_message[1]] = self.timer()

            # A loop release count the time since the pad was pressed, if the time is longer than LONG_PRESS_TIME, all
            # current playing loops are stored under the corresponding preset key. If the time is shorter, the preset
            # starts to play.
            elif interaction['function'] == 'loop_released':
                note = midi_message[1]
                if self.timer() - self.pressed_presets.pop(note) < LONG_PRESS_TIME:
                    self.recorder.play_preset(note)
                    if note in self.saved_presets:
                        if self.current_playing_preset:
                            self.preset_saved_feedback(self.current_playing_preset)
                        self.current_playing_preset = note
                else:
                    self.recorder.save_preset(note)
                    self.preset_saved_feedback(note)
                    self.saved_presets[note] = True
                    if self.current_playing_preset:
                        self.preset_saved_feedback(self.current_playing_preset)
                    self.current_playing_preset = note

            # switch_recording interaction switch the recording state between on/off.
            elif interaction['function'] == 'switch_recording':
                self.switch_recording()
            elif interaction['function'] == 'switch_recording_feedback':
                self.switch_recording_feedback()

            # Switch metronome alternates between metronome on/off.
            elif interaction['function'] == 'switch_metronome':
                self.switch_metronome()
            elif interaction['function'] == 'switch_metronome_feedback':
                self.switch_metronome_feedback()

            # Switch triplets alternates between metronome on/off.
            elif interaction['function'] == 'switch_triplets':
                self.switch_triplets()

            elif interaction['function'] == 'switch_triplets_feedback':
                self.switch_triplets_feedback()

            # Set new bpm
            elif interaction['function'] == 'tempo':
                self.set_bpm(midi_message[2])

    def process_tick_event(self, tick_count):
        """
        This function is executed every time a clock midi event occurs, either for external or internal sync.
        :return: None
        """

        # If metronome is active will play the note, loud or weak depending on the tick value (first beat of bar or not)
        if tick_count % 24 == 1:
            if self.is_metronome:
                if tick_count == 1:
                    self.main_midi.send(self.loud_metronome_message)
                else:
                    self.main_midi.send(self.weak_metronome_message)

            # Lighting synchronized with metronome
            self.process_metronome_feedback_on()
            self.metronome_lighted = True

        # If the tick corresponds to a 16th note
        if tick_count % 6 == 1:
            self.process_midi_16th_note_event()

        # If th tick corresponds to a triplet note
        if tick_count % 4 == 1 and self.is_triplets:
            self.metronome_lighted = True
            self.process_midi_16th_3_note_event()

        # If recording state is active or not...
        if self.is_recording:
            self.notes_to_play_now.update(
                self.recorder.set_rec_get_play(tick_count, self.notes_to_play_now, self.last_note_16th_buffer))
        else:
            self.notes_to_play_now.update(self.recorder.set_rec_get_play(tick_count, {}, {}))

        # Add notes played closer to last note 16th
        self.process_last_16th_notes()

        # Process notes to play now
        self.process_notes_to_play_now()

        if tick_count % 24 == 2:
            self.process_metronome_feedback_off()

    def get_interaction_from_midi_message(self, midi_message):
        """
        Checks whether an input midi message corresponds to a instrument function using the interaction map.
        :param midi_message:
        :return: Function/None
        """
        if midi_message:
            heading = midi_message[0]

            if heading in self.midi_map.keys():
                id = midi_message[1]

                if id in self.midi_map[heading]:
                    return self.midi_map[heading][id]

            else:
                return None

    def process_notes_to_play_now(self):
        """
        Last action to be processed every clock event. Notes in notes_to_play_now come from recorder or instant playing
        and are sent together every time clock event.
        :return: None
        """
        notes = list(self.notes_to_play_now)
        current_notes_lighted = copy.deepcopy(self.current_notes_lighted)
        self.current_notes_lighted = {}

        # Send notes on
        for note in notes:
            midi_message = self.notes_to_play_now.pop(note)

            if not self.note_mutes[note]:
                self.main_midi.send(midi_message)
                self.main_midi.send([midi_data.NOTE_ON[self.note_channel], note, 0])

            # If device support note on feedback, turn note light on
            if self.note_on_feedback:
                self.drum_pad.send(midi_message)
                self.current_notes_lighted[midi_message[1]] = midi_message

            if not self.is_triplets and note in self.pressed_notes:
                self.note_mutes[note] = True

        # Turn previous lighted notes off
        for note in current_notes_lighted:
            self.drum_pad.send([midi_data.NOTE_ON[self.note_channel], note, 0])

    def process_midi_16th_3_note_event(self):
        """
        When the clock time corresponds to a 16th, notes quantized to be played in this note are placed to the buffer
        self.notes_to_play_now.
        :return: None
        """
        notes = self.pressed_notes.keys()
        for note in notes:
            message = self.pressed_notes[note]
            if message[0] == midi_data.POLY_PRESSURE[self.note_channel]:
                self.notes_to_play_now.update({note: [midi_data.NOTE_ON[self.note_channel], note, message[2]]})

    def process_midi_16th_note_event(self):
        """
        When the clock time corresponds to a 16th, notes quantized to be played in this note are placed to the buffer
        self.notes_to_play_now.
        :return: None
        """
        self.notes_to_play_now.update(self.next_note_16th_buffer)
        self.next_note_16th_buffer = {}

    def process_last_16th_notes(self):
        """
        When the clock time corresponds to a 16th, notes quantized to be played in this note are placed to the buffer
        self.notes_to_play_now.
        :return: None
        """
        self.notes_to_play_now.update(self.last_note_16th_buffer)
        self.last_note_16th_buffer = {}

    def set_bpm(self, value):
        """
        This method adjust the input value from the corresponding midi control change to the bpm range and sets it to
        the midi clock.
        :param value: value between 0 and 127
        :return: None
        """
        # Adjust control change range to bpm range
        bpm = int(self.min_bpm + value * (self.max_bpm - self.min_bpm) / 127.)
        self.clock.set_bpm(bpm)

    def play_stop(self):
        if self.is_play:
            self.is_play = 0
            self.main_midi.send([midi_data.SONG_STOP])
            self.clock.stop()
        elif not self.is_play:
            self.is_play = 2
            self.clock.start()

    def switch_recording(self):
        if self.is_recording:
            self.is_recording = False
        else:
            self.is_recording = True

    def switch_triplets(self):
        if self.is_triplets:
            self.is_triplets = False
        else:
            self.is_triplets = True

    def switch_metronome(self):
        if self.is_metronome:
            self.is_metronome = False
        else:
            self.is_metronome = True

    def play_stop_feedback(self):
        if self.is_play:
            self.set_feedback('play_stop', 'on')
        elif not self.is_play:
            self.set_feedback('play_stop', 'off')

    def switch_recording_feedback(self):
        if self.is_recording:
            self.set_feedback('switch_recording', 'on')
        else:
            self.set_feedback('switch_recording', 'off')

    def switch_triplets_feedback(self):
        if self.is_triplets:
            self.set_feedback('switch_triplets', 'on')
        else:
            self.set_feedback('switch_triplets', 'off')

    def switch_metronome_feedback(self):
        if self.is_metronome:
            self.set_feedback('switch_metronome', 'on')
        else:
            self.set_feedback('switch_metronome', 'off')

    def set_feedback(self, key, state):
        feedback_message = self.midi_map['feedback_functions'][key][state]
        self.drum_pad.send(feedback_message)

    def preset_saved_feedback(self, note):
        feedback_message = self.midi_map['feedback_functions']['preset_saved'][note]
        self.drum_pad.send(feedback_message)

    def process_metronome_feedback_on(self):
        if self.current_playing_preset:
            self.drum_pad.send([153, self.current_playing_preset, 127])

    def process_metronome_feedback_off(self):
        if self.current_playing_preset:
            self.drum_pad.send([153, self.current_playing_preset, 0])

