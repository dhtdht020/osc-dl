from PySide6.QtCore import QSettings

settings = QSettings("Open Shop Channel", "OSCDL")

DATASENT = False
CURRENTLY_SENDING = False
IN_DOWNLOAD_DIALOG = False
INI_ACTION = False

MULTISELECT = []
MULTISELECT_INI = []
QUEUE_SIGNAL_COLORS = {"in queue":"#cbc845","downloaded":"#3db072","failed":"#cb5045"}
IS_IMPORTED_FILE = False
PUT_IN_ORDER = True
        


