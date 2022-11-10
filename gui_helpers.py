import os
import logging
from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QMessageBox

settings = QSettings("Open Shop Channel", "OSCDL")

DATASENT = True

def sendGecko(data,conn,window,path_to_app):
    try:
        conn.send(data)
    except Exception as e:
        logging.error('Error while connecting to the HBC. Close any dialogs on HBC and try again.')
        QMessageBox.warning(window, 'Connection error',
            'Error while connecting to the HBC. Close any dialogs on HBC and try again.')
        print(f'WiiLoad: {e}')
        window.ui.progressBar.setValue(0)
        window.status_message('Error: Could not connect to the Homebrew Channel. :(')

        # delete application zip file
        os.remove(path_to_app)
        conn.close()
        DATASENT = False
        return
    DATASENT = True
        


