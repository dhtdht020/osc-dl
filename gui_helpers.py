from PySide6.QtCore import QSettings

settings = QSettings("Open Shop Channel", "OSCDL")

DATASENT = False
CURRENTLY_SENDING = False
IN_DOWNLOAD_DIALOG = False

MULTISELECT = []
QUEUE_SIGNAL_COLORS = {"in queue":"#cbc845","downloaded":"#3db072"}
        


