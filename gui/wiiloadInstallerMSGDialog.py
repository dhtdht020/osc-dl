import logging

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QGuiApplication
from PySide6.QtWidgets import QDialog, QMessageBox, QDialogButtonBox

import gui_helpers
from gui import ui_wiiloadInstallerMSGDialog
from utils import resource_path

class wiiloadInstallerMSG(ui_wiiloadInstallerMSGDialog.Ui_MSGBox, QDialog):
    def __init__(self, text, showHBText=False,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.HBNotice.setVisible(showHBText)
        self.textBox.setPlainText(text)
        
        self.screen = QGuiApplication.primaryScreen()
