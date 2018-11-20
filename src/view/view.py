from src.view.view_maps.mpd232 import colors
from src.interfaces.midi_interface.midi_interface import MidiInterface


class View:

    def __init__(self, view_interface: MidiInterface, view_map: dict):
        self.interface = view_interface
        self.view_map = view_map
        self.colors = colors

        # Interface state
        self.clips = {key: False for key in range(36, 100)}
        self.current_clip = 36
        self.current_view = 'default_view'
        self.delete_mode = False
        self.is_rec = False
        self.tiplets_mode = False

    def draw_feedback(self, control):

        # Functionality to be handled from harmony interface --> name of a method from this class
        method = control['fcn']
        # Keyword arguments to be passed to the method
        kwargs = control['kwargs']

        # If the fcn name passed matches with a method from this class
        if hasattr(self, method):
            # Get local reference to the method
            fcn = getattr(self, method)

            # Call the method with keyword arguments
            fcn(**kwargs)

    def draw_state(self, state, state_id=None):
        if state_id:
            address = self.view_map[state][state_id]['midi_address']
            value = self.view_map[state][state_id]['color']
            msg = (address, state_id, value)
            self.interface.enqueue(msg)

        else:
            for state_id in self.view_map[state]:
                address = self.view_map[state][state_id]['midi_address']
                value = self.view_map[state][state_id]['color']
                msg = (address, state_id, value)
                self.interface.enqueue(msg)

    def set_view(self, view):
        self.current_view = view
        self.draw_state(view)

        if self.current_view == 'default_view':
            self.draw_state('note_off')

        elif self.current_view == 'clips_view':
            for clip in self.clips:
                if self.clips[clip]:
                    self.draw_state('clip_on', clip)
                else:
                    self.draw_state('clip_off', clip)

    def switch_mode(self, mode):
        self.delete_mode = bool(abs(self.delete_mode - 1))
        if self.delete_mode:
            self.draw_state('delete_mode')
        else:
            self.draw_state('default_mode')

    def set_triplets_on_off(self):
        self.tiplets_mode = bool(abs(self.tiplets_mode - 1))
        if self.tiplets_mode:
            self.draw_state('triplets_button_on')
        else:
            self.draw_state('triplets_button_off')

    def set_rec_on_off(self):
        self.is_rec = bool(abs(self.is_rec - 1))
        if self.is_rec:
            self.draw_state('rec_on')
        else:
            self.draw_state('rec_off')

    def play_clip(self, message):

        if self.clips[self.current_clip]:
            self.draw_state('clip_on', self.current_clip)
        else:
            self.draw_state('clip_off', self.current_clip)

        self.current_clip = message[1]

    def notes_feedback(self, notes):
        if self.current_view == 'default_view':
            self.interface.enqueue_many(notes)

    def delete_clip(self, message):
        self.clips[message[1]] = False
        self.draw_state('clip_off', message[1])

    def save_clip(self, message):
        self.clips[message[1]] = True
        self.play_clip(message)

    def time_sync_feedback_on(self):

        if self.current_clip and self.current_view == 'clips_view':
            self.draw_state('clip_on', self.current_clip)

    def time_sync_feedback_off(self):

        if self.current_clip and self.current_view == 'clips_view':
            self.draw_state('clip_off', self.current_clip)
