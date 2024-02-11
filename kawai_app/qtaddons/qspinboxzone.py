# qspinboxzone.py
#
# written by: Oliver Cordes 2023-02-11
# changed by: Oliver Cordes 2024-02-11

from PySide6.QtWidgets import QSpinBox


k4_zone_keys = ['C-2', 'Cis-2', 'D-2', 'Dis-2', 'E-2', 'F-2', 'Fis-2', 'G-2', 'Gis-2', 'A-2', 'b-2', 'H-2',
           'C-1', 'Cis-1', 'D-1', 'Dis-1', 'E-1', 'F-1', 'Fis-1', 'G-1', 'Gis-1', 'A-1', 'b-1', 'H-1',
           'C0', 'Cis0', 'D0', 'Dis0', 'E0', 'F0', 'Fis0', 'G0', 'Gis0', 'A0', 'b0', 'H0',
           'C1', 'Cis1', 'D1', 'Dis1', 'E1', 'F1', 'Fis1', 'G1', 'Gis1', 'A1', 'b1', 'H1',
           'C2', 'Cis2', 'D2', 'Dis2', 'E2', 'F2', 'Fis2', 'G2', 'Gis2', 'A2', 'b2', 'H2',
           'C3', 'Cis3', 'D3', 'Dis3', 'E3', 'F3', 'Fis3', 'G3', 'Gis3', 'A3', 'b3', 'H3',
           'C4', 'Cis4', 'D4', 'Dis4', 'E4', 'F4', 'Fis4', 'G4', 'Gis4', 'A4', 'b4', 'H4',
           'C5', 'Cis5', 'D5', 'Dis5', 'E5', 'F5', 'Fis5', 'G5', 'Gis5', 'A5', 'b5', 'H5',
           'C6', 'Cis6', 'D6', 'Dis6', 'E6', 'F6', 'Fis6', 'G6', 'Gis6', 'A6', 'b6', 'H6',
           'C7', 'Cis7', 'D7', 'Dis7', 'E7', 'F7', 'Fis7', 'G7', 'Gis7', 'A7', 'b7', 'H7',
           'C8', 'Cis8', 'D8', 'Dis8', 'E8', 'F8', 'Fis8', 'G8' ]
           


class QSpinBoxZone(QSpinBox):
    def textFromValue(self, val):
        if val >= len(k4_zone_keys):
            return 'err'
        else:
            return k4_zone_keys[val]

