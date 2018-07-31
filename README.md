# e-voorg - Live Rhythm Box Assistant


## Description
This code is a super first approach to a live and fun rhythm machine. :) It has been developed to work together with an
Akai MPD218 but it could be easily extended to any other midi device by modifying the interface_map.py file, replacing
corresponding heading keys (NOTE and CHANNEL messages) by the right ones according to the interface to be used. Default
midi channel is 10 (9 in the code) for midi notes and 1 (0 in the code) for control change messages.

## Notes
The code is Python 3.6 and can runs on Windows, Linux and Mac, with the rtmidi dependencies previously installed.

## Requirements

- Hardware
    Midi drum pad controller with velocity sensitive pads and ideally polyphonic aftertouch.

- Linux (Tested on Raspbian Stretch & Raspbian Stretch Lite)
    sudo apt-get update
    sudo apt-get install libasound2-dev
    sudo apt-get install libjack-dev
    sudo pip install -r requirements.txt

- Windows (Tested on Windows 10)
    Microsoft Visual C++ 14.0 standalone: Visual C++ Build Tools 2015 (x86, x64, ARM)
    pip install -r requirements.txt

- MacOS 10.13
    pip install -r requirements.txt

## Features

### Live quantization (always active)
The step resolution is a 96th part of a bar and is called midi tick. A bar has 4 4th notes and a 4th note 4 16th notes,
so a 4th note last 24 midi ticks and a 16th note 6 midi ticks. Tick have values from 1 to 96 being the first one the one
that indicates the beginning of the bar. When the finger drummer plays a note in the midi interface, the note is placed
in the next or the previous 16th note, due to the next quantization rule:
    - If the rest resulting from the current tick divided by 6 is 1 or 2, the note is played instantly and placed, if
    recording active, in the previous 16th note.
    - If the rest is 3, 4, 5 or 6 , the note is played and placed (if recording active) in the next 16th note.

### Live Recording
- Switched ON/OFF by midi note on 82
Recording feature is able to memorize loops for each note individually and with different lengths. When recording state
is active, a loop in a note is stored in three steps:
    1. When a note is played during a bar, the recorder immediately stores the note for the played note and the
    recording state for this note is switched to ON. All notes played during the rest of this bar will be recorded. Note
    that any recorded bar is fulfilled, either from the beginning until the end of the bar.
    2. When the next bar comes on, the loop starts to play from the beginning but the recording state remains in a WAIT
    MODE during this bar. If this note is played during this bar, a new bar is added to the end of the current note loop
    and the played note is placed in its corresponding position, as it was played. The recording state switches again to
    ON.
    3. When a new bar comes, the recording state changes to wait mode and the note is not played anymore during this
    whole bar, the recording states switches OFF.
    4. If a note is played and the recording state for that note is OFF, the whole current playing loop for the note is
    removed and replaced for what is being playing now.

### Store what is playing now to a preset
- Whatever is playing now by each note loop, can be stored by long-pressing (>0.1s) midi notes from 68 to 79. Once a
preset is stored, it can be played later by short pressing the same note.

### Removing loops without playing a note
Midi notes on from 52 to 67 will delete notes on played from note 36 until 51.

### Metronome
The metronome can be activated or deactivated by pressing the note 80.

### Tiplets
Triplets functionality can be activated or deactivated by pressing note 81. When this functionality is active,
poly-pressure messages received, from id 36 to 51 will play triplets in the note with the same id. Triplets are stored
in loops as the rest of the notes.

### Coming features
- Randomize
- Grooves