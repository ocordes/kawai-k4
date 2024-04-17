# midifile.py
#
# written by: Oliver Cordes 2023-01-29
# changed by: Oliver Cordes 2024-04-17


def chunk_size(bdata):
    length = bdata[0]*256*256*256
    length += bdata[1]*256*256
    length += bdata[2]*256
    length += bdata[3]

    return length


def two_bytes(bdata):
    tb = bdata[0]*256
    tb += bdata[1]

    return tb


class MidiFile(object):
    def __init__(self, filename):
        self._filename = filename

        self._data = None
        with open(filename, 'rb') as f:
            self._data = f.read()

        if self._data is None:
            raise ValueError(f'Cannot read MIDI file \'{filename}\'')

        self._is_midi = self._data[0:4] == b'MThd'

        print(f'FILE {filename} is MIDI: {self._is_midi}')

        if self._is_midi:
            self._header_length = chunk_size(self._data[4:8])
            self._format = two_bytes(self._data[8:10])
            self._tracks = two_bytes(self._data[10:12])

            print(f'format={self._format}')
            print(f'length={self._header_length}')
            print(f'nr_tracks={self._tracks}')

            self._header_offset = 8 + self._header_length

        else:
            self._header_offset = 0


    def get_track(self, nr):
        # skip to the correct track number

        ofs = self._header_offset

        # simply walk through all tracks
        for tnr in range(nr+1):
            # ofs is at the beginning of a track
            is_track = self._data[ofs:ofs+4] == b'MTrk'

            if not is_track:
                raise ValueError(f'Not a valid track #{tnr}')
            
            track_length = chunk_size(self._data[ofs+4:ofs+8])

            start_track = ofs + 8
            end_track = start_track + track_length

            ofs += 8 + track_length

        # if the loop stops, some variables indicate
        # the data positions of the last track!

        data = self._data[start_track:end_track]
        return data

