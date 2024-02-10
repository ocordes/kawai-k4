# This Python file uses the following encoding: utf-8

# written by: Oliver Cordes 2023-01-30
# changed by: Oliver Cordes 2023-05-06

import sys, os

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication, QMainWindow , QFileDialog


translate = QCoreApplication.translate

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py

from ui_form import Ui_MainWindow

from mainform import MainUI


class MainWindow(QMainWindow):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self._app = app
        #self.ui = Ui_MainWindow()
        self.ui = MainUI(app, self)
        self.ui.setupUi(self)
        self.ui.action_Quit.triggered.connect(self.prg_quit)
        self.ui.action_Open.triggered.connect(self.file_open)
        self.ui.actionOpen_Default.triggered.connect(self.file_open_default)
        self.ui.action_Save.triggered.connect(self.file_save)
        self.ui.actionSave_As.triggered.connect(self.file_saveas)

    def prg_quit(self):
        self._app.quit()

    def file_open(self):
        self.ui.file_open()
        #print('File Open')
        #fileName = QFileDialog.getOpenFileName(self, translate('main', "Open File"),
        #                                                os.getcwd(),
        #                                                translate('main', "MIDI Files (*.mid *.MID *.MIDI);;SysEX Files (*.syx)"))
        #print(fileName)
        #if fileName[0] != '':
        #s    self.ui.file_open_file(fileName[0])


    def file_open_default(self):
        self.ui.file_open_file('k4.mid', read_only=True)

    def file_save(self):
        self.ui.file_save(None)

    def file_saveas(self):
        self.ui.file_saveas()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow(app)
    widget.show()
    sys.exit(app.exec())
