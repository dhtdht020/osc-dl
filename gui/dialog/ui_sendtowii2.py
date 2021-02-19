# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sendtowii2.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(400, 427)
        MainWindow.setMinimumSize(QSize(400, 427))
        MainWindow.setStyleSheet(u"[accessibleName=\"background\"] {\n"
"background-color: rgb(255, 255, 255);\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.TitleFrame = QFrame(self.centralwidget)
        self.TitleFrame.setObjectName(u"TitleFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TitleFrame.sizePolicy().hasHeightForWidth())
        self.TitleFrame.setSizePolicy(sizePolicy)
        self.TitleFrame.setMinimumSize(QSize(0, 48))
        self.TitleFrame.setMaximumSize(QSize(16777215, 40))
        self.TitleFrame.setStyleSheet(u"")
        self.TitleFrame.setFrameShape(QFrame.StyledPanel)
        self.TitleFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.TitleFrame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.SendToWiiTitleFrame = QFrame(self.TitleFrame)
        self.SendToWiiTitleFrame.setObjectName(u"SendToWiiTitleFrame")
        self.SendToWiiTitleFrame.setMinimumSize(QSize(0, 48))
        self.SendToWiiTitleFrame.setStyleSheet(u"QFrame {\n"
"	background-color: #3273dc\n"
"}")
        self.SendToWiiTitleFrame.setFrameShape(QFrame.StyledPanel)
        self.SendToWiiTitleFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.SendToWiiTitleFrame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 0, 0, 0)
        self.TitleLabel = QLabel(self.SendToWiiTitleFrame)
        self.TitleLabel.setObjectName(u"TitleLabel")
        self.TitleLabel.setMinimumSize(QSize(0, 0))
        self.TitleLabel.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setPointSize(19)
        self.TitleLabel.setFont(font)
        self.TitleLabel.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"}")

        self.horizontalLayout_3.addWidget(self.TitleLabel)


        self.horizontalLayout_2.addWidget(self.SendToWiiTitleFrame)

        self.HomebrewIconLabel = QLabel(self.TitleFrame)
        self.HomebrewIconLabel.setObjectName(u"HomebrewIconLabel")
        self.HomebrewIconLabel.setMinimumSize(QSize(128, 48))
        self.HomebrewIconLabel.setMaximumSize(QSize(128, 48))
        self.HomebrewIconLabel.setStyleSheet(u"QLabel {\n"
"	background-color: #eff1fa;\n"
"}")
        self.HomebrewIconLabel.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.HomebrewIconLabel)


        self.verticalLayout.addWidget(self.TitleFrame)

        self.verticalSpacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.HelpLabel = QLabel(self.centralwidget)
        self.HelpLabel.setObjectName(u"HelpLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.HelpLabel.sizePolicy().hasHeightForWidth())
        self.HelpLabel.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.HelpLabel)

        self.MetadataFrame = QFrame(self.centralwidget)
        self.MetadataFrame.setObjectName(u"MetadataFrame")
        self.MetadataFrame.setStyleSheet(u"QFrame {\n"
"	background-color: #eff1fa;\n"
"}")
        self.MetadataFrame.setFrameShape(QFrame.StyledPanel)
        self.MetadataFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.MetadataFrame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_3 = QFrame(self.MetadataFrame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.MetaLayout = QFormLayout()
        self.MetaLayout.setObjectName(u"MetaLayout")
        self.label_version = QLabel(self.frame_3)
        self.label_version.setObjectName(u"label_version")

        self.MetaLayout.setWidget(1, QFormLayout.LabelRole, self.label_version)

        self.version = QLineEdit(self.frame_3)
        self.version.setObjectName(u"version")
        self.version.setMinimumSize(QSize(149, 20))
        self.version.setEchoMode(QLineEdit.Normal)
        self.version.setReadOnly(True)

        self.MetaLayout.setWidget(1, QFormLayout.FieldRole, self.version)

        self.label_developer = QLabel(self.frame_3)
        self.label_developer.setObjectName(u"label_developer")

        self.MetaLayout.setWidget(2, QFormLayout.LabelRole, self.label_developer)

        self.label_releasedate = QLabel(self.frame_3)
        self.label_releasedate.setObjectName(u"label_releasedate")

        self.MetaLayout.setWidget(3, QFormLayout.LabelRole, self.label_releasedate)

        self.label_filesize = QLabel(self.frame_3)
        self.label_filesize.setObjectName(u"label_filesize")

        self.MetaLayout.setWidget(4, QFormLayout.LabelRole, self.label_filesize)

        self.filesize = QLineEdit(self.frame_3)
        self.filesize.setObjectName(u"filesize")
        self.filesize.setMinimumSize(QSize(149, 20))
        self.filesize.setEchoMode(QLineEdit.Normal)
        self.filesize.setReadOnly(True)

        self.MetaLayout.setWidget(4, QFormLayout.FieldRole, self.filesize)

        self.appname = QLineEdit(self.frame_3)
        self.appname.setObjectName(u"appname")
        self.appname.setMinimumSize(QSize(149, 20))
        self.appname.setEchoMode(QLineEdit.Normal)
        self.appname.setReadOnly(True)

        self.MetaLayout.setWidget(0, QFormLayout.FieldRole, self.appname)

        self.label_appname = QLabel(self.frame_3)
        self.label_appname.setObjectName(u"label_appname")

        self.MetaLayout.setWidget(0, QFormLayout.LabelRole, self.label_appname)

        self.releasedate = QLineEdit(self.frame_3)
        self.releasedate.setObjectName(u"releasedate")
        self.releasedate.setMinimumSize(QSize(149, 20))
        self.releasedate.setEchoMode(QLineEdit.Normal)
        self.releasedate.setReadOnly(True)

        self.MetaLayout.setWidget(3, QFormLayout.FieldRole, self.releasedate)

        self.developer = QLineEdit(self.frame_3)
        self.developer.setObjectName(u"developer")
        self.developer.setMinimumSize(QSize(149, 20))
        self.developer.setEchoMode(QLineEdit.Normal)
        self.developer.setReadOnly(True)

        self.MetaLayout.setWidget(2, QFormLayout.FieldRole, self.developer)


        self.verticalLayout_3.addLayout(self.MetaLayout)


        self.horizontalLayout.addWidget(self.frame_3)


        self.verticalLayout.addWidget(self.MetadataFrame)

        self.HelpLabel2 = QLabel(self.centralwidget)
        self.HelpLabel2.setObjectName(u"HelpLabel2")

        self.verticalLayout.addWidget(self.HelpLabel2)

        self.IPFrame = QFrame(self.centralwidget)
        self.IPFrame.setObjectName(u"IPFrame")
        self.IPFrame.setStyleSheet(u"QFrame {\n"
"	background-color: #eff1fa;\n"
"}")
        self.IPFrame.setFrameShape(QFrame.StyledPanel)
        self.IPFrame.setFrameShadow(QFrame.Raised)
        self.formLayout = QFormLayout(self.IPFrame)
        self.formLayout.setObjectName(u"formLayout")
        self.IPLabel = QLabel(self.IPFrame)
        self.IPLabel.setObjectName(u"IPLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.IPLabel)

        self.IPEdit = QLineEdit(self.IPFrame)
        self.IPEdit.setObjectName(u"IPEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.IPEdit)


        self.verticalLayout.addWidget(self.IPFrame)

        self.InstructionsFrame = QFrame(self.centralwidget)
        self.InstructionsFrame.setObjectName(u"InstructionsFrame")
        self.InstructionsFrame.setMinimumSize(QSize(0, 72))
        self.InstructionsFrame.setStyleSheet(u"QFrame {\n"
"	background-color: #eff1fa;\n"
"}")
        self.InstructionsFrame.setFrameShape(QFrame.StyledPanel)
        self.InstructionsFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.InstructionsFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.InstructionsLabel = QLabel(self.InstructionsFrame)
        self.InstructionsLabel.setObjectName(u"InstructionsLabel")

        self.verticalLayout_2.addWidget(self.InstructionsLabel)

        self.StatusLabel = QLabel(self.InstructionsFrame)
        self.StatusLabel.setObjectName(u"StatusLabel")
        self.StatusLabel.setVisible(False)

        self.verticalLayout_2.addWidget(self.StatusLabel)

        self.ProgressBar = QProgressBar(self.InstructionsFrame)
        self.ProgressBar.setObjectName(u"ProgressBar")
        self.ProgressBar.setValue(0)
        self.ProgressBar.setVisible(False)

        self.verticalLayout_2.addWidget(self.ProgressBar)


        self.verticalLayout.addWidget(self.InstructionsFrame)

        self.SendButton = QPushButton(self.centralwidget)
        self.SendButton.setObjectName(u"SendButton")
        self.SendButton.setEnabled(False)

        self.verticalLayout.addWidget(self.SendButton)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
#if QT_CONFIG(accessibility)
        self.centralwidget.setAccessibleName(QCoreApplication.translate("MainWindow", u"background", None))
#endif // QT_CONFIG(accessibility)
        self.TitleLabel.setText(QCoreApplication.translate("MainWindow", u"Send to Wii", None))
        self.HomebrewIconLabel.setText(QCoreApplication.translate("MainWindow", u"No homebrew icon. Aw.", None))
        self.HelpLabel.setText(QCoreApplication.translate("MainWindow", u"The following application will be sent:", None))
        self.label_version.setText(QCoreApplication.translate("MainWindow", u"Version", None))
        self.label_developer.setText(QCoreApplication.translate("MainWindow", u"Developer", None))
        self.label_releasedate.setText(QCoreApplication.translate("MainWindow", u"Release Date", None))
        self.label_filesize.setText(QCoreApplication.translate("MainWindow", u"File Size", None))
        self.appname.setText("")
        self.appname.setPlaceholderText("")
        self.label_appname.setText(QCoreApplication.translate("MainWindow", u"App Name", None))
        self.HelpLabel2.setText(QCoreApplication.translate("MainWindow", u"To the wii console at:", None))
        self.IPLabel.setText(QCoreApplication.translate("MainWindow", u"IP Address", None))
        self.IPEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter IP address..", None))
        self.InstructionsLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>To find your Wii's IP address:<br/>1) Enter the Homebrew Channel.<br/>2) Press the home button on the Wii Remote.<br/>3) Copy the IP address written in the top left corner.</p></body></html>", None))
        self.StatusLabel.setText(QCoreApplication.translate("MainWindow", u"Sending to Wii..", None))
        self.SendButton.setText(QCoreApplication.translate("MainWindow", u"Send", None))
    # retranslateUi

