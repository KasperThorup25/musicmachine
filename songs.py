#!/usr/bin/env pybricks-micropython

# This program contains all the songs and functions related to the songs that's used in the music machine project

NOTES = [1150, 1189, 1229, 1270, 1313, 1357, 1402, 1448] # this is the frequencies the glass vibrate at

# Notes (for redability)
C = 0
D = 1
E = 2
F = 3
G = 4
A = 5
B = 6
C5 = 7

songs = []

class Song:
    count = 0

    def __init__(self, name, events):
        self.name = name
        self.events = events
        self.song_number = Song.count # counting from 0
        print("Song {} created with name {}".format(self.song_number, self.name))
        Song.count += 1

# Example song using 4 notes
songs.append(Song(
    name="Simple Melody",
    events=[
        {"time_ms": 0,    "notes": [C]},
        {"time_ms": 400,  "notes": [D]},
        {"time_ms": 800,  "notes": [E]},
        {"time_ms": 1200, "notes": [D, G]},  # chord
        {"time_ms": 1600, "notes": [C]},
        {"time_ms": 2000, "notes": [A]}
    ]
))

songs.append(Song(
    name="Simple ascend and descend",
    events=[
        {"time_ms": 0,      "notes": [C]},
        {"time_ms": 200,    "notes": [D]},
        {"time_ms": 400,    "notes": [E]},
        {"time_ms": 600,    "notes": [F]},
        {"time_ms": 800,    "notes": [G]},
        {"time_ms": 1000,   "notes": [A]},
        {"time_ms": 1200,   "notes": [B]},
        {"time_ms": 1400,   "notes": [C5]},
    ]
))

songs.append(Song(
    name="Simple ascend and descend fast",
    events=[
        {"time_ms": 0,      "notes": [C]},
        {"time_ms": 50,     "notes": [D]},
        {"time_ms": 100,    "notes": [E]},
        {"time_ms": 150,    "notes": [F]},
        {"time_ms": 200,    "notes": [G]},
        {"time_ms": 250,    "notes": [A]},
        {"time_ms": 300,    "notes": [B]},
        {"time_ms": 350,    "notes": [C5]},
    ]
))

songs.append(Song(
    name="Test Melody",
    events=[
        {"time_ms": 0,    "notes": [C]},
        {"time_ms": 500,  "notes": [E]}
    ],
))
