import logging

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QGuiApplication
from PySide6.QtWidgets import QDialog, QMessageBox, QDialogButtonBox

import gui_helpers
import wiiload
from gui import ui_SendDialog
from utils import resource_path
import serial
import serial.tools.list_ports


class WiiLoadDialog(ui_SendDialog.Ui_Dialog, QDialog):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.send_type = {"dol": "App", "elf": "App", "thm": "Theme"}
        try:
            self.send_as = self.send_type[app["package_type"]]
        except:  # Just in case, but should never happen.
            self.send_as = "App"

        self.buttonBox.button(QDialogButtonBox.Ok).setText(f"Send {self.send_as}")

        self.setWindowIcon(QIcon(resource_path("assets/gui/icons/send.png")))
        self.setWindowTitle(f"Send to Wii - {app['name']}")

        self.USBDes.setTextFormat(Qt.TextFormat.RichText)
        self.IPDes.setTextFormat(Qt.TextFormat.RichText)

        self.USBGeckoVIDPID = (0x403, 0x6001)  # USBGecko: VID 0x43, PID 0x6001
        self.PortBoxSerial = []

        # Check if USBGecko is plugged in, and ready.
        for x in serial.tools.list_ports.comports():
            if (x.vid, x.pid) == self.USBGeckoVIDPID:
                self.PortBox.addItem(x.device)
                self.PortBoxSerial.append((x.vid, x.pid))
                self.PortBox.setCurrentIndex(self.PortBoxSerial.index(self.USBGeckoVIDPID))

        if self.PortBox.count() == 0:
            self.PortBox.setPlaceholderText("No USB Gecko devices connected.")
            self.PortBox.setEnabled(False)

        self.IPBox.insert(gui_helpers.settings.value("sendtowii/address"))
        if gui_helpers.settings.value("sendtowii/previousTab") is None:
            gui_helpers.settings.setValue("sendtowii/previousTab", 0)
            gui_helpers.settings.sync()

        self.Tab.setCurrentIndex(int(gui_helpers.settings.value("sendtowii/previousTab")))

        self.app = app
        self.selection = None

        self.modeSelect = None
        self.address = None

    def accept(self):
        self.modeSelect = currTab = self.Tab.currentIndex()

        if currTab == 0:
            gui_helpers.settings.setValue("sendtowii/address", self.IPBox.text())
            self.address = self.IPBox.text()

            if not wiiload.validate_ip_regex(self.address):
                logging.warning('Invalid IP Address: ' + self.address)
                QMessageBox.warning(self, 'Invalid IP Address', 'This IP address is invalid.')
                return
        else:
            self.address = self.PortBox.currentText()
            if self.address is None or self.address == "":
                logging.warning('Invalid device')
                QMessageBox.warning(self, 'Invalid device', 'Please select a vaild device.')
                return

        gui_helpers.settings.setValue("sendtowii/previousTab", currTab)
        gui_helpers.settings.sync()
        super().accept()

    def reject(self):
        super().reject()

    def update(self):
        self.PortBox.clear()
        self.PortBoxSerial = []

        for x in serial.tools.list_ports.comports():
            if (x.vid, x.pid) == self.USBGeckoVIDPID:
                self.PortBox.addItem(x.device)
                self.PortBoxSerial.append((x.vid, x.pid))
                self.PortBox.setCurrentIndex(self.PortBoxSerial.index(self.USBGeckoVIDPID))

        if self.PortBox.count():
            self.PortBox.setPlaceholderText("")
            self.PortBox.setEnabled(True)
        else:
            self.PortBox.setPlaceholderText("No USB Gecko devices connected.")
            self.PortBox.setEnabled(False)
        super().update()
