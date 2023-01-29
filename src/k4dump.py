# k4dump.py
#
# written by: Oliver Cordes 2023-01-29
# changed by: Oliver Cordes 2023-01-29

from midifile import MidiFile


def read_delta(bytes):
    delta = 0
    rbytes = 0

    while True:
        b = bytes[0]
        #print('1', delta, b, b & 0x7f)
        bytes = bytes[1:]
        delta = (delta << 7) | (b & 0x7f)
        if b < 0x80:
            return delta, bytes



class K4Dump(MidiFile):
    def __init__(self, filename):
        MidiFile.__init__(self, filename)

        self._trackdata = self.get_track(0)



    def parse_midi_stream(self):
        ofs = 0

        midi_channel_prefix = 0

        data = self._trackdata
        #while ofs < len(self._trackdata):
        while len(data) > 0:
            delta, data = read_delta(data)
            if data[0] == 0xff:
                if data[1] == 0x20:
                    if data[2] == 0x01:
                        midi_channel_prefix = data[3]
                        data = data[4:]
                        print(f'{delta:d} midi_channel_prefix={midi_channel_prefix}')
                #elif data[1] == 0x01:
                elif data[1] in range(0x01, 0x08):
                    # text events 
                    tlen = data[2]
                    text = data[3:3+tlen]
                    print(f'{delta} text={text}')
                    data = data[3+tlen:]
                elif data[1] == 0x2f:
                    if data[2] == 0:
                        print('End of track')
                        data = data[3:]
                else:
                    raise ValueError(f'Unknown byte {data[1]:x}')
            elif data[0] == 0xf0:
                # sysex message
                length, data = read_delta(data[1:])
                self.k4_dump(data)
                data = data[length:]
            else:
                raise ValueError(f'Unknown byte {data[0]:x}')


    def k4_dump(self, data):
        vendor = data[0]
        channel  = data[1]
        function = data[2]
        group = data[3]
        machine = data[4]
        sub_status1 = data[5]
        sub_status2 = data[6]
        print(f'vendor={vendor:x}')
        print(f'channel={channel:x}')
        print(f'function={function:x}')
        print(f'group={group:x}')
        print(f'machine={machine:x}')
        print(f'sub_status1={sub_status1:x}')
        print(f'sub_status2={sub_status2:x}')
        

