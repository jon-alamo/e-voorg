import time


class Controller:

    def __init__(self, interface, controller_map):
        self.interface = interface
        self.controller_map = controller_map

        self.current_view = 'default_view'
        self.current_mode = 'default_mode'

        self.time_events = {}

    def get_interaction(self):
        input_msg = self.interface.receive()
        if input_msg:
            return self.get_control(input_msg)

    def get_control(self, message):
        # todo: check cost of copying here partial map from controller map for every interaction
        control = self.controller_map[self.current_view][self.current_mode]

        for interaction_index in range(len(message)):

            if self.time_events and message[interaction_index] in self.time_events:
                time_event = self.time_events.pop(message[interaction_index])

                if time.time() - time_event['t0'] > time_event['time']:
                    return self.put_arguments(self.controller_map['waitfor'][message[interaction_index]]['long'], message)
                else:
                    return self.put_arguments(self.controller_map['waitfor'][message[interaction_index]]['short'], message)

            # If interaction has functionality
            if message[interaction_index] in control:
                control = control[message[interaction_index]]

                if 'waitfor' in control:
                    self.time_events[control['waitfor']] = {'time': control['time'], 't0': time.time()}
                    break

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

    @staticmethod
    def put_arguments(control, message):
        if 'kwargs' not in control and 'fcn' in control:
            return {'fcn': control['fcn'], 'kwargs': {'message': message}}

        return control
