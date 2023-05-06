# qspinboxeffect.py
#
# written by: Oliver Cordes 2023-04-15
# changed by: Oliver Cordes 2023-04-15

from PySide6.QtWidgets import QSpinBox


class QSpinBoxEffect(QSpinBox):
    def textFromValue(self, val):
        if val >= len(effect_list):
            return 'err'
        else:
            return effect_list[val]


effect_list = [
    'REVERB 1',
    'REVERB 2',
    'REVERB 3',
    'REVERB 4',
    'GATE REVERB',
    'REVERSE GATE',
    'Normal DELAY',
    'Stereo PANPOT DELAY',
    'CHORUS',
    'OVER DRIVE + FLANGER',
    'OVER DRIVE + Normal DELAY',
    'OVER DRIVE + REVERB',
    'Normal DELAY + Normal DELAY',
    'Normal DELAY + Stereo PAN. DELAY',
    'CHORUS + Normal DELAY',
    'CHORUS + Stereo PAN. DELAY'
]