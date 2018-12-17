from src.interfaces.midi_interface.midi_interface import MidiInterface


class View:

    def __init__(self, view_interface: MidiInterface, viewer_map):
        self.interface = view_interface
        self.view_map = viewer_map.view_map
        self.colors = viewer_map.colors

        # Interface state
        self.clips = {key: False for key in viewer_map.memory_clips}
        self.current_clip = min(self.clips.keys())
        self.current_view = 'default_view'
        self.delete_mode = False
        self.is_rec = False
        self.is_triplets = False
        self.cue_state = 0

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
        if self.is_triplets:
            self.set_triplets('off')
        else:
            self.set_triplets('on')

    def set_triplets(self, state):
        if state == 'on':
            self.is_triplets = True
            self.draw_state('triplets_button_on')
        elif state == 'off':
            self.is_triplets = False
            self.draw_state('triplets_button_off')

    # def set_rec_on_off(self):
    #
    #     if self.is_rec:
    #         self.set_rec('off')
    #     else:
    #         self.set_rec('on')
    #
    # def set_global_rec(self, state):
    #     self.set_rec(state)

    # def set_rec(self, state):
    #     if state == 'on':
    #         self.is_rec = True
    #         self.draw_state('rec_on')
    #
    #     elif state == 'off':
    #         self.is_rec = False
    #         self.draw_state('rec_off')

    def play(self):
        self.draw_state('play')

    def stop(self):
        self.draw_state('stop')

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

        if self.current_clip and self.view_map['clip_on'][self.current_clip]['view'] == self.current_view:
            self.draw_state('clip_on', self.current_clip)

    def time_sync_feedback_off(self):

        if self.current_clip and self.view_map['clip_on'][self.current_clip]['view'] == self.current_view:
            self.draw_state('clip_off', self.current_clip)

    def note_8th_sync_feedback_on(self):
        if self.cue_state == 1:
            self.draw_state('cue_button_on')

    def note_16th_sync_feedback_off(self):
        if self.cue_state == 1:
            self.draw_state('cue_button_off')

    def set_cue_state(self, state):
        self.cue_state = state
        if state:
            self.draw_state('cue_button_on')
        else:
            self.draw_state('cue_button_off')
