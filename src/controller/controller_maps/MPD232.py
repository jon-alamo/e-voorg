channels = [channel for channel in range(36, 100)]
memory_clips = [clip for clip in range(36, 100)]


controller_map = {

    'default_view': {

        'default_mode': {
            153: {'fcn': 'note_on'},
            137: {'fcn': 'note_off'},
            # 248: {'fcn': 'external_tick', 'kwargs': {}},
            217: {'fcn': 'set_channel_pressure'},

            176: {
                8: {'fcn': 'increase_bpm'},
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
                    0: {'fcn': 'set_triplets_on_off', 'kwargs': {}}
                },
                25: {
                    127: {'set_waitfor_trigger': (176, 25, 0), 'wait_time': 0.5, 'time': None,
                     'short': {'fcn': 'change_cue_loop_status'}, 'long': {'fcn': 'remove_cue_loop'}},
                },
                26: {
                    0: {'fcn': 'set_hold_tempo_on_off', 'kwargs': {}}
                },
                # 117: {
                #     127: {'fcn': 'stop', 'kwargs': {}}
                # },
                # 118: {
                #     127: {'fcn': 'play', 'kwargs': {}}
                # },
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
            # 248: {'fcn': 'external_tick', 'kwargs': {}},
            153: {'fcn': 'delete_note'},

            176: {
                8: {'fcn': 'increase_bpm'},
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
                    0: {'fcn': 'set_triplets_on_off', 'kwargs': {}}
                },
                25: {
                    127: {'set_waitfor_trigger': (176, 25, 0), 'wait_time': 0.5, 'time': None,
                          'short': {'fcn': 'change_cue_loop_status'}, 'long': {'fcn': 'remove_cue_loop'}},
                },
                26: {
                    0: {'fcn': 'set_hold_tempo_on_off', 'kwargs': {}}
                },
                # 117: {
                #     127: {'fcn': 'stop', 'kwargs': {}}
                # },
                # 118: {
                #     127: {'fcn': 'play', 'kwargs': {}}
                # },
                -1: {'fcn': 'cc'}
            }
        }
    },

    'clips_view': {

        'default_mode': {
            # 248: {'fcn': 'external_tick', 'kwargs': {}},
            153: {
                channel: {'set_waitfor_trigger': (137, channel, 0), 'wait_time': 0.5, 'time': None, 'long': {'fcn': 'save_clip'}, 'short': {'fcn': 'play_clip'}} for channel in channels
            },
            176: {
                8: {'fcn': 'increase_bpm'},
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
                    0: {'fcn': 'set_triplets_on_off', 'kwargs': {}}
                },
                25: {
                    127: {'set_waitfor_trigger': (176, 25, 0), 'wait_time': 0.5, 'time': None,
                          'short': {'fcn': 'change_cue_loop_status'}, 'long': {'fcn': 'remove_cue_loop'}},
                },
                26: {
                    0: {'fcn': 'set_hold_tempo_on_off', 'kwargs': {}}
                },
                # 117: {
                #     127: {'fcn': 'stop', 'kwargs': {}}
                # },
                # 118: {
                #     127: {'fcn': 'play', 'kwargs': {}}
                # },
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
            # 248: {'fcn': 'external_tick', 'kwargs': {}},
            153: {'fcn': 'delete_clip'},

            176: {
                8: {'fcn': 'increase_bpm'},
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
                    0: {'fcn': 'set_triplets_on_off', 'kwargs': {}}
                },
                25: {
                    127: {'set_waitfor_trigger': (176, 25, 0), 'wait_time': 0.5, 'time': None,
                          'short': {'fcn': 'change_cue_loop_status'}, 'long': {'fcn': 'remove_cue_loop'}},
                },
                26: {
                    0: {'fcn': 'set_hold_tempo_on_off', 'kwargs': {}}
                },
                # 117: {
                #     127: {'fcn': 'stop', 'kwargs': {}}
                # },
                # 118: {
                #     127: {'fcn': 'play', 'kwargs': {}}
                # },
                -1: {'fcn': 'cc'}
            }
        }
    }
}
