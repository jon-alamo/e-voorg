ETHERNET_IP = '192.168.1.6'
ETHERNET_PORT = 9095

KNOWN_DEVICES = {
    'controller': {
        'MPD232': {
            'osx': 'MPD232 Port A',
            'win32': 'MPD232 ',
            'linux': 'MPD232 MIDI 1'
        },
        'MPD218': {
            'linux': 'MPD218',
            'win32': 'MPD218',
            'osx': 'MPD218'
        }
    },
    'midi_interface': {
        'UM-ONE': {
            'linux': 'UM-ONE',
            'win32': 'UM-ONE',
            'osx': 'UM-ONE'
        },
        'MPD232': {
            'win32': 'MIDIOUT3',
            'osx': 'MPD232 MIDI',
            'linux': 'MPD232 MIDI 3'
        }
    }
}

KNOWN_PLATFORMS = {
    'linux': 'linux',
    'win32': 'win32',
    'osx': 'darwin'
}

CONTROLLER_ROUTE = 'src.controller.controller_maps.'
VIEWER_ROUTE = 'src.view.view_maps.'
