from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QDialog

from gui import ui_wiiloadInstallerMSGDialog

class wiiloadInstallerMSG(ui_wiiloadInstallerMSGDialog.Ui_MSGBox, QDialog):
    def __init__(self, text, showHBText=False,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.HBNotice.setVisible(showHBText)
        self.textBox.setMarkdown(text)
        
        self.screen = QGuiApplication.primaryScreen()
