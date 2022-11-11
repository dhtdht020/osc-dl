# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_wiiloaddialog.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QTabWidget, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(562, 427)
        Dialog.setMinimumSize(QSize(562, 427))
        Dialog.setMaximumSize(QSize(562, 427))
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.Tab = QTabWidget(Dialog)
        self.Tab.setObjectName(u"Tab")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.label_2 = QLabel(self.tab)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(80, 280, 191, 31))
        self.IPDes = QLabel(self.tab)
        self.IPDes.setObjectName(u"IPDes")
        self.IPDes.setGeometry(QRect(10, 10, 511, 251))
        self.IPBox = QLineEdit(self.tab)
        self.IPBox.setObjectName(u"IPBox")
        self.IPBox.setGeometry(QRect(270, 280, 181, 31))
        self.Tab.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.USBDes = QLabel(self.tab_2)
        self.USBDes.setObjectName(u"USBDes")
        self.USBDes.setGeometry(QRect(10, 10, 511, 251))
        self.label_4 = QLabel(self.tab_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(70, 290, 91, 16))
        self.PortBox = QComboBox(self.tab_2)
        self.PortBox.setObjectName(u"PortBox")
        self.PortBox.setGeometry(QRect(150, 280, 241, 41))
        self.RefreshBTN = QPushButton(self.tab_2)
        self.RefreshBTN.setObjectName(u"RefreshBTN")
        self.RefreshBTN.setGeometry(QRect(400, 280, 91, 41))
        self.Tab.addTab(self.tab_2, "")

        self.verticalLayout_2.addWidget(self.Tab)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.RefreshBTN.clicked.connect(Dialog.update)

        self.Tab.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Wii", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"IP address (e.g. 192.168.1...):", None))
        self.IPDes.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
        self.Tab.setTabText(self.Tab.indexOf(self.tab), QCoreApplication.translate("Dialog", u"Network", None))
        self.USBDes.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Device port:", None))
        self.RefreshBTN.setText(QCoreApplication.translate("Dialog", u"Refresh", None))
        self.Tab.setTabText(self.Tab.indexOf(self.tab_2), QCoreApplication.translate("Dialog", u"USB Gecko", None))
    # retranslateUi

