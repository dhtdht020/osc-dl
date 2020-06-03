# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'meta.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_Metadata(object):
    def setupUi(self, Metadata):
        if not Metadata.objectName():
            Metadata.setObjectName(u"Metadata")
        Metadata.resize(400, 200)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Metadata.sizePolicy().hasHeightForWidth())
        Metadata.setSizePolicy(sizePolicy)
        Metadata.setMinimumSize(QSize(400, 200))
        Metadata.setMaximumSize(QSize(400, 200))
        self.HowToContinueBox = QGroupBox(Metadata)
        self.HowToContinueBox.setObjectName(u"HowToContinueBox")
        self.HowToContinueBox.setGeometry(QRect(250, 20, 141, 81))
        self.verticalLayoutWidget = QWidget(self.HowToContinueBox)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 20, 121, 51))
        self.HowToContinueLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.HowToContinueLayout.setObjectName(u"HowToContinueLayout")
        self.HowToContinueLayout.setContentsMargins(0, 0, 0, 0)
        self.DownloadAppBtn = QPushButton(self.verticalLayoutWidget)
        self.DownloadAppBtn.setObjectName(u"DownloadAppBtn")
        self.DownloadAppBtn.setAutoFillBackground(False)
        self.DownloadAppBtn.setFlat(False)

        self.HowToContinueLayout.addWidget(self.DownloadAppBtn)

        self.CloseBtn = QPushButton(self.verticalLayoutWidget)
        self.CloseBtn.setObjectName(u"CloseBtn")

        self.HowToContinueLayout.addWidget(self.CloseBtn)

        self.AppTabs = QTabWidget(Metadata)
        self.AppTabs.setObjectName(u"AppTabs")
        self.AppTabs.setGeometry(QRect(10, 20, 231, 161))
        self.ApplicationMetadataTab = QWidget()
        self.ApplicationMetadataTab.setObjectName(u"ApplicationMetadataTab")
        self.formLayoutWidget = QWidget(self.ApplicationMetadataTab)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(10, 10, 211, 101))
        self.MetaLayout = QFormLayout(self.formLayoutWidget)
        self.MetaLayout.setObjectName(u"MetaLayout")
        self.MetaLayout.setContentsMargins(0, 0, 0, 0)
        self.label_appname = QLabel(self.formLayoutWidget)
        self.label_appname.setObjectName(u"label_appname")

        self.MetaLayout.setWidget(0, QFormLayout.LabelRole, self.label_appname)

        self.appname = QLineEdit(self.formLayoutWidget)
        self.appname.setObjectName(u"appname")
        self.appname.setEchoMode(QLineEdit.Normal)
        self.appname.setReadOnly(True)

        self.MetaLayout.setWidget(0, QFormLayout.FieldRole, self.appname)

        self.label_version = QLabel(self.formLayoutWidget)
        self.label_version.setObjectName(u"label_version")

        self.MetaLayout.setWidget(1, QFormLayout.LabelRole, self.label_version)

        self.version = QLineEdit(self.formLayoutWidget)
        self.version.setObjectName(u"version")
        self.version.setEchoMode(QLineEdit.Normal)
        self.version.setReadOnly(True)

        self.MetaLayout.setWidget(1, QFormLayout.FieldRole, self.version)

        self.label_developer = QLabel(self.formLayoutWidget)
        self.label_developer.setObjectName(u"label_developer")

        self.MetaLayout.setWidget(2, QFormLayout.LabelRole, self.label_developer)

        self.developer = QLineEdit(self.formLayoutWidget)
        self.developer.setObjectName(u"developer")
        self.developer.setEchoMode(QLineEdit.Normal)
        self.developer.setReadOnly(True)

        self.MetaLayout.setWidget(2, QFormLayout.FieldRole, self.developer)

        self.label_contributors = QLabel(self.formLayoutWidget)
        self.label_contributors.setObjectName(u"label_contributors")

        self.MetaLayout.setWidget(3, QFormLayout.LabelRole, self.label_contributors)

        self.contributors = QLineEdit(self.formLayoutWidget)
        self.contributors.setObjectName(u"contributors")
        self.contributors.setEchoMode(QLineEdit.Normal)
        self.contributors.setReadOnly(True)

        self.MetaLayout.setWidget(3, QFormLayout.FieldRole, self.contributors)

        self.PoweredByLabel = QLabel(self.ApplicationMetadataTab)
        self.PoweredByLabel.setObjectName(u"PoweredByLabel")
        self.PoweredByLabel.setGeometry(QRect(80, 110, 151, 21))
        self.AppTabs.addTab(self.ApplicationMetadataTab, "")
        self.SettingsTab = QWidget()
        self.SettingsTab.setObjectName(u"SettingsTab")
        self.GeneralConfig = QGroupBox(self.SettingsTab)
        self.GeneralConfig.setObjectName(u"GeneralConfig")
        self.GeneralConfig.setGeometry(QRect(10, 10, 201, 51))
        self.verticalLayoutWidget_3 = QWidget(self.GeneralConfig)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(10, 20, 181, 21))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.ExtractAppCheckbox = QCheckBox(self.verticalLayoutWidget_3)
        self.ExtractAppCheckbox.setObjectName(u"ExtractAppCheckbox")

        self.verticalLayout.addWidget(self.ExtractAppCheckbox)

        self.OutputConfig = QGroupBox(self.SettingsTab)
        self.OutputConfig.setObjectName(u"OutputConfig")
        self.OutputConfig.setGeometry(QRect(10, 70, 201, 51))
        self.formLayoutWidget_2 = QWidget(self.OutputConfig)
        self.formLayoutWidget_2.setObjectName(u"formLayoutWidget_2")
        self.formLayoutWidget_2.setGeometry(QRect(10, 20, 181, 22))
        self.formLayout = QFormLayout(self.formLayoutWidget_2)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.FileNameLabel = QLabel(self.formLayoutWidget_2)
        self.FileNameLabel.setObjectName(u"FileNameLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.FileNameLabel)

        self.FileNameLineEdit = QLineEdit(self.formLayoutWidget_2)
        self.FileNameLineEdit.setObjectName(u"FileNameLineEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.FileNameLineEdit)

        self.AppTabs.addTab(self.SettingsTab, "")
        self.HowToContinueBox_2 = QGroupBox(Metadata)
        self.HowToContinueBox_2.setObjectName(u"HowToContinueBox_2")
        self.HowToContinueBox_2.setGeometry(QRect(250, 110, 141, 71))
        self.label = QLabel(self.HowToContinueBox_2)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 20, 81, 16))

        self.retranslateUi(Metadata)

        self.DownloadAppBtn.setDefault(True)
        self.AppTabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Metadata)
    # setupUi

    def retranslateUi(self, Metadata):
        Metadata.setWindowTitle(QCoreApplication.translate("Metadata", u"Metadata", None))
#if QT_CONFIG(whatsthis)
        Metadata.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.HowToContinueBox.setTitle(QCoreApplication.translate("Metadata", u"How to continue?", None))
        self.DownloadAppBtn.setText(QCoreApplication.translate("Metadata", u"Download App", None))
        self.CloseBtn.setText(QCoreApplication.translate("Metadata", u"Close", None))
        self.label_appname.setText(QCoreApplication.translate("Metadata", u"App Name", None))
        self.appname.setText("")
        self.appname.setPlaceholderText("")
        self.label_version.setText(QCoreApplication.translate("Metadata", u"Version", None))
        self.label_developer.setText(QCoreApplication.translate("Metadata", u"Developer", None))
        self.label_contributors.setText(QCoreApplication.translate("Metadata", u"Contributors", None))
        self.PoweredByLabel.setText(QCoreApplication.translate("Metadata", u"From the Open Shop Channel", None))
        self.AppTabs.setTabText(self.AppTabs.indexOf(self.ApplicationMetadataTab), QCoreApplication.translate("Metadata", u"Application Metadata", None))
        self.GeneralConfig.setTitle(QCoreApplication.translate("Metadata", u"Options", None))
        self.ExtractAppCheckbox.setText(QCoreApplication.translate("Metadata", u"Extract Downloaded App", None))
        self.OutputConfig.setTitle(QCoreApplication.translate("Metadata", u"Output", None))
        self.FileNameLabel.setText(QCoreApplication.translate("Metadata", u"File Name", None))
        self.AppTabs.setTabText(self.AppTabs.indexOf(self.SettingsTab), QCoreApplication.translate("Metadata", u"Settings", None))
        self.HowToContinueBox_2.setTitle(QCoreApplication.translate("Metadata", u"Application Icon", None))
        self.label.setText(QCoreApplication.translate("Metadata", u"IconGoesHere", None))
    # retranslateUi

