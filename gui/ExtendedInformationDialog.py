import json

from PySide6 import QtCore
from PySide6.QtGui import QIcon, QGuiApplication, QPixmap
from PySide6.QtWidgets import QDialog, QTreeWidgetItem, QMenu
from gui import ui_ExtendedInformationDialog
from utils import resource_path


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

        self.setWindowIcon(QIcon(resource_path("assets/gui/icons/icons8-about-16.png")))
        self.setWindowTitle(f"\"{self.app['name']}\" - Extended Information")

        self.populate_information()

        self.assets_treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.assets_treeWidget.customContextMenuRequested.connect(self.assets_tree_context_menu)
        self.shop_treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.shop_treeWidget.customContextMenuRequested.connect(self.shop_tree_context_menu)

    def populate_information(self):
        # Application
        self.AppDisplayName_Label.setText(self.app["name"])
        self.AppDescription_Label.setText(self.app["description"]["short"])

        category = self.app["category"]
        if category == "utilities":
            self.CategoryIcon_Label.setPixmap(QPixmap(resource_path("assets/gui/icons/category/utility-30.png")))
        elif category == "games":
            self.CategoryIcon_Label.setPixmap(QPixmap(resource_path("assets/gui/icons/category/game-30.png")))
        elif category == "emulators":
            self.CategoryIcon_Label.setPixmap(QPixmap(resource_path("assets/gui/icons/category/emulator-30.png")))
        elif category == "media":
            self.CategoryIcon_Label.setPixmap(QPixmap(resource_path("assets/gui/icons/category/media-30.png")))
        elif category == "demos":
            self.CategoryIcon_Label.setPixmap(QPixmap(resource_path("assets/gui/icons/category/demo-30.png")))
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

    def assets_tree_context_menu(self, pos):
        item = self.assets_treeWidget.itemAt(pos)
        if not item:
            return
        value = item.text(2)
        if not value:
            return

        menu = QMenu(self.assets_treeWidget)
        copy_action = menu.addAction("Copy Value")
        copy_action.triggered.connect(lambda: QGuiApplication.clipboard().setText(value))
        menu.exec(self.assets_treeWidget.viewport().mapToGlobal(pos))

    def shop_tree_context_menu(self, pos):
        item = self.shop_treeWidget.itemAt(pos)
        if not item:
            return
        value = item.text(1)
        if not value:
            return

        menu = QMenu(self.shop_treeWidget)
        copy_action = menu.addAction("Copy Value")
        copy_action.triggered.connect(lambda: QGuiApplication.clipboard().setText(value))
        menu.exec(self.shop_treeWidget.viewport().mapToGlobal(pos))
