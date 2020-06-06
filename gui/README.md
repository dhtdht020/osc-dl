# Contributions to GUIs

OSC-DL's GUI is built with Qt, and designed with Qt Designer.

We don't have any plans to replace Qt at the moment.

To modify the UI, you should follow these guidelines:

1. Do not modify the .py files in this directory, they are python classes built directly from the .ui files.
2. You should almost always modify the .UI files with Qt Designer, to know what you are doing will fit well.
3. Populating the UI or overwriting it is only done through the xosc_dl.py file at repository root. Any changes made directly to the .py files here will be rejected.

To build the .UI files as python classes after modifying them, do the following command:

`pyside2-uic united.ui > ui_united.py`
