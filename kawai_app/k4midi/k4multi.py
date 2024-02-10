# k4multi.py
#
# written by: Oliver Cordes 2023-04-10
# changed by: Oliver Cordes 2024-02-10

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

    # easy template definitions
    volume      = property(*K4Base.func_template(10))
    effect      = property(*K4Base.func_template(11, correct=1))

    # section 1
    sect1_single    = property(*K4Base.func_template(12))
    sect1_zone_low  = property(*K4Base.func_template(13))
    sect1_zone_high = property(*K4Base.func_template(14))   
    sect1_rec_chan  = property(*K4Base.func_template(15, mask=0b1111))
    sect1_vel_sw    = property(*K4Base.func_template(15, shift=4, mask=0b11))
    sect1_mute      = property(*K4Base.func_template(15, shift=6, mask=0b1) )
    sect1_out_sel   = property(*K4Base.func_template(16, mask=0b111))
    sect1_mode      = property(*K4Base.func_template(16, shift=3, mask=0b11))
    sect1_level     = property(*K4Base.func_template(17))
    sect1_transpose = property(*K4Base.func_template(18))
    sect1_tune      = property(*K4Base.func_template(19))

    # section 2
    sect2_single    = property(*K4Base.func_template(20))
    sect2_zone_low  = property(*K4Base.func_template(21))
    sect2_zone_high = property(*K4Base.func_template(22))
    sect2_rec_chan  = property(*K4Base.func_template(23, mask=0b1111))
    sect2_vel_sw    = property(*K4Base.func_template(23, shift=4, mask=0b11))
    sect2_mute      = property(*K4Base.func_template(23, shift=6, mask=0b1))
    sect2_out_sel   = property(*K4Base.func_template(24, mask=0b111))
    sect2_mode      = property(*K4Base.func_template(24, shift=3, mask=0b11))
    sect2_level     = property(*K4Base.func_template(25))
    sect2_transpose = property(*K4Base.func_template(26))
    sect2_tune      = property(*K4Base.func_template(27))

    # section 3
    sect3_single    = property(*K4Base.func_template(28))
    sect3_zone_low  = property(*K4Base.func_template(29))
    sect3_zone_high = property(*K4Base.func_template(30))
    sect3_rec_chan  = property(*K4Base.func_template(31, mask=0b1111))
    sect3_vel_sw    = property(*K4Base.func_template(31, shift=4, mask=0b11))
    sect3_mute      = property(*K4Base.func_template(31, shift=6, mask=0b1))
    sect3_out_sel   = property(*K4Base.func_template(32, mask=0b111))
    sect3_mode      = property(*K4Base.func_template(32, shift=3, mask=0b11))
    sect3_level     = property(*K4Base.func_template(33))
    sect3_transpose = property(*K4Base.func_template(34))
    sect3_tune      = property(*K4Base.func_template(35))

    # section 4
    sect4_single    = property(*K4Base.func_template(36))
    sect4_zone_low  = property(*K4Base.func_template(37))
    sect4_zone_high = property(*K4Base.func_template(38))
    sect4_rec_chan  = property(*K4Base.func_template(39, mask=0b1111))
    sect4_vel_sw    = property(*K4Base.func_template(39, shift=4, mask=0b11))
    sect4_mute      = property(*K4Base.func_template(39, shift=6, mask=0b1))
    sect4_out_sel   = property(*K4Base.func_template(40, mask=0b111))
    sect4_mode      = property(*K4Base.func_template(40, shift=3, mask=0b11))
    sect4_level     = property(*K4Base.func_template(41))
    sect4_transpose = property(*K4Base.func_template(42))
    sect4_tune      = property(*K4Base.func_template(43))

    # section 5
    sect5_single    = property(*K4Base.func_template(44))
    sect5_zone_low  = property(*K4Base.func_template(45))
    sect5_zone_high = property(*K4Base.func_template(46))
    sect5_rec_chan  = property(*K4Base.func_template(47, mask=0b1111))
    sect5_vel_sw    = property(*K4Base.func_template(47, shift=4, mask=0b11))
    sect5_mute      = property(*K4Base.func_template(47, shift=6, mask=0b1))
    sect5_out_sel   = property(*K4Base.func_template(48, mask=0b111))
    sect5_mode      = property(*K4Base.func_template(48, shift=3, mask=0b11))
    sect5_level     = property(*K4Base.func_template(49))
    sect5_transpose = property(*K4Base.func_template(50))
    sect5_tune      = property(*K4Base.func_template(51))

    # section 6
    sect6_single    = property(*K4Base.func_template(52))
    sect6_zone_low  = property(*K4Base.func_template(53))
    sect6_zone_high = property(*K4Base.func_template(54))
    sect6_rec_chan  = property(*K4Base.func_template(55, mask=0b1111))
    sect6_vel_sw    = property(*K4Base.func_template(55, shift=4, mask=0b11))
    sect6_mute      = property(*K4Base.func_template(55, shift=6, mask=0b1))
    sect6_out_sel   = property(*K4Base.func_template(56, mask=0b111))
    sect6_mode      = property(*K4Base.func_template(56, shift=3, mask=0b11))
    sect6_level     = property(*K4Base.func_template(57))
    sect6_transpose = property(*K4Base.func_template(58))
    sect6_tune      = property(*K4Base.func_template(59))

    # section 7
    sect7_single    = property(*K4Base.func_template(60))
    sect7_zone_low  = property(*K4Base.func_template(61))
    sect7_zone_high = property(*K4Base.func_template(62))
    sect7_rec_chan  = property(*K4Base.func_template(63, mask=0b1111))
    sect7_vel_sw    = property(*K4Base.func_template(63, shift=4, mask=0b11))
    sect7_mute      = property(*K4Base.func_template(63, shift=6, mask=0b1))
    sect7_out_sel   = property(*K4Base.func_template(64, mask=0b111))
    sect7_mode      = property(*K4Base.func_template(64, shift=3, mask=0b11))
    sect7_level     = property(*K4Base.func_template(65))
    sect7_transpose = property(*K4Base.func_template(66))
    sect7_tune      = property(*K4Base.func_template(67))

    # section 8
    sect8_single    = property(*K4Base.func_template(68))
    sect8_zone_low  = property(*K4Base.func_template(69))
    sect8_zone_high = property(*K4Base.func_template(70))
    sect8_rec_chan  = property(*K4Base.func_template(71, mask=0b1111))
    sect8_vel_sw    = property(*K4Base.func_template(71, shift=4, mask=0b11))
    sect8_mute      = property(*K4Base.func_template(71, shift=6, mask=0b1))
    sect8_out_sel   = property(*K4Base.func_template(72, mask=0b111))
    sect8_mode      = property(*K4Base.func_template(72, shift=3, mask=0b11))
    sect8_level     = property(*K4Base.func_template(73))
    sect8_transpose = property(*K4Base.func_template(74))
    sect8_tune      = property(*K4Base.func_template(75))