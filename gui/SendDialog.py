import logging

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QGuiApplication
from PySide6.QtWidgets import QDialog, QMessageBox

import gui_helpers
import wiiload
from gui import ui_SendDialog
from utils import resource_path
import serial
import serial.tools.list_ports


class WiiLoadDialog(ui_SendDialog.Ui_Dialog, QDialog):
    def __init__(self, package, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.send_type = {"dol": "App", "elf": "App", "thm": "Theme"}
        try:
            self.send_as = self.send_type[package["package_type"]]
        except:  # Just in case, but should never happen.
            self.send_as = "App"

        self.setWindowIcon(QIcon(resource_path("assets/gui/icons/send.png")))
        self.USBDes.setText('Select the serial port for the USB Gecko adapter.<br>'
                            f'The selected {self.send_as.lower()} will be sent through the USBGecko to your Wii.<br><br>'
                            f'<b>{self.send_as} to send: {package["display_name"]}</b><br><br>'
                            'Make sure the USB Gecko device is attached to Slot B.<br>'
                            'It may appear as /dev/cu.usbserial-GECKUSB0 or COM# depending on your system.<br><br>'
                            '<b>If the selection below is not blank, your USB Gecko is the selected device.</b>')

        self.USBDes.setTextFormat(Qt.TextFormat.RichText)

        self.IPDes.setText('Enter the IP address of your Wii.<br>'
                           f'The selected {self.send_as.lower()} will be sent through the network to your Wii.<br><br>'
                           f'<b>{self.send_as} to send: {package["display_name"]}</b><br><br>'
                           'To find your Wii\'s IP address:<br>'
                           '1) Enter the Homebrew Channel.<br>'
                           '2) Press the home button on the Wii Remote.<br>'
                           '3) Copy the IP address written in the top left corner.')
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

        self.screen = QGuiApplication.primaryScreen()
        self.package = package
        self.selection = None

        self.setWindowTitle(f"Send to Wii")

        self.modeSelect = None
        self.address = None

    def accept(self):
        self.modeSelect = currTab = self.Tab.currentIndex()

        if currTab == 0:
            gui_helpers.settings.setValue("sendtowii/address", self.IPBox.text())
            self.address = self.IPBox.text()

            if wiiload.validate_ip_regex(self.address) is None:
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
