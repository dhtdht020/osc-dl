# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'united.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QListView, QListWidget, QListWidgetItem,
    QMainWindow, QMenu, QMenuBar, QProgressBar,
    QPushButton, QSizePolicy, QStatusBar, QTabWidget,
    QTextBrowser, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(900, 460)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(900, 460))
        MainWindow.setStyleSheet(u"")
        MainWindow.setDockOptions(QMainWindow.DockOption.AllowTabbedDocks|QMainWindow.DockOption.AnimatedDocks)
        self.About_Action = QAction(MainWindow)
        self.About_Action.setObjectName(u"About_Action")
        self.CheckForUpdates_Action = QAction(MainWindow)
        self.CheckForUpdates_Action.setObjectName(u"CheckForUpdates_Action")
        self.Refresh_Action = QAction(MainWindow)
        self.Refresh_Action.setObjectName(u"Refresh_Action")
        self.IconsByIcons8_Action = QAction(MainWindow)
        self.IconsByIcons8_Action.setObjectName(u"IconsByIcons8_Action")
        self.IconsByIcons8_Action.setEnabled(False)
        self.CopyDirectLink_Action = QAction(MainWindow)
        self.CopyDirectLink_Action.setObjectName(u"CopyDirectLink_Action")
        self.FilterByDeveloper_Action = QAction(MainWindow)
        self.FilterByDeveloper_Action.setObjectName(u"FilterByDeveloper_Action")
        self.Central_Widget = QWidget(MainWindow)
        self.Central_Widget.setObjectName(u"Central_Widget")
        self.horizontalLayout_2 = QHBoxLayout(self.Central_Widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.AppsLibrary_GroupBox = QGroupBox(self.Central_Widget)
        self.AppsLibrary_GroupBox.setObjectName(u"AppsLibrary_GroupBox")
        self.verticalLayout = QVBoxLayout(self.AppsLibrary_GroupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 4, -1, -1)
        self.LibraryInfo_Frame = QFrame(self.AppsLibrary_GroupBox)
        self.LibraryInfo_Frame.setObjectName(u"LibraryInfo_Frame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.LibraryInfo_Frame.sizePolicy().hasHeightForWidth())
        self.LibraryInfo_Frame.setSizePolicy(sizePolicy1)
        self.LibraryInfo_Frame.setFrameShape(QFrame.Shape.NoFrame)
        self.LibraryInfo_Frame.setLineWidth(0)
        self.horizontalLayout_3 = QHBoxLayout(self.LibraryInfo_Frame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.Repositories_ComboBox = QComboBox(self.LibraryInfo_Frame)
        self.Repositories_ComboBox.setObjectName(u"Repositories_ComboBox")
        self.Repositories_ComboBox.setEnabled(True)

        self.horizontalLayout_3.addWidget(self.Repositories_ComboBox)

        self.AppsCount_Label = QLabel(self.LibraryInfo_Frame)
        self.AppsCount_Label.setObjectName(u"AppsCount_Label")
        self.AppsCount_Label.setMaximumSize(QSize(60, 16777215))
        self.AppsCount_Label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.AppsCount_Label)


        self.verticalLayout.addWidget(self.LibraryInfo_Frame)

        self.LibraryContents_Frame = QFrame(self.AppsLibrary_GroupBox)
        self.LibraryContents_Frame.setObjectName(u"LibraryContents_Frame")
        self.verticalLayout_2 = QVBoxLayout(self.LibraryContents_Frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.Search_Frame = QFrame(self.LibraryContents_Frame)
        self.Search_Frame.setObjectName(u"Search_Frame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.Search_Frame.sizePolicy().hasHeightForWidth())
        self.Search_Frame.setSizePolicy(sizePolicy2)
        self.Search_Frame.setMaximumSize(QSize(16777215, 20))
        self.Search_Frame.setFrameShape(QFrame.Shape.NoFrame)
        self.Search_Frame.setFrameShadow(QFrame.Shadow.Plain)
        self.Search_Frame.setLineWidth(0)
        self.horizontalLayout_5 = QHBoxLayout(self.Search_Frame)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.SearchBar_LineEdit = QLineEdit(self.Search_Frame)
        self.SearchBar_LineEdit.setObjectName(u"SearchBar_LineEdit")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.SearchBar_LineEdit.sizePolicy().hasHeightForWidth())
        self.SearchBar_LineEdit.setSizePolicy(sizePolicy3)

        self.horizontalLayout_5.addWidget(self.SearchBar_LineEdit)

        self.Categories_ComboBox = QComboBox(self.Search_Frame)
        self.Categories_ComboBox.addItem("")
        self.Categories_ComboBox.addItem("")
        self.Categories_ComboBox.addItem("")
        self.Categories_ComboBox.addItem("")
        self.Categories_ComboBox.addItem("")
        self.Categories_ComboBox.addItem("")
        self.Categories_ComboBox.setObjectName(u"Categories_ComboBox")
        self.Categories_ComboBox.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_5.addWidget(self.Categories_ComboBox)

        self.ResetFilters_PushButton = QPushButton(self.Search_Frame)
        self.ResetFilters_PushButton.setObjectName(u"ResetFilters_PushButton")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.ResetFilters_PushButton.sizePolicy().hasHeightForWidth())
        self.ResetFilters_PushButton.setSizePolicy(sizePolicy4)

        self.horizontalLayout_5.addWidget(self.ResetFilters_PushButton)


        self.verticalLayout_2.addWidget(self.Search_Frame)

        self.AppsList_Widget = QListWidget(self.LibraryContents_Frame)
        self.AppsList_Widget.setObjectName(u"AppsList_Widget")
        sizePolicy3.setHeightForWidth(self.AppsList_Widget.sizePolicy().hasHeightForWidth())
        self.AppsList_Widget.setSizePolicy(sizePolicy3)
        self.AppsList_Widget.setBaseSize(QSize(581, 281))
        self.AppsList_Widget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.verticalLayout_2.addWidget(self.AppsList_Widget)


        self.verticalLayout.addWidget(self.LibraryContents_Frame)


        self.horizontalLayout_2.addWidget(self.AppsLibrary_GroupBox)

        self.SelectionInfo_GroupBox = QGroupBox(self.Central_Widget)
        self.SelectionInfo_GroupBox.setObjectName(u"SelectionInfo_GroupBox")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.SelectionInfo_GroupBox.sizePolicy().hasHeightForWidth())
        self.SelectionInfo_GroupBox.setSizePolicy(sizePolicy5)
        self.SelectionInfo_GroupBox.setMaximumSize(QSize(271, 16777215))
        self.verticalLayout_3 = QVBoxLayout(self.SelectionInfo_GroupBox)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 4, 0, -1)
        self.AppInformationTabs_Frame = QFrame(self.SelectionInfo_GroupBox)
        self.AppInformationTabs_Frame.setObjectName(u"AppInformationTabs_Frame")
        self.AppInformationTabs_Frame.setFrameShape(QFrame.Shape.NoFrame)
        self.AppInformationTabs_Frame.setLineWidth(0)
        self.AppInformationTabs_TabWidget = QTabWidget(self.AppInformationTabs_Frame)
        self.AppInformationTabs_TabWidget.setObjectName(u"AppInformationTabs_TabWidget")
        self.AppInformationTabs_TabWidget.setGeometry(QRect(10, 0, 251, 271))
        self.InfoTab_Widget = QWidget()
        self.InfoTab_Widget.setObjectName(u"InfoTab_Widget")
        self.AppDescription_Label = QLabel(self.InfoTab_Widget)
        self.AppDescription_Label.setObjectName(u"AppDescription_Label")
        self.AppDescription_Label.setGeometry(QRect(10, 80, 221, 16))
        self.AppDescription_Label.setMaximumSize(QSize(221, 16777215))
        self.AppDescription_Label.setWordWrap(True)
        self.AppDescription_Label.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByMouse)
        self.AppDisplayName_Label = QLabel(self.InfoTab_Widget)
        self.AppDisplayName_Label.setObjectName(u"AppDisplayName_Label")
        self.AppDisplayName_Label.setGeometry(QRect(10, 60, 221, 16))
        self.AppDisplayName_Label.setMaximumSize(QSize(221, 16777215))
        font = QFont()
        font.setBold(True)
        self.AppDisplayName_Label.setFont(font)
        self.AppDisplayName_Label.setWordWrap(True)
        self.AppDisplayName_Label.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByMouse)
        self.ProgressBar = QProgressBar(self.InfoTab_Widget)
        self.ProgressBar.setObjectName(u"ProgressBar")
        self.ProgressBar.setGeometry(QRect(150, 0, 91, 23))
        self.ProgressBar.setVisible(False)
        self.ProgressBar.setValue(0)
        self.AppIcon_Label = QLabel(self.InfoTab_Widget)
        self.AppIcon_Label.setObjectName(u"AppIcon_Label")
        self.AppIcon_Label.setGeometry(QRect(10, 10, 128, 48))
        self.AppIcon_Label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.AppCategory_Label = QLabel(self.InfoTab_Widget)
        self.AppCategory_Label.setObjectName(u"AppCategory_Label")
        self.AppCategory_Label.setGeometry(QRect(147, 10, 81, 48))
        font1 = QFont()
        font1.setPointSize(11)
        font1.setBold(True)
        self.AppCategory_Label.setFont(font1)
        self.AppCategory_Label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.StatusIcon = QLabel(self.InfoTab_Widget)
        self.StatusIcon.setObjectName(u"StatusIcon")
        self.StatusIcon.setGeometry(QRect(120, 0, 16, 16))
        self.StatusIcon.setMaximumSize(QSize(30, 30))
        self.StatusIcon.setScaledContents(True)
        self.StatusIcon.setMargin(3)
        self.gridLayoutWidget = QWidget(self.InfoTab_Widget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 100, 223, 136))
        self.AppMetadata_GridLayout = QGridLayout(self.gridLayoutWidget)
        self.AppMetadata_GridLayout.setObjectName(u"AppMetadata_GridLayout")
        self.AppMetadata_GridLayout.setContentsMargins(0, 0, 0, 0)
        self.AppReleaseDate_Label = QLabel(self.gridLayoutWidget)
        self.AppReleaseDate_Label.setObjectName(u"AppReleaseDate_Label")

        self.AppMetadata_GridLayout.addWidget(self.AppReleaseDate_Label, 3, 0, 1, 1)

        self.AppFileSize_Label = QLabel(self.gridLayoutWidget)
        self.AppFileSize_Label.setObjectName(u"AppFileSize_Label")

        self.AppMetadata_GridLayout.addWidget(self.AppFileSize_Label, 4, 0, 1, 1)

        self.AppVersion_Label = QLabel(self.gridLayoutWidget)
        self.AppVersion_Label.setObjectName(u"AppVersion_Label")

        self.AppMetadata_GridLayout.addWidget(self.AppVersion_Label, 1, 0, 1, 1)

        self.AppDeveloper_Label = QLabel(self.gridLayoutWidget)
        self.AppDeveloper_Label.setObjectName(u"AppDeveloper_Label")

        self.AppMetadata_GridLayout.addWidget(self.AppDeveloper_Label, 2, 0, 1, 1)

        self.AppName_Label = QLabel(self.gridLayoutWidget)
        self.AppName_Label.setObjectName(u"AppName_Label")

        self.AppMetadata_GridLayout.addWidget(self.AppName_Label, 0, 0, 1, 1)

        self.AppName_LineEdit = QLineEdit(self.gridLayoutWidget)
        self.AppName_LineEdit.setObjectName(u"AppName_LineEdit")
        self.AppName_LineEdit.setEchoMode(QLineEdit.EchoMode.Normal)
        self.AppName_LineEdit.setReadOnly(True)

        self.AppMetadata_GridLayout.addWidget(self.AppName_LineEdit, 0, 1, 1, 1)

        self.AppVersion_LineEdit = QLineEdit(self.gridLayoutWidget)
        self.AppVersion_LineEdit.setObjectName(u"AppVersion_LineEdit")
        self.AppVersion_LineEdit.setEchoMode(QLineEdit.EchoMode.Normal)
        self.AppVersion_LineEdit.setReadOnly(True)

        self.AppMetadata_GridLayout.addWidget(self.AppVersion_LineEdit, 1, 1, 1, 1)

        self.AppDeveloper_LineEdit = QLineEdit(self.gridLayoutWidget)
        self.AppDeveloper_LineEdit.setObjectName(u"AppDeveloper_LineEdit")
        self.AppDeveloper_LineEdit.setEchoMode(QLineEdit.EchoMode.Normal)
        self.AppDeveloper_LineEdit.setReadOnly(True)

        self.AppMetadata_GridLayout.addWidget(self.AppDeveloper_LineEdit, 2, 1, 1, 1)

        self.AppReleaseDate_LineEdit = QLineEdit(self.gridLayoutWidget)
        self.AppReleaseDate_LineEdit.setObjectName(u"AppReleaseDate_LineEdit")
        self.AppReleaseDate_LineEdit.setEchoMode(QLineEdit.EchoMode.Normal)
        self.AppReleaseDate_LineEdit.setReadOnly(True)

        self.AppMetadata_GridLayout.addWidget(self.AppReleaseDate_LineEdit, 3, 1, 1, 1)

        self.AppFileSize_LineEdit = QLineEdit(self.gridLayoutWidget)
        self.AppFileSize_LineEdit.setObjectName(u"AppFileSize_LineEdit")
        self.AppFileSize_LineEdit.setEchoMode(QLineEdit.EchoMode.Normal)
        self.AppFileSize_LineEdit.setReadOnly(True)

        self.AppMetadata_GridLayout.addWidget(self.AppFileSize_LineEdit, 4, 1, 1, 1)

        self.AppInformationTabs_TabWidget.addTab(self.InfoTab_Widget, "")
        self.StatusIcon.raise_()
        self.AppDescription_Label.raise_()
        self.AppDisplayName_Label.raise_()
        self.ProgressBar.raise_()
        self.AppIcon_Label.raise_()
        self.AppCategory_Label.raise_()
        self.gridLayoutWidget.raise_()
        self.DescriptionTab_Widget = QWidget()
        self.DescriptionTab_Widget.setObjectName(u"DescriptionTab_Widget")
        self.LongDescription_TextBrowser = QTextBrowser(self.DescriptionTab_Widget)
        self.LongDescription_TextBrowser.setObjectName(u"LongDescription_TextBrowser")
        self.LongDescription_TextBrowser.setGeometry(QRect(-1, -1, 247, 244))
        self.LongDescription_TextBrowser.setStyleSheet(u"QTextBrowser {\n"
"	border-style: hidden;\n"
"}")
        self.LongDescription_TextBrowser.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.AppInformationTabs_TabWidget.addTab(self.DescriptionTab_Widget, "")
        self.CompatibilityTab_Widget = QWidget()
        self.CompatibilityTab_Widget.setObjectName(u"CompatibilityTab_Widget")
        self.Compatibility_ListWidget = QListWidget(self.CompatibilityTab_Widget)
        self.Compatibility_ListWidget.setObjectName(u"Compatibility_ListWidget")
        self.Compatibility_ListWidget.setGeometry(QRect(0, 0, 245, 244))
        self.Compatibility_ListWidget.setStyleSheet(u"QListWidget {\n"
"	border: unset;\n"
"}")
        self.Compatibility_ListWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.Compatibility_ListWidget.setDragDropMode(QAbstractItemView.DragDropMode.NoDragDrop)
        self.Compatibility_ListWidget.setIconSize(QSize(30, 30))
        self.Compatibility_ListWidget.setMovement(QListView.Movement.Static)
        self.Compatibility_ListWidget.setViewMode(QListView.ViewMode.ListMode)
        self.Compatibility_ListWidget.setWordWrap(True)
        self.AppInformationTabs_TabWidget.addTab(self.CompatibilityTab_Widget, "")

        self.verticalLayout_3.addWidget(self.AppInformationTabs_Frame)

        self.NandWarning_Frame = QFrame(self.SelectionInfo_GroupBox)
        self.NandWarning_Frame.setObjectName(u"NandWarning_Frame")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.NandWarning_Frame.sizePolicy().hasHeightForWidth())
        self.NandWarning_Frame.setSizePolicy(sizePolicy6)
        self.NandWarning_Frame.setStyleSheet(u"")
        self.NandWarning_Frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.NandWarning_Frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.NandWarning_Frame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.NandWarningBanner_Frame = QFrame(self.NandWarning_Frame)
        self.NandWarningBanner_Frame.setObjectName(u"NandWarningBanner_Frame")
        self.NandWarningBanner_Frame.setStyleSheet(u"background-color: rgb(255, 102, 102);\n"
"color: rgb(255, 255, 255);")
        self.NandWarningBanner_Frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.NandWarningBanner_Frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.NandWarningBanner_Frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.NandWarningIcon_Label = QLabel(self.NandWarningBanner_Frame)
        self.NandWarningIcon_Label.setObjectName(u"NandWarningIcon_Label")
        self.NandWarningIcon_Label.setMinimumSize(QSize(32, 32))
        self.NandWarningIcon_Label.setMaximumSize(QSize(32, 32))

        self.horizontalLayout.addWidget(self.NandWarningIcon_Label)

        self.NandWarningText_Label = QLabel(self.NandWarningBanner_Frame)
        self.NandWarningText_Label.setObjectName(u"NandWarningText_Label")
        self.NandWarningText_Label.setWordWrap(True)

        self.horizontalLayout.addWidget(self.NandWarningText_Label)


        self.verticalLayout_4.addWidget(self.NandWarningBanner_Frame)


        self.verticalLayout_3.addWidget(self.NandWarning_Frame)

        self.DownloadButtons_Frame = QFrame(self.SelectionInfo_GroupBox)
        self.DownloadButtons_Frame.setObjectName(u"DownloadButtons_Frame")
        self.DownloadButtons_Frame.setMaximumSize(QSize(16777215, 34))
        self.DownloadButtons_Frame.setFrameShape(QFrame.Shape.NoFrame)
        self.DownloadButtons_Frame.setLineWidth(0)
        self.horizontalLayout_6 = QHBoxLayout(self.DownloadButtons_Frame)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(-1, 0, -1, 0)
        self.Download_PushButton = QPushButton(self.DownloadButtons_Frame)
        self.Download_PushButton.setObjectName(u"Download_PushButton")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.Download_PushButton.sizePolicy().hasHeightForWidth())
        self.Download_PushButton.setSizePolicy(sizePolicy7)

        self.horizontalLayout_6.addWidget(self.Download_PushButton)

        self.SendToWii_PushButton = QPushButton(self.DownloadButtons_Frame)
        self.SendToWii_PushButton.setObjectName(u"SendToWii_PushButton")
        sizePolicy7.setHeightForWidth(self.SendToWii_PushButton.sizePolicy().hasHeightForWidth())
        self.SendToWii_PushButton.setSizePolicy(sizePolicy7)

        self.horizontalLayout_6.addWidget(self.SendToWii_PushButton)


        self.verticalLayout_3.addWidget(self.DownloadButtons_Frame)

        self.DownloadButtons_Frame.raise_()
        self.AppInformationTabs_Frame.raise_()
        self.NandWarning_Frame.raise_()

        self.horizontalLayout_2.addWidget(self.SelectionInfo_GroupBox)

        MainWindow.setCentralWidget(self.Central_Widget)
        self.MenuBar = QMenuBar(MainWindow)
        self.MenuBar.setObjectName(u"MenuBar")
        self.MenuBar.setGeometry(QRect(0, 0, 900, 22))
        self.About_Menu = QMenu(self.MenuBar)
        self.About_Menu.setObjectName(u"About_Menu")
        self.Debug_Menu = QMenu(self.MenuBar)
        self.Debug_Menu.setObjectName(u"Debug_Menu")
        MainWindow.setMenuBar(self.MenuBar)
        self.StatusBar = QStatusBar(MainWindow)
        self.StatusBar.setObjectName(u"StatusBar")
        self.StatusBar.setSizeGripEnabled(False)
        MainWindow.setStatusBar(self.StatusBar)

        self.MenuBar.addAction(self.About_Menu.menuAction())
        self.MenuBar.addAction(self.Debug_Menu.menuAction())
        self.About_Menu.addAction(self.About_Action)
        self.About_Menu.addAction(self.IconsByIcons8_Action)
        self.Debug_Menu.addAction(self.Refresh_Action)
        self.Debug_Menu.addAction(self.CopyDirectLink_Action)
        self.Debug_Menu.addSeparator()
        self.Debug_Menu.addAction(self.CheckForUpdates_Action)

        self.retranslateUi(MainWindow)

        self.AppsList_Widget.setCurrentRow(-1)
        self.AppInformationTabs_TabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Open Shop Channel Downloader - Library", None))
        self.About_Action.setText(QCoreApplication.translate("MainWindow", u"About OSC-DL", None))
        self.CheckForUpdates_Action.setText(QCoreApplication.translate("MainWindow", u"Check for Updates", None))
        self.Refresh_Action.setText(QCoreApplication.translate("MainWindow", u"Refresh List", None))
#if QT_CONFIG(shortcut)
        self.Refresh_Action.setShortcut(QCoreApplication.translate("MainWindow", u"F5", None))
#endif // QT_CONFIG(shortcut)
        self.IconsByIcons8_Action.setText(QCoreApplication.translate("MainWindow", u"Icons provided by https://icons8.com", None))
        self.CopyDirectLink_Action.setText(QCoreApplication.translate("MainWindow", u"Copy Direct Link to App", None))
        self.FilterByDeveloper_Action.setText(QCoreApplication.translate("MainWindow", u"Filter by Developer", None))
#if QT_CONFIG(tooltip)
        self.FilterByDeveloper_Action.setToolTip(QCoreApplication.translate("MainWindow", u"Filter by Developer", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.Central_Widget.setAccessibleName(QCoreApplication.translate("MainWindow", u"centralcontainer", None))
#endif // QT_CONFIG(accessibility)
        self.AppsLibrary_GroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Apps Library", None))
        self.AppsCount_Label.setText(QCoreApplication.translate("MainWindow", u"0 Apps", None))
        self.SearchBar_LineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search Applications..", None))
        self.Categories_ComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"All Apps", None))
        self.Categories_ComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Utilities", None))
        self.Categories_ComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Emulators", None))
        self.Categories_ComboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"Games", None))
        self.Categories_ComboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"Media", None))
        self.Categories_ComboBox.setItemText(5, QCoreApplication.translate("MainWindow", u"Demos", None))

        self.ResetFilters_PushButton.setText(QCoreApplication.translate("MainWindow", u"Reset Filters", None))
        self.SelectionInfo_GroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Application Information", None))
#if QT_CONFIG(accessibility)
        self.InfoTab_Widget.setAccessibleName(QCoreApplication.translate("MainWindow", u"tabcontent", None))
#endif // QT_CONFIG(accessibility)
        self.AppDescription_Label.setText(QCoreApplication.translate("MainWindow", u"Description", None))
        self.AppDisplayName_Label.setText(QCoreApplication.translate("MainWindow", u"Title", None))
        self.AppIcon_Label.setText(QCoreApplication.translate("MainWindow", u"No homebrew icon. Aw.", None))
        self.AppCategory_Label.setText(QCoreApplication.translate("MainWindow", u"Category", None))
        self.StatusIcon.setText("")
        self.AppReleaseDate_Label.setText(QCoreApplication.translate("MainWindow", u"Release Date", None))
        self.AppFileSize_Label.setText(QCoreApplication.translate("MainWindow", u"File Size", None))
        self.AppVersion_Label.setText(QCoreApplication.translate("MainWindow", u"Version", None))
        self.AppDeveloper_Label.setText(QCoreApplication.translate("MainWindow", u"Developer", None))
        self.AppName_Label.setText(QCoreApplication.translate("MainWindow", u"App Name", None))
        self.AppName_LineEdit.setText("")
        self.AppName_LineEdit.setPlaceholderText("")
        self.AppInformationTabs_TabWidget.setTabText(self.AppInformationTabs_TabWidget.indexOf(self.InfoTab_Widget), QCoreApplication.translate("MainWindow", u"Info", None))
#if QT_CONFIG(accessibility)
        self.DescriptionTab_Widget.setAccessibleName(QCoreApplication.translate("MainWindow", u"tabcontent", None))
#endif // QT_CONFIG(accessibility)
        self.LongDescription_TextBrowser.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.AppInformationTabs_TabWidget.setTabText(self.AppInformationTabs_TabWidget.indexOf(self.DescriptionTab_Widget), QCoreApplication.translate("MainWindow", u"Description", None))
#if QT_CONFIG(accessibility)
        self.CompatibilityTab_Widget.setAccessibleName(QCoreApplication.translate("MainWindow", u"tabcontent", None))
#endif // QT_CONFIG(accessibility)
        self.AppInformationTabs_TabWidget.setTabText(self.AppInformationTabs_TabWidget.indexOf(self.CompatibilityTab_Widget), QCoreApplication.translate("MainWindow", u"Compatibility", None))
        self.NandWarningIcon_Label.setText("")
        self.NandWarningText_Label.setText(QCoreApplication.translate("MainWindow", u"This app makes changes to the system's NAND. Use with caution!", None))
        self.Download_PushButton.setText(QCoreApplication.translate("MainWindow", u"Download", None))
        self.SendToWii_PushButton.setText(QCoreApplication.translate("MainWindow", u"Send to Wii", None))
        self.About_Menu.setTitle(QCoreApplication.translate("MainWindow", u"About", None))
        self.Debug_Menu.setTitle(QCoreApplication.translate("MainWindow", u"Options", None))
    # retranslateUi

