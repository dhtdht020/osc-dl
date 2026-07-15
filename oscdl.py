# Entry point for OSCDL's GUI
import logging

import updater

if __name__ == "__main__":
    import sys
    import traceback

    from PySide6 import QtGui
    from PySide6.QtWidgets import QApplication, QDialog, QDialogButtonBox, QLabel, \
        QPlainTextEdit, QSplashScreen, QVBoxLayout

    import gui_helpers
    import utils
    import xosc_dl

    # Actions to perform only when the program is frozen:
    if updater.is_frozen() or utils.is_test("debug"):
        logging.basicConfig(level=logging.DEBUG)
        logging.info(f"Open Shop Channel Downloader v{updater.current_version()}")
        logging.info(f"OSCDL, Open Source Software by dhtdht020. https://github.com/dhtdht020.\n\n\n")
        logging.getLogger("PIL.PngImagePlugin").setLevel(logging.CRITICAL + 1) # Hide annoying spam from PIL

    # Initialize app
    app = QApplication()

    # Display uncaught exceptions in a dialog so that we don't crash silently
    def exception_dialog(exc_type, exc_value, exc_tb):
        traceback_text = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        logging.critical(f"== Unhandled exception ==\n{traceback_text}")

        dialog = QDialog()
        dialog.setWindowTitle("Open Shop Channel Downloader - Exception")
        layout = QVBoxLayout(dialog)

        label = QLabel('A critical error occurred, please report this at '
                       '<a href="https://github.com/dhtdht020/osc-dl/issues">github.com/dhtdht020/osc-dl/issues</a>!')
        label.setOpenExternalLinks(True)
        layout.addWidget(label)

        traceback_textedit = QPlainTextEdit(traceback_text)
        traceback_textedit.setReadOnly(True)
        traceback_textedit.setFont(QtGui.QFontDatabase.systemFont(QtGui.QFontDatabase.FixedFont))
        layout.addWidget(traceback_textedit)

        buttons = QDialogButtonBox(QDialogButtonBox.Close)
        copy_button = buttons.addButton("Copy Traceback", QDialogButtonBox.ActionRole)
        copy_button.clicked.connect(lambda: QApplication.clipboard().setText(traceback_text))
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        dialog.resize(600, 400)
        dialog.exec()

    sys.excepthook = exception_dialog

    # Spare us from Qt's horrible design decisions
    if app.style().name() == "windows11":
        app.setStyle("windowsvista")

    gui_helpers.PLATFORM_DEFAULT_QT_STYLE = app.style().name()
    gui_helpers.apply_theme(app)

    # Splash
    image = QtGui.QImage(utils.resource_path("assets/gui/splash.png"))
    splash = QSplashScreen(QtGui.QPixmap(image))
    splash.show()

    main_window = xosc_dl.MainWindow(app, splash)
    main_window.show()

    sys.exit(app.exec())
