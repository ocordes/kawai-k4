# qspinboxchannel.py
#
# written by: Oliver Cordes 2024-02-11
# changed by: Oliver Cordes 2024-02-11

from PySide6.QtWidgets import QSpinBox


class QSpinBoxChannel(QSpinBox):
    def textFromValue(self, val):
        return chr(ord('A')+val)

