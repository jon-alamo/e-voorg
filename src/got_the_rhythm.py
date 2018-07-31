from src.midi_clock import MidiClock
from src.midi_interface import MidiInterface
from src.recorder import Recorder
import src.midi_data as midi_data
import time

LONG_PRESS_TIME = 0.1


class Rhythm(object):

    def __init__(self, usb_midi_interface=None, drum_pad_interface=None, midi_map=None,
                 metronome_note=37, note_channel=9, control_channel=0, poly_pressure_heading=None, note_on_heading=None,
                 note_off_heading=None, control_change_heading=None):

        # Place arguments
        self.usb_midi_interface = usb_midi_interface
        self.drum_pad_interface = drum_pad_interface
        self.midi_map = midi_map

        self.poly_pressure_heading = poly_pressure_heading
        self.note_on_heading = note_on_heading
        self.note_off_heading = note_off_heading
        self.contorl_change_heading = control_change_heading
        self.note_channel = note_channel
        self.control_channel = control_channel
        self.metronome_note = metronome_note
        self.loud_metronome_message = [self.note_channel, self.metronome_note, 110]
        self.weak_metronome_message = [self.note_channel, self.metronome_note, 90]

        # Note on arrays to relate note loops with playing notes
        self.playing_notes = list(filter(lambda x: self.midi_map[self.note_on_heading][x]['function'] == 'note_on',
                                         self.midi_map[self.note_on_heading]))
        self.note_loops = list(filter(lambda x: self.midi_map[self.note_on_heading][x]['function'] == 'delete',
                                      self.midi_map[self.note_on_heading]))

        # INITIALIZE MIDI INTERFACES
        self.main_midi = MidiInterface(usb_midi_interface)
        # Initialize drum pad.
        self.drum_pad = MidiInterface(drum_pad_interface)

        # INITIALIZE MIDI CLOCK
        self.clock = MidiClock(120)

        # INITIALIZE RECORDER
        self.recorder = Recorder(self.playing_notes)

        # REFERENCE TO EXTERNAL PACKAGES METHODS
        self.timer = time.perf_counter

        # INITIALIZE PARAMETERS
        self.is_recording = False
        # Notes to play quantized on next note 16th
        self.next_note_16th_buffer = {}
        # Notes to be appended to previous note 16th
        self.last_note_16th_buffer = {}
        # Interface state
        self.interface_state = {
            'play': False,
            'playing_preset': None,
            'saved_presets': [],
            'note_loop_with_notes': [],
            'metronome': False,
            'recording': False,
            'triplets': False
        }
        # Feedback notes buffer
        self.feedback_note_buffer = {}
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

            # Feedback
            self.send_feedback()

    def send_feedback(self):
        # Get remaining time to the next clock tick event
        remaining_time = self.clock.remaining_time()

        # If there is enough time and notes to be send back to drum pad interface
        if self.feedback_note_buffer and remaining_time > 0.0:
            feedback_max_actions = int(remaining_time * 1000)
            feedback_actions = 0

        feedback_actions = list(self.feedback_note_buffer.keys())

        for feedback_action in feedback_actions:
            feedback_value = self.feedback_note_buffer.pop(feedback_action)
            if feedback_action == 'play':
                self.drum_pad.send([self.note_on_heading, feedback_value])

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

            # A note off interaction is meant to be a release for the long press functionalities, since note_on
            # interactions manage their own note off midi messages.
            elif interaction['function'] == 'note_off':
                note = midi_message[1]
                self.pressed_notes[note] = 0
                self.pressed_notes.pop(note)

            # Pressure interactions are used to perform triplets on the note with the same id of the pressure message.
            elif interaction['function'] == 'pressure':
                note = midi_message[1]
                self.pressed_notes[note] = midi_message

            # Delete interaction removes if exists the entire corresponding note loop playing in that moment.
            elif interaction['function'] == 'delete':
                self.recorder.delete_loop(midi_message[1])
                self.feedback_note_buffer['delete_note_loop_with_notes'] = midi_message

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
                else:
                    self.recorder.save_preset(note)

            # switch_recording interaction switch the recording state between on/off.
            elif interaction['function'] == 'switch_recording':
                self.switch_recording()

            # Switch metronome alternates between metronome on/off.
            elif interaction['function'] == 'switch_metronome':
                self.switch_metronome()

            # Switch triplets alternates between metronome on/off.
            elif interaction['function'] == 'switch_triplets':
                self.switch_triplets()

    def process_tick_event(self, tick_count):
        """
        This function is executed every time a clock midi event occurs, either for external or internal sync.
        :return: None
        """

        # If metronome is active will play the note, loud or weak depending on the tick value (first beat of bar or not)
        if self.is_metronome and tick_count % 24 == 1:
            if tick_count == 1:
                self.main_midi.send(self.loud_metronome_message)
            else:
                self.main_midi.send([self.weak_metronome_message])

        # If the tick corresponds to a 16th note
        if tick_count % 6 == 1:
            self.process_midi_16th_note_event()

        # If th tick corresponds to a triplet note
        if tick_count % 4 == 1:
            self.process_midi_16th_3_note_event()

        # If recording state is active or not...
        if self.is_recording:
            self.notes_to_play_now.update(
                self.recorder.set_rec_get_play(tick_count, self.notes_to_play_now, self.last_note_16th_buffer))

            # Feedback buffer
            if 'note_loop_with_notes' in self.feedback_note_buffer:
                self.feedback_note_buffer['note_loop_with_notes'].extend(list(self.notes_to_play_now.keys())).extend(
                    list(self.last_note_16th_buffer.keys()))
            else:
                self.feedback_note_buffer['note_loop_with_notes'] = list(self.notes_to_play_now.keys()) + list(
                    self.last_note_16th_buffer.keys())

        else:
            self.notes_to_play_now.update(self.recorder.set_rec_get_play(tick_count, {}, {}))

        # Add notes played closer to last note 16th
        self.process_last_16th_notes()

        # Process notes to play now
        self.process_notes_to_play_now()

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

        # Send notes on
        for note in notes:
            midi_message = self.notes_to_play_now.pop(note)
            self.main_midi.send(midi_message)
            self.main_midi.send([midi_data.NOTE_ON[self.note_channel], note, 0])

        if 'notes' in self.feedback_note_buffer:
            self.feedback_note_buffer['notes'].extend(notes)
        else:
            self.feedback_note_buffer['notes'] = notes

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
        self.clock.set_bpm(value)

    def play_stop(self):
        if self.is_play:
            self.is_play = 0
            self.main_midi.send([midi_data.SONG_STOP])
            self.clock.stop()
            self.feedback_note_buffer['play'] = False
        elif not self.is_play:
            self.is_play = 2
            self.clock.start()
            self.feedback_note_buffer['play'] = True

    def switch_recording(self):
        if self.is_recording:
            self.is_recording = False
            self.feedback_note_buffer['recording'] = False
        else:
            self.is_recording = True
            self.feedback_note_buffer['recording'] = True

    def switch_triplets(self):
        if self.is_triplets:
            self.is_triplets = False
            self.feedback_note_buffer['triplets'] = False
        else:
            self.is_triplets = True
            self.feedback_note_buffer['triplets'] = True

    def switch_metronome(self):
        if self.is_metronome:
            self.is_metronome = False
            self.feedback_note_buffer['metronome'] = False
        else:
            self.is_metronome = True
            self.feedback_note_buffer['metronome'] = True
