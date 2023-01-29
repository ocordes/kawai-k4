# k4dump.py
#
# written by: Oliver Cordes 2023-01-29
# changed by: Oliver Cordes 2023-01-29

from midifile import MidiFile


class K4Dump(MidiFile):
    def __init__(self, filename):
        MidiFile.__init__(self, filename)

        self._trackdata = self.get_track(0)



    def parse_midi_stream(self):
        ofs = 0

        midi_channel_prefix = 0

        data = self._trackdata
        while ofs < len(self._trackdata):
            delta = data[0]
            data = data[1:]
            if data[0] == 0xff:
                if data[1] == 0x20:
                    if data[2] == 0x01:
                        midi_channel_prefix = data[3]
                        data = data[4:]
                        print(f'{delta:d} midi_channel_prefix={midi_channel_prefix}')
                elif data[1] == 0x01:
                    # text event
                    tlen = data[2]
                    text = data[3:3+tlen]
                    print(f'{delta} text={text}')
                    data = data[3+tlen:]
                else:
                    raise ValueError(f'Unknown byte {data[1]:x} at {ofs+2}')
            else:
                raise ValueError(f'Unknown byte {data[0]:x} at {ofs+2}')

