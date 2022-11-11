import logging

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QGuiApplication
from PySide6.QtWidgets import QDialog, QMessageBox

import gui_helpers
import wiiload
from gui import ui_WiiLoadDialog
from utils import resource_path, file_size
import serial
import serial.tools.list_ports

class WiiLoadDialog(ui_WiiLoadDialog.Ui_Dialog,QDialog):
    def __init__(self, package, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        self.setWindowIcon(QIcon(resource_path("assets/gui/icons/downloadlocationdialog.png")))
        self.USBDes.setText('Select the serial port for the USB Gecko adapter.<br>'
                                'The selected app will be sent through the USBGecko to your Wii.<br><br>'
                                f'<b>App to send: {package["display_name"]}</b><br><br>'
                                'Make sure the USB Gecko device is attached to Slot B.<br>'
                                'It may appear as /dev/cu.usbserial-GECKUSB0 or COM# depending on your system.<br><br>'
                                '<b>If the selection below is not blank, your USB Gecko is the selected device.</b><br><br>')
                                
        self.USBDes.setTextFormat(Qt.TextFormat.RichText)
        
        self.IPDes.setText('Enter the IP address of your Wii.<br>'
                                'The selected app will be sent through the network to your Wii.<br><br>'
                                f'<b>App to send: {package["display_name"]}</b><br><br>'
                                'To find your Wii\'s IP address:<br>'
                                '1) Enter the Homebrew Channel.<br>'
                                '2) Press the home button on the Wii Remote.<br>'
                                '3) Copy the IP address written in the top left corner.<br><br>')
        self.IPDes.setTextFormat(Qt.TextFormat.RichText)
        
        self.USBGeckoVIDPID = (0x403, 0x6001) #USBGecko: VID 0x43, PID 0x6001 
        self.PortBox.addItem("")
        self.PortBoxSerial = []
        self.PortBoxSerial.append((None,None))

        # Check if USBGecko is plugged in, and ready.
        for x in serial.tools.list_ports.comports():
            self.PortBox.addItem(x.device)
            self.PortBoxSerial.append((x.vid,x.pid))
        
        if self.USBGeckoVIDPID in self.PortBoxSerial: 
            self.PortBox.setCurrentIndex(self.PortBoxSerial.index(self.USBGeckoVIDPID))
        
        self.IPBox.insert(gui_helpers.settings.value("sendtowii/address"))
        if gui_helpers.settings.value("sendtowii/previousTab") == None:
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
        
        if (currTab == 0):
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
        self.PortBox.addItem("")
        self.PortBoxSerial.append((None,None))
        for x in serial.tools.list_ports.comports():
            self.PortBox.addItem(x.device)
            self.PortBoxSerial.append((x.vid,x.pid))
        if self.USBGeckoVIDPID in self.PortBoxSerial:
            self.PortBox.setCurrentIndex(self.PortBoxSerial.index(self.USBGeckoVIDPID))
        super().update()
    
        