import io
import json
import yaml
import sentry_sdk
import os
import re
import socket
import sys
from contextlib import redirect_stdout

import logging  # for logs
from functools import partial

import requests
import pyperclip
from PySide2 import QtGui
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication, QMainWindow, QInputDialog, QLineEdit, QMessageBox, QSplashScreen

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
        # DEBUG
        self.ui.actionEnable_Log_File.setIcon(QIcon(resource_path("assets/gui/icons/enable-log.png")))
        self.ui.actionClear_Log.setIcon(QIcon(resource_path("assets/gui/icons/clear-log.png")))
        self.ui.actionClose_the_shop.setIcon(QIcon(resource_path("assets/gui/icons/close-shop.png")))
        self.ui.menuExperimental.setIcon(QIcon(resource_path("assets/gui/icons/experimental.png")))
        self.ui.actionAdd_Fake_Application.setIcon(QIcon(resource_path("assets/gui/icons/add-fake-listing.png")))
        # DEBUG -> EXPERIMENTAL
        self.ui.menuAnnouncement_Banner.setIcon(QIcon(resource_path("assets/gui/icons/announcement-banner.png")))
        # DEBUG -> EXPERIMENTAL -> ANNOUNCEMENT BANNER
        self.ui.actionDisplay_Banner.setIcon(QIcon(resource_path("assets/gui/icons/announcement-banner-reload.png")))
        # BUNDLES
        self.ui.actionLoad_Collection.setIcon(QIcon(resource_path("assets/gui/icons/load-bundle.png")))
        self.ui.actionCreate_Collection.setIcon(QIcon(resource_path("assets/gui/icons/create-bundle.png")))

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
        self.ui.actionAbout_OSC_DL.setText(f"osc-dl Version v{VERSION}")
        self.populate_repositories()
        self.populate_list()
        self.assign_initial_actions()

    def populate_repositories(self):
        try:
            yaml_file = requests.get("https://raw.githubusercontent.com/dhtdht020/oscdl-updateserver/master/v1/announcement"
                                     "/repositories.yml").text
            parsed_yaml = yaml.load(yaml_file, Loader=yaml.FullLoader)
            repos = parsed_yaml["repos"]
            n = 0
            for i in repos:
                display_name = parsed_yaml["repositories"][i]["name"]
                host = parsed_yaml["repositories"][i]["host"]
                description = parsed_yaml["repositories"][i]["description"]
                self.ui.ReposComboBox.addItem(display_name)
                self.ui.ReposComboBox.setItemData(n, [display_name, host, description], Qt.UserRole)
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
                                                  "Built in: Open Shop Channel default repository."], Qt.UserRole)
            self.ui.ReposComboBox.setItemData(1, ["Homebrew Channel Themes",
                                                  "hbb2.oscwii.org",
                                                  "Built in: Open Shop Channel default theme repository."], Qt.UserRole)


    def assign_initial_actions(self):
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
        self.ui.actionAdd_Fake_Application.triggered.connect(self.add_fake_listing_action)
        self.ui.actionDisplay_Banner.triggered.connect(self.load_announcement_banner)
        # -- Clients
        # ---- Homebrew Browser
        self.ui.actionDownload_HBB_Client_Latest.triggered.connect(partial(self.download_latest_hbb_action))
        # ---- OSC-DL
        self.ui.actionCheck_for_Updates.triggered.connect(partial(self.check_for_updates_action))
        # -- Collections
        # ----- Load Collection
        self.ui.actionLoad_Collection.triggered.connect(partial(self.load_collection))

    # When user selects a different homebrew from the list
    def selection_changed(self):
        try:
            app_name = self.ui.listAppsWidget.currentItem().text()
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
            self.ui.developer.setText("")
            self.ui.label_description.setText("")

            self.repaint()

            info = metadata.dictionary(app_name, repo=HOST)
            # Get actual metadata
            self.ui.appname.setText(info.get("display_name"))
            self.ui.SelectionInfoBox.setTitle("Metadata: " + info.get("display_name"))
            self.ui.label_displayname.setText(info.get("display_name"))
            self.ui.version.setText(info.get("version"))
            try:
                self.ui.filesize.setText(metadata.file_size(app_name, repo=HOST))
            except KeyError:
                self.ui.filesize.setText("Unknown")

            self.ui.releasedate.setText(info.get("release_date"))
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
        self.app_name = self.ui.listAppsWidget.currentItem().text()

    def validate_collection(self, collection, repos):
        # Check if there are contents
        try:
            apps = collection["applications"]
            first_app = apps[0]
        except TypeError as e:
            QMessageBox.critical(self, 'OSC-DL: Critical Collection Validator Error',
                                 'This collection seems to have 0 apps. Instructions unclear!\n'
                                 'Loading of collection has been stopped.\n'
                                 'Please report this incident.\n\n'
                                 f'Exception: {e}')
            raise e



    def load_collection(self):
        global HOST
        id, ok = QInputDialog.getText(self, 'Load OSC Collection',
                                      'Enter the ID associated with your collection.\n'
                                      'The ID is in all-caps, and matches the collection YAML name. \n\n'
                                      'If you are testing a local collection, please use the Collection Editor tool.',
                                      QLineEdit.Normal)
        if not ok:
            return

        collection_req = requests.get(f"https://raw.githubusercontent.com/dhtdht020/OSCDL-Collections/master/v1/collection/{id}.yml")
        repos_req = requests.get(f"https://raw.githubusercontent.com/dhtdht020/oscdl-updateserver/master/v1/announcement/repositories.yml")
        collection_file = collection_req.text
        repos_file = repos_req.text

        if collection_req.status_code != 200:
            QMessageBox.critical(self, 'OSC-DL: Critical Collections Error',
                                 'Could not find this collection or connect to the collection server.\n'
                                 'Please check your internet connection, or report this incident.')
        if repos_req.status_code != 200:
            QMessageBox.critical(self, 'OSC-DL: Critical Repository List Error',
                                 'Could not connect to the repository list server.\n'
                                 'Please check your internet connection, or report this incident.')
        else:
            parsed_collection = yaml.load(collection_file, Loader=yaml.FullLoader)
            parsed_repos = yaml.load(repos_file, Loader=yaml.FullLoader)
            # Validate collection
            self.validate_collection(parsed_collection, parsed_repos)
            # Disconnect repository signals while nobody's looking :eyes:
            self.ui.ReposComboBox.currentIndexChanged.disconnect(self.changed_host)
            self.ui.listAppsWidget.currentItemChanged.disconnect(self.selection_changed)

            collection_internal_name = parsed_collection["metadata"]["host"]
            collection_host_name = parsed_repos["repositories"][collection_internal_name]["name"]
            collection_host_addr = parsed_repos["repositories"][collection_internal_name]["host"]
            collection_contents = parsed_collection["applications"]

            HOST = collection_host_addr

            # Get dropdown index of repo by name
            repo_index = self.ui.ReposComboBox.findText(collection_host_name)
            # Set current dropdown index
            self.ui.ReposComboBox.setCurrentIndex(repo_index)

            # Set displayed repo info
            display_name = parsed_collection["metadata"]["name"]
            description = parsed_collection["metadata"]["description"]
            author = parsed_collection["metadata"]["author"]
            self.ui.RepositoryNameLabel.setText(f"Collection: {display_name}")
            self.ui.RepositoryDescLabel.setText(f"Made by {author}. {description}")

            # Clear list and repopulate with collection
            self.ui.listAppsWidget.clear()
            amount = 0
            for i in collection_contents:
                self.ui.listAppsWidget.addItem(i)
                amount += 1

            # Set apps amount
            self.ui.AppsAmountLabel.setText(f"{amount} Apps")

            # Reconnect repository signals. Good. Nobody noticed.
            self.ui.ReposComboBox.currentIndexChanged.connect(self.changed_host)
            self.ui.listAppsWidget.currentItemChanged.connect(self.selection_changed)

            # Select row 0
            self.ui.listAppsWidget.setCurrentRow(0)

    def download_button(self):
        self.app_name = self.ui.listAppsWidget.currentItem().text()
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

        self.app_name = self.ui.listAppsWidget.currentItem().text()
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
        self.app_name = self.ui.listAppsWidget.currentItem().text()
        pyperclip.copy(metadata.url(self.app_name, repo=HOST))
        self.status_message(f"Copied the download link for {self.app_name} to clipboard")

    def changed_host(self):
        global HOST
        index = self.ui.ReposComboBox.currentIndex()
        repo_data = self.ui.ReposComboBox.itemData(index, Qt.UserRole)
        HOST = repo_data[1]
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
        try:
            self.applist = parsecontents.list(repo=HOST)
        except Exception:
            QMessageBox.critical(self, 'OSC-DL: Critical Network Error',
                                 'Could not connect to the Open Shop Channel server.\n'
                                 'Cannot continue. :(\n'
                                 'Please check your internet connection, or report this incident.')
            sys.exit(1)
        for item in self.applist:
            self.ui.listAppsWidget.addItem(item)
        self.ui.listAppsWidget.setCurrentRow(0)
        self.ui.AppsAmountLabel.setText(str(self.ui.listAppsWidget.count()) + " Apps")

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

    def add_fake_listing_action(self):
        amount, ok = QInputDialog.getInt(self, 'Debug: Fake Listing Wizard',
                                         'Enter the amount of fake listings to add:',
                                         QLineEdit.Normal)
        if not ok:
            return

        self.status_message("DEBUG: Adding fake entries.. Please wait..")

        word_json = requests.get(f"https://random-word-api.herokuapp.com/word?number={amount}").text
        words = json.loads(word_json)
        for item in words:
            self.ui.listAppsWidget.addItem(item + "_wii")

        self.status_message(f"DEBUG: Added {amount} fake entries to applications list.")

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
    app = QApplication()

    # Splash
    try:
        # data = updater.obtain_splash()
        image = QtGui.QImage(resource_path("assets/gui/splash.png"))
        splash = QSplashScreen(QtGui.QPixmap(image))
        splash.show()
    except Exception:
        pass

    window = MainWindow()
    window.show()
    try:
        splash.hide()
    except Exception:
        pass
    app.exec_()
