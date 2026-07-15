# Entry point for OSCDL's GUI
import logging

import updater

if __name__ == "__main__":
    import sys

    from PySide6 import QtGui
    from PySide6.QtWidgets import QApplication, QSplashScreen

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
