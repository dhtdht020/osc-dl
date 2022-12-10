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
    QDialogButtonBox, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QTabWidget,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(484, 274)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.Tab = QTabWidget(Dialog)
        self.Tab.setObjectName(u"Tab")
        self.Tab.setFocusPolicy(Qt.ClickFocus)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_3 = QVBoxLayout(self.tab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.IPDes = QLabel(self.tab)
        self.IPDes.setObjectName(u"IPDes")

        self.verticalLayout_3.addWidget(self.IPDes)

        self.frame = QFrame(self.tab)
        self.frame.setObjectName(u"frame")
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.IPBox = QLineEdit(self.frame)
        self.IPBox.setObjectName(u"IPBox")

        self.horizontalLayout.addWidget(self.IPBox)


        self.verticalLayout_3.addWidget(self.frame)

        self.Tab.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_4 = QVBoxLayout(self.tab_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.USBDes = QLabel(self.tab_2)
        self.USBDes.setObjectName(u"USBDes")

        self.verticalLayout_4.addWidget(self.USBDes)

        self.frame_2 = QFrame(self.tab_2)
        self.frame_2.setObjectName(u"frame_2")
        self.horizontalLayout_2 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.frame_2)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_2.addWidget(self.label_4)

        self.PortBox = QComboBox(self.frame_2)
        self.PortBox.setObjectName(u"PortBox")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PortBox.sizePolicy().hasHeightForWidth())
        self.PortBox.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.PortBox)

        self.RefreshBTN = QPushButton(self.frame_2)
        self.RefreshBTN.setObjectName(u"RefreshBTN")

        self.horizontalLayout_2.addWidget(self.RefreshBTN)


        self.verticalLayout_4.addWidget(self.frame_2)

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

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Wii", None))
        self.IPDes.setText(QCoreApplication.translate("Dialog", u"Enter the IP address of your Wii.<br>\n"
"The selected app will be sent through the network to your Wii.<br><br>\n"
"<b>App to send:</b><br><br>\n"
"To find your Wii's IP address:<br>\n"
"1) Enter the Homebrew Channel.<br>\n"
"2) Press the home button on the Wii Remote.<br>\n"
"3) Copy the IP address written in the top left corner.", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"IP address (e.g. 192.168.1...):", None))
        self.Tab.setTabText(self.Tab.indexOf(self.tab), QCoreApplication.translate("Dialog", u"Network", None))
        self.USBDes.setText(QCoreApplication.translate("Dialog", u"Select the serial port for the USB Gecko adapter.<br>\n"
"The selected app will be sent through the USBGecko to your Wii.<br><br>\n"
"<b>App to send:</b><br><br>\n"
"Make sure the USB Gecko device is attached to Slot B.<br>\n"
"It may appear as /dev/cu.usbserial-GECKUSB0 or COM# depending on your system.<br><br>\n"
"<b>If the selection below is not blank, your USB Gecko is the selected device.</b>", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Device port:", None))
        self.RefreshBTN.setText(QCoreApplication.translate("Dialog", u"Refresh", None))
        self.Tab.setTabText(self.Tab.indexOf(self.tab_2), QCoreApplication.translate("Dialog", u"USB Gecko", None))
    # retranslateUi

