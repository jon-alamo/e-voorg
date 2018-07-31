import unittest
from src.recorder import Recorder
import src.midi_data as midi_data

RECORDING_STATE = 2
LEAVING_RECORDING_STATE = 1
PLAY_STATE = 0
NOTE_ON_HEADING_RIGHT_CHANNEL = midi_data.NOTE_ON[9]
NOTE_ON_HEADING_WRONG_CHANNEL = midi_data.NOTE_ON[15]
POLY_PRESSURE_HEADING = midi_data.POLY_PRESSURE[9]
PLAYING_NOTES = list(range(16))
BAR_CLOCK_EVENTS = list(range(1, 97))


class TestRecorderSetRecPlay(unittest.TestCase):

    def test_when_an_available_note_on_is_passed_the_note_switch_immediately_to_recording_state_every_clock_step(self):

        notes = {}

        # All available playing notes
        for note in PLAYING_NOTES:
            notes[note] = [NOTE_ON_HEADING_RIGHT_CHANNEL, note, 127]

        # For each time event
        for clock_event in BAR_CLOCK_EVENTS:
            self.recorder = Recorder(PLAYING_NOTES)
            self.recorder.set_rec_get_play(clock_event, notes, {})

            for recording_note in PLAYING_NOTES:
                self.assertEqual(self.recorder.recording_status[recording_note], RECORDING_STATE)

    def test_when_an_unavailable_note_on_is_passed_the_note_keeps_in_play_state(self):

        notes = {}

        # All available playing notes
        for note in PLAYING_NOTES:
            wrong_note = note + PLAYING_NOTES[-1] + 1
            notes[wrong_note] = [NOTE_ON_HEADING_WRONG_CHANNEL, wrong_note, 127]

        # For each time event
        for clock_event in BAR_CLOCK_EVENTS:
            self.recorder = Recorder(PLAYING_NOTES)
            self.recorder.set_rec_get_play(clock_event, notes, {})

            for recording_note in PLAYING_NOTES:
                self.assertEqual(self.recorder.recording_status[recording_note], PLAY_STATE)

    def test_when_a_note_is_played_switch_immediately_to_recording_state_and_persist_during_the_rest_of_the_bar(self):
        notes = {}

        # All available playing notes
        for note in PLAYING_NOTES:
            notes[note] = [NOTE_ON_HEADING_RIGHT_CHANNEL, note, 127]

        # Creates recorder
        self.recorder = Recorder(PLAYING_NOTES)

        for bar in [1]:

            # For each time event
            for clock_event in BAR_CLOCK_EVENTS:

                if bar == 1 and clock_event == 1:
                    self.recorder.set_rec_get_play(clock_event, notes, {})
                else:
                    self.recorder.set_rec_get_play(clock_event, {}, {})

                    for recording_note in PLAYING_NOTES:
                        self.assertEqual(self.recorder.recording_status[recording_note], RECORDING_STATE)

    def test_when_a_note_is_in_recording_state_and_a_new_bar_comes_then_its_state_changes_to_leaving_recording(self):
        notes = {}

        # All available playing notes
        for note in PLAYING_NOTES:
            notes[note] = [NOTE_ON_HEADING_RIGHT_CHANNEL, note, 127]

        # Creates recorder
        self.recorder = Recorder(PLAYING_NOTES)

        for bar in [1, 2]:

            # For each time event
            for clock_event in BAR_CLOCK_EVENTS:

                if bar == 1:
                    self.recorder.set_rec_get_play(clock_event, notes, {})

                if bar == 2:
                    self.recorder.set_rec_get_play(clock_event, {}, {})
                    for recording_note in PLAYING_NOTES:
                        self.assertEqual(self.recorder.recording_status[recording_note], LEAVING_RECORDING_STATE)

    def test_when_a_note_is_in_recording_state_the_rec_stat_2_is_changed_to_0_after_2_bars_if_now_new_notes_are_played(
            self):

        notes = {}

        # All available playing notes
        for note in PLAYING_NOTES:
            notes[note] = [NOTE_ON_HEADING_RIGHT_CHANNEL, note, 127]

        # Creates recorder
        self.recorder = Recorder(PLAYING_NOTES)

        for bar in [1, 2, 3]:

            # For each time event
            for clock_event in BAR_CLOCK_EVENTS:

                if bar == 1 and clock_event == 1:
                    self.recorder.set_rec_get_play(clock_event, notes, {})
                else:
                    self.recorder.set_rec_get_play(clock_event, {}, {})

                if bar == 3:
                    self.recorder.set_rec_get_play(clock_event, {}, {})
                    for recording_note in PLAYING_NOTES:
                        self.assertEqual(self.recorder.recording_status[recording_note], PLAY_STATE)


if __name__ == '__main__':
    unittest.main()
