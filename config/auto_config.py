from src.interfaces.midi_interface import midi_interface
import sys
import importlib


def get_current_platform(known_platforms):
    # Determine current platform
    for known_platform in known_platforms:
        if known_platforms[known_platform] in sys.platform:
            return known_platform

    return None


def get_midi_io_ports(known_devices, current_platform):
    found_io_ports = {'midi_in': None, 'midi_out': None}
    # Determine midi devices
    available_midi_devices = midi_interface.get_devices()
    controller_name = ''

    for known_controller_device in known_devices:

        for in_device in available_midi_devices['midi_in']:
            if known_devices[known_controller_device][current_platform] in in_device:
                found_io_ports['midi_in'] = in_device
                controller_name = known_controller_device
                break

        for out_device in available_midi_devices['midi_out']:
            if known_devices[known_controller_device][current_platform] in out_device:
                found_io_ports['midi_out'] = out_device
                break

    return found_io_ports, controller_name


def get_python_module(route, name):
    return importlib.import_module(route + name)
