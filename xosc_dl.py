import configparser
import io
import re
import threading
import time
import zipfile
from datetime import datetime
from os import listdir
from os.path import isfile, join

import os
import sys
import markdown
import serial
import serial.tools.list_ports

import logging
from functools import partial

import func_timeout
import requests
from PIL import Image
from PySide6 import QtGui, QtCore
from PySide6.QtCore import Qt, QObject, QSize, QEvent
from PySide6.QtGui import QIcon, QColor, QPixmap, QMovie, QDesktopServices, QHoverEvent
from PySide6.QtWidgets import QApplication, QMainWindow, QInputDialog, QLineEdit, QMessageBox, \
    QListWidgetItem, QFileDialog, QPushButton

import gui.ui_united
import api
from gui.wiiloadInstallerMSGDialog import wiiloadInstallerMSG
import gui_helpers
import metadata
import updater
import utils
import wiiload
from gui.DownloadLocationDialog import DownloadLocationDialog
from gui.SendDialog import WiiLoadDialog
from utils import resource_path


class MainWindow(gui.ui_united.Ui_MainWindow, QMainWindow):
    IconSignal = QtCore.Signal(QPixmap)
    LongDescriptionSignal = QtCore.Signal(str)
    AnnouncementBannerHidden = QtCore.Signal(bool)

    def __init__(self, app=None, splash=None, test_mode=False):
        super(MainWindow, self).__init__()
        self.repos = None
        self.apps = None
        self.current_repo = None
        self.ui = gui.ui_united.Ui_MainWindow()
        self.ui.setupUi(self)

        self.message = QMessageBox(self)
        self.message.setIcon(QMessageBox.Warning)
        self.message.setWindowTitle("Operation in progress")
        self.message.setText("Please wait for the operation to finish.")
        self.message.setModal(True)

        self.iniMSG = QMessageBox(self)
        self.iniMSG.setModal(False)
        self.iniMSG.setIcon(QMessageBox.Question)
        self.iniMSG.setWindowTitle("Confirm destination")
        self.iniMSG.setText("Download the zip files, or send to the Wii?")
        self.iniMSG_downloadBtn = QPushButton(self)
        self.iniMSG_wiiLoadBtn = QPushButton(self)
        self.iniMSG_cancelBtn = QPushButton(self)

        self.iniMSG_downloadBtn.setText("Download")
        self.iniMSG_wiiLoadBtn.setText("Send to Wii")
        self.iniMSG_cancelBtn.setText("Cancel")
        self.iniMSG_wiiLoadBtn.setObjectName("WiiLoadButton")

        self.iniMSG.addButton(self.iniMSG_wiiLoadBtn,
                              QMessageBox.ButtonRole.AcceptRole)
        self.iniMSG.addButton(self.iniMSG_downloadBtn,
                              QMessageBox.ButtonRole.AcceptRole)
        self.iniMSG.addButton(self.iniMSG_cancelBtn,
                              QMessageBox.ButtonRole.DestructiveRole)

        self.app = app
        self.splash = splash
        self.test_mode = test_mode

        # Set title and icon of window
        self.setWindowTitle(
            f"Open Shop Channel Downloader v{updater.current_version()} - Library")
        app_icon = QIcon(resource_path("assets/gui/windowicon.png"))
        self.setWindowIcon(app_icon)

        self.current_app = None
        self.current_category = "all"
        self.current_developer = ""
        self.repo_data = None
        self.icons_images = None
        self.long_description_cache = {}

        # Set GUI Icons

        # ABOUT
        self.ui.actionAbout_OSC_DL.setIcon(
            QIcon(resource_path("assets/gui/icons/about-open-version.png")))
        self.ui.actionIcons_provided_by.setIcon(
            QIcon(resource_path("assets/gui/icons/iconsprovider.png")))
        # CLIENTS
        self.ui.menuHomebrew_Browser.setIcon(
            QIcon(resource_path("assets/gui/icons/hbb-icon.png")))
        self.ui.actionDownload_HBB_Client_Latest.setIcon(
            QIcon(resource_path("assets/gui/icons/download.png")))
        self.ui.actionCheck_for_Updates.setIcon(
            QIcon(resource_path("assets/gui/icons/check-for-updates.png")))
        self.ui.actionRefresh.setIcon(
            QIcon(resource_path("assets/gui/icons/refresh.png")))
        # OPTIONS
        self.ui.actionCopy_Direct_Link.setIcon(
            QIcon(resource_path("assets/gui/icons/copy-link.png")))
        self.ui.actionEnable_Log_File.setIcon(
            QIcon(resource_path("assets/gui/icons/enable-log.png")))
        self.ui.actionClear_Log.setIcon(
            QIcon(resource_path("assets/gui/icons/clear-log.png")))
        self.ui.actionGenerate_Package_INI.setIcon(
            QIcon(resource_path("assets/gui/icons/ini.png")))
        self.ui.actionRead_Package_INI.setIcon(
            QIcon(resource_path("assets/gui/icons/ini-install.png")))
        self.ui.actionDownload_All_From_Repo.setIcon(
            QIcon(resource_path("assets/gui/icons/download-all.png")))
        self.ui.menuExperimental.setIcon(
            QIcon(resource_path("assets/gui/icons/experimental.png")))
        self.ui.actionSelect_Theme.setIcon(
            QIcon(resource_path("assets/gui/icons/theme.png")))
        # OPTIONS -> EXPERIMENTAL
        self.ui.menuAnnouncement_Banner.setIcon(
            QIcon(resource_path("assets/gui/icons/announcement-banner.png")))
        self.ui.actionDisplay_Banner.setIcon(
            QIcon(resource_path("assets/gui/icons/announcement-banner-reload.png")))

        # CATEGORIES COMBOBOX
        self.ui.CategoriesComboBox.setItemIcon(
            1, QIcon(resource_path("assets/gui/icons/category/utility.png")))
        self.ui.CategoriesComboBox.setItemIcon(
            2, QIcon(resource_path("assets/gui/icons/category/emulator.png")))
        self.ui.CategoriesComboBox.setItemIcon(
            3, QIcon(resource_path("assets/gui/icons/category/game.png")))
        self.ui.CategoriesComboBox.setItemIcon(
            4, QIcon(resource_path("assets/gui/icons/category/media.png")))
        self.ui.CategoriesComboBox.setItemIcon(
            5, QIcon(resource_path("assets/gui/icons/category/demo.png")))
        self.ui.CategoriesComboBox.setItemIcon(
            6, QIcon(resource_path("assets/gui/icons/category/queue.png")))

        # ACTIONS
        self.ui.actionDeveloper_Profile.setIcon(
            QIcon(resource_path("assets/gui/icons/profile.png")))
        self.ui.developer.addAction(
            self.ui.actionDeveloper_Profile, QLineEdit.TrailingPosition)

        # create spinner movie
        self.spinner = QMovie(resource_path("assets/gui/icons/spinner.gif"))
        self.spinner.setScaledSize(QSize(32, 32))
        self.spinner.start()

        self.ui.longDescriptionLoadingSpinner.setMovie(self.spinner)

        # set initial status icon
        self.status_icon("online")

        self.populate()
        self.selection_changed()
        self.ui.progressBar.setHidden(False)
        self.ui.statusBar.addPermanentWidget(self.ui.progressBar)
        self.ui.statusBar.addPermanentWidget(self.ui.statusIcon)
        # Load announcement banner
        t = threading.Thread(target=self.load_announcement_banner, daemon=True)
        t.start()

        # Close splash
        splash.finish(self)

    def update_splash_status(self, text):
        # if anyone has a better idea how to go about this.. will be appreciated
        try:
            if not self.splash.isHidden():
                self.splash.showMessage(text, color=QColor("White"))
        except NameError:
            pass

    def about_dialog(self):
        QMessageBox.about(self, f"About OSCDL",
                          f"<b>Open Shop Channel Downloader v{updater.current_version()} {updater.get_branch()}</b><br>"
                          f"by dhtdht020<br><br>"
                          f"<a href=\"https://github.com/dhtdht020/osc-dl\">https://github.com/dhtdht020/osc-dl</a><br>"
                          f"<a href=\"https://oscwii.org\">https://oscwii.org</a><br><br>"
                          f"Many icons provided by <a href=\"https://icons8.com/\">icons8.com</a><br><br>"
                          f"Using Qt {QtCore.qVersion()}<br>"
                          f"Using Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")

    # show given status message on bottom status bar
    def status_message(self, message):
        self.ui.statusBar.showMessage(message)

    def status_icon(self, icon):
        self.ui.statusIcon.setPixmap(
            QPixmap(resource_path(f"assets/gui/icons/status/{icon}.png")))

    # populate UI elements
    def populate(self):
        self.update_splash_status("Loading contents..")
        self.ui.actionAbout_OSC_DL.setText(
            f"About OSCDL v{updater.current_version()} by dhtdht020")
        self.populate_repositories()
        self.populate_list()
        self.assign_initial_actions()

    # Populate list of repositories
    def populate_repositories(self):
        self.repos = api.Hosts()
        n = 0
        for host in self.repos.list():
            repo = self.repos.list()[host]
            display_name = repo["name"]
            hostname = repo["host"]
            description = repo["description"]
            self.ui.ReposComboBox.addItem(display_name)
            self.ui.ReposComboBox.setItemData(
                n, [display_name, hostname, description, host], Qt.UserRole)
            gui_helpers.QUEUE_SIGNAL_CACHE[host] = {}
            n += 1
            self.update_splash_status(f"Loaded {n} repositories..")
        # set current repository
        self.current_repo = self.repos.get("primary")
        index = self.ui.ReposComboBox.currentIndex()
        self.repo_data = self.ui.ReposComboBox.itemData(index, Qt.UserRole)

    def assign_initial_actions(self):
        self.update_splash_status("Finishing (1/2)..")

        # Connect signals
        # Buttons

        # Copy app download link
        self.ui.actionCopy_Direct_Link.triggered.connect(
            lambda: (QApplication.clipboard().setText(self.current_app['zip_url']),
                     self.status_message(f"Copied the download link for "
                                         f"\"{self.current_app['display_name']}\" to clipboard")))

        self.ui.ViewMetadataBtn.clicked.connect(self.download_app)
        self.ui.WiiLoadButton.clicked.connect(self.wiiload_button)
        self.ui.ReturnToMainBtn.clicked.connect(self.return_to_all_apps_btn)
        self.ui.MultiSelectToggle.clicked.connect(partial(self.multi_select))
        self.ui.ClearMultiSelectButton.clicked.connect(
            lambda: self.clear_multi_select(user_request=True))

        # Search Bar
        self.ui.SearchBar.textChanged.connect(self.search_bar)

        # Others
        self.ui.ReposComboBox.currentIndexChanged.connect(self.changed_host)
        self.ui.CategoriesComboBox.currentIndexChanged.connect(
            self.changed_category)
        self.ui.listAppsWidget.currentItemChanged.connect(
            self.selection_changed)
        self.ui.tabMetadata.currentChanged.connect(self.tab_changed)
        self.ui.actionDeveloper_Profile.triggered.connect(
            self.developer_profile)
        self.iniMSG_downloadBtn.clicked.connect(self.download_app)
        self.iniMSG_wiiLoadBtn.clicked.connect(self.wiiload_button)
        self.iniMSG_cancelBtn.clicked.connect(self.cancelINI)

        # Actions
        # -- About
        self.ui.actionAbout_OSC_DL.triggered.connect(self.about_dialog)
        # -- Debug
        self.ui.actionEnable_Log_File.triggered.connect(self.turn_log_on)
        self.ui.actionGenerate_Package_INI.triggered.connect(self.createINI)
        self.ui.actionRead_Package_INI.triggered.connect(self.readINI)
        self.ui.actionDisplay_Banner.triggered.connect(
            self.load_announcement_banner)
        self.ui.actionSelect_Theme.triggered.connect(self.select_theme_action)
        # -- Clients
        # ---- Homebrew Browser
        self.ui.actionDownload_HBB_Client_Latest.triggered.connect(
            lambda: QDesktopServices().openUrl("https://oscwii.org/"))
        # ---- OSCDL
        self.ui.actionCheck_for_Updates.triggered.connect(
            partial(self.check_for_updates_action))
        self.ui.actionRefresh.triggered.connect(partial(self.repopulate))
        # -- Options
        self.ui.actionDownload_All_From_Repo.triggered.connect(
            self.select_all_apps)

    # When user switches to a different tab
    def tab_changed(self):
        if self.ui.tabMetadata.currentIndex() == 1:
            t = threading.Thread(
                target=self.load_long_description, daemon=True)
            t.start()

    # Load long description
    def load_long_description(self):
        self.LongDescriptionSignal.connect(
            self.ui.longDescriptionBrowser.setText)

        if self.current_app["internal_name"] in self.long_description_cache.keys():
            self.LongDescriptionSignal.emit(
                self.long_description_cache[self.current_app["internal_name"]])
        else:
            self.ui.longDescriptionLoadingSpinner.setVisible(True)
            self.LongDescriptionSignal.emit("Loading description..")

            long_description = metadata.long_description(
                self.current_app["internal_name"], repo=self.current_repo['host'])
            self.LongDescriptionSignal.emit(long_description)

            # save to long description cache
            self.long_description_cache[self.current_app["internal_name"]
                                        ] = long_description

            # hide loading spinner
            self.ui.longDescriptionLoadingSpinner.setVisible(False)

    # When user selects a different homebrew from the list
    def selection_changed(self):
        self.update_splash_status("Finishing (2/2) - Loading first app..")

        try:
            self.current_app = self.ui.listAppsWidget.currentItem().data(Qt.UserRole)
            app_name = self.current_app["internal_name"]
        except Exception:
            app_name = None
        if app_name is not None:
            # Set active tab to first
            self.ui.tabMetadata.setCurrentIndex(0)

            # Set loading animation
            self.ui.HomebrewIconLabel.setMovie(self.spinner)

            # Clear supported controllers listview:
            self.ui.SupportedControllersListWidget.clear()

            # Enable Send to Wii button
            self.ui.WiiLoadButton.setEnabled(True)
            if len(gui_helpers.MULTISELECT):
                self.ui.WiiLoadButton.setText("Send queue to Wii")
            else:
                self.ui.WiiLoadButton.setText("Send to Wii")

            # see if its part of the queue.
            self.ui.MultiSelectToggle.setChecked(
                self.current_app in gui_helpers.MULTISELECT)

            # -- Get actual metadata
            # App Name
            self.ui.appname.setText(self.current_app["display_name"])
            self.ui.SelectionInfoBox.setTitle(
                "Information: " + self.current_app["display_name"])
            self.ui.label_displayname.setText(self.current_app["display_name"])

            # File Size
            try:
                extracted = utils.file_size(self.current_app["extracted"])
                compressed = utils.file_size(self.current_app["zip_size"])
                self.ui.filesize.setText(f"{compressed} / {extracted}")
                self.ui.filesize.setToolTip(
                    f"Compressed Download: {compressed}\nExtracted Size: {extracted}")
            except KeyError:
                self.ui.filesize.setText("Unknown")

            # Category
            self.ui.HomebrewCategoryLabel.setText(
                metadata.category_display_name(self.current_app["category"]))

            # Release Date
            self.ui.releasedate.setText(
                datetime.fromtimestamp(int(self.current_app["release_date"])).strftime('%B %e, %Y'))

            # Peripherals
            peripherals = metadata.parse_peripherals(
                self.current_app["controllers"])
            # Add icons for Wii Remotes
            if peripherals["wii_remotes"] > 1:
                item = QListWidgetItem()
                item.setText(f"{str(peripherals['wii_remotes'])} Wii Remotes")
                item.setIcon(QIcon(
                    resource_path(f"assets/gui/icons/controllers/{str(peripherals['wii_remotes'])}WiiRemote.png")))
                item.setToolTip(
                    f"This app supports up to {str(peripherals['wii_remotes'])} Wii Remotes.")
                self.ui.SupportedControllersListWidget.addItem(item)
            elif peripherals["wii_remotes"] == 1:
                item = QListWidgetItem()
                item.setText(f"1 Wii Remote")
                item.setIcon(
                    QIcon(resource_path(f"assets/gui/icons/controllers/1WiiRemote.png")))
                item.setToolTip("This app supports a single Wii Remote.")
                self.ui.SupportedControllersListWidget.addItem(item)
            if peripherals["nunchuk"] is True:
                item = QListWidgetItem()
                item.setText(f"Nunchuk")
                item.setIcon(
                    QIcon(resource_path(f"assets/gui/icons/controllers/Nunchuk.png")))
                item.setToolTip("This app can be used with a Nunchuk.")
                self.ui.SupportedControllersListWidget.addItem(item)
            if peripherals["classic"] is True:
                item = QListWidgetItem()
                item.setText(f"Classic Controller")
                item.setIcon(
                    QIcon(resource_path(f"assets/gui/icons/controllers/ClassicController.png")))
                item.setToolTip(
                    "This app can be used with a Classic Controller.")
                self.ui.SupportedControllersListWidget.addItem(item)
            if peripherals["gamecube"] is True:
                item = QListWidgetItem()
                item.setText(f"GameCube Controller")
                item.setIcon(
                    QIcon(resource_path(f"assets/gui/icons/controllers/GamecubeController.png")))
                item.setToolTip(
                    "This app can be used with a Gamecube Controller.")
                self.ui.SupportedControllersListWidget.addItem(item)
            if peripherals["wii_zapper"] is True:
                item = QListWidgetItem()
                item.setText(f"Wii Zapper")
                item.setIcon(
                    QIcon(resource_path(f"assets/gui/icons/controllers/WiiZapper.png")))
                item.setToolTip("This app can be used with a Wii Zapper.")
                self.ui.SupportedControllersListWidget.addItem(item)
            if peripherals["keyboard"] is True:
                item = QListWidgetItem()
                item.setText(f"USB Keyboard")
                item.setIcon(
                    QIcon(resource_path(f"assets/gui/icons/controllers/USBKeyboard.png")))
                item.setToolTip("This app can be used with a USB Keyboard.")
                self.ui.SupportedControllersListWidget.addItem(item)
            if peripherals["sdhc"] is True:
                item = QListWidgetItem()
                item.setText(f"SDHC Card")
                item.setIcon(
                    QIcon(resource_path(f"assets/gui/icons/controllers/SDHC.png")))
                item.setToolTip("This app is confirmed to support SDHC cards.")
                self.ui.SupportedControllersListWidget.addItem(item)

            # Version
            self.ui.version.setText(self.current_app["version"])

            # Coder
            self.ui.developer.setText(self.current_app["coder"])

            # Short Description
            self.ui.label_description.setToolTip(None)
            if self.current_app["short_description"] == "":
                self.ui.label_description.setText("No description specified.")
            else:
                self.ui.label_description.setText(
                    self.current_app["short_description"])
                if len(self.current_app["short_description"]) >= 40:
                    self.ui.label_description.setToolTip(
                        self.current_app["short_description"])

            # Long Description
            self.ui.longDescriptionBrowser.setText(
                self.current_app["long_description"])

        self.ui.progressBar.setValue(0)
        self.repaint()
        # Load icon
        t = threading.Thread(target=self.load_icon, args=[app_name], daemon=True)
        t.start()

    def view_metadata(self):
        data = self.ui.listAppsWidget.currentItem().data(Qt.UserRole)
        self.app_name = data["internal_name"]

    def trugh(self, text):
        return QObject.tr(self, text)

    # TODO FULL REWRITE
    def download_app(self, extract_root=False):
        gui_helpers.IN_DOWNLOAD_DIALOG = True
        total_downloads = []
        internal_names = []
        display_names = []
        if len(gui_helpers.MULTISELECT) == 0:
            gui_helpers.MULTISELECT.append(self.current_app)

        self.status_message(f"Downloading {gui_helpers.MULTISELECT[0]['display_name']} from Open Shop Channel..")
        self.status_icon("pending")
        self.ui.progressBar.setMaximum(0)

        if self.sender():
            object_name = self.sender().objectName()
        else:
            object_name = None

        # determine if should ask for path
        DownloadLocationDialogAlreadyAsked = False
        AcknowldegedOverwrite = False
        DirectorySelected = ''
        save_location = ''
        alreadyCreatedFolder = False
        duplicateCounts = 0

        dialog = DownloadLocationDialog(gui_helpers.MULTISELECT, parent=self)

        for index, package in enumerate(gui_helpers.MULTISELECT):
            dupCheck = [i for i, x in enumerate(
                gui_helpers.MULTISELECT) if x == package]
            if len(dupCheck) > 1 and index in dupCheck and dupCheck[0] != index:
                total_downloads.append(save_location)
                internal_names.append(package['internal_name'])
                display_names.append(package)
                duplicateCounts += 1
                continue
            if (object_name != "WiiLoadButton") and not self.test_mode:
                if not DownloadLocationDialogAlreadyAsked:
                    status = dialog.exec()

                if status:
                    DownloadLocationDialogAlreadyAsked = True
                    logging.debug(f"Selected drive: {dialog.selection}")
                    if dialog.selection == "browse":
                        if len(gui_helpers.MULTISELECT) == 1:
                            save_location, _ = QFileDialog.getSaveFileName(self, 'Save Application',
                                                                           self.current_app["internal_name"] + ".zip")
                        else:
                            if DirectorySelected == '':
                                DirectorySelected = QFileDialog.getExistingDirectory(
                                    self, 'Save Application to Directory', os.path.expanduser("~"), QFileDialog.ShowDirsOnly)
                                if DirectorySelected == '':
                                    save_location = ''
                                else:
                                    save_location = f'{DirectorySelected}/{package["internal_name"]}.zip'
                            else:
                                save_location = f'{DirectorySelected}/{package["internal_name"]}.zip'

                    else:
                        if not dialog.selection["appsdir"] and alreadyCreatedFolder == False:
                            try:
                                os.mkdir(
                                    dialog.selection["drive"].rootPath() + "/apps")
                            except PermissionError:
                                QMessageBox.critical(self, "Permission Error",
                                                     "Could not create the apps directory on the selected device.")
                                return
                            alreadyCreatedFolder = True
                        save_location = dialog.selection["drive"].rootPath() + "/apps/" + package[
                            "internal_name"] + ".zip"
                        extract_root = True
                else:
                    save_location = ''

                if len(gui_helpers.MULTISELECT) > 1 and not AcknowldegedOverwrite and (os.path.exists(save_location) or os.path.exists(save_location.replace(".zip", "/"))):
                    shouldOverwrite = QMessageBox.question(self, "Confirm overwrite", f"'{package['display_name']}' already exists in this directory. Overwrite anyway?",
                                                           QMessageBox.StandardButton.No | QMessageBox.StandardButton.YesToAll | QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No)

                    if shouldOverwrite == QMessageBox.StandardButton.No:
                        save_location = ''
                    elif shouldOverwrite == QMessageBox.StandardButton.YesToAll:
                        AcknowldegedOverwrite = True

            else:
                # create output dir
                if os.name == 'nt':
                    dir_path = '%s\\OSCDL\\' % os.environ['APPDATA']
                    if not os.path.exists(dir_path):
                        os.makedirs(dir_path)
                    save_location = f'%s{package["internal_name"]}' % dir_path
                else:
                    save_location = f"{package['internal_name']}.zip"
            self.ui.progressBar.setValue(0)
            if save_location:
                # stream file, so we can iterate
                response = requests.get(package["zip_url"], stream=True)
                total_size = int(response.headers.get('content-length', 0))

                # set progress bar
                self.ui.progressBar.setMaximum(total_size)
                block_size = 1024
                if response.status_code == 200:
                    self.safe_mode(True)
                    self.status_icon("download")

                    with open(save_location, "wb") as app_data_file:
                        for data in response.iter_content(block_size):
                            self.ui.progressBar.setValue(
                                self.ui.progressBar.value() + 1024)
                            self.status_message(
                                f"Downloading {package['display_name']} from Open Shop Channel.. ({utils.file_size(self.ui.progressBar.value())}/{utils.file_size(total_size)})")
                            try:
                                self.app.processEvents()
                            except NameError:
                                pass
                            app_data_file.write(data)

                    if extract_root:
                        self.status_message("Extracting..")

                        with zipfile.ZipFile(save_location, 'r') as zip_file:
                            # unzip to root_path
                            root_path = utils.get_mount_point(save_location)
                            zip_file.extractall(root_path)

                        os.remove(save_location)

                self.ui.progressBar.setValue(total_size)
                self.status_message(
                    f"Download of \"{package['display_name']}\" has completed successfully")
                total_downloads.append(save_location)
                internal_names.append(package['internal_name'])
                display_names.append(package)
                if object_name != "WiiLoadButton":
                    # add entry to applications list
                    self.changeQueueStatus(package,"downloaded")
            else:
                self.ui.progressBar.setMaximum(100)
                self.ui.progressBar.setValue(0)
                self.safe_mode(False)
                self.status_message("Cancelled Download")
                self.status_icon("online")
                if len(gui_helpers.MULTISELECT) == 1:
                    self.clear_multi_select(user_request=False)
                gui_helpers.IN_DOWNLOAD_DIALOG = False
                return None
        if len(total_downloads) > 1:
            self.status_message(
                f"{len(total_downloads)-duplicateCounts} downloads has completed successfully")
        if object_name != "WiiLoadButton":
            if len(gui_helpers.MULTISELECT) == 1:
                self.clear_multi_select(user_request=False)
            self.safe_mode(False)
        self.status_icon("online")
        gui_helpers.IN_DOWNLOAD_DIALOG = False
        return total_downloads, internal_names, display_names

    def reset_status(self):
        if not gui_helpers.CURRENTLY_SENDING and not gui_helpers.IN_DOWNLOAD_DIALOG:
            self.ui.progressBar.setMaximum(100)
            self.status_message("Ready to download")
            self.status_icon("online")

    def safe_mode(self, state: bool):
        """
        Disable all widgets that could interrupt sensitive processes
        :param state: bool
        """
        self.ui.ViewMetadataBtn.setDisabled(state)
        self.ui.WiiLoadButton.setDisabled(state)
        self.ui.ReposComboBox.setDisabled(state)
        self.ui.listAppsWidget.setDisabled(state)
        self.ui.MultiSelectToggle.setDisabled(state)
        self.ui.ClearMultiSelectButton.setDisabled(
            state or not bool(len(gui_helpers.MULTISELECT)))
    
    def changeQueueStatus(self, pkgData, statusType, repoChange=False):
        for bgcolor in self.ui.listAppsWidget.findItems(f"{utils.file_size(pkgData['extracted'])} | "
            f"{pkgData['version']} | "
            f"{pkgData['coder']} | "
            f"{pkgData['short_description']}", Qt.MatchContains):
            bgcolor.setBackground(QColor(gui_helpers.QUEUE_SIGNAL_COLORS[statusType]))
        if not repoChange:
            gui_helpers.QUEUE_SIGNAL_CACHE[pkgData["repo"]][pkgData["internal_name"]] = statusType

    def wiiload_button(self):
        warnText = "This app contains"
        if len(gui_helpers.MULTISELECT) > 1:
            warnText = "Several apps contain"
        if not utils.app_has_extra_directories(self.current_app) and QMessageBox.question(self, "Send to Wii", f"{warnText} extra files and directories that may need configuration. Send anyway?") == QMessageBox.StandardButton.No:
            if gui_helpers.IS_IMPORTED_FILE:
                self.cancelINI()
            return

        if len(gui_helpers.MULTISELECT) == 0:
            gui_helpers.MULTISELECT.append(self.current_app)
        dialog = WiiLoadDialog(self.current_app, parent=self)
        status = dialog.exec()
        if not status:
            if len(gui_helpers.MULTISELECT) == 1:
                self.clear_multi_select(user_request=False)
            if gui_helpers.IS_IMPORTED_FILE:
                self.cancelINI()
            return
        gui_helpers.CURRENTLY_SENDING = True

        self.status_message(
            "Downloading " + gui_helpers.MULTISELECT[0]['display_name'] + " from Open Shop Channel..")
        self.ui.progressBar.setValue(25)

        # get app
        app_paths, internal_names, display_names = self.download_app()
        self.ui.progressBar.setMaximum(100)
        conn = None

        iniIter = 0
        dolOnly = None
        failCount = 0
        for i, path in enumerate(app_paths):
            if gui_helpers.IS_IMPORTED_FILE:
                while (gui_helpers.MULTISELECT_INI[iniIter] not in path and "~" not in gui_helpers.MULTISELECT_INI[iniIter]):
                    InstallMsg = wiiloadInstallerMSG(gui_helpers.MULTISELECT_INI[iniIter].replace(
                        "|", ""), showHBText=False, parent=self)
                    status = InstallMsg.exec()
                    #QMessageBox.information(self,"Installation Notice",gui_helpers.MULTISELECT_INI[iniIter].replace("|",""))
                    self.app.processEvents()
                    iniIter += 1
                if ("~" in gui_helpers.MULTISELECT_INI[iniIter]):
                    dolOnly = gui_helpers.MULTISELECT_INI[iniIter]
                iniIter += 1

            with open(path, 'rb') as f:
                content = f.read()

            zipped_app = io.BytesIO(content)
            preparedData = io.BytesIO()

            # Our zip file should only contain one directory with the app data in it,
            # but the downloaded file contains an apps/ directory. We're removing that here.
            bootType, OK = wiiload.organize_zip(
                zipped_app, preparedData, dolOnly, internal_names[i])

            if not OK:
                QMessageBox.warning(self, 'Package error',
                                    f'"{display_names[i]["display_name"]}" is a theme, and cannot be used with ~.')
                dolOnly = False

            # preparing
            prep = wiiload.prepare(preparedData)

            file_size = prep[0]
            compressed_size = prep[1]
            chunks = prep[2]
            c_data = prep[3]

            # connecting
            self.status_message('Connecting to the HBC...')
            self.status_icon('connecting_hbc')
            self.ui.progressBar.setValue(50)

            try:
                if dialog.modeSelect == 0:  # TCP/IP
                    conn = wiiload.connect(dialog.address)
                else:  # USBGecko
                    conn = serial.Serial()
                    conn.inter_byte_timeout = 1.0
                    conn.port = dialog.address
                    # Timeout: 1 sec, function: conn.open()
                    func_timeout.func_timeout(1, conn.open)
                    conn.send = conn.write  # Keeps the wiiload logic the same
            except (func_timeout.exceptions.FunctionTimedOut, Exception) as e:
                self.status_icon('sad')
                conn_type = ["IP address", "connection"]
                logging.error(
                    f'Error while connecting to the HBC. Please check the {conn_type[dialog.modeSelect]} and try again.')
                QMessageBox.warning(self, 'Connection error',
                                    f'Error while connecting to the HBC. Please check the {conn_type[dialog.modeSelect]} and try again.')
                print(f'WiiLoad: {e}')
                self.ui.progressBar.setValue(0)
                self.status_message('Error: Could not connect to the Homebrew Channel. :(')
                self.status_icon('online')
                failCount+=1
                '''

                # delete application zip file
                for path in (app_paths):
                    if os.path.isfile(path):
                        os.remove(path)
                gui_helpers.CURRENTLY_SENDING = False
                gui_helpers.IS_IMPORTED_FILE = False
                self.safe_mode(False)
                return
                
                '''
                self.changeQueueStatus(display_names[i],"failed")
                if dolOnly and iniIter < len(gui_helpers.MULTISELECT_INI) and gui_helpers.MULTISELECT_INI[iniIter] and "|" in gui_helpers.MULTISELECT_INI[iniIter]:
                    iniIter += 1
                continue
                

            wiiload.handshake(conn, compressed_size, file_size)

            # Sending file
            self.status_message('Sending app...')
            self.status_icon('sending')

            chunk_num = 1
            if dialog.modeSelect == 0:  # TCP/IP
                try:
                    for chunk in chunks:
                        conn.send(chunk)
                        chunk_num += 1
                        progress = round(chunk_num / len(chunks) * 50) + 50
                        self.ui.progressBar.setValue(progress)
                        try:
                            self.app.processEvents()
                        except NameError:
                            pass
                except Exception as e:
                    logging.error(
                        'Error while connecting to the HBC. Operation timed out. Close any dialogs on HBC and try again.')
                    QMessageBox.warning(self, 'Connection error',
                                        'Error while connecting to the HBC. Operation timed out. Close any dialogs on HBC and try again.')
                    print(f'WiiLoad: {e}')
                    self.ui.progressBar.setValue(0)
                    self.status_message('Error: Could not connect to the Homebrew Channel. :(')
                    failCount+=1
                    '''
                    # delete application zip file
                    for path in (app_paths):
                        if os.path.isfile(path):
                            os.remove(path)
                    gui_helpers.CURRENTLY_SENDING = False
                    gui_helpers.IS_IMPORTED_FILE = False
                    self.safe_mode(False)
                    return
                    '''
                    self.changeQueueStatus(display_names[i],"failed")
                    if dolOnly and iniIter < len(gui_helpers.MULTISELECT_INI) and gui_helpers.MULTISELECT_INI[iniIter] and "|" in gui_helpers.MULTISELECT_INI[iniIter]:
                        iniIter += 1
                    continue
            # USBGecko
            else:
                # conn.send is blocking, used thread to avoid.
                t = threading.Thread(target=self.send_gecko, daemon=True, args=[
                                     c_data, conn, path])
                t.start()
                self.ui.progressBar.setMaximum(0)
                while t.is_alive():
                    try:
                        self.app.processEvents()
                    except NameError:
                        pass
                t.join()
                if not gui_helpers.DATASENT:
                    self.changeQueueStatus(display_names[i],"failed")
                    if dolOnly and iniIter < len(gui_helpers.MULTISELECT_INI) and gui_helpers.MULTISELECT_INI[iniIter] and "|" in gui_helpers.MULTISELECT_INI[iniIter]:
                        iniIter += 1  
                    failCount+=1       
                    '''
                    for path in (app_paths):
                        if os.path.isfile(path):
                            os.remove(path)
                    gui_helpers.CURRENTLY_SENDING = False
                    gui_helpers.IS_IMPORTED_FILE = False
                    self.safe_mode(False)
                    return
                    '''
                    continue
                    
                self.ui.progressBar.setMaximum(100)
                self.ui.progressBar.setValue(100)

            #file_name = f'{self.current_app["internal_name"]}.zip'
            if (dolOnly):
                splitArg = []
                argList = re.findall("(<.*>)", dolOnly)
                if len(argList) != 0:
                    argList = argList[0]
                    splitArg = argList[1:-1].split(",")
                args = [f"boot.{bootType}"] + splitArg
                args = "\x00".join(args) + "\x00"
                conn.send(bytes(args, 'utf-8'))
            else:
                conn.send(bytes(path, 'utf-8') + b'\x00')
            
            if conn:
                if dialog.modeSelect == 1:
                    conn.flush()
                conn.close()

            self.ui.progressBar.setValue(100)
            self.status_message('App transmitted!')
            self.status_icon('online')
            logging.info(f"App transmitted to HBC at {dialog.address}")
            self.changeQueueStatus(display_names[i],"downloaded")
            if dolOnly and iniIter < len(gui_helpers.MULTISELECT_INI) and gui_helpers.MULTISELECT_INI[iniIter] and "|" in gui_helpers.MULTISELECT_INI[iniIter]:
                InstallMsg = wiiloadInstallerMSG(gui_helpers.MULTISELECT_INI[iniIter].replace(
                    "|", ""), showHBText=True, parent=self)
                status = InstallMsg.exec()
                #QMessageBox.information(self,"Installation Notice",gui_helpers.MULTISELECT_INI[iniIter].replace("|","")+"\nClick OK after returning to the Homebrew Channel and the network is connected.")
                self.app.processEvents()
                iniIter += 1
            else:
                QMessageBox.information(
                    self, "Send to Wii", f"{i+1} file{'s' if (i+1)>1 else ''} sent. On the Homebrew Channel, please select 'Yes' to extract the file, then click OK here.")
            dolOnly = None
        for path in (app_paths):
            if os.path.isfile(path):
                os.remove(path)
        gui_helpers.CURRENTLY_SENDING = False
        self.safe_mode(False)
        if len(gui_helpers.MULTISELECT) == 1:
            self.clear_multi_select(user_request=False)
        else:
            if len(app_paths) - failCount == 0:
                self.status_message('Error: Could not connect to the Homebrew Channel. :(')
            else:
                self.status_message(f"{len(app_paths) - failCount} apps tansmitted!")
        gui_helpers.IS_IMPORTED_FILE = False

    def send_gecko(self, c_data, conn, path_to_app):
        try:
            conn.send(c_data)
        except Exception as e:
            logging.error(
                'Error while connecting to the HBC. Close any dialogs on HBC and try again.')
            QMessageBox.warning(self, 'Connection error',
                                'Error while connecting to the HBC. Close any dialogs on HBC and try again.')
            print(f'WiiLoad: {e}')
            self.ui.progressBar.setValue(0)
            self.status_message(
                'Error: Could not connect to the Homebrew Channel. :(')

            # delete application zip file
            conn.close()
            gui_helpers.DATASENT = False
            return
        gui_helpers.DATASENT = True

    def changed_host(self):
        # or (len(gui_helpers.MULTISELECT) and QMessageBox.question(self,"Change repositiory","Changing the repository will clear the queue.\nContinue anyway?") == QMessageBox.StandardButton.No):
        if (self.ongoingOperations() and self.message.show() == None):
            try:
                self.ui.ReposComboBox.currentIndexChanged.disconnect(
                    self.changed_host)
            except Exception:
                pass
            self.ui.ReposComboBox.setCurrentIndex(self.ui.ReposComboBox.findData(
                [self.current_repo["name"], self.current_repo["host"], self.current_repo["description"], self.current_repo["id"]]))
            self.ui.ReposComboBox.currentIndexChanged.connect(
                self.changed_host)
            return
        # self.clear_multi_select(user_request=False)
        self.icons_images = None
        self.long_description_cache.clear()
        index = self.ui.ReposComboBox.currentIndex()
        self.repo_data = self.ui.ReposComboBox.itemData(index, Qt.UserRole)
        self.current_repo = self.repos.get(self.repo_data[3])
        self.status_message(
            f"Loading {self.current_repo['host']} repository..")
        logging.info(f"Loading {self.current_repo['host']}")
        self.repopulate(fromRepoChange=True)

    def repopulate(self, fromRepoChange=False):
        if self.ongoingOperations():
            self.message.show()
            return

        if not fromRepoChange and len(gui_helpers.MULTISELECT) and QMessageBox.question(self, "Refresh list", "Refreshing the list will clear the queue.\nIs this okay?") == QMessageBox.StandardButton.Yes:
            self.clear_multi_select(user_request=False)
        # Make sure everything is hidden / shown
        self.ui.ReturnToMainBtn.setHidden(True)
        self.ui.CategoriesComboBox.setHidden(False)
        self.ui.ReposComboBox.setHidden(False)
        self.ui.SearchBar.setText("")

        self.status_message("Reloading list..")
        self.status_icon("loading")
        try:
            self.ui.CategoriesComboBox.currentIndexChanged.disconnect(
                self.changed_category)
        except Exception:
            pass
        self.ui.CategoriesComboBox.setCurrentIndex(0)
        self.ui.listAppsWidget.clear()
        self.populate_list()
        self.ui.CategoriesComboBox.currentIndexChanged.connect(
            self.changed_category)

    def populate_list(self):
        try:
            self.update_splash_status("Connecting to server..")

            # Set default icon size
            self.ui.listAppsWidget.setIconSize(QSize(-1, -1))

            # Get apps json
            self.apps = api.Applications(
                self.repos.get(self.current_repo['id']))
            i = 0

            for package in self.apps.get_apps():
                try:
                    # let's check if the app celebrates its birthday today
                    birthday = utils.app_birthday_string(package)
                    if birthday:
                        birthday = f" [{birthday}]"
                    else:
                        birthday = ""

                    # add entry to applications list
                    self.ui.listAppsWidget.addItem(f"{package['display_name']}{birthday}\n"
                                                   f"{utils.file_size(package['extracted'])} | "
                                                   f"{package['version']} | "
                                                   f"{package['coder']} | "
                                                   f"{package['short_description']}")
                    list_item = self.ui.listAppsWidget.item(i)

                    list_item.setData(Qt.UserRole, package)

                    if list_item.data(Qt.UserRole)["internal_name"] in gui_helpers.QUEUE_SIGNAL_CACHE[self.current_repo['id']]:
                        self.changeQueueStatus(package,gui_helpers.QUEUE_SIGNAL_CACHE[self.current_repo['id']][list_item.data(Qt.UserRole)["internal_name"]],repoChange=True)

                    # Set category icon
                    category = package["category"]

                    if category == "utilities":
                        list_item.setIcon(
                            QIcon(resource_path("assets/gui/icons/category/utility.png")))
                    elif category == "games":
                        list_item.setIcon(
                            QIcon(resource_path("assets/gui/icons/category/game.png")))
                    elif category == "emulators":
                        list_item.setIcon(
                            QIcon(resource_path("assets/gui/icons/category/emulator.png")))
                    elif category == "media":
                        list_item.setIcon(
                            QIcon(resource_path("assets/gui/icons/category/media.png")))
                    elif category == "demos":
                        list_item.setIcon(
                            QIcon(resource_path("assets/gui/icons/category/demo.png")))
                    self.update_splash_status(f"Loaded {i} apps..")
                    i += 1
                except IndexError:
                    pass
            self.sort_list_alphabetically()
            self.ui.listAppsWidget.setCurrentRow(0)
            self.ui.AppsAmountLabel.setText(
                str(self.ui.listAppsWidget.count()) + " Apps")

        except Exception as e:
            QMessageBox.critical(self, 'OSCDL: Critical Network Error',
                                 'Could not connect to the Open Shop Channel server.\n'
                                 'Cannot continue. :(\n'
                                 'Please check your internet connection, or report this incident.\n\n'
                                 f'{e}')
            sys.exit(1)

        # load app icons
        if not gui_helpers.CURRENTLY_SENDING and not gui_helpers.IN_DOWNLOAD_DIALOG and not gui_helpers.INI_ACTION:
            self.status_message("Loading app icons from server..")
            self.ui.progressBar.setMaximum(0)
        t = threading.Thread(target=self.download_app_icons, daemon=True)
        t.start()

    # Actions
    # Enable log
    def turn_log_on(self):
        logging.basicConfig(filename='oscdl-gui.log', level=logging.DEBUG,
                            format="%(asctime)s | %(levelname)s:%(name)s:%(message)s")
        logging.info('Enabled log file. Hello!')
        logging.info(
            f"OSCDL v{updater.current_version()} {updater.get_branch()}")
        logging.info(updater.get_type())
        self.status_message('DEBUG: Enabled log file. To disable, exit OSCDL.')
        self.ui.actionEnable_Log_File.setDisabled(True)
        self.ui.actionClear_Log.setEnabled(True)
        self.ui.actionClear_Log.triggered.connect(self.clear_log)

    # Clear log file
    def clear_log(self):
        open("oscdl-gui.log", 'w').close()
        self.status_message('Cleared log file.')

    # Sort apps in app list in alphabetical, ascending order.
    def sort_list_alphabetically(self):
        self.ui.listAppsWidget.sortItems(Qt.AscendingOrder)

    # Check for updates dialog
    def check_for_updates_action(self):
        self.status_message(
            "Checking for updates.. This will take a few moments..")
        latest = updater.latest_version()
        if updater.check_update(latest) is True:
            self.status_message(
                "New version available! (" + latest['tag_name'] + ") OSCDL is out of date.")
            body = latest['body'].replace("![image]", "")
            QMessageBox.warning(self, 'OSCDL is out of date - New Release Available!',
                                f"<a href='https://github.com/dhtdht020/osc-dl'>View on GitHub</a><br>"
                                f"<b style=\"font-size: 20px\">{latest['name']}</b><hr>"
                                f"<b>Released on {datetime.strptime(latest['published_at'], '%Y-%m-%dT%H:%M:%SZ')}</b><br><br>"
                                f"{markdown.markdown((body[:705] + '... <br><i>Learn more on GitHub</i>') if len(body) > 705 else body)}<hr>"
                                f"Please go to the <a href='https://github.com/dhtdht020/osc-dl'>GitHub page</a> and obtain the latest release<br>"
                                f"Newest Version: {latest['tag_name']}")
        else:
            self.status_message("OSCDL is up to date!")
            QMessageBox.information(self, 'OSCDL is up to date',
                                    'You are running the latest version of OSCDL!\n')

    # Load app icon
    def load_icon(self, app_name):
        self.IconSignal.connect(self.ui.HomebrewIconLabel.setPixmap)
        # check if icons_images is populated, if not load from server
        if self.icons_images and app_name in self.icons_images:
            self.IconSignal.emit(self.icons_images[app_name])
            self.ui.HomebrewIconLabel.show()
        else:
            # Gets raw image data from server
            # Check if still relevant
            if self.current_app["internal_name"] == app_name:
                data = metadata.icon(self.current_app)

                # Loads image
                image = QtGui.QImage()
                image.loadFromData(data)

                # Adds image to label
                # Once again check if still relevant
                if self.current_app["internal_name"] == app_name:
                    self.IconSignal.emit(QPixmap(image))
                    self.ui.HomebrewIconLabel.show()

    def load_announcement_banner(self):
        try:
            announcement = updater.get_announcement()
            announcement_label = announcement[0]
            announcement_url_label = announcement[1]
            announcement_banner_color = announcement[2]
            announcement_banner_text_color = announcement[3]
            announcement_website_enabled = announcement[4]
            if announcement is not None:
                # Un-hide banner
                self.AnnouncementBannerHidden.connect(
                    self.ui.announcement.setHidden)
                self.AnnouncementBannerHidden.emit(False)

                # Set banner styling
                self.ui.announcement.setStyleSheet(f'QFrame {{'
                                                   f'background-color: {announcement_banner_color};'
                                                   f'color: {announcement_banner_text_color};'
                                                   f'}}')

                # Populate banner
                self.ui.announcementLabel.setText(announcement_label)
                self.ui.announcementURLLabel.setText(announcement_url_label)

                if announcement_website_enabled is False:
                    self.ui.announcementURLLabel.setHidden(True)

        except Exception:
            pass

    def search_bar(self):
        text = self.ui.SearchBar.text()
        n = 0
        results = []

        # Filter items with search term
        for i in self.ui.listAppsWidget.findItems(text, Qt.MatchContains):
            if self.current_category == "all" and (self.current_developer in i.data(Qt.UserRole)["coder"]):
                results.append(i.text())
                n += 1
            elif self.current_category == "queued" and i.data(Qt.UserRole) in gui_helpers.MULTISELECT and (self.current_developer in i.data(Qt.UserRole)["coder"]):
                results.append(i.text())
                n += 1
            elif i.data(Qt.UserRole)["category"] == self.current_category and (
                    self.current_developer in i.data(Qt.UserRole)["coder"]):
                results.append(i.text())
                n += 1
            else:
                pass

        # Get All Items
        for i in self.ui.listAppsWidget.findItems("", Qt.MatchContains):
            # Hide and unhide!
            if i.text() in results:
                i.setHidden(False)
            else:
                i.setHidden(True)
        if text == "":
            if n == 1:
                self.ui.AppsAmountLabel.setText(f"{n} App")
            else:
                self.ui.AppsAmountLabel.setText(f"{n} Apps")
        else:
            if n == 1:
                self.ui.AppsAmountLabel.setText(f"{n} Result")
            else:
                self.ui.AppsAmountLabel.setText(f"{n} Results")

    # When a different category is selected
    def changed_category(self):

        if self.ui.CategoriesComboBox.currentText() == "All Apps":
            self.current_category = "all"
        else:
            self.current_category = self.ui.CategoriesComboBox.currentText().lower()

        # hide anything from a different category
        for i in range(self.ui.listAppsWidget.count()):
            item = self.ui.listAppsWidget.item(i)
            if self.current_category == "all":
                item.setHidden(False)
            elif self.current_category == "queued" and item.data(Qt.UserRole) not in gui_helpers.MULTISELECT:
                item.setHidden(True)
            elif self.current_category != "queued" and item.data(Qt.UserRole)["category"] != self.current_category:
                item.setHidden(True)
            else:
                item.setHidden(False)

        # count apps
        self.search_bar()

    # Add remove app to multiselect
    def multi_select(self, all_select=False):
        a = self.ui.listAppsWidget.currentItem().background()
        if not all_select and self.current_app in gui_helpers.MULTISELECT:
            gui_helpers.MULTISELECT.remove(self.current_app)
            self.ui.MultiSelectToggle.setChecked(False)
            self.ui.listAppsWidget.currentItem().setBackground(QColor(0, 0, 0, 1))
            gui_helpers.QUEUE_SIGNAL_CACHE[self.current_repo['id']].pop(self.current_app["internal_name"])

        else:
            if not all_select:
                gui_helpers.MULTISELECT.append(self.current_app)
                self.ui.listAppsWidget.currentItem().setBackground(
                    QColor(gui_helpers.QUEUE_SIGNAL_COLORS["in queue"]))
                gui_helpers.QUEUE_SIGNAL_CACHE[self.current_repo['id']][self.current_app["internal_name"]] = "in queue"
            else:
                for i in range(self.ui.listAppsWidget.count()):
                    item = self.ui.listAppsWidget.item(i)
                    if item.data(Qt.UserRole) in gui_helpers.MULTISELECT:
                        item.setBackground(
                            QColor(gui_helpers.QUEUE_SIGNAL_COLORS["in queue"]))
                        gui_helpers.QUEUE_SIGNAL_CACHE[self.current_repo['id']][item.data(Qt.UserRole)["internal_name"]] = "in queue"
                        
            self.ui.MultiSelectToggle.setChecked(True)
            self.ui.AppsLibraryBox.setTitle(
                "Apps Library - Multi Selection Mode")
            self.ui.ViewMetadataBtn.setText("Download queue")
            self.ui.WiiLoadButton.setText("Send queue to Wii")
            self.ui.ClearMultiSelectButton.setDisabled(False)

        if len(gui_helpers.MULTISELECT) == 0:
            self.ui.AppsLibraryBox.setTitle("Apps Library")
            self.ui.ViewMetadataBtn.setText("Download")
            self.ui.WiiLoadButton.setText("Send to Wii")
            self.ui.ClearMultiSelectButton.setDisabled(True)
        self.search_bar()

    def clear_multi_select(self, user_request=True):
        if user_request and QMessageBox.question(self, "Clear queue", f"Clear the current download queue?\n({len(gui_helpers.MULTISELECT)} item{'s' if len(gui_helpers.MULTISELECT) > 1 else ''} present.)") == QMessageBox.StandardButton.No:
            return False
        for i in range(self.ui.listAppsWidget.count()):
            item = self.ui.listAppsWidget.item(i)
            if item.data(Qt.UserRole) in gui_helpers.MULTISELECT:
                item.setBackground(QColor(0, 0, 0, 1))
        gui_helpers.MULTISELECT.clear()
        gui_helpers.MULTISELECT_INI.clear()
        for repo in self.repos.list():
            gui_helpers.QUEUE_SIGNAL_CACHE[repo].clear()
        self.ui.MultiSelectToggle.setChecked(False)
        self.ui.AppsLibraryBox.setTitle("Apps Library")
        self.ui.ViewMetadataBtn.setText("Download")
        self.ui.WiiLoadButton.setText("Send to Wii")
        self.ui.ClearMultiSelectButton.setDisabled(True)
        self.search_bar()
        return True

    # Load developer profile
    def developer_profile(self):
        self.current_developer = self.ui.developer.text()

        self.ui.SearchBar.setText("")

        # Set category
        self.ui.CategoriesComboBox.setCurrentIndex(0)

        # Hide unneeded elements
        self.ui.ReposComboBox.setHidden(True)
        self.ui.ReturnToMainBtn.setHidden(False)
        self.ui.ViewDevWebsite.setHidden(False)

        # Set information
        self.ui.AppsLibraryBox.setTitle(
            f"Developer Profile: {self.current_developer}")

        # Set website URL
        self.ui.ViewDevWebsite.setText(f'<a href="https://oscwii.org/library?coder={self.current_developer}">'
                                       f'<span style=" text-decoration: underline; color:#0000ff;">Profile on '
                                       f'Website</span></a>')

        # hide anything from a different coder
        for i in range(self.ui.listAppsWidget.count()):
            item = self.ui.listAppsWidget.item(i)
            if item.data(Qt.UserRole)["coder"] != self.current_developer:
                item.setHidden(True)

        # count apps
        self.search_bar()

    # Return from developer view to normal view
    def return_to_all_apps_btn(self):
        # Unhide unneeded elements
        self.ui.ReturnToMainBtn.setHidden(True)
        self.ui.ViewDevWebsite.setHidden(True)
        self.ui.ReposComboBox.setHidden(False)

        # set repo title and description
        self.ui.AppsLibraryBox.setTitle("Apps Library")

        self.current_developer = ""

        # show all items
        for i in range(self.ui.listAppsWidget.count()):
            item = self.ui.listAppsWidget.item(i)
            item.setHidden(False)

        # count apps
        self.search_bar()

    # Select theme dialog
    def select_theme_action(self):
        path = resource_path("assets/themes")
        theme_files = [f for f in listdir(path) if isfile(join(path, f))]

        theme, ok = QInputDialog.getItem(self, "Experimental: Select Theme",
                                         "Choose theme to use from the list", theme_files, 0, False)
        if not ok:
            return

        with open(resource_path(f"assets/themes/{theme}"), "r") as fh:
            self.setStyleSheet(fh.read())
    # Adds all apps in repo to queue.

    def select_all_apps(self):
        if QMessageBox.question(self, "Download all apps", "You are about to add all apps to the queue. This will take up a lot of storage. Are you sure?") == QMessageBox.StandardButton.No:
            return
        gui_helpers.MULTISELECT.clear()
        for package in self.apps.get_apps():
            gui_helpers.MULTISELECT.append(package)
        self.multi_select(all_select=True)

    # load all icons from zip
    def download_app_icons(self):
        # Debug info
        original_host = self.current_repo['host']
        logging.debug("Started download of app icons")
        start_time = time.time()
        icons_zip = requests.get(
            f"https://{self.current_repo['host']}/hbb/homebrew_browser/temp_files.zip", timeout=10)
        end_time = time.time()
        logging.debug(
            f"Finished download of app icons in {str(end_time - start_time)}")

        if icons_zip.ok and (original_host == self.current_repo['host']):
            # prepare app icons dictionary
            self.icons_images = {}
            self.list_icons_images = {}
            zip_file = zipfile.ZipFile(io.BytesIO(icons_zip.content))

            # prepare icon files
            demo_icon = Image.open(resource_path(
                "assets/gui/icons/category/demo.png"))
            emulator_icon = Image.open(resource_path(
                "assets/gui/icons/category/emulator.png"))
            game_icon = Image.open(resource_path(
                "assets/gui/icons/category/game.png"))
            media_icon = Image.open(resource_path(
                "assets/gui/icons/category/media.png"))
            utility_icon = Image.open(resource_path(
                "assets/gui/icons/category/utility.png"))

            # prepare apps and their category icons dictionary
            apps_category_icons = {}
            for package in self.apps.get_apps():
                if package["category"] == "demos":
                    category_icon = demo_icon
                elif package["category"] == "emulators":
                    category_icon = emulator_icon
                elif package["category"] == "games":
                    category_icon = game_icon
                elif package["category"] == "media":
                    category_icon = media_icon
                elif package["category"] == "utilities":
                    category_icon = utility_icon
                else:
                    continue

                apps_category_icons[package["internal_name"]] = category_icon

            for name in zip_file.namelist():
                app_name = name.replace(".png", "")

                # Prepare with Pillow
                pillow_icon = Image.open(io.BytesIO(
                    zip_file.read(name))).convert("RGBA")

                # for faster unmodified icon loading, saving original image to icons images list
                # remove icc profile
                if pillow_icon.info.get('icc_profile'):
                    pillow_icon.info['icc_profile'] = ''

                # convert pillow image to bytes
                icon_bytes = io.BytesIO()
                pillow_icon.save(icon_bytes, format='PNG')

                # add to icons images list
                pixmap = QPixmap()
                pixmap.loadFromData(icon_bytes.getvalue())
                try:
                    self.icons_images[app_name] = pixmap
                except TypeError:
                    break

                # per platform sizing
                padding = 33
                category_icon_size = 24
                if self.app.style().name() == "fusion":
                    padding = int(padding * 1.5) - 4
                    category_icon_size = int(category_icon_size * 1.5)

                # Add transparent pixels on the left
                prepared_icon = Image.new(
                    'RGBA', (pillow_icon.width + padding, pillow_icon.height))
                prepared_icon.alpha_composite(pillow_icon, (padding, 0))

                # add category icon
                try:
                    category_icon = apps_category_icons[app_name].resize(
                        (category_icon_size, category_icon_size))
                except KeyError:
                    # in a scenario where an app has icon but does not exist on repo
                    continue

                # place category icon in the middle
                x, category_icon_height = category_icon.size
                x, prepared_icon_height = prepared_icon.size
                y = int((prepared_icon_height / 2) -
                        (category_icon_height / 2))
                prepared_icon.alpha_composite(category_icon, (0, y))

                # convert pillow image to bytes
                icon_bytes = io.BytesIO()
                prepared_icon.save(icon_bytes, format='PNG')

                # create list image
                pixmap = QPixmap()
                pixmap.loadFromData(icon_bytes.getvalue())
                self.list_icons_images[app_name] = pixmap

            if original_host == self.current_repo['host']:
                QtCore.QMetaObject.invokeMethod(self, 'set_app_icons')
        else:
            self.reset_status()
            logging.warning(
                "Loading of app icons for list failed, continuing without them.")

    def createINI(self):
        if self.ongoingOperations():
            self.message.show()
            return
        gui_helpers.INI_ACTION = True

        output = PKName = Author = ""
        repoSource = {}
        #appOP = "[PRIMARY]\n"
        #themeOP = "[THEMES]\n"
        if len(gui_helpers.MULTISELECT) == 0:
            QMessageBox.critical(self, "Cannot create INI",
                                 "The queue is empty, please add items first.")
            gui_helpers.INI_ACTION = False
            return
        if (QMessageBox.question(self, "Create package INI", f"This utility will assist in making a package INI for OSC-DL. (This has nothing to do with app.xml.) Continue?", QMessageBox.StandardButton.No | QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No) == QMessageBox.StandardButton.No):
            return

        for x in self.repos.list():
            repoSource[x] = []

        while 1:
            PKName, okay = QInputDialog.getText(
                self, "Creating package INI", "What should the package be named?")
            if not okay:
                gui_helpers.INI_ACTION = False
                return
            if PKName == "":
                QMessageBox.critical(
                    self, "Cannot create INI", "Please enter a package name.")
            else:
                break
        while 1:
            Author, okay = QInputDialog.getText(
                self, "Creating package INI", "Who is the author?")
            if not okay:
                gui_helpers.INI_ACTION = False
                return
            if Author == "":
                QMessageBox.critical(
                    self, "Cannot create INI", "Please enter an author name.")
            else:
                break
        while 1:
            Version, okay = QInputDialog.getText(
                self, "Creating package INI", "What version should this package be?")
            if not okay:
                gui_helpers.INI_ACTION = False
                return
            if Version == "":
                QMessageBox.critical(
                    self, "Cannot create INI", "Please enter a version number.")
            else:
                break
        save_location, _ = QFileDialog.getSaveFileName(self, 'Save Package INI',
                                                       PKName.replace(" ", "_") + ".ini")
        if save_location == "":
            gui_helpers.INI_ACTION = False
            return

        pkgtype = {"dol": "App", "elf": "App", "thm": "Theme"}

        for package in gui_helpers.MULTISELECT:
            repoSource[package["repo"]].append(package["internal_name"])

        output = f'''[META]
Title = {PKName}
Author = {Author}
Version = {Version}
#### Syntax: ####
# ('packageName' -> Download/send package ZIP),
# ('#' -> Comment), 
# ('~packageName~' -> Send DOL/ELF only)
## For arguments: ('~packageName~ = <arg1,arg2,...>')
# ('|str|' -> Install message (can be before or after download.))
#################

'''
        for element in repoSource:
            if len(repoSource[element]) > 0:
                output += f"[{element.upper()}]\n"
                output += '\n'.join(repoSource[element])

        with open(save_location, "w") as f:
            f.write(output)
        gui_helpers.INI_ACTION = False
        self.status_message(f"Saved INI file!")

    def readINI(self):
        if self.ongoingOperations():
            self.message.show()
            return
        gui_helpers.INI_ACTION = True
        if len(gui_helpers.MULTISELECT) > 0:
            if not self.clear_multi_select():
                gui_helpers.INI_ACTION = False
                return
        selectedFile, _ = QFileDialog.getOpenFileName(
            self, "Select INI file", filter="*.ini")
        if selectedFile == "":
            gui_helpers.INI_ACTION = False
            return
        self.safe_mode(True)
        config = configparser.ConfigParser(allow_no_value=True)
        config.optionxform = str
        try:
            config.read(selectedFile)
        except Exception as e:
            QMessageBox.critical(self, "INI Error",
                f"Reading failure: '{e}' ")
            self.cancelINI()
            return
            

        self.status_icon("pending")
        self.status_message(
            f"Reading '{config['META']['Title']}' by {config['META']['Author']} (version {config['META']['Version']})")
        self.ui.progressBar.setMaximum(0)
        self.ui.progressBar.setMinimum(0)
        self.ui.progressBar.setValue(0)

        for section in config.sections():
            if section == "META" or section == "DEFAULT":
                continue
            elif section.lower() != self.repo_data[-1]:
                newRepo = self.repos.get(section.lower())
                if newRepo == None:
                    QMessageBox.critical(self, "INI Error",
                                         f"Repository '{section.lower()}' does not exist.")
                    self.cancelINI()
                    return
                try:
                    self.ui.ReposComboBox.currentIndexChanged.disconnect(
                        self.changed_host)
                except Exception:
                    pass
                self.ui.ReposComboBox.setCurrentIndex(self.ui.ReposComboBox.findData(
                    [newRepo["name"], newRepo["host"], newRepo["description"], newRepo["id"]]))
                self.ui.ReposComboBox.currentIndexChanged.connect(
                    self.changed_host)
                self.changed_host()

            for package in config[section]:
                if package[0] == "#":
                    continue
                elif package[0] == package[-1] == "|":
                    # Installer Note
                    gui_helpers.MULTISELECT_INI.append(package)
                    continue
                elif package[0] == package[-1] == "~":
                    if "<" in package and ">" not in config[section][package]:
                        QMessageBox.critical(self, "INI Error",
                                             f"You may be missing a bracket (>): '{package} = {config[section][package]}'")
                        self.cancelINI()
                        return
                    # Send DOL, maybe with argements
                    if config[section][package]:
                        gui_helpers.MULTISELECT_INI.append(
                            f"~{package.replace('~','')+config[section][package]}~")
                    else:
                        gui_helpers.MULTISELECT_INI.append(
                            f"~{package.replace('~','')}~")

                    file = self.apps.get_by_name(package.replace("~", ""))
                    if file == None:
                        QMessageBox.critical(self, "INI Error",
                                             f"Package '{package}' does not exist.")
                        self.cancelINI()
                        return
                    gui_helpers.MULTISELECT.append(file)
                else:
                    file = self.apps.get_by_name(package)
                    if file == None:
                        errorNote = ""
                        if package[0] != "~" and package[-1] != "~":
                            errorNote = "\nProbably a missing tilde. (~)"
                        QMessageBox.critical(self, "INI Error",
                                             f"Package '{package}' does not exist."+errorNote)
                        self.cancelINI()
                        return

                    gui_helpers.MULTISELECT_INI.append(file["internal_name"])
                    gui_helpers.MULTISELECT.append(file)
                    #print("Extract the file on HBC, then press enter to continue...")
                    # input()

        gui_helpers.INI_ACTION = False
        gui_helpers.IS_IMPORTED_FILE = True
        if len(gui_helpers.MULTISELECT) == 0:
            QMessageBox.critical(self, "INI Error",
                f"Please include at least one package to download.")
            self.cancelINI()
            return
        self.iniMSG.show()
        '''
                index = self.ui.ReposComboBox.currentIndex()
        self.repo_data = self.ui.ReposComboBox.itemData(index, Qt.UserRole)
        '''

    def cancelINI(self):
        self.status_message("Cancelled download")
        self.status_icon("online")
        self.ui.progressBar.setMaximum(100)
        self.clear_multi_select(user_request=False)
        gui_helpers.IS_IMPORTED_FILE = False
        gui_helpers.INI_ACTION = False
        self.safe_mode(False)

    @QtCore.Slot()
    def set_app_icons(self):
        original_host = self.current_repo['host']
        for i in range(self.ui.listAppsWidget.count()):
            item = self.ui.listAppsWidget.item(i)
            if original_host == self.current_repo['host']:
                try:
                    item.setIcon(self.list_icons_images[item.data(
                        Qt.UserRole)["internal_name"]])
                except KeyError:
                    self.reset_status()
                    return
        # set size of icon to 171x64
        self.ui.listAppsWidget.setIconSize(QSize(171, 32))
        # complete loading
        self.reset_status()

    def ongoingOperations(self):
        return gui_helpers.CURRENTLY_SENDING or gui_helpers.IN_DOWNLOAD_DIALOG

    #
    # Event overrides
    #
    def event(self, event):
        # Cancel status tip update events
        if event.type() == QEvent.StatusTip:
            event.ignore()
            return True

        # For debugging: print most events
        # event_type = QEvent.type(event)
        # event_type_name = QEvent.Type(event_type).name
        # if event_type_name not in ["HoverMove", "Paint", "UpdateRequest"]:
        #     print(f"Event type: {event_type_name}")
        return super().event(event)

    def closeEvent(self, closeEvent):
        if self.ongoingOperations():
            # QMessageBox.warning is modal, this is not.
            self.message.show()
            closeEvent.ignore()
        else:
            closeEvent.accept()


if __name__ == "__main__":
    print("!!!!!\n"
          "The entry point for OSCDL has been changed.\n"
          "To launch OSCDL, run \"oscdl.py\"\n"
          "!!!!!")
