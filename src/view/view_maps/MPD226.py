channels = [channel for channel in range(36, 100)]
memory_clips = [clip for clip in range(36, 100)]

colors = {
    'on': 127,
    'off': 0
}

view_map = {
    'note_on': {
        key: {'midi_address': 153, 'color': colors['on'], 'view': 'clips_view'} for key in range(36, 100)
    },
    'note_off': {
        key: {'midi_address': 153, 'color': colors['off'], 'view': 'clips_view'} for key in range(36, 100)
    },
    'clip_on': {
        key: {'midi_address': 153, 'color': colors['on'], 'view': 'clips_view'} for key in range(36, 100)
    },
    'clip_off': {
        key: {'midi_address': 153, 'color': colors['off'], 'view': 'clips_view'} for key in range(36, 100)
    },
    'rec_on': {
        28: {'midi_address': 176, 'color': colors['on'], 'view': 'always'},
    },
    'rec_off': {
        28: {'midi_address': 176, 'color': colors['off'], 'view': 'always'},
    },
    'delete_mode': {
        23: {'midi_address': 176, 'color': colors['on'], 'view': 'always'},
    },
    'default_mode': {
        23: {'midi_address': 176, 'color': colors['off'], 'view': 'always'},
    },
    'default_view': {
        21: {'midi_address': 176, 'color': colors['on'], 'view': 'always'},
        22: {'midi_address': 176, 'color': colors['off'], 'view': 'always'}
    },
    'clips_view': {
        21: {'midi_address': 176, 'color': colors['off'], 'view': 'always'},
        22: {'midi_address': 176, 'color': colors['on'], 'view': 'always'}
    },
    'triplets_button_on': {
        24: {'midi_address': 176, 'color': colors['on'], 'view': 'always'},
    },
    'triplets_button_off': {
        24: {'midi_address': 176, 'color': colors['on'], 'view': 'always'},
    },
    'cue_button_on': {
        25: {'midi_address': 176, 'color': colors['on'], 'view': 'always'},
    },
    'cue_button_off': {
        25: {'midi_address': 176, 'color': colors['off'], 'view': 'always'},
    },
    'hold_tempo_on': {
        26: {'midi_address': 176, 'color': colors['on'], 'view': 'always'},
    },
    'hold_tempo_off': {
        26: {'midi_address': 176, 'color': colors['off'], 'view': 'always'},
    },
    'play': {},
    'stop': {}
}
