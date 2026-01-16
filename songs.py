#!/usr/bin/env pybricks-micropython

# This program contains all the songs and functions related to the songs that's used in the music machine project


# Notes (for redability)
C = 0
D = 1
E = 2
G = 3


class Song:
    def __init__(self, name, events):
        self.name = name
        self.events = events

# Example song using 4 notes
SONG_SIMPLE = Song(
    name="Simple Melody",
    events=[
        {"time_ms": 0,    "notes": [C]},
        {"time_ms": 400,  "notes": [D]},
        {"time_ms": 800,  "notes": [E]},
        {"time_ms": 1200, "notes": [D, G]},  # chord
        {"time_ms": 1600, "notes": [C]},
    ]
)

SONG_TEST = Song(
    name="Test Melody",
    events=[
        {"time_ms": 0,    "notes": [C]}
    ],
)
