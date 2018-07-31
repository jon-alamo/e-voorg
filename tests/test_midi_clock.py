import unittest
import src.midi_clock as midi_clock
from time import perf_counter as timer, sleep
import threading
import timeit

SETUP = """
import src.midi_clock as midi_clock
from time import sleep
clock = midi_clock.MidiClock({})
wait_tick = clock.wait_tick
clock.reset()
clock.start()
        """


class TestWaitTick(unittest.TestCase):

    def setUp(self):
        sleep(1)

    def tearDown(self):
        sleep(1)

    def test_wait_tick_is_accurate_at_120bpm_entire_bar(self):

        # Standard as most common bpm value
        bpm = 120
        # At this bpm clock should have high performance (low tolerance margin)
        bpm_tolerance = 0.2

        # Meassurements over a whole bar (96 ticks)
        ticks_to_meassure = 96

        # Theoretical values in time
        theoretical_tick_time = 2.5 / bpm
        max_tick_time = 2.5 / (bpm - bpm_tolerance)
        min_tick_time = 2.5 / (bpm + bpm_tolerance)

        # Time class to make measurements
        t = timeit.Timer(stmt="wait_tick()", setup=SETUP.format(bpm))
        # Make measurements
        tick_values = t.repeat(ticks_to_meassure, 1)

        # Assert results
        self.assertTrue(min_tick_time < min(tick_values) < max(tick_values) < max_tick_time,
                        '\nTheoretical tick time: {}'
                        '\nMin tick time (real/theoretical) {}/{}'
                        '\nMax tick time (real/theoretical: {}/{}.'.format(
                            theoretical_tick_time,
                            min(tick_values),
                            min_tick_time,
                            max(tick_values),
                            max_tick_time
                        ))

    def test_wait_tick_is_accurate_for_bpm_from_60_to_200_1_4th_bar(self):

        # BPM values from 60 to 200
        for bpm in range(60, 200, 5):

            # Increased tolerance due to wide range of values and no so common ones
            bpm_tolerance = 1
            theoretical_tick_time = 2.5 / bpm

            # Measurements take place in 4 first ticks of a bar
            ticks_to_meassure = 4

            # Theoretical time values for each bpm value
            max_tick_time = 2.5 / (bpm - bpm_tolerance)
            min_tick_time = 2.5 / (bpm + bpm_tolerance)

            # Timer
            t = timeit.Timer(stmt="wait_tick()", setup=SETUP.format(bpm))
            # Make measurements
            tick_values = t.repeat(ticks_to_meassure, 1)

            # Assert measurements
            self.assertTrue(min_tick_time < min(tick_values) < max(tick_values) < max_tick_time,
                            '\nBPM: {}'
                            '\nTheoretical tick time: {}'
                            '\nMin tick time (real/theoretical) {}/{}'
                            '\nMax tick time (real/theoretical: {}/{}.'.format(
                                bpm,
                                theoretical_tick_time,
                                min(tick_values),
                                min_tick_time,
                                max(tick_values),
                                max_tick_time
                            ))

            sleep(0.5)

    def test_wait_tick_is_accurate_for_bpm_120_and_some_elapsed_time_before_entering_clock(self):

        # Set bpm
        bpm = 120

        # Low tolerance again
        bpm_tolerance = 0.2
        theoretical_tick_time = 2.5 / bpm

        # Set an elapsed time amount before wait for clock tick
        elapsed_time = 0.010

        # Measurements take place in a whole bar
        ticks_to_meassure = 96

        # Theoretical time values for each bpm value
        max_tick_time = 2.5 / (bpm - bpm_tolerance)
        min_tick_time = 2.5 / (bpm + bpm_tolerance)

        # Timer
        t = timeit.Timer(stmt="sleep({});wait_tick()".format(elapsed_time), setup=SETUP.format(bpm))
        # Make measurements
        tick_values = t.repeat(ticks_to_meassure, 1)

        # Assert measurements
        self.assertTrue(min_tick_time < min(tick_values) < max(tick_values) < max_tick_time,
                        '\nBPM: {}'
                        '\nTheoretical tick time: {}'
                        '\nMin tick time (real/theoretical) {}/{}'
                        '\nMax tick time (real/theoretical: {}/{}.'.format(
                            bpm,
                            theoretical_tick_time,
                            min(tick_values),
                            min_tick_time,
                            max(tick_values),
                            max_tick_time
                        ))

    def test_wait_tick_is_accurate_for_bpm_120_and_elapsed_times_before_entering_clock_from_1ms_to_tick_time(self):

        # Set bpm
        bpm = 120

        # Low tolerance again
        bpm_tolerance = 0.2
        theoretical_tick_time = 2.5 / bpm

        # Measurements take place in a whole bar
        ticks_to_meassure = 12

        # Theoretical time values for each bpm value
        max_tick_time = 2.5 / (bpm - bpm_tolerance)
        min_tick_time = 2.5 / (bpm + bpm_tolerance)

        time_divisions = 5

        for i in range(time_divisions):

            # Set an elapsed time amount before wait for clock tick
            elapsed_time = i * theoretical_tick_time / time_divisions

            # Timer
            t = timeit.Timer(stmt="sleep({});wait_tick()".format(elapsed_time), setup=SETUP.format(bpm))
            # Make measurements
            tick_values = t.repeat(ticks_to_meassure, 1)

            # Assert measurements
            self.assertTrue(min_tick_time < min(tick_values) < max(tick_values) < max_tick_time,
                            '\nBPM: {}'
                            '\nElapsed time before clock: {}'
                            '\nTheoretical tick time: {}'
                            '\nMin tick time (real/theoretical) {}/{}'
                            '\nMax tick time (real/theoretical: {}/{}.'.format(
                                bpm,
                                elapsed_time,
                                theoretical_tick_time,
                                min(tick_values),
                                min_tick_time,
                                max(tick_values),
                                max_tick_time
                            ))

    def test_wait_tick_is_accurate_for_bpm_120_and_multi_threading_no_stress(self):

        # Standard as most common bpm value
        bpm = 120
        # At this bpm clock should have high performance (low tolerance margin)
        bpm_tolerance = 0.2

        # Meassurements over a whole bar (96 ticks)
        ticks_to_measure = 96

        # Theoretical values in time
        theoretical_tick_time = 2.5 / bpm
        max_tick_time = 2.5 / (bpm - bpm_tolerance)
        min_tick_time = 2.5 / (bpm + bpm_tolerance)

        # Time class to make measurements
        t = timeit.Timer(stmt="wait_tick()", setup=SETUP.format(bpm))

        global tick_values

        def get_clock_measurements():
            global tick_values
            tick_values = t.repeat(ticks_to_measure, 1)

        # Thread
        clock_thread = threading.Thread(target=get_clock_measurements)
        # Make measurements
        clock_thread.start()

        # Wait until the clock finishes without additional processing effort
        while clock_thread.is_alive():
            sleep(0.1)

        # Assert results
        self.assertTrue(min_tick_time < min(tick_values) < max(tick_values) < max_tick_time,
                        '\nTheoretical tick time: {}'
                        '\nMin tick time (real/theoretical) {}/{}'
                        '\nMax tick time (real/theoretical: {}/{}.'.format(
                            theoretical_tick_time,
                            min(tick_values),
                            min_tick_time,
                            max(tick_values),
                            max_tick_time
                        ))

    def test_wait_tick_is_accurate_for_bpm_120_and_multi_threading_stress(self):

        # Standard as most common bpm value
        bpm = 120
        # At this bpm clock should have high performance (low tolerance margin)
        bpm_tolerance = 0.5

        # Meassurements over a whole bar (96 ticks)
        ticks_to_measure = 96

        # Theoretical values in time
        theoretical_tick_time = 2.5 / bpm
        max_tick_time = 2.5 / (bpm - bpm_tolerance)
        min_tick_time = 2.5 / (bpm + bpm_tolerance)

        # Time class to make measurements
        t = timeit.Timer(stmt="wait_tick()", setup=SETUP.format(bpm))

        global tick_values

        def get_clock_measurements():
            global tick_values
            tick_values = t.repeat(ticks_to_measure, 1)

        # Thread
        clock_thread = threading.Thread(target=get_clock_measurements)
        # Make measurements
        clock_thread.start()

        # Wait until the clock finishes without additional processing effort
        while clock_thread.is_alive():
            pass

        # Assert results
        self.assertTrue(min_tick_time < min(tick_values) < max(tick_values) < max_tick_time,
                        '\nTheoretical tick time: {}'
                        '\nMin tick time (real/theoretical) {}/{}'
                        '\nMax tick time (real/theoretical: {}/{}.'.format(
                            theoretical_tick_time,
                            min(tick_values),
                            min_tick_time,
                            max(tick_values),
                            max_tick_time
                        ))

    def test_wait_tick_is_accurate_for_bpm_120_and_multi_threading_increasing_stress(self):

        # Standard as most common bpm value
        bpm = 120
        # At this bpm clock should have high performance (low tolerance margin)
        bpm_tolerance = 0.5

        # Meassurements over a whole bar (96 ticks)
        ticks_to_measure = 96

        # Theoretical values in time
        theoretical_tick_time = 2.5 / bpm
        max_tick_time = 2.5 / (bpm - bpm_tolerance)
        min_tick_time = 2.5 / (bpm + bpm_tolerance)

        # Time class to make measurements
        t = timeit.Timer(stmt="wait_tick()", setup=SETUP.format(bpm))

        stress_values = range(10)

        for stress_value in stress_values:

            def stress(n):
                def parallel_process():
                    ti = timer()
                    while timer() - ti < 10:
                        pass

                for i in range(n):
                    thread = threading.Thread(target=parallel_process)
                    thread.start()

            stress(stress_value)
            sleep(1)
            tick_values = t.repeat(ticks_to_measure, 1)

            # Assert results
            self.assertTrue(min_tick_time < min(tick_values) < max(tick_values) < max_tick_time,
                            '\nStress value: {}'
                            '\nTheoretical tick time: {}'
                            '\nMin tick time (real/theoretical) {}/{}'
                            '\nMax tick time (real/theoretical: {}/{}.'.format(
                                stress_value,
                                theoretical_tick_time,
                                min(tick_values),
                                min_tick_time,
                                max(tick_values),
                                max_tick_time
                            ))


if __name__ == '__main__':
    unittest.main(verbosity=2)
