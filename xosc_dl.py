import io
import json
from datetime import datetime

import yaml
import sentry_sdk
import os
import re
import socket
import sys
from contextlib import redirect_stdout

import logging  # for logs
from functools import partial
from jsonpath_ng import jsonpath, parse

import requests
import pyperclip
from PySide2 import QtGui
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon, QColor
from PySide2.QtWidgets import QApplication, QMainWindow, QInputDialog, QLineEdit, QMessageBox, QSplashScreen, QLabel, \
    QListWidgetItem

import download
import gui.ui_united
import metadata
import parsecontents
import updater
import wiiload

VERSION = updater.current_version()
BRANCH = updater.get_branch()
if BRANCH == "Stable":
    DISPLAY_VERSION = VERSION
else:
    DISPLAY_VERSION = VERSION + " " + BRANCH

HOST = "hbb1.oscwii.org"
HOST_NAME = "primary"


# escape ansi for stdout output of download status
def escape_ansi(line):
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', line)


# Get resource when frozen with PyInstaller
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


if updater.is_frozen():
    # Init sentry
    sentry_sdk.init(
        "https://619963fe9ec346e1b032fb19ea1632c8@o456896.ingest.sentry.io/5450395",
        traces_sample_rate=1.0
    )

    with sentry_sdk.configure_scope() as scope:
        scope.set_tag("osc.release", VERSION)


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
        # DEBUG -> EXPERIMENTAL
        self.ui.menuAnnouncement_Banner.setIcon(QIcon(resource_path("assets/gui/icons/announcement-banner.png")))
        # DEBUG -> EXPERIMENTAL -> ANNOUNCEMENT BANNER
        self.ui.actionDisplay_Banner.setIcon(QIcon(resource_path("assets/gui/icons/announcement-banner-reload.png")))

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
        self.ui.actionAbout_OSC_DL.setText(f"osc-dl Version v{VERSION} by dhtdht020")
        self.populate_repositories()
        self.populate_list()
        self.assign_initial_actions()

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
        if not splash.isHidden():
            splash.showMessage(f"Finishing (1/3)..", color=splash_color)
        # Buttons
        self.ui.CopyDirectLinkBtn.clicked.connect(self.copy_download_link_button)
        self.ui.RefreshListBtn.clicked.connect(self.repopulate)
        self.ui.ViewMetadataBtn.clicked.connect(self.download_button)
        self.ui.WiiLoadButton.clicked.connect(self.wiiload_button)


        # Others
        self.ui.ReposComboBox.currentIndexChanged.connect(self.changed_host)
        self.ui.listAppsWidget.currentItemChanged.connect(self.selection_changed)


        # Actions
        # -- Debug
        self.ui.actionEnable_Log_File.triggered.connect(self.turn_log_on)
        self.ui.actionClose_the_shop.triggered.connect(self.close_the_shop)
        self.ui.actionDisplay_Banner.triggered.connect(self.load_announcement_banner)
        # -- Clients
        # ---- Homebrew Browser
        self.ui.actionDownload_HBB_Client_Latest.triggered.connect(partial(self.download_latest_hbb_action))
        # ---- OSC-DL
        self.ui.actionCheck_for_Updates.triggered.connect(partial(self.check_for_updates_action))
        self.ui.actionRefresh.triggered.connect(partial(self.repopulate))

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
            # Set text to Loading
            self.ui.HomebrewIconLabel.hide()
            self.ui.appname.setText("")
            self.ui.SelectionInfoBox.setTitle("Metadata: Loading..")
            self.ui.label_displayname.setText("Loading..")
            self.ui.version.setText("")
            self.ui.filesize.setText("")
            self.ui.releasedate.setText("")
            self.ui.HomebrewCategoryLabel.setText("")
            self.ui.developer.setText("")
            self.ui.label_description.setText("")
            # Clear supported controllers:
            self.ui.SupportedControllersListWidget.clear()

            self.repaint()

            info = metadata.dictionary(app_name, repo=HOST)
            data = self.ui.listAppsWidget.currentItem().data(Qt.UserRole)
            # Get actual metadata
            self.ui.appname.setText(data[1])
            self.ui.SelectionInfoBox.setTitle("Metadata: " + data[1])
            self.ui.label_displayname.setText(data[1])
            self.ui.version.setText(info.get("version"))
            try:
                self.ui.filesize.setText(metadata.file_size(data[2]))
            except KeyError:
                self.ui.filesize.setText("Unknown")

            # Get controllers
            controllers = self.parse_controllers(data[5])
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

            if data[3] == "demos":
                self.ui.HomebrewCategoryLabel.setText("Demo")
            elif data[3] == "emulators":
                self.ui.HomebrewCategoryLabel.setText("Emulator")
            elif data[3] == "games":
                self.ui.HomebrewCategoryLabel.setText("Game")
            elif data[3] == "media":
                self.ui.HomebrewCategoryLabel.setText("Media")
            elif data[3] == "utilities":
                self.ui.HomebrewCategoryLabel.setText("Utility")
            else:
                self.ui.HomebrewCategoryLabel.setText("")

            self.ui.releasedate.setText(datetime.fromtimestamp(int(data[4])).strftime('%B %e, %Y at %R'))
            self.ui.developer.setText(info.get("coder"))
            if info.get("short_description") == "Unknown":
                self.ui.label_description.setText("No description specified.")
            else:
                self.ui.label_description.setText(info.get("short_description"))
            self.ui.longDescriptionBrowser.setText(info.get("long_description"))
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

    def parse_controllers(self, controllers):
        wii_remotes = 0
        nunchuk = classic_controller = gamecube_controller = wii_zapper = keyboard = sdhc_compatible = False
        # Wii Remotes
        if "wwww" in controllers:
            wii_remotes = 4
        elif "www" in controllers:
            wii_remotes = 3
        elif "ww" in controllers:
            wii_remotes = 2
        elif "w" in controllers:
            wii_remotes = 1

        # nunchuk
        if "n" in controllers:
            nunchuk = True
        # Classic Controller
        if "c" in controllers:
            classic_controller = True
        if "g" in controllers:
            gamecube_controller = True
        if "z" in controllers:
            wii_zapper = True
        if "k" in controllers:
            keyboard = True
        if "s" in controllers:
            sdhc_compatible = True

        return wii_remotes, nunchuk, classic_controller, gamecube_controller, wii_zapper, keyboard, sdhc_compatible

    def download_button(self):
        data = self.ui.listAppsWidget.currentItem().data(Qt.UserRole)
        self.app_name = data[0]
        self.status_message(f"Downloading {self.app_name} from Open Shop Channel..")
        output = self.ui.FileNameLineEdit.text()
        extract = self.ui.ExtractAppCheckbox.isChecked()
        if extract is True:
            logging.info("Set to extract app too!")
        self.ui.progressBar.setValue(25)
        console_output = io.StringIO()
        with redirect_stdout(console_output):
            download.get(app_name=self.app_name, repo=HOST, output=output, extract=extract)
        self.ui.progressBar.setValue(100)
        self.status_message(escape_ansi(console_output.getvalue()))

    def wiiload_button(self):
        ip, ok = QInputDialog.getText(self, 'WiiLoad IP Address',
                                      'Enter the IP address of your Wii:',
                                      QLineEdit.Normal)
        if not ok:
            return

        ip_match = wiiload.validate_ip_regex(ip)

        if ip_match is None:
            logging.warning('Invalid IP Address: ' + ip)
            QMessageBox.warning(self, 'Invalid IP Address', 'This IP address is invalid.')
            return

        data = self.ui.listAppsWidget.currentItem().data(Qt.UserRole)
        self.app_name = data[0]
        self.status_message("Downloading " + self.app_name + " from Open Shop Channel..")
        self.ui.progressBar.setValue(25)

        # download.get() cannot save to our own file-like object.
        # Alt fix: add a file parameter to write to instead?
        url = f"https://{HOST}/hbb/{self.app_name}/{self.app_name}.zip"
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

        file_name = f'{self.app_name}.zip'
        conn.send(bytes(file_name, 'utf-8') + b'\x00')

        self.ui.progressBar.setValue(100)
        self.status_message('App transmitted!')
        logging.info(f"App transmitted to HBC at {ip}")

    def copy_download_link_button(self):
        data = self.ui.listAppsWidget.currentItem().data(Qt.UserRole)
        self.app_name = data[0]
        pyperclip.copy(metadata.url(self.app_name, repo=HOST))
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
        self.status_message("Reloading list..")
        index = self.ui.ReposComboBox.currentIndex()
        repo_data = self.ui.ReposComboBox.itemData(index, Qt.UserRole)
        self.ui.RepositoryNameLabel.setText(repo_data[0])
        self.ui.RepositoryDescLabel.setText(repo_data[2])

        self.ui.listAppsWidget.clear()
        self.populate_list()
        self.ui.progressBar.setValue(100)

    def populate_list(self):
        # Can't have a list when there's no connection :P
        # try:
        #    self.applist = parsecontents.list(repo=HOST)
        # except Exception:
        #    QMessageBox.critical(self, 'OSC-DL: Critical Network Error',
        #                         'Could not connect to the Open Shop Channel server.\n'
        #                         'Cannot continue. :(\n'
        #                         'Please check your internet connection, or report this incident.')
        #    sys.exit(1)
        # for item in self.applist:
        #    self.ui.listAppsWidget.addItem(item)
        # self.ui.listAppsWidget.setCurrentRow(0)
        # self.ui.AppsAmountLabel.setText(str(self.ui.listAppsWidget.count()) + " Apps")
        if not splash.isHidden():
            splash.showMessage(f"Connecting to server..", color=splash_color)
        json_req = requests.get(f"https://api.oscwii.org/v1/{HOST_NAME}/packages")
        loaded_json = json.loads(json_req.text)
        if json_req.status_code == 200:
            i = 0
            ongoing = True
            internal_name_dict = self.parse_json_expression(json=loaded_json,
                                                            expression=f"$[*].internal_name")
            display_name_dict = self.parse_json_expression(json=loaded_json,
                                                           expression=f"$[*].display_name")
            extracted_size_dict = self.parse_json_expression(json=loaded_json,
                                                             expression=f"$[*].extracted")
            category_dict = self.parse_json_expression(json=loaded_json,
                                                       expression=f"$[*].category")
            release_date_dict = self.parse_json_expression(json=loaded_json,
                                                           expression=f"$[*].release_date")
            controllers_dict = self.parse_json_expression(json=loaded_json,
                                                          expression=f"$[*].controllers")
            while ongoing is True:
                try:
                    internal_name = internal_name_dict[i].value
                    display_name = display_name_dict[i].value
                    extracted_size = extracted_size_dict[i].value
                    category = category_dict[i].value
                    release_date = release_date_dict[i].value
                    controllers = controllers_dict[i].value
                    self.ui.listAppsWidget.addItem(display_name)
                    self.ui.listAppsWidget.item(i).setData(Qt.UserRole, [internal_name,
                                                                         display_name,
                                                                         extracted_size,
                                                                         category,
                                                                         release_date,
                                                                         controllers])
                    # self.ui.listAppsWidget.setItemData(i, [internal_name, display_name], Qt.UserRole)
                    if not splash.isHidden():
                        splash.showMessage(f"Loaded {i} apps..", color=splash_color)
                    i += 1
                except IndexError:
                    ongoing = False

            self.sort_list_alphabetically()
            self.ui.listAppsWidget.setCurrentRow(0)
            self.ui.AppsAmountLabel.setText(str(self.ui.listAppsWidget.count()) + " Apps")

        else:
            QMessageBox.critical(self, 'OSC-DL: Critical Network Error',
                                 'Could not connect to the Open Shop Channel server.\n'
                                 'Cannot continue. :(\n'
                                 'Please check your internet connection, or report this incident.')

    # Actions

    def turn_log_on(self):
        logging.basicConfig(filename='osc-dl-gui.log', level=logging.DEBUG,
                            format="%(asctime)s | %(levelname)s:%(name)s:%(message)s")
        logging.info('User chose to enable log file. Hello there!')
        logging.info("OSC-DL v" + DISPLAY_VERSION + ": Running on " + updater.get_type())
        self.status_message('DEBUG: Enabled log file. To disable, exit the program.')
        self.ui.actionEnable_Log_File.setDisabled(True)
        self.ui.actionClear_Log.setEnabled(True)
        self.ui.actionClear_Log.triggered.connect(self.clear_log)

    def clear_log(self):
        open("osc-dl-gui.log", 'w').close()
        self.status_message('DEBUG: Removed / cleared log file.')

    def sort_list_alphabetically(self):
        self.ui.listAppsWidget.sortItems(Qt.AscendingOrder)

    def download_latest_hbb_action(self):
        self.status_message("Downloading Homebrew Browser from Open Shop Channel..")
        self.ui.progressBar.setValue(25)
        download.hbb()
        self.ui.progressBar.setValue(100)
        self.status_message("Download success! Output: homebrew_browser_v0.3.9e.zip")

    def check_for_updates_action(self):
        self.status_message("Checking for updates..")
        if updater.check_update() is True:
            latest = updater.latest_version()
            self.status_message("New version available! (" + updater.latest_version() + ") OSC-DL is out of date.")
            QMessageBox.warning(self, 'OSC-DL is out of date',
                                'Please go to GitHub and obtain the latest release\n'
                                'Newest Version: ' + latest)
        else:
            self.status_message("OSC-DL is up to date!")
            QMessageBox.information(self, 'OSC-DL is up to date',
                                    'You are running the latest version of OSC-DL!\n')

    # in case OSC gods are angry
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
        self.ui.RefreshListBtn.setDisabled(True)
        logging.critical('OSC GODS:CLOSED THE SHOP')
        self.status_message("The shop is now closed")

    def parse_json_expression(self, json, expression):
        json_expression = parse(expression)
        json_thing = json_expression.find(json)

        return json_thing

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


if __name__ == "__main__":
    global splash
    global splash_color
    app = QApplication()

    # Splash
    image = QtGui.QImage(resource_path("assets/gui/splash.png"))
    splash_color = QColor("White")
    splash = QSplashScreen(QtGui.QPixmap(image))
    splash.show()

    window = MainWindow()
    window.show()
    splash.hide()
    app.exec_()
