import keyboard


class FootSwitch:
    def __init__(self):
        self.is_recording = False

    def get_interaction(self):

        if keyboard.is_pressed('b') and not self.is_recording:
            self.is_recording = True
            return {'fcn': 'set_rec_mode', 'kwargs': {'state': 'on'}}
        elif not keyboard.is_pressed('b') and self.is_recording:
            self.is_recording = False
            return {'fcn': 'set_rec_mode', 'kwargs': {'state': 'off'}}
        else:
            return None
