import metadata
import download
import parsecontents
import gui.ui_united
import updater
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtGui import QIcon
import sys, os


version = updater.current_version()


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class MainWindow(gui.ui_united.Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = gui.ui_united.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Open Shop Channel Downloader v"+version+" - Library")
        self.setIcon()
        self.populate()
        self.populate_meta()

    def setIcon(self):
        appIcon = QIcon(resource_path("oscicon.ico"))
        self.setWindowIcon(appIcon)

    def populate(self):
        self.ui.ViewMetadataBtn.clicked.connect(self.view_metadata)
        self.applist = parsecontents.list()
        self.ui.actionAbout_OSC_DL.setText("osc-dl Version v" + version)
        for item in self.applist:
            self.ui.listAppsWidget.addItem(item)

    def populate_meta(self):
        self.ui.ViewMetadataBtn.clicked.connect(self.download_button)

        self.ui.listAppsWidget.currentItemChanged.connect(self.selection_changed)

    def selection_changed(self):
        app_name = self.ui.listAppsWidget.currentItem().text()
        info = metadata.dictionary(app_name)
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
        self.ui.progressBar.setValue(0)

    def view_metadata(self):
        self.app_name = self.ui.listAppsWidget.currentItem().text()

    def download_button(self):
        self.app_name = self.ui.listAppsWidget.currentItem().text()
        output = self.ui.FileNameLineEdit.text()
        extract = self.ui.ExtractAppCheckbox.isChecked()
        self.ui.progressBar.setValue(25)
        download.get(app_name=self.app_name, output=output, extract=extract)
        self.ui.progressBar.setValue(100)


if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec_()
