# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'collection.ui'
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
        MainWindow.resize(764, 458)
        self.actionNew_Collection = QAction(MainWindow)
        self.actionNew_Collection.setObjectName(u"actionNew_Collection")
        self.actionLoad_Collection = QAction(MainWindow)
        self.actionLoad_Collection.setObjectName(u"actionLoad_Collection")
        self.actionSave_Collection = QAction(MainWindow)
        self.actionSave_Collection.setObjectName(u"actionSave_Collection")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.mdiArea = QMdiArea(self.centralwidget)
        self.mdiArea.setObjectName(u"mdiArea")

        self.verticalLayout.addWidget(self.mdiArea)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 764, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.SaveLoadToolBar = QToolBar(MainWindow)
        self.SaveLoadToolBar.setObjectName(u"SaveLoadToolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.SaveLoadToolBar)
        self.ControlsDock = QDockWidget(MainWindow)
        self.ControlsDock.setObjectName(u"ControlsDock")
        self.ControlsDock.setMinimumSize(QSize(200, 185))
        self.ControlsDock.setFeatures(QDockWidget.DockWidgetFloatable|QDockWidget.DockWidgetMovable)
        self.ControlsDock.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
        self.DockContents = QWidget()
        self.DockContents.setObjectName(u"DockContents")
        self.verticalLayout_2 = QVBoxLayout(self.DockContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.DockscrollArea = QScrollArea(self.DockContents)
        self.DockscrollArea.setObjectName(u"DockscrollArea")
        self.DockscrollArea.setFrameShape(QFrame.NoFrame)
        self.DockscrollArea.setFrameShadow(QFrame.Plain)
        self.DockscrollArea.setLineWidth(0)
        self.DockscrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 200, 372))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.CollectionContentsGroup = QGroupBox(self.scrollAreaWidgetContents)
        self.CollectionContentsGroup.setObjectName(u"CollectionContentsGroup")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CollectionContentsGroup.sizePolicy().hasHeightForWidth())
        self.CollectionContentsGroup.setSizePolicy(sizePolicy)
        self.verticalLayout_5 = QVBoxLayout(self.CollectionContentsGroup)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.AddAppControl = QPushButton(self.CollectionContentsGroup)
        self.AddAppControl.setObjectName(u"AddAppControl")
        self.AddAppControl.setMinimumSize(QSize(0, 31))
        self.AddAppControl.setMaximumSize(QSize(16777215, 31))

        self.verticalLayout_5.addWidget(self.AddAppControl)


        self.verticalLayout_3.addWidget(self.CollectionContentsGroup)

        self.CollectionMetaGroup = QGroupBox(self.scrollAreaWidgetContents)
        self.CollectionMetaGroup.setObjectName(u"CollectionMetaGroup")
        sizePolicy.setHeightForWidth(self.CollectionMetaGroup.sizePolicy().hasHeightForWidth())
        self.CollectionMetaGroup.setSizePolicy(sizePolicy)
        self.verticalLayout_6 = QVBoxLayout(self.CollectionMetaGroup)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.ConfigureCollectionMetaControl = QPushButton(self.CollectionMetaGroup)
        self.ConfigureCollectionMetaControl.setObjectName(u"ConfigureCollectionMetaControl")
        self.ConfigureCollectionMetaControl.setMinimumSize(QSize(0, 31))
        self.ConfigureCollectionMetaControl.setMaximumSize(QSize(16777215, 31))

        self.verticalLayout_6.addWidget(self.ConfigureCollectionMetaControl)


        self.verticalLayout_3.addWidget(self.CollectionMetaGroup)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.DockscrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_2.addWidget(self.DockscrollArea)

        self.ControlsDock.setWidget(self.DockContents)
        MainWindow.addDockWidget(Qt.LeftDockWidgetArea, self.ControlsDock)

        self.menubar.addAction(self.menuFile.menuAction())
        self.SaveLoadToolBar.addAction(self.actionNew_Collection)
        self.SaveLoadToolBar.addAction(self.actionLoad_Collection)
        self.SaveLoadToolBar.addAction(self.actionSave_Collection)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionNew_Collection.setText(QCoreApplication.translate("MainWindow", u"New", None))
#if QT_CONFIG(tooltip)
        self.actionNew_Collection.setToolTip(QCoreApplication.translate("MainWindow", u"Create New Collection", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionNew_Collection.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.actionLoad_Collection.setText(QCoreApplication.translate("MainWindow", u"Load", None))
#if QT_CONFIG(tooltip)
        self.actionLoad_Collection.setToolTip(QCoreApplication.translate("MainWindow", u"Load existing collection", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionLoad_Collection.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave_Collection.setText(QCoreApplication.translate("MainWindow", u"Save", None))
#if QT_CONFIG(shortcut)
        self.actionSave_Collection.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.SaveLoadToolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
        self.ControlsDock.setWindowTitle(QCoreApplication.translate("MainWindow", u"Collection Manager", None))
        self.CollectionContentsGroup.setTitle(QCoreApplication.translate("MainWindow", u"Collection Contents", None))
        self.AddAppControl.setText(QCoreApplication.translate("MainWindow", u"Add New Application", None))
        self.CollectionMetaGroup.setTitle(QCoreApplication.translate("MainWindow", u"Collection Extras", None))
        self.ConfigureCollectionMetaControl.setText(QCoreApplication.translate("MainWindow", u"Configure Collection Metadata", None))
    # retranslateUi

