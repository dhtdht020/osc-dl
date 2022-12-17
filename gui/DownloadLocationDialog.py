import logging

from PySide6 import QtCore
from PySide6.QtCore import QSize, QStorageInfo, QDir, QTimer, QFileInfo
from PySide6.QtGui import QIcon, QGuiApplication
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QListWidgetItem, QFileIconProvider

import gui_helpers
from gui import ui_DownloadLocationDialog
from utils import resource_path, file_size


class DownloadLocationDialog(ui_DownloadLocationDialog.Ui_Dialog, QDialog):
    def __init__(self, packages, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon(resource_path("assets/gui/icons/downloadlocationdialog.png")))
        self.comboBox.setIconSize(QSize(32, 32))
        self.buttonBox.button(QDialogButtonBox.Ok).setText("Download")
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.screen = QGuiApplication.primaryScreen()
        self.packages = packages
        self.selection = None
        self.drives = set()
        if len(self.packages) > 1:
            self.setWindowTitle(f"Download Multiple Files")
            self.buttonBox.button(QDialogButtonBox.Ok).setText("Download to directory")
        else:
            self.setWindowTitle(f"Download \"{self.packages[0]['display_name']}\"")

        # set required space label
        total_file_size = 0
        for package in self.packages:
            total_file_size+=package['extracted']
        
        self.label_required_space.setText(f"**{'Total ' if len(self.packages) > 1 else ''}Required Space:** {file_size(total_file_size)}")

        # populate list of extra dirs
        for package in self.packages:
            for directory in package["extra_directories"]:
                if not directory.startswith("/apps"):
                    item = QListWidgetItem()
                    item.setText(directory)
                    item.setIcon(QIcon(resource_path("assets/gui/icons/directory.png")))
                    self.listWidget.addItem(item)

        # initialize volumes, set timer for checking for changes to volumes once per second
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_for_volume_changes)
        self.timer.start(1000)

        # perform first volume scan
        self.check_for_volume_changes()
        self.update_volume_list()
        self.combobox_index_changed()

        self.comboBox.currentIndexChanged.connect(self.combobox_index_changed)

    # check if a volume is changed/added/removed
    def check_for_volume_changes(self):
        current_volumes = QStorageInfo.mountedVolumes()

        # remove devices that aren't ready
        for volume in current_volumes:
            if not volume.isReady():
                current_volumes.remove(volume)

        if current_volumes != self.drives:
            logging.debug("Scanned mounted volumes, as a change to mounted volumes was detected, or the dialog was initialized.")
            # update drives list once everything is ready
            self.drives = current_volumes
            self.update_volume_list()

    def update_volume_list(self):
        # temporarly disconnect combobox signals
        self.comboBox.blockSignals(True)

        # clear all locations
        self.comboBox.clear()

        # create browse location
        self.comboBox.addItem("Manual Save\n"
                              "Save this app as a ZIP to a custom path using the system dialog.")
        self.comboBox.setItemIcon(0, QIcon(resource_path("assets/gui/icons/browse.png")))
        self.comboBox.setItemData(0, "browse")

        # add volumes to locations list
        i = 1  # start at 1 because first item is select path
        for drive in self.drives:
            if not drive.isRoot():
                apps_exists = QDir(drive.rootPath() + "/apps").exists()
                if apps_exists:
                    self.comboBox.addItem(f"{drive.displayName()}\nRecommended! Found apps directory! Automatically installs app.")
                    self.comboBox.setItemIcon(i, QIcon(resource_path("assets/gui/icons/sdcard.png")))
                else:
                    self.comboBox.addItem(f"{drive.displayName()}\nUnknown. An apps folder will be created. Automatically installs app.")
                    self.comboBox.setItemIcon(i, QFileIconProvider().icon(QFileInfo(drive.rootPath())))

                # set drive data
                self.comboBox.setItemData(i, {"drive": drive, "appsdir": apps_exists})
                i += 1

        if gui_helpers.settings.value("download/device"):
            for i in range(self.comboBox.count()):
                if self.comboBox.itemData(i) == "browse":
                    if gui_helpers.settings.value("download/device") == "browse":
                        self.comboBox.setCurrentIndex(i)
                    else:
                        continue
                elif gui_helpers.settings.value("download/device") == self.comboBox.itemData(i)["drive"].device():
                    self.comboBox.setCurrentIndex(i)

        self.comboBox.blockSignals(False)
        self.combobox_index_changed()

    def combobox_index_changed(self):
        if self.comboBox.currentData() == "browse":
            self.listWidget.hide()
            self.label_2.hide()
            self.checkBox.setChecked(False)
            self.label_available_space.setVisible(False)
        else:
            # set available space label
            self.label_available_space.setVisible(True)
            self.label_available_space.setText(
                f"**Available Space:** {file_size(self.comboBox.currentData()['drive'].bytesFree())}")
            if gui_helpers.settings.value("download/device") == self.comboBox.currentData()["drive"].device():
                self.checkBox.setChecked(True)
            else:
                self.checkBox.setChecked(False)
            if self.listWidget.count() > 0:
                self.listWidget.show()
                self.label_2.show()
            else:
                self.listWidget.hide()
                self.label_2.hide()
        QtCore.QTimer.singleShot(0, self.adjust_size)

    def adjust_size(self):
        self.resize(QSize(400, self.sizeHint().height()))

    def accept(self):
        self.selection = self.comboBox.currentData()
        # save selection if checkbox is checked
        if self.checkBox.isChecked():
            if self.selection == "browse":
                device = "browse"
            else:
                device = self.selection["drive"].device()

            # save device id
            gui_helpers.settings.setValue("download/device", device)
            gui_helpers.settings.sync()
            logging.debug(f"Saved {device} to setting `download/device`")
        super().accept()
