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


class Ui_CollectionMainForm(object):
    def setupUi(self, CollectionMainForm):
        if not CollectionMainForm.objectName():
            CollectionMainForm.setObjectName(u"CollectionMainForm")
        CollectionMainForm.resize(400, 300)
        self.verticalLayout = QVBoxLayout(CollectionMainForm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.AppsCount = QLabel(CollectionMainForm)
        self.AppsCount.setObjectName(u"AppsCount")

        self.verticalLayout.addWidget(self.AppsCount)

        self.HostName = QLabel(CollectionMainForm)
        self.HostName.setObjectName(u"HostName")

        self.verticalLayout.addWidget(self.HostName)

        self.AppsList = QListWidget(CollectionMainForm)
        self.AppsList.setObjectName(u"AppsList")

        self.verticalLayout.addWidget(self.AppsList)


        self.retranslateUi(CollectionMainForm)

        QMetaObject.connectSlotsByName(CollectionMainForm)
    # setupUi

    def retranslateUi(self, CollectionMainForm):
        CollectionMainForm.setWindowTitle(QCoreApplication.translate("CollectionMainForm", u"Collection - New Unnamed Collection", None))
        self.AppsCount.setText(QCoreApplication.translate("CollectionMainForm", u"0 Apps", None))
        self.HostName.setText(QCoreApplication.translate("CollectionMainForm", u"Host: primary", None))
    # retranslateUi

