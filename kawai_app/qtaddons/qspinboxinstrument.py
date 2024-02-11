# qspinboxinstrument.py
#
# written by: Oliver Cordes 2024-02-11
# changed by: Oliver Cordes 2023-02-11

from PySide6.QtWidgets import QSpinBox


class QSpinBoxInstrument(QSpinBox):
    def textFromValue(self, val):
        if val >= len(instrument_list):
            return 'err'
        else:
            return instrument_list[val]


instrument_list = []

def set_instruments(instruments):
    global instrument_list
    instrument_list = instruments
