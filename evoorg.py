from src.got_the_rhythm import Rhythm
import src.midi_data as midi_data
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

NOTE_CHANNEL = config.getint(section='MIDI', option='note_channel')
CONTROL_CHANNEL = config.getint(section='MIDI', option='control_change_channel')
METRONOME_NOTE = config.get(section='MIDI', option='metronome_note')
USB_MIDI_INTERFACE = config.get(section='DEVICES', option='usb_midi_interface')
DRUM_PAD_INTERFACE = config.get(section='DEVICES', option='drum_pad_interface')
DRUM_PAD_MIDI_MAP = config.get(section='DEVICES', option='drum_pad_midi_map')

POLY_PRESSURE_HEADING = midi_data.POLY_PRESSURE[NOTE_CHANNEL]
NOTE_ON_HEADING = midi_data.NOTE_ON[NOTE_CHANNEL]
NOTE_OFF_HEADING = midi_data.NOTE_OFF[NOTE_CHANNEL]
CONTROL_CHANGE_HEADING = midi_data.CONTROL_CHANGE[CONTROL_CHANNEL]

MIDI_MAP = eval(open(DRUM_PAD_MIDI_MAP, 'r').read())

if __name__ == '__main__':

    # INIT AND SETUP
    music = Rhythm(
        usb_midi_interface=USB_MIDI_INTERFACE,
        drum_pad_interface=DRUM_PAD_INTERFACE,
        midi_map=MIDI_MAP,
        metronome_note=METRONOME_NOTE,
        note_channel=NOTE_CHANNEL,
        control_channel=CONTROL_CHANNEL,
        poly_pressure_heading=POLY_PRESSURE_HEADING,
        note_on_heading=NOTE_ON_HEADING,
        note_off_heading=NOTE_OFF_HEADING,
        control_change_heading=CONTROL_CHANGE_HEADING
    )

    # START EXECUTION
    music.main_loop()
