# k4single.py
#
# written by: Oliver Cordes 2023-02-01
# changed by: Oliver Cordes 2023-02-01


class K4SingleInstrument(object):
    def __init__(self, data):
        self._data = data

    @property
    def name(self):
        return self._data[0:10].decode('utf8').strip()

