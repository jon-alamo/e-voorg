from src.view.view_maps.mpd232 import colors

class View:

    def __init__(self, view_interface, view_map):
        self.interface = view_interface
        self.view_map = view_map
        self.colors = colors

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

    def draw_state(self, state):
        midi_map = self.view_map[state]['midi_map']
        value = self.view_map[state]['color']
        msg = (midi_map[0], midi_map[1], value)
        self.interface.enqueue(msg)

    def set_view(self, view):
        print(view)
        if view == 'clips_view':
            self.view_map['clips_view_button']['color'] = colors['on']
            self.view_map['default_view_button']['color'] = colors['off']
        elif view == 'default_view':
            self.view_map['default_view_button']['color'] = colors['on']
            self.view_map['clips_view_button']['color'] = colors['off']

        self.draw_state('clips_view_button')
        self.draw_state('default_view_button')

        for state in filter(lambda x: self.view_map[x]['view'] == view, self.view_map):
            self.draw_state(state)

    def switch_mode(self, mode):
        self.default_mode = mode
        if self.view_map[mode]['color'] == colors['off']:
            self.view_map[mode]['color'] = colors['on']
        else:
            self.view_map[mode]['color'] = colors['off']

        self.draw_state(mode)

    def set_tripplets_on_off(self):
        if self.view_map['tripplets']['color'] == colors['off']:
            self.view_map['tripplets']['color'] = colors['on']
        else:
            self.view_map['tripplets']['color'] = colors['off']

        self.draw_state('tripplets')

    def set_rec_on_off(self):
        if self.view_map['rec_mode']['color'] == colors['off']:
            self.view_map['rec_mode']['color'] = colors['on']
        else:
            self.view_map['rec_mode']['color'] = colors['off']

        self.draw_state('rec_mode')

    def play_clip(self, message):
        print(f'play_clip: {message}')

    def delete_clip(self, message):
        print(f'delete_clip: {message}')

    def save_clip(self, message):
        print(f'save_clip: {message}')