from src.app import App
from src.interfaces.midi_interface import midi_interface

import sys
import importlib

known_devices = {
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

known_platforms = {
    'linux': 'linux',
    'win32': 'win32',
    'osx': 'darwin'
}

# Determine current platform
current_patform = None
for known_platform in known_platforms:
    if known_platforms[known_platform] in sys.platform:
        current_platform = known_platform

devices = {'controller': {'midi_in': None, 'midi_out': None}, 'midi_interface': {'midi_in': None, 'midi_out': None}}
controller_name = None
# Determine midi devices
available_midi_devices = midi_interface.get_devices()
for known_controller_device in known_devices['controller']:
    for in_device in available_midi_devices['midi_in']:
        if known_devices['controller'][known_controller_device][current_platform] in in_device:
            devices['controller']['midi_in'] = in_device
            controller_name = known_controller_device
    for out_device in available_midi_devices['midi_out']:
        if known_devices['controller'][known_controller_device][current_platform] in out_device:
            devices['controller']['midi_out'] = out_device

for known_midi_device in known_devices['midi_interface']:
    for in_device in available_midi_devices['midi_in']:
        if known_devices['midi_interface'][known_midi_device][current_platform] in in_device:
            devices['midi_interface']['midi_in'] = in_device
    for out_device in available_midi_devices['midi_out']:
        if known_devices['midi_interface'][known_midi_device][current_platform] in out_device:
            devices['midi_interface']['midi_out'] = out_device


controller_route = 'src.controller.controller_maps.'
viewer_route = 'src.view.view_maps.'

# Importing controllers and views
controller = importlib.import_module(controller_route + controller_name)
viewer = importlib.import_module(viewer_route + controller_name)

print('Controller devices: {controller}'.format(controller=devices['controller']))
print('Midi interface devices: {midi_interface}'.format(midi_interface=devices['midi_interface']))

# Init application
app = App(devices['controller'], devices['midi_interface'], controller, viewer)
app.loop()
