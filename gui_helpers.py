from PySide6.QtCore import QSettings

settings = QSettings("Open Shop Channel", "OSCDL")

DATASENT = False
CURRENTLY_SENDING = False
IN_DOWNLOAD_DIALOG = False

MULTISELECT = []
MULTISELECT_SIGNAL_COLORS = {
    "notselected": "#000000FF",
    "in queue": "#cbc845",
    "downloaded": "#3db072",
    "failed": "#cb5045"
}
MULTISELECT_SIGNAL_CACHE = {}
