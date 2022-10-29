# Contributions to GUIs

OSCDL's GUI is built with Qt, and designed with Qt Designer.

Do not modify the ui_.py files in this directory, they are automatically generated from the .ui files.

To build the .UI files as python classes after modifying them, run the following command:

`pyside6-uic DownloadLocationDialog.ui > ui_DownloadLocationDialog.py`
