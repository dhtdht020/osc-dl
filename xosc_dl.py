import metadata
import download
import parsecontents
import gui.ui_united
import updater
import export
import io
import re
from contextlib import redirect_stdout
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog


version = updater.current_version()


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
        self.status_message("Ready to download")
        self.ui.statusBar.addPermanentWidget(self.ui.progressBar)

        # set up menu bar
        # self.ui.actionTXT_file.triggered.connect(self.export_applist_txt_button)

    def status_message(self, message):
        self.ui.statusBar.showMessage(message)

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
            download.get(app_name=self.app_name, output=output, extract=extract)
        self.ui.progressBar.setValue(100)
        self.status_message(escape_ansi(console_output.getvalue()))


if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec_()
