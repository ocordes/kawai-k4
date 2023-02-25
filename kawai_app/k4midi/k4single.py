# k4single.py
#
# written by: Oliver Cordes 2023-02-01
# changed by: Oliver Cordes 2023-02-25


class K4SingleInstrument(object):
    def __init__(self, data):
        self._data = bytearray(data)

    # most functions can be used by templates
    # which defines the offset, shift-right(read)
    # shift-left(set) and mask

    def func_template(ofs, shift=0, mask=255, correct=0):
        def set_f(self, newval):
            print(f'set value @{ofs}: {newval}')
            print(f'mask={mask}, shift={shift} correct={correct}')

            newval = newval - correct
            nmask = ~(mask << shift)
            print(nmask)

            print(f'oldval={self._data[ofs]:0b} {self._data[ofs]}')
            d = self._data[ofs] & nmask # clear all bits

            print(f'oldval(cleared)={d:0b}')
            nnewval = newval << shift
            print(f'val(shifted)={nnewval:0b}')
            d = d | nnewval
            print(f'newval={d:0b} {d}')
            # set the new data
            self._data[ofs] = d
                    
        def get_f(self):
            b = ((self._data[ofs] >> shift) & mask) + correct
            print(f'get value @{ofs} {self._data[ofs]} {self._data[ofs]:0b}')
            print(f'mask={mask}, shift={shift} correct={correct} -> {b} {b:0b}')
            return b

        return get_f, set_f

    
    @property
    def name(self):
        return self._data[0:10].decode('utf8').strip()

    @name.setter
    def name(self, val):
        while len(val) < 10: val = val + ' '
        self._data[0:10] = bytearray(val, 'utf8')

    # easy template definitions
    volume      = property(*func_template(10))
    effect      = property(*func_template(11,correct=1))
    out_select  = property(*func_template(12))
    source_mode = property(*func_template(13, mask=0b11))
    poly_mode = property(*func_template(13, shift=2, mask=0b11))
    am12 = property(*func_template(13, shift=4, mask=0b1))
    am34 = property(*func_template(13, shift=5, mask=0b1))
    mute_s1 = property(*func_template(14, shift=0, mask=0b1))
    mute_s2 = property(*func_template(14, shift=1, mask=0b1))
    mute_s3 = property(*func_template(14, shift=2, mask=0b1))
    mute_s4 = property(*func_template(14, shift=3, mask=0b1))
    vib_shape = property(*func_template(14, shift=4, mask=0b11))
    pitch_bend = property(*func_template(15, shift=0, mask=0b1111))
    wheel_assign = property(*func_template(15, shift=4, mask=0b11))
    vib_speed = property(*func_template(16))
    wheel_dep = property(*func_template(17, correct=-50))
    auto_bend_time = property(*func_template(18))
    auto_bend_depth = property(*func_template(19, correct=-50))
    auto_bend_ks_time = property(*func_template(20, correct=-50))
    auto_bend_vel_dep = property(*func_template(21, correct=-50))
    vib_prs_vib = property(*func_template(22, correct=-50))
    vibrato_dep = property(*func_template(23, correct=-50))
    lfo_shape = property(*func_template(24, mask=0b11))
    lfo_speed = property(*func_template(25))
    lfo_delay = property(*func_template(26))
    lfo_dep = property(*func_template(27, correct=-50))
    lfo_prs_dep = property(*func_template(28, correct=-50))
    pres_freq = property(*func_template(29, correct=-50))


    # sources

    # Source 1
    @property
    def s1_delay(self):
        return self._data[30] 

    @property
    def s1_wave_select(self):
        return ((self._data[34] & 1)<<7 | (self._data[38]))

    @property    
    def s1_ks_curve(self):
        return (self._data[34] >> 4) + 1

    @property
    def s1_coarse(self):
        return (self._data[42] & 0b111111) - 24

    @property
    def s1_key_track(self):
        return self._data[42] >> 6

    @property    
    def s1_fix(self):
        return self._data[46]

    @property
    def s1_fine(self):
        return self._data[50] - 50

    @property    
    def s1_prs_frq(self):
        return self._data[54] & 1

    @property
    def s1_vib_bend(self):
        return (self._data[54] >> 1) & 1

    @property
    def s1_vel_curve(self):
        return ((self._data[54] >> 2) & 0b111) + 1


    # Source 2
    @property
    def s2_delay(self):
        return self._data[31] 

    @property
    def s2_wave_select(self):
        return ((self._data[35] & 1)<<7 | (self._data[39]))

    @property    
    def s2_ks_curve(self):
        return (self._data[35] >> 4) + 1

    @property
    def s2_coarse(self):
        return (self._data[43] & 0b111111) - 24

    @property
    def s2_key_track(self):
        return self._data[43] >> 6

    @property    
    def s2_fix(self):
        return self._data[47]

    @property
    def s2_fine(self):
        return self._data[51] - 50

    @property    
    def s2_prs_frq(self):
        return self._data[55] & 1

    @property
    def s2_vib_bend(self):
        return (self._data[55] >> 1) & 1

    @property
    def s2_vel_curve(self):
        return ((self._data[55] >> 2) & 0b111) + 1


    # Source 3
    @property
    def s3_delay(self):
        return self._data[32] 

    @property
    def s3_wave_select(self):
        return ((self._data[36] & 1)<<7 | (self._data[40]))

    @property    
    def s3_ks_curve(self):
        return (self._data[36] >> 4) + 1

    @property
    def s3_coarse(self):
        return (self._data[44] & 0b111111) - 24

    @property
    def s3_key_track(self):
        return self._data[44] >> 6

    @property    
    def s3_fix(self):
        return self._data[48]

    @property
    def s3_fine(self):
        return self._data[52] - 50

    @property    
    def s3_prs_frq(self):
        return self._data[56] & 1

    @property
    def s3_vib_bend(self):
        return (self._data[56] >> 1) & 1

    @property
    def s3_vel_curve(self):
        return ((self._data[56] >> 2) & 0b111) + 1


    # Source 4
    @property
    def s4_delay(self):
        return self._data[33] 

    @property
    def s4_wave_select(self):
        return ((self._data[37] & 1)<<7 | (self._data[41]))

    @property    
    def s4_ks_curve(self):
        return (self._data[37] >> 4) + 1

    @property
    def s4_coarse(self):
        return (self._data[45] & 0b111111) - 24

    @property
    def s4_key_track(self):
        return self._data[45] >> 6

    @property    
    def s4_fix(self):
        return self._data[49]

    @property
    def s4_fine(self):
        return self._data[53] - 50

    @property    
    def s4_prs_frq(self):
        return self._data[57] & 1

    @property
    def s4_vib_bend(self):
        return (self._data[57] >> 1) & 1

    @property
    def s4_vel_curve(self):
        return ((self._data[57] >> 2) & 0b111) + 1


    # DCA 1
    @property
    def s1_envelope_level(self):
        return self._data[58]

    @property
    def s1_envelope_attack(self):
        return self._data[62]

    @property
    def s1_envelope_decay(self):
        return self._data[66]

    @property
    def s1_envelope_sustain(self):
        return self._data[70]

    @property
    def s1_envelope_release(self):
        return self._data[74]

    @property
    def s1_level_mod_vel(self):
        return self._data[78] - 50 

    @property
    def s1_level_mod_prs(self):
        return self._data[82] - 50 

    @property
    def s1_level_mod_ks(self):
        return self._data[86] - 50 

    @property
    def s1_time_mod_on_vel(self):
        return self._data[90] - 50 

    @property
    def s1_time_mod_off_vel(self):
        return self._data[94] - 50 

    @property
    def s1_time_mod_ks(self):
        return self._data[98] - 50


    # DCA 2
    @property
    def s2_envelope_level(self):
        return self._data[59]

    @property
    def s2_envelope_attack(self):
        return self._data[63]

    @property
    def s2_envelope_decay(self):
        return self._data[67]

    @property
    def s2_envelope_sustain(self):
        return self._data[71]

    @property
    def s2_envelope_release(self):
        return self._data[75]

    @property
    def s2_level_mod_vel(self):
        return self._data[79] - 50 

    @property
    def s2_level_mod_prs(self):
        return self._data[83] - 50 

    @property
    def s2_level_mod_ks(self):
        return self._data[87] - 50 

    @property
    def s2_time_mod_on_vel(self):
        return self._data[91] - 50

    @property
    def s2_time_mod_off_vel(self):
        return self._data[95] - 50 

    @property
    def s2_time_mod_ks(self):
        return self._data[99] - 50 

    # DCA 3
    @property
    def s3_envelope_level(self):
        return self._data[60]

    @property
    def s3_envelope_attack(self):
        return self._data[64]

    @property
    def s3_envelope_decay(self):
        return self._data[68]

    @property
    def s3_envelope_sustain(self):
        return self._data[72]

    @property
    def s3_envelope_release(self):
        return self._data[76]

    @property
    def s3_level_mod_vel(self):
        return self._data[80] - 50 

    @property
    def s3_level_mod_prs(self):
        return self._data[84] - 50

    @property
    def s3_level_mod_ks(self):
        return self._data[88] - 50 

    @property
    def s3_time_mod_on_vel(self):
        return self._data[92] - 50 

    @property
    def s3_time_mod_off_vel(self):
        return self._data[96] - 50

    @property
    def s3_time_mod_ks(self):
        return self._data[100] - 50


    # DCA 4
    @property
    def s4_envelope_level(self):
        return self._data[61]

    @property
    def s4_envelope_attack(self):
        return self._data[65]

    @property
    def s4_envelope_decay(self):
        return self._data[69]

    @property
    def s4_envelope_sustain(self):
        return self._data[73]

    @property
    def s4_envelope_release(self):
        return self._data[77]

    @property
    def s4_level_mod_vel(self):
        return self._data[81] - 50

    @property
    def s4_level_mod_prs(self):
        return self._data[85] - 50

    @property
    def s4_level_mod_ks(self):
        return self._data[89] - 50

    @property
    def s4_time_mod_on_vel(self):
        return self._data[93] - 50

    @property
    def s4_time_mod_off_vel(self):
        return self._data[97] - 50

    @property
    def s4_time_mod_ks(self):
        return self._data[101] - 50
