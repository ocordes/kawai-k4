# mainform.py
#
# written by: Oliver Cordes 2023-01-30
# changed by: Oliver Cordes 2023-01-30

from ui_form import Ui_MainWindow

from PySide6.QtCore import Slot
from PySide6 import QtWidgets

class MainUI(Ui_MainWindow):
    def __init__(self, app):
        #Ui_MainWindow.__init__(self)
        super().__init__()
        self._app = app


    def setupUi(self, window):
        super().setupUi(window)
        #Ui_MainWindow.setupUi(self)

        for back in ['A', 'B', 'C', 'D']:
            for nr in range(1,17):
                pass
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


