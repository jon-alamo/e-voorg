import time
from src.interfaces.midi_interface.midi_interface import MidiInterface


class Controller:

    def __init__(self, interface: MidiInterface, controller_map):

        self.interface = interface

        self.controller_map = controller_map.controller_map

        # Initial view and mode states.
        self.current_view = 'default_view'
        self.current_mode = 'default_mode'

        # Time events to short/long press handling.
        self.time_events = {}

    def get_interaction(self):
        input_msg = self.interface.receive()
        if input_msg:
            control = self.get_control(input_msg)
            return control

    def get_control(self, message):

        time_event = self.check_time_events(message)

        if time_event:
            return time_event

        control = self.controller_map[self.current_view][self.current_mode]

        for interaction_index in range(len(message)):

            # If interaction has functionality
            if message[interaction_index] in control:
                control = control[message[interaction_index]]

                if 'set_waitfor_trigger' in control:
                    control['time'] = time.time()
                    self.time_events[control['set_waitfor_trigger']] = control

                if 'fcn' in control and control['fcn'] == 'set_view':
                    self.current_view = control['kwargs']['view']
                    return self.put_arguments(control, message)

                if 'fcn' in control and control['fcn'] == 'switch_mode':
                    self.current_mode = control['kwargs']['mode']
                    return self.put_arguments(control, message)

                elif 'fcn' in control:
                    return self.put_arguments(control, message)

            elif -1 in control:
                return self.put_arguments(control[-1], message)

            else:
                break

    @staticmethod
    def put_arguments(control, message):
        if 'kwargs' not in control and 'fcn' in control:
            return {'fcn': control['fcn'], 'kwargs': {'message': message}}

        return control

    def check_time_events(self, message):
        time_event = self.time_events.pop(tuple(message), {})

        if time_event:
            t_now = time.time()
            elapsed = t_now - time_event['time']

            if elapsed > time_event['wait_time']:
                return self.put_arguments(time_event['long'], message)
            else:
                return self.put_arguments(time_event['short'], message)

        return None
