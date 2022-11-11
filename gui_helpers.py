import os
import logging
from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QMessageBox

settings = QSettings("Open Shop Channel", "OSCDL")

DATASENT = True
CURRENTLY_SENDING = False
        


