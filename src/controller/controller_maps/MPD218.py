
channels = [channel for channel in range(36, 48)]
channels.extend([channel for channel in range(52, 64)])
memory_clips = [clip for clip in range(68, 80)]

controller_map = {
    'waitfor': {
        137: {'long': {'fcn': 'save_clip'}, 'short': {'fcn': 'play_clip'}}
    },

    'default_view': {

        'default_mode': {
            153: {
                36: {'fcn': 'note_on'},
                37: {'fcn': 'note_on'},
                38: {'fcn': 'note_on'},
                39: {'fcn': 'note_on'},
                40: {'fcn': 'note_on'},
                41: {'fcn': 'note_on'},
                42: {'fcn': 'note_on'},
                43: {'fcn': 'note_on'},
                44: {'fcn': 'note_on'},
                45: {'fcn': 'note_on'},
                46: {'fcn': 'note_on'},
                47: {'fcn': 'note_on'},
                52: {'fcn': 'note_on'},
                53: {'fcn': 'note_on'},
                54: {'fcn': 'note_on'},
                55: {'fcn': 'note_on'},
                56: {'fcn': 'note_on'},
                57: {'fcn': 'note_on'},
                58: {'fcn': 'note_on'},
                59: {'fcn': 'note_on'},
                60: {'fcn': 'note_on'},
                61: {'fcn': 'note_on'},
                62: {'fcn': 'note_on'},
                63: {'fcn': 'note_on'},

                68: {'waitfor': 137, 'time': 0.5},
                69: {'waitfor': 137, 'time': 0.5},
                70: {'waitfor': 137, 'time': 0.5},
                71: {'waitfor': 137, 'time': 0.5},
                72: {'waitfor': 137, 'time': 0.5},
                73: {'waitfor': 137, 'time': 0.5},
                74: {'waitfor': 137, 'time': 0.5},
                75: {'waitfor': 137, 'time': 0.5},
                76: {'waitfor': 137, 'time': 0.5},
                77: {'waitfor': 137, 'time': 0.5},
                78: {'waitfor': 137, 'time': 0.5},
                79: {'waitfor': 137, 'time': 0.5},

            },

            217: {'fcn': 'set_channel_pressure'},

            137: {
                36: {'fcn': 'note_off'},
                37: {'fcn': 'note_off'},
                38: {'fcn': 'note_off'},
                39: {'fcn': 'note_off'},
                40: {'fcn': 'note_off'},
                41: {'fcn': 'note_off'},
                42: {'fcn': 'note_off'},
                43: {'fcn': 'note_off'},
                44: {'fcn': 'note_off'},
                45: {'fcn': 'note_off'},
                46: {'fcn': 'note_off'},
                47: {'fcn': 'note_off'},
                52: {'fcn': 'note_off'},
                53: {'fcn': 'note_off'},
                54: {'fcn': 'note_off'},
                55: {'fcn': 'note_off'},
                56: {'fcn': 'note_off'},
                57: {'fcn': 'note_off'},
                58: {'fcn': 'note_off'},
                59: {'fcn': 'note_off'},
                60: {'fcn': 'note_off'},
                61: {'fcn': 'note_off'},
                62: {'fcn': 'note_off'},
                63: {'fcn': 'note_off'},

                48: {'fcn': 'set_triplets_on_off', 'kwargs': {}},
                49: {'fcn': 'switch_mode', 'kwargs': {'mode': 'delete_mode'}},
                50: {'fcn': 'set_rec_on_off', 'kwargs': {}},
                51: {'fcn': 'internal_play_stop', 'kwargs': {}},

                64: {'fcn': 'set_triplets_on_off', 'kwargs': {}},
                65: {'fcn': 'switch_mode', 'kwargs': {'mode': 'delete_mode'}},
                66: {'fcn': 'set_rec_on_off', 'kwargs': {}},
                67: {'fcn': 'internal_play_stop', 'kwargs': {}},

                80: {'fcn': 'set_triplets_on_off', 'kwargs': {}},
                81: {'fcn': 'switch_mode', 'kwargs': {'mode': 'delete_mode'}},
                82: {'fcn': 'set_rec_on_off', 'kwargs': {}},
                83: {'fcn': 'internal_play_stop', 'kwargs': {}},

            },

            176: {
                10: {'fcn': 'increase_bpm'}
            },

        },
        'delete_mode': {
            153: {
                36: {'fcn': 'delete_note'},
                37: {'fcn': 'delete_note'},
                38: {'fcn': 'delete_note'},
                39: {'fcn': 'delete_note'},
                40: {'fcn': 'delete_note'},
                41: {'fcn': 'delete_note'},
                42: {'fcn': 'delete_note'},
                43: {'fcn': 'delete_note'},
                44: {'fcn': 'delete_note'},
                45: {'fcn': 'delete_note'},
                46: {'fcn': 'delete_note'},
                47: {'fcn': 'delete_note'},

                52: {'fcn': 'delete_note'},
                53: {'fcn': 'delete_note'},
                54: {'fcn': 'delete_note'},
                55: {'fcn': 'delete_note'},
                56: {'fcn': 'delete_note'},
                57: {'fcn': 'delete_note'},
                58: {'fcn': 'delete_note'},
                59: {'fcn': 'delete_note'},
                60: {'fcn': 'delete_note'},
                61: {'fcn': 'delete_note'},
                62: {'fcn': 'delete_note'},
                63: {'fcn': 'delete_note'},

                68: {'fcn': 'delete_clip'},
                69: {'fcn': 'delete_clip'},
                70: {'fcn': 'delete_clip'},
                71: {'fcn': 'delete_clip'},
                72: {'fcn': 'delete_clip'},
                73: {'fcn': 'delete_clip'},
                74: {'fcn': 'delete_clip'},
                75: {'fcn': 'delete_clip'},
                76: {'fcn': 'delete_clip'},
                77: {'fcn': 'delete_clip'},
                78: {'fcn': 'delete_clip'},
                79: {'fcn': 'delete_clip'},

            },
            137: {
                48: {'fcn': 'set_triplets_on_off', 'kwargs': {}},
                49: {'fcn': 'switch_mode', 'kwargs': {'mode': 'default_mode'}},
                50: {'fcn': 'set_rec_on_off', 'kwargs': {}},
                51: {'fcn': 'internal_play_stop', 'kwargs': {}},

                64: {'fcn': 'set_triplets_on_off', 'kwargs': {}},
                65: {'fcn': 'switch_mode', 'kwargs': {'mode': 'default_mode'}},
                66: {'fcn': 'set_rec_on_off', 'kwargs': {}},
                67: {'fcn': 'internal_play_stop', 'kwargs': {}},

                80: {'fcn': 'set_triplets_on_off', 'kwargs': {}},
                81: {'fcn': 'switch_mode', 'kwargs': {'mode': 'default_mode'}},
                82: {'fcn': 'set_rec_on_off', 'kwargs': {}},
                83: {'fcn': 'internal_play_stop', 'kwargs': {}},
            },
            176: {
                10: {'fcn': 'increase_bpm'}
            },
        }
    }
}
