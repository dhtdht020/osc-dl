# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'forwarderwiz.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_Wizard(object):
    def setupUi(self, Wizard):
        if not Wizard.objectName():
            Wizard.setObjectName(u"Wizard")
        Wizard.resize(400, 300)
        Wizard.setWizardStyle(QWizard.ModernStyle)
        self.wizardPage1 = QWizardPage()
        self.wizardPage1.setObjectName(u"wizardPage1")
        self.verticalLayout = QVBoxLayout(self.wizardPage1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.wizardPage1)
        self.label.setObjectName(u"label")
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        self.label_2 = QLabel(self.wizardPage1)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_2)

        self.label_3 = QLabel(self.wizardPage1)
        self.label_3.setObjectName(u"label_3")
        font = QFont()
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_3)

        Wizard.addPage(self.wizardPage1)
        self.wizardPage2 = QWizardPage()
        self.wizardPage2.setObjectName(u"wizardPage2")
        self.verticalLayout_2 = QVBoxLayout(self.wizardPage2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_4 = QLabel(self.wizardPage2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label_4)

        self.AvailableIDsListWidget = QListWidget(self.wizardPage2)
        self.AvailableIDsListWidget.setObjectName(u"AvailableIDsListWidget")
        self.AvailableIDsListWidget.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.AvailableIDsListWidget)

        Wizard.addPage(self.wizardPage2)
        self.wizardPage3 = QWizardPage()
        self.wizardPage3.setObjectName(u"wizardPage3")
        self.verticalLayout_3 = QVBoxLayout(self.wizardPage3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_5 = QLabel(self.wizardPage3)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_3.addWidget(self.label_5)

        self.RadioSelectOSC = QRadioButton(self.wizardPage3)
        self.RadioSelectOSC.setObjectName(u"RadioSelectOSC")
        self.RadioSelectOSC.setChecked(True)

        self.verticalLayout_3.addWidget(self.RadioSelectOSC)

        self.SelectOSCApplication = QPushButton(self.wizardPage3)
        self.SelectOSCApplication.setObjectName(u"SelectOSCApplication")

        self.verticalLayout_3.addWidget(self.SelectOSCApplication)

        self.RadioSelectLocal = QRadioButton(self.wizardPage3)
        self.RadioSelectLocal.setObjectName(u"RadioSelectLocal")

        self.verticalLayout_3.addWidget(self.RadioSelectLocal)

        self.SelectLocalDirApplication = QPushButton(self.wizardPage3)
        self.SelectLocalDirApplication.setObjectName(u"SelectLocalDirApplication")
        self.SelectLocalDirApplication.setEnabled(False)

        self.verticalLayout_3.addWidget(self.SelectLocalDirApplication)

        Wizard.addPage(self.wizardPage3)
        self.wizardPage4 = QWizardPage()
        self.wizardPage4.setObjectName(u"wizardPage4")
        self.verticalLayout_4 = QVBoxLayout(self.wizardPage4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_6 = QLabel(self.wizardPage4)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)
        self.label_6.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.label_6)

        self.Summary_SDCardPath = QLabel(self.wizardPage4)
        self.Summary_SDCardPath.setObjectName(u"Summary_SDCardPath")
        self.Summary_SDCardPath.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.Summary_SDCardPath)

        self.label_7 = QLabel(self.wizardPage4)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font)
        self.label_7.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.label_7)

        self.Summary_ApplicationSource = QLabel(self.wizardPage4)
        self.Summary_ApplicationSource.setObjectName(u"Summary_ApplicationSource")
        self.Summary_ApplicationSource.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.Summary_ApplicationSource)

        self.label_8 = QLabel(self.wizardPage4)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font)
        self.label_8.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.label_8)

        self.Summary_TitleID = QLabel(self.wizardPage4)
        self.Summary_TitleID.setObjectName(u"Summary_TitleID")
        self.Summary_TitleID.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.Summary_TitleID)

        Wizard.addPage(self.wizardPage4)
        self.wizardPage5 = QWizardPage()
        self.wizardPage5.setObjectName(u"wizardPage5")
        self.verticalLayout_5 = QVBoxLayout(self.wizardPage5)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.graphicsView = QGraphicsView(self.wizardPage5)
        self.graphicsView.setObjectName(u"graphicsView")

        self.verticalLayout_5.addWidget(self.graphicsView)

        self.progressBar = QProgressBar(self.wizardPage5)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.verticalLayout_5.addWidget(self.progressBar)

        self.StatusLabel = QLabel(self.wizardPage5)
        self.StatusLabel.setObjectName(u"StatusLabel")

        self.verticalLayout_5.addWidget(self.StatusLabel)

        Wizard.addPage(self.wizardPage5)

        self.retranslateUi(Wizard)

        QMetaObject.connectSlotsByName(Wizard)
    # setupUi

    def retranslateUi(self, Wizard):
        Wizard.setWindowTitle(QCoreApplication.translate("Wizard", u"Create Forwarder", None))
        self.wizardPage1.setTitle(QCoreApplication.translate("Wizard", u"Forwarder Creation Wizard", None))
        self.label.setText(QCoreApplication.translate("Wizard", u"This automatic wizard will assist you on the process of creating a forwarder channel for this application.", None))
        self.label_2.setText(QCoreApplication.translate("Wizard", u"Forwarders are shortcut channels to homebrew which display on the Home Menu.", None))
        self.label_3.setText(QCoreApplication.translate("Wizard", u"Press \"Next\" to begin.", None))
        self.wizardPage2.setTitle(QCoreApplication.translate("Wizard", u"Select Title ID", None))
        self.wizardPage2.setSubTitle(QCoreApplication.translate("Wizard", u"Choose a Title ID which isn't used by existing channels or forwarders.", None))
        self.label_4.setText(QCoreApplication.translate("Wizard", u"Available Title IDs (From GameTDB, some might already be used by other forwarders):", None))
        self.wizardPage3.setTitle(QCoreApplication.translate("Wizard", u"Select Application", None))
        self.wizardPage3.setSubTitle(QCoreApplication.translate("Wizard", u"Select App from Open Shop Channel or from local directory", None))
        self.label_5.setText(QCoreApplication.translate("Wizard", u"Select an application:", None))
        self.RadioSelectOSC.setText(QCoreApplication.translate("Wizard", u"Application from Open Shop Channel", None))
        self.SelectOSCApplication.setText(QCoreApplication.translate("Wizard", u"Select App", None))
        self.RadioSelectLocal.setText(QCoreApplication.translate("Wizard", u"Application from local directory", None))
        self.SelectLocalDirApplication.setText(QCoreApplication.translate("Wizard", u"Open Folder", None))
        self.wizardPage4.setTitle(QCoreApplication.translate("Wizard", u"Summary", None))
        self.wizardPage4.setSubTitle(QCoreApplication.translate("Wizard", u"Summary of forwarder to generate", None))
        self.label_6.setText(QCoreApplication.translate("Wizard", u"SD Card Path:", None))
        self.Summary_SDCardPath.setText("")
        self.label_7.setText(QCoreApplication.translate("Wizard", u"Application Source:", None))
        self.Summary_ApplicationSource.setText("")
        self.label_8.setText(QCoreApplication.translate("Wizard", u"Title ID:", None))
        self.Summary_TitleID.setText("")
        self.wizardPage5.setTitle(QCoreApplication.translate("Wizard", u"Generating Forwarder...", None))
        self.wizardPage5.setSubTitle(QCoreApplication.translate("Wizard", u"OSCDL Forwarder Wizard is preparing your forwarder.", None))
        self.StatusLabel.setText(QCoreApplication.translate("Wizard", u"Status: ", None))
    # retranslateUi

