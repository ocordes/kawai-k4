# k4drums.py
#
# written by: Oliver Cordes 2023-04-10
# changed by: Oliver Cordes 2023-04-10

from k4midi.k4base import K4Base


class K4DrumCommon(K4Base):
    id = 0x12
    size = 11


class K4Drums(K4Base):
    id = 0x13
    size = 11
