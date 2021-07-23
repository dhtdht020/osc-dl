import platform
import random
import string
import threading

import os
import sys

import logging  # for logs

import requests
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication,QWizard

import gui.ui_forwarderwiz
import updater


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
class ForwarderWizard(gui.ui_forwarderwiz.Ui_Wizard, QWizard):
    def __init__(self, test_mode=False, selected_app=None):
        super(ForwarderWizard, self).__init__()
        self.ui = gui.ui_forwarderwiz.Ui_Wizard()
        self.ui.setupUi(self)

        self.test_mode = test_mode

        self.selected_app = selected_app

        self.id_list_loaded = False

        # Set title and icon of window
        app_icon = QIcon(resource_path("assets/gui/windowicon.png"))
        self.setWindowIcon(app_icon)

        self.initial_connections()


    def initial_connections(self):
        #pass
        self.currentIdChanged.connect(self.page_changed)

    def page_changed(self):
        # get list of title ids if page is 1
        if self.currentId() == 1:
            if not self.id_list_loaded:
                self.ui.AvailableIDsListWidget.clear()
                self.ui.AvailableIDsListWidget.setEnabled(False)
                self.ui.AvailableIDsListWidget.addItem("Loading..")
                t = threading.Thread(target=self.populate_ids)
                t.start()

        # set app as current app if applicable if page is 2
        if self.currentId() == 2:
            if self.selected_app:
                self.ui.SelectOSCApplication.setText(f"Selected: {self.selected_app['display_name']}")

        # populate summary if page is 3
        if self.currentId() == 3:
            if self.selected_app:
                self.ui.Summary_SDCardPath.setText(f"SD:/apps/{self.selected_app['internal_name']}/boot.{self.selected_app['package_type']}")
                self.ui.Summary_TitleID.setText(self.ui.AvailableIDsListWidget.currentItem().text())
                self.ui.Summary_ApplicationSource.setText(f"{self.selected_app['display_name']} from Open Shop Channel")


    def populate_ids(self):
        # download database from gametdb
        request = requests.get("https://www.gametdb.com/wiitdb.txt?LANG=EN")

        # 4 letter ID structure:
        # 1-3rd letters: Anything
        # 4th letter: Can use A / B / U / X

        possible_last_letters = ["A", "B", "U", "X"]

        available_ids = []

        # generate IDs:
        while len(available_ids) < 1000:
            current_id = random.choice(string.ascii_uppercase) + \
                         random.choice(string.ascii_uppercase) + \
                         random.choice(string.ascii_uppercase) + \
                         random.choice(possible_last_letters)
            # check if available and not generated already
            if current_id.upper() not in request.text and (current_id.upper not in available_ids):
                available_ids.append(current_id.upper())

        available_ids.sort()

        self.ui.AvailableIDsListWidget.clear()
        self.ui.AvailableIDsListWidget.setEnabled(True)

        # add the ids to list
        for id in available_ids:
            self.ui.AvailableIDsListWidget.addItem(id)

        self.id_list_loaded = True

        self.ui.AvailableIDsListWidget.setCurrentRow(0)


if __name__ == "__main__":
    global app
    app = QApplication()

    # set windows style for macOS users
    if platform.system() == "Darwin":
        app.setStyle('Fusion')

    window = ForwarderWizard()
    window.show()
    app.exec()
