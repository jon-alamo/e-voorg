import copy
from timeit import default_timer as timer


class Recorder(object):

    def __init__(self, playing_notes, note_loops):
        # Playing notes
        self.playing_notes = playing_notes
        self.note_loops = note_loops

        # Empty bar
        self.empty_bar = [0] * 96

        # Reset note bar indexes
        self.note_bar_indexes = {
            self.playing_notes[0]: 0,
            self.playing_notes[1]: 0,
            self.playing_notes[2]: 0,
            self.playing_notes[3]: 0,
            self.playing_notes[4]: 0,
            self.playing_notes[5]: 0,
            self.playing_notes[6]: 0,
            self.playing_notes[7]: 0,
            self.playing_notes[8]: 0,
            self.playing_notes[9]: 0,
            self.playing_notes[10]: 0,
            self.playing_notes[11]: 0,
            self.playing_notes[12]: 0,
            self.playing_notes[13]: 0,
            self.playing_notes[14]: 0,
            self.playing_notes[15]: 0
        }
        # Here will be placed records. 0 is current record, will be pasted or not in a preset between 1 and 16 by long
        # press corresponding pad pattern.
        self.recordings = {
            0:  {
                self.playing_notes[0]: [copy.deepcopy(self.empty_bar)],
                self.playing_notes[1]: [copy.deepcopy(self.empty_bar)],
                self.playing_notes[2]: [copy.deepcopy(self.empty_bar)],
                self.playing_notes[3]: [copy.deepcopy(self.empty_bar)],
                self.playing_notes[4]: [copy.deepcopy(self.empty_bar)],
                self.playing_notes[5]: [copy.deepcopy(self.empty_bar)],
                self.playing_notes[6]: [copy.deepcopy(self.empty_bar)],
                self.playing_notes[7]: [copy.deepcopy(self.empty_bar)],
                self.playing_notes[8]: [copy.deepcopy(self.empty_bar)],
                self.playing_notes[9]: [copy.deepcopy(self.empty_bar)],
                self.playing_notes[10]: [copy.deepcopy(self.empty_bar)],
                self.playing_notes[11]: [copy.deepcopy(self.empty_bar)],
                self.playing_notes[12]: [copy.deepcopy(self.empty_bar)],
                self.playing_notes[13]: [copy.deepcopy(self.empty_bar)],
                self.playing_notes[14]: [copy.deepcopy(self.empty_bar)],
                self.playing_notes[15]: [copy.deepcopy(self.empty_bar)],
            }
        }

        # Recording status by note: 0 = not recording, 1 = waiting to next bar, 2 = recording
        self.recording_status = {
            self.playing_notes[0]: 0,
            self.playing_notes[1]: 0,
            self.playing_notes[2]: 0,
            self.playing_notes[3]: 0,
            self.playing_notes[4]: 0,
            self.playing_notes[5]: 0,
            self.playing_notes[6]: 0,
            self.playing_notes[7]: 0,
            self.playing_notes[8]: 0,
            self.playing_notes[9]: 0,
            self.playing_notes[10]: 0,
            self.playing_notes[11]: 0,
            self.playing_notes[12]: 0,
            self.playing_notes[13]: 0,
            self.playing_notes[14]: 0,
            self.playing_notes[15]: 0
        }

        # Note loop indexes
        self.note_loop_bar_indexes = {
            self.playing_notes[0]: -1,
            self.playing_notes[1]: -1,
            self.playing_notes[2]: -1,
            self.playing_notes[3]: -1,
            self.playing_notes[4]: -1,
            self.playing_notes[5]: -1,
            self.playing_notes[6]: -1,
            self.playing_notes[7]: -1,
            self.playing_notes[8]: -1,
            self.playing_notes[9]: -1,
            self.playing_notes[10]: -1,
            self.playing_notes[11]: -1,
            self.playing_notes[12]: -1,
            self.playing_notes[13]: -1,
            self.playing_notes[14]: -1,
            self.playing_notes[15]: -1
        }

    def set_rec_get_play(self, tick, notes_to_rec_next_16th, notes_to_rec_last_16th):
        notes_to_play = {}
        t0 = timer()

        # Loop over every available notes
        for note in self.playing_notes:

            # When a bar starts, bar indexes are reset.
            if tick == 1:

                self.note_loop_bar_indexes[note] = (self.note_loop_bar_indexes[note] + 1) % len(
                    self.recordings[0][note])

                if self.recording_status[note] > 0:
                    self.recording_status[note] -= 1

            # When recording state is ON (==2)
            if self.recording_status[note] == 2:
                # If curent note was played to be placed in next note 16th
                if note in notes_to_rec_next_16th:
                    self.recordings[0][note][self.note_loop_bar_indexes[note]][tick - 1] = notes_to_rec_next_16th[note]
                # If no note was played
                else:
                    self.recordings[0][note][self.note_loop_bar_indexes[note]][tick - 1] = 0

                if note in notes_to_rec_last_16th:
                    self.recordings[0][note][self.note_loop_bar_indexes[note]][int((tick - 1) / 6) * 6] = \
                        notes_to_rec_last_16th[note]

            elif self.recording_status[note] == 1:

                # Note to be placed on next note 16th
                if note in notes_to_rec_next_16th:
                    self.recordings[0][note].append(copy.deepcopy(self.empty_bar))
                    self.note_loop_bar_indexes[note] = len(self.recordings[0][note]) - 1
                    self.recordings[0][note][self.note_loop_bar_indexes[note]][tick - 1] = notes_to_rec_next_16th[note]
                    self.recording_status[note] = 2

                # If note was not found, silence is placed.
                else:
                    note_to_play = self.recordings[0][note][self.note_loop_bar_indexes[note]][tick - 1]
                    if note_to_play:
                        notes_to_play[note] = note_to_play

                # Note to be placed on previous note 16th
                if note in notes_to_rec_last_16th:
                    self.recordings[0][note][self.note_loop_bar_indexes[note]][int((tick - 1) / 6) * 6] = \
                        notes_to_rec_last_16th[note]

            elif self.recording_status[note] == 0:
                note_to_play = self.recordings[0][note][self.note_loop_bar_indexes[note]][tick - 1]
                if note_to_play:
                    notes_to_play[note] = note_to_play

                if note in notes_to_rec_next_16th:
                    self.recordings[0][note] = [copy.deepcopy(self.empty_bar)]
                    self.note_loop_bar_indexes[note] = bar = 0
                    self.recordings[0][note][bar][tick - 1] = notes_to_rec_next_16th[note]
                    self.recording_status[note] = 2

                if note in notes_to_rec_last_16th:
                    self.recordings[0][note] = [copy.deepcopy(self.empty_bar)]
                    self.note_loop_bar_indexes[note] = bar = 0
                    self.recordings[0][note][bar][int((tick - 1) / 6) * 6] = notes_to_rec_last_16th[note]
                    self.recording_status[note] = 2

        return notes_to_play

    def delete_loop(self, note):
        map_note = self.playing_notes[self.note_loops.index(note)]
        self.recordings[0][map_note] = [self.empty_bar]
        self.note_loop_bar_indexes[map_note] = 0

    def save_preset(self, note):
        self.recordings[note] = copy.deepcopy(self.recordings[0])

    def play_preset(self, note):
        if note in self.recordings:
            self.note_loop_bar_indexes = copy.deepcopy(self.note_bar_indexes)
            self.recordings[0] = copy.deepcopy(self.recordings[note])
