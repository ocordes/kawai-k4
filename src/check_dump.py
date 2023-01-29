import os

from midifile import MidiFile

from k4dump import K4Dump


# main

mf = K4Dump('k4.mid')

print(mf.version())

mf.parse_midi_stream()

#print(len(data), type(data))
#print(f'{data[0]:x}')
