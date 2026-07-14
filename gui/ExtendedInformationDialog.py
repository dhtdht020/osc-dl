import json
import logging

from PySide6 import QtCore
from PySide6.QtCore import QSize, QStorageInfo, QDir, QTimer, QFileInfo
from PySide6.QtGui import QIcon, QGuiApplication, QPixmap
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QListWidgetItem, QFileIconProvider, QTreeWidgetItem
from gui import ui_ExtendedInformationDialog
from utils import resource_path, file_size


class ExtendedInformationDialog(ui_ExtendedInformationDialog.Ui_Dialog, QDialog):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon(resource_path("assets/gui/icons/downloadlocationdialog.png")))
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.screen = QGuiApplication.primaryScreen()
        self.app = app
        self.selection = None
        self.drives = set()

        self.setWindowTitle(f"\"{self.app['name']}\" - Extended Information")

        self.populate_information()

    def populate_information(self):
        # Application
        self.AppDisplayName_Label.setText(self.app["name"])
        self.AppDescription_Label.setText(self.app["description"]["short"])

        category = self.app["category"]
        if category == "utilities":
            self.CategoryIcon_Label.setPixmap(QPixmap(resource_path("assets/gui/icons/category/utility.png")))
        elif category == "games":
            self.CategoryIcon_Label.setPixmap(QPixmap(resource_path("assets/gui/icons/category/game.png")))
        elif category == "emulators":
            self.CategoryIcon_Label.setPixmap(QPixmap(resource_path("assets/gui/icons/category/emulator.png")))
        elif category == "media":
            self.CategoryIcon_Label.setPixmap(QPixmap(resource_path("assets/gui/icons/category/media.png")))
        elif category == "demos":
            self.CategoryIcon_Label.setPixmap(QPixmap(resource_path("assets/gui/icons/category/demo.png")))
        self.CategoryIcon_Label.setScaledContents(True)

        # Assets Tab
        for asset_name, asset_info in self.app["assets"].items():
            parent = QTreeWidgetItem(self.assets_treeWidget)
            parent.setText(0, asset_name)
            parent.setExpanded(True)

            for key, value in asset_info.items():
                item = QTreeWidgetItem(parent)
                item.setText(1, str(key))
                item.setText(2, str(value))

        self.assets_treeWidget.resizeColumnToContents(0)
        self.assets_treeWidget.resizeColumnToContents(1)

        # Shop Tab
        for key, value in self.app["shop"].items():
            item = QTreeWidgetItem(self.shop_treeWidget)
            item.setText(0, str(key))
            item.setText(1, str(value))

        # Raw Tab
        self.raw_textBrowser.setText(json.dumps(self.app, indent=2))
