channels = list(range(36, 48))
channels.extend(list(range(52, 64)))
memory_clips = [clip for clip in range(68, 80)]

controller_map = {

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

                68: {'set_waitfor_trigger': (137, 68, 0), 'wait_time': 0.5, 'time': None, 'long': {'fcn': 'save_clip'}, 'short': {'fcn': 'play_clip'}},
                69: {'set_waitfor_trigger': (137, 69, 0), 'wait_time': 0.5, 'time': None, 'long': {'fcn': 'save_clip'}, 'short': {'fcn': 'play_clip'}},
                70: {'set_waitfor_trigger': (137, 70, 0), 'wait_time': 0.5, 'time': None, 'long': {'fcn': 'save_clip'}, 'short': {'fcn': 'play_clip'}},
                71: {'set_waitfor_trigger': (137, 71, 0), 'wait_time': 0.5, 'time': None, 'long': {'fcn': 'save_clip'}, 'short': {'fcn': 'play_clip'}},
                72: {'set_waitfor_trigger': (137, 72, 0), 'wait_time': 0.5, 'time': None, 'long': {'fcn': 'save_clip'}, 'short': {'fcn': 'play_clip'}},
                73: {'set_waitfor_trigger': (137, 73, 0), 'wait_time': 0.5, 'time': None, 'long': {'fcn': 'save_clip'}, 'short': {'fcn': 'play_clip'}},
                74: {'set_waitfor_trigger': (137, 74, 0), 'wait_time': 0.5, 'time': None, 'long': {'fcn': 'save_clip'}, 'short': {'fcn': 'play_clip'}},
                75: {'set_waitfor_trigger': (137, 75, 0), 'wait_time': 0.5, 'time': None, 'long': {'fcn': 'save_clip'}, 'short': {'fcn': 'play_clip'}},
                76: {'set_waitfor_trigger': (137, 76, 0), 'wait_time': 0.5, 'time': None, 'long': {'fcn': 'save_clip'}, 'short': {'fcn': 'play_clip'}},
                77: {'set_waitfor_trigger': (137, 77, 0), 'wait_time': 0.5, 'time': None, 'long': {'fcn': 'save_clip'}, 'short': {'fcn': 'play_clip'}},
                78: {'set_waitfor_trigger': (137, 78, 0), 'wait_time': 0.5, 'time': None, 'long': {'fcn': 'save_clip'}, 'short': {'fcn': 'play_clip'}},
                79: {'set_waitfor_trigger': (137, 79, 0), 'wait_time': 0.5, 'time': None, 'long': {'fcn': 'save_clip'}, 'short': {'fcn': 'play_clip'}},

                50: {'set_waitfor_trigger': (137, 50, 0), 'wait_time': 0.5, 'time': None,
                     'short': {'fcn': 'change_cue_loop_status'}, 'long': {'fcn': 'remove_cue_loop'}},
                66: {'set_waitfor_trigger': (137, 66, 0), 'wait_time': 0.5, 'time': None,
                     'short': {'fcn': 'change_cue_loop_status'}, 'long': {'fcn': 'remove_cue_loop'}},
                82: {'set_waitfor_trigger': (137, 82, 0), 'wait_time': 0.5, 'time': None,
                     'short': {'fcn': 'change_cue_loop_status'}, 'long': {'fcn': 'remove_cue_loop'}},

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
                # 51: {'fcn': 'internal_play_stop', 'kwargs': {}},

                64: {'fcn': 'set_triplets_on_off', 'kwargs': {}},
                65: {'fcn': 'switch_mode', 'kwargs': {'mode': 'delete_mode'}},
                # 67: {'fcn': 'internal_play_stop', 'kwargs': {}},

                80: {'fcn': 'set_triplets_on_off', 'kwargs': {}},
                81: {'fcn': 'switch_mode', 'kwargs': {'mode': 'delete_mode'}},
                # 83: {'fcn': 'internal_play_stop', 'kwargs': {}},

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

                50: {'set_waitfor_trigger': (137, 50, 0), 'wait_time': 0.5, 'time': None,
                     'long': {'fcn': 'change_cue_loop_status'}, 'short': {'fcn': 'remove_cue_loop'}},
                66: {'set_waitfor_trigger': (137, 66, 0), 'wait_time': 0.5, 'time': None,
                     'long': {'fcn': 'change_cue_loop_status'}, 'short': {'fcn': 'remove_cue_loop'}},
                82: {'set_waitfor_trigger': (137, 82, 0), 'wait_time': 0.5, 'time': None,
                     'long': {'fcn': 'change_cue_loop_status'}, 'short': {'fcn': 'remove_cue_loop'}},

            },
            137: {
                48: {'fcn': 'set_triplets_on_off', 'kwargs': {}},
                49: {'fcn': 'switch_mode', 'kwargs': {'mode': 'default_mode', }},
                51: {'fcn': 'internal_play_stop', 'kwargs': {}},
                64: {'fcn': 'set_triplets_on_off', 'kwargs': {}},
                65: {'fcn': 'switch_mode', 'kwargs': {'mode': 'default_mode'}},
                67: {'fcn': 'internal_play_stop', 'kwargs': {}},
                80: {'fcn': 'set_triplets_on_off', 'kwargs': {}},
                81: {'fcn': 'switch_mode', 'kwargs': {'mode': 'default_mode'}},
                83: {'fcn': 'internal_play_stop', 'kwargs': {}},
            },
            176: {
                10: {'fcn': 'increase_bpm'}
            },
        }
    }
}
