# k4multi.py
#
# written by: Oliver Cordes 2023-04-10
# changed by: Oliver Cordes 2023-04-10

from k4midi.k4base import K4Base


class K4MultiInstrument(K4Base):
    id = 0x11
    size = 77

    @property
    def name(self):
        return self._data[0:10].decode('utf8').strip()

    @name.setter
    def name(self, val):
        while len(val) < 10:
            val = val + ' '
        self._data[0:10] = bytearray(val, 'utf8')
