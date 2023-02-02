# mainform.py
#
# written by: Oliver Cordes 2023-01-30
# changed by: Oliver Cordes 2023-02-02

from ui_form import Ui_MainWindow

from PySide6.QtCore import Slot
from PySide6 import QtWidgets

from k4midi.k4dump import K4Dump

class MainUI(Ui_MainWindow):
    def __init__(self, app):
        #Ui_MainWindow.__init__(self)
        super().__init__()
        self._app = app


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


    @Slot(QtWidgets.QTreeWidgetItem, int)
    def onItemClicked(self, item, col):
        print(item, col, item.text(col))
        print('Clicked')
        print(item.parent())
        if item.parent() is not None:
            # correct sub element ;-)
            print(item.parent().text(0))
        #print(params)
        #print(params.data)
        #print(dir(params))


    def file_open(self, filename):
        mf = K4Dump(filename)

        print(mf.version())

        results = mf.parse_midi_stream()


