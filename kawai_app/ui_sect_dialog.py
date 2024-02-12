# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sect_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QLabel, QSizePolicy, QSpinBox, QWidget)

class Ui_Sect_Dialog(object):
    def setupUi(self, Sect_Dialog):
        if not Sect_Dialog.objectName():
            Sect_Dialog.setObjectName(u"Sect_Dialog")
        Sect_Dialog.resize(173, 85)
        self.buttonBox = QDialogButtonBox(Sect_Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(10, 40, 151, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.label = QLabel(Sect_Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 58, 22))
        self.sect_sel = QSpinBox(Sect_Dialog)
        self.sect_sel.setObjectName(u"sect_sel")
        self.sect_sel.setGeometry(QRect(90, 10, 42, 22))
        self.sect_sel.setMinimum(1)
        self.sect_sel.setMaximum(8)

        self.retranslateUi(Sect_Dialog)
        self.buttonBox.accepted.connect(Sect_Dialog.accept)
        self.buttonBox.rejected.connect(Sect_Dialog.reject)

        QMetaObject.connectSlotsByName(Sect_Dialog)
    # setupUi

    def retranslateUi(self, Sect_Dialog):
        Sect_Dialog.setWindowTitle(QCoreApplication.translate("Sect_Dialog", u"Instrument Section ", None))
        self.label.setText(QCoreApplication.translate("Sect_Dialog", u"Section:", None))
    # retranslateUi

