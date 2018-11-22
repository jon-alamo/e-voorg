import time

# CONSTANTS
MIN_BPM = 60
MAX_BPM = 180


class MidiClock(object):

    def __init__(self, bpm=100):
        # Set bpm parameter default value to 120.
        self.bpm = bpm
        # Clock control flag
        self.is_play = False
        # Time since las clock event
        self.t0 = 0
        # Timing clock event count
        self.tick = None
        self.tick_time = 2.5 / self.bpm

        # Reference to functions from packages to be used
        # Cross platform accurate time measurement
        self.timer = time.perf_counter

    def get_tick(self):
        """
        This method returns the midi tick count or none depending on the elapsed time from the last returned tick. If
        the elapsed time is equal or greater than the tick time, returns the new tick value, else returns None.
        :return: self.tick_count or None
        """

        if self.is_play:

            if self.timer() - self.t0 >= self.tick_time:
                self.t0 = self.timer()
                return True

            else:
                return False

        else:
            return False

    def set_bpm(self, bpm):
        """
        Sets the current bpm to the input value and calculate the new tick time
        :param bpm: Integer from MIN_BPM (60) to MAX_BPM (180)
        :return: None
        """
        if MIN_BPM <= bpm <= MAX_BPM:
            self.bpm = bpm
            self.tick_time = 2.5 / self.bpm

    def reset(self):
        self.tick = 0
        self.t0 = self.timer()

    def stop(self):
        self.is_play = False

    def start(self):
        self.is_play = True
        self.reset()

    def remaining_time(self):
        return self.tick_time - (self.timer() - self.t0)