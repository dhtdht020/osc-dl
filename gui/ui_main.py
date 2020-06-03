# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
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
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.SelectionOptionsBox = QGroupBox(self.centralwidget)
        self.SelectionOptionsBox.setObjectName(u"SelectionOptionsBox")
        self.SelectionOptionsBox.setGeometry(QRect(700, 10, 191, 61))
        self.verticalLayoutWidget = QWidget(self.SelectionOptionsBox)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 20, 171, 31))
        self.SelectionOptionsLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.SelectionOptionsLayout.setObjectName(u"SelectionOptionsLayout")
        self.SelectionOptionsLayout.setContentsMargins(0, 0, 0, 0)
        self.ViewMetadataBtn = QPushButton(self.verticalLayoutWidget)
        self.ViewMetadataBtn.setObjectName(u"ViewMetadataBtn")

        self.SelectionOptionsLayout.addWidget(self.ViewMetadataBtn)

        self.GeneralOptionsBox = QGroupBox(self.centralwidget)
        self.GeneralOptionsBox.setObjectName(u"GeneralOptionsBox")
        self.GeneralOptionsBox.setGeometry(QRect(700, 80, 191, 61))
        self.verticalLayoutWidget_3 = QWidget(self.GeneralOptionsBox)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(10, 20, 171, 31))
        self.GeneralOptionsLayout = QVBoxLayout(self.verticalLayoutWidget_3)
        self.GeneralOptionsLayout.setObjectName(u"GeneralOptionsLayout")
        self.GeneralOptionsLayout.setContentsMargins(0, 0, 0, 0)
        self.DownloadEverythingBtn = QPushButton(self.verticalLayoutWidget_3)
        self.DownloadEverythingBtn.setObjectName(u"DownloadEverythingBtn")

        self.GeneralOptionsLayout.addWidget(self.DownloadEverythingBtn)

        self.AppsLibraryBox = QGroupBox(self.centralwidget)
        self.AppsLibraryBox.setObjectName(u"AppsLibraryBox")
        self.AppsLibraryBox.setGeometry(QRect(10, 10, 681, 361))
        self.listAppsWidget = QListWidget(self.AppsLibraryBox)
        QListWidgetItem(self.listAppsWidget)
        QListWidgetItem(self.listAppsWidget)
        self.listAppsWidget.setObjectName(u"listAppsWidget")
        self.listAppsWidget.setGeometry(QRect(10, 20, 661, 331))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 900, 21))
        self.menuAbout = QMenu(self.menubar)
        self.menuAbout.setObjectName(u"menuAbout")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuAbout.menuAction())
        self.menuAbout.addAction(self.actionAbout_OSC_DL)

        self.retranslateUi(MainWindow)

        self.listAppsWidget.setCurrentRow(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Open Shop Channel Downloader - Library", None))
        self.actionAbout_OSC_DL.setText(QCoreApplication.translate("MainWindow", u"About OSC-DL", None))
        self.SelectionOptionsBox.setTitle(QCoreApplication.translate("MainWindow", u"Selection Options", None))
        self.ViewMetadataBtn.setText(QCoreApplication.translate("MainWindow", u"Download App", None))
        self.GeneralOptionsBox.setTitle(QCoreApplication.translate("MainWindow", u"General Options", None))
        self.DownloadEverythingBtn.setText(QCoreApplication.translate("MainWindow", u"Download Everything", None))
        self.AppsLibraryBox.setTitle(QCoreApplication.translate("MainWindow", u"Apps Library", None))

        __sortingEnabled = self.listAppsWidget.isSortingEnabled()
        self.listAppsWidget.setSortingEnabled(False)
        ___qlistwidgetitem = self.listAppsWidget.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("MainWindow", u"WiiVNC", None));
        ___qlistwidgetitem1 = self.listAppsWidget.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("MainWindow", u"wiixplorer", None));
        self.listAppsWidget.setSortingEnabled(__sortingEnabled)

        self.menuAbout.setTitle(QCoreApplication.translate("MainWindow", u"About", None))
    # retranslateUi

