from PySide6.QtCore import QSettings, Qt

settings = QSettings("Open Shop Channel", "OSCDL")

DATASENT = False
CURRENTLY_SENDING = False
IN_DOWNLOAD_DIALOG = False

PLATFORM_DEFAULT_QT_STYLE = None

def apply_theme(app):
    """Applies set theme from settings"""
    theme = settings.value("theme", "system")

    if theme == "dark":
        app.styleHints().setColorScheme(Qt.ColorScheme.Dark)
    elif theme == "light":
        app.styleHints().setColorScheme(Qt.ColorScheme.Light)
    else:
        app.styleHints().setColorScheme(Qt.ColorScheme.Unknown)

    # Default Windows style doesn't support dark mode, so we use Fusion
    if app.styleHints().colorScheme() == Qt.ColorScheme.Dark:
        app.setStyle("fusion")
    elif PLATFORM_DEFAULT_QT_STYLE:
        app.setStyle(PLATFORM_DEFAULT_QT_STYLE)
