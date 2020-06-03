import argparse
import metadata
import download
import gui.ui_meta
import sys
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import QFile


parser = argparse.ArgumentParser(
    description="Open Shop Channel Package DL Graphical"
)

subparser = parser.add_subparsers(dest='cmd')
meta = subparser.add_parser('meta')

meta.add_argument(
    "-n",
    "--name",
    help="Name of homebrew app",
    required=True
)

args = parser.parse_args()

# get metadata command
if args.cmd == 'meta':
    app_name = args.name
else:
    app_name = "WiiVNC"


class MetadataWindow(gui.ui_meta.Ui_Metadata, QMainWindow):
    def __init__(self):
        super(MetadataWindow, self).__init__()
        self.ui = gui.ui_meta.Ui_Metadata()
        self.ui.setupUi(self)
        self.setWindowTitle("bruh")
        self.populate_lineedits()

    def populate_lineedits(self):
        info = metadata.dictionary(app_name)
        self.ui.appname.setText(info.get("display_name"))
        self.ui.version.setText(info.get("version"))
        self.ui.contributors.setText(info.get("contributors"))
        self.ui.developer.setText(info.get("coder"))
        self.ui.FileNameLineEdit.setText(app_name + ".zip")
        self.ui.DownloadAppBtn.clicked.connect(self.download_button)

    def download_button(self):
        output = self.ui.FileNameLineEdit.text()
        window.close()
        download.get(app_name=app_name, output=output)


if __name__ == "__main__":
    app = QApplication()
    window = MetadataWindow()
    window.show()
    app.exec_()


#class Metadata(QtWidgets.QWidget):
#    def __init__(self):
#        super().__init__()
#        self.setWindowTitle("Metadata")
#        self.setIcon()
#
#        info = metadata.dictionary(app_name)
#        info.get("version")
#
#        self.name = QtWidgets.QLabel("Display Name: "+info.get("display_name"))
#        self.version = QtWidgets.QLabel("Version: "+info.get("version"))
#        self.coder = QtWidgets.QLabel("Coder: "+info.get("coder"))
#        self.contributors = QtWidgets.QLabel("Contributors: " + info.get("contributors"))
#
#        # load icon image
#        #icon = QtGui.QPixmap(metadata.icon(app_name))
#        #label = QtWidgets.QLabel()
#        #label.setPixmap(icon)
#        #label.show()
#
#        self.layout = QtWidgets.QVBoxLayout()
#        self.layout.addWidget(self.name)
#        self.layout.addWidget(self.version)
#        self.layout.addWidget(self.coder)
#        self.layout.addWidget(self.contributors)
#        #self.layout.addWidget(label)
#
#        self.setLayout(self.layout)
#
#    def setIcon(self):
#        appIcon = QIcon("oscicon.ico")
#        self.setWindowIcon(appIcon)
#
#
#if __name__ == "__main__":
#    app = QtWidgets.QApplication([])
#
#    widget = Metadata()
#    widget.resize(400, 200)
#    widget.show()
#
#    sys.exit(app.exec_())
