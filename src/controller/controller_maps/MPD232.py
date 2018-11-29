channels = [channel for channel in range(36, 100)]
memory_clips = [clip for clip in range(36, 100)]


controller_map = {
    'waitfor': {
        137: {'long': {'fcn': 'save_clip'}, 'short': {'fcn': 'play_clip'}}
    },

    'default_view': {

        'default_mode': {
            153: {'fcn': 'note_on'},
            137: {'fcn': 'note_off'},
            248: {'fcn': 'external_tick', 'kwargs': {}},

            176: {
                21: {
                    0: {'fcn': 'set_view', 'kwargs': {'view': 'default_view'}}
                },
                22: {
                    0: {'fcn': 'set_view', 'kwargs': {'view': 'clips_view'}}
                },
                23: {
                    0: {'fcn': 'switch_mode', 'kwargs': {'mode': 'delete_mode'}}
                },
                24: {
                    0: {'fcn': 'set_tripplets_on_off', 'kwargs': {}}
                },
                117: {
                    127: {'fcn': 'stop', 'kwargs': {}}
                },
                118: {
                    127: {'fcn': 'play', 'kwargs': {}}
                },
                119: {
                    127: {'fcn': 'set_rec_on_off', 'kwargs': {}}
                },
                28: {
                    0: {'fcn': 'set_rec_on_off', 'kwargs': {}}
                },
                -1: {'fcn': 'cc'}
            }

        },

        'delete_mode': {
            248: {'fcn': 'external_tick', 'kwargs': {}},
            153: {'fcn': 'delete_note'},

            176: {
                21: {
                    0: {'fcn': 'set_view', 'kwargs': {'view': 'default_view'}}
                },
                22: {
                    0: {'fcn': 'set_view', 'kwargs': {'view': 'clips_view'}}
                },
                23: {
                    0: {'fcn': 'switch_mode', 'kwargs': {'mode': 'default_mode'}}
                },
                24: {
                    0: {'fcn': 'set_tripplets_on_off', 'kwargs': {}}
                },
                117: {
                    127: {'fcn': 'stop', 'kwargs': {}}
                },
                118: {
                    127: {'fcn': 'play', 'kwargs': {}}
                },
                -1: {'fcn': 'cc'}
            }
        }
    },

    'clips_view': {

        'default_mode': {
            248: {'fcn': 'external_tick', 'kwargs': {}},
            153: {'waitfor': 137, 'time': 0.5},

            176: {
                21: {
                    0: {'fcn': 'set_view', 'kwargs': {'view': 'default_view'}}
                },
                22: {
                    0: {'fcn': 'set_view', 'kwargs': {'view': 'clips_view'}}
                },
                23: {
                    0: {'fcn': 'switch_mode', 'kwargs': {'mode': 'delete_mode'}}
                },
                24: {
                    0: {'fcn': 'set_tripplets_on_off', 'kwargs': {}}
                },
                117: {
                    127: {'fcn': 'stop', 'kwargs': {}}
                },
                118: {
                    127: {'fcn': 'play', 'kwargs': {}}
                },
                119: {
                    127: {'fcn': 'set_rec_on_off', 'kwargs': {}}
                },
                28: {
                    0: {'fcn': 'set_rec_on_off', 'kwargs': {}}
                },
                -1: {'fcn': 'cc'}
            }
        },

        'delete_mode': {
            248: {'fcn': 'external_tick', 'kwargs': {}},
            153: {'fcn': 'delete_clip'},

            176: {
                21: {
                    0: {'fcn': 'set_view', 'kwargs': {'view': 'default_view'}}
                },
                22: {
                    0: {'fcn': 'set_view', 'kwargs': {'view': 'clips_view'}}
                },
                23: {
                    0: {'fcn': 'switch_mode', 'kwargs': {'mode': 'default_mode'}}
                },
                24: {
                    0: {'fcn': 'set_tripplets_on_off', 'kwargs': {}}
                },
                117: {
                    127: {'fcn': 'stop', 'kwargs': {}}
                },
                118: {
                    127: {'fcn': 'play', 'kwargs': {}}
                },
                -1: {'fcn': 'cc'}
            }
        }
    }
}
