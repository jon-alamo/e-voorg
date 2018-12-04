import copy


class Recorder:

    def __init__(self, channels, memory_clips, combine_channels=False):

        # General recording
        self.is_recording = False
        self.is_leaving_recording = False

        # Quantization notes to tick steps table
        self.quantization_table = {0: 0, 4: 24, 8: 12, 16: 6, 24: 4, 32: 3, 96: 1}

        # Parameters
        self.channels = channels

        self.memory_clips = memory_clips
        self.empty_bar = [[] for i in range(1, 97)]

        # Playing quantized bar
        self.playing_quantized_bar = {channel: copy.deepcopy(self.empty_bar) for channel in self.channels}

        # Current loop with empty bar by channel
        self.current_loops = {channel: [copy.deepcopy(self.empty_bar)] for channel in self.channels}

        # Memory loops
        self.memories = {clip: {channel: [copy.deepcopy(self.empty_bar)] for channel in self.channels} for clip in self.memory_clips}

        # Recording states
        self.recording_states = {channel: 0 for channel in self.channels}

        # Bar indexes by channel
        self.bar_indexes = {channel: -1 for channel in self.channels}

    def get_quantized_notes(self, tick):
        notes_to_play = set()

        if tick == 1:
            # Leave recording at bar's beginning if leaving recording active and recording active now.
            if self.is_recording and self.is_leaving_recording:
                self.stop_recording_now()

        for channel in self.channels:

            if tick == 1:
                # Reset bar
                if not self.recording_states[channel]:
                    self.bar_indexes[channel] = (self.bar_indexes[channel] + 1) % len(self.current_loops[channel])

                elif self.recording_states[channel] == 1:
                    # New empty bar after the current one
                    self.current_loops[channel].append(copy.deepcopy(self.empty_bar))
                    self.bar_indexes[channel] = len(self.current_loops[channel]) - 1

                elif self.recording_states[channel] == 2:
                    self.recording_states[channel] = 1

            # Get notes from current loop
            notes_to_play.update(self.current_loops[channel][self.bar_indexes[channel]][tick - 1])
            # Get playing quantized notes
            notes_to_play.update(self.playing_quantized_bar[channel][tick - 1])
            # Reset playing quantized notes
            self.playing_quantized_bar[channel][tick - 1].clear()

        return list(notes_to_play)

    def rec_quantized_note(self, current_tick, event_to_rec_on_tick, channel, quantization=16, tick_offset=0):
        """
        Only recording
        :param current_tick:
        :param event_to_rec_on_tick:
        :param channel:
        :param quantization:
        :param tick_offset:
        :return:
        """
        quantization_ticks = self.quantization_table[quantization]
        if not self.recording_states[channel]:
            # If this channel have some event to be recorded
            if self.is_recording:
                self.recording_states[channel] = 3
                self.current_loops[channel] = [copy.deepcopy(self.empty_bar)]
                self.bar_indexes[channel] = 0

        # If current channel is being recorded or precount is active
        if self.recording_states[channel]:

            if self.recording_states[channel] == 3:
                # Once the first note is recorder, bar can be expanded
                self.recording_states[channel] = 2

            # Get quantized tick position
            tick_position = (self.get_quantized_tick(current_tick, quantization_ticks, 1) + tick_offset) % 96
            # Save event on current position
            self.current_loops[channel][self.bar_indexes[channel]][tick_position].append(event_to_rec_on_tick)

        # Get next tick position to live playing quantization
        next_tick_position = (self.get_quantized_tick(current_tick, quantization_ticks, 1) + tick_offset) % 96
        # Add to live playing quantized loop
        self.playing_quantized_bar[channel][next_tick_position].append(event_to_rec_on_tick)

    @staticmethod
    def get_quantized_tick(tick, quantization, offset=0.5):
        return int(((tick - 1) + quantization * offset) / quantization) * quantization % 96

    def leave_recording(self):
        self.is_leaving_recording = True

    def stop_recording_now(self):
        self.recording_states = {key: False for key in self.channels}
        self.is_leaving_recording = False
        self.is_recording = False

    def activate_recording(self):
        self.is_recording = True

    def save_preset(self, channels, clip):
        for channel in channels:
            self.memories[clip][channel] = list(self.current_loops[channel])

    def delete_current_loop(self, channel):
        self.current_loops[channel] = [list(self.empty_bar)]
        self.bar_indexes[channel] = 0

    def play_channel_clip(self, channels, clip):
        for channel in channels:
            self.current_loops[channel] = list(self.memories[clip][channel])
            self.bar_indexes[channel] = 0

    def play_clips_line(self, clip):
        self.current_loops = {channel: copy.deepcopy(self.memories[channel][clip]) for channel in self.channels}

    def delete_channel_clip(self, channels, clip):
        for channel in channels:
            self.memories[clip][channel] = [list(self.empty_bar)]
            self.bar_indexes[channel] = 0
