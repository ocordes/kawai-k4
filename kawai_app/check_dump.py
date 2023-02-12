import os

from k4midi.midifile import MidiFile

from k4midi.k4dump import K4Dump


# main

#mf = K4Dump('k4.mid')
mf = K4Dump('K4 full dump nach Kauf.mid')

print(mf.version())

results = mf.parse_midi_stream()

if 'single_instruments' in results:
    for si in results['single_instruments']:
        print(si.name)

#print(len(data), type(data))
#print(f'{data[0]:x}')
