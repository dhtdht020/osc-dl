import io
import threading
import time
import zipfile
from datetime import datetime

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
from PySide6.QtCore import Qt, QSize, QEvent
from PySide6.QtGui import QIcon, QColor, QPixmap, QMovie
from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QMessageBox, \
    QListWidgetItem, QFileDialog

import gui.ui_united
import api
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

    def __init__(self, app=None, splash=None, test_mode=False):
        super(MainWindow, self).__init__()
        self.apps = None
        self.ui = gui.ui_united.Ui_MainWindow()
        self.ui.setupUi(self)

        self.message = QMessageBox(self)
        self.message.setIcon(QMessageBox.Warning)
        self.message.setWindowTitle("Operation in progress")
        self.message.setText("Please wait for the operation to finish.")
        self.message.setModal(True)

        self.app = app
        self.splash = splash
        self.test_mode = test_mode

        # Set title and icon of window
        self.setWindowTitle(f"Open Shop Channel Downloader v{updater.current_version()} - Library")
        app_icon = QIcon(resource_path("assets/gui/windowicon.png"))
        self.setWindowIcon(app_icon)

        self.current_app = None
        self.current_category = "all"
        self.current_developer = ""
        self.icons_images = None

        # Set GUI Icons

        # ABOUT
        self.ui.actionAbout_OSC_DL.setIcon(QIcon(resource_path("assets/gui/icons/oscdl-icon.png")))
        self.ui.actionIcons_provided_by.setIcon(QIcon(resource_path("assets/gui/icons/iconsprovider.png")))
        # CLIENTS
        self.ui.actionCheck_for_Updates.setIcon(QIcon(resource_path("assets/gui/icons/check-for-updates.png")))
        self.ui.actionRefresh.setIcon(QIcon(resource_path("assets/gui/icons/refresh.png")))
        # OPTIONS
        self.ui.actionCopy_Direct_Link.setIcon(QIcon(resource_path("assets/gui/icons/copy-link.png")))

        # CATEGORIES COMBOBOX
        self.ui.CategoriesComboBox.setItemIcon(1, QIcon(resource_path("assets/gui/icons/category/utility.png")))
        self.ui.CategoriesComboBox.setItemIcon(2, QIcon(resource_path("assets/gui/icons/category/emulator.png")))
        self.ui.CategoriesComboBox.setItemIcon(3, QIcon(resource_path("assets/gui/icons/category/game.png")))
        self.ui.CategoriesComboBox.setItemIcon(4, QIcon(resource_path("assets/gui/icons/category/media.png")))
        self.ui.CategoriesComboBox.setItemIcon(5, QIcon(resource_path("assets/gui/icons/category/demo.png")))

        # ACTIONS
        self.ui.actionFilter_by_Developer.setIcon(QIcon(resource_path("assets/gui/icons/filter.png")))
        self.ui.developer.addAction(self.ui.actionFilter_by_Developer, QLineEdit.TrailingPosition)

        # create spinner movie
        self.spinner = QMovie(resource_path("assets/gui/icons/spinner.gif"))
        self.spinner.setScaledSize(QSize(32, 32))
        self.spinner.start()

        # set initial status icon
        self.set_status_icon("online")

        self.ui.ReposComboBox.setPlaceholderText("Open Shop Channel")
        self.ui.WarningIcon.setPixmap(QPixmap(resource_path("assets/gui/icons/warning.png")))
        self.ui.WarningIcon.setScaledContents(True)

        self.ui.ResetFiltersBtn.setIcon(QIcon(resource_path("assets/gui/icons/close.png")))

        self.check_for_updates_action(silent=True)

        self.populate()
        self.selection_changed()
        self.ui.progressBar.setHidden(False)
        self.ui.ResetFiltersBtn.setHidden(True)
        self.ui.statusBar.addPermanentWidget(self.ui.progressBar)
        self.ui.statusBar.addPermanentWidget(self.ui.statusIcon)

        # Close splash
        splash.finish(self)

    def about_dialog(self):
        QMessageBox.about(self, f"About OSCDL",
                          f"<b>Open Shop Channel Downloader v{updater.current_version()}</b><br>"
                          f"by dhtdht020<br><br>"
                          f"<a href=\"https://github.com/dhtdht020/osc-dl\">https://github.com/dhtdht020/osc-dl</a><br>"
                          f"Many icons provided by <a href=\"https://icons8.com/\">icons8.com</a><br><br>"
                          f"Using Qt {QtCore.qVersion()}<br>"
                          f"Using Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")

    def set_splash_status(self, text: str) -> None:
        """Updates the splash screen with the provided text if the splash is visible."""
        if self.splash and not self.splash.isHidden():
            self.splash.showMessage(text, color=QColor("White"))

    def set_status_message(self, message: str) -> None:
        """Displays a status message in the bottom status bar of the UI."""
        self.ui.statusBar.showMessage(message)

    def set_status_icon(self, icon: str) -> None:
        """Updates the status icon displayed in the UI status bar."""
        self.ui.statusIcon.setPixmap(QPixmap(resource_path(f"assets/gui/icons/status/{icon}.png")))

    # populate UI elements
    def populate(self):
        self.set_splash_status("Loading contents..")
        self.ui.actionAbout_OSC_DL.setText(f"About OSCDL v{updater.current_version()} by dhtdht020")
        self.populate_list()
        self.assign_initial_actions()

    def assign_initial_actions(self):
        self.set_splash_status("Finishing (1/2)..")

        # Connect signals
        # Buttons

        # Copy app download link
        self.ui.actionCopy_Direct_Link.triggered.connect(
            lambda: (QApplication.clipboard().setText(self.current_app["url"]["zip"]),
                     self.set_status_message(f"Copied the download link for {self.current_app['name']}\" to clipboard")))

        self.ui.ViewMetadataBtn.clicked.connect(self.download_app)
        self.ui.WiiLoadButton.clicked.connect(self.wiiload_button)
        self.ui.ResetFiltersBtn.clicked.connect(self.reset_filters_btn)

        # Search Bar
        self.ui.SearchBar.textChanged.connect(self.search_bar)

        # Others
        self.ui.CategoriesComboBox.currentIndexChanged.connect(self.changed_category)
        self.ui.listAppsWidget.currentItemChanged.connect(self.selection_changed)
        self.ui.actionFilter_by_Developer.triggered.connect(self.filter_by_developer)

        # Actions
        # -- About
        self.ui.actionAbout_OSC_DL.triggered.connect(self.about_dialog)
        # -- Options
        self.ui.actionCheck_for_Updates.triggered.connect(partial(self.check_for_updates_action))
        self.ui.actionRefresh.triggered.connect(partial(self.repopulate))

    # When user selects a different homebrew from the list
    def selection_changed(self):
        self.set_splash_status("Finishing (2/2) - Loading first app..")

        try:
            self.current_app = self.ui.listAppsWidget.currentItem().data(Qt.UserRole)
            app_name = self.current_app["slug"]
        except Exception:
            app_name = None
        if app_name is not None:
            # Set loading animation
            self.ui.HomebrewIconLabel.setMovie(self.spinner)

            # Clear supported controllers listview:
            self.ui.SupportedControllersListWidget.clear()

            # Enable Send to Wii button
            self.ui.WiiLoadButton.setEnabled(True)
            self.ui.WiiLoadButton.setText("Send to Wii")

            # -- Get actual metadata
            # App Name
            self.ui.appname.setText(self.current_app["name"])
            self.ui.SelectionInfoBox.setTitle("Information: " + self.current_app["name"])
            self.ui.label_displayname.setText(self.current_app["name"])

            # File Size
            try:
                extracted = utils.file_size(self.current_app['file_size']['zip_uncompressed'])
                compressed = utils.file_size(self.current_app["file_size"]["zip_compressed"])
                self.ui.filesize.setText(f"{compressed} / {extracted}")
                self.ui.filesize.setToolTip(f"Compressed Download: {compressed}\nExtracted Size: {extracted}")
            except KeyError:
                self.ui.filesize.setText("Unknown")

            # Category
            self.ui.HomebrewCategoryLabel.setText(metadata.category_display_name(self.current_app["category"]))

            # Release Date
            if self.current_app["release_date"] == 0:
                release_date_text = "Unknown"
            else:
                if self.current_app["release_date"] < 0:
                    release_date_text = "Before 1970?? Crazy. (Bug)"
                else:
                    release_date_text = datetime.fromtimestamp(int(self.current_app["release_date"])).strftime('%B %e, %Y')
            self.ui.releasedate.setText(release_date_text)

            #
            # Peripherals
            #

            item = QListWidgetItem()
            item.setText("Supported Peripherals")
            item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
            self.ui.SupportedControllersListWidget.addItem(item)

            peripherals = self.current_app["peripherals"]
            # Add icons for Wii Remotes
            if peripherals.count("Wii Remote") > 1:
                item = QListWidgetItem()
                item.setText(f"{str(peripherals.count('Wii Remote'))} Wii Remotes")
                item.setIcon(QIcon(
                    resource_path(f"assets/gui/icons/controllers/{str(peripherals.count('Wii Remote'))}WiiRemote.png")))
                item.setToolTip(f"This app supports up to {str(peripherals.count('Wii Remote'))} Wii Remotes.")
                self.ui.SupportedControllersListWidget.addItem(item)
            elif peripherals.count('Wii Remote') == 1:
                item = QListWidgetItem()
                item.setText(f"1 Wii Remote")
                item.setIcon(QIcon(resource_path(f"assets/gui/icons/controllers/1WiiRemote.png")))
                item.setToolTip("This app supports a single Wii Remote.")
                self.ui.SupportedControllersListWidget.addItem(item)
            if "Nunchuk" in peripherals:
                item = QListWidgetItem()
                item.setText(f"Nunchuk")
                item.setIcon(QIcon(resource_path(f"assets/gui/icons/controllers/Nunchuk.png")))
                item.setToolTip("This app can be used with a Nunchuk.")
                self.ui.SupportedControllersListWidget.addItem(item)
            if "Classic Controller" in peripherals:
                item = QListWidgetItem()
                item.setText(f"Classic Controller")
                item.setIcon(QIcon(resource_path(f"assets/gui/icons/controllers/ClassicController.png")))
                item.setToolTip("This app can be used with a Classic Controller.")
                self.ui.SupportedControllersListWidget.addItem(item)
            if "GameCube Controller" in peripherals:
                item = QListWidgetItem()
                item.setText(f"GameCube Controller")
                item.setIcon(QIcon(resource_path(f"assets/gui/icons/controllers/GamecubeController.png")))
                item.setToolTip("This app can be used with a Gamecube Controller.")
                self.ui.SupportedControllersListWidget.addItem(item)
            if "Wii Zapper" in peripherals:
                item = QListWidgetItem()
                item.setText(f"Wii Zapper")
                item.setIcon(QIcon(resource_path(f"assets/gui/icons/controllers/WiiZapper.png")))
                item.setToolTip("This app can be used with a Wii Zapper.")
                self.ui.SupportedControllersListWidget.addItem(item)
            if "USB Keyboard" in peripherals:
                item = QListWidgetItem()
                item.setText(f"USB Keyboard")
                item.setIcon(QIcon(resource_path(f"assets/gui/icons/controllers/USBKeyboard.png")))
                item.setToolTip("This app can be used with a USB Keyboard.")
                self.ui.SupportedControllersListWidget.addItem(item)
            if "SDHC" in peripherals:
                item = QListWidgetItem()
                item.setText(f"SDHC Card")
                item.setIcon(QIcon(resource_path(f"assets/gui/icons/controllers/SDHC.png")))
                item.setToolTip("This app is confirmed to support SDHC cards.")
                self.ui.SupportedControllersListWidget.addItem(item)

            # Supported platforms
            item = QListWidgetItem()
            item.setText("Supported Platforms")
            item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
            self.ui.SupportedControllersListWidget.addItem(item)

            supported_platforms = self.current_app["supported_platforms"]
            if "wii" in supported_platforms:
                item = QListWidgetItem()
                item.setText(f"Wii")
                item.setIcon(QIcon(resource_path(f"assets/gui/icons/platforms/wii.png")))
                self.ui.SupportedControllersListWidget.addItem(item)
            if "vwii" in supported_platforms:
                item = QListWidgetItem()
                item.setText(f"Wii U (Virtual Wii)")
                item.setIcon(QIcon(resource_path(f"assets/gui/icons/platforms/vwii.png")))
                self.ui.SupportedControllersListWidget.addItem(item)
            if "wii_mini" in supported_platforms:
                item = QListWidgetItem()
                item.setText(f"Wii Mini")
                item.setIcon(QIcon(resource_path(f"assets/gui/icons/platforms/wii_mini.png")))
                self.ui.SupportedControllersListWidget.addItem(item)

            # Version
            self.ui.version.setText(self.current_app["version"])

            # Coder
            self.ui.developer.setText(self.current_app["author"])

            # Short Description
            self.ui.label_description.setToolTip(None)
            if self.current_app["description"]["short"] == "":
                self.ui.label_description.setText("No description specified.")
            else:
                self.ui.label_description.setText(self.current_app["description"]["short"])
                if len(self.current_app["description"]["short"]) >= 40:
                    self.ui.label_description.setToolTip(self.current_app["description"]["short"])

            # Long Description
            self.ui.longDescriptionBrowser.setText(self.current_app["description"]["long"])

            # Warning Banner
            self.ui.WarningFrame.setVisible("writes_to_nand" in self.current_app["flags"])

        self.ui.progressBar.setValue(0)
        self.repaint()
        # Load icon
        t = threading.Thread(target=self.load_icon, args=[app_name], daemon=True)
        t.start()

    # TODO FULL REWRITE
    def download_app(self, extract_root=False):
        gui_helpers.IN_DOWNLOAD_DIALOG = True
        self.set_status_message(f"Downloading {self.current_app['name']} from Open Shop Channel..")
        self.set_status_icon("pending")
        self.ui.progressBar.setMaximum(0)

        if self.sender():
            object_name = self.sender().objectName()
        else:
            object_name = None

        # determine if should ask for path
        if (object_name != "WiiLoadButton") and not self.test_mode:
            dialog = DownloadLocationDialog(self.current_app, parent=self)
            status = dialog.exec()

            if status:
                logging.debug(f"Selected drive: {dialog.selection}")
                if dialog.selection == "browse":
                    save_location, _ = QFileDialog.getSaveFileName(self, 'Save Application',
                                                                   self.current_app["slug"] + ".zip")
                else:
                    if not dialog.selection["appsdir"]:
                        try:
                            os.mkdir(dialog.selection["drive"].rootPath() + "/apps")
                        except PermissionError:
                            QMessageBox.critical(self, "Permission Error",
                                                 "Could not create the apps directory on the selected device.")
                            return
                    save_location = dialog.selection["drive"].rootPath() + "/apps/" + self.current_app[
                        "slug"] + ".zip"
                    extract_root = True
            else:
                save_location = ''
        else:
            # create output dir
            if os.name == 'nt':
                dir_path = '%s\\OSCDL\\' % os.environ['APPDATA']
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                save_location = f'%s{self.current_app["slug"]}' % dir_path
            else:
                save_location = f"{self.current_app['slug']}.zip"
        self.ui.progressBar.setValue(0)
        if save_location:
            # stream file, so we can iterate
            response = requests.get(self.current_app["url"]["zip"], stream=True)
            total_size = int(response.headers.get('content-length', 0))

            # set progress bar
            self.ui.progressBar.setMaximum(total_size)
            block_size = 1024
            if response.status_code == 200:
                self.safe_mode(True)
                self.set_status_icon("download")

                with open(save_location, "wb") as app_data_file:
                    for data in response.iter_content(block_size):
                        self.ui.progressBar.setValue(self.ui.progressBar.value() + 1024)
                        self.set_status_message(
                            f"Downloading {self.current_app['name']} from Open Shop Channel.. ({utils.file_size(self.ui.progressBar.value())}/{utils.file_size(total_size)})")
                        try:
                            self.app.processEvents()
                        except NameError:
                            pass
                        app_data_file.write(data)

                if extract_root:
                    self.set_status_message("Extracting..")

                    with zipfile.ZipFile(save_location, 'r') as zip_file:
                        # unzip to root_path
                        root_path = utils.get_mount_point(save_location)
                        zip_file.extractall(root_path)

                    os.remove(save_location)

            self.ui.progressBar.setValue(total_size)
            if object_name != "WiiLoadButton":
                self.safe_mode(False)
            self.set_status_message(f"Download of \"{self.current_app['name']}\" has completed successfully")
            self.set_status_icon("online")
            gui_helpers.IN_DOWNLOAD_DIALOG = False
            return save_location
        else:
            self.ui.progressBar.setMaximum(100)
            self.ui.progressBar.setValue(0)
            self.safe_mode(False)
            self.set_status_message("Cancelled Download")
            self.set_status_icon("online")
            gui_helpers.IN_DOWNLOAD_DIALOG = False

    def reset_status(self):
        if not gui_helpers.CURRENTLY_SENDING and not gui_helpers.IN_DOWNLOAD_DIALOG:
            self.ui.progressBar.setMaximum(100)
            self.set_status_message("Ready to download")
            self.set_status_icon("online")

    def safe_mode(self, state: bool):
        """
        Disable all widgets that could interrupt sensitive processes
        :param state: bool
        """
        self.ui.ViewMetadataBtn.setDisabled(state)
        self.ui.WiiLoadButton.setDisabled(state)
        self.ui.ReposComboBox.setDisabled(state)
        self.ui.listAppsWidget.setDisabled(state)

    def wiiload_button(self):
        if not utils.app_has_extra_directories(self.current_app) and QMessageBox.question(self, "Send to Wii", "This app contains extra files and directories that may need configuration. Send anyway?") == QMessageBox.StandardButton.No:
            return

        dialog = WiiLoadDialog(self.current_app, parent=self)
        status = dialog.exec()
        if not status:
            return
        gui_helpers.CURRENTLY_SENDING = True

        self.set_status_message("Downloading " + self.current_app["name"] + " from Open Shop Channel..")
        self.ui.progressBar.setValue(25)

        # get app
        path_to_app = self.download_app()
        self.ui.progressBar.setMaximum(100)

        with open(path_to_app, 'rb') as f:
            content = f.read()

        zipped_app = io.BytesIO(content)
        zip_buf = io.BytesIO()

        # Our zip file should only contain one directory with the app data in it,
        # but the downloaded file contains an apps/ directory. We're removing that here.
        wiiload.organize_zip(zipped_app, zip_buf)

        # preparing
        prep = wiiload.prepare(zip_buf)

        file_size = prep[0]
        compressed_size = prep[1]
        chunks = prep[2]
        c_data = prep[3]

        # connecting
        self.set_status_message('Connecting to the HBC...')
        self.set_status_icon('connecting_hbc')
        self.ui.progressBar.setValue(50)

        try:
            if dialog.modeSelect == 0:  # TCP/IP
                conn = wiiload.connect(dialog.address)
            else:  # USBGecko
                conn = serial.Serial()
                conn.inter_byte_timeout = 1.0
                conn.port = dialog.address
                func_timeout.func_timeout(1, conn.open)  # Timeout: 1 sec, function: conn.open()
                conn.send = conn.write  # Keeps the wiiload logic the same
        except (func_timeout.exceptions.FunctionTimedOut, Exception) as e:
            self.set_status_icon('sad')
            conn_type = ["IP address", "connection"]
            logging.error(
                f'Error while connecting to the HBC. Please check the {conn_type[dialog.modeSelect]} and try again.')
            QMessageBox.warning(self, 'Connection error',
                                f'Error while connecting to the HBC. Please check the {conn_type[dialog.modeSelect]} and try again.')
            print(f'WiiLoad: {e}')
            self.ui.progressBar.setValue(0)
            self.set_status_message('Error: Could not connect to the Homebrew Channel. :(')
            self.set_status_icon('online')

            # delete application zip file
            os.remove(path_to_app)
            gui_helpers.CURRENTLY_SENDING = False
            self.safe_mode(False)
            return

        wiiload.handshake(conn, compressed_size, file_size)

        # Sending file
        self.set_status_message('Sending app...')
        self.set_status_icon('sending')

        chunk_num = 1
        if dialog.modeSelect == 0:  # TCP/IP
            for chunk in chunks:
                try:
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
                    self.set_status_message('Error: Could not connect to the Homebrew Channel. :(')

                    # delete application zip file
                    os.remove(path_to_app)
                    gui_helpers.CURRENTLY_SENDING = False
                    self.safe_mode(False)
                    return
        # USBGecko
        else:
            # conn.send is blocking, used thread to avoid.
            t = threading.Thread(target=self.send_gecko, daemon=True, args=[c_data, conn, path_to_app])
            t.start()
            self.ui.progressBar.setMaximum(0)
            while t.is_alive():
                try:
                    self.app.processEvents()
                except NameError:
                    pass
            t.join()
            if not gui_helpers.DATASENT:
                gui_helpers.CURRENTLY_SENDING = False
                self.safe_mode(False)
                return
            self.ui.progressBar.setMaximum(100)
            self.ui.progressBar.setValue(100)

        file_name = f'{self.current_app["slug"]}.zip'
        conn.send(bytes(file_name, 'utf-8') + b'\x00')

        # delete application zip file
        os.remove(path_to_app)

        if dialog.modeSelect == 1:
            conn.flush()
            conn.close()

        self.ui.progressBar.setValue(100)
        self.set_status_message('App transmitted!')
        self.set_status_icon('online')
        logging.info(f"App transmitted to HBC at {dialog.address}")
        gui_helpers.CURRENTLY_SENDING = False
        self.safe_mode(False)

    def send_gecko(self, c_data, conn, path_to_app):
        try:
            conn.send(c_data)
        except Exception as e:
            logging.error('Error while connecting to the HBC. Close any dialogs on HBC and try again.')
            QMessageBox.warning(self, 'Connection error',
                                'Error while connecting to the HBC. Close any dialogs on HBC and try again.')
            print(f'WiiLoad: {e}')
            self.ui.progressBar.setValue(0)
            self.set_status_message('Error: Could not connect to the Homebrew Channel. :(')

            # delete application zip file
            os.remove(path_to_app)
            conn.close()
            gui_helpers.DATASENT = False
            return
        gui_helpers.DATASENT = True

    def repopulate(self):
        # Make sure everything is hidden / shown
        self.ui.ResetFiltersBtn.setHidden(True)
        self.ui.CategoriesComboBox.setHidden(False)
        self.ui.SearchBar.setText("")

        self.set_status_message("Reloading list..")
        self.set_status_icon("loading")
        try:
            self.ui.CategoriesComboBox.currentIndexChanged.disconnect(self.changed_category)
        except Exception:
            pass
        self.ui.CategoriesComboBox.setCurrentIndex(0)
        self.ui.listAppsWidget.clear()
        self.populate_list()
        self.ui.CategoriesComboBox.currentIndexChanged.connect(self.changed_category)

    def populate_list(self):
        try:
            self.set_splash_status("Connecting to server..")

            # Set default icon size
            self.ui.listAppsWidget.setIconSize(QSize(-1, -1))

            # Get apps json
            self.apps = api.Applications()
            i = 0

            for app in self.apps.get_apps():
                try:
                    # let's check if the app celebrates its birthday today
                    birthday = utils.app_birthday_string(app)
                    if birthday:
                        birthday = f" [{birthday}]"
                    else:
                        birthday = ""

                    # add entry to applications list
                    self.ui.listAppsWidget.addItem(f"{app['name']}{birthday}\n"
                                                   f"{utils.file_size(app['file_size']['zip_uncompressed'])} | "
                                                   f"{app['version']} | "
                                                   f"{app['author']} | "
                                                   f"{app['description']['short']}")
                    list_item = self.ui.listAppsWidget.item(i)

                    list_item.setData(Qt.UserRole, app)
                    # Set category icon
                    category = app["category"]

                    if category == "utilities":
                        list_item.setIcon(QIcon(resource_path("assets/gui/icons/category/utility.png")))
                    elif category == "games":
                        list_item.setIcon(QIcon(resource_path("assets/gui/icons/category/game.png")))
                    elif category == "emulators":
                        list_item.setIcon(QIcon(resource_path("assets/gui/icons/category/emulator.png")))
                    elif category == "media":
                        list_item.setIcon(QIcon(resource_path("assets/gui/icons/category/media.png")))
                    elif category == "demos":
                        list_item.setIcon(QIcon(resource_path("assets/gui/icons/category/demo.png")))
                    self.set_splash_status(f"Loaded {i} apps..")
                    i += 1
                except IndexError:
                    pass
            self.ui.listAppsWidget.sortItems(Qt.AscendingOrder)
            self.ui.listAppsWidget.setCurrentRow(0)
            self.ui.AppsAmountLabel.setText(str(self.ui.listAppsWidget.count()) + " Apps")

        except Exception as e:
            QMessageBox.critical(self, 'OSCDL: Critical Network Error',
                                 'Could not connect to the Open Shop Channel server.\n'
                                 'Cannot continue. :(\n'
                                 'Please check your internet connection, or report this incident.\n\n'
                                 f'{e}')
            sys.exit(1)

        # load app icons
        if not gui_helpers.CURRENTLY_SENDING and not gui_helpers.IN_DOWNLOAD_DIALOG:
            self.set_status_message("Loading app icons from server..")
            self.ui.progressBar.setMaximum(0)
        t = threading.Thread(target=self.download_app_icons, daemon=True)
        t.start()

    #
    # Actions
    #
    # Check for updates dialog
    def check_for_updates_action(self, silent=False):
        self.set_splash_status("Checking for updates..")
        if not silent:
            self.set_status_message("Checking for updates.. This will take a few moments..")

        try:
            latest = updater.latest_version()
        except:
            if not silent:
                QMessageBox.critical(self, 'OSCDL updater', 'An error occurred while checking for updates.\n'
                                                            'Please manually search for a new release!')
            return

        if updater.check_update(latest) is True:
            self.set_status_message("New version available! (" + latest['tag_name'] + ") OSCDL is out of date.")
            body = latest['body'].replace("![image]", "")
            QMessageBox.warning(self, 'OSCDL is out of date - New release available!',
                                f"<hr><center><b style=\"font-size: 20px\">New Update Available</b></center><hr>"
                                f"<b style=\"font-size: 20px\">{latest['name']}</b><br>"
                                f"<b>Released on {datetime.strptime(latest['published_at'], '%Y-%m-%dT%H:%M:%SZ')}</b><br><br>"
                                f"<a href='https://github.com/dhtdht020/osc-dl'>View on GitHub</a><br>"
                                f"{markdown.markdown((body[:600] + '... <br><br><br><i>Learn more on GitHub</i>') if len(body) > 600 else body)}<hr>"
                                f"Please go to the <a href='https://github.com/dhtdht020/osc-dl'>GitHub page</a> and obtain the latest release.<br>"
                                f"Newest detected version: {latest['tag_name']}")
        else:
            if not silent:
                self.set_status_message("OSCDL is up to date!")
                QMessageBox.information(self, 'OSCDL is up to date', 'You are running the latest version of OSCDL!\n')

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
            if self.current_app["slug"] == app_name:
                data = metadata.icon(self.current_app)

                # Loads image
                image = QtGui.QImage()
                image.loadFromData(data)

                # Adds image to label
                # Once again check if still relevant
                if self.current_app["slug"] == app_name:
                    self.IconSignal.emit(QPixmap(image))
                    self.ui.HomebrewIconLabel.show()

    def search_bar(self):
        text = self.ui.SearchBar.text()
        n = 0
        results = []

        # Filter items with search term
        for i in self.ui.listAppsWidget.findItems(text, Qt.MatchContains):
            if self.current_category == "all" and (self.current_developer in i.data(Qt.UserRole)["author"]):
                results.append(i.text())
                n += 1
            elif i.data(Qt.UserRole)["category"] == self.current_category and (
                    self.current_developer in i.data(Qt.UserRole)["author"]):
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
            elif item.data(Qt.UserRole)["category"] != self.current_category:
                item.setHidden(True)
            else:
                item.setHidden(False)

        # count apps
        self.search_bar()

    def filter_by_developer(self):
        """
        Filter by developer
        """
        self.current_developer = self.ui.developer.text()

        # Set category and clear search bar, to display all apps
        self.ui.CategoriesComboBox.setCurrentIndex(0)
        self.ui.SearchBar.setText("")
        self.search_bar()

        self.ui.ResetFiltersBtn.setHidden(False)
        # hide anything from a different coder
        for i in range(self.ui.listAppsWidget.count()):
            item = self.ui.listAppsWidget.item(i)
            if item.data(Qt.UserRole)["author"] != self.current_developer:
                item.setHidden(True)


    # Return from filtering by developer to normal view
    def reset_filters_btn(self):
        # Unhide unneeded elements
        self.ui.ResetFiltersBtn.setHidden(True)

        self.current_developer = ""

        # show all items
        for i in range(self.ui.listAppsWidget.count()):
            item = self.ui.listAppsWidget.item(i)
            item.setHidden(False)

        # count apps
        self.search_bar()

    # load all icons from zip
    def download_app_icons(self):
        # Debug info
        logging.debug("Started download of app icons")
        start_time = time.time()
        icons_zip = requests.get(f"https://hbb1.oscwii.org/hbb/homebrew_browser/temp_files.zip", timeout=10)
        end_time = time.time()
        logging.debug(f"Finished download of app icons in {str(end_time - start_time)}")

        if icons_zip.ok:
            # prepare app icons dictionary
            self.icons_images = {}
            self.list_icons_images = {}
            zip_file = zipfile.ZipFile(io.BytesIO(icons_zip.content))

            # prepare icon files
            demo_icon = Image.open(resource_path("assets/gui/icons/category/demo.png"))
            emulator_icon = Image.open(resource_path("assets/gui/icons/category/emulator.png"))
            game_icon = Image.open(resource_path("assets/gui/icons/category/game.png"))
            media_icon = Image.open(resource_path("assets/gui/icons/category/media.png"))
            utility_icon = Image.open(resource_path("assets/gui/icons/category/utility.png"))
            nothing_icon = Image.open(resource_path("assets/gui/icons/category/nothing.png"))

            # prepare apps and their category icons dictionary
            apps_category_icons = {}
            for app in self.apps.get_apps():
                if app["category"] == "demos":
                    category_icon = demo_icon
                elif app["category"] == "emulators":
                    category_icon = emulator_icon
                elif app["category"] == "games":
                    category_icon = game_icon
                elif app["category"] == "media":
                    category_icon = media_icon
                elif app["category"] == "utilities":
                    category_icon = utility_icon
                else:
                    category_icon = nothing_icon

                apps_category_icons[app["slug"]] = category_icon

            for name in zip_file.namelist():
                app_name = name.replace(".png", "")

                # Prepare with Pillow
                pillow_icon = Image.open(io.BytesIO(zip_file.read(name))).convert("RGBA")

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
                prepared_icon = Image.new('RGBA', (pillow_icon.width + padding, pillow_icon.height))
                prepared_icon.alpha_composite(pillow_icon, (padding, 0))

                # add category icon
                try:
                    category_icon = apps_category_icons[app_name].resize((category_icon_size, category_icon_size))
                except KeyError:
                    # in a scenario where an app has icon but does not exist on repo
                    continue

                # place category icon in the middle
                x, category_icon_height = category_icon.size
                x, prepared_icon_height = prepared_icon.size
                y = int((prepared_icon_height / 2) - (category_icon_height / 2))
                prepared_icon.alpha_composite(category_icon, (0, y))

                # convert pillow image to bytes
                icon_bytes = io.BytesIO()
                prepared_icon.save(icon_bytes, format='PNG')

                # create list image
                pixmap = QPixmap()
                pixmap.loadFromData(icon_bytes.getvalue())
                self.list_icons_images[app_name] = pixmap

            QtCore.QMetaObject.invokeMethod(self, 'set_app_icons')
        else:
            self.reset_status()
            logging.warning("Loading of app icons for list failed, continuing without them.")

    @QtCore.Slot()
    def set_app_icons(self):
        for i in range(self.ui.listAppsWidget.count()):
            item = self.ui.listAppsWidget.item(i)
            try:
                item.setIcon(self.list_icons_images[item.data(Qt.UserRole)["slug"]])
            except KeyError:
                self.reset_status()
                return
        # set size of icon to 171x64
        self.ui.listAppsWidget.setIconSize(QSize(171, 32))
        # complete loading
        self.reset_status()

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
        if gui_helpers.CURRENTLY_SENDING or gui_helpers.IN_DOWNLOAD_DIALOG:
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
