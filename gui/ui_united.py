# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'united.ui'
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


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(900, 400)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(900, 400))
        MainWindow.setMaximumSize(QSize(900, 400))
        MainWindow.setDockOptions(QMainWindow.AllowTabbedDocks|QMainWindow.AnimatedDocks)
        self.actionAbout_OSC_DL = QAction(MainWindow)
        self.actionAbout_OSC_DL.setObjectName(u"actionAbout_OSC_DL")
        self.actionAbout_OSC_DL.setEnabled(False)
        self.actionTXT_file = QAction(MainWindow)
        self.actionTXT_file.setObjectName(u"actionTXT_file")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.AppsLibraryBox = QGroupBox(self.centralwidget)
        self.AppsLibraryBox.setObjectName(u"AppsLibraryBox")
        self.AppsLibraryBox.setGeometry(QRect(10, 10, 601, 341))
        self.listAppsWidget = QListWidget(self.AppsLibraryBox)
        self.listAppsWidget.setObjectName(u"listAppsWidget")
        self.listAppsWidget.setGeometry(QRect(10, 20, 581, 311))
        self.SelectionInfoBox = QGroupBox(self.centralwidget)
        self.SelectionInfoBox.setObjectName(u"SelectionInfoBox")
        self.SelectionInfoBox.setGeometry(QRect(620, 10, 271, 341))
        self.ExtractAppCheckbox = QCheckBox(self.SelectionInfoBox)
        self.ExtractAppCheckbox.setObjectName(u"ExtractAppCheckbox")
        self.ExtractAppCheckbox.setGeometry(QRect(10, 260, 179, 17))
        self.progressBar = QProgressBar(self.SelectionInfoBox)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(180, 10, 91, 23))
        self.progressBar.setValue(0)
        self.tabMetadata = QTabWidget(self.SelectionInfoBox)
        self.tabMetadata.setObjectName(u"tabMetadata")
        self.tabMetadata.setGeometry(QRect(10, 20, 251, 221))
        self.GeneralTab = QWidget()
        self.GeneralTab.setObjectName(u"GeneralTab")
        self.formLayoutWidget = QWidget(self.GeneralTab)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(10, 60, 221, 126))
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

        self.label_releasedate = QLabel(self.formLayoutWidget)
        self.label_releasedate.setObjectName(u"label_releasedate")

        self.MetaLayout.setWidget(4, QFormLayout.LabelRole, self.label_releasedate)

        self.releasedate = QLineEdit(self.formLayoutWidget)
        self.releasedate.setObjectName(u"releasedate")
        self.releasedate.setEchoMode(QLineEdit.Normal)
        self.releasedate.setReadOnly(True)

        self.MetaLayout.setWidget(4, QFormLayout.FieldRole, self.releasedate)

        self.label_description = QLabel(self.GeneralTab)
        self.label_description.setObjectName(u"label_description")
        self.label_description.setGeometry(QRect(10, 30, 221, 16))
        self.label_description.setMaximumSize(QSize(221, 16777215))
        self.label_description.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)
        self.label_displayname = QLabel(self.GeneralTab)
        self.label_displayname.setObjectName(u"label_displayname")
        self.label_displayname.setGeometry(QRect(10, 10, 221, 16))
        self.label_displayname.setMaximumSize(QSize(221, 16777215))
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_displayname.setFont(font)
        self.label_displayname.setWordWrap(True)
        self.label_displayname.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)
        self.tabMetadata.addTab(self.GeneralTab, "")
        self.Description = QWidget()
        self.Description.setObjectName(u"Description")
        self.longDescriptionBrowser = QTextBrowser(self.Description)
        self.longDescriptionBrowser.setObjectName(u"longDescriptionBrowser")
        self.longDescriptionBrowser.setGeometry(QRect(10, 20, 221, 171))
        self.LongDescLabel = QLabel(self.Description)
        self.LongDescLabel.setObjectName(u"LongDescLabel")
        self.LongDescLabel.setGeometry(QRect(10, 0, 91, 20))
        self.tabMetadata.addTab(self.Description, "")
        self.ViewMetadataBtn = QPushButton(self.SelectionInfoBox)
        self.ViewMetadataBtn.setObjectName(u"ViewMetadataBtn")
        self.ViewMetadataBtn.setGeometry(QRect(10, 310, 149, 23))
        self.formLayoutWidget_2 = QWidget(self.SelectionInfoBox)
        self.formLayoutWidget_2.setObjectName(u"formLayoutWidget_2")
        self.formLayoutWidget_2.setGeometry(QRect(10, 280, 251, 22))
        self.MetaLayout_2 = QFormLayout(self.formLayoutWidget_2)
        self.MetaLayout_2.setObjectName(u"MetaLayout_2")
        self.MetaLayout_2.setContentsMargins(0, 0, 0, 0)
        self.FileNameLabel = QLabel(self.formLayoutWidget_2)
        self.FileNameLabel.setObjectName(u"FileNameLabel")

        self.MetaLayout_2.setWidget(0, QFormLayout.LabelRole, self.FileNameLabel)

        self.FileNameLineEdit = QLineEdit(self.formLayoutWidget_2)
        self.FileNameLineEdit.setObjectName(u"FileNameLineEdit")

        self.MetaLayout_2.setWidget(0, QFormLayout.FieldRole, self.FileNameLineEdit)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 900, 21))
        self.menuAbout = QMenu(self.menubar)
        self.menuAbout.setObjectName(u"menuAbout")
        self.menuExport = QMenu(self.menubar)
        self.menuExport.setObjectName(u"menuExport")
        self.menuApplication_List = QMenu(self.menuExport)
        self.menuApplication_List.setObjectName(u"menuApplication_List")
        MainWindow.setMenuBar(self.menubar)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        self.statusBar.setSizeGripEnabled(False)
        MainWindow.setStatusBar(self.statusBar)

        self.menubar.addAction(self.menuAbout.menuAction())
        self.menubar.addAction(self.menuExport.menuAction())
        self.menuAbout.addAction(self.actionAbout_OSC_DL)
        self.menuExport.addAction(self.menuApplication_List.menuAction())
        self.menuApplication_List.addAction(self.actionTXT_file)

        self.retranslateUi(MainWindow)

        self.listAppsWidget.setCurrentRow(-1)
        self.tabMetadata.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Open Shop Channel Downloader - Library", None))
        self.actionAbout_OSC_DL.setText(QCoreApplication.translate("MainWindow", u"About OSC-DL", None))
        self.actionTXT_file.setText(QCoreApplication.translate("MainWindow", u"Text File", None))
        self.AppsLibraryBox.setTitle(QCoreApplication.translate("MainWindow", u"Apps Library", None))
        self.SelectionInfoBox.setTitle(QCoreApplication.translate("MainWindow", u"Application Metadata", None))
        self.ExtractAppCheckbox.setText(QCoreApplication.translate("MainWindow", u"Extract Downloaded App", None))
        self.label_appname.setText(QCoreApplication.translate("MainWindow", u"App Name", None))
        self.appname.setText("")
        self.appname.setPlaceholderText("")
        self.label_version.setText(QCoreApplication.translate("MainWindow", u"Version", None))
        self.label_developer.setText(QCoreApplication.translate("MainWindow", u"Developer", None))
        self.label_contributors.setText(QCoreApplication.translate("MainWindow", u"Contributors", None))
        self.label_releasedate.setText(QCoreApplication.translate("MainWindow", u"Release Date", None))
        self.label_description.setText(QCoreApplication.translate("MainWindow", u"Description", None))
        self.label_displayname.setText(QCoreApplication.translate("MainWindow", u"Title", None))
        self.tabMetadata.setTabText(self.tabMetadata.indexOf(self.GeneralTab), QCoreApplication.translate("MainWindow", u"General", None))
        self.longDescriptionBrowser.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.LongDescLabel.setText(QCoreApplication.translate("MainWindow", u"Long Description", None))
        self.tabMetadata.setTabText(self.tabMetadata.indexOf(self.Description), QCoreApplication.translate("MainWindow", u"Long Description", None))
        self.ViewMetadataBtn.setText(QCoreApplication.translate("MainWindow", u"Download App", None))
        self.FileNameLabel.setText(QCoreApplication.translate("MainWindow", u"Output File", None))
        self.menuAbout.setTitle(QCoreApplication.translate("MainWindow", u"About", None))
        self.menuExport.setTitle(QCoreApplication.translate("MainWindow", u"Export Data", None))
        self.menuApplication_List.setTitle(QCoreApplication.translate("MainWindow", u"Application List", None))
    # retranslateUi

