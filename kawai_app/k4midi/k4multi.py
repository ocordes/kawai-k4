# k4multi.py
#
# written by: Oliver Cordes 2023-04-10
# changed by: Oliver Cordes 2024-02-13

from k4midi.k4base import K4Base, K4BaseSection


class K4MultiInstrumentSection(K4BaseSection):
    single = property(*K4BaseSection.func_template(0))
    zone_low = property(*K4BaseSection.func_template(1))
    zone_high = property(*K4BaseSection.func_template(2))
    rec_chan = property(
        *K4BaseSection.func_template(3, correct=1, mask=0b1111))
    vel_sw = property(*K4BaseSection.func_template(3, shift=4, mask=0b11))
    mute = property(*K4BaseSection.func_template(3, shift=6, mask=0b1))
    out_sel = property(*K4BaseSection.func_template(4, mask=0b111))
    mode = property(*K4BaseSection.func_template(4, shift=3, mask=0b11))
    level = property(*K4BaseSection.func_template(5))
    transpose = property(*K4BaseSection.func_template(6, correct=-24))
    tune = property(*K4BaseSection.func_template(7, correct=-50))

    def __len__(self):
        return 8


class K4MultiInstrument(K4Base):
    id = 0x11
    size = 77

    def __init__(self, data):
        super().__init__(data)  

        self.sections = [K4MultiInstrumentSection(self._data, ofs=12),
                         K4MultiInstrumentSection(self._data, ofs=20),
                         K4MultiInstrumentSection(self._data, ofs=28),
                         K4MultiInstrumentSection(self._data, ofs=36),
                         K4MultiInstrumentSection(self._data, ofs=44),
                         K4MultiInstrumentSection(self._data, ofs=52),
                         K4MultiInstrumentSection(self._data, ofs=60),
                         K4MultiInstrumentSection(self._data, ofs=68)]


    def update_data(self):
        for s in self.sections:
            s.update_data(self._data)

    @property
    def name(self):
        return self._data[0:10].decode('utf8').strip()

    @name.setter
    def name(self, val):
        while len(val) < 10:
            val = val + ' '
        self._data[0:10] = bytearray(val, 'utf8')

    # easy template definitions
    volume      = property(*K4Base.func_template(10))
    effect      = property(*K4Base.func_template(11, correct=1))
    
    # section 1
    # the section defintions are moved into a subclass

    #sect1_single    = property(*K4Base.func_template(12))
    #sect1_zone_low  = property(*K4Base.func_template(13))
    #sect1_zone_high = property(*K4Base.func_template(14))   
    #sect1_rec_chan  = property(*K4Base.func_template(15, correct=1, mask=0b1111))
    #sect1_vel_sw    = property(*K4Base.func_template(15, shift=4, mask=0b11))
    #sect1_mute      = property(*K4Base.func_template(15, shift=6, mask=0b1) )
    #sect1_out_sel   = property(*K4Base.func_template(16, mask=0b111))
    #sect1_mode      = property(*K4Base.func_template(16, shift=3, mask=0b11))
    #sect1_level     = property(*K4Base.func_template(17))
    #sect1_transpose = property(*K4Base.func_template(18, correct=-24))
    #sect1_tune      = property(*K4Base.func_template(19, correct=-50))
