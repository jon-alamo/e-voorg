from src.app import App
from src.interfaces.midi_interface.midi_interface import get_devices
from config.auto_config import get_current_platform, get_midi_io_ports, get_python_module
from config.config_data import KNOWN_PLATFORMS, KNOWN_DEVICES, CONTROLLER_ROUTE, VIEWER_ROUTE, ETHERNET_PORT, ETHERNET_IP
import traceback
import datetime

if __name__ == '__main__':

    print(get_devices())

    # Operative System
    platform = get_current_platform(KNOWN_PLATFORMS)
    # Controller device midi ports
    controller_io_ports, controller_name = get_midi_io_ports(KNOWN_DEVICES['controller'], platform)
    # Midi interface ports
    midi_interface_io_ports, midi_interface_name = get_midi_io_ports(KNOWN_DEVICES['midi_interface'], platform)
    # Controller map python module
    controller_module = get_python_module(CONTROLLER_ROUTE, controller_name)
    # Viewer map python module
    viewer_module = get_python_module(VIEWER_ROUTE, controller_name)

    # App config dictionary
    config = {
        'controller': controller_io_ports,
        'midi_interface': midi_interface_io_ports,
        'controller_map': controller_module,
        'viewer_map': viewer_module,
        'ethernet_port': ETHERNET_PORT,
        'ethernet_ip': ETHERNET_IP
    }

    try:

        # Init application
        app = App(**config)
        app.loop()

    except:
        print(traceback.format_exc())
        file_name = "logs/{date}_crash".format(date=datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        f = open(file_name, 'w')
        f.write(traceback.format_exc())
        f.close()
