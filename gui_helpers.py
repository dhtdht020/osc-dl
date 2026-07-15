import darkdetect
from PySide6.QtCore import QSettings, Qt

settings = QSettings("Open Shop Channel", "OSCDL")

DATASENT = False
CURRENTLY_SENDING = False
IN_DOWNLOAD_DIALOG = False

PLATFORM_DEFAULT_QT_STYLE = None

def apply_theme(app):
    """Applies the theme from settings: "light", "dark" or "system" (default)."""
    theme = settings.value("theme", "system")
    dark = theme == "dark" or (theme == "system" and darkdetect.isDark())

    # The default Windows style doesn't support dark mode, Fusion does
    if dark:
        app.setStyle("fusion")
    elif PLATFORM_DEFAULT_QT_STYLE:
        app.setStyle(PLATFORM_DEFAULT_QT_STYLE)

    if theme == "dark":
        app.styleHints().setColorScheme(Qt.ColorScheme.Dark)
    elif theme == "light":
        app.styleHints().setColorScheme(Qt.ColorScheme.Light)
    else:
        app.styleHints().setColorScheme(Qt.ColorScheme.Unknown)
