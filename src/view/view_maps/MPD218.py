
colors = {
    'on': 127,
    'off': 0
}

view_map = {
    'note_on': {
        key: {'midi_address': 153, 'color': colors['on'], 'view': 'clips_view'} for key in range(36, 48)
    },
    'note_off': {
        key: {'midi_address': 153, 'color': colors['off'], 'view': 'clips_view'} for key in range(36, 48)
    },
    'clip_on': {
        key: {'midi_address': 153, 'color': colors['on'], 'view': 'clips_view'} for key in range(52, 64)
    },
    'clip_off': {
        key: {'midi_address': 153, 'color': colors['off'], 'view': 'clips_view'} for key in range(52, 64)
    },
    'play': {
        51: {'midi_address': 153, 'color': colors['on'], 'view': 'always'},
        67: {'midi_address': 153, 'color': colors['on'], 'view': 'always'},
        83: {'midi_address': 153, 'color': colors['on'], 'view': 'always'},
    },
    'stop': {
        51: {'midi_address': 153, 'color': colors['off'], 'view': 'always'},
        67: {'midi_address': 153, 'color': colors['off'], 'view': 'always'},
        83: {'midi_address': 153, 'color': colors['off'], 'view': 'always'},
    },
    'rec_on': {
        50: {'midi_address': 153, 'color': colors['on'], 'view': 'always'},
        66: {'midi_address': 153, 'color': colors['on'], 'view': 'always'},
        82: {'midi_address': 153, 'color': colors['on'], 'view': 'always'},
    },
    'rec_off': {
        50: {'midi_address': 153, 'color': colors['off'], 'view': 'always'},
        66: {'midi_address': 153, 'color': colors['off'], 'view': 'always'},
        82: {'midi_address': 153, 'color': colors['off'], 'view': 'always'},
    },
    'delete_mode': {
        49: {'midi_address': 153, 'color': colors['on'], 'view': 'always'},
        65: {'midi_address': 153, 'color': colors['on'], 'view': 'always'},
        81: {'midi_address': 153, 'color': colors['on'], 'view': 'always'},
    },
    'default_mode': {
        49: {'midi_address': 153, 'color': colors['off'], 'view': 'always'},
        65: {'midi_address': 153, 'color': colors['off'], 'view': 'always'},
        81: {'midi_address': 153, 'color': colors['off'], 'view': 'always'},
    },
    'triplets_button_on': {
        48: {'midi_address': 176, 'color': colors['on'], 'view': 'always'},
        64: {'midi_address': 176, 'color': colors['on'], 'view': 'always'},
        80: {'midi_address': 176, 'color': colors['on'], 'view': 'always'},
    },
    'triplets_button_off': {
        48: {'midi_address': 176, 'color': colors['off'], 'view': 'always'},
        64: {'midi_address': 176, 'color': colors['off'], 'view': 'always'},
        80: {'midi_address': 176, 'color': colors['off'], 'view': 'always'},
    }
}
