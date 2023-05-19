# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'wiiloadInstallerMSGDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractScrollArea, QApplication, QDialog,
    QDialogButtonBox, QGridLayout, QGroupBox, QLabel,
    QSizePolicy, QTextEdit, QVBoxLayout, QWidget)

class Ui_MSGBox(object):
    def setupUi(self, MSGBox):
        if not MSGBox.objectName():
            MSGBox.setObjectName(u"MSGBox")
        MSGBox.resize(572, 203)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MSGBox.sizePolicy().hasHeightForWidth())
        MSGBox.setSizePolicy(sizePolicy)
        MSGBox.setMinimumSize(QSize(0, 0))
        self.verticalLayout = QVBoxLayout(MSGBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(25, -1, 25, -1)
        self.groupBox = QGroupBox(MSGBox)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(False)
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.textBox = QTextEdit(self.groupBox)
        self.textBox.setObjectName(u"textBox")
        self.textBox.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textBox.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textBox.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.textBox.setReadOnly(True)

        self.gridLayout.addWidget(self.textBox, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.groupBox)

        self.HBNotice = QLabel(MSGBox)
        self.HBNotice.setObjectName(u"HBNotice")
        sizePolicy.setHeightForWidth(self.HBNotice.sizePolicy().hasHeightForWidth())
        self.HBNotice.setSizePolicy(sizePolicy)
        self.HBNotice.setScaledContents(True)
        self.HBNotice.setAlignment(Qt.AlignCenter)
        self.HBNotice.setMargin(0)

        self.verticalLayout.addWidget(self.HBNotice)

        self.OK = QDialogButtonBox(MSGBox)
        self.OK.setObjectName(u"OK")
        self.OK.setOrientation(Qt.Horizontal)
        self.OK.setStandardButtons(QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.OK)


        self.retranslateUi(MSGBox)
        self.OK.accepted.connect(MSGBox.accept)

        QMetaObject.connectSlotsByName(MSGBox)
    # setupUi

    def retranslateUi(self, MSGBox):
        MSGBox.setWindowTitle(QCoreApplication.translate("MSGBox", u"Installation Notice", None))
        self.groupBox.setTitle(QCoreApplication.translate("MSGBox", u"Installation Notice", None))
        self.textBox.setPlaceholderText(QCoreApplication.translate("MSGBox", u"Something went wrong...", None))
        self.HBNotice.setText(QCoreApplication.translate("MSGBox", u"<strong>Click OK after returning to the Homebrew Channel and the network is connected.</strong>", None))
    # retranslateUi

