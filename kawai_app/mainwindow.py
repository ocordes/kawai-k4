# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QMainWindow

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
        self.ui = MainUI(app)
        self.ui.setupUi(self)
        self.ui.action_Quit.triggered.connect(self.prg_quit)
        self.ui.action_Open.triggered.connect(self.file_open)
        self.ui.action_Save.triggered.connect(self.file_save)
        self.ui.actionSave_As.triggered.connect(self.file_saveas)

    def prg_quit(self):
        self._app.quit()

    def file_open(self):
        print('File Open')
        self.ui.file_open('k4.mid')


    def file_save(self):
        print('File Save')

    def file_saveas(self):
        print('File SaveAs')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow(app)
    widget.show()
    sys.exit(app.exec())