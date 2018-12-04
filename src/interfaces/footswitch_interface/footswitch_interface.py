import keyboard


class FootSwitch:
    def __init__(self):
        self.pressed_keys = []

    def get_interaction(self):

        if keyboard.is_pressed('Shift') and 'shift' not in self.pressed_keys:
            self.pressed_keys.append('shift')
            return {'fcn': 'set_global_rec', 'kwargs': {'state': 'on'}}
        elif not keyboard.is_pressed('Shift') and 'shift' in self.pressed_keys:
            self.pressed_keys.remove('shift')
            return {'fcn': 'set_global_rec', 'kwargs': {'state': 'off'}}

        elif keyboard.is_pressed('Ctrl') and 'ctrl' not in self.pressed_keys:
            self.pressed_keys.append('ctrl')
            return {'fcn': 'set_rec', 'kwargs': {'state': 'on'}}
        elif not keyboard.is_pressed('Ctrl') and 'ctrl' in self.pressed_keys:
            self.pressed_keys.remove('ctrl')
            return {'fcn': 'set_rec', 'kwargs': {'state': 'off'}}

        else:
            return None


if __name__ == '__main__':
    f = FootSwitch()

    while True:
        interaction = f.get_interaction()

        if interaction:
            print(interaction)
