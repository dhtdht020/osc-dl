import copy
import io
import os
import re
import socket
import struct
import zipfile
import zlib
from contextlib import redirect_stdout

import logging  # for logs
import requests
import pyperclip
from PySide2.QtWidgets import QApplication, QMainWindow, QInputDialog, QLineEdit, QMessageBox

import download
import gui.ui_united
import metadata
import parsecontents
import updater
import wiiload

VERSION = updater.current_version()
BRANCH = updater.get_branch()
if BRANCH is "Stable":
    DISPLAY_VERSION = VERSION
else:
    DISPLAY_VERSION = VERSION + " " + BRANCH


HOST = "hbb1.oscwii.org"

# WiiLoad
WIILOAD_VER_MAJOR = 0
WIILOAD_VER_MINOR = 5
CHUNK_SIZE = 1024 * 128


def get_repo_host(display_name):
    if display_name == "Open Shop Channel":
        return "hbb1.oscwii.org"
    elif display_name == "Homebrew Channel Themes":
        return "hbb3.oscwii.org"


def escape_ansi(line):
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)


class MainWindow(gui.ui_united.Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = gui.ui_united.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Open Shop Channel Downloader v" + DISPLAY_VERSION + " - Library")
        self.populate()
        self.populate_meta()
        self.selection_changed()
        self.status_message("Ready to download")
        self.ui.statusBar.addPermanentWidget(self.ui.progressBar)

        # set up menu bar
        # self.ui.actionTXT_file.triggered.connect(self.export_applist_txt_button)

    def status_message(self, message):
        self.ui.statusBar.showMessage(message)

    def populate(self):
        self.ui.CopyDirectLinkBtn.clicked.connect(self.copy_download_link_button)
        self.ui.RefreshListBtn.clicked.connect(self.repopulate)
        self.ui.ReposComboBox.currentIndexChanged.connect(self.changed_host)
        self.ui.actionEnable_Log_File.triggered.connect(self.turn_log_on)
        self.ui.actionAbout_OSC_DL.setText("osc-dl Version v" + VERSION)
        self.populate_list()

    def populate_meta(self):
        self.ui.ViewMetadataBtn.clicked.connect(self.download_button)
        self.ui.WiiLoadButton.clicked.connect(self.wiiload_button)

        self.ui.listAppsWidget.currentItemChanged.connect(self.selection_changed)

    def selection_changed(self):
        try:
            app_name = self.ui.listAppsWidget.currentItem().text()
        except Exception:
            app_name = None
        if app_name is not None:
            info = metadata.dictionary(app_name, repo=HOST)
            self.ui.appname.setText(info.get("display_name"))
            self.ui.SelectionInfoBox.setTitle("Metadata: " + info.get("display_name"))
            self.ui.label_displayname.setText(info.get("display_name"))
            self.ui.version.setText(info.get("version"))
            self.ui.contributors.setText(info.get("contributors"))
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
        self.status_message("Ready to download")

    def view_metadata(self):
        self.app_name = self.ui.listAppsWidget.currentItem().text()

    def download_button(self):
        self.app_name = self.ui.listAppsWidget.currentItem().text()
        self.status_message("Downloading " + self.app_name + " from Open Shop Channel..")
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

        wiiload.send(chunks, conn, self.app_name)

        self.ui.progressBar.setValue(100)
        self.status_message('App transmitted!')
        logging.info('App transmitted to HBC at ' + ip)

    def copy_download_link_button(self):
        self.app_name = self.ui.listAppsWidget.currentItem().text()
        pyperclip.copy(metadata.url(self.app_name, repo=HOST))
        self.status_message("Copied the download link for " + self.app_name + " to clipboard")

    def changed_host(self):
        global HOST
        HOST = get_repo_host(self.ui.ReposComboBox.currentText())
        self.status_message("Loading " + HOST + " repository..")
        logging.info('Loading ' + HOST)
        self.ui.progressBar.setValue(20)
        self.repopulate()

    def repopulate(self):
        self.status_message("Reloading list..")
        self.ui.listAppsWidget.clear()
        self.populate_list()
        self.ui.progressBar.setValue(100)

    def populate_list(self):
        self.applist = parsecontents.list(repo=HOST)
        for item in self.applist:
            self.ui.listAppsWidget.addItem(item)
        self.ui.listAppsWidget.setCurrentRow(0)
        self.ui.AppsAmountLabel.setText("Displaying " + str(self.ui.listAppsWidget.count()) + " apps.")

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


if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec_()
