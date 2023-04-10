# k4base.py
#
# written by: Oliver Cordes 2023-04-10
# changed by: Oliver Cordes 2023-04-10


class K4Base(object):
    def __init__(self, data):
        self._data = bytearray(data)

        # self.verify_checksum()

    def verify_checksum(self):
        sum = 0
        for i in self._data[:-1]:
            sum += i
        sum += 0xa5
        sum &= 0b1111111

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

        # print(f'change checksum from {self._data[-1]:x} to {sum:x}')
        self._data[-1] = sum

    # most functions can be used by templates
    # which defines the offset, shift-right(read)
    # shift-left(set) and mask

    def func_template(ofs, shift=0, mask=255, correct=0):
        def set_f(self, newval):
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
            print(f'newval={d:0b} {d}')
            # set the new data
            self._data[ofs] = d

            self.update_checksum()

        def get_f(self):
            b = ((self._data[ofs] >> shift) & mask) + correct
            print(f'get value @{ofs} {self._data[ofs]} {self._data[ofs]:0b}')
            print(f'mask={mask}, shift={shift} correct={correct} -> {b} {b:0b}')
            return b

        return get_f, set_f
