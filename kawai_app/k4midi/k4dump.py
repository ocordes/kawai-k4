# k4dump.py
#
# written by: Oliver Cordes 2023-01-29
# changed by: Oliver Cordes 2023-05-06


from k4midi.midifile import MidiFile

from k4midi.k4single import K4SingleInstrument
from k4midi.k4multi import K4MultiInstrument
from k4midi.k4drums import K4DrumCommon, K4Drums
from k4midi.k4effects import K4Effects

_debug = False

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

        self._header = None

        # read the dump data
        self._results = self.parse_midi_stream()


    @property
    def data(self):
        return self._results

        
    def parse_midi_stream(self):
        # if not MIDI file, then treat as sysex file

        if not self._is_midi:
            results = self.k4_dump(self._data[1:])
            return results

        # assume data is a MIDI file
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
                        if _debug:
                            print(f'{delta:d} midi_channel_prefix={midi_channel_prefix}')
                    elif data[1] in range(0x01, 0x08):
                        # text events 
                        text = data[3:3+tlen]
                        if _debug:
                            print(f'{delta} text={text}')
                    elif data[1] == 0x2f:
                        if _debug:
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

            self._results = results

        return results


    def k4_dump(self, data):
        vendor = data[0]
        channel  = data[1]
        function = data[2]
        group = data[3]
        machine = data[4]
        sub_status1 = data[5]
        sub_status2 = data[6]

        if _debug:
            print(f'vendor={vendor:x}')
            print(f'channel={channel:x}')
            print(f'function={function:x}')
            print(f'group={group:x}')
            print(f'machine={machine:x}')
            print(f'sub_status1={sub_status1:x}')
            print(f'sub_status2={sub_status2:x}')

        self._header = bytearray(data[:7])
        

        data = data[7:]
        results = {}
        results['function'] = function
        if function == 0x22:
            # full dump

            # 64 single instruments
            single = []
            size = K4SingleInstrument.size
            for nr in range(64):
                i = K4SingleInstrument(data[nr*size:(nr+1)*size])
                if not i.verify_checksum():
                    print(f'Checksum mismatched for single instrument nr. {nr+1}!')
                single.append(i)
            results['single_instruments'] = single
            data = data[(size*64):]

            # 64 multi instrumens
            multi = []
            size = K4MultiInstrument.size
            for nr in range(64):
                i = K4MultiInstrument(data[nr*size:(nr+1)*size])
                if not i.verify_checksum():
                    print(f'Checksum mismatched for multi instrument nr. {nr+1}!')
                multi.append(i)
            results['multi_instruments'] = multi
            data = data[(size*64):]

            # 1 drum common
            size = K4DrumCommon.size
            i = K4DrumCommon(data[:size])
            if not i.verify_checksum():
                print(f'Checksum mismatched for drum common!')
            results['drum_common'] = i
            data = data[size:]

            # 61 drums
            size = K4Drums.size
            drums = []
            for nr in range(61):
                i = K4Drums(data[nr*size:(nr+1)*size])
                if not i.verify_checksum():
                    print(f'Checksum mismatched for drums nr. {nr+1}!')
                drums.append(i)
            results['drums'] = drums
            data = data[(size*61):]
            
            # 32 effects
            size = K4Effects.size
            effects = []
            for nr in range(32):
                i = K4Effects(data[nr*size:(nr+1)*size])
                if not i.verify_checksum():
                    print(f'Checksum mismatched for effects nr. {nr+1}!')
                effects.append(i)
            results['effects'] = effects
            data = data[(size*32):]

            #print(f'Bytes left over: {len(data)}')

        return results


    def save_file(self, filename, start_header, end_header):
        with open(filename, 'wb') as f:
            # write start bytes
            f.write(start_header)
            
            f.write(self._header)

            for i in self._results['single_instruments']:
                 i.raw_save(f)
            for i in self._results['multi_instruments']:
                i.raw_save(f)
            self._results['drum_common'].raw_save(f)
            for i in self._results['drums']:
                i.raw_save(f)
            for i in self._results['effects']:
                i.raw_save(f)

            # write ending bytes
            f.write(end_header)
        
        

    def save_midifile(self, filename):

        midi_header = b'\x4d\x54\x68\x64\x00\x00\x00\x06\x00\x01\x00\x02\x01\xe0\x4d\x54' \
                        +  b'\x72\x6b\x00\x00\x00\x13\x00\xff\x58\x04\x04\x02\x18\x08\x00\xff' \
                        +  b'\x51\x03\x07\xa1\x20\x00\xff\x2f\x00\x4d\x54\x72\x6b\x00\x00\x3b' \
                        +  b'\x1a\x00\xf0\xf6\x12' 
        midi_end = b'\xf7\x00\xff\x2f\x00'

        self.save_file(filename, midi_header, midi_end)


    def save_sysexfile(self, filename):        
        self.save_file(filename, b'\xf0', b'\xf7')
