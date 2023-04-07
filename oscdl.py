# Entry point for OSCDL's GUI

if __name__ == "__main__":
    import sys
    import platform

    from PySide6 import QtGui
    from PySide6.QtWidgets import QApplication, QSplashScreen

    import utils
    import xosc_dl

    if not utils.is_test("qtdark"):
        app = QApplication()
    else:
        app = QApplication([sys.argv[0], '-platform', f'windows:darkmode={sys.argv[2]}'])

    # set windows style for macOS users
    if platform.system() == "Darwin":
        app.setStyle('Fusion')

    # Splash
    image = QtGui.QImage(utils.resource_path("assets/gui/splash.png"))
    splash = QSplashScreen(QtGui.QPixmap(image))
    splash.show()

    main_window = xosc_dl.MainWindow(app, splash)
    main_window.show()

    sys.exit(app.exec())
