
channels = [channel for channel in range(36, 48)]
channels.extend([channel for channel in range(52, 64)])
memory_clips = [clip for clip in range(68, 80)]

colors = {
    'on': 127,
    'off': 0
}

view_map = {
    'note_on': {
        key: {'midi_address': 153, 'color': colors['on'], 'view': 'default_view'} for key in channels
    },
    'note_off': {
        key: {'midi_address': 153, 'color': colors['off'], 'view': 'default_view'} for key in channels
    },
    'clip_on': {
        key: {'midi_address': 153, 'color': colors['on'], 'view': 'default_view'} for key in memory_clips
    },
    'clip_off': {
        key: {'midi_address': 153, 'color': colors['off'], 'view': 'default_view'} for key in memory_clips
    },
    'play': {
        51: {'midi_address': 153, 'color': colors['on'], 'view': 'default_view'},
        67: {'midi_address': 153, 'color': colors['on'], 'view': 'default_view'},
        83: {'midi_address': 153, 'color': colors['on'], 'view': 'default_view'},
    },
    'stop': {
        51: {'midi_address': 153, 'color': colors['off'], 'view': 'default_view'},
        67: {'midi_address': 153, 'color': colors['off'], 'view': 'default_view'},
        83: {'midi_address': 153, 'color': colors['off'], 'view': 'default_view'},
    },
    'rec_on': {
        50: {'midi_address': 153, 'color': colors['on'], 'view': 'default_view'},
        66: {'midi_address': 153, 'color': colors['on'], 'view': 'default_view'},
        82: {'midi_address': 153, 'color': colors['on'], 'view': 'default_view'},
    },
    'rec_off': {
        50: {'midi_address': 153, 'color': colors['off'], 'view': 'default_view'},
        66: {'midi_address': 153, 'color': colors['off'], 'view': 'default_view'},
        82: {'midi_address': 153, 'color': colors['off'], 'view': 'default_view'},
    },
    'delete_mode': {
        49: {'midi_address': 153, 'color': colors['on'], 'view': 'default_view'},
        65: {'midi_address': 153, 'color': colors['on'], 'view': 'default_view'},
        81: {'midi_address': 153, 'color': colors['on'], 'view': 'default_view'},
    },
    'default_mode': {
        49: {'midi_address': 153, 'color': colors['off'], 'view': 'default_view'},
        65: {'midi_address': 153, 'color': colors['off'], 'view': 'default_view'},
        81: {'midi_address': 153, 'color': colors['off'], 'view': 'default_view'},
    },
    'triplets_button_on': {
        48: {'midi_address': 176, 'color': colors['on'], 'view': 'default_view'},
        64: {'midi_address': 176, 'color': colors['on'], 'view': 'default_view'},
        80: {'midi_address': 176, 'color': colors['on'], 'view': 'default_view'},
    },
    'triplets_button_off': {
        48: {'midi_address': 176, 'color': colors['off'], 'view': 'default_view'},
        64: {'midi_address': 176, 'color': colors['off'], 'view': 'default_view'},
        80: {'midi_address': 176, 'color': colors['off'], 'view': 'default_view'},
    }
}
