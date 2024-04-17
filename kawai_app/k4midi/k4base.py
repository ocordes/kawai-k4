# k4base.py
#
# written by: Oliver Cordes 2023-04-10
# changed by: Oliver Cordes 2024-04-17

from typing import ByteString

import copy

_debug = False

class K4Base(object):
    id = 0x00 # some defaults
    size =  0 # some defaults

    #_data: ByteString = None

    def __init__(self, data):
        self._data = bytearray(data)

        # self.verify_checksum()

    def verify_checksum(self):
        sum : int = 0
        for i in self._data[:-1]:
            sum += i
        sum += 0xa5
        sum &= 0b1111111

        if _debug:
            print(f'checksum check: {sum:x} == {self._data[-1]:x} = {sum == self._data[-1]}')
        return sum == self._data[-1]


    # update_checksum
    #
    # updates the checksum field (last byte in dataarray)
    # chksum = sum(b[0]-b[129]) + hex A5 -> last 7 bits
    def update_checksum(self):
        sum = 0
        for i in self._data[:-1]:
            sum += i
        sum += 0xa5
        sum &= 0b1111111

        if _debug:
            print(f'change checksum from {self._data[-1]:x} to {sum:x}')
        self._data[-1] = sum


    # update_data
    #
    # update_data is called after the data has changed
    def update_data(self):
        pass


    # most functions can be used by templates
    # which defines the offset, shift-right(read)
    # shift-left(set) and mask
    def func_template(ofs, shift=0, mask=255, correct=0):
        def set_f(self, newval):
            if _debug:
                print(f'set value @{ofs}: {newval}')
            # print(f'mask={mask}, shift={shift} correct={correct}')

            newval = newval - correct
            nmask = ~(mask << shift)
            # print(nmask)

            # print(f'oldval={self._data[ofs]:0b} {self._data[ofs]}')
            d = self._data[ofs] & nmask  # clear all bits

            # print(f'oldval(cleared)={d:0b}')
            nnewval = newval << shift
            # print(f'val(shifted)={nnewval:0b}')
            d = d | nnewval
            if _debug:                
                print(f'newval={d:0b} {d}')
            # set the new data
            self._data[ofs] = d

            self.update_checksum()

        def get_f(self):
            b = ((self._data[ofs] >> shift) & mask) + correct
            if _debug:
                print(f'get value @{ofs} {self._data[ofs]} {self._data[ofs]:0b}')
                print(f'mask={mask}, shift={shift} correct={correct} -> {b} {b:0b}')
            return b

        return get_f, set_f


    # save
    #
    # saves the data block into filename, the file format is:
    # 0      id
    # 1-2    size in bytes
    # 3-...  data block
    def save(self, filename):
        # fix any error made before ;-)
        self.update_checksum()

        print(f'Save data to {filename} ...')

        with open(filename, 'bw') as f:
            _ = f.write(str(self.id.to_bytes(1)))
            _ = f.write(str(len(self._data).to_bytes(2)))
            _ = f.write(str(self._data))


    # load
    #
    # loads the data from filename, the consistency is checked by the id and the size
    def load(self, filename):
        print(f'Load data from {filename} ...')

        with open(filename, 'rb') as f:
            b = int(f.read(1)[0])
            if b == self.id:
                dsize = int.from_bytes(f.read(2))
                if dsize == len(self._data):
                    olddata = self._data
                    self._data = bytearray(f.read(dsize))
                    check = self.verify_checksum()
                    if not check:
                        print('Checksum error while reading data from disk!')
                        self._data = olddata    # restore old data if failing...
                    return check

        return False


    def raw_save(self, f):
        # fix any error made before ;-)
        self.update_checksum()
        f.write(self._data)


    def copy(self):
        return copy.copy(self._data)


    def paste(self, data) -> None:
        if data is None: return

        if len(data) == len(self._data):
            self._data = copy.copy(data)
            self.update_data()


# k4BaseSection
#
# the class is used for sections of the binary data
# it uses the same data block as the main class
# but refers to a specific part of the data block by an offset
# changes of a section property are directly reflected in the data block

class K4BaseSection(object):
    def __init__(self, data, ofs=0):
        self._data = data
        self._ofs = ofs

    def __len__(self):
        return 0


    # update_data
    #
    # update_data is called after the data has changed, it
    # overwrites the data block with the new data
    def update_data(self, data):
        self._data = data   # update the data block


    # get_data
    #
    # returns the bytes of the section
    def get_data(self):
        return self._data[self._ofs:self._ofs+len(self)]

    # paste
    #
    # paste the section data into the data block
    def paste(self, section):
        if section is None: return

        # copy the section data into the data block
        data = section.get_data()   # get binary data
        self._data[self._ofs:self._ofs+len(self)] = data

        
    # func_template
    #
    # function template to gegerate the getter and setter functions for the properties
    def func_template(ofs, shift=0, mask=255, correct=0):
        def set_f(self, newval):
            if _debug:
                print(f'set value @{self._ofs+ofs}: {newval}')
            # print(f'mask={mask}, shift={shift} correct={correct}')

            newval = newval - correct
            nmask = ~(mask << shift)
            # print(nmask)

            # print(f'oldval={self._data[self._ofs+ofs]:0b} {self._data[self._ofs+ofs]}')
            d = self._data[self._ofs+ofs] & nmask  # clear all bits

            # print(f'oldval(cleared)={d:0b}')
            nnewval = newval << shift
            # print(f'val(shifted)={nnewval:0b}')
            d = d | nnewval
            if _debug:                
                print(f'newval={d:0b} {d}')
            # set the new data
            self._data[self._ofs+ofs] = d


        def get_f(self):
            b = ((self._data[self._ofs+ofs] >> shift) & mask) + correct
            if _debug:
                print(f'get value @{ofs} {self._data[self._ofs+ofs]} {self._data[self._ofs+ofs]:0b}')
                print(f'mask={mask}, shift={shift} correct={correct} -> {b} {b:0b}')
            return b

        return get_f, set_f
    