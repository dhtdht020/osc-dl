import copy
import io
import os
import re
import socket
import struct
import zipfile
import zlib
from contextlib import redirect_stdout

import pyperclip
import requests
from PySide2.QtWidgets import QApplication, QMainWindow, QInputDialog, QLineEdit, QMessageBox

import download
import gui.ui_united
import metadata
import parsecontents
import updater

version = updater.current_version()
host = "hbb1.oscwii.org"

ip_regex = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")

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
        self.setWindowTitle("Open Shop Channel Downloader v"+version+" - Library")
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
        self.ui.actionAbout_OSC_DL.setText("osc-dl Version v" + version)
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
            info = metadata.dictionary(app_name, repo=host)
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
            self.ui.DirectLinkLineEdit.setText(metadata.url(app_name, repo=host))
        self.ui.progressBar.setValue(0)
        self.status_message("Ready to download")

    def view_metadata(self):
        self.app_name = self.ui.listAppsWidget.currentItem().text()

    """def export_applist_txt_button(self):
        self.status_message("Exporting list of apps from Open Shop Channel..")
        file_name = None
        try:
            file_name = str(QFileDialog.getSaveFileName())
        except Exception:
            pass

        self.ui.progressBar.setValue(25)
        export_txt_output = io.StringIO()
        with redirect_stdout(export_txt_output):
            export.app_list(txt_path=file_name)
        self.ui.progressBar.setValue(100)
        self.status_message(escape_ansi(export_txt_output.getvalue()))
        print("Exported application list to " + file_name)"""

    def download_button(self):
        self.app_name = self.ui.listAppsWidget.currentItem().text()
        self.status_message("Downloading " + self.app_name + " from Open Shop Channel..")
        output = self.ui.FileNameLineEdit.text()
        extract = self.ui.ExtractAppCheckbox.isChecked()
        self.ui.progressBar.setValue(25)
        console_output = io.StringIO()
        with redirect_stdout(console_output):
            download.get(app_name=self.app_name, repo=host, output=output, extract=extract)
        self.ui.progressBar.setValue(100)
        self.status_message(escape_ansi(console_output.getvalue()))

    def wiiload_button(self):
        ip, ok = QInputDialog.getText(self, 'WiiLoad IP Address',
                                      'Enter the IP address of your Wii:',
                                      QLineEdit.Normal)
        if not ok:
            return

        ip_match = ip_regex.match(ip)
        if not ip_match:
            QMessageBox.warning(self, 'Invalid IP Address', 'This IP address is invalid.')

            return

        self.app_name = self.ui.listAppsWidget.currentItem().text()
        self.status_message("Downloading " + self.app_name + " from Open Shop Channel..")
        self.ui.progressBar.setValue(25)

        # download.get() cannot save to our own file-like object.
        # Alt fix: add a file parameter to write to instead?
        url = f"https://{host}/hbb/{self.app_name}/{self.app_name}.zip"
        r = requests.get(url)

        self.status_message("Preparing app...")
        self.ui.progressBar.setValue(50)

        zipped_app = io.BytesIO(r.content)
        zip_file = zipfile.ZipFile(zipped_app, mode='r')
        app_infolist = zip_file.infolist()

        # Our zip file should only contain one directory with the app data in it,
        # but the downloaded file contains an apps/ directory. We're removing that here.
        zip_buf = io.BytesIO()
        app_zip = zipfile.ZipFile(zip_buf, mode='w', compression=zipfile.ZIP_DEFLATED)

        # copy over all files
        for info in app_infolist:
            new_path = info.filename.replace('apps/', '')
            if not new_path:
                continue

            # we need to copy over the member info manually because
            # python's zipfile implementation sucks and
            # the HBC is very insecure about it.
            new_info = copy.copy(info)
            new_info.filename = new_path

            if new_info.filename[-1] in ('/', '\\'):  # directory
                continue

            with zip_file.open(info.filename, 'r') as file:
                data = file.read()

            app_zip.writestr(new_path, data)

        # cleanup
        zipped_app.close()
        zip_file.close()
        app_zip.close()

        # preparing
        zip_buf.seek(0, os.SEEK_END)
        file_size = zip_buf.tell()
        zip_buf.seek(0)

        c_data = zlib.compress((zip_buf.read()))
        compressed_size = len(c_data)
        chunks = [c_data[i:i + CHUNK_SIZE] for i in range(0, compressed_size, CHUNK_SIZE)]

        # connecting
        self.status_message('Connecting to the HBC...')

        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.settimeout(5)
        try:
            conn.connect((ip, 4299))
        except socket.error as e:
            QMessageBox.warning(self, 'Connection error',
                                'Error while connecting to the HBC. Please check the IP address and try again.')
            print(f'WiiLoad: {e}')

            return

        # handshake, all data types are unsigned
        conn.send(b'HAXX')
        conn.send(struct.pack('B', WIILOAD_VER_MAJOR))  # char
        conn.send(struct.pack('B', WIILOAD_VER_MINOR))  # char
        conn.send(struct.pack('>H', 0))  # big endian short
        conn.send(struct.pack('>L', compressed_size))  # big endian long
        conn.send(struct.pack('>L', file_size))  # big endian long

        # Sending file
        self.status_message('Sending app...')

        chunk_num = 1
        for chunk in chunks:
            conn.send(chunk)

            chunk_num += 1
            progress = round(chunk_num / len(chunks) * 50) + 50
            self.ui.progressBar.setValue(progress)

        file_name = f'{self.app_name}.zip'
        conn.send(bytes(file_name, 'utf-8') + b'\x00')

        self.status_message('App transmitted!')

    def copy_download_link_button(self):
        self.app_name = self.ui.listAppsWidget.currentItem().text()
        pyperclip.copy(metadata.url(self.app_name, repo=host))
        self.status_message("Copied the download link for " + self.app_name + " to clipboard")

    def changed_host(self):
        global host
        host = get_repo_host(self.ui.ReposComboBox.currentText())
        self.status_message("Loading " + host + " repository..")
        self.ui.progressBar.setValue(20)
        self.repopulate()

    def repopulate(self):
        self.status_message("Reloading list..")
        self.ui.listAppsWidget.clear()
        self.populate_list()
        self.ui.progressBar.setValue(100)

    def populate_list(self):
        self.applist = parsecontents.list(repo=host)
        for item in self.applist:
            self.ui.listAppsWidget.addItem(item)
        self.ui.listAppsWidget.setCurrentRow(0)
        self.ui.AppsAmountLabel.setText("Displaying " + str(self.ui.listAppsWidget.count()) + " apps.")


if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec_()
