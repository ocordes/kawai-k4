# mainform.py
#
# written by: Oliver Cordes 2023-01-30
# changed by: Oliver Cordes 2023-02-17

from ui_form import Ui_MainWindow

from PySide6.QtCore import Slot
from PySide6 import QtWidgets

from k4midi.k4dump import K4Dump


window_title = 'K4 Instrument Editor'

# helper functions
def name2pos(name):
    return (ord(name[0]) - ord('A'))*16 + int(name[1:3])-1


class MainUI(Ui_MainWindow):
    def __init__(self, app):
        #Ui_MainWindow.__init__(self)
        super().__init__()
        self._app = app

        self._data = None

        self._ins      = None
        self._ins_item = None

        self._has_changed = False


    def setupUi(self, window):
        super().setupUi(window)
        #Ui_MainWindow.setupUi(self)

        self._window = window
        window.setWindowTitle(window_title)

        single_instruments = self.treeWidget.topLevelItem(0)
        multiple_instruments = self.treeWidget.topLevelItem(1)
        for back in ['A', 'B', 'C', 'D']:
            for nr in range(1,17):
                it = QtWidgets.QTreeWidgetItem([f'{back}{nr:02d}'])
                single_instruments.addChild(it)
                it = QtWidgets.QTreeWidgetItem([f'{back}{nr:02d}'])
                multiple_instruments.addChild(it)
        self.treeWidget.itemClicked.connect(self.onItemClicked)

        # define the change functions for all widgets
        self.si_name.textChanged.connect(self.ins_gen_valueChanged('set_name'))
        self.si_volume.valueChanged.connect(self.ins_gen_valueChanged('set_volume'))


    # generator to change a data entry
    # the function is connected to a widget, so the inner function
    # wil be called with the new value,
    # with 'funcname' the name of the set function can be specified,
    # so the specific value can be set, important is that
    # self._ins can be changed externally, it will always the correct
    # instance member function be called!
    def ins_gen_valueChanged(self, funcname):

        def valuechanged(val):
            func = getattr(self._ins, funcname)
            func(val)

            self._bas_changed = True
            self._window.setWindowTitle(window_title+' *')

            if funcname == 'set_name':
                if self._ins_item is not None:
                   s = self._ins_item.text(0).split()[0]+' - '+val
                   self._ins_item.setText(0, s)

        return valuechanged


    def select_instrument(self, si_nr):
        # selects the si_nr'th instrument
        ins = self._data['single_instruments'][si_nr]
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
        self.si_wheel_assign.children()[ins.wheel_assign].setChecked(True)
        self.si_vib_shape.children()[ins.vib_shape].setChecked(True)
        self.si_am_s12.setChecked(ins.am12)
        self.si_am_s34.setChecked(ins.am34)
        self.s1_wave.setValue(ins.s1_wave_select)
        self.s1_ks_curve.setValue(ins.s1_ks_curve)
        self.s1_delay.setValue(ins.s1_delay)
        self.s1_coarse.setValue(ins.s1_coarse)
        self.s1_fix.setValue(ins.s1_fix)
        self.s1_fine.setValue(ins.s1_fine)
        self.s1_key_track.setChecked(ins.s1_key_track)
        self.s1_prs_freq.setChecked(ins.s1_prs_frq)
        self.s1_vib_bend.setChecked(ins.s1_vib_bend)
        self.s1_vel_curve.setValue(ins.s1_vel_curve)
        self.s2_wave.setValue(ins.s2_wave_select)
        self.s2_ks_curve.setValue(ins.s2_ks_curve)
        self.s2_delay.setValue(ins.s2_delay)
        self.s2_coarse.setValue(ins.s2_coarse)
        self.s2_fix.setValue(ins.s2_fix)
        self.s2_fine.setValue(ins.s2_fine)
        self.s2_key_track.setChecked(ins.s2_key_track)
        self.s2_prs_freq.setChecked(ins.s2_prs_frq)
        self.s2_vib_bend.setChecked(ins.s2_vib_bend)
        self.s2_vel_curve.setValue(ins.s2_vel_curve)
        self.s3_wave.setValue(ins.s3_wave_select)
        self.s3_ks_curve.setValue(ins.s3_ks_curve)
        self.s3_delay.setValue(ins.s3_delay)
        self.s3_coarse.setValue(ins.s3_coarse)
        self.s3_fix.setValue(ins.s3_fix)
        self.s3_fine.setValue(ins.s3_fine)
        self.s3_key_track.setChecked(ins.s3_key_track)
        self.s3_prs_freq.setChecked(ins.s3_prs_frq)
        self.s3_vib_bend.setChecked(ins.s3_vib_bend)
        self.s3_vel_curve.setValue(ins.s3_vel_curve)
        self.s4_wave.setValue(ins.s4_wave_select)
        self.s4_ks_curve.setValue(ins.s4_ks_curve)
        self.s4_delay.setValue(ins.s4_delay)
        self.s4_coarse.setValue(ins.s4_coarse)
        self.s4_fix.setValue(ins.s4_fix)
        self.s4_fine.setValue(ins.s4_fine)
        self.s4_key_track.setChecked(ins.s4_key_track)
        self.s4_prs_freq.setChecked(ins.s4_prs_frq)
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




    @Slot(QtWidgets.QTreeWidgetItem, int)
    def onItemClicked(self, item, col):
        print(item, col, item.text(col))
        print('Clicked')
        print(item.parent())
        if item.parent() is not None:
            # correct sub element ;-)
            print('>',item.parent().text(0))
            if item.parent().text(0) == 'Single Instruments':
                # select instrument
                if self._data is not None and 'single_instruments' in self._data:
                    si_nr = name2pos(item.text(col))
                    self.select_instrument(si_nr)
                    self._ins_item = item




    def file_open(self, filename):
        mf = K4Dump(filename)

        print(mf.version())

        self._data = mf.parse_midi_stream()

        # insert single multiple_instruments
        single_instruments = self.treeWidget.topLevelItem(0)
        nr = 0
        for ins in self._data['single_instruments']:
            #print(ins.name)
            w = single_instruments.child(nr)
            pre = w.text(0).split()[0]
            w.setText(0, f'{pre} - {ins.name}')
            nr += 1

        self.select_instrument(0)
        self._ins_item = self.treeWidget.topLevelItem(0).child(0)

        self._window.setWindowTitle(window_title)


