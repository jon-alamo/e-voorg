import copy


class Recorder:

    def __init__(self, channels, memory_clips):

        # General recording
        self.is_recording = False
        self.is_leaving_recording = False

        # Quantization notes to tick steps table
        self.quantization_table = {0: 0, 4: 24, 8: 12, 16: 6, 24: 4, 32: 3, 96: 1}

        # Parameters
        self.channels = channels
        self.channels_to_mute = {}

        self.memory_clips = memory_clips
        self.empty_bar = [[] for i in range(1, 97)]
        self.stop_recordings = {key: False for key in self.channels}

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

        self.next_bar_events = {channel: [] for channel in self.channels}

    def get_quantized_notes(self, tick):
        notes_to_play = {}

        if tick == 1:
            # Leave recording at bar's beginning if leaving recording active and recording active now.
            if self.is_recording and self.is_leaving_recording:
                self.stop_recording_now()

        for channel in self.channels:
            channel_notes = set()

            if tick == 1:
                # Reset bar
                if not self.recording_states[channel]:
                    self.bar_indexes[channel] = (self.bar_indexes[channel] + 1) % len(self.current_loops[channel])

                elif self.recording_states[channel] == 1:
                    # New empty bar after the current one
                    self.current_loops[channel].append(list(self.empty_bar))
                    self.bar_indexes[channel] = len(self.current_loops[channel]) - 1

                elif self.recording_states[channel] == 2:
                    self.recording_states[channel] = 1

                if self.next_bar_events[channel]:
                    self.current_loops[channel][self.bar_indexes[channel]][0] = list(self.next_bar_events[channel])
                    self.next_bar_events[channel] = []

            if (channel in self.channels_to_mute and not self.channels_to_mute[channel]) or channel not in self.channels_to_mute:
                # Get notes from current loop
                channel_notes.update(self.current_loops[channel][self.bar_indexes[channel]][tick - 1])

            # Get playing quantized notes
            live_playing_notes = self.playing_quantized_bar[channel][tick - 1]
            channel_notes.update(live_playing_notes)

            if len(live_playing_notes) > 0 and channel in self.channels_to_mute:
                self.channels_to_mute[channel] = True

            # Reset playing quantized notes
            self.playing_quantized_bar[channel][tick - 1].clear()

            if channel_notes:
                notes_to_play[channel] = channel_notes

        return notes_to_play

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

        # Received note channel to be recorded is not already recording but recording state is active
        if not self.recording_states[channel] and self.is_recording:
            self.current_loops[channel] = [list(self.empty_bar)]
            self.bar_indexes[channel] = 0

            # If note to rec is after the last note 16th of the bar note is supposed to be at the bar beginning, so no
            # new empty bar will be added next to the current empty one.
            if current_tick > 91:
                self.recording_states[channel] = 2
            # Otherwise, if note is played before last note 16th of the bar, all previous part of the bar is considered
            # silence and a new bar will be added if recording state continues.
            else:
                self.recording_states[channel] = 1

        # If current channel is being recorded or precount is active
        if self.recording_states[channel]:

            # Get quantized tick position
            tick_position = (self.get_quantized_tick(current_tick, quantization_ticks, 1) + tick_offset) % 96

            if tick_position < 90 < current_tick < 97:
                self.next_bar_events[channel].append(event_to_rec_on_tick)
            else:
                # Save event on current position
                self.current_loops[channel][self.bar_indexes[channel]][tick_position] = \
                    self.current_loops[channel][self.bar_indexes[channel]][tick_position] + [event_to_rec_on_tick]

        # Get next tick position to live playing quantization
        next_tick_position = (self.get_quantized_tick(current_tick, quantization_ticks, 1) + tick_offset) % 96
        # Add to live playing quantized loop
        self.playing_quantized_bar[channel][next_tick_position] = \
            self.playing_quantized_bar[channel][next_tick_position] + [event_to_rec_on_tick]

    @staticmethod
    def get_quantized_tick(tick, quantization, offset=0.5):
        return int(((tick - 1) + quantization * offset) / quantization) * quantization % 96

    def start_recording(self):
        self.is_leaving_recording = False
        self.is_recording = True

    def leave_recording(self):
        self.is_leaving_recording = True

    def stop_recording_now(self):
        self.recording_states = dict(self.stop_recordings)
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

    def delete_channel_clip(self, channels, clip):
        for channel in channels:
            self.memories[clip][channel] = [list(self.empty_bar)]
            self.bar_indexes[channel] = 0
