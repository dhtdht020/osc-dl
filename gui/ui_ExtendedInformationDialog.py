# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ExtendedInformationDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFrame, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QSizePolicy, QTabWidget, QTextBrowser,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(406, 350)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.Application_groupBox = QGroupBox(Dialog)
        self.Application_groupBox.setObjectName(u"Application_groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Application_groupBox.sizePolicy().hasHeightForWidth())
        self.Application_groupBox.setSizePolicy(sizePolicy)
        self.horizontalLayout_2 = QHBoxLayout(self.Application_groupBox)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.frame_2 = QFrame(self.Application_groupBox)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, -1)
        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.CategoryIcon_Label = QLabel(self.frame_4)
        self.CategoryIcon_Label.setObjectName(u"CategoryIcon_Label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.CategoryIcon_Label.sizePolicy().hasHeightForWidth())
        self.CategoryIcon_Label.setSizePolicy(sizePolicy1)
        self.CategoryIcon_Label.setMinimumSize(QSize(30, 30))
        self.CategoryIcon_Label.setMaximumSize(QSize(30, 30))

        self.horizontalLayout_4.addWidget(self.CategoryIcon_Label)

        self.AppDisplayName_Label = QLabel(self.frame_4)
        self.AppDisplayName_Label.setObjectName(u"AppDisplayName_Label")
        font = QFont()
        font.setBold(True)
        self.AppDisplayName_Label.setFont(font)
        self.AppDisplayName_Label.setWordWrap(True)
        self.AppDisplayName_Label.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.horizontalLayout_4.addWidget(self.AppDisplayName_Label)


        self.verticalLayout_2.addWidget(self.frame_4)

        self.AppDescription_Label = QLabel(self.frame_2)
        self.AppDescription_Label.setObjectName(u"AppDescription_Label")
        self.AppDescription_Label.setMaximumSize(QSize(221, 16777215))
        self.AppDescription_Label.setWordWrap(True)
        self.AppDescription_Label.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_2.addWidget(self.AppDescription_Label)


        self.horizontalLayout_2.addWidget(self.frame_2)


        self.verticalLayout.addWidget(self.Application_groupBox)

        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.Information_tabWidget = QTabWidget(self.frame)
        self.Information_tabWidget.setObjectName(u"Information_tabWidget")
        self.assets_tab = QWidget()
        self.assets_tab.setObjectName(u"assets_tab")
        self.verticalLayout_5 = QVBoxLayout(self.assets_tab)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.assets_treeWidget = QTreeWidget(self.assets_tab)
        self.assets_treeWidget.setObjectName(u"assets_treeWidget")
        self.assets_treeWidget.setAutoExpandDelay(1)
        self.assets_treeWidget.setIndentation(2)
        self.assets_treeWidget.setRootIsDecorated(False)
        self.assets_treeWidget.setWordWrap(True)
        self.assets_treeWidget.setColumnCount(3)

        self.verticalLayout_5.addWidget(self.assets_treeWidget)

        self.Information_tabWidget.addTab(self.assets_tab, "")
        self.shop_tab = QWidget()
        self.shop_tab.setObjectName(u"shop_tab")
        self.verticalLayout_3 = QVBoxLayout(self.shop_tab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.shop_treeWidget = QTreeWidget(self.shop_tab)
        self.shop_treeWidget.setObjectName(u"shop_treeWidget")
        self.shop_treeWidget.setIndentation(0)
        self.shop_treeWidget.setColumnCount(2)

        self.verticalLayout_3.addWidget(self.shop_treeWidget)

        self.Information_tabWidget.addTab(self.shop_tab, "")
        self.raw_tab = QWidget()
        self.raw_tab.setObjectName(u"raw_tab")
        self.verticalLayout_4 = QVBoxLayout(self.raw_tab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.raw_textBrowser = QTextBrowser(self.raw_tab)
        self.raw_textBrowser.setObjectName(u"raw_textBrowser")

        self.verticalLayout_4.addWidget(self.raw_textBrowser)

        self.Information_tabWidget.addTab(self.raw_tab, "")

        self.horizontalLayout.addWidget(self.Information_tabWidget)


        self.verticalLayout.addWidget(self.frame)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        self.Information_tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.Application_groupBox.setTitle(QCoreApplication.translate("Dialog", u"Application", None))
        self.CategoryIcon_Label.setText("")
        self.AppDisplayName_Label.setText(QCoreApplication.translate("Dialog", u"Title", None))
        self.AppDescription_Label.setText(QCoreApplication.translate("Dialog", u"Short Description", None))
        ___qtreewidgetitem = self.assets_treeWidget.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Dialog", u"Value", None))
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Key", None))
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Asset", None))
        self.Information_tabWidget.setTabText(self.Information_tabWidget.indexOf(self.assets_tab), QCoreApplication.translate("Dialog", u"Assets", None))
        ___qtreewidgetitem1 = self.shop_treeWidget.headerItem()
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("Dialog", u"Value", None))
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("Dialog", u"Key", None))
        self.Information_tabWidget.setTabText(self.Information_tabWidget.indexOf(self.shop_tab), QCoreApplication.translate("Dialog", u"Shop", None))
        self.Information_tabWidget.setTabText(self.Information_tabWidget.indexOf(self.raw_tab), QCoreApplication.translate("Dialog", u"Raw", None))
    # retranslateUi

