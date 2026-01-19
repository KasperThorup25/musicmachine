"""
midi_to_ev3_song.py

Converts a MIDI file into EV3-ready song data with millisecond timing.
"""

import math
import pretty_midi

# ----------------------------
# CONFIG
# ----------------------------

INPUT_MIDI = "input.mid"
OUTPUT_FILE = "song_data.py"
BPM = 120

GLASS_FREQUENCIES = [1154, 1192, 1231, 1271, 1313, 1356, 1401, 1448]

# ----------------------------
# UTILS
# ----------------------------

def midi_note_to_freq(midi_note):
    return 440.0 * (2 ** ((midi_note - 69) / 12))

def closest_glass(freq):
    return min(
        range(len(GLASS_FREQUENCIES)),
        key=lambda i: abs(GLASS_FREQUENCIES[i] - freq)
    )

def seconds_to_ms(seconds):
    return int(seconds * 1000)

# ----------------------------
# CORE LOGIC
# ----------------------------

def parse_midi(midi_path):
    midi = pretty_midi.PrettyMIDI(midi_path)
    events = {}

    for instrument in midi.instruments:
        if instrument.is_drum:
            continue

        for note in instrument.notes:
            start_ms = seconds_to_ms(note.start)
            freq = midi_note_to_freq(note.pitch)
            glass = closest_glass(freq)

            if start_ms not in events:
                events[start_ms] = set()

            events[start_ms].add(glass)

    # Convert to sorted list
    song = [
        (time_ms, sorted(list(glasses)))
        for time_ms, glasses in sorted(events.items())
    ]

    return song

# ----------------------------
# EXPORT
# ----------------------------

def export_song(song, output_path):
    with open(output_path, "w") as f:
        f.write("# Auto-generated song file (time in milliseconds)\n\n")
        f.write("SONG = [\n")
        for time_ms, notes in song:
            f.write(f"    ({time_ms}, {notes}),\n")
        f.write("]\n")

# ----------------------------
# MAIN
# ----------------------------

if __name__ == "__main__":
    song = parse_midi(INPUT_MIDI)
    export_song(song, OUTPUT_FILE)
    print(f"Generated {OUTPUT_FILE} with {len(song)} events")
