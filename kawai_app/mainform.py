# mainform.py
#
# written by: Oliver Cordes 2023-01-30
# changed by: Oliver Cordes 2023-05-06

import os

from ui_form import Ui_MainWindow

from PySide6.QtCore import Slot
from PySide6 import QtWidgets

from PySide6.QtWidgets import QFileDialog

from PySide6.QtCore import QCoreApplication
translate = QCoreApplication.translate

from k4midi.k4dump import K4Dump
from k4midi.k4single import K4SingleInstrument
from k4midi.k4effects import K4Effects

from qtaddons.qthelper import keyboard_keys_k4


window_title = 'K4 Instrument Editor'

# helper functions
def name2pos(name):
    return (ord(name[0]) - ord('A'))*16 + int(name[1:3])-1


def eff_name2pos(name):
    return int(name.split()[-1])-1


def generate_button_group(window, buttons):
    grp = QtWidgets.QButtonGroup(window)
    nr = 0
    for btn in buttons:
        grp.addButton(btn)
        grp.setId(btn, nr)
        nr += 1

    return grp


def suggest_filename(filename):
    s = filename.split('.')
    n = ''.join(s[:-1])+'_2'
    print(f'{filename} {n}')
    return n



class MainUI(Ui_MainWindow):
    def __init__(self, app, window):
        #Ui_MainWindow.__init__(self)
        super().__init__()
        self._app             = app
        self._window          = window

        self._mf              = None   # the MIDI file

        self._si_nr           = 0
        self._ins             = None
        self._ins_item        = None
        self._copy_instrument = None

        self._eff_nr          = 0
        self._effect          = None
        self._copy_effect     = None

        self._filename        = None
        self._lastdir         = None
        self._edit_mode       = False
        self._has_changed     = False
        self._read_only       = True


    def get_working_dir(self):
        if self._lastdir is None:
            return os.getcwd()
        else:
            return self._lastdir


    def set_working_dir(self, filename=None):
        if filename is not None:
           self._lastdir = os.path.dirname(filename)

    # update_status
    #
    # if the editor is in edit-mode, then change the flag
    def update_status(self, has_changed=True):
        if self._filename is None:
            fname = ''
        else:
            fname = f' - {self._filename}'
        if self._edit_mode and not self._read_only:
            self._has_changed = has_changed


        if self._has_changed:
            self._window.setWindowTitle(window_title+f' *{fname}')
        else:
            self._window.setWindowTitle(window_title+fname)


    def lock_status(self):
        self._edit_mode = False


    def unlock_status(self):
        self._edit_mode = True


    def setupUi(self, window):
        super().setupUi(window)
        #Ui_MainWindow.setupUi(self)

        self._window = window
        window.setWindowTitle(window_title)

        single_instruments = self.treeWidget.topLevelItem(0)
        multiple_instruments = self.treeWidget.topLevelItem(1)
        drums = self.treeWidget.topLevelItem(2)
        effects = self.treeWidget.topLevelItem(3)
        for back in ['A', 'B', 'C', 'D']:
            for nr in range(1,17):
                it = QtWidgets.QTreeWidgetItem([f'{back}{nr:02d}'])
                single_instruments.addChild(it)
                it = QtWidgets.QTreeWidgetItem([f'{back}{nr:02d}'])
                multiple_instruments.addChild(it)


        for drumkey in keyboard_keys_k4:
            it = QtWidgets.QTreeWidgetItem([f'Drumkey {drumkey}'])
            drums.addChild(it)

        for nr in range(1,33):
            it = QtWidgets.QTreeWidgetItem([f'Effect {nr:02d}'])
            effects.addChild(it)

        # connect the treeWidget with mouse clicks
        self.treeWidget.itemClicked.connect(self.onItemClicked)




        # define the change functions for all widgets
        self.si_name.textChanged.connect(self.ins_gen_valueChanged('name'))
        self.si_volume.valueChanged.connect(self.ins_gen_valueChanged('volume'))
        self.si_effect.valueChanged.connect(self.ins_gen_valueChanged('effect'))
        self.si_out_select.valueChanged.connect(self.ins_gen_valueChanged('out_select'))

        # create a special button group with ids
        self.si_source_mode_grp = generate_button_group(self._window,
                                                        [self.si_sm_norm,
                                                        self.si_sm_twin,
                                                        self.si_sm_double])
        self.si_source_mode_grp.buttonClicked.connect(self.ins_gen_radio_buttonClicked(self.si_source_mode_grp,'source_mode'))

        self.si_poly_mode_grp = generate_button_group(self._window,
                                                      [self.si_pm_poly1,
                                                      self.si_pm_poly2,
                                                      self.si_pm_solo1,
                                                      self.si_pm_solo2])
        self.si_poly_mode_grp.buttonClicked.connect(self.ins_gen_radio_buttonClicked(self.si_poly_mode_grp,'poly_mode'))

        self.si_am_s12.stateChanged.connect(self.ins_gen_check_buttonClicked('am12'))
        self.si_am_s34.stateChanged.connect(self.ins_gen_check_buttonClicked('am34'))
        self.si_mute_s1.stateChanged.connect(self.ins_gen_check_buttonClicked('mute_s1'))
        self.si_mute_s2.stateChanged.connect(self.ins_gen_check_buttonClicked('mute_s2'))
        self.si_mute_s3.stateChanged.connect(self.ins_gen_check_buttonClicked('mute_s3'))
        self.si_mute_s4.stateChanged.connect(self.ins_gen_check_buttonClicked('mute_s4'))

        self.si_vib_shape_grp = generate_button_group(self._window,
                                                        [self.si_vs_triangle,
                                                        self.si_vs_saw,
                                                        self.si_vs_square,
                                                        self.si_vs_random])
        self.si_vib_shape_grp.buttonClicked.connect(self.ins_gen_radio_buttonClicked(self.si_vib_shape_grp,'vib_shape'))

        self.si_pitch_bend.valueChanged.connect(self.ins_gen_valueChanged('pitch_bend'))

        self.si_wheel_assign_grp = generate_button_group(self._window,
                                                            [self.si_wa_vibrato,
                                                            self.si_wa_lfo,
                                                            self.si_wa_dcf])
        self.si_wheel_assign_grp.buttonClicked.connect(self.ins_gen_radio_buttonClicked(self.si_wheel_assign_grp, 'wheel_assign'))

        self.si_vib_speed.valueChanged.connect(self.ins_gen_valueChanged('vib_speed'))
        self.si_wheel_dep.valueChanged.connect(self.ins_gen_valueChanged('wheel_dep'))
        self.si_auto_bend_time.valueChanged.connect(self.ins_gen_valueChanged('auto_bend_time'))
        self.si_auto_bend_depth.valueChanged.connect(self.ins_gen_valueChanged('auto_bend_depth'))
        self.si_auto_bend_ks_time.valueChanged.connect(self.ins_gen_valueChanged('auto_bend_ks_time'))
        self.si_auto_bend_vel_dep.valueChanged.connect(self.ins_gen_valueChanged('auto_bend_vel_dep'))
        self.si_vib_prs_vib.valueChanged.connect(self.ins_gen_valueChanged('vib_prs_vib'))
        self.si_vibrato_dep.valueChanged.connect(self.ins_gen_valueChanged('vibrato_dep'))

        self.si_lfo_shape_grp = generate_button_group(self._window,
                                                        [self.si_ls_triangle,
                                                        self.si_ls_saw,
                                                        self.si_ls_square,
                                                        self.si_ls_random])
        self.si_lfo_shape_grp.buttonClicked.connect(self.ins_gen_radio_buttonClicked(self.si_lfo_shape_grp,'lfo_shape'))
        self.si_lfo_speed.valueChanged.connect(self.ins_gen_valueChanged('lfo_speed'))
        self.si_lfo_delay.valueChanged.connect(self.ins_gen_valueChanged('lfo_delay'))
        self.si_lfo_dep.valueChanged.connect(self.ins_gen_valueChanged('lfo_dep'))
        self.si_lfo_prs_dep.valueChanged.connect(self.ins_gen_valueChanged('lfo_prs_dep'))
        self.si_pres_freq.valueChanged.connect(self.ins_gen_valueChanged('pres_freq'))

        # SOURCES 1
        self.s1_wave.valueChanged.connect(self.ins_gen_valueChanged('s1_wave_select'))
        self.s1_delay.valueChanged.connect(self.ins_gen_valueChanged('s1_delay'))
        self.s1_ks_curve.valueChanged.connect(self.ins_gen_valueChanged('s1_ks_curve'))
        self.s1_coarse.valueChanged.connect(self.ins_gen_valueChanged('s1_coarse'))
        self.s1_key_track.stateChanged.connect(self.ins_gen_check_buttonClicked('s1_key_track'))
        self.s1_fix.valueChanged.connect(self.ins_gen_valueChanged('s1_fix'))
        self.s1_fine.valueChanged.connect(self.ins_gen_valueChanged('s1_fine'))
        self.s1_prs_freq.stateChanged.connect(self.ins_gen_check_buttonClicked('s1_prs_freq'))
        self.s1_vib_bend.stateChanged.connect(self.ins_gen_check_buttonClicked('s1_vib_bend'))
        self.s1_vel_curve.valueChanged.connect(self.ins_gen_valueChanged('s1_vel_curve'))

        # SOURCES 2
        self.s2_wave.valueChanged.connect(self.ins_gen_valueChanged('s2_wave_select'))
        self.s2_delay.valueChanged.connect(self.ins_gen_valueChanged('s2_delay'))
        self.s2_ks_curve.valueChanged.connect(self.ins_gen_valueChanged('s2_ks_curve'))
        self.s2_coarse.valueChanged.connect(self.ins_gen_valueChanged('s2_coarse'))
        self.s2_key_track.stateChanged.connect(self.ins_gen_check_buttonClicked('s2_key_track'))
        self.s2_fix.valueChanged.connect(self.ins_gen_valueChanged('s2_fix'))
        self.s2_fine.valueChanged.connect(self.ins_gen_valueChanged('s2_fine'))
        self.s2_prs_freq.stateChanged.connect(self.ins_gen_check_buttonClicked('s2_prs_freq'))
        self.s2_vib_bend.stateChanged.connect(self.ins_gen_check_buttonClicked('s2_vib_bend'))
        self.s2_vel_curve.valueChanged.connect(self.ins_gen_valueChanged('s2_vel_curve'))

        # SOURCES 3
        self.s3_wave.valueChanged.connect(self.ins_gen_valueChanged('s3_wave_select'))
        self.s3_delay.valueChanged.connect(self.ins_gen_valueChanged('s3_delay'))
        self.s3_ks_curve.valueChanged.connect(self.ins_gen_valueChanged('s3_ks_curve'))
        self.s3_coarse.valueChanged.connect(self.ins_gen_valueChanged('s3_coarse'))
        self.s3_key_track.stateChanged.connect(self.ins_gen_check_buttonClicked('s3_key_track'))
        self.s3_fix.valueChanged.connect(self.ins_gen_valueChanged('s3_fix'))
        self.s3_fine.valueChanged.connect(self.ins_gen_valueChanged('s3_fine'))
        self.s3_prs_freq.stateChanged.connect(self.ins_gen_check_buttonClicked('s3_prs_freq'))
        self.s3_vib_bend.stateChanged.connect(self.ins_gen_check_buttonClicked('s3_vib_bend'))
        self.s3_vel_curve.valueChanged.connect(self.ins_gen_valueChanged('s3_vel_curve'))

        # SOURCES 4
        self.s4_wave.valueChanged.connect(self.ins_gen_valueChanged('s4_wave_select'))
        self.s4_delay.valueChanged.connect(self.ins_gen_valueChanged('s4_delay'))
        self.s4_ks_curve.valueChanged.connect(self.ins_gen_valueChanged('s4_ks_curve'))
        self.s4_coarse.valueChanged.connect(self.ins_gen_valueChanged('s4_coarse'))
        self.s4_key_track.stateChanged.connect(self.ins_gen_check_buttonClicked('s4_key_track'))
        self.s4_fix.valueChanged.connect(self.ins_gen_valueChanged('s4_fix'))
        self.s4_fine.valueChanged.connect(self.ins_gen_valueChanged('s4_fine'))
        self.s4_prs_freq.stateChanged.connect(self.ins_gen_check_buttonClicked('s4_prs_freq'))
        self.s4_vib_bend.stateChanged.connect(self.ins_gen_check_buttonClicked('s4_vib_bend'))
        self.s4_vel_curve.valueChanged.connect(self.ins_gen_valueChanged('s4_vel_curve'))

        # DCA 1
        self.s1_env_level.valueChanged.connect(self.ins_gen_valueChanged('s1_envelope_level'))
        self.s1_env_attack.valueChanged.connect(self.ins_gen_valueChanged('s1_envelope_attack'))
        self.s1_env_decay.valueChanged.connect(self.ins_gen_valueChanged('s1_envelope_decay'))
        self.s1_env_sustain.valueChanged.connect(self.ins_gen_valueChanged('s1_envelope_sustain'))
        self.s1_env_release.valueChanged.connect(self.ins_gen_valueChanged('s1_envelope_release'))
        self.s1_level_mod_vel.valueChanged.connect(self.ins_gen_valueChanged('s1_level_mod_vel'))
        self.s1_level_mod_prs.valueChanged.connect(self.ins_gen_valueChanged('s1_level_mod_prs'))
        self.s1_level_mod_ks.valueChanged.connect(self.ins_gen_valueChanged('s1_level_mod_ks'))
        self.s1_time_mod_on_vel.valueChanged.connect(self.ins_gen_valueChanged('s1_time_mod_on_vel'))
        self.s1_time_mod_off_vel.valueChanged.connect(self.ins_gen_valueChanged('s1_time_mod_off_vel'))
        self.s1_time_mod_ks.valueChanged.connect(self.ins_gen_valueChanged('s1_time_mod_ks'))

        # DCA 2
        self.s2_env_level.valueChanged.connect(self.ins_gen_valueChanged('s2_envelope_level'))
        self.s2_env_attack.valueChanged.connect(self.ins_gen_valueChanged('s2_envelope_attack'))
        self.s2_env_decay.valueChanged.connect(self.ins_gen_valueChanged('s2_envelope_decay'))
        self.s2_env_sustain.valueChanged.connect(self.ins_gen_valueChanged('s2_envelope_sustain'))
        self.s2_env_release.valueChanged.connect(self.ins_gen_valueChanged('s2_envelope_release'))
        self.s2_level_mod_vel.valueChanged.connect(self.ins_gen_valueChanged('s2_level_mod_vel'))
        self.s2_level_mod_prs.valueChanged.connect(self.ins_gen_valueChanged('s2_level_mod_prs'))
        self.s2_level_mod_ks.valueChanged.connect(self.ins_gen_valueChanged('s2_level_mod_ks'))
        self.s2_time_mod_on_vel.valueChanged.connect(self.ins_gen_valueChanged('s2_time_mod_on_vel'))
        self.s2_time_mod_off_vel.valueChanged.connect(self.ins_gen_valueChanged('s2_time_mod_off_vel'))
        self.s2_time_mod_ks.valueChanged.connect(self.ins_gen_valueChanged('s2_time_mod_ks'))

        # DCA 3
        self.s3_env_level.valueChanged.connect(self.ins_gen_valueChanged('s3_envelope_level'))
        self.s3_env_attack.valueChanged.connect(self.ins_gen_valueChanged('s3_envelope_attack'))
        self.s3_env_decay.valueChanged.connect(self.ins_gen_valueChanged('s3_envelope_decay'))
        self.s3_env_sustain.valueChanged.connect(self.ins_gen_valueChanged('s3_envelope_sustain'))
        self.s3_env_release.valueChanged.connect(self.ins_gen_valueChanged('s3_envelope_release'))
        self.s3_level_mod_vel.valueChanged.connect(self.ins_gen_valueChanged('s3_level_mod_vel'))
        self.s3_level_mod_prs.valueChanged.connect(self.ins_gen_valueChanged('s3_level_mod_prs'))
        self.s3_level_mod_ks.valueChanged.connect(self.ins_gen_valueChanged('s3_level_mod_ks'))
        self.s3_time_mod_on_vel.valueChanged.connect(self.ins_gen_valueChanged('s3_time_mod_on_vel'))
        self.s3_time_mod_off_vel.valueChanged.connect(self.ins_gen_valueChanged('s3_time_mod_off_vel'))
        self.s3_time_mod_ks.valueChanged.connect(self.ins_gen_valueChanged('s3_time_mod_ks'))

        # DCA 4
        self.s4_env_level.valueChanged.connect(self.ins_gen_valueChanged('s4_envelope_level'))
        self.s4_env_attack.valueChanged.connect(self.ins_gen_valueChanged('s4_envelope_attack'))
        self.s4_env_decay.valueChanged.connect(self.ins_gen_valueChanged('s4_envelope_decay'))
        self.s4_env_sustain.valueChanged.connect(self.ins_gen_valueChanged('s4_envelope_sustain'))
        self.s4_env_release.valueChanged.connect(self.ins_gen_valueChanged('s4_envelope_release'))
        self.s4_level_mod_vel.valueChanged.connect(self.ins_gen_valueChanged('s4_level_mod_vel'))
        self.s4_level_mod_prs.valueChanged.connect(self.ins_gen_valueChanged('s4_level_mod_prs'))
        self.s4_level_mod_ks.valueChanged.connect(self.ins_gen_valueChanged('s4_level_mod_ks'))
        self.s4_time_mod_on_vel.valueChanged.connect(self.ins_gen_valueChanged('s4_time_mod_on_vel'))
        self.s4_time_mod_off_vel.valueChanged.connect(self.ins_gen_valueChanged('s4_time_mod_off_vel'))
        self.s4_time_mod_ks.valueChanged.connect(self.ins_gen_valueChanged('s4_time_mod_ks'))

        # LFO1/DCF1
        self.si_lfo1_cutoff.valueChanged.connect(self.ins_gen_valueChanged('lfo1_cutoff'))
        self.si_lfo1_resonance.valueChanged.connect(self.ins_gen_valueChanged('lfo1_resonance'))
        self.si_lfo1_switch.toggled.connect(self.ins_gen_toggled('lfo1_switch'))
        self.si_lfo1_cutoff_mod_vel.valueChanged.connect(self.ins_gen_valueChanged('lfo1_cutoff_mod_vel'))
        self.si_lfo1_cutoff_mod_prs.valueChanged.connect(self.ins_gen_valueChanged('lfo1_cutoff_mod_prs'))
        self.si_lfo1_cutoff_mod_ks.valueChanged.connect(self.ins_gen_valueChanged('lfo1_cutoff_mod_ks'))
        self.si_dcf1_env_dep.valueChanged.connect(self.ins_gen_valueChanged('dcf1_env_dep'))
        self.si_dcf1_env_vel_dep.valueChanged.connect(self.ins_gen_valueChanged('dcf1_env_vel_dep'))
        self.si_dcf1_env_attack.valueChanged.connect(self.ins_gen_valueChanged('dcf1_env_attack'))
        self.si_dcf1_env_decay.valueChanged.connect(self.ins_gen_valueChanged('dcf1_env_decay'))
        self.si_dcf1_env_sustain.valueChanged.connect(self.ins_gen_valueChanged('dcf1_env_sustain'))
        self.si_dcf1_env_release.valueChanged.connect(self.ins_gen_valueChanged('dcf1_env_release'))
        self.si_dcf1_time_mod_on_vel.valueChanged.connect(self.ins_gen_valueChanged('dcf1_time_mod_on_vel'))
        self.si_dcf1_time_mod_off_vel.valueChanged.connect(self.ins_gen_valueChanged('dcf1_time_mod_off_vel'))
        self.si_dcf1_time_mod_ks.valueChanged.connect(self.ins_gen_valueChanged('dcf1_time_mod_ks'))

        # LFO2/DCF2
        self.si_lfo2_cutoff.valueChanged.connect(self.ins_gen_valueChanged('lfo2_cutoff'))
        self.si_lfo2_resonance.valueChanged.connect(self.ins_gen_valueChanged('lfo2_resonance'))
        self.si_lfo2_switch.toggled.connect(self.ins_gen_toggled('lfo2_switch'))
        self.si_lfo2_cutoff_mod_vel.valueChanged.connect(self.ins_gen_valueChanged('lfo2_cutoff_mod_vel'))
        self.si_lfo2_cutoff_mod_prs.valueChanged.connect(self.ins_gen_valueChanged('lfo2_cutoff_mod_prs'))
        self.si_lfo2_cutoff_mod_ks.valueChanged.connect(self.ins_gen_valueChanged('lfo2_cutoff_mod_ks'))
        self.si_dcf2_env_dep.valueChanged.connect(self.ins_gen_valueChanged('dcf2_env_dep'))
        self.si_dcf2_env_vel_dep.valueChanged.connect(self.ins_gen_valueChanged('dcf2_env_vel_dep'))
        self.si_dcf2_env_attack.valueChanged.connect(self.ins_gen_valueChanged('dcf2_env_attack'))
        self.si_dcf2_env_decay.valueChanged.connect(self.ins_gen_valueChanged('dcf2_env_decay'))
        self.si_dcf2_env_sustain.valueChanged.connect(self.ins_gen_valueChanged('dcf2_env_sustain'))
        self.si_dcf2_env_release.valueChanged.connect(self.ins_gen_valueChanged('dcf2_env_release'))
        self.si_dcf2_time_mod_on_vel.valueChanged.connect(self.ins_gen_valueChanged('dcf2_time_mod_on_vel'))
        self.si_dcf2_time_mod_off_vel.valueChanged.connect(self.ins_gen_valueChanged('dcf2_time_mod_off_vel'))
        self.si_dcf2_time_mod_ks.valueChanged.connect(self.ins_gen_valueChanged('dcf2_time_mod_ks'))


        self.si_load.clicked.connect(self.load_instrument)
        self.si_save.clicked.connect(self.save_instrument)
        self.si_copy.clicked.connect(self.copy_instrument)
        self.si_paste.clicked.connect(self.paste_instrument)

        # effects

        self.eff_para1.valueChanged.connect(self.effect_gen_valueChanged('para1'))
        self.eff_para2.valueChanged.connect(self.effect_gen_valueChanged('para2'))
        self.eff_para3.valueChanged.connect(self.effect_gen_valueChanged('para3'))

        self.eff_pan_a.valueChanged.connect(self.effect_gen_valueChanged('pan_A'))
        self.eff_send1_a.valueChanged.connect(self.effect_gen_valueChanged('send1_A'))
        self.eff_send2_a.valueChanged.connect(self.effect_gen_valueChanged('send2_A'))

        self.eff_pan_b.valueChanged.connect(self.effect_gen_valueChanged('pan_B'))
        self.eff_send1_b.valueChanged.connect(self.effect_gen_valueChanged('send1_B'))
        self.eff_send2_b.valueChanged.connect(self.effect_gen_valueChanged('send2_B'))

        self.eff_pan_c.valueChanged.connect(self.effect_gen_valueChanged('pan_C'))
        self.eff_send1_c.valueChanged.connect(self.effect_gen_valueChanged('send1_C'))
        self.eff_send2_c.valueChanged.connect(self.effect_gen_valueChanged('send2_C'))

        self.eff_pan_d.valueChanged.connect(self.effect_gen_valueChanged('pan_D'))
        self.eff_send1_d.valueChanged.connect(self.effect_gen_valueChanged('send1_D'))
        self.eff_send2_d.valueChanged.connect(self.effect_gen_valueChanged('send2_D'))

        self.eff_pan_e.valueChanged.connect(self.effect_gen_valueChanged('pan_E'))
        self.eff_send1_e.valueChanged.connect(self.effect_gen_valueChanged('send1_E'))
        self.eff_send2_e.valueChanged.connect(self.effect_gen_valueChanged('send2_E'))

        self.eff_pan_f.valueChanged.connect(self.effect_gen_valueChanged('pan_F'))
        self.eff_send1_f.valueChanged.connect(self.effect_gen_valueChanged('send1_F'))
        self.eff_send2_f.valueChanged.connect(self.effect_gen_valueChanged('send2_F'))

        self.eff_pan_g.valueChanged.connect(self.effect_gen_valueChanged('pan_G'))
        self.eff_send1_g.valueChanged.connect(self.effect_gen_valueChanged('send1_G'))
        self.eff_send2_g.valueChanged.connect(self.effect_gen_valueChanged('send2_G'))

        self.eff_pan_h.valueChanged.connect(self.effect_gen_valueChanged('pan_H'))
        self.eff_send1_h.valueChanged.connect(self.effect_gen_valueChanged('send1_H'))
        self.eff_send2_h.valueChanged.connect(self.effect_gen_valueChanged('send2_H'))

        self.eff_load.clicked.connect(self.load_effect)
        self.eff_save.clicked.connect(self.save_effect)
        self.eff_copy.clicked.connect(self.copy_effect)
        self.eff_paste.clicked.connect(self.paste_effect)


    # generator to change a data entry
    # the function is connected to a widget, so the inner function
    # wil be called with the new value,
    # with 'funcname' the name of the set function can be specified,
    # so the specific value can be set, important is that
    # self._ins can be changed externally, it will always the correct
    # instance member function be called!
    def ins_gen_valueChanged(self, funcname):

        def valuechanged(val):
            if self._ins is None:
                return

            func = getattr(K4SingleInstrument, funcname)
            if type(func) == property:
               func.fset(self._ins, val)
            else:
               func(self._ins, val)

            self.update_status()

            if funcname == 'name':
                if self._ins_item is not None:
                   s = self._ins_item.text(0).split()[0]+' - '+val
                   self._ins_item.setText(0, s)

        return valuechanged


    def effect_gen_valueChanged(self, funcname):

        def valuechanged(val):
            if self._effect is None:
                return

            func = getattr(K4Effects, funcname)
            if type(func) == property:
               func.fset(self._effect, val)
            else:
               func(self._effect, val)

            self.update_status()

        return valuechanged


    def ins_gen_radio_buttonClicked(self, grp, funcname):

        def buttonclicked(button):
            if self._ins is None:
                return

            id = grp.id(button)
            print('radio Button clicked:', id)

            # the id is the bit mask of the pressed button
            func = getattr(K4SingleInstrument, funcname)
            if type(func) == property:
                func.fset(self._ins, id)
            else:
                func(self._ins, id)

            self.update_status()

        return buttonclicked


    def ins_gen_check_buttonClicked(self, funcname):

        def statechanged(newstate):
            if self._ins is None:
                return

            if newstate == 2:  # fully checked
               val = 1
            else:
               val = 0

            print('check button clicked', newstate)

            # the id is the bit mask of the pressed button
            func = getattr(K4SingleInstrument, funcname)
            if type(func) == property:
                func.fset(self._ins, val)
            else:
                func(self._ins, val)

            self.update_status()

        return statechanged


    def ins_gen_toggled(self, funcname):

        def toggled(checked):
            if self._ins is None:
                return

            print('radio button toggled', checked)

            # the id is the bit mask of the pressed button
            func = getattr(K4SingleInstrument, funcname)
            if type(func) == property:
                func.fset(self._ins, checked)
            else:
                func(self._ins, checked)

            self.update_status()

        return toggled


    def select_instrument(self, si_nr):
        #self.Instrument_Widget.removeTab(self.tab_5)
        self.lock_status()
        self._si_nr = si_nr
        # selects the si_nr'th instrument
        ins = self._mf.data['single_instruments'][si_nr]
        self._ins = ins
        # fill the single instrument data
        self.si_name.setText(ins.name)
        self.si_volume.setValue(ins.volume)
        self.si_effect.setValue(ins.effect)
        self.si_out_select.setValue(ins.out_select)
        self.si_source_mode.children()[ins.source_mode].setChecked(True)
        self.si_poly_mode.children()[ins.poly_mode].setChecked(True)
        self.si_am_s12.setChecked(ins.am12)
        self.si_am_s34.setChecked(ins.am34)
        self.si_mute_s1.setChecked(ins.mute_s1)
        self.si_mute_s2.setChecked(ins.mute_s2)
        self.si_mute_s3.setChecked(ins.mute_s3)
        self.si_mute_s4.setChecked(ins.mute_s4)
        self.si_vib_shape.children()[ins.vib_shape].setChecked(True)
        self.si_pitch_bend.setValue(ins.pitch_bend)
        self.si_wheel_assign.children()[ins.wheel_assign].setChecked(True)
        self.si_vib_speed.setValue(ins.vib_speed)
        self.si_wheel_dep.setValue(ins.wheel_dep)
        self.si_auto_bend_time.setValue(ins.auto_bend_time)
        self.si_auto_bend_depth.setValue(ins.auto_bend_depth)
        self.si_auto_bend_ks_time.setValue(ins.auto_bend_ks_time)
        self.si_auto_bend_vel_dep.setValue(ins.auto_bend_vel_dep)
        self.si_vib_prs_vib.setValue(ins.vib_prs_vib)
        self.si_vibrato_dep.setValue(ins.vibrato_dep)
        self.si_lfo_shape.children()[ins.lfo_shape].setChecked(True)
        self.si_lfo_speed.setValue(ins.lfo_speed)
        self.si_lfo_delay.setValue(ins.lfo_delay)
        self.si_lfo_dep.setValue(ins.lfo_dep)
        self.si_lfo_prs_dep.setValue(ins.lfo_prs_dep)
        self.si_pres_freq.setValue(ins.pres_freq)

        self.s1_wave.setValue(ins.s1_wave_select)
        self.s1_ks_curve.setValue(ins.s1_ks_curve)
        self.s1_delay.setValue(ins.s1_delay)
        self.s1_coarse.setValue(ins.s1_coarse)
        self.s1_fix.setValue(ins.s1_fix)
        self.s1_fine.setValue(ins.s1_fine)
        self.s1_key_track.setChecked(ins.s1_key_track)
        self.s1_prs_freq.setChecked(ins.s1_prs_freq)
        self.s1_vib_bend.setChecked(ins.s1_vib_bend)
        self.s1_vel_curve.setValue(ins.s1_vel_curve)
        self.s2_wave.setValue(ins.s2_wave_select)
        self.s2_ks_curve.setValue(ins.s2_ks_curve)
        self.s2_delay.setValue(ins.s2_delay)
        self.s2_coarse.setValue(ins.s2_coarse)
        self.s2_fix.setValue(ins.s2_fix)
        self.s2_fine.setValue(ins.s2_fine)
        self.s2_key_track.setChecked(ins.s2_key_track)
        self.s2_prs_freq.setChecked(ins.s2_prs_freq)
        self.s2_vib_bend.setChecked(ins.s2_vib_bend)
        self.s2_vel_curve.setValue(ins.s2_vel_curve)
        self.s3_wave.setValue(ins.s3_wave_select)
        self.s3_ks_curve.setValue(ins.s3_ks_curve)
        self.s3_delay.setValue(ins.s3_delay)
        self.s3_coarse.setValue(ins.s3_coarse)
        self.s3_fix.setValue(ins.s3_fix)
        self.s3_fine.setValue(ins.s3_fine)
        self.s3_key_track.setChecked(ins.s3_key_track)
        self.s3_prs_freq.setChecked(ins.s3_prs_freq)
        self.s3_vib_bend.setChecked(ins.s3_vib_bend)
        self.s3_vel_curve.setValue(ins.s3_vel_curve)
        self.s4_wave.setValue(ins.s4_wave_select)
        self.s4_ks_curve.setValue(ins.s4_ks_curve)
        self.s4_delay.setValue(ins.s4_delay)
        self.s4_coarse.setValue(ins.s4_coarse)
        self.s4_fix.setValue(ins.s4_fix)
        self.s4_fine.setValue(ins.s4_fine)
        self.s4_key_track.setChecked(ins.s4_key_track)
        self.s4_prs_freq.setChecked(ins.s4_prs_freq)
        self.s4_vib_bend.setChecked(ins.s4_vib_bend)
        self.s4_vel_curve.setValue(ins.s4_vel_curve)

        self.s1_env_level.setValue(ins.s1_envelope_level)
        self.s1_env_attack.setValue(ins.s1_envelope_attack)
        self.s1_env_decay.setValue(ins.s1_envelope_decay)
        self.s1_env_sustain.setValue(ins.s1_envelope_sustain)
        self.s1_env_release.setValue(ins.s1_envelope_release)
        self.s1_level_mod_vel.setValue(ins.s1_level_mod_vel)
        self.s1_level_mod_prs.setValue(ins.s1_level_mod_prs)
        self.s1_level_mod_ks.setValue(ins.s1_level_mod_ks)
        self.s1_time_mod_on_vel.setValue(ins.s1_time_mod_on_vel)
        self.s1_time_mod_off_vel.setValue(ins.s1_time_mod_off_vel)
        self.s1_time_mod_ks.setValue(ins.s1_time_mod_ks)
        self.s2_env_level.setValue(ins.s2_envelope_level)
        self.s2_env_attack.setValue(ins.s2_envelope_attack)
        self.s2_env_decay.setValue(ins.s2_envelope_decay)
        self.s2_env_sustain.setValue(ins.s2_envelope_sustain)
        self.s2_env_release.setValue(ins.s2_envelope_release)
        self.s2_level_mod_vel.setValue(ins.s2_level_mod_vel)
        self.s2_level_mod_prs.setValue(ins.s2_level_mod_prs)
        self.s2_level_mod_ks.setValue(ins.s2_level_mod_ks)
        self.s2_time_mod_on_vel.setValue(ins.s2_time_mod_on_vel)
        self.s2_time_mod_off_vel.setValue(ins.s2_time_mod_off_vel)
        self.s2_time_mod_ks.setValue(ins.s2_time_mod_ks)
        self.s3_env_level.setValue(ins.s3_envelope_level)
        self.s3_env_attack.setValue(ins.s3_envelope_attack)
        self.s3_env_decay.setValue(ins.s3_envelope_decay)
        self.s3_env_sustain.setValue(ins.s3_envelope_sustain)
        self.s3_env_release.setValue(ins.s3_envelope_release)
        self.s3_level_mod_vel.setValue(ins.s3_level_mod_vel)
        self.s3_level_mod_prs.setValue(ins.s3_level_mod_prs)
        self.s3_level_mod_ks.setValue(ins.s3_level_mod_ks)
        self.s3_time_mod_on_vel.setValue(ins.s3_time_mod_on_vel)
        self.s3_time_mod_off_vel.setValue(ins.s3_time_mod_off_vel)
        self.s3_time_mod_ks.setValue(ins.s3_time_mod_ks)
        self.s4_env_level.setValue(ins.s4_envelope_level)
        self.s4_env_attack.setValue(ins.s4_envelope_attack)
        self.s4_env_decay.setValue(ins.s4_envelope_decay)
        self.s4_env_sustain.setValue(ins.s4_envelope_sustain)
        self.s4_env_release.setValue(ins.s4_envelope_release)
        self.s4_level_mod_vel.setValue(ins.s4_level_mod_vel)
        self.s4_level_mod_prs.setValue(ins.s4_level_mod_prs)
        self.s4_level_mod_ks.setValue(ins.s4_level_mod_ks)
        self.s4_time_mod_on_vel.setValue(ins.s4_time_mod_on_vel)
        self.s4_time_mod_off_vel.setValue(ins.s4_time_mod_off_vel)
        self.s4_time_mod_ks.setValue(ins.s4_time_mod_ks)

        # LFO 1
        self.si_lfo1_cutoff.setValue(ins.lfo1_cutoff)
        self.si_lfo1_resonance.setValue(ins.lfo1_resonance)
        self.si_lfo1_switch.setChecked(ins.lfo1_switch)
        self.si_lfo1_cutoff_mod_vel.setValue(ins.lfo1_cutoff_mod_vel)
        self.si_lfo1_cutoff_mod_prs.setValue(ins.lfo1_cutoff_mod_prs)
        self.si_lfo1_cutoff_mod_ks.setValue(ins.lfo1_cutoff_mod_ks)
        self.si_dcf1_env_dep.setValue(ins.dcf1_env_dep)
        self.si_dcf1_env_vel_dep.setValue(ins.dcf1_env_vel_dep)
        self.si_dcf1_env_attack.setValue(ins.dcf1_env_attack)
        self.si_dcf1_env_decay.setValue(ins.dcf1_env_decay)
        self.si_dcf1_env_sustain.setValue(ins.dcf1_env_sustain)
        self.si_dcf1_env_release.setValue(ins.dcf1_env_release)
        self.si_dcf1_time_mod_on_vel.setValue(ins.dcf1_time_mod_on_vel)
        self.si_dcf1_time_mod_off_vel.setValue(ins.dcf1_time_mod_off_vel)
        self.si_dcf1_time_mod_ks.setValue(ins.dcf1_time_mod_ks)

        # LFO 2
        self.si_lfo2_cutoff.setValue(ins.lfo2_cutoff)
        self.si_lfo2_resonance.setValue(ins.lfo2_resonance)
        self.si_lfo2_switch.setChecked(ins.lfo2_switch)
        self.si_lfo2_cutoff_mod_vel.setValue(ins.lfo2_cutoff_mod_vel)
        self.si_lfo2_cutoff_mod_prs.setValue(ins.lfo2_cutoff_mod_prs)
        self.si_lfo2_cutoff_mod_ks.setValue(ins.lfo2_cutoff_mod_ks)
        self.si_dcf2_env_dep.setValue(ins.dcf2_env_dep)
        self.si_dcf2_env_vel_dep.setValue(ins.dcf2_env_vel_dep)
        self.si_dcf2_env_attack.setValue(ins.dcf2_env_attack)
        self.si_dcf2_env_decay.setValue(ins.dcf2_env_decay)
        self.si_dcf2_env_sustain.setValue(ins.dcf2_env_sustain)
        self.si_dcf2_env_release.setValue(ins.dcf2_env_release)
        self.si_dcf2_time_mod_on_vel.setValue(ins.dcf2_time_mod_on_vel)
        self.si_dcf2_time_mod_off_vel.setValue(ins.dcf2_time_mod_off_vel)
        self.si_dcf2_time_mod_ks.setValue(ins.dcf2_time_mod_ks)

        self.unlock_status()


    def select_effect(self, eff_nr):
        self.lock_status()
        self._eff_nr = eff_nr

        effect = self._mf.data['effects'][eff_nr]
        self._effect = effect

        self.eff_number.setText(f'{eff_nr+1}')

        self.eff_type.setValue(effect.effect_type)
        print(effect.effect_type)

        self.eff_para1.setValue(effect.para1)
        self.eff_para2.setValue(effect.para2)
        self.eff_para3.setValue(effect.para3)

        self.eff_pan_a.setValue(effect.pan_A)
        self.eff_send1_a.setValue(effect.send1_A)
        self.eff_send2_a.setValue(effect.send2_A)

        self.eff_pan_b.setValue(effect.pan_B)
        self.eff_send1_b.setValue(effect.send1_B)
        self.eff_send2_b.setValue(effect.send2_B)

        self.eff_pan_c.setValue(effect.pan_C)
        self.eff_send1_c.setValue(effect.send1_C)
        self.eff_send2_c.setValue(effect.send2_C)

        self.eff_pan_d.setValue(effect.pan_D)
        self.eff_send1_d.setValue(effect.send1_D)
        self.eff_send2_d.setValue(effect.send2_D)

        self.eff_pan_e.setValue(effect.pan_E)
        self.eff_send1_e.setValue(effect.send1_E)
        self.eff_send2_e.setValue(effect.send2_E)

        self.eff_pan_f.setValue(effect.pan_F)
        self.eff_send1_f.setValue(effect.send1_F)
        self.eff_send2_f.setValue(effect.send2_F)

        self.eff_pan_g.setValue(effect.pan_G)
        self.eff_send1_g.setValue(effect.send1_G)
        self.eff_send2_g.setValue(effect.send2_G)

        self.eff_pan_h.setValue(effect.pan_H)
        self.eff_send1_h.setValue(effect.send1_H)
        self.eff_send2_h.setValue(effect.send2_H)

        self.unlock_status()



    @Slot(QtWidgets.QTreeWidgetItem, int)
    def onItemClicked(self, item, col):
        #print(item, col, item.text(col))
        #print('Clicked')
        #print(item.parent())
        if item.parent() is not None:
            # correct sub element ;-)
            #print('>',item.parent().text(0))
            itemtext = item.parent().text(0)
            if itemtext == 'Single Instruments':
                # select instrument
                if self._mf.data is not None and 'single_instruments' in self._mf.data:
                    # sets the item first, since select_instrument sets the widgets
                    # which calles the update function which will update the list
                    # name, so self._ins should be set properly!
                    self._ins_item = item
                    si_nr = name2pos(item.text(col))
                    self.select_instrument(si_nr)
            elif itemtext == 'Drums':
                # select drums
                print(f'Drums {item.text(col)}')
            elif itemtext == 'Effects':
                # select effect
                if self._mf.data is not None and 'effects' in self._mf.data:
                    print(f'Effect {item.text(col)}')
                    effect_nr = eff_name2pos(item.text(col))
                    self.select_effect(effect_nr)




    def load_instrument(self):
        if self._mf.data is not None:
            print('Load instrument')

            filename = QFileDialog.getOpenFileName(self._window, translate('main', "Load instrument file"),
                                                        #os.getcwd(),
                                                        self.get_working_dir(),
                                                        translate('main', "k4 Files (*.k4 *.K4);;Bin Files (*.bin)"))
            print(filename)

            if filename[0] != '':
                self.set_working_dir(filename[0])
                self._ins.load(filename[0])
                self.select_instrument(self._si_nr)
                s = self._ins_item.text(0).split()[0]+' - '+self._ins.name
                self._ins_item.setText(0, s)


    def save_instrument(self):
        if self._mf.data is not None:
            name = self.get_working_dir()+'/'+self._ins.name+'.k4'
            filename = QFileDialog.getSaveFileName(self._window, translate('main', "Save instrument file"),
                                                        #os.getcwd(),
                                                        name,
                                                        translate('main', "k4 Files (*.k4 *.K4);;Bin Files (*.bin)"))
            if filename[0] != '':
                self.set_working_dir(filename[0])
                self._ins.save(filename[0])


    def copy_instrument(self):
        print('Copy instrument')
        self._copy_instrument = self._ins.copy()


    def paste_instrument(self):
        print('Paste instrument')
        self._ins.paste(self._copy_instrument)
        s = self._ins_item.text(0).split()[0]+' - '+self._ins.name
        self._ins_item.setText(0, s)


    def load_effect(self):
        if self._mf.data is not None:
            print('Load instrument')

            filename = QFileDialog.getOpenFileName(self._window, translate('main', "Load effect file"),
                                                        #os.getcwd(),
                                                        self.get_working_dir(),
                                                        translate('main', "k4 Files (*.k4 *.K4);;Bin Files (*.bin)"))
            print(filename)
            if filename[0] != '':
                self.set_working_dir(filename[0])
                self._effect.load(filename[0])
                self.select_effect(self._eff_nr)



    def save_effect(self):
        if self._mf.data is not None:
            name = f'{self.get_working_dir()}/effect{(self._eff_nr+1):02d}.k4'
            filename = QFileDialog.getSaveFileName(self._window, translate('main', "Save effect file"),
                                                        #os.getcwd(),
                                                        name,
                                                        translate('main', "k4 Files (*.k4 *.K4);;Bin Files (*.bin)"))
            if filename[0] != '':
                self.set_working_dir(filename[0])
                self._effect.save(filename[0])


    def copy_effect(self):
        self._copy_effect = self._effect.copy()


    def paste_effect(self):
        self._effect.paste(self._copy_effect)
        self.select_effect(self._eff_nr)


    def file_open(self):
        filename = QFileDialog.getOpenFileName(self._window, translate('main', "Open File"),
                                                            #os.getcwd(),
                                                            self.get_working_dir(),
                                                            translate('main', "MIDI Files (*.mid *.MID *.MIDI);;SysEX Files (*.syx)"))
        print(filename)
        if filename[0] != '':
            self.set_working_dir(filename[0])
            self.file_open_file(filename[0])


    def file_open_file(self, filename, read_only=False):
        self._mf = K4Dump(filename)

        self._filename = filename

        # insert single multiple_instruments
        single_instruments = self.treeWidget.topLevelItem(0)
        nr = 0
        for ins in self._mf.data['single_instruments']:
            #print(ins.name)
            w = single_instruments.child(nr)
            pre = w.text(0).split()[0]
            w.setText(0, f'{pre} - {ins.name}')
            nr += 1

        self._has_changed = False

        self.select_instrument(0)
        self._ins_item = self.treeWidget.topLevelItem(0).child(0)

        self._read_only = read_only
        self.update_status(has_changed=False)


    def file_save(self, filename):
        print('File save')
        if self._read_only:
            print('File is read-only!')
            return

        if filename is None:
            # use the original file name
            pass
        else:
            # save file to another filename
            self._filename = filename

        print(self._filename)
        #self._mf.save_midifile(self._filename)

        # reset the status flags
        self.update_status(has_changed=False)


    def file_saveas(self):
        print('File SaveAs')

        if self._mf is None:
            print('Nothing to save ...')
            return

        name = self.get_working_dir()+'/'+suggest_filename(self._filename)
        filename = QFileDialog.getSaveFileName(self._window, translate('main', "Save SysEX/MIDI file"),
                                                        #os.getcwd(),
                                                        name,
                                                        translate('main', "MIDI Files (*.mid *.MID *.MIDI);;SysEX Files (*.syx)"))
        if filename[0] != '':
            self.set_working_dir(filename[0])
            filename = filename[0]
            print(filename)
            if filename.endswith('.mid'):
                self._mf.save_midifile(filename)
            else:
                self._mf.save_sysexfile(filename)
