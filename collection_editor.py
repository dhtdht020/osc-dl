import io
import json
import yaml
import os
import re
import socket
import sys
from contextlib import redirect_stdout

import logging  # for logs
from functools import partial

import requests
import pyperclip
from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication, QMainWindow, QInputDialog, QLineEdit, QMessageBox, QSplashScreen, QWidget, \
    QMdiSubWindow, QVBoxLayout

import download
import gui.ui_cedit
import gui.ceditor_mdi.ui_collection
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


# G U I
class MainWindow(gui.ui_cedit.Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = gui.ui_cedit.Ui_MainWindow()
        self.ui.setupUi(self)

        # Set title and icon of window
        self.setWindowTitle(f"Open Shop Channel Collection Editor v{DISPLAY_VERSION}")
        app_icon = QIcon(resource_path("assets/gui/windowicon.png"))
        self.setWindowIcon(app_icon)


        # Set GUI Icons
        self.ui.actionNew_Collection.setIcon(QIcon(resource_path("assets/gui/ceditor-icons/CreateCollection.png")))
        self.ui.actionLoad_Collection.setIcon(QIcon(resource_path("assets/gui/ceditor-icons/LoadCollection.png")))
        self.ui.actionSave_Collection.setIcon(QIcon(resource_path("assets/gui/ceditor-icons/SaveCollection.png")))

        #sub_window = QMdiSubWindow()
        #sub_window.setWidget(QWidget(CollectionWindow))
        #self.ui.mdiArea.addSubWindow(sub_window)

        self.create_collection_contents_pane()
        self.create_host_contents_pane()

    def create_collection_contents_pane(self):
        collection_view = QMdiSubWindow()
        widget = QtWidgets.QListWidget()
        collection_view.setWidget(widget)
        self.ui.mdiArea.addSubWindow(collection_view)
        collection_view.setWindowTitle("Contents: Unnamed New Collection")
        collection_view.show()
        widget.addItem("WiiVNC")
        widget.addItem("NewoEscape")
        widget.addItem("wiibricker_9000")
        widget.addItem("Achtung_Wii_Kurve")
        widget.addItem("BootMiiConfigurationEditor")

    def create_host_contents_pane(self, host="hbb1.oscwii.org"):
        collection_view = QMdiSubWindow()
        layout = QVBoxLayout()
        widget = QtWidgets.QListWidget()
        button = QtWidgets.QPushButton()
        layout.addWidget(widget)
        layout.addWidget(button)
        collection_view.setLayout(layout)
        self.ui.mdiArea.addSubWindow(collection_view)
        collection_view.setWindowTitle("Open Shop Channel")
        collection_view.show()
        self.applist = parsecontents.list(repo=host)
        for i in self.applist:
            widget.addItem(i)

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
