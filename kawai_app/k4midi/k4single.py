# k4single.py
#
# written by: Oliver Cordes 2023-02-01
# changed by: Oliver Cordes 2023-03-12


class K4SingleInstrument(object):
    id = 0x10
    size = 131
    def __init__(self, data):
        self._data = bytearray(data)

        #self.verify_checksum()


    def verify_checksum(self):
        sum = 0
        for i in self._data[:-1]:
            sum += i
        sum += 0xa5
        sum &= 0b1111111

        return sum == self._data[-1]


    # update_checksum
    #
    # updates the checksum field (last byte in dataarray)
    # chksum = sum(b[0]-b[129]) + hex A5 -> last 7 bits
    def update_checksum(self):
        sum = 0
        for i in self._data[:-1]:
            sum += i
        sum += 0xa5
        sum &= 0b1111111

        #print(f'change checksum from {self._data[-1]:x} to {sum:x}')
        self._data[-1] = sum


    # most functions can be used by templates
    # which defines the offset, shift-right(read)
    # shift-left(set) and mask

    def func_template(ofs, shift=0, mask=255, correct=0):
        def set_f(self, newval):
            print(f'set value @{ofs}: {newval}')
            #print(f'mask={mask}, shift={shift} correct={correct}') 

            newval = newval - correct
            nmask = ~(mask << shift)
            #print(nmask)

            #print(f'oldval={self._data[ofs]:0b} {self._data[ofs]}')
            d = self._data[ofs] & nmask # clear all bits

            #print(f'oldval(cleared)={d:0b}')
            nnewval = newval << shift
            #print(f'val(shifted)={nnewval:0b}')
            d = d | nnewval
            print(f'newval={d:0b} {d}')
            # set the new data
            self._data[ofs] = d

            self.update_checksum()

                    
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


    # Source 1
    s1_delay = property(*func_template(30))
    
    @property
    def s1_wave_select(self):
        return ((self._data[34] & 1)<<7 | (self._data[38]))

    @s1_wave_select.setter
    def s1_wave_select(self, val):
        print(f's1_wave_select={val}')
        self._data[38] = val & 0b1111111
        self._data[34] = (val >> 7) & 1


    s1_ks_curve = property(*func_template(34, shift=4, correct=1))
    s1_coarse = property(*func_template(42, mask=0b111111, correct=-24))
    s1_key_track = property(*func_template(42, shift=6, mask=0b1))
    s1_fix = property(*func_template(46))
    s1_fine = property(*func_template(50, correct=-50))
    s1_prs_freq = property(*func_template(54, mask=0b1))
    s1_vib_bend = property(*func_template(54, shift=1, mask=0b1))
    s1_vel_curve = property(*func_template(54, shift=2, mask=0b111))

    # Source 2
    s2_delay = property(*func_template(31))

    @property
    def s2_wave_select(self):
        return ((self._data[35] & 1) << 7 | (self._data[39]))

    @s2_wave_select.setter
    def s2_wave_select(self, val):
        print(f's2_wave_select={val}')
        self._data[39] = val & 0b1111111
        self._data[35] = (val >> 7) & 1

    s2_ks_curve = property(*func_template(35, shift=4, correct=1))
    s2_coarse = property(*func_template(43, mask=0b111111, correct=-24))
    s2_key_track = property(*func_template(43, shift=6, mask=0b1))
    s2_fix = property(*func_template(47))
    s2_fine = property(*func_template(51, correct=-50))
    s2_prs_freq = property(*func_template(55, mask=0b1))
    s2_vib_bend = property(*func_template(55, shift=1, mask=0b1))
    s2_vel_curve = property(*func_template(55, shift=2, mask=0b111))


    # Source 3
    s3_delay = property(*func_template(31))

    @property
    def s3_wave_select(self):
        return ((self._data[36] & 1) << 7 | (self._data[40]))

    @s3_wave_select.setter
    def s3_wave_select(self, val):
        print(f's3_wave_select={val}')
        self._data[40] = val & 0b1111111
        self._data[36] = (val >> 7) & 1

    s3_ks_curve = property(*func_template(36, shift=4, correct=1))
    s3_coarse = property(*func_template(44, mask=0b111111, correct=-24))
    s3_key_track = property(*func_template(44, shift=6, mask=0b1))
    s3_fix = property(*func_template(48))
    s3_fine = property(*func_template(52, correct=-50))
    s3_prs_freq = property(*func_template(56, mask=0b1))
    s3_vib_bend = property(*func_template(56, shift=1, mask=0b1))
    s3_vel_curve = property(*func_template(56, shift=2, mask=0b111))


    # Source 4
    s4_delay = property(*func_template(31))

    @property
    def s4_wave_select(self):
        return ((self._data[37] & 1) << 7 | (self._data[41]))

    @s4_wave_select.setter
    def s4_wave_select(self, val):
        print(f's4_wave_select={val}')
        self._data[41] = val & 0b1111111
        self._data[37] = (val >> 7) & 1

    s4_ks_curve = property(*func_template(37, shift=4, correct=1))
    s4_coarse = property(*func_template(45, mask=0b111111, correct=-24))
    s4_key_track = property(*func_template(45, shift=6, mask=0b1))
    s4_fix = property(*func_template(49))
    s4_fine = property(*func_template(53, correct=-50))
    s4_prs_freq = property(*func_template(57, mask=0b1))
    s4_vib_bend = property(*func_template(57, shift=1, mask=0b1))
    s4_vel_curve = property(*func_template(57, shift=2, mask=0b111))


    # DCA 1
    s1_envelope_level = property(*func_template(58))
    s1_envelope_attack = property(*func_template(62))
    s1_envelope_decay = property(*func_template(66))
    s1_envelope_sustain = property(*func_template(70))
    s1_envelope_release = property(*func_template(74))
    s1_level_mod_vel = property(*func_template(78, correct=-50))
    s1_level_mod_prs = property(*func_template(82, correct=-50))
    s1_level_mod_ks = property(*func_template(86, correct=-50))
    s1_time_mod_on_vel = property(*func_template(90, correct=-50))
    s1_time_mod_off_vel = property(*func_template(94, correct=-50))
    s1_time_mod_ks = property(*func_template(98, correct=-50))


    # DCA 2
    s2_envelope_level = property(*func_template(59))
    s2_envelope_attack = property(*func_template(63))
    s2_envelope_decay = property(*func_template(67))
    s2_envelope_sustain = property(*func_template(71))
    s2_envelope_release = property(*func_template(75))
    s2_level_mod_vel = property(*func_template(79, correct=-50))
    s2_level_mod_prs = property(*func_template(83, correct=-50))
    s2_level_mod_ks = property(*func_template(87, correct=-50))
    s2_time_mod_on_vel = property(*func_template(91, correct=-50))
    s2_time_mod_off_vel = property(*func_template(95, correct=-50))
    s2_time_mod_ks = property(*func_template(99, correct=-50))


    # DCA 3
    s3_envelope_level = property(*func_template(60))
    s3_envelope_attack = property(*func_template(64))
    s3_envelope_decay = property(*func_template(68))
    s3_envelope_sustain = property(*func_template(72))
    s3_envelope_release = property(*func_template(76))
    s3_level_mod_vel = property(*func_template(80, correct=-50))
    s3_level_mod_prs = property(*func_template(84, correct=-50))
    s3_level_mod_ks = property(*func_template(88, correct=-50))
    s3_time_mod_on_vel = property(*func_template(92, correct=-50))
    s3_time_mod_off_vel = property(*func_template(96, correct=-50))
    s3_time_mod_ks = property(*func_template(100, correct=-50))
    

    # DCA 4
    s4_envelope_level = property(*func_template(61))
    s4_envelope_attack = property(*func_template(65))
    s4_envelope_decay = property(*func_template(69))
    s4_envelope_sustain = property(*func_template(73))
    s4_envelope_release = property(*func_template(77))
    s4_level_mod_vel = property(*func_template(81, correct=-50))
    s4_level_mod_prs = property(*func_template(85, correct=-50))
    s4_level_mod_ks = property(*func_template(89, correct=-50))
    s4_time_mod_on_vel = property(*func_template(93, correct=-50))
    s4_time_mod_off_vel = property(*func_template(97, correct=-50))
    s4_time_mod_ks = property(*func_template(101, correct=-50))
    

    # LFO1/DCF1
    lfo1_cutoff = property(*func_template(102))
    lfo1_resonance = property(*func_template(104, mask=0b111, correct=1))
    lfo1_switch = property(*func_template(104, shift=3, mask=0b1))
    lfo1_cutoff_mod_vel = property(*func_template(106, correct=-50))
    lfo1_cutoff_mod_prs = property(*func_template(108, correct=-50))
    lfo1_cutoff_mod_ks = property(*func_template(110, correct=-50))
    dcf1_env_dep = property(*func_template(112, correct=-50))
    dcf1_env_vel_dep = property(*func_template(114, correct=-50))
    dcf1_env_attack = property(*func_template(116))
    dcf1_env_decay = property(*func_template(118))
    dcf1_env_sustain = property(*func_template(120))
    dcf1_env_release = property(*func_template(122))
    dcf1_time_mod_on_vel = property(*func_template(124, correct=-50))
    dcf1_time_mod_off_vel = property(*func_template(126, correct=-50))
    dcf1_time_mod_ks = property(*func_template(128, correct = -50))

    # LFO2/DCF2
    lfo2_cutoff = property(*func_template(103))
    lfo2_resonance = property(*func_template(105, mask=0b111, correct=1))
    lfo2_switch = property(*func_template(105, shift=3, mask=0b1))
    lfo2_cutoff_mod_vel = property(*func_template(107, correct=-50))
    lfo2_cutoff_mod_prs = property(*func_template(109, correct=-50))
    lfo2_cutoff_mod_ks = property(*func_template(111, correct=-50))
    dcf2_env_dep = property(*func_template(113, correct=-50))
    dcf2_env_vel_dep = property(*func_template(115, correct=-50))
    dcf2_env_attack = property(*func_template(117))
    dcf2_env_decay = property(*func_template(119))
    dcf2_env_sustain = property(*func_template(121))
    dcf2_env_release = property(*func_template(123))
    dcf2_time_mod_on_vel = property(*func_template(125, correct=-50))
    dcf2_time_mod_off_vel = property(*func_template(127, correct=-50))
    dcf2_time_mod_ks = property(*func_template(129, correct=-50))


    def save(self, filename):
        print(f'Save instrument to {filename} ...')

        with open(filename, 'bw') as f:
            f.write(self.id.to_bytes(1))
            f.write(len(self._data).to_bytes(2))
            f.write(self._data)



    def load(self, filename):
        print(f'Load instrument from {filename} ...')

        with open(filename, 'rb') as f:
            b = f.read(1)[0]
            if b == self.id:
                size = int.from_bytes(f.read(2))
                if size == len(self._data):
                    self._data = bytearray(f.read(size))
                    return True
            
        return False
