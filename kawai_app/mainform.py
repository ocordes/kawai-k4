# mainform.py
#
# written by: Oliver Cordes 2023-01-30
# changed by: Oliver Cordes 2023-02-025

from ui_form import Ui_MainWindow

from PySide6.QtCore import Slot
from PySide6 import QtWidgets

from k4midi.k4dump import K4Dump


# helper functions
def name2pos(name):
    return (ord(name[0]) - ord('A'))*16 + int(name[1:3])-1


class MainUI(Ui_MainWindow):
    def __init__(self, app):
        #Ui_MainWindow.__init__(self)
        super().__init__()
        self._app = app

        self._data = None


    def setupUi(self, window):
        super().setupUi(window)
        #Ui_MainWindow.setupUi(self)

        single_instruments = self.treeWidget.topLevelItem(0)
        multiple_instruments = self.treeWidget.topLevelItem(1)
        for back in ['A', 'B', 'C', 'D']:
            for nr in range(1,17):
                it = QtWidgets.QTreeWidgetItem([f'{back}{nr:02d}'])
                single_instruments.addChild(it)
                it = QtWidgets.QTreeWidgetItem([f'{back}{nr:02d}'])
                multiple_instruments.addChild(it)
        self.treeWidget.itemClicked.connect(self.onItemClicked)

        #self.


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
                    ins = self._data['single_instruments'][si_nr]
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

