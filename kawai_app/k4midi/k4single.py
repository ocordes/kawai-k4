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

    @property
    def volume(self):
        return self._data[10]

    @property
    def effect(self):
        return self._data[11]+1

    @property
    def out_select(self):
        return self._data[12]

    @property
    def source_mode(self):
        return self._data[13] & 0b11

    @property
    def poly_mode(self):
        return (self._data[13] >> 2) & 0b11

    @property
    def am12(self):
        return (self._data[13] >> 4) & 1

    @property
    def am34(self):
        return (self._data[13] >> 5) & 1

    @property
    def mute_s1(self):
        return self._data[14] & 1

    @property
    def mute_s2(self):
        return (self._data[14] >> 1 ) & 1

    @property
    def mute_s3(self):
        return (self._data[14] >> 2 ) & 1

    @property
    def mute_s4(self):
        return (self._data[14] >> 3 ) & 1

    @property
    def vib_shape(self):
        return (self._data[14] >> 4 ) & 0b11

    @property
    def pitch_bend(self):
        return self._data[15] & 0b1111

    @property
    def wheel_assign(self):
        return (self._data[15] >> 4 ) & 0b11

    @property
    def vib_speed(self):
        return self._data[16]

    @property
    def wheel_dep(self):
        return self._data[17]

    @property
    def auto_bend_time(self):
        return self._data[18]

    @property
    def auto_bend_depth(self):
        return self._data[19]

    @property
    def auto_bend_ks_time(self):
        return self._data[20]
    
    @property
    def auto_bend_vel_dep(self):
        return self._data[21]

    @property
    def vib_prs_vib(self):
        return self._data[22]

    @property
    def vibrato_dep(self):
        return self._data[23]

    @property
    def lfo_shape(self):
        return self._data[24]

    @property
    def lfo_speed(self):
        return self._data[25]

    @property
    def lfo_delay(self):
        return self._data[26]
    
    @property
    def lfo_dep(self):
        return self._data[27]

    @property
    def lfo_prs_dep(self):
        return self._data[28]

    @property
    def pres_freq(self):
        return self._data[29]


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