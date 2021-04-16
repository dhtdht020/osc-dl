import io
from datetime import datetime
from os import listdir
from os.path import isfile, join

import yaml
import os
import socket
import sys
from contextlib import redirect_stdout

import logging  # for logs
from functools import partial

import requests
from PySide2 import QtGui
from PySide2.QtCore import Qt, QObject
from PySide2.QtGui import QIcon, QColor
from PySide2.QtWidgets import QApplication, QMainWindow, QInputDialog, QLineEdit, QMessageBox, QSplashScreen, \
    QListWidgetItem, QFileDialog

import download
import gui.ui_united
import metadata
import updater
import utils
import wiiload


VERSION = updater.current_version()
BRANCH = updater.get_branch()
if BRANCH == "Stable":
    DISPLAY_VERSION = VERSION
else:
    DISPLAY_VERSION = VERSION + " " + BRANCH

HOST = "hbb1.oscwii.org"
HOST_NAME = "primary"


# Get resource when frozen with PyInstaller
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# Actions to perform only when the program is frozen:
if updater.is_frozen():
    logging.basicConfig(level=logging.DEBUG)
    logging.info(f"Open Shop Channel Downloader v{updater.current_version()} {updater.get_branch()}")
    logging.info(f"OSCDL, Open Source Software by dhtdht020. https://github.com/dhtdht020.\n\n\n")


# G U I
class MainWindow(gui.ui_united.Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = gui.ui_united.Ui_MainWindow()
        self.ui.setupUi(self)

        # Set title and icon of window
        self.setWindowTitle(f"Open Shop Channel Downloader v{DISPLAY_VERSION} - Library")
        app_icon = QIcon(resource_path("assets/gui/windowicon.png"))
        self.setWindowIcon(app_icon)

        # Set GUI Icons

        # ABOUT
        self.ui.actionAbout_OSC_DL.setIcon(QIcon(resource_path("assets/gui/icons/about-open-version.png")))
        # CLIENTS
        self.ui.menuHomebrew_Browser.setIcon(QIcon(resource_path("assets/gui/icons/hbb-icon.png")))
        self.ui.menuOpen_Shop_Channel_DL.setIcon(QIcon(resource_path("assets/gui/icons/oscdl-icon.png")))
        self.ui.actionDownload_HBB_Client_Latest.setIcon(QIcon(resource_path("assets/gui/icons/download.png")))
        self.ui.actionCheck_for_Updates.setIcon(QIcon(resource_path("assets/gui/icons/check-for-updates.png")))
        self.ui.actionRefresh.setIcon(QIcon(resource_path("assets/gui/icons/refresh.png")))
        # DEBUG
        self.ui.actionEnable_Log_File.setIcon(QIcon(resource_path("assets/gui/icons/enable-log.png")))
        self.ui.actionClear_Log.setIcon(QIcon(resource_path("assets/gui/icons/clear-log.png")))
        self.ui.actionClose_the_shop.setIcon(QIcon(resource_path("assets/gui/icons/close-shop.png")))
        self.ui.menuExperimental.setIcon(QIcon(resource_path("assets/gui/icons/experimental.png")))
        self.ui.actionSelect_Theme.setIcon(QIcon(resource_path("assets/gui/icons/theme.png")))
        # DEBUG -> EXPERIMENTAL
        self.ui.menuAnnouncement_Banner.setIcon(QIcon(resource_path("assets/gui/icons/announcement-banner.png")))
        # DEBUG -> EXPERIMENTAL -> ANNOUNCEMENT BANNER
        self.ui.actionDisplay_Banner.setIcon(QIcon(resource_path("assets/gui/icons/announcement-banner-reload.png")))

        # CATEGORIES COMBOBOX
        self.ui.CategoriesComboBox.setItemIcon(1, QIcon(resource_path("assets/gui/icons/category/utility.png")))
        self.ui.CategoriesComboBox.setItemIcon(2, QIcon(resource_path("assets/gui/icons/category/emulator.png")))
        self.ui.CategoriesComboBox.setItemIcon(3, QIcon(resource_path("assets/gui/icons/category/game.png")))
        self.ui.CategoriesComboBox.setItemIcon(4, QIcon(resource_path("assets/gui/icons/category/media.png")))
        self.ui.CategoriesComboBox.setItemIcon(5, QIcon(resource_path("assets/gui/icons/category/demo.png")))

        self.populate_stylesheets()
        self.populate()
        self.selection_changed()
        self.status_message("Ready to download")
        self.ui.progressBar.setHidden(False)
        self.ui.statusBar.addPermanentWidget(self.ui.progressBar)
        self.load_announcement_banner()

    # show given status message on bottom status bar
    def status_message(self, message):
        self.ui.statusBar.showMessage(message)

    # populate UI elements
    def populate(self):
        if not splash.isHidden():
            splash.showMessage(f"Loading contents..", color=splash_color)
        self.ui.actionAbout_OSC_DL.setText(f"OSCDL v{VERSION} by dhtdht020")
        self.populate_repositories()
        self.populate_list()
        self.assign_initial_actions()

    # Populate list of repositories
    def populate_repositories(self):
        try:
            yaml_file = requests.get(
                "https://raw.githubusercontent.com/dhtdht020/oscdl-updateserver/master/v1/announcement"
                "/repositories.yml").text
            parsed_yaml = yaml.load(yaml_file, Loader=yaml.FullLoader)
            repos = parsed_yaml["repos"]
            n = 0
            for i in repos:
                display_name = parsed_yaml["repositories"][i]["name"]
                host = parsed_yaml["repositories"][i]["host"]
                description = parsed_yaml["repositories"][i]["description"]
                name = i
                self.ui.ReposComboBox.addItem(display_name)
                self.ui.ReposComboBox.setItemData(n, [display_name, host, description, name], Qt.UserRole)
                if not splash.isHidden():
                    splash.showMessage(f"Loaded {n} repositories..", color=splash_color)
                n += 1

            index = self.ui.ReposComboBox.currentIndex()
            repo_data = self.ui.ReposComboBox.itemData(index, Qt.UserRole)

            self.ui.RepositoryNameLabel.setText(repo_data[0])
            self.ui.RepositoryDescLabel.setText(repo_data[2])
        except Exception:
            # Add base repos
            self.ui.ReposComboBox.addItem("Open Shop Channel")
            self.ui.ReposComboBox.addItem("Homebrew Channel Themes")
            self.ui.ReposComboBox.setItemData(0, ["Open Shop Channel",
                                                  "hbb1.oscwii.org",
                                                  "Built in: Open Shop Channel default repository.",
                                                  "primary"], Qt.UserRole)
            self.ui.ReposComboBox.setItemData(1, ["Homebrew Channel Themes",
                                                  "hbb3.oscwii.org",
                                                  "Built in: Open Shop Channel default theme repository.",
                                                  "themes"], Qt.UserRole)

    def assign_initial_actions(self):
        # Connect signals
        if not splash.isHidden():
            splash.showMessage(f"Finishing (1/3)..", color=splash_color)
        # Buttons
        self.ui.CopyDirectLinkBtn.clicked.connect(self.copy_download_link_button)
        self.ui.ViewMetadataBtn.clicked.connect(self.download_button)
        self.ui.WiiLoadButton.clicked.connect(self.wiiload_button)
        self.ui.ReturnToMainBtn.clicked.connect(self.return_to_all_apps_btn)

        # Search Bar
        self.ui.SearchBar.textChanged.connect(self.search_bar)

        # Others
        self.ui.ReposComboBox.currentIndexChanged.connect(self.changed_host)
        self.ui.CategoriesComboBox.currentIndexChanged.connect(self.changed_category)
        self.ui.listAppsWidget.currentItemChanged.connect(self.selection_changed)
        self.ui.tabMetadata.currentChanged.connect(self.tab_changed)
        self.ui.developer_profile_btn.clicked.connect(self.developer_profile)

        # Actions
        # -- Debug
        self.ui.actionEnable_Log_File.triggered.connect(self.turn_log_on)
        self.ui.actionClose_the_shop.triggered.connect(self.close_the_shop)
        self.ui.actionDisplay_Banner.triggered.connect(self.load_announcement_banner)
        self.ui.actionSelect_Theme.triggered.connect(self.select_theme_action)
        # -- Clients
        # ---- Homebrew Browser
        self.ui.actionDownload_HBB_Client_Latest.triggered.connect(partial(self.download_latest_hbb_action))
        # ---- OSCDL
        self.ui.actionCheck_for_Updates.triggered.connect(partial(self.check_for_updates_action))
        self.ui.actionRefresh.triggered.connect(partial(self.repopulate))

    # When user switches to a different tab
    def tab_changed(self):
        if self.ui.tabMetadata.currentIndex() == 1:
            self.ui.longDescriptionBrowser.setText("Loading description..")
            self.repaint()
            app_name = self.ui.listAppsWidget.currentItem().data(Qt.UserRole)[0]
            self.ui.longDescriptionBrowser.setText(metadata.long_description(app_name, repo=HOST))

    # When user selects a different homebrew from the list
    def selection_changed(self):
        if not splash.isHidden():
            splash.showMessage(f"Finishing (2/3) - Loading first app..", color=splash_color)
        try:
            # app_name = self.ui.listAppsWidget.currentItem().text()
            data = self.ui.listAppsWidget.currentItem().data(Qt.UserRole)
            app_name = data[0]
        except Exception:
            app_name = None
        if app_name is not None:
            # Set active tab to first
            self.ui.tabMetadata.setCurrentIndex(0)

            # Hide icon
            self.ui.HomebrewIconLabel.hide()

            # Clear supported controllers listview:
            self.ui.SupportedControllersListWidget.clear()

            # Set data
            data = self.ui.listAppsWidget.currentItem().data(Qt.UserRole)

            # -- Get actual metadata
            # App Name
            self.ui.appname.setText(data[1])
            self.ui.SelectionInfoBox.setTitle("Metadata: " + data[1])
            self.ui.label_displayname.setText(data[1])

            # File Size
            try:
                self.ui.filesize.setText(metadata.file_size(data[2]))
            except KeyError:
                self.ui.filesize.setText("Unknown")

            # Category
            self.ui.HomebrewCategoryLabel.setText(metadata.category_display_name(data[3]))

            # Release Date
            self.ui.releasedate.setText(datetime.fromtimestamp(int(data[4])).strftime('%B %e, %Y at %R'))

            # Controllers
            controllers = metadata.parse_controllers(data[5])
            # Add icons for Wii Remotes
            if controllers[0] > 1:
                item = QListWidgetItem()
                item.setText(f"{str(controllers[0])} Wii Remotes")
                item.setIcon(QIcon(resource_path(f"assets/gui/icons/controllers/{str(controllers[0])}WiiRemote.png")))
                item.setToolTip(f"This app supports up to {str(controllers[0])} Wii Remotes.")
                self.ui.SupportedControllersListWidget.addItem(item)
            elif controllers[0] == 1:
                item = QListWidgetItem()
                item.setText(f"1 Wii Remote")
                item.setIcon(QIcon(resource_path(f"assets/gui/icons/controllers/1WiiRemote.png")))
                item.setToolTip("This app supports a single Wii Remote.")
                self.ui.SupportedControllersListWidget.addItem(item)
            if controllers[1] is True:
                item = QListWidgetItem()
                item.setText(f"Nunchuk")
                item.setIcon(QIcon(resource_path(f"assets/gui/icons/controllers/Nunchuk.png")))
                item.setToolTip("This app can be used with a Nunchuk.")
                self.ui.SupportedControllersListWidget.addItem(item)
            if controllers[2] is True:
                item = QListWidgetItem()
                item.setText(f"Classic Controller")
                item.setIcon(QIcon(resource_path(f"assets/gui/icons/controllers/ClassicController.png")))
                item.setToolTip("This app can be used with a Classic Controller.")
                self.ui.SupportedControllersListWidget.addItem(item)
            if controllers[3] is True:
                item = QListWidgetItem()
                item.setText(f"GameCube Controller")
                item.setIcon(QIcon(resource_path(f"assets/gui/icons/controllers/GamecubeController.png")))
                item.setToolTip("This app can be used with a Gamecube Controller.")
                self.ui.SupportedControllersListWidget.addItem(item)
            if controllers[4] is True:
                item = QListWidgetItem()
                item.setText(f"Wii Zapper")
                item.setIcon(QIcon(resource_path(f"assets/gui/icons/controllers/WiiZapper.png")))
                item.setToolTip("This app can be used with a Wii Zapper.")
                self.ui.SupportedControllersListWidget.addItem(item)
            if controllers[5] is True:
                item = QListWidgetItem()
                item.setText(f"USB Keyboard")
                item.setIcon(QIcon(resource_path(f"assets/gui/icons/controllers/USBKeyboard.png")))
                item.setToolTip("This app can be used with a USB Keyboard.")
                self.ui.SupportedControllersListWidget.addItem(item)
            if controllers[6] is True:
                item = QListWidgetItem()
                item.setText(f"SDHC Card")
                item.setIcon(QIcon(resource_path(f"assets/gui/icons/controllers/SDHC.png")))
                item.setToolTip("This app is confirmed to support SDHC cards.")
                self.ui.SupportedControllersListWidget.addItem(item)

            # Version
            self.ui.version.setText(data[6])

            # Coder
            self.ui.developer.setText(data[7])

            # Short Description
            if data[8] == "":
                self.ui.label_description.setText("No description specified.")
            else:
                self.ui.label_description.setText(data[8])

            # Long Description
            self.ui.longDescriptionBrowser.setText(data[9])

            # File Name Line Edit
            self.ui.FileNameLineEdit.setText(app_name + ".zip")
            self.ui.DirectLinkLineEdit.setText(metadata.url(app_name, repo=HOST))
        self.ui.progressBar.setValue(0)
        self.repaint()
        # Load icon
        self.load_icon(app_name=app_name, repo=HOST)
        self.status_message("Ready to download")

    def view_metadata(self):
        data = self.ui.listAppsWidget.currentItem().data(Qt.UserRole)
        self.app_name = data[0]

    def trugh(self, text):
        return QObject.tr(self, text)

    def download_button(self):
        data = self.ui.listAppsWidget.currentItem().data(Qt.UserRole)
        self.app_name = data[0]
        self.status_message(f"Downloading {self.app_name} from Open Shop Channel..")
        path_to_file, _ = QFileDialog.getSaveFileName(None, 'Save Application', self.ui.FileNameLineEdit.text())
        output = path_to_file
        self.ui.progressBar.setValue(25)
        console_output = io.StringIO()
        if output != '':
            with redirect_stdout(console_output):
                download.get(app_name=self.app_name, repo=HOST, output=output)
            self.ui.progressBar.setValue(100)
            self.status_message(utils.escape_ansi(console_output.getvalue()))
        else:
            self.ui.progressBar.setValue(0)
            self.status_message("Cancelled Download.")

    def wiiload_button(self):
        data = self.ui.listAppsWidget.currentItem().data(Qt.UserRole)
        app_name = data[0]
        app_display_name = data[1]

        ip, ok = QInputDialog.getText(self, 'Send to Wii: Enter IP address',
                                      'Enter the IP address of your Wii.\n'
                                      'The selected app will be sent through the network to your Wii.\n\n'
                                      f'App to send: {app_display_name}\n\n'
                                      'To find your Wii\'s IP address:\n'
                                      '1) Enter the Homebrew Channel.\n'
                                      '2) Press the home button on the Wii Remote.\n'
                                      '3) Copy the IP address written in the top left corner.\n\n'
                                      'IP address (e.g. 192.168.1...):',
                                      QLineEdit.Normal)
        if not ok:
            return

        ip_match = wiiload.validate_ip_regex(ip)

        if ip_match is None:
            logging.warning('Invalid IP Address: ' + ip)
            QMessageBox.warning(self, 'Invalid IP Address', 'This IP address is invalid.')
            return

        self.status_message("Downloading " + app_name + " from Open Shop Channel..")
        self.ui.progressBar.setValue(25)

        # download.get() cannot save to our own file-like object.
        # Alt fix: add a file parameter to write to instead?
        url = f"https://{HOST}/hbb/{app_name}/{app_name}.zip"
        r = requests.get(url)

        self.status_message("Preparing app...")
        self.ui.progressBar.setValue(40)

        zipped_app = io.BytesIO(r.content)
        zip_buf = io.BytesIO()

        # Our zip file should only contain one directory with the app data in it,
        # but the downloaded file contains an apps/ directory. We're removing that here.
        wiiload.organize_zip(zipped_app, zip_buf)

        # preparing
        prep = wiiload.prepare(zip_buf)

        file_size = prep[0]
        compressed_size = prep[1]
        chunks = prep[2]

        # connecting
        self.status_message('Connecting to the HBC...')
        self.ui.progressBar.setValue(50)

        try:
            conn = wiiload.connect(ip)
        except socket.error as e:
            logging.error('Error while connecting to the HBC. Please check the IP address and try again.')
            QMessageBox.warning(self, 'Connection error',
                                'Error while connecting to the HBC. Please check the IP address and try again.')
            print(f'WiiLoad: {e}')
            self.ui.progressBar.setValue(0)
            self.status_message('Error: Could not connect to the Homebrew Channel. :(')

            return

        wiiload.handshake(conn, compressed_size, file_size)

        # Sending file
        self.status_message('Sending app...')

        chunk_num = 1
        for chunk in chunks:
            conn.send(chunk)

            chunk_num += 1
            progress = round(chunk_num / len(chunks) * 50) + 50
            self.ui.progressBar.setValue(progress)
            self.repaint()

        file_name = f'{app_name}.zip'
        conn.send(bytes(file_name, 'utf-8') + b'\x00')

        self.ui.progressBar.setValue(100)
        self.status_message('App transmitted!')
        logging.info(f"App transmitted to HBC at {ip}")

    def copy_download_link_button(self):
        data = self.ui.listAppsWidget.currentItem().data(Qt.UserRole)
        self.app_name = data[0]
        QApplication.clipboard().setText(metadata.url(self.app_name, repo=HOST))
        self.status_message(f"Copied the download link for {self.app_name} to clipboard")

    def changed_host(self):
        global HOST
        global HOST_NAME
        index = self.ui.ReposComboBox.currentIndex()
        repo_data = self.ui.ReposComboBox.itemData(index, Qt.UserRole)
        HOST = repo_data[1]
        HOST_NAME = repo_data[3]
        self.ui.RepositoryNameLabel.setText(repo_data[0])
        self.ui.RepositoryDescLabel.setText(repo_data[2])
        self.status_message(f"Loading {HOST} repository..")
        logging.info(f"Loading {HOST}")
        self.ui.progressBar.setValue(20)
        self.repopulate()

    def repopulate(self):
        # Make sure everything is hidden / shown
        self.ui.ReturnToMainBtn.setHidden(True)
        self.ui.CategoriesComboBox.setHidden(False)
        self.ui.ReposComboBox.setHidden(False)
        self.ui.RepositoryLabel.setHidden(False)

        self.ui.SearchBar.setText("")

        self.status_message("Reloading list..")
        index = self.ui.ReposComboBox.currentIndex()
        repo_data = self.ui.ReposComboBox.itemData(index, Qt.UserRole)
        self.ui.RepositoryNameLabel.setText(repo_data[0])
        self.ui.RepositoryDescLabel.setText(repo_data[2])
        try:
            self.ui.CategoriesComboBox.currentIndexChanged.disconnect(self.changed_category)
        except Exception:
            pass
        self.ui.CategoriesComboBox.setCurrentIndex(0)
        self.ui.listAppsWidget.clear()
        self.populate_list()
        self.ui.progressBar.setValue(100)
        self.ui.CategoriesComboBox.currentIndexChanged.connect(self.changed_category)

    def populate_list(self, category="all", coder=None):
        try:
            if not splash.isHidden():
                splash.showMessage(f"Connecting to server..", color=splash_color)

            # Get apps json
            loaded_json = metadata.get_apps(host_name=HOST_NAME, category=category, coder=coder)
            i = 0
            for package in loaded_json:
                try:
                    self.ui.listAppsWidget.addItem(package["display_name"])
                    list_item = self.ui.listAppsWidget.item(i)
                    list_item.setData(Qt.UserRole, [package["internal_name"],
                                                    package["display_name"],
                                                    package["extracted"],
                                                    package["category"],
                                                    package["release_date"],
                                                    package["controllers"],
                                                    package["version"],
                                                    package["coder"],
                                                    package["short_description"],
                                                    package["long_description"]])
                    # Set category icon
                    category = package["category"]
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
                    # self.ui.listAppsWidget.setItemData(i, [internal_name, display_name], Qt.UserRole)
                    if not splash.isHidden():
                        splash.showMessage(f"Loaded {i} apps..", color=splash_color)
                    i += 1
                except IndexError:
                    ongoing = False
            self.sort_list_alphabetically()
            self.ui.listAppsWidget.setCurrentRow(0)
            self.ui.AppsAmountLabel.setText(str(self.ui.listAppsWidget.count()) + " Apps")

        except Exception as e:
            QMessageBox.critical(self, 'OSCDL: Critical Network Error',
                                 'Could not connect to the Open Shop Channel server.\n'
                                 'Cannot continue. :(\n'
                                 'Please check your internet connection, or report this incident.\n\n'
                                 f'Exception: {e}')
            sys.exit(1)

    # Actions
    # Enable log
    def turn_log_on(self):
        logging.basicConfig(filename='oscdl-gui.log', level=logging.DEBUG,
                            format="%(asctime)s | %(levelname)s:%(name)s:%(message)s")
        logging.info('User chose to enable log file. Hello there!')
        logging.info("OSCDL v" + DISPLAY_VERSION + ": Running on " + updater.get_type())
        self.status_message('DEBUG: Enabled log file. To disable, exit the program.')
        self.ui.actionEnable_Log_File.setDisabled(True)
        self.ui.actionClear_Log.setEnabled(True)
        self.ui.actionClear_Log.triggered.connect(self.clear_log)

    # Clear log file
    def clear_log(self):
        open("oscdl-gui.log", 'w').close()
        self.status_message('DEBUG: Removed / cleared log file.')

    # Sort apps in app list in alphabetical, ascending order.
    def sort_list_alphabetically(self):
        self.ui.listAppsWidget.sortItems(Qt.AscendingOrder)

    # Download Homebrew Browser
    def download_latest_hbb_action(self):
        self.status_message("Downloading Homebrew Browser from Open Shop Channel..")
        path_to_file, _ = QFileDialog.getSaveFileName(None, 'Save Application', "homebrew_browser_v0.3.9e.zip")
        output = path_to_file
        self.ui.progressBar.setValue(25)
        if output != "":
            download.hbb(output)
            self.ui.progressBar.setValue(100)
            self.status_message(f"Download success! Output: {output}")
        else:
            self.ui.progressBar.setValue(0)
            self.status_message(f"Cancelled Download.")

    # Check for updates dialog
    def check_for_updates_action(self):
        self.status_message("Checking for updates..")
        if updater.check_update() is True:
            latest = updater.latest_version()
            self.status_message("New version available! (" + updater.latest_version() + ") OSCDL is out of date.")
            QMessageBox.warning(self, 'OSCDL is out of date',
                                'Please go to GitHub and obtain the latest release\n'
                                'Newest Version: ' + latest)
        else:
            self.status_message("OSCDL is up to date!")
            QMessageBox.information(self, 'OSCDL is up to date',
                                    'You are running the latest version of OSCDL!\n')

    # In case OSC gods are angry
    def close_the_shop(self):
        # Close the shop
        logging.critical('OSC GODS:CLOSING THE SHOP')
        self.ui.listAppsWidget.setDisabled(True)
        self.ui.ViewMetadataBtn.setDisabled(True)
        self.ui.WiiLoadButton.setDisabled(True)
        self.ui.progressBar.setDisabled(True)
        self.ui.ExtractAppCheckbox.setDisabled(True)
        self.ui.menubar.setDisabled(True)
        self.ui.ReposComboBox.setDisabled(True)
        self.ui.CategoriesComboBox.setDisabled(True)
        self.ui.SupportedControllersListWidget.setDisabled(True)
        logging.critical('OSC GODS:CLOSED THE SHOP')
        self.status_message("The shop is now closed")

    # Load app icon
    def load_icon(self, app_name, repo):
        # Gets raw image data from server
        data = metadata.icon(app_name=app_name, repo=repo)

        # Loads image
        image = QtGui.QImage()
        image.loadFromData(data)

        # Adds image to label
        lbl = self.ui.HomebrewIconLabel
        lbl.setPixmap(QtGui.QPixmap(image))
        lbl.show()

    def load_announcement_banner(self):
        if not splash.isHidden():
            splash.showMessage(f"Finishing (3/3) - Checking for announcements..", color=splash_color)
        try:
            announcement = updater.get_announcement()
            announcement_label = announcement[0]
            announcement_url_label = announcement[1]
            announcement_banner_color = announcement[2]
            announcement_banner_text_color = announcement[3]
            announcement_website_enabled = announcement[4]
            if announcement is not None:
                # Un-hide banner
                self.ui.announcement.setHidden(False)

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
            # print(i.text())
            results.append(i.text())
            n += 1

        # Get All Items
        for i in self.ui.listAppsWidget.findItems("", Qt.MatchContains):
            # Hide and unhide!
            if i.text() in results:
                i.setHidden(False)
            else:
                i.setHidden(True)
        if text == "":
            self.ui.AppsAmountLabel.setText(f"{n} Apps")
        else:
            if n == 1:
                self.ui.AppsAmountLabel.setText(f"{n} Result")
            else:
                self.ui.AppsAmountLabel.setText(f"{n} Results")

    # When a different category is selected
    def changed_category(self):
        category = "all"

        if self.ui.CategoriesComboBox.currentText() == "Utilities":
            category = "utilities"
        elif self.ui.CategoriesComboBox.currentText() == "Emulators":
            category = "emulators"
        elif self.ui.CategoriesComboBox.currentText() == "Games":
            category = "games"
        elif self.ui.CategoriesComboBox.currentText() == "Media":
            category = "media"
        elif self.ui.CategoriesComboBox.currentText() == "Demos":
            category = "demos"

        self.ui.listAppsWidget.clear()
        self.populate_list(category=category)

    # Load developer profile
    def developer_profile(self):
        developer = self.ui.developer.text()

        # Begin
        self.status_message(f"Loading developer profile for \"{developer}\"..")

        self.ui.SearchBar.setText("")

        # Disconnect categories
        self.ui.CategoriesComboBox.currentIndexChanged.disconnect(self.changed_category)
        self.ui.CategoriesComboBox.setCurrentIndex(0)
        self.ui.CategoriesComboBox.currentIndexChanged.connect(self.changed_category)

        # Hide unneeded elements
        self.ui.CategoriesComboBox.setHidden(True)
        self.ui.ReposComboBox.setHidden(True)
        self.ui.RepositoryLabel.setHidden(True)
        self.ui.ReturnToMainBtn.setHidden(False)

        # Set information
        self.ui.RepositoryNameLabel.setText(f"Developer Profile: {developer}")
        self.ui.RepositoryDescLabel.setText(f"Showing all apps made by the developer \"{developer}\".")

        self.ui.listAppsWidget.clear()

        self.populate_list(coder=developer)

    # Return from developer view to normal view
    def return_to_all_apps_btn(self):
        # Unhide unneeded elements
        self.ui.ReturnToMainBtn.setHidden(True)
        self.ui.CategoriesComboBox.setHidden(False)
        self.ui.ReposComboBox.setHidden(False)
        self.ui.RepositoryLabel.setHidden(False)

        # Return to host
        self.changed_host()

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

    # Set default stylesheet
    def populate_stylesheets(self):
        # Developer Profile Button
        self.ui.developer_profile_btn.setStyleSheet(f"""
        QPushButton {{
            border: none;
            background: none;
        }}

        QPushButton:hover {{
            color: #0078D7;
        }}
        """)


if __name__ == "__main__":
    app = QApplication()

    global splash
    global splash_color

    # Splash
    image = QtGui.QImage(resource_path("assets/gui/splash.png"))
    splash_color = QColor("White")
    splash = QSplashScreen(QtGui.QPixmap(image))
    splash.show()

    window = MainWindow()
    window.show()
    splash.hide()
    app.exec_()
