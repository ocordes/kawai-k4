# k4dump.py
#
# written by: Oliver Cordes 2023-01-29
# changed by: Oliver Cordes 2023-01-29

from k4midi.midifile import MidiFile

from k4midi.k4single import K4SingleInstrument


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

        #self._trackdata = self.get_track(0)



    def parse_midi_stream(self):
        
        results = None
        track_nr = 0

        midi_channel_prefix = 0

        while (track_nr < self._tracks) and (results is None):
            data = self.get_track(track_nr)
        
            while len(data) > 0:
                delta, data = read_delta(data)
                if data[0] == 0xff:
                    tlen = data[2]

                    if data[1] == 0x20:
                        midi_channel_prefix = data[3]
                        print(f'{delta:d} midi_channel_prefix={midi_channel_prefix}')
                    elif data[1] in range(0x01, 0x08):
                        # text events 
                        text = data[3:3+tlen]
                        print(f'{delta} text={text}')
                    elif data[1] == 0x2f:
                        print('End of track')
                    elif data[1] == 0x51:
                        # FF 51 03 tttttt Set Tempo
                        tttttt = data[3:7]
                    elif data[1] == 0x58:
                        # 58 04 nn dd cc bb Time Signature
                        nn = data[3]
                        dd = data[4]
                        cc = data[5]
                        bb = data[6]                    
                    else:
                        raise ValueError(f'Unknown byte 0x{data[1]:x}')
                    data = data[3+tlen:]
                elif data[0] == 0xf0:
                    # sysex message
                    length, data = read_delta(data[1:])
                    results = self.k4_dump(data)
                    data = data[length:]
                else:
                    raise ValueError(f'Unknown byte 0x{data[0]:x}')

            track_nr += 1

        return results


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

        data = data[7:]
        results = {}
        results['function'] = function
        if function == 0x22:
            # full dump
            single = []
            for nr in range(64):
                i = K4SingleInstrument(data[nr*131:(nr+1)*131])
                single.append(i)
            results['single_instruments'] = single

        return results

        

